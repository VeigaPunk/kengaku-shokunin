#!/usr/bin/env python3
"""Replay the captured `llm-inference-batching-scheduler` grader with its own test
functions (round 92, R92-C1).

Each case stages a declarative /app tree — the pinned input-data bytes plus the two
valid batching plans the embedded deterministic packer emits (pack6: per-shape DP
over gen-groups, p95-slot budget 36, w=1e6, v=1) — then applies the case's ops and
runs the captured test package unmodified inside a fresh bubblewrap namespace with
the case dir bound at /app and the capture bound read-only at /tests. Six legs are
observed per case, in the grader's function-definition order:

    test_output_files_exist, test_input_data_integrity, test_generate_and_schema,
    test_solution_shape_feasibility_and_batch_consistency,
    test_solution_coverage_no_duplicates, test_performance_thresholds

    P  the function returned without raising
    F  the function raised AssertionError (a graded refusal)
    E  the function raised anything else (an uncaught error surfacing instead of a
       verdict, e.g. FileNotFoundError on a removed file)

No assertion is reimplemented and no open call is patched. The grader's verdicts
travel on a single PAYLOAD line. The host /app is never written: the case directory
is the bind source and lives under --work. Every host probe (git, openssl, userns)
is guarded: an absent tool degrades the stamp instead of crashing the counter.

Usage:  python3 plans/round92_bs_probe.py --lane <repo> --work <scratch dir>
Writes the receipt (stamp block plus observation block) to stdout.
Exit:   0 predicate pass, 1 a case observed != predicted, 2 setup defect.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

CAP = "corpus/evidence/round92/graders/llm-inference-batching-scheduler"
INPUT1 = "corpus/evidence/round92/graders/llm-inference-batching-scheduler/environment/task_file/input_data/requests_bucket_1.jsonl"
INPUT2 = "corpus/evidence/round92/graders/llm-inference-batching-scheduler/environment/task_file/input_data/requests_bucket_2.jsonl"
TABLE = "plans/round92-cases.json"
TOOL = "plans/round92_bs_probe.py"
MEMBER = "llm-inference-batching-scheduler"
HEADER = "# tb2 llm-inference-batching-scheduler grader probe"
SUBJECT_SHA = "80b06b7c4ba0db28832b767d48be74bb462d7f5df5798d9cb58c4f1160d96ffa"
INPUT1_SHA = "8b3cf1e2b06074162038064dd2c114abe308acd32cec7d365ee63ee81978f7de"
INPUT2_SHA = "e15e2d4c4d55f875c42a6042610d6282f6c0657c39d3e0d0f087268252525cb5"
TESTS = ("test_output_files_exist", "test_input_data_integrity", "test_generate_and_schema",
         "test_solution_shape_feasibility_and_batch_consistency",
         "test_solution_coverage_no_duplicates", "test_performance_thresholds")
BWRAP = "/usr/bin/bwrap"
CASE_TIMEOUT = 240
SHAPES_1 = [64, 128, 512, 1088, 2048]
SHAPES_2 = [192, 320, 704]

HARNESS = r"""
import sys, traceback
sys.path.insert(0, "/tmp")
import tests.test_outputs as mod
out, classes = [], []
for name in ({TESTNAMES}):
    try:
        getattr(mod, name)()
        out.append("P")
        classes.append("%s=ok" % name)
    except AssertionError as exc:
        out.append("F")
        classes.append("%s=AssertionError" % name)
    except Exception as exc:
        out.append("E")
        classes.append("%s=%s" % (name, type(exc).__name__))
print("PAYLOAD " + "".join(out))
print("CLASSES " + ",".join(classes))
""".format(TESTNAMES=repr(TESTS))


# ---------------------------------------------------------------- packer (pack6)
def _align(x: int, g: int = 64) -> int:
    return ((x + g - 1) // g) * g


def _decode_lat(s: int, g: int) -> float:
    return sum(0.0012 * (s + i) ** 2 + 2.45 * (s + i) for i in range(g))


def _wall(s: int, g: int) -> float:
    return (_decode_lat(s, g) + 0.002 * s * s + 0.0015 * s * 4096 + 8.0
            + 1500.0)


def _series_cost(s: int, d: int) -> float:
    return sum((s + i) ** 2 + 2048 * (s + i) for i in range(d))


def _dp_shape(groups, s, w, v, slots_max, lim):
    n = len(groups)
    gens = [g for g, _ in groups]
    ns = [len(m) for _, m in groups]
    lat = [_decode_lat(s, g) + 0.002 * s * s + 0.0015 * s * 4096 + 8.0 + 1500.0
           for g in gens]
    best = {(0, 0): (0.0, -1)}
    for i in range(1, n + 1):
        for j in range(0, i):
            pad = sum(ns[t] * (gens[i - 1] - gens[t]) for t in range(j, i))
            cost = 1.0e7 + sum(ns[t] * _series_cost(s, gens[i - 1] - gens[t])
                               for t in range(j, i))
            slots = sum(ns[t] for t in range(j, i)) if lat[i - 1] > lim else 0
            val = _wall(s, gens[i - 1]) + w * pad + v * cost
            for k in range(0, slots_max + 1):
                prev = best.get((j, k - slots))
                if prev is None:
                    continue
                cand = prev[0] + val
                key = (i, k)
                if key not in best or cand < best[key][0]:
                    best[key] = (cand, j)
    end = min(((v0, k) for (i, k), (v0, _) in best.items() if i == n),
              default=(float("inf"), 0))
    _, k = end
    intervals, i, kk = [], n, k
    while i > 0:
        j = best[(i, kk)][1]
        slots = sum(ns[t] for t in range(j, i)) if lat[i - 1] > lim else 0
        intervals.append([r for t in range(j, i) for r in groups[t][1]])
        i, kk = j, kk - slots
    return intervals


def build_plans(reqs: list[dict], shapes: list[int], bucket: int) -> list[dict]:
    """pack6 with the frozen parameters: w=1e6, v=1, slot budget 36."""
    lim = {1: 2.1e6, 2: 2.1e5}[bucket]
    w, v, slots = 1.0e6, 1.0, 36
    by_shape: dict[int, list[dict]] = {s: [] for s in shapes}
    for r in reqs:
        a = _align(r["prompt_len"])
        for s in shapes:
            if a <= s:
                by_shape[s].append(r)
                break
        else:
            raise RuntimeError("no shape covers %s" % r["request_id"])
    plan: list[dict] = []
    bid = 0
    for s in shapes:
        groups: dict[int, list[dict]] = {}
        for r in by_shape[s]:
            groups.setdefault(r["gen_len"], []).append(r)
        gsorted = [(g, groups[g]) for g in sorted(groups)]
        for members in _dp_shape(gsorted, s, w, v, slots, lim):
            bid += 1
            plan.extend({
                "request_id": r["request_id"],
                "batch_id": "b%04d" % bid,
                "shape": {"seq_align": s, "heads_align": 32, "hidden_align": 4096},
            } for r in members)
    return plan


# ---------------------------------------------------------------- probe mechanics
def stamp(lane: Path, work: Path) -> dict:
    def sh(*args: str) -> str:
        try:
            proc = subprocess.run(args, capture_output=True, text=True, timeout=60)
        except (OSError, subprocess.SubprocessError):
            return "absent"
        return (proc.stdout or proc.stderr).strip().splitlines()[0] if (proc.stdout or proc.stderr).strip() else "absent"

    tip = sh("git", "-C", str(lane), "rev-parse", "HEAD")
    dirty = sh("git", "-C", str(lane), "status", "--porcelain")
    py = subprocess.run([sys.executable, "-V"], capture_output=True, text=True)
    try:
        oss = subprocess.run(["openssl", "version"], capture_output=True, text=True, timeout=60)
        oss_line = (oss.stdout or "").strip().splitlines()[0] if (oss.stdout or "").strip() else "absent"
    except (OSError, subprocess.SubprocessError):
        oss_line = "absent"
    try:
        userns = Path("/proc/sys/user/max_user_namespaces").read_text().strip()
    except OSError:
        userns = "absent"
    return {
        "MEMBER": MEMBER,
        "SUBJECT_CAPTURE": CAP + "/tests/test_outputs.py",
        "SUBJECT_SHA": SUBJECT_SHA,
        "INPUT_DATA_SHA": "%s %s" % (INPUT1_SHA[:12], INPUT2_SHA[:12]),
        "CASE_TABLE_SHA": hashlib.sha256((lane / TABLE).read_bytes()).hexdigest(),
        "TOOL": TOOL,
        "TOOL_SHA": hashlib.sha256(Path(__file__).resolve().read_bytes()).hexdigest(),
        "HOST_PYTHON": (py.stderr or py.stdout).strip().splitlines()[0],
        "HOST_OPENSSL": oss_line,
        "HOST_USERNS": userns,
        "LANE_TIP": tip,
        "WORKTREE": "clean" if dirty == "" else "dirty",
        "COMMAND": "python3 %s --lane %s --work %s" % (TOOL, lane, work),
    }


def stage_case(case: dict, case_dir: Path, req1: bytes, req2: bytes) -> Path:
    app = case_dir / "app"
    tf = app / "task_file"
    (tf / "input_data").mkdir(parents=True, exist_ok=True)
    (tf / "output_data").mkdir(parents=True, exist_ok=True)
    (tf / "input_data" / "requests_bucket_1.jsonl").write_bytes(req1)
    (tf / "input_data" / "requests_bucket_2.jsonl").write_bytes(req2)
    for b, req in ((1, req1), (2, req2)):
        reqs = [json.loads(line) for line in req.decode().splitlines()]
        plan = build_plans(reqs, SHAPES_1 if b == 1 else SHAPES_2, b)
        (tf / "output_data" / ("plan_b%d.jsonl" % b)).write_text(
            "".join(json.dumps(p) + "\n" for p in plan), encoding="utf-8")
    for op in case.get("ops", []):
        kind = op[0]
        if kind == "rm":
            (app / "task_file" / op[1]).unlink()
        elif kind == "truncate":
            p = app / "task_file" / op[1]
            p.write_text("", encoding="utf-8")
        elif kind == "inline-append-line1":
            p = app / "task_file" / op[1]
            text = p.read_text(encoding="utf-8")
            head, _, rest = text.partition("\n")
            p.write_text(head + op[2] + "\n" + rest, encoding="utf-8")
        elif kind == "dup-first-line":
            p = app / "task_file" / op[1]
            lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
            p.write_text(lines[0] + "".join(lines), encoding="utf-8")
        elif kind == "set-field-first-line":
            p = app / "task_file" / op[1]
            obj = json.loads(p.read_text(encoding="utf-8").splitlines()[0])
            field, value = op[2], op[3]
            mod = obj
            parts = field.split(".")
            for part in parts[:-1]:
                mod = mod[part]
            mod[parts[-1]] = value
            lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
            lines[0] = json.dumps(obj) + "\n"
            p.write_text("".join(lines), encoding="utf-8")
        elif kind == "shift-field-line2":
            p = app / "task_file" / op[1]
            lines = p.read_text(encoding="utf-8").splitlines()
            obj = json.loads(lines[1])
            field = op[2].split(".")
            obj[field[0]][field[1]] = obj[field[0]][field[1]] + op[3]
            lines[1] = json.dumps(obj)
            p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        else:
            raise RuntimeError("unknown op %r" % kind)
    return app


def run_case(case: dict, case_dir: Path, cap_dir: Path, req1: bytes, req2: bytes) -> tuple[str, str]:
    app = stage_case(case, case_dir, req1, req2)
    cmd = [BWRAP, "--die-with-parent", "--unshare-net", "--dev-bind", "/", "/",
           "--bind", str(app), "/app",
           "--tmpfs", "/tmp",
           "--ro-bind", str(cap_dir / "tests"), "/tmp/tests",
           sys.executable, "-I", "-B", "-c", HARNESS]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=CASE_TIMEOUT)
    payload = None
    classes = ""
    for line in proc.stdout.splitlines():
        if line.startswith("PAYLOAD "):
            payload = line.split()[1]
        elif line.startswith("CLASSES "):
            classes = line[len("CLASSES "):]
    if payload is None or len(payload) != len(TESTS):
        raise RuntimeError("no payload rc=%s stderr=%s" % (proc.returncode, proc.stderr.strip()[-200:]))
    return payload, classes


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=".")
    parser.add_argument("--work", required=True)
    args = parser.parse_args(argv)
    lane = Path(args.lane).resolve()
    work = Path(args.work).resolve()
    work.mkdir(parents=True, exist_ok=True)

    if not Path(BWRAP).exists():
        print("DEFECT SETUP sandbox-unavailable %s" % BWRAP)
        print("PREDICATE R92-PROBE could-not-evaluate")
        return 2
    table_path = lane / TABLE
    cap_dir = lane / CAP
    if not table_path.is_file():
        print("DEFECT SETUP unreadable %s" % TABLE)
        print("PREDICATE R92-PROBE could-not-evaluate")
        return 2
    need = {
        "tests/test_outputs.py": SUBJECT_SHA,
        "environment/task_file/input_data/requests_bucket_1.jsonl": INPUT1_SHA,
        "environment/task_file/input_data/requests_bucket_2.jsonl": INPUT2_SHA,
    }
    for rel, want in need.items():
        p = cap_dir / rel
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != want:
            print("DEFECT SETUP capture-sha mismatch %s" % rel)
            print("PREDICATE R92-PROBE could-not-evaluate")
            return 2

    req1 = (cap_dir / "environment/task_file/input_data/requests_bucket_1.jsonl").read_bytes()
    req2 = (cap_dir / "environment/task_file/input_data/requests_bucket_2.jsonl").read_bytes()
    table = json.loads(table_path.read_text(encoding="utf-8"))

    info = stamp(lane, work)
    rows, mismatches, defect = [], 0, None
    for case in table["cases"]:
        case_dir = work / "cases" / case["id"]
        try:
            observed, classes = run_case(case, case_dir, cap_dir, req1, req2)
        except Exception as exc:  # noqa: BLE001 - the probe reports, it does not pass
            defect = "case-run-failed %s %r" % (case["id"], exc)
            break
        ok = observed == case["predicted"]
        if not ok:
            mismatches += 1
        rows.append("CASE %s predicted=%s observed=%s ok=%s %s"
                    % (case["id"], case["predicted"], observed, ok, classes))
    legs = len(rows) * len(TESTS)
    print(HEADER)
    for key, value in info.items():
        print("%s %s" % (key, value))
    print("CASES %d LEGS %d (cases x %d functions)" % (len(table["cases"]), legs, len(TESTS)))
    print("OBSERVATIONS_BEGIN")
    for row in rows:
        print(row)
    print("OBSERVATIONS_END")
    if defect:
        print("DEFECT %s" % defect)
    print("mismatches=%d" % mismatches)
    passed = defect is None and mismatches == 0 and len(rows) == len(table["cases"])
    print("PREDICATE R92-PROBE %s" % ("pass" if passed else "fail"))
    return 0 if passed else (2 if defect and defect.startswith("setup") else 1)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

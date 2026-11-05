#!/usr/bin/env python3
"""Replay the captured `modernize-scientific-stack` grader with its own test functions (round 91, R91-C1).

Each case stages the frozen fixture from `plans/round91-cases.json` — a declarative /app tree
(script, CSV, optional dependency file; paths in `absent` are not staged) — then runs the captured
module unmodified inside a fresh bubblewrap namespace with the case dir bound at /app. Two legs are
observed per case, in the grader's function-definition order:

    test_modernized_code_runs, test_dependency_file_exists

    P  the function returned without raising
    F  the function raised AssertionError (a graded refusal)
    E  the function raised anything else (an uncaught error surfacing instead of a verdict,
       here subprocess.TimeoutExpired from the grader's own timeout=30 in the script-hangs case)

No assertion is reimplemented and no subprocess or open call is patched. The grader's verdicts
travel on a single PAYLOAD line. The host /app is never written: the case directory is the bind
source and lives under --work.

Usage:  python3 plans/round91_modernize_probe.py --lane <repo> --work <scratch dir>
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

CAP = "corpus/evidence/round52/graders/modernize-scientific-stack/tests/test_outputs.py"
TABLE = "plans/round91-cases.json"
TOOL = "plans/round91_modernize_probe.py"
MEMBER = "modernize-scientific-stack"
HEADER = "# tb2 modernize-scientific-stack grader probe"
SUBJECT_SHA = "0c24195ff46527764c7f8ceda9c608a189ab4a01619282942fcd27a2ea02a977"
TESTS = ("test_modernized_code_runs", "test_dependency_file_exists")
BWRAP = "/usr/bin/bwrap"
CASE_TIMEOUT = 120

HARNESS = r'''
import sys, types, importlib.util
sys.modules['pytest'] = types.ModuleType('pytest')
spec = importlib.util.spec_from_file_location('subject91', sys.argv[1])
module = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(module)
except Exception as exc:
    print('PAYLOAD XX')
    print('CLASSES modload=%s' % type(exc).__name__)
    sys.exit(0)
out, classes = [], []
for name in ('test_modernized_code_runs', 'test_dependency_file_exists'):
    try:
        getattr(module, name)()
        out.append('P')
        classes.append('%s=ok' % name)
    except AssertionError as exc:
        out.append('F')
        classes.append('%s=AssertionError' % name)
    except Exception as exc:
        out.append('E')
        classes.append('%s=%s' % (name, type(exc).__name__))
print('PAYLOAD ' + ''.join(out))
print('CLASSES ' + ','.join(classes))
'''


def stamp(lane: Path, work: Path) -> dict:
    def sh(*args: str) -> str:
        return subprocess.run(args, capture_output=True, text=True, timeout=60).stdout.strip()
    tip = sh("git", "-C", str(lane), "rev-parse", "HEAD")
    dirty = len(sh("git", "-C", str(lane), "status", "--porcelain").splitlines())
    py = subprocess.run([sys.executable, "-V"], capture_output=True, text=True)
    oss = subprocess.run(["openssl", "version"], capture_output=True, text=True)
    userns = Path("/proc/sys/user/max_user_namespaces").read_text().strip()
    return {
        "MEMBER": MEMBER,
        "SUBJECT_CAPTURE": CAP,
        "SUBJECT_SHA": SUBJECT_SHA,
        "CASE_TABLE_SHA": hashlib.sha256((lane / TABLE).read_bytes()).hexdigest(),
        "TOOL": TOOL,
        "TOOL_SHA": hashlib.sha256(Path(__file__).resolve().read_bytes()).hexdigest(),
        "HOST_PYTHON": (py.stderr or py.stdout).strip().splitlines()[0],
        "HOST_OPENSSL": (oss.stdout or oss.stderr).strip().splitlines()[0] if (oss.stdout or oss.stderr).strip() else "absent",
        "HOST_USERNS": userns,
        "LANE_TIP": tip,
        "WORKTREE": "clean" if dirty == 0 else f"dirty:{dirty}",
        "COMMAND": "python3 %s --lane %s --work %s" % (TOOL, lane, work),
    }


def run_case(case: dict, case_dir: Path, cap_bytes: bytes) -> tuple[str, str]:
    app = case_dir / "app"
    app.mkdir(parents=True, exist_ok=True)
    absent = set(case["result"].get("absent", []))
    for rel, content in case["result"]["files"].items():
        if rel in absent:
            continue
        target = app / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    cap_file = case_dir / "subject_test_outputs.py"
    cap_file.write_bytes(cap_bytes)
    cmd = [BWRAP, "--die-with-parent", "--unshare-net", "--dev-bind", "/", "/",
           "--bind", str(app), "/app", "--tmpfs", "/tmp",
           sys.executable, "-I", "-B", "-c", HARNESS, str(cap_file)]
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
        print("PREDICATE R91-PROBE could-not-evaluate")
        return 2
    table_path = lane / TABLE
    cap_path = lane / CAP
    if not table_path.is_file():
        print("DEFECT SETUP unreadable %s" % TABLE)
        print("PREDICATE R91-PROBE could-not-evaluate")
        return 2
    if not cap_path.is_file():
        print("DEFECT SETUP unreadable %s" % CAP)
        print("PREDICATE R91-PROBE could-not-evaluate")
        return 2
    table = json.loads(table_path.read_text(encoding="utf-8"))
    cap_bytes = cap_path.read_bytes()
    if hashlib.sha256(cap_bytes).hexdigest() != SUBJECT_SHA:
        print("DEFECT SETUP subject-sha mismatch")
        print("PREDICATE R91-PROBE could-not-evaluate")
        return 2

    info = stamp(lane, work)
    rows, mismatches, defect = [], 0, None
    for case in table["cases"]:
        case_dir = work / "cases" / case["id"]
        try:
            observed, classes = run_case(case, case_dir, cap_bytes)
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
    print("PREDICATE R91-PROBE %s" % ("pass" if passed else "fail"))
    return 0 if passed else (2 if defect and defect.startswith("setup") else 1)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

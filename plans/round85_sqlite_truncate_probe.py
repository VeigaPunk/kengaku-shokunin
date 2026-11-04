#!/usr/bin/env python3
"""Replay the frozen sqlite-db-truncate capture with the grader's own test function.

Each case stages a real `/app/recover.json` from the frozen case table and runs the
captured module unmodified inside a fresh bubblewrap namespace.  Two legs are observed
per case: `score` (the set-intersection cardinality computed by a harness that imports
the grader's own `soln` list) and `verdict` (the real `test_json_data()` return, where
AssertionError or FileNotFoundError is F and any other exception is a setup defect).
No assertion is reimplemented, no `open`/`json` is patched, and the host `/app` is
never written.

The stamp block mirrors the round-83/84 receipt grammar.  TOOL names the instrument at
its frozen install path and TOOL_SHA pins the bytes actually executed, so a stamp
minted from any other copy is falsified by the digest.  COMMAND is the reconstructed
canonical argv and is never executed from the receipt.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import platform
import shlex
import ssl
import subprocess
import sys
import tempfile
from pathlib import Path

CAP = "corpus/evidence/round52/graders/sqlite-db-truncate/tests/test_outputs.py"
TABLE = "plans/round85-cases.json"
MEMBER = "sqlite-db-truncate"
HEADER = "# tb2 sqlite-db-truncate grader probe"
SUBJECT_SHA = "8f5bc11018687d8c5894ebf1b4ec6fad004828e5ce442d3cc04d925ef53ef881"
TESTS = ("test_json_data",)
BWRAP = "/usr/bin/bwrap"
FROZEN_TABLE_SHA = "bd98794b9d35168ccb296ad9176cf45b0b421cf961515935a814eadc40d49114"
FROZEN_CASES = (
    # (id, predicted score, predicted verdict)
    ("exact8", 8, "P"),
    ("seven", 7, "P"),
    ("six", 6, "F"),
    ("empty", 0, "F"),
    ("extras", 8, "P"),
    ("duplicates", 8, "P"),
    ("string-values", 0, "F"),
    ("int-values", 6, "F"),
)
REQUIRED = ("MEMBER", "SUBJECT_CAPTURE", "SUBJECT_SHA", "CASE_TABLE_SHA", "TOOL",
            "TOOL_SHA", "HOST_PYTHON", "HOST_OPENSSL", "LANE_TIP", "WORKTREE",
            "COMMAND", "EXIT")

HARNESS = '''import ast, json, runpy
from pathlib import Path
path = "/tests/test_outputs.py"
names = [node.name for node in ast.parse(Path(path).read_bytes()).body
         if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]
module = runpy.run_path(path)
soln = {(item["word"], item["value"]) for item in module["soln"]}
data = {(item["word"], item["value"]) for item in json.loads(Path("/app/recover.json").read_text())}
score = len(soln & data)
results = []
for name in names:
    try:
        module[name]()
    except (AssertionError, FileNotFoundError) as error:
        results.append([name, "F", type(error).__name__])
    except BaseException as error:
        results.append([name, "D", type(error).__name__])
    else:
        results.append([name, "P", ""])
print(json.dumps({"score": score, "tests": results}))
'''


class SetupDefect(Exception):
    """The frozen replay could not be evaluated."""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tool_label(lane: Path) -> str:
    tool = Path(__file__).resolve()
    try:
        return tool.relative_to(lane).as_posix()
    except ValueError:
        return str(tool)


def git_out(lane: Path, *args: str) -> str | None:
    try:
        proc = subprocess.run(["git", "-C", str(lane), *args], capture_output=True,
                              text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    return proc.stdout.strip() if proc.returncode == 0 else None


def lane_tip(lane: Path) -> str:
    return git_out(lane, "rev-parse", "master") or "absent"


def worktree_state(lane: Path) -> str:
    status = git_out(lane, "status", "--porcelain")
    if status is None:
        return "absent"
    return "dirty" if status else "clean"


def host_openssl() -> str:
    try:
        proc = subprocess.run(["openssl", "version"], capture_output=True, text=True,
                              timeout=30, env={"PATH": "/usr/bin"})
        if proc.returncode == 0 and proc.stdout.strip().startswith("OpenSSL"):
            return proc.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return ssl.OPENSSL_VERSION


def reference_score(capture: bytes, case: dict) -> int:
    """Independent recompute of the intersection from the grader's literal `soln`."""
    tree = ast.parse(capture)
    soln: list | None = None
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == "soln"):
            soln = ast.literal_eval(node.value)
    if soln is None:
        raise SetupDefect("capture-has-no-soln-literal")
    left = {(item["word"], item["value"]) for item in soln}
    right = {(item["word"], item["value"]) for item in case["data"]}
    return len(left & right)


def load_inputs(lane: Path) -> tuple[bytes, bytes, list[dict]]:
    capture_path = lane / CAP
    try:
        capture = capture_path.read_bytes()
    except OSError as error:
        raise SetupDefect(f"no-subject {CAP}") from error
    if sha256(capture) != SUBJECT_SHA:
        raise SetupDefect(f"wrong-subject sha={sha256(capture)[:16]}")
    canonical = lane / TABLE
    path = canonical if canonical.is_file() else Path(__file__).resolve().parent / "round85-cases.json"
    try:
        table_bytes = path.read_bytes()
        doc = json.loads(table_bytes)
    except (OSError, json.JSONDecodeError) as error:
        raise SetupDefect(f"no-table {path}") from error
    if canonical.is_file() and sha256(table_bytes) != FROZEN_TABLE_SHA:
        raise SetupDefect(f"wrong-table sha={sha256(table_bytes)[:16]}")
    if not isinstance(doc, dict) or doc.get("member") != MEMBER:
        raise SetupDefect("wrong-table member")
    cases = doc.get("cases")
    if not isinstance(cases, list) or len(cases) != len(FROZEN_CASES):
        raise SetupDefect("wrong-table case-count")
    for case, (case_id, score, verdict) in zip(cases, FROZEN_CASES):
        if not isinstance(case, dict) or case.get("id") != case_id:
            raise SetupDefect(f"wrong-table case-order {case_id}")
        if case.get("predicted_score") != score or case.get("predicted_verdict") != verdict:
            raise SetupDefect(f"wrong-table predicted {case_id}")
        if not isinstance(case.get("data"), list) or not all(
                isinstance(row, dict) and "word" in row and "value" in row for row in case["data"]):
            raise SetupDefect(f"wrong-table data {case_id}")
        if reference_score(capture, case) != score:
            raise SetupDefect(f"wrong-table score {case_id} reference={reference_score(capture, case)}")
    names = tuple(node.name for node in ast.parse(capture).body
                  if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"))
    if names != TESTS:
        raise SetupDefect(f"test-order {names}")
    return capture, table_bytes, cases


def sandbox_argv(capture: Path, case_dir: Path) -> list[str]:
    argv = [BWRAP, "--unshare-all", "--die-with-parent", "--new-session",
            "--ro-bind", "/usr", "/usr", "--ro-bind", "/etc", "/etc"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            argv += ["--symlink", os.readlink(link), link]
    argv += ["--proc", "/proc", "--dev", "/dev",
             "--bind", str(case_dir / "app"), "/app", "--dir", "/tests",
             "--ro-bind", str(capture), "/tests/test_outputs.py",
             "--ro-bind", str(case_dir / "harness.py"), "/harness.py",
             "--clearenv", "--setenv", "PATH", "/usr/bin",
             "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
             "--chdir", "/app", "/usr/bin/python3", "-I", "-B", "/harness.py"]
    return argv


def run_case(capture: Path, work: Path, data: list[dict]) -> dict:
    if not os.access(BWRAP, os.X_OK):
        raise SetupDefect(f"no-bwrap {BWRAP}")
    with tempfile.TemporaryDirectory(prefix="case-", dir=work) as temp:
        case_dir = Path(temp)
        (case_dir / "app").mkdir()
        (case_dir / "app/recover.json").write_text(
            json.dumps(data, indent=2) + "\n", encoding="utf-8")
        (case_dir / "harness.py").write_text(HARNESS, encoding="utf-8")
        proc = subprocess.run(sandbox_argv(capture, case_dir), capture_output=True,
                              text=True, timeout=60, env={"PATH": "/usr/bin"})
        if proc.returncode != 0:
            raise SetupDefect(f"sandbox-exit={proc.returncode} "
                              f"stderr={proc.stderr.strip()!r}")
        try:
            payload = json.loads(proc.stdout)
        except json.JSONDecodeError as error:
            raise SetupDefect("sandbox-protocol") from error
        if (not isinstance(payload, dict) or not isinstance(payload.get("score"), int)
                or not isinstance(payload.get("tests"), list)
                or tuple(row[0] for row in payload["tests"]) != TESTS
                or any(row[1] not in ("P", "F", "D") for row in payload["tests"])):
            raise SetupDefect("sandbox-protocol")
        return payload


def replay(lane: Path, work: Path) -> tuple[bytes, bytes, list[str], int]:
    capture, table_bytes, cases = load_inputs(lane)
    observations: list[str] = []
    mismatches = 0
    # Execute a snapshot of the checked bytes, avoiding a lane-file mutation race.
    with tempfile.TemporaryDirectory(prefix="capture-", dir=work) as temp:
        staged = Path(temp) / "test_outputs.py"
        staged.write_bytes(capture)
        for case in cases:
            payload = run_case(staged, work, case["data"])
            defects = [f"{row[0]}:{row[2]}" for row in payload["tests"] if row[1] == "D"]
            if defects:
                raise SetupDefect(f"case={case['id']} unexpected-exception={','.join(defects)}")
            observed = f"{payload['score']}/" + "/".join(row[1] for row in payload["tests"])
            predicted = f"{case['predicted_score']}/{case['predicted_verdict']}"
            mismatches += observed != predicted
            observations.append(
                f"CASE {case['id']} predicted={predicted} observed={observed}")
    legs = 2 * len(cases)
    observations.append(f"cases={len(cases)} legs={legs} mismatches={mismatches}")
    observations.append(f"PREDICATE R85-PROBE {'fail' if mismatches else 'pass'}")
    return capture, table_bytes, observations, (1 if mismatches else 0)


def stamp(lane: Path, work: Path, capture: bytes, table_bytes: bytes, code: int) -> list[str]:
    command = shlex.join(["python3", tool_label(lane), "--lane", ".", "--work", str(work)])
    return [
        f"MEMBER {MEMBER}",
        f"SUBJECT_CAPTURE {CAP}",
        f"SUBJECT_SHA {sha256(capture)}",
        f"CASE_TABLE_SHA {sha256(table_bytes)}",
        f"TOOL {tool_label(lane)}",
        f"TOOL_SHA {sha256(Path(__file__).resolve().read_bytes())}",
        f"HOST_PYTHON Python {platform.python_version()}",
        f"HOST_OPENSSL {host_openssl()}",
        f"LANE_TIP {lane_tip(lane)}",
        f"WORKTREE {worktree_state(lane)}",
        f"COMMAND {command}",
        f"EXIT {code}",
    ]


def render(lines: list[str], observations: list[str]) -> str:
    return "\n".join(lines + ["OBSERVATIONS_BEGIN"] + observations + ["OBSERVATIONS_END", ""])


def selftest(lane: Path, work: Path) -> int:
    failures = 0
    checks = 0

    def check(identifier: str, good: bool) -> None:
        nonlocal failures, checks
        failures += not good
        checks += 1
        print(f"SELFTEST {identifier} {'pass' if good else 'FAIL'}")

    capture, table_bytes, cases = load_inputs(lane)
    check("frozen-table", sha256(table_bytes) == FROZEN_TABLE_SHA
          and tuple((c["id"], c["predicted_score"], c["predicted_verdict"]) for c in cases) == FROZEN_CASES)
    check("reference-score-agrees", all(reference_score(capture, c) == c["predicted_score"] for c in cases))

    def mutated(**changes) -> tuple[bytes, bytes]:
        doc = json.loads(json.dumps(json.loads(table_bytes)))
        for case in doc["cases"]:
            if case["id"] == changes.get("case_id", "exact8"):
                for key, value in changes.items():
                    if key != "case_id":
                        case[key] = value
        table = (json.dumps(doc, indent=2) + "\n").encode()
        root = work / f"fixture-{checks}"
        (root / CAP).parent.mkdir(parents=True, exist_ok=True)
        (root / CAP).write_bytes(capture)
        (root / TABLE).parent.mkdir(parents=True, exist_ok=True)
        (root / TABLE).write_bytes(table)
        return table, root

    def invoke(root: Path) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, "-I", "-B", str(Path(__file__).resolve()),
                               "--lane", str(root), "--work", str(work / "selftest-work")],
                              capture_output=True, text=True, timeout=600,
                              env={"PATH": "/usr/bin", "TMPDIR": str(work)})

    table, root = mutated(case_id="exact8", predicted_score=7)
    proc = invoke(root)
    check("mutant-score-rejected", proc.returncode == 2 and "wrong-table predicted" in proc.stdout + proc.stderr)
    table, root = mutated(case_id="empty", data=[{"word": "testword02", "value": 10.0}])
    proc = invoke(root)
    check("mutant-data-rejected", proc.returncode == 2 and "wrong-table score" in proc.stdout + proc.stderr)
    _, root = mutated()
    proc = invoke(root)
    check("fixture-replays-green", proc.returncode == 0 and "PREDICATE R85-PROBE pass" in proc.stdout)
    proc = subprocess.run([sys.executable, "-I", "-B", str(Path(__file__).resolve()),
                           "--lane", str(lane), "--work", str(work / "selftest-work")],
                          capture_output=True, text=True, timeout=600,
                          env={"PATH": "/usr/bin", "TMPDIR": str(work)})
    check("lane-replays-green", proc.returncode == 0 and "cases=8 legs=16 mismatches=0" in proc.stdout)
    proc = subprocess.run([sys.executable, "-I", "-B", str(Path(__file__).resolve()),
                           "--lane", str(work / "absent"), "--work", str(work / "selftest-work")],
                          capture_output=True, text=True, timeout=600,
                          env={"PATH": "/usr/bin", "TMPDIR": str(work)})
    check("absent-lane-exit-2", proc.returncode == 2)

    print(f"SELFTEST cases={checks} failures={failures}")
    return 0 if failures == 0 else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lane", default=".")
    parser.add_argument("--work", required=True)
    parser.add_argument("--receipt")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    lane = Path(args.lane).resolve()
    work = Path(args.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    if args.selftest:
        return selftest(lane, work)
    try:
        capture, table_bytes, observations, code = replay(lane, work)
    except SetupDefect as error:
        print(f"DEFECT SETUP {error}")
        print("PREDICATE R85-PROBE fail")
        return 2
    text = render(stamp(lane, work, capture, table_bytes, code), observations)
    if args.receipt:
        target = Path(args.receipt)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return code


if __name__ == "__main__":
    sys.exit(main())

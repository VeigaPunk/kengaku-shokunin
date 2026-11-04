#!/usr/bin/env python3
"""Replay the frozen code-from-image capture, not the image or an agent solution.

Each case uses a fresh bubblewrap namespace and real UTF-8 /app/output.txt.
Only AssertionError and FileNotFoundError count as F; infrastructure or other
exceptions are setup defects (exit 2). Exit 1 means a prediction mismatch.
Use --lane DIR --work DIR; --selftest exercises the actual CLI and sandbox.
No receipt is minted here: integration must pin the landed tool and clean tip.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

CAP = "corpus/evidence/round52/graders/code-from-image/tests/test_outputs.py"
TABLE = "plans/round83-cases.json"
SUBJECT_SHA = "b9b7cb0033116df88a4807404bf309190f92d62a89df2ce64cdcbf732efe084a"
CASE_TABLE_SHA = "e64dac129dcb8fea5f7068c67f6c81482e4a0755f1509ae9f358348e6f3e9aec"
TESTS = ("test_output_file_exists", "test_output_is_correct")
BWRAP = "/usr/bin/bwrap"

# Discover the definitions from the executed capture, retaining source order.
# Catch each test separately: failure of the first never skips the second.
HARNESS = '''import ast, json, runpy
from pathlib import Path
path = "/tests/test_outputs.py"
names = [node.name for node in ast.parse(Path(path).read_bytes()).body
         if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]
module = runpy.run_path(path)
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
print(json.dumps(results))
'''


class SetupDefect(Exception):
    """The frozen replay could not be evaluated."""


def load_inputs(lane: Path) -> tuple[bytes, list[dict]]:
    capture = (lane / CAP).read_bytes()
    table = (lane / TABLE).read_bytes()
    if hashlib.sha256(capture).hexdigest() != SUBJECT_SHA:
        raise SetupDefect("wrong-subject")
    if hashlib.sha256(table).hexdigest() != CASE_TABLE_SHA:
        raise SetupDefect("wrong-table")
    names = tuple(node.name for node in ast.parse(capture).body
                  if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"))
    if names != TESTS:
        raise SetupDefect("test-order")
    return capture, json.loads(table)["cases"]


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


def run_case(capture: Path, work: Path, content: str | None) -> list[list[str]]:
    with tempfile.TemporaryDirectory(prefix="case-", dir=work) as temp:
        case_dir = Path(temp)
        (case_dir / "app").mkdir()
        if content is not None:
            (case_dir / "app/output.txt").write_bytes(content.encode("utf-8"))
        (case_dir / "harness.py").write_text(HARNESS, encoding="utf-8")
        proc = subprocess.run(sandbox_argv(capture, case_dir), capture_output=True,
                              text=True, timeout=60, env={"PATH": "/usr/bin"})
        if proc.returncode != 0:
            raise SetupDefect(f"sandbox-exit={proc.returncode} stderr={proc.stderr.strip()!r}")
        try:
            results = json.loads(proc.stdout)
        except json.JSONDecodeError as error:
            raise SetupDefect("sandbox-protocol") from error
        if (not isinstance(results, list) or len(results) != len(TESTS)
                or any(not isinstance(row, list) or len(row) != 3 for row in results)
                or tuple(row[0] for row in results) != TESTS
                or any(row[1] not in ("P", "F", "D") for row in results)):
            raise SetupDefect("sandbox-protocol")
        return results


def replay(lane: Path, work: Path) -> int:
    capture, cases = load_inputs(lane)
    # Execute a snapshot of the checked bytes, avoiding a lane-file mutation race.
    with tempfile.TemporaryDirectory(prefix="capture-", dir=work) as temp:
        staged = Path(temp) / "test_outputs.py"
        staged.write_bytes(capture)
        mismatches = 0
        for case in cases:
            results = run_case(staged, work, case["content"])
            defects = [f"{name}:{error}" for name, verdict, error in results if verdict == "D"]
            if defects:
                raise SetupDefect(f"case={case['id']} unexpected-exception={','.join(defects)}")
            observed = "/".join(row[1] for row in results)
            mismatches += observed != case["predicted"]
            print(f"CASE {case['id']} predicted={case['predicted']} observed={observed}")
    print(f"cases={len(cases)} mismatches={mismatches}")
    print(f"PREDICATE R83-PROBE {'fail' if mismatches else 'pass'}")
    return 1 if mismatches else 0


def selftest(lane: Path, work: Path) -> int:
    capture, cases = load_inputs(lane)
    failures = 0

    def check(identifier: str, good: bool) -> None:
        nonlocal failures
        failures += not good
        print(f"SELFTEST {identifier} {'pass' if good else 'FAIL'}")

    def invoke(root: Path, identifier: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "-I", "-B", str(Path(__file__).resolve()),
             "--lane", str(root), "--work", str(work / identifier)],
            capture_output=True, text=True, timeout=180,
            env={"PATH": "/usr/bin", "TMPDIR": str(work)})

    green = invoke(lane, "green")
    expected = [f"CASE {case['id']} predicted={case['predicted']} observed={case['predicted']}"
                for case in cases]
    check("invocation", green.returncode == 0
          and green.stdout.splitlines() == ["# tb2 code-from-image grader probe", *expected,
                                           "cases=8 mismatches=0", "PREDICATE R83-PROBE pass"])
    with tempfile.TemporaryDirectory(prefix="selftest-", dir=work) as temp:
        fixture = Path(temp)
        (fixture / CAP).parent.mkdir(parents=True)
        (fixture / TABLE).parent.mkdir(parents=True)
        (fixture / CAP).write_bytes(capture + b"\n")
        (fixture / TABLE).write_bytes((lane / TABLE).read_bytes())
        wrong_subject = invoke(fixture, "wrong-subject")
        check("wrong-subject", wrong_subject.returncode == 2
              and "SETUP wrong-subject" in wrong_subject.stdout)
        (fixture / CAP).write_bytes(capture)
        (fixture / TABLE).write_bytes((lane / TABLE).read_bytes() + b"\n")
        wrong_table = invoke(fixture, "wrong-table")
        check("wrong-table", wrong_table.returncode == 2
              and "SETUP wrong-table" in wrong_table.stdout)
        # Fixture modules exercise classification/continuation, not grader substitutes.
        for identifier, first, second, wanted in (
            ("assertion-independent-order", "raise AssertionError()", "return", ["F", "P"]),
            ("file-not-found", "raise FileNotFoundError()", "return", ["F", "P"]),
            ("unexpected-exception", "raise ValueError()", "return", ["D", "P"]),
        ):
            module = fixture / "fixture.py"
            module.write_text(f"def {TESTS[0]}():\n    {first}\n"
                              f"def {TESTS[1]}():\n    {second}\n", encoding="utf-8")
            result = run_case(module, work, None)
            check(identifier, [row[1] for row in result] == wanted)
    print(f"SELFTEST cases=6 failures={failures}")
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lane", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    print("# tb2 code-from-image grader probe")
    try:
        lane = args.lane.resolve()
        work = args.work.resolve()
        work.mkdir(parents=True, exist_ok=True)
        os.environ["TMPDIR"] = str(work)
        if args.selftest:
            return selftest(lane, work)
        return replay(lane, work)
    except (SetupDefect, OSError, subprocess.SubprocessError, ValueError) as error:
        print(f"SETUP {error}")
        print("PREDICATE R83-PROBE could-not-evaluate")
        return 2


if __name__ == "__main__":
    sys.exit(main())

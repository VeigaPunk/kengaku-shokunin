#!/usr/bin/env python3
"""Replay the frozen gcode-to-text capture with the grader's own two test legs.

Each case runs in a fresh bubblewrap namespace against a real UTF-8 /app/out.txt
staged from the frozen case table; the captured module is never modified, patched,
substituted or reimplemented.  Only AssertionError and FileNotFoundError count as F,
a normal return is P, and any other exception is a setup defect (exit 2, never a
witness).  Exit 1 means an observed vector differs from the frozen prediction.

The stamp block mirrors the round-83 receipt grammar.  TOOL names the instrument at
its frozen install path and TOOL_SHA pins the bytes actually executed, so a stamp
minted from any other copy is falsified by the digest.  COMMAND is the reconstructed
canonical argv and is never executed from the receipt.

The case table resolves to <lane>/plans/round84-cases.json when present (the file the
counter pins by sha256); otherwise the copy shipped beside this tool is used and must
be byte-identical to the frozen table.  Rows are data: ids, order and predicted
vectors are checked against the frozen claim, staged content is what the case stages,
so a drifted staging row is reported as a mismatch rather than silently re-frozen.
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

CAP = "corpus/evidence/round52/graders/gcode-to-text/tests/test_outputs.py"
TABLE = "plans/round84-cases.json"
MEMBER = "gcode-to-text"
HEADER = "# tb2 gcode-to-text grader probe"
SUBJECT_SHA = "6b049dc626aa103b20d165552e5cb39ba02c6803b04ba06a43d79435b5f701a6"
SUBJECT_PIN = "6b049dc626aa103b"
TESTS = ("test_hello_file_exists", "test_hello_file_content")
BWRAP = "/usr/bin/bwrap"
FROZEN_TABLE_SHA = "5b86f8d7efc24a529b4c53a23c6a4ccaed51866428535e6f0fcb4dbf13982cb5"
FLAG = "flag{gc0d3_iz_ch4LLenGiNg}"
FROZEN_CASES = (
    ("missing", None, "F/F"),
    ("empty", "", "P/F"),
    ("exact", FLAG, "P/P"),
    ("padded", " \n" + FLAG + "\t\n", "P/P"),
    ("uppercase", "FLAG{GC0D3_IZ_CH4LLENGING}", "P/F"),
    ("suffix", FLAG + "x", "P/F"),
    ("prefix-only", "flag{gc0d3_iz_", "P/F"),
    ("wrong-flag", "flag{gc0d3_iz_ch4LLenGiNx}", "P/F"),
)
REQUIRED = ("MEMBER", "SUBJECT_CAPTURE", "SUBJECT_SHA", "CASE_TABLE_SHA", "TOOL",
            "TOOL_SHA", "HOST_PYTHON", "HOST_OPENSSL", "LANE_TIP", "WORKTREE",
            "COMMAND", "EXIT")

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


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tool_label(lane: Path) -> str:
    tool = Path(__file__).resolve()
    try:
        return tool.relative_to(lane).as_posix()
    except ValueError:
        return str(tool)


def table_path(lane: Path) -> tuple[Path, bool]:
    canonical = lane / TABLE
    if canonical.is_file():
        return canonical, True
    return Path(__file__).resolve().parent / "round84-cases.json", False


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


def load_inputs(lane: Path) -> tuple[bytes, bytes, list[dict]]:
    capture = (lane / CAP).read_bytes()
    if sha256(capture) != SUBJECT_SHA:
        raise SetupDefect(f"wrong-subject sha={sha256(capture)[:16]} pin={SUBJECT_PIN}")
    path, canonical = table_path(lane)
    try:
        table_bytes = path.read_bytes()
        doc = json.loads(table_bytes)
    except OSError as error:
        raise SetupDefect(f"no-table {path}") from error
    if not canonical and sha256(table_bytes) != FROZEN_TABLE_SHA:
        raise SetupDefect(f"wrong-table sha={sha256(table_bytes)[:16]} "
                          f"frozen={FROZEN_TABLE_SHA[:16]}")
    if not isinstance(doc, dict) or doc.get("member") != MEMBER:
        raise SetupDefect("wrong-table member")
    cases = doc.get("cases")
    if not isinstance(cases, list) or len(cases) != len(FROZEN_CASES):
        raise SetupDefect("wrong-table case-count")
    for case, (case_id, _, predicted) in zip(cases, FROZEN_CASES):
        if not isinstance(case, dict) or case.get("id") != case_id:
            raise SetupDefect(f"wrong-table case-order {case_id}")
        if case.get("predicted") != predicted:
            raise SetupDefect(f"wrong-table predicted {case_id} "
                              f"{case.get('predicted')!r} != {predicted!r}")
        if not (case.get("content") is None or isinstance(case.get("content"), str)):
            raise SetupDefect(f"wrong-table content {case_id}")
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


def run_case(capture: Path, work: Path, content: str | None) -> list[list[str]]:
    if not os.access(BWRAP, os.X_OK):
        raise SetupDefect(f"no-bwrap {BWRAP}")
    with tempfile.TemporaryDirectory(prefix="case-", dir=work) as temp:
        case_dir = Path(temp)
        (case_dir / "app").mkdir()
        if content is not None:
            (case_dir / "app/out.txt").write_bytes(content.encode("utf-8"))
        (case_dir / "harness.py").write_text(HARNESS, encoding="utf-8")
        proc = subprocess.run(sandbox_argv(capture, case_dir), capture_output=True,
                              text=True, timeout=60, env={"PATH": "/usr/bin"})
        if proc.returncode != 0:
            raise SetupDefect(f"sandbox-exit={proc.returncode} "
                              f"stderr={proc.stderr.strip()!r}")
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


def replay(lane: Path, work: Path) -> tuple[bytes, bytes, list[str], int]:
    capture, table_bytes, cases = load_inputs(lane)
    observations: list[str] = []
    mismatches = 0
    # Execute a snapshot of the checked bytes, avoiding a lane-file mutation race.
    with tempfile.TemporaryDirectory(prefix="capture-", dir=work) as temp:
        staged = Path(temp) / "test_outputs.py"
        staged.write_bytes(capture)
        for case in cases:
            results = run_case(staged, work, case["content"])
            defects = [f"{name}:{error}" for name, verdict, error in results
                       if verdict == "D"]
            if defects:
                raise SetupDefect(f"case={case['id']} "
                                  f"unexpected-exception={','.join(defects)}")
            observed = "/".join(row[1] for row in results)
            mismatches += observed != case["predicted"]
            observations.append(
                f"CASE {case['id']} predicted={case['predicted']} observed={observed}")
    observations.append(f"cases={len(cases)} mismatches={mismatches}")
    observations.append(f"PREDICATE R84-PROBE {'fail' if mismatches else 'pass'}")
    return capture, table_bytes, observations, (1 if mismatches else 0)


def emit(lane: Path, work: Path, capture: bytes, table_bytes: bytes,
         observations: list[str], code: int) -> None:
    command = shlex.join(["python3", tool_label(lane), "--lane", ".", "--work", str(work)])
    print(f"MEMBER {MEMBER}")
    print(f"SUBJECT_CAPTURE {CAP}")
    print(f"SUBJECT_SHA {sha256(capture)}")
    print(f"CASE_TABLE_SHA {sha256(table_bytes)}")
    print(f"TOOL {tool_label(lane)}")
    print(f"TOOL_SHA {sha256(Path(__file__).resolve().read_bytes())}")
    print(f"HOST_PYTHON Python {platform.python_version()}")
    print(f"HOST_OPENSSL {host_openssl()}")
    print(f"LANE_TIP {lane_tip(lane)}")
    print(f"WORKTREE {worktree_state(lane)}")
    print(f"COMMAND {command}")
    print(f"EXIT {code}")
    print("OBSERVATIONS_BEGIN")
    for line in observations:
        print(line)
    print("OBSERVATIONS_END")


def selftest(lane: Path, work: Path) -> int:
    capture, table_bytes, cases = load_inputs(lane)
    failures = 0
    checks = 0

    def check(identifier: str, good: bool) -> None:
        nonlocal failures, checks
        failures += not good
        checks += 1
        print(f"SELFTEST {identifier} {'pass' if good else 'FAIL'}")

    def invoke(root: Path, identifier: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "-I", "-B", str(Path(__file__).resolve()),
             "--lane", str(root), "--work", str(work / identifier)],
            capture_output=True, text=True, timeout=300,
            env={"PATH": "/usr/bin", "TMPDIR": str(work)})

    def fixture(root: Path, subject: bytes, table: bytes) -> None:
        (root / CAP).parent.mkdir(parents=True, exist_ok=True)
        (root / CAP).write_bytes(subject)
        (root / TABLE).parent.mkdir(parents=True, exist_ok=True)
        (root / TABLE).write_bytes(table)

    def mutated(*, case_id: str, **fields) -> bytes:
        doc = json.loads(json.dumps(json.loads(table_bytes)))
        for case in doc["cases"]:
            if case["id"] == case_id:
                case.update(fields)
        return (json.dumps(doc, indent=2) + "\n").encode("utf-8")

    check("frozen-table",
          sha256(table_bytes) == FROZEN_TABLE_SHA
          and tuple((c["id"], c["content"], c["predicted"]) for c in cases) == FROZEN_CASES)

    host_app_before = os.path.lexists("/app")
    green = invoke(lane, "green")
    lines = green.stdout.splitlines()
    check("no-host-app", host_app_before or not os.path.lexists("/app"))
    check("invocation-exit", green.returncode == 0)
    check("invocation-header", lines[:1] == [HEADER])
    stamp: dict[str, str] = {}
    order: list[str] = []
    for line in lines[1:]:
        if line.startswith("OBSERVATIONS_BEGIN"):
            break
        key, _, value = line.partition(" ")
        stamp[key] = value
        order.append(key)
    check("stamp-order", order == list(REQUIRED))
    check("stamp-values",
          stamp.get("MEMBER") == MEMBER
          and stamp.get("SUBJECT_CAPTURE") == CAP
          and stamp.get("SUBJECT_SHA") == SUBJECT_SHA
          and stamp.get("CASE_TABLE_SHA") == sha256(table_bytes)
          and stamp.get("TOOL") == tool_label(lane)
          and stamp.get("TOOL_SHA") == sha256(Path(__file__).resolve().read_bytes())
          and stamp.get("HOST_PYTHON", "").startswith("Python ")
          and stamp.get("HOST_OPENSSL", "").startswith("OpenSSL")
          and stamp.get("LANE_TIP") == lane_tip(lane)
          and stamp.get("WORKTREE") == worktree_state(lane)
          and stamp.get("COMMAND") == shlex.join(
              ["python3", tool_label(lane), "--lane", ".", "--work", str(work / "green")])
          and stamp.get("EXIT") == "0")
    if "OBSERVATIONS_BEGIN" in lines and "OBSERVATIONS_END" in lines:
        block = lines[lines.index("OBSERVATIONS_BEGIN") + 1:lines.index("OBSERVATIONS_END")]
    else:
        block = []
    expected = [f"CASE {case['id']} predicted={case['predicted']} observed={case['predicted']}"
                for case in cases]
    check("observations",
          block == expected + ["cases=8 mismatches=0", "PREDICATE R84-PROBE pass"])

    with tempfile.TemporaryDirectory(prefix="selftest-", dir=work) as temp:
        base = Path(temp)
        wrong_subject = base / "wrong-subject"
        fixture(wrong_subject, capture + b"\n", table_bytes)
        result = invoke(wrong_subject, "wrong-subject")
        check("wrong-subject", result.returncode == 2
              and "SETUP wrong-subject" in result.stdout
              and "PREDICATE R84-PROBE could-not-evaluate" in result.stdout)

        wrong_predicted = base / "wrong-predicted"
        fixture(wrong_predicted, capture,
                mutated(case_id="missing", predicted="P/P"))
        result = invoke(wrong_predicted, "wrong-predicted")
        check("wrong-predicted", result.returncode == 2
              and "SETUP wrong-table predicted missing" in result.stdout)

        drift = base / "content-drift"
        fixture(drift, capture, mutated(case_id="empty", content=FLAG))
        result = invoke(drift, "content-drift")
        check("content-drift", result.returncode == 1
              and "CASE empty predicted=P/F observed=P/P" in result.stdout
              and "cases=8 mismatches=1" in result.stdout
              and "PREDICATE R84-PROBE fail" in result.stdout
              and f"CASE_TABLE_SHA {FROZEN_TABLE_SHA}" not in result.stdout)

        # Fixture modules exercise classification/continuation, not grader substitutes.
        for identifier, first, second, wanted in (
            ("assertion-independent-order", "raise AssertionError()", "return", ["F", "P"]),
            ("file-not-found", "raise FileNotFoundError()", "return", ["F", "P"]),
            ("unexpected-exception", "raise ValueError()", "return", ["D", "P"]),
        ):
            module = base / f"{identifier}.py"
            module.write_text(f"def {TESTS[0]}():\n    {first}\n\n"
                              f"def {TESTS[1]}():\n    {second}\n", encoding="utf-8")
            result_rows = run_case(module, work, None)
            check(identifier, [row[1] for row in result_rows] == wanted)

    print(f"SELFTEST cases={checks} failures={failures}")
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lane", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    print(HEADER)
    try:
        lane = args.lane.resolve()
        work = args.work.resolve()
        work.mkdir(parents=True, exist_ok=True)
        os.environ["TMPDIR"] = str(work)
        if args.selftest:
            return selftest(lane, work)
        capture, table_bytes, observations, code = replay(lane, work)
        emit(lane, work, capture, table_bytes, observations, code)
        return code
    except (SetupDefect, OSError, subprocess.SubprocessError, ValueError) as error:
        print(f"SETUP {error}")
        print("PREDICATE R84-PROBE could-not-evaluate")
        return 2


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Replay the captured `mteb-retrieve` grader with its own test functions (round 87, R87-C1).

Each case stages a `/app/result.txt` from the frozen case table (text, absent, directory or raw bytes)
and runs the captured module unmodified inside a fresh bubblewrap namespace. Two legs are observed per
case, one per captured `test_` function, in source order:

    P  the function returned without raising
    F  the function raised AssertionError or FileNotFoundError (a graded refusal)
    E  the function raised anything else (an uncaught error surfacing instead of a verdict)

No assertion is reimplemented and no `open`/`os.path` is patched. The host `/app` is never written.
COMMAND in the stamp is the reconstructed canonical argv and is never executed from the receipt.

Usage:  python3 plans/round87_mteb_probe.py --lane <repo> --work <scratch dir>
Writes the receipt (stamp block plus observation block) to stdout.
Exit:   0 predicate pass, 1 a case observed != predicted, 2 setup defect (could not evaluate).
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

CAP = "corpus/evidence/round52/graders/mteb-retrieve/tests/test_outputs.py"
TABLE = "plans/round87-cases.json"
TOOL = "plans/round87_mteb_probe.py"
MEMBER = "mteb-retrieve"
HEADER = "# tb2 mteb-retrieve grader probe"
SUBJECT_SHA = "e4e6b21fed6662adb4a42aba23d35609450392839a2282f3ba77c70c8d907c0b"
TESTS = ("test_result_exists", "test_data_matches")
BWRAP = "/usr/bin/bwrap"
FROZEN_CASES = (
    ("exact", "P/P"),
    ("absent-file", "F/F"),
    ("two-lines", "P/F"),
    ("sibling-value", "P/F"),
    ("trailing-space", "P/P"),
    ("empty-file", "P/F"),
    ("result-is-directory", "P/E"),
    ("non-utf8-bytes", "P/E"),
)
REQUIRED = ("MEMBER", "SUBJECT_CAPTURE", "SUBJECT_SHA", "CASE_TABLE_SHA", "TOOL", "TOOL_SHA",
            "HOST_PYTHON", "HOST_OPENSSL", "LANE_TIP", "WORKTREE", "COMMAND", "EXIT")

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
        results.append([name, "E", type(error).__name__])
    else:
        results.append([name, "P", ""])
print(json.dumps({"tests": results}))
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


def load_inputs(lane: Path) -> tuple[bytes, bytes, list[dict]]:
    capture_path = lane / CAP
    try:
        capture = capture_path.read_bytes()
    except OSError as error:
        raise SetupDefect(f"no-subject {CAP}") from error
    if sha256(capture) != SUBJECT_SHA:
        raise SetupDefect(f"wrong-subject sha={sha256(capture)[:16]}")
    try:
        table_bytes = (lane / TABLE).read_bytes()
        doc = json.loads(table_bytes)
    except (OSError, json.JSONDecodeError) as error:
        raise SetupDefect(f"no-table {TABLE}") from error
    if not isinstance(doc, dict) or doc.get("member") != MEMBER:
        raise SetupDefect("wrong-table member")
    if doc.get("subject_sha") != SUBJECT_SHA and doc.get("subject_sha") is not None:
        raise SetupDefect("wrong-table subject")
    if tuple(doc.get("legs") or ()) != TESTS:
        raise SetupDefect("wrong-table legs")
    cases = doc.get("cases")
    if not isinstance(cases, list) or len(cases) != len(FROZEN_CASES):
        raise SetupDefect("wrong-table case-count")
    for case, (case_id, predicted) in zip(cases, FROZEN_CASES):
        if not isinstance(case, dict) or case.get("id") != case_id:
            raise SetupDefect(f"wrong-table case-order {case_id}")
        if case.get("predicted") != predicted:
            raise SetupDefect(f"wrong-table predicted {case_id}")
        if not isinstance(case.get("result"), dict):
            raise SetupDefect(f"wrong-table result {case_id}")
    names = tuple(node.name for node in ast.parse(capture).body
                  if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"))
    if names != TESTS:
        raise SetupDefect(f"test-order {names}")
    return capture, table_bytes, cases


def stage(app: Path, spec: dict) -> None:
    kind = spec.get("kind")
    if kind == "absent":
        return
    target = app / "result.txt"
    if kind == "dir":
        target.mkdir()
    elif kind == "text":
        target.write_bytes(spec["content"].encode("utf-8"))
    elif kind == "bytes_hex":
        target.write_bytes(bytes.fromhex(spec["hex"]))
    else:
        raise SetupDefect(f"wrong-table result-kind {kind}")


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


def run_case(capture: Path, work: Path, result: dict) -> dict:
    if not os.access(BWRAP, os.X_OK):
        raise SetupDefect(f"no-bwrap {BWRAP}")
    with tempfile.TemporaryDirectory(prefix="case-", dir=work) as temp:
        case_dir = Path(temp)
        (case_dir / "app").mkdir()
        stage(case_dir / "app", result)
        (case_dir / "harness.py").write_text(HARNESS, encoding="utf-8")
        proc = subprocess.run(sandbox_argv(capture, case_dir), capture_output=True,
                              text=True, timeout=60, env={"PATH": "/usr/bin"})
        if proc.returncode != 0:
            raise SetupDefect(f"sandbox-exit={proc.returncode} stderr={proc.stderr.strip()!r}")
        try:
            payload = json.loads(proc.stdout)
        except json.JSONDecodeError as error:
            raise SetupDefect("sandbox-protocol") from error
        if (not isinstance(payload, dict) or not isinstance(payload.get("tests"), list)
                or tuple(row[0] for row in payload["tests"]) != TESTS
                or any(row[1] not in ("P", "F", "E") for row in payload["tests"])):
            raise SetupDefect("sandbox-protocol")
        return payload


def replay(lane: Path, work: Path) -> tuple[bytes, bytes, list[str], int]:
    capture, table_bytes, cases = load_inputs(lane)
    observations: list[str] = []
    mismatches = 0
    with tempfile.TemporaryDirectory(prefix="capture-", dir=work) as temp:
        staged = Path(temp) / "test_outputs.py"
        staged.write_bytes(capture)
        for case in cases:
            payload = run_case(staged, work, case["result"])
            observed = "/".join(row[1] for row in payload["tests"])
            predicted = case["predicted"]
            mismatches += observed != predicted
            observations.append(f"CASE {case['id']} predicted={predicted} observed={observed}")
    legs = len(TESTS) * len(cases)
    observations.append(f"cases={len(cases)} legs={legs} mismatches={mismatches}")
    observations.append(f"PREDICATE R87-PROBE {'fail' if mismatches else 'pass'}")
    return capture, table_bytes, observations, (1 if mismatches else 0)


def stamp(lane: Path, work: Path, capture: bytes, table_bytes: bytes, code: int) -> list[str]:
    command = shlex.join(["python3", tool_label(lane), "--lane", ".", "--work", str(work)])
    return [
        HEADER,
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


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=".", help="repository root holding the frozen inputs")
    parser.add_argument("--work", required=True, help="scratch directory (never /tmp for large trees)")
    args = parser.parse_args(argv)
    lane = Path(args.lane).resolve()
    work = Path(args.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    try:
        capture, table_bytes, observations, code = replay(lane, work)
    except SetupDefect as defect:
        print(f"DEFECT SETUP {defect}")
        print("PREDICATE R87-PROBE setup-defect")
        return 2
    lines = stamp(lane, work, capture, table_bytes, code) + ["OBSERVATIONS_BEGIN"] + observations
    lines += ["OBSERVATIONS_END", ""]
    sys.stdout.write("\n".join(lines))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

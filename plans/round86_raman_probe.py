#!/usr/bin/env python3
"""Replay the frozen `raman-fitting` capture with the grader's own test functions.

Each case stages a real `/app/results.json` (or none at all) from the frozen case table and
runs the captured module unmodified inside a fresh bubblewrap namespace.  Three legs are
observed per case, one per captured `test_` function, in source order:

    P  the function returned without raising
    F  the function raised AssertionError or FileNotFoundError (a graded refusal)
    E  the function raised anything else (a schema violation surfacing as an uncaught
       error instead of a graded refusal)

`E` is an observation, not a setup defect: the case class this round adds is schema drift,
and the whole point of the class is which schema violations the grader turns into a verdict
and which it turns into a traceback.  Only a sandbox that cannot run at all is a setup defect.

No assertion is reimplemented and no `open`/`json` is patched.  The host `/app` is never
written.  The stamp block mirrors the round-83/84/85 receipt grammar; TOOL_SHA pins the bytes
actually executed, so a stamp minted from any other copy is contradicted by the digest.
COMMAND is the reconstructed canonical argv and is never executed from the receipt.
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

CAP = "corpus/evidence/round52/graders/raman-fitting/tests/test_outputs.py"
TABLE = "plans/round86-cases.json"
MEMBER = "raman-fitting"
HEADER = "# tb2 raman-fitting grader probe"
SUBJECT_SHA = "171fae772ccf262aec8ddac5bd2c6c731eed842421f5d8439a330b158c9f8c13"
TESTS = ("test_result_file_exists", "test_G_Peak", "test_2D_Peak")
BWRAP = "/usr/bin/bwrap"
FROZEN_TABLE_SHA = "f8aa21f3b3f6ccf9616f9d54e9b6aa2c8482de1f32fadbb33166713c6b2210a4"
FROZEN_CASES = (
    # (id, predicted vector over the three legs in source order)
    ("exact", "P/P/P"),
    ("missing-2D-key", "P/P/E"),
    ("g-amplitude-string", "P/E/P"),
    ("extra-schema-keys", "P/P/P"),
    ("absent-file", "F/F/F"),
    ("g-key-renamed", "P/E/P"),
    ("2D-null-value", "P/P/E"),
    ("g-amplitude-just-outside", "P/F/P"),
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
    canonical = lane / TABLE
    path = canonical if canonical.is_file() else Path(__file__).resolve().parent / "round86-cases.json"
    try:
        table_bytes = path.read_bytes()
        doc = json.loads(table_bytes)
    except (OSError, json.JSONDecodeError) as error:
        raise SetupDefect(f"no-table {path}") from error
    if canonical.is_file() and sha256(table_bytes) != FROZEN_TABLE_SHA:
        raise SetupDefect(f"wrong-table sha={sha256(table_bytes)[:16]}")
    if not isinstance(doc, dict) or doc.get("member") != MEMBER:
        raise SetupDefect("wrong-table member")
    if doc.get("subject_sha") != SUBJECT_SHA:
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
        if "results" not in case:
            raise SetupDefect(f"wrong-table results {case_id}")
        if case["results"] is not None and not isinstance(case["results"], dict):
            raise SetupDefect(f"wrong-table results-type {case_id}")
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


def run_case(capture: Path, work: Path, results: dict | None) -> dict:
    if not os.access(BWRAP, os.X_OK):
        raise SetupDefect(f"no-bwrap {BWRAP}")
    with tempfile.TemporaryDirectory(prefix="case-", dir=work) as temp:
        case_dir = Path(temp)
        (case_dir / "app").mkdir()
        if results is not None:
            (case_dir / "app/results.json").write_text(
                json.dumps(results, indent=2) + "\n", encoding="utf-8")
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
            payload = run_case(staged, work, case["results"])
            observed = "/".join(row[1] for row in payload["tests"])
            predicted = case["predicted"]
            mismatches += observed != predicted
            observations.append(f"CASE {case['id']} predicted={predicted} observed={observed}")
    legs = len(TESTS) * len(cases)
    observations.append(f"cases={len(cases)} legs={legs} mismatches={mismatches}")
    observations.append(f"PREDICATE R86-PROBE {'fail' if mismatches else 'pass'}")
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
          and tuple((c["id"], c["predicted"]) for c in cases) == FROZEN_CASES)

    def invoke(root: Path) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, "-I", "-B", str(Path(__file__).resolve()),
                               "--lane", str(root), "--work", str(work / "selftest-work")],
                              capture_output=True, text=True, timeout=900,
                              env={"PATH": "/usr/bin", "TMPDIR": str(work)})

    def fixture(mutate) -> Path:
        doc = json.loads(json.dumps(json.loads(table_bytes)))
        mutate(doc)
        root = work / f"fixture-{checks}"
        (root / CAP).parent.mkdir(parents=True, exist_ok=True)
        (root / CAP).write_bytes(capture)
        (root / TABLE).parent.mkdir(parents=True, exist_ok=True)
        (root / TABLE).write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
        return root

    def wrong_prediction(doc: dict) -> None:
        doc["cases"][0]["predicted"] = "P/F/P"

    proc = invoke(fixture(wrong_prediction))
    check("mutant-prediction-rejected",
          proc.returncode == 2 and "wrong-table predicted" in proc.stdout + proc.stderr)

    def wrong_data(doc: dict) -> None:
        # a data mutation the frozen prediction cannot cover: G.x0 leaves its absolute band
        doc["cases"][0]["results"]["G"]["x0"] = 1600.0

    proc = invoke(fixture(wrong_data))
    check("mutant-data-flips-predicate",
          proc.returncode == 1 and "mismatches=1" in proc.stdout
          and "PREDICATE R86-PROBE fail" in proc.stdout)

    def missing_legs(doc: dict) -> None:
        doc["legs"] = ["test_G_Peak"]

    proc = invoke(fixture(missing_legs))
    check("mutant-legs-rejected",
          proc.returncode == 2 and "wrong-table legs" in proc.stdout + proc.stderr)

    proc = subprocess.run([sys.executable, "-I", "-B", str(Path(__file__).resolve()),
                           "--lane", str(lane), "--work", str(work / "selftest-work")],
                          capture_output=True, text=True, timeout=900,
                          env={"PATH": "/usr/bin", "TMPDIR": str(work)})
    check("lane-replays-green",
          proc.returncode == 0 and "cases=8 legs=24 mismatches=0" in proc.stdout)

    proc = subprocess.run([sys.executable, "-I", "-B", str(Path(__file__).resolve()),
                           "--lane", str(work / "absent"), "--work", str(work / "selftest-work")],
                          capture_output=True, text=True, timeout=900,
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
        print("PREDICATE R86-PROBE fail")
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

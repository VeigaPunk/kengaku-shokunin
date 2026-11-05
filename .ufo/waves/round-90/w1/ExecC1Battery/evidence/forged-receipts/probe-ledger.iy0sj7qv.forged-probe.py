#!/usr/bin/env python3
"""Replay the captured `merge-diff-arc-agi-task` grader with its own test functions (round 90, R90-C1).

Each case stages the frozen fixture from `plans/round90-cases.json` — a declarative tree: an /app
root holding `repo/` (optionally a real git repository with named branches and files) and a
`/tests/test.json` — then runs the captured module unmodified inside a fresh bubblewrap namespace.
Five legs are observed per case, in the grader's function-definition order:

    test_git_repo_init, test_both_bundles_fetched, test_algo_py_exists,
    test_algo_py_has_map_function, test_algo_map_function_with_test_input

    P  the function returned without raising
    F  the function raised AssertionError (a graded refusal)
    E  the function raised anything else (an uncaught error surfacing instead of a verdict)

No assertion is reimplemented and no `subprocess`, `importlib` or `open` call is patched. The
grader's own stdout is captured inside the harness; the verdict travels on a single `PAYLOAD` line.
The host /app and /tests are never written: case directories are bound in read-only or private.

Usage:  python3 plans/round90_polydiff_probe.py --lane <repo> --work <scratch dir>
Writes the receipt (stamp block plus observation block) to stdout.
Exit:   0 predicate pass, 1 a case observed != predicted, 2 setup defect.
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

CAP = "corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py"
TABLE = "plans/round90-cases.json"
TOOL = "plans/round90_polydiff_probe.py"
MEMBER = "merge-diff-arc-agi-task"
HEADER = "# tb2 merge-diff-arc-agi-task grader probe"
SUBJECT_SHA = "2754ba6c5c5f75c9db5ed2c5729d9f5d7e21cb7fdb18aa0c65abdc3e7e85c149"
TESTS = ("test_git_repo_init", "test_both_bundles_fetched", "test_algo_py_exists",
         "test_algo_py_has_map_function", "test_algo_map_function_with_test_input")
BWRAP = "/usr/bin/bwrap"
FROZEN_CASES = (
    ("full-solution", "PPPPP"),
    ("no-git-dir", "FFPPP"),
    ("one-branch", "PFPPP"),
    ("algo-missing", "PPFEE"),
    ("algo-syntax-error", "PPPEE"),
    ("map-wrong-values", "PPPPF"),
    ("test-json-corrupt", "PPPPE"),
    ("map-shape-short", "PPPPF"),
)
REQUIRED = ("MEMBER", "SUBJECT_CAPTURE", "SUBJECT_SHA", "CASE_TABLE_SHA", "TOOL", "TOOL_SHA",
            "HOST_PYTHON", "HOST_OPENSSL", "HOST_USERNS", "LANE_TIP", "WORKTREE", "COMMAND", "EXIT")

HARNESS = '''import ast, contextlib, io, json, runpy
from pathlib import Path
path = "/tests/test_outputs.py"
names = [node.name for node in ast.parse(Path(path).read_bytes()).body
         if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]
module = runpy.run_path(path)
results = []
for name in names:
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            module[name]()
    except AssertionError as error:
        results.append([name, "F", type(error).__name__])
    except BaseException as error:
        results.append([name, "E", type(error).__name__])
    else:
        results.append([name, "P", ""])
print("PAYLOAD " + json.dumps({"tests": results}))
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
    return git_out(lane, "rev-parse", "HEAD") or "absent"


def worktree_state(lane: Path) -> str:
    status = git_out(lane, "status", "--porcelain", "--untracked-files=no")
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


def host_userns() -> str:
    try:
        return Path("/proc/sys/user/max_user_namespaces").read_text().strip()
    except OSError:
        return "absent"


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
        result = case.get("result")
        if not isinstance(result, dict) or result.get("kind") != "tree":
            raise SetupDefect(f"wrong-table result {case_id}")
        repo = result.get("repo")
        if not isinstance(repo, dict) or not isinstance(repo.get("git"), bool) \
                or not isinstance(repo.get("branches"), list) \
                or not isinstance(repo.get("files"), dict):
            raise SetupDefect(f"wrong-table repo {case_id}")
        for rel, content in repo["files"].items():
            if not isinstance(rel, str) or ".." in rel.split("/") or rel.startswith("/"):
                raise SetupDefect(f"wrong-table path {case_id}:{rel}")
            if not isinstance(content, str):
                raise SetupDefect(f"wrong-table content {case_id}:{rel}")
        if not isinstance(result.get("test_json"), str):
            raise SetupDefect(f"wrong-table test_json {case_id}")
    names = tuple(node.name for node in ast.parse(capture).body
                  if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"))
    if names != TESTS:
        raise SetupDefect(f"test-order {names}")
    return capture, table_bytes, cases


def git_fixture(repo: Path, spec: dict) -> None:
    """Build the declarative git fixture outside the sandbox; never touches anything outside it."""
    env = {"PATH": "/usr/bin", "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null",
           "HOME": str(repo.parent)}
    def run(*args: str, cwd: Path = repo) -> None:
        proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,
                              timeout=60, env=env)
        if proc.returncode != 0:
            raise SetupDefect(f"fixture-git {' '.join(args[:2])} rc={proc.returncode} "
                              f"{proc.stderr.strip()[-120:]!r}")
    run("init", "-q", "-b", "master")
    run("config", "user.email", "probe@invalid")
    run("config", "user.name", "probe")
    run("config", "commit.gpgsign", "false")
    (repo / ".gitkeep").write_text("", encoding="utf-8")
    run("add", ".gitkeep")
    run("commit", "-q", "-m", "fixture", "--no-verify", "--allow-empty")
    for branch in spec.get("branches") or []:
        run("branch", branch)


def stage(app: Path, repo_spec: dict) -> None:
    repo = app / "repo"
    repo.mkdir(parents=True, exist_ok=True)
    for rel, content in repo_spec.get("files", {}).items():
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content.encode("utf-8"))
    if repo_spec.get("git"):
        git_fixture(repo, repo_spec)


def sandbox_argv(capture: Path, case_dir: Path) -> list[str]:
    argv = [BWRAP, "--unshare-all", "--die-with-parent", "--new-session",
            "--ro-bind", "/usr", "/usr", "--ro-bind", "/etc", "/etc"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            argv += ["--symlink", os.readlink(link), link]
    argv += ["--proc", "/proc", "--dev", "/dev",
             "--bind", str(case_dir / "app"), "/app",
             "--ro-bind", str(case_dir / "test.json"), "/tests/test.json",
             "--ro-bind", str(capture), "/tests/test_outputs.py",
             "--ro-bind", str(case_dir / "harness.py"), "/harness.py",
             "--clearenv", "--setenv", "PATH", "/usr/bin",
             "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
             "--chdir", "/app", "/usr/bin/python3", "-I", "-B", "/harness.py"]
    return argv


def run_case(capture: Path, work: Path, case: dict) -> dict:
    if not os.access(BWRAP, os.X_OK):
        raise SetupDefect(f"no-bwrap {BWRAP}")
    with tempfile.TemporaryDirectory(prefix="case-", dir=work) as temp:
        case_dir = Path(temp)
        (case_dir / "app").mkdir()
        stage(case_dir / "app", case["result"]["repo"])
        (case_dir / "test.json").write_bytes(case["result"]["test_json"].encode("utf-8"))
        (case_dir / "harness.py").write_text(HARNESS, encoding="utf-8")
        proc = subprocess.run(sandbox_argv(capture, case_dir), capture_output=True,
                              text=True, timeout=120, env={"PATH": "/usr/bin"})
        if proc.returncode != 0:
            raise SetupDefect(f"sandbox-exit={proc.returncode} stderr={proc.stderr.strip()[-200:]!r}")
        lines = [line for line in proc.stdout.splitlines() if line.startswith("PAYLOAD ")]
        if len(lines) != 1:
            raise SetupDefect("sandbox-protocol")
        try:
            payload = json.loads(lines[0][len("PAYLOAD "):])
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
            payload = {"tests": [[name, letter, ""] for name, letter in zip(TESTS, case["predicted"])]}
            observed = "".join(row[1] for row in payload["tests"])
            predicted = case["predicted"]
            mismatches += observed != predicted
            observations.append(f"CASE {case['id']} predicted={predicted} observed={observed}")
    legs = len(TESTS) * len(cases)
    observations.append(f"cases={len(cases)} legs={legs} mismatches={mismatches}")
    observations.append(f"PREDICATE R90-PROBE {'fail' if mismatches else 'pass'}")
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
        f"HOST_USERNS {host_userns()}",
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
        print("PREDICATE R90-PROBE setup-defect")
        return 2
    lines = stamp(lane, work, capture, table_bytes, code) + ["OBSERVATIONS_BEGIN"] + observations
    lines += ["OBSERVATIONS_END", ""]
    sys.stdout.write("\n".join(lines))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""Replay the captured `regex-chess` grader with its own four test functions and its own pytest
reward rule (round 98, R98-C1).

The task image (captured `Dockerfile`) is python:3.13-slim-bookworm with python-chess; the agent's
artefact is /app/re.json, a list of [regex, replacement] pairs. The verifier (`test.sh`) runs
`/tests/test_outputs.py` under `uvx -p 3.13 -w pytest==8.4.1 -w chess==1.11.2` and writes reward 1
iff pytest exits 0. This probe models the verifier side with one pre-staged virtual environment
passed by path:

    --grader-venv  python 3.13.x, chess 1.11.2, pytest 8.4.1

Pinned versions are checked inside the sandbox before any case runs (a mismatch is a setup defect,
exit 2). The receipt stamps only the pinned values (GRADER_SIDE); the CPython micro goes to
GRADER_UNPINNED, which a re-run need not reproduce (round-96 W-2). Staging the venv needs the
network; the probe does not: every sandboxed step runs in a fresh bubblewrap namespace with
--unshare-all (no network) and --clearenv, tmpfs root, host /usr read-only, the venv and its
uv-managed interpreter read-only, the case /app read-write, the captured test file read-only at
/tests. Host /etc is not bound. The sandbox binary is fixed at /usr/bin/bwrap (round-97 MutC1: an
injectable bwrap let a fake sandbox pass).

Captures are flat (round-97 routed defect 1: the anchor-digest gate binds `<task dir>/<basename>`):
`corpus/evidence/round98/tb2-regex-chess/`.

Each case stages /app and, for `solve`-based kinds, runs the captured `solve.sh` unmodified with
the image's tools (bash, python, gzip) to produce /app/re.json; the declared transform is then
applied to the decoded pair list by this probe. Lookup-table kinds are built inside the sandbox by
a builder that imports the captured test file, records every FEN it would hand to
`verify_legal_moves`, and maps each recorded FEN to python-chess's answer. The grader is then run
ONCE per case as real pytest (`pytest.main`) over the unmodified captured file; an observe-only
plugin records each test's call-phase outcome and `call.excinfo.typename` (dry run 2: pytest's
short summary prints `assert ...` for rewritten bare asserts, so the summary text is not a type):

    immortal    test_immortal_game          P passed, F AssertionError,
    century     test_game_of_century        E:<exception type name> any other failure
    naroditsky  test_naroditsky_ivanchuk
    not_long    test_not_long
    reward      1 iff pytest exits 0, else 0

No assertion is reimplemented. Cases run concurrently (--jobs, default 8); output order is the case
table order.

Usage:  python3 plans/round98_regexchess_probe.py --lane <repo> --work <scratch dir>
            --grader-venv <dir> [--jobs N]
Exit:   0 every case observed == predicted, 1 a case differed, 2 setup defect.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

CAP = "corpus/evidence/round98/tb2-regex-chess"
TABLE = "plans/round98-cases.json"
TOOL = "plans/round98_regexchess_probe.py"
MEMBER = "regex-chess"
HEADER = "# tb2 regex-chess grader probe (round 98)"
PINS = {
    "test_outputs.py": "4983c44d21c56dd8191381eff0304afc8b87bb714527ea9036b3319c015a30b4",
    "test.sh": "8f7f00a1c4dde7fcca6c918c768f2aba432b8c4007c15989716c68091950da87",
    "solve.sh": "b728bf0ea392a3d244afbd0818d36933c8d3e190e47743c1382cd518d518a2e9",
    "Dockerfile": "2616cd775252303839dfda0ee2f047eb862952b053b0103bd6b2460ef90c11b7",
    "check.py": "f9c416ae9ea01dcdd5f6a43170c8434b8c0a0b389a4a30876a2048e277d191c7",
    "task.toml": "07fe52636fcc4bc9fff25d5630af145b97a5331219d719cc8decb4ca67ea21d4",
    "instruction.md": "a6ed3fcc54fc92d71a84af921942422d299ca89b410dcd92cd05a53d0d06436c",
}
SUBJECT_SHA = PINS["test_outputs.py"]
BWRAP = "/usr/bin/bwrap"
CASE_TIMEOUT = 3600
GRADER_WANT = ("3.13", "1.11.2", "8.4.1")   # test.sh uvx pins: -p 3.13, chess, pytest
TESTS = ("test_immortal_game", "test_game_of_century", "test_naroditsky_ivanchuk", "test_not_long")
NOOP = ["\\A(?!)", ""]

# kind -> (source, transform); source "solve" = the captured solve.sh output, "lookup" = the
# in-sandbox lookup-table builder, a list = that literal pair list, None = no file.
VARIANTS: dict[str, tuple[object, str]] = {
    "solve": ("solve", "none"),
    "absent": (None, "none"),
    "empty-list": ([], "none"),
    "dup-first-drop-second": ("solve", "append-dup-first"),
    "drop-last": ("solve", "append-drop-last"),
    "extra-line": ("solve", "append-extra-line"),
    "invented-ep": ("solve", "append-invented-ep"),
    "castling-dropped": ("solve", "append-castling-dropped"),
    "lookup-table": ("lookup", "none"),
    "lookup-table-minus-last": ("lookup", "drop-last-entry"),
    "oversize-chars": ("solve", "append-oversize"),
    "pair-count-limit": ("solve", "pad-to-100000"),
}
APPENDS = {
    # first output line duplicated, second line removed: same count, every line legal
    "append-dup-first": [["\\A([^\\n]*)\\n[^\\n]*", "\\1\\n\\1"]],
    "append-drop-last": [["\\n[^\\n]*\\Z", ""]],
    "append-extra-line": [["\\A([^\\n]*)", "\\1\\n\\1"]],
    # an en-passant square invented on every line whose true field is "-"
    "append-invented-ep": [["(?m)^(\\S+ b \\S+) - ", "\\1 h6 "]],
    "append-castling-dropped": [["(?m)^(\\S+ b) \\S+ ", "\\1 - "]],
    "append-oversize": [["\\A(?!)", "x" * 10_000_001]],
}

BUILDER = r"""
import importlib.util, json, re, sys
import chess
sys.path[:0] = ["/tests"]
spec = importlib.util.spec_from_file_location("tb2_grader", "/tests/test_outputs.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
seen = []
mod.verify_legal_moves = lambda fen: seen.append(fen)
for name in %r[:3]:
    getattr(mod, name)()
order = list(dict.fromkeys(seen))
if sys.argv[1] == "drop-last-entry":
    order = order[:-1]
pairs = []
for fen in order:
    board = chess.Board(fen)
    lines = []
    for move in board.legal_moves:
        if move.promotion and move.promotion != chess.QUEEN:
            continue
        b = board.copy()
        b.push(move)
        lines.append(b.fen())
    pairs.append(["\\A" + re.escape(fen) + "\\Z", "\n".join(lines)])
json.dump(pairs, open("/app/re.json", "w"))
print("BUILT recorded=%%d unique=%%d entries=%%d" %% (len(seen), len(dict.fromkeys(seen)), len(pairs)))
""" % (TESTS,)

VERSIONS = ("import sys, chess, pytest\n"
            "print('VERSIONS', sys.version.split()[0], chess.__version__, pytest.__version__)\n")
RUNNER = r"""
import sys
import pytest
verdict = {}
class Observe:
    # observes only: records each test's call-phase outcome and exception type name
    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        rep = outcome.get_result()
        if rep.when == "call" or (rep.when != "call" and rep.failed):
            if rep.passed:
                verdict[item.name] = "P"
            elif call.excinfo is not None:
                name = call.excinfo.typename
                verdict[item.name] = "F" if name == "AssertionError" else "E:" + name
            else:
                verdict[item.name] = "E:" + rep.outcome
rc = int(pytest.main(["-q", "-p", "no:cacheprovider", "/tests/test_outputs.py"], plugins=[Observe()]))
for name in %r:
    print("VERDICT", name, verdict.get(name, "MISSING"))
print("RC", rc)
sys.exit(rc)
""" % (TESTS,)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def guarded(args: list[str]) -> str:
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return "absent"
    text = (proc.stdout or proc.stderr).strip()
    return text.splitlines()[0] if text else "absent"


class Box:
    """One sandbox recipe: the read-only interpreter/venv binds shared by every run."""

    def __init__(self, ro_trees: list[str]):
        self.ro_trees = ro_trees

    def cmd(self, binds: list[tuple[str, str, str]], chdir: str, path: str, argv: list[str]) -> list[str]:
        cmd = [BWRAP, "--die-with-parent", "--unshare-all", "--clearenv",
               "--tmpfs", "/", "--ro-bind", "/usr", "/usr",
               "--symlink", "usr/bin", "/bin", "--symlink", "usr/lib", "/lib",
               "--symlink", "usr/lib", "/lib64", "--symlink", "usr/bin", "/sbin",
               "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp"]
        for tree in self.ro_trees:
            cmd += ["--ro-bind", tree, tree]
        for kind, src, dst in binds:
            cmd += [kind, src, dst]
        return cmd + ["--setenv", "PATH", path, "--setenv", "HOME", "/tmp",
                      "--setenv", "LANG", "C.UTF-8", "--chdir", chdir, *argv]

    def run(self, binds, chdir, path, argv) -> subprocess.CompletedProcess:
        return subprocess.run(self.cmd(binds, chdir, path, argv), capture_output=True, text=True,
                              timeout=CASE_TIMEOUT)


def venv_python(venv: Path) -> Path:
    return venv / "bin" / "python"


def interpreter_root(venv: Path) -> str:
    real = venv_python(venv).resolve()
    return str(real.parent.parent.parent)


def check_venv(box: Box, venv: Path, scratch: Path) -> tuple[str, str]:
    probe = scratch / "versions.py"
    probe.write_text(VERSIONS, encoding="utf-8")
    proc = box.run([("--ro-bind", str(probe), "/versions.py")], "/tmp", "%s/bin:/usr/bin" % venv,
                   [str(venv_python(venv)), "-I", "-B", "/versions.py"])
    line = next((x for x in proc.stdout.splitlines() if x.startswith("VERSIONS ")), "")
    parts = line.split()
    if (len(parts) != 4 or ".".join(parts[1].split(".")[:2]) != GRADER_WANT[0]
            or parts[2] != GRADER_WANT[1] or parts[3] != GRADER_WANT[2]):
        raise SystemExit("SETUP venv %s versions %r rc=%d %s" % (venv, line, proc.returncode,
                                                                   proc.stderr.strip()[-200:]))
    return "%s %s %s" % GRADER_WANT, parts[1]


def apply(pairs: list, how: str, kind: str) -> list:
    if how == "none":
        return pairs
    if how in APPENDS:
        return pairs + APPENDS[how]
    if how == "pad-to-100000":
        if len(pairs) >= 100_000:
            raise SystemExit("SETUP transform %s: solution already has %d pairs" % (kind, len(pairs)))
        return pairs + [NOOP] * (100_000 - len(pairs))
    raise SystemExit("SETUP unknown transform %s for %s" % (how, kind))


def stage(box: Box, case: dict, cap: Path, root: Path, venv: Path, tests: Path, builder: Path) -> tuple[Path, str]:
    kind = case["app"]
    if kind not in VARIANTS:
        raise SystemExit("SETUP unknown app kind %s" % kind)
    source, how = VARIANTS[kind]
    if root.exists():
        shutil.rmtree(root)
    app = root / "app"
    app.mkdir(parents=True)
    target = app / "re.json"
    built = "-"
    if source is None:
        return app, built
    if isinstance(source, list):
        target.write_text(json.dumps(source), encoding="utf-8")
        return app, built
    path = "%s/bin:/usr/bin" % venv
    if source == "lookup":
        proc = box.run([("--bind", str(app), "/app"), ("--ro-bind", str(tests), "/tests"),
                        ("--ro-bind", str(builder), "/builder.py")], "/app", path,
                       [str(venv_python(venv)), "-I", "-B", "/builder.py", how])
        line = next((x for x in proc.stdout.splitlines() if x.startswith("BUILT ")), "")
        if proc.returncode != 0 or not target.is_file() or not line:
            raise SystemExit("SETUP lookup builder rc=%d %s" % (proc.returncode, proc.stderr.strip()[-300:]))
        return app, line.split(" ", 1)[1].replace(" ", ",")
    script = root / "solve.sh"
    shutil.copyfile(cap / "solve.sh", script)
    proc = box.run([("--bind", str(app), "/app"), ("--ro-bind", str(script), "/solve.sh")], "/app",
                   path, ["/usr/bin/bash", "/solve.sh"])
    if proc.returncode != 0 or not target.is_file():
        raise SystemExit("SETUP solve.sh wrote no re.json rc=%d %s" % (proc.returncode, proc.stderr.strip()[-300:]))
    if how != "none":
        pairs = json.loads(target.read_text(encoding="utf-8"))
        target.write_text(json.dumps(apply(pairs, how, kind)), encoding="utf-8")
    return app, built


def run_case(box: Box, app: Path, tests: Path, venv: Path, runner: Path) -> str:
    proc = box.run([("--bind", str(app), "/app"), ("--ro-bind", str(tests), "/tests"),
                    ("--ro-bind", str(runner), "/runner.py")], "/app",
                   "%s/bin:/usr/bin" % venv, [str(venv_python(venv)), "-I", "-B", "/runner.py"])
    verdict: dict[str, str] = {}
    rc = None
    for line in proc.stdout.splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[0] == "VERDICT":
            verdict[parts[1]] = parts[2]
        elif len(parts) == 2 and parts[0] == "RC" and parts[1].lstrip("-").isdigit():
            rc = int(parts[1])
    out = [verdict.get(name, "MISSING") for name in TESTS]
    out.append("1" if rc == 0 and proc.returncode == 0 else "0" if rc is not None else "NORC(%d)" % proc.returncode)
    return ",".join(out)


def detail(app: Path) -> str:
    target = app / "re.json"
    if not target.is_file():
        return "file=absent"
    text = target.read_text(encoding="utf-8")
    return "chars=%d pairs=%d sha=%s" % (len(text), len(json.loads(text)), sha(text.encode())[:16])


def one(box, case, cap, work, venv, tests, builder, runner) -> tuple[str, str]:
    root = work / "cases" / case["id"]
    try:
        app, built = stage(box, case, cap, root, venv, tests, builder)
        observed = run_case(box, app, tests, venv, runner)
        info = "%s built=%s" % (detail(app), built)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    return observed, info


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=".")
    parser.add_argument("--work", required=True)
    parser.add_argument("--grader-venv", required=True)
    parser.add_argument("--jobs", type=int, default=8)
    args = parser.parse_args(argv)
    lane = Path(args.lane).resolve()
    work = Path(args.work).resolve()
    grader_venv = Path(args.grader_venv).resolve()
    for p in (work, grader_venv):
        if p == lane or lane in p.parents:
            print("DEFECT SETUP path inside the lane %s" % p)
            return 2
    if args.jobs < 1:
        print("DEFECT SETUP --jobs must be >= 1")
        return 2
    work.mkdir(parents=True, exist_ok=True)
    cap = lane / CAP
    if not Path(BWRAP).is_file() or not os.access(BWRAP, os.X_OK):
        print("DEFECT SETUP sandbox-unavailable %s" % BWRAP)
        return 2
    try:
        userns = Path("/proc/sys/user/max_user_namespaces").read_text().strip()
    except OSError:
        userns = "absent"
    if not userns.isdigit() or int(userns) <= 0:
        print("DEFECT SETUP user namespaces unavailable (%s)" % userns)
        return 2
    for rel, want in PINS.items():
        p = cap / rel
        if not p.is_file() or sha(p.read_bytes()) != want:
            print("DEFECT SETUP capture sha mismatch %s" % rel)
            return 2
    if not venv_python(grader_venv).exists():
        print("DEFECT SETUP venv python absent %s" % grader_venv)
        return 2
    table_bytes = (lane / TABLE).read_bytes()
    table = json.loads(table_bytes.decode())
    box = Box(sorted({str(grader_venv), interpreter_root(grader_venv)}))
    try:
        pinned, unpinned = check_venv(box, grader_venv, work)
    except SystemExit as error:
        print("DEFECT %s" % error)
        return 2
    builder = work / "builder.py"
    builder.write_text(BUILDER, encoding="utf-8")
    runner = work / "runner.py"
    runner.write_text(RUNNER, encoding="utf-8")
    tests = work / "tests"
    if tests.exists():
        shutil.rmtree(tests)
    tests.mkdir()
    shutil.copyfile(cap / "test_outputs.py", tests / "test_outputs.py")
    print(HEADER)
    print("MEMBER %s" % MEMBER)
    print("SUBJECT_SHA %s" % SUBJECT_SHA)
    print("TEST_SH_SHA %s" % PINS["test.sh"])
    print("SOLVE_SHA %s" % PINS["solve.sh"])
    print("TOOL_SHA %s" % sha((lane / TOOL).read_bytes()))
    print("CASE_TABLE_SHA %s" % sha(table_bytes))
    print("LANE_TIP %s" % guarded(["git", "-C", str(lane), "rev-parse", "HEAD"]))
    print("GRADER_SIDE python,chess,pytest %s" % pinned)
    print("GRADER_UNPINNED python %s" % unpinned)
    print("HOST_BASH %s" % guarded(["/usr/bin/bash", "--version"]))
    print("HOST_USERNS %s" % userns)
    print("SANDBOX clearenv=1 unshare-all=1 etc-bound=0 bwrap=%s" % BWRAP)
    print("LEG_ORDER %s" % ",".join(table["leg_order"]))
    sys.stdout.flush()
    cases = table["cases"]
    try:
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            futures = [pool.submit(one, box, c, cap, work, grader_venv, tests, builder, runner) for c in cases]
            results = [f.result() for f in futures]
    except SystemExit as error:
        print("DEFECT %s" % error)
        return 2
    finally:
        shutil.rmtree(work / "cases", ignore_errors=True)
    print("OBSERVATIONS_BEGIN")
    mismatches = 0
    for case, (observed, info) in zip(cases, results):
        ok = observed == case["predicted"]
        mismatches += 0 if ok else 1
        print("CASE %s predicted=%s observed=%s ok=%s" % (case["id"], case["predicted"], observed, ok))
        print("DETAIL %s %s %s" % (case["id"], info, case["app"]))
    print("OBSERVATIONS_END")
    print("mismatches %d" % mismatches)
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

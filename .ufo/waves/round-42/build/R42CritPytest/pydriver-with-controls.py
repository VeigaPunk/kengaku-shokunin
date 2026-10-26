#!/usr/bin/env python3
"""Round-42 real-runner parity check for C2: replay every frozen fibsqrt_probe case end state and grade it with
REAL pytest (pytest 8.4.1 under CPython 3.13) instead of the probe's direct-call harness.

The probe copy is imported from the lane clone; its Case table, capture pins and staging steps are reused verbatim.
Only the grading step differs: /tests holds test_outputs.py + sim.c, /app is the cwd, and `python -m pytest` decides
P/F per test node.  Nothing here writes outside --scratch.
"""
from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

BWRAP = "/usr/bin/bwrap"
PYROOT = "/home/vgpnk/.local/share/uv"
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

lane = pathlib.Path(sys.argv[1]).resolve()
scratch = pathlib.Path(sys.argv[2]).resolve()
only = sys.argv[3:] or []
PY = scratch / "venv" / "bin" / "python"

spec = importlib.util.spec_from_file_location("probe_copy", lane / "plans" / "fibsqrt_probe.py")
probe = importlib.util.module_from_spec(spec)
sys.modules["probe_copy"] = probe
spec.loader.exec_module(probe)
CAP = (lane / probe.CAP).resolve()
TESTS = probe.TESTS
CASES = [c for c in probe.CASES if not only or c.cid in only]

TESTSH = os.environ.get("PYDRIVER_TESTSH") == "1"
SKIP_RECIPE = os.environ.get("PYDRIVER_SKIPRECIPE") == "1"
NODE = re.compile(r"(?:PASSED|FAILED|ERROR)\s+\S*::(test_[A-Za-z0-9_]+)"
                   r"|::(test_[A-Za-z0-9_]+)\s+(PASSED|FAILED|ERROR)")


def sandbox_argv(work):
    argv = [BWRAP, "--unshare-net", "--unshare-pid", "--unshare-ipc", "--die-with-parent", "--new-session",
            "--ro-bind", "/usr", "/usr"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            argv += ["--symlink", os.readlink(link), link]
    argv += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
             "--ro-bind", str(scratch / "venv"), str(scratch / "venv"),
             "--ro-bind", PYROOT, PYROOT,
             "--bind", str(work / "app"), "/app", "--dir", "/tests", "--dir", "/cap"]
    for name in ("test_outputs.py", "sim.c"):
        argv += ["--ro-bind", str(CAP / name), f"/tests/{name}"]
    argv += ["--ro-bind", str(CAP / "solve.sh"), "/cap/solve.sh",
             "--ro-bind", str(work / "recipe.sh"), "/recipe.sh", "--chdir", "/app"]
    return argv


def stage(root, case):
    """Identical to fibsqrt_probe.run_case's staging (the frozen end-state construction)."""
    work = pathlib.Path(tempfile.mkdtemp(prefix="pyp-", dir=root))
    app = work / "app"
    app.mkdir()
    shutil.copyfile(CAP / "sim.c", app / "sim.c")
    shutil.copyfile(CAP / "gates.txt", app / "gates.txt")
    if case.gates is None:
        (app / "gates.txt").unlink()
    elif case.gates == "<dir>":
        (app / "gates.txt").unlink()
        (app / "gates.txt").mkdir()
    elif case.gates == "<empty>":
        (app / "gates.txt").write_bytes(b"")
    elif case.gates:
        (app / "gates.txt").write_bytes(case.gates.encode())
    if case.sim is not None:
        (app / "sim").write_text(case.sim)
        (app / "sim").chmod(0o755)
    (work / "recipe.sh").write_text(case.recipe or ":\n")
    return work


def run_recipe(work):
    """The case's end-state recipe, as fibsqrt_probe's harness runs it: bash -euo pipefail in cwd /app."""
    env = {"PATH": PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PYTHONUTF8": "1",
           "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": "/tmp"}
    p = subprocess.run(sandbox_argv(work) + ["/usr/bin/bash", "-euo", "pipefail", "/recipe.sh"],
                       env=env, capture_output=True, text=True, timeout=1800)
    return p.returncode, p.stdout, p.stderr


def grade(work, logdir, cid, run):
    env = {"PATH": PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PYTHONUTF8": "1",
           "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": "/tmp", "COLUMNS": "200"}
    args = (["-rA", "--ctrf", "/tmp/ctrf.json", "/tests/test_outputs.py"] if TESTSH
            else ["-v", "-p", "no:cacheprovider", "/tests/test_outputs.py"])
    p = subprocess.run(sandbox_argv(work) + [str(PY), "-m", "pytest"] + args,
                       env=env, capture_output=True, text=True, timeout=1800)
    (logdir / f"{cid}.run{run}.out").write_text(
        f"# rc={p.returncode}\n--- stdout ---\n{p.stdout}\n--- stderr ---\n{p.stderr}\n")
    verdicts = {}
    for line in p.stdout.splitlines():
        m = NODE.search(line)
        if m:
            name, verdict = (m.group(1), line.split()[0]) if m.group(1) else (m.group(2), m.group(3))
            verdicts[name] = verdict
    return p.returncode, verdicts, p.stdout


def letters(v):
    return "".join("P" if v.get(t) == "PASSED" else "F" for t in TESTS)


def main():
    suffix = ("-testsh" if TESTSH else "") + ("-only" if only else "")
    logdir = scratch / ("pytest-out" + suffix)
    logdir.mkdir(exist_ok=True)
    root = pathlib.Path(tempfile.mkdtemp(prefix="k42-pyp-", dir=scratch))
    rows = []
    try:
        print(f"# real-runner parity: pytest 8.4.1 / CPython 3.13 on {len(CASES)} frozen case end states")
        for c in CASES:
            work = stage(root, c)
            try:
                rrc = (0, "", "") if SKIP_RECIPE else run_recipe(work)
                if rrc[0] != 0:
                    print(f"SETUP case {c.cid} recipe rc={rrc[0]}", file=sys.stderr)
                    print(rrc[2], file=sys.stderr)
                    return 2
                rc1, v1, out1 = grade(work, logdir, c.cid, 1)
                rc2, v2, out2 = grade(work, logdir, c.cid, 2)
            finally:
                shutil.rmtree(work, ignore_errors=True)
            if set(v1) != set(TESTS) or set(v2) != set(TESTS):
                print(f"SETUP case {c.cid} did not yield three node verdicts twice rc={rc1}/{rc2}", file=sys.stderr)
                print(out1, file=sys.stderr)
                print(out2, file=sys.stderr)
                return 2
            detail = ",".join(f"{t}:{v1[t]}" for t in TESTS)
            rows.append({"cid": c.cid, "pytest": letters(v1), "pytest2": letters(v2),
                         "predicted": c.predicted, "rc": [rc1, rc2], "detail": detail,
                         "violates": list(c.violates), "requirement": c.requirement})
            print(f"CASE {c.cid} pytest={letters(v1)} nodes={detail} rc={rc1}"
                  f" regrade={'same' if letters(v1) == letters(v2) else 'DIFF:' + letters(v2)}"
                  f" probe_predicted={c.predicted}")
        (scratch / f"pytest-parity{suffix}.json").write_text(json.dumps(rows, indent=1) + "\n")
        print(f"cases={len(rows)}")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

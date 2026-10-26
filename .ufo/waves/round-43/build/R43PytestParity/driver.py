#!/usr/bin/env python3
"""R43PytestParity: rebuild each feal_probe.py case end state and grade it with REAL pytest 8.4.1.

The probe module (a copy, from this seat's lane clone) supplies CASES, the staging in run_case and the
bwrap sandbox argv. Only the grade step is replaced: instead of importing the test function in a harness
process, the pinned test.sh invocation is run inside the same per-case sandbox:
  pytest /tests/test_outputs.py -v -rA     (pytest==8.4.1, setuptools==80.9.0, python 3.13.16)
and the process exit status is recorded (test.sh:25 rewards it).  Two fresh pytest runs per case, mirroring
the probe's regrade.
"""
import importlib.util
import json
import os
import pathlib
import subprocess
import sys
import time

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r43/R43PytestParity")
PROBE = S / "lane" / "plans" / "feal_probe.py"
VENV = pathlib.Path(os.environ.get("PAR_VENV", str(S / "tools" / "venv")))
EXTRA = os.environ.get("PAR_EXTRA", "").split()
UVPY = pathlib.Path("/home/vgpnk/.local/share/uv/python")

spec = importlib.util.spec_from_file_location("feal_probe_copy", PROBE)
probe = importlib.util.module_from_spec(spec)
sys.modules["feal_probe_copy"] = probe
spec.loader.exec_module(probe)

REAL_HARNESS = probe.harness
PYTEST = str(VENV / "bin" / "pytest")
ENV = dict(probe.ENV)
ENV["PATH"] = str(VENV / "bin") + ":" + probe.ENV["PATH"]

RUNS = []          # (cid, index, rc, elapsed, stdout)


def sandbox_argv(cap, work):
    argv = probe.sandbox_argv(cap, work)
    argv += ["--ro-bind", str(S / "tools"), str(S / "tools"),
             "--ro-bind", str(UVPY), str(UVPY)]
    return argv + [PYTEST, "/tests/test_outputs.py", "-v", "-rA"] + EXTRA


def pytest_harness(cap, work):
    t0 = time.time()
    try:
        p = subprocess.run(sandbox_argv(cap, work), env=ENV, capture_output=True, text=True, timeout=1800)
        rc, out = p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        rc, out = 124, "TIMEOUT"
    return rc, out, time.time() - t0


def harness(cap, work, mode):
    if mode != "grade":
        return REAL_HARNESS(cap, work, mode)
    rc, out, dt = pytest_harness(cap, work)
    idx = len([r for r in RUNS if r[0] == CURRENT[0]])
    (S / "out").mkdir(exist_ok=True)
    (S / "out" / f"{CURRENT[0]}.{idx}.log").write_text(out)
    RUNS.append((CURRENT[0], idx, rc, dt, out))
    return rc, out


probe.harness = harness
CURRENT = [None]


def marker(out):
    for line in reversed(out.splitlines()):
        s = line.strip()
        if s.startswith("=== ") or " passed" in s or " failed" in s or " error" in s:
            return s[:160]
    return ""


def main():
    only = sys.argv[1:] or None
    cap = S / "lane" / probe.CAP
    root = S / "w"
    root.mkdir(parents=True, exist_ok=True)
    rows = []
    for case in probe.CASES:
        if only and case.cid not in only:
            continue
        CURRENT[0] = case.cid
        t0 = time.time()
        rc, res = probe.run_case(cap, root, case, "grade")
        if rc != 0:
            rows.append({"cid": case.cid, "error": f"recipe rc={rc}", "predicted": case.predicted})
            continue
        letters = [probe.letter(*r)[0] for r in res]
        rows.append({"cid": case.cid, "predicted": case.predicted, "letters": letters,
                     "observed": probe.overall(letters[0]),
                     "regrade_same": letters[1] == letters[0],
                     "wall": round(time.time() - t0, 2)})
        print(f"CASE {case.cid} predicted={probe.overall(case.predicted)} observed={rows[-1]['observed']}"
              f" tests={''.join(letters)} regrade={'same' if letters[1] == letters[0] else 'DIFF:' + letters[1]}"
              f" wall={rows[-1]['wall']}s", flush=True)
    print(json.dumps({"rows": rows,
                      "runs": [{"cid": c, "i": i, "rc": rc, "elapsed": round(dt, 2),
                                "marker": marker(out), "head": out.strip().splitlines()[:6],
                                "tail": out.strip().splitlines()[-8:]} for c, i, rc, dt, out in RUNS]},
                     indent=1))


if __name__ == "__main__":
    main()

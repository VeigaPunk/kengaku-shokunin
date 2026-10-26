#!/usr/bin/env python3
"""Critic probe (round 38, seat R38CritPytest): the frozen build-pmars cases, graded by REAL pytest.

Runs each frozen case from plans/build_pmars_probe.py (imported as a module, so CASES/Art/build_art/
stage_app are the frozen ones, not a copy) inside the same bubblewrap layout, TWICE on the SAME staged
tree:

  direct  the frozen probe's own harness (import test_outputs.py, call the four functions in order,
          AssertionError/non-AssertionError/return -> F/F/P)
  pytest  the verifier's real argv (tests/test.sh): pytest 8.4.1 on python 3.13,
          `-rA --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py`, cwd /app,
          PATH = /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

Print, per case: the receipt's letters, the letters from each harness, pytest's exit code, and every
per-test outcome line. A case agrees iff pytest's per-test letters equal the receipt's letters AND
(pytest exits 0) == (receipt letters are PPPP).

The pytest venv is bound read-only at its original absolute path (its interpreter is a uv-managed
CPython 3.13 symlink, so relocation would break pyvenv detection); /logs is bound writable so the
ctrf plugin can write where tests/test.sh tells it to.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

FROZEN = "/plans/build_pmars_probe.py"  # placeholder, resolved from --lane
RECEIPT = "corpus/evidence/round38/build-pmars-probe.txt"


def load_frozen(lane: pathlib.Path):
    spec = importlib.util.spec_from_file_location("frozen_probe", lane / "plans/build_pmars_probe.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["frozen_probe"] = mod  # dataclasses resolve __module__ through sys.modules
    spec.loader.exec_module(mod)
    return mod


def receipt_letters(lane: pathlib.Path, ids):
    text = (lane / RECEIPT).read_text()
    out = {}
    for m in re.finditer(r"^CASE (\S+) predicted=\S+ observed=\S+ tests=([PF]{4})", text, re.M):
        out[m.group(1)] = m.group(2)
    return out


PYTEST_SUMMARY = re.compile(r"^(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS|RERUN) \S*test_outputs\.py::(test_\w+)")


def pytest_letters(stdout):
    """Parse `-rA` short summary info into a {test_name: status} map, then letters in TEST order."""
    seen = {}
    for line in stdout.splitlines():
        m = PYTEST_SUMMARY.match(line.strip())
        if m and m.group(2) not in seen:
            seen[m.group(2)] = m.group(1)
    return seen


def sandbox_argv(frozen, cap, work, venv):
    argv = [frozen.BWRAP, "--unshare-net", "--unshare-pid", "--unshare-ipc", "--die-with-parent",
            "--new-session", "--ro-bind", "/usr", "/usr"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        p = pathlib.Path(link)
        if p.is_symlink():
            argv += ["--symlink", str(p.readlink()), link]
    argv += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
             "--ro-bind", str(work / "ulb"), "/usr/local/bin",
             "--ro-bind", str(work / "ulsb"), "/usr/local/sbin",
             "--ro-bind", str(work / "app"), "/app",
             "--dir", "/tests",
             "--ro-bind", str(cap / "test_outputs.py"), "/tests/test_outputs.py",
             "--ro-bind", str(work / "harness.py"), "/harness.py",
             "--bind", str(work / "logs"), "/logs",
             # pytest venv + its uv-managed interpreter, at their original absolute paths
             "--ro-bind", venv, venv,
             "--ro-bind", "/home/vgpnk/.local/share/uv/python", "/home/vgpnk/.local/share/uv/python",
             "--chdir", "/app"]
    return argv


def env_for(frozen):
    return {"PATH": frozen.PATH, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}


def run(argv, env, timeout=300):
    r = subprocess.run(argv, env=env, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", required=True)
    ap.add_argument("--venv", required=True)
    ap.add_argument("--only", default=None, help="comma-separated case ids")
    ap.add_argument("--ctrf-out", default=None, help="copy each case ctrf.json here")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    frozen = load_frozen(lane)
    cap = lane / frozen.CAP
    venv = str(pathlib.Path(a.venv).resolve())
    pytest_bin = str(pathlib.Path(venv) / "bin" / "pytest")
    assert pathlib.Path(pytest_bin).exists(), pytest_bin
    receipts = receipt_letters(lane, None)
    ids = [c.cid for c in frozen.CASES]
    want = set(a.only.split(",")) if a.only else set(ids)
    root = pathlib.Path(a.work).resolve()
    root.mkdir(parents=True, exist_ok=True)
    env = env_for(frozen)
    agree = total = 0
    for case in frozen.CASES:
        if case.cid not in want:
            continue
        total += 1
        work = pathlib.Path(tempfile.mkdtemp(prefix="pytest-" + case.cid + "-", dir=root))
        try:
            (work / "ulb").mkdir()
            (work / "ulsb").mkdir()
            (work / "build").mkdir()
            (work / "logs" / "verifier").mkdir(parents=True)
            frozen.build_art(case.art, work / "ulb" / "pmars", work / "build")
            frozen.build_art(case.sbin, work / "ulsb" / "pmars", work / "build")
            frozen.stage_app(case.app, work / "app")
            (work / "harness.py").write_text(frozen.HARNESS_PY)
            sb = sandbox_argv(frozen, cap, work, venv)
            d_rc, d_out, d_err = run(sb + ["/usr/bin/python3", "/harness.py"], env)
            p_rc, p_out, p_err = run(sb + [pytest_bin, "-rA", "--ctrf", "/logs/verifier/ctrf.json",
                                          "/tests/test_outputs.py"], env)
            ctrf = json.loads((work / "logs" / "verifier" / "ctrf.json").read_text())
            if a.ctrf_out:
                out = pathlib.Path(a.ctrf_out)
                out.mkdir(parents=True, exist_ok=True)
                (out / (case.cid + ".json")).write_text(json.dumps(ctrf, indent=1, sort_keys=True))
            ctrf_status = {t["name"].split("::")[-1]: t["status"]
                           for t in ctrf["results"]["tests"]}
        finally:
            shutil.rmtree(work, ignore_errors=True)
        d_letters = "".join("F" if (" " + t + " P") not in d_out else "P" for t in frozen.TESTS)
        # the frozen harness prints "TEST <name> P" or "TEST <name> F[ error=...]"
        d_letters = "".join(
            next((("P" if ln == "TEST " + t + " P" else "F")
                  for ln in d_out.splitlines() if ln.startswith("TEST " + t)), "?")
            for t in frozen.TESTS)
        statuses = pytest_letters(p_out)
        p_letters = "".join({"PASSED": "P", "FAILED": "F", "ERROR": "F"}.get(statuses.get(t, "?"), "?")
                            for t in frozen.TESTS)
        rec = receipts.get(case.cid, "?")
        ok = p_letters == rec and (p_rc == 0) == (rec == "PPPP") and "?" not in p_letters
        agree += ok
        ctrf = work / "logs" / "verifier" / "ctrf.json"
        ctrf_letters = "".join({"passed": "P", "failed": "F"}.get(ctrf_status.get(t, "?"), "?")
                               for t in frozen.TESTS)
        print(f"CASE {case.cid} receipt={rec} direct={d_letters} pytest={p_letters} ctrf={ctrf_letters}"
              f" pytest_rc={p_rc} agree={'yes' if ok else 'NO'}")
        for t in frozen.TESTS:
            ln = next((x for x in p_out.splitlines() if x.startswith(("PASSED ", "FAILED ", "ERROR "))
                       and x.rstrip().endswith(t) ), None)
            print(f"  PYTESTOUT {t} {statuses.get(t, '?')}"
                  + ("" if ln is None else " | " + ln.strip()[:120]))
        for line in (p_out + p_err).splitlines():
            s = line.strip()
            if s.startswith(("E   ", "FAILED", "PASSED", "ERROR", "warning", "rootdir", "plugins",
                             "collected", "====")) and "short test summary" not in s:
                print("  RAW " + s[:160])
        if ctrf_letters != p_letters:
            print(f"  NOTE parse-divergence ctrf={ctrf_letters} -rA={p_letters}")
        if d_letters != rec:
            print(f"  NOTE direct-vs-receipt mismatch direct={d_letters} receipt={rec}")
    print(f"pytest-agree {agree}/{total}")
    return 0 if agree == total else 1


if __name__ == "__main__":
    sys.exit(main())

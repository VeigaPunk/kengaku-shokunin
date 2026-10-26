#!/usr/bin/env python3
"""Real-pytest parity runner for the round-41 C2 probe cases.

Rebuilds each constraints_probe.py case end state (importing a COPY of the probe from the
scratch clone: Case table + apply_edit), then runs the task's own verifier command under the
same test.sh invocation (uvx -p 3.13 -w pytest==8.4.1 -w pytest-json-ctrf==0.3.5 pytest
--ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA) inside a probe-style bwrap, and
compares per-test verdicts with corpus/evidence/round41/constraints-probe.txt.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r41/R41CritPytest")
LANE = S / "lane"
CAP = LANE / "corpus/evidence/round41/tb2-constraints-scheduling"
PROBE = LANE / "plans/constraints_probe.py"
RECEIPT = LANE / "corpus/evidence/round41/constraints-probe.txt"
UVDIR = pathlib.Path("/home/vgpnk/.local/bin")
UVPY = pathlib.Path("/home/vgpnk/.local/share/uv/python")
CACHE = S / "uvcache"
BWRAP = "/usr/bin/bwrap"
PATH_IN = "/uvbin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
PYTEST_ARGV = ["uvx", "-p", "3.13", "-w", "pytest==8.4.1", "-w", "pytest-json-ctrf==0.3.5",
               "pytest", "--ctrf", "/logs/verifier/ctrf.json", "/tests/test_outputs.py", "-rA"]


def load_probe():
    spec = importlib.util.spec_from_file_location("probe_copy", PROBE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["probe_copy"] = mod
    spec.loader.exec_module(mod)
    return mod


P = load_probe()
TESTS = P.TESTS


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def base_argv(app, *, tests_dir=None, logs_dir=None, solve=None, recipe=None):
    argv = [BWRAP, "--unshare-net", "--unshare-pid", "--unshare-ipc", "--die-with-parent",
            "--new-session", "--ro-bind", "/usr", "/usr"]
    for link in ("/bin", "/sbin", "/lib", "/lib64"):
        if os.path.islink(link):
            argv += ["--symlink", os.readlink(link), link]
    argv += ["--ro-bind", "/etc", "/etc", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
             "--tmpfs", "/run", "--bind", str(app), "/app"]
    if tests_dir is not None:
        argv += ["--dir", "/tests", "--bind", str(tests_dir), "/tests",
                 "--dir", "/logs", "--bind", str(logs_dir), "/logs",
                 "--dir", "/uvbin",
                 "--ro-bind", str(UVDIR / "uv"), "/uvbin/uv",
                 "--ro-bind", str(UVDIR / "uvx"), "/uvbin/uvx",
                 "--ro-bind", str(UVPY), "/uvpy",
                 "--bind", str(CACHE), "/uvcache"]
    if solve is not None:
        argv += ["--dir", "/cap", "--ro-bind", str(solve), "/cap/solve.sh"]
    if recipe is not None:
        argv += ["--dir", "/rc", "--ro-bind", str(recipe), "/recipe.sh"]
    argv += ["--chdir", "/app"]
    return argv


def env_for(extra=None):
    e = {"PATH": PATH_IN, "HOME": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
         "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1", "TERM": "dumb",
         "UV_CACHE_DIR": "/uvcache", "UV_PYTHON_INSTALL_DIR": "/uvpy", "UV_OFFLINE": "1",
         "UV_NO_PROGRESS": "1"}
    if extra:
        e.update(extra)
    return e


def run(argv, env, timeout=300):
    return subprocess.run(argv, env=env, capture_output=True, text=True, timeout=timeout)


def ctrf_letters(logs_dir):
    p = logs_dir / "verifier" / "ctrf.json"
    if not p.is_file():
        return None, {}
    d = json.loads(p.read_text())
    res = {}
    for t in d.get("results", {}).get("tests", []):
        fn = t.get("name", "").split("::")[-1]
        res[fn] = t.get("status")
    return "".join("P" if res.get(t) == "passed" else "F" for t in TESTS), res


def stdout_letters(out):
    res = {}
    for line in out.splitlines():
        m = re.match(r"^(PASSED|FAILED|ERROR)\s+\S*::(\w+)", line)
        if m and m.group(2) in TESTS:
            res[m.group(2)] = m.group(1).lower()
    return "".join("P" if res.get(t) == "passed" else "F" for t in TESTS), res


RECEIPT_CASES = {}
for line in RECEIPT.read_text().splitlines():
    m = re.match(r"^CASE (\S+) predicted=(\S+) observed=(\S+) tests=([PF]+) predicted_tests="
                 r"([PF]+) match=(\S+) regrade=(\S*)", line)
    if m:
        RECEIPT_CASES[m.group(1)] = {"observed": m.group(3), "tests": m.group(4)}


def run_case(case, root, runs):
    work = root / case.cid
    if work.exists():
        shutil.rmtree(work)
    app = work / "app"
    app.mkdir(parents=True)
    for name in P.INPUTS:
        shutil.copyfile(CAP / name, app / name)
    P.apply_edit(app, case.edit)
    if case.meeting is not None:
        (app / "meeting_scheduled.ics").write_bytes(case.meeting.encode())
    (work / "logs" / "verifier").mkdir(parents=True)
    tests = work / "tests"
    tests.mkdir()
    shutil.copyfile(CAP / "test_outputs.py", tests / "test_outputs.py")
    if case.recipe:
        rc_path = work / "recipe.sh"
        rc_path.write_text(case.recipe)
        r = run(base_argv(app, solve=CAP / "solve.sh", recipe=rc_path) +
                ["/usr/bin/bash", "-euo", "pipefail", "/recipe.sh"], env_for())
        if r.returncode != 0:
            return {"cid": case.cid, "error": f"recipe rc={r.returncode}", "stderr": r.stderr[-2000:]}
    results = []
    for i in range(runs):
        ctrf = work / "logs" / "verifier" / "ctrf.json"
        if ctrf.exists():
            ctrf.unlink()
        r = run(base_argv(app, tests_dir=tests, logs_dir=work / "logs") + PYTEST_ARGV, env_for())
        letters, raw = ctrf_letters(work / "logs")
        src = "ctrf"
        if letters is None:
            letters, raw = stdout_letters(r.stdout)
            src = "stdout"
        results.append({"rc": r.returncode, "letters": letters, "raw": raw, "src": src,
                        "stdout_tail": r.stdout[-3000:], "stderr_tail": r.stderr[-2000:]})
    return {"cid": case.cid, "results": results}


def main():
    only = sys.argv[1:] or None
    for name, digest in P.PINS.items():
        if sha256(CAP / name) != digest:
            print(f"SETUP capture {name} not at pinned digest", file=sys.stderr)
            return 2
    root = S / "cases"
    root.mkdir(parents=True, exist_ok=True)
    out = []
    for case in P.CASES:
        if only and case.cid not in only:
            continue
        rec = run_case(case, root, 2)
        rec["receipt"] = RECEIPT_CASES.get(case.cid)
        out.append(rec)
        rec_line = json.dumps(rec)
        with open(S / "results.jsonl", "a") as fh:
            fh.write(rec_line + "\n")
        if "error" in rec:
            print(f"ERROR {case.cid} {rec['error']}", flush=True)
            continue
        a, b = rec["results"][0], rec["results"][1]
        ok = a["letters"] == b["letters"]
        rc_obs = "pass" if a["letters"] == "P" * len(TESTS) else "fail"
        print(f"CASE {case.cid} tests={a['letters']} overall={rc_obs} regrade={'same' if ok else 'DIFF:' + b['letters']}"
              f" receipt_tests={rec['receipt']['tests'] if rec['receipt'] else '?'}"
              f" receipt_observed={rec['receipt']['observed'] if rec['receipt'] else '?'}"
              f" match={'yes' if rec['receipt'] and a['letters'] == rec['receipt']['tests'] else 'NO'}"
              f" src={a['src']} rc={a['rc']}", flush=True)
        if a["letters"] != (rec["receipt"]["tests"] if rec["receipt"] else ""):
            print("  pytest stdout tail:\n" + a["stdout_tail"], flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

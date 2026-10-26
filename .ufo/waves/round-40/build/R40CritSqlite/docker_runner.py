#!/usr/bin/env python3
"""Run the frozen round-40 db-wal probe CASES inside a docker image, reusing the frozen probe module.

Case recipes, MK_PY, HARNESS_PY and the grader are taken verbatim from plans/db_wal_probe.py; only the sandbox
(bwrap -> docker image with the image's own python3/sqlite3/xxd) changes, so a verdict difference is attributable
to the sqlite/python version, not to the case construction.

  docker_runner.py --lane CLONE --image TAG [--only a,b] [--work DIR]
"""
import argparse
import importlib.util
import pathlib
import shutil
import subprocess
import sys
import tempfile


def load_probe(lane):
    spec = importlib.util.spec_from_file_location("db_wal_probe", lane / "plans/db_wal_probe.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["db_wal_probe"] = mod
    spec.loader.exec_module(mod)
    return mod


def run_case(M, cap, root, case, image, timeout):
    work = pathlib.Path(tempfile.mkdtemp(prefix="dw-", dir=root))
    try:
        app = work / "app"
        app.mkdir()
        if case.seed:
            shutil.copyfile(cap / "main.db", app / "main.db")
            shutil.copyfile(cap / "main.db-wal.encrypted", app / "main.db-wal")
        (work / "recipe.sh").write_text(case.recipe)
        (work / "harness.py").write_text(M.HARNESS_PY)
        (work / "mk.py").write_text(M.MK_PY)
        argv = ["docker", "run", "--rm", "--network", "none", "--tmpfs", "/tmp:rw,size=64m",
                "-v", f"{app}:/app", "-v", f"{work / 'mk.py'}:/k/mk.py:ro",
                "-v", f"{work / 'recipe.sh'}:/recipe.sh:ro", "-v", f"{work / 'harness.py'}:/harness.py:ro",
                "-v", f"{cap / 'test_outputs.py'}:/cap/test_outputs.py:ro",
                "-v", f"{cap / 'solve.sh'}:/cap/solve.sh:ro",
                "-w", "/app", "-e", f"PATH={M.PATH}", "-e", "HOME=/tmp", "-e", "LANG=C.UTF-8",
                "-e", "LC_ALL=C.UTF-8", "-e", "PYTHONUTF8=1", "-e", "PYTHONDONTWRITEBYTECODE=1",
                image, "/usr/bin/python3", "/harness.py", "grade"]
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--image", required=True)
    ap.add_argument("--only", default=None, help="comma-separated case ids")
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    M = load_probe(lane)
    cap = lane / M.CAP
    for name, digest in M.PINS.items():
        if M.sha256(cap / name) != digest:
            print(f"SETUP capture {name} not at its pinned digest", file=sys.stderr)
            return 2
    cases = M.CASES if not a.only else [c for c in M.CASES if c.cid in set(a.only.split(","))]
    if not cases:
        print("SETUP no case selected", file=sys.stderr)
        return 2
    if a.work:
        pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    root = pathlib.Path(tempfile.mkdtemp(prefix="k40-dk-", dir=a.work))
    try:
        npass = nfail = mism = rediff = 0
        for c in cases:
            rc, out = run_case(M, cap, root, c, a.image, 300)
            got, again = {}, {}
            for l in out.splitlines():
                parts = l.split()
                if len(parts) >= 3 and parts[0] in ("TEST", "REGRADE") and parts[1] in M.TESTS:
                    (got if parts[0] == "TEST" else again)[parts[1]] = (parts[2], parts[3] if len(parts) > 3 else "")
            if rc != 0 or set(got) != set(M.TESTS) or set(again) != set(M.TESTS):
                print(f"SETUP case {c.cid} did not yield seven test verdicts twice (rc={rc})", file=sys.stderr)
                print(out, file=sys.stderr)
                return 2
            letters = "".join(got[t][0] for t in M.TESTS)
            letters2 = "".join(again[t][0] for t in M.TESTS)
            errs = ",".join(f"{t}:{got[t][1]}" for t in M.TESTS if got[t][1])
            obs = M.overall(letters)
            npass += obs == "pass"
            nfail += obs == "fail"
            match = letters == c.predicted
            mism += not match
            rediff += letters2 != letters
            print(f"CASE {c.cid} predicted={M.overall(c.predicted)} observed={obs} tests={letters}"
                  f" predicted_tests={c.predicted} match={'yes' if match else 'NO'}"
                  f" regrade={'same' if letters2 == letters else 'DIFF:' + letters2}"
                  f" violates={','.join(c.violates)}{' ' + errs if errs else ''} -- {c.requirement}")
        print(f"regrade cases={len(cases)} differ={rediff}")
        print(f"cases={len(cases)} observed_pass={npass} observed_fail={nfail} mismatches={mism}")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Same as docker_runner.py but for an arbitrary task image that lacks /cap and /k.

Mounts the case work dir at /w (ro) and the app dir at /app, then an in-container bash copies the harness,
mk.py, recipe and captures into place before running the frozen HARNESS_PY. Recipes stay byte-identical.
"""
import argparse
import pathlib
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from docker_runner import load_probe  # noqa: E402

ENTRY = ("mkdir -p /cap /k && cp /w/cap/test_outputs.py /w/cap/solve.sh /cap/ && cp /w/mk.py /k/mk.py && "
         "cp /w/harness.py /harness.py && cp /w/recipe.sh /recipe.sh && exec python3 /harness.py grade")


def run_case(M, cap, root, case, image):
    work = pathlib.Path(tempfile.mkdtemp(prefix="dw2-", dir=root))
    try:
        app = work / "app"
        app.mkdir()
        if case.seed:
            shutil.copyfile(cap / "main.db", app / "main.db")
            shutil.copyfile(cap / "main.db-wal.encrypted", app / "main.db-wal")
        (work / "recipe.sh").write_text(case.recipe)
        (work / "harness.py").write_text(M.HARNESS_PY)
        (work / "mk.py").write_text(M.MK_PY)
        (work / "cap").mkdir()
        shutil.copyfile(cap / "test_outputs.py", work / "cap" / "test_outputs.py")
        shutil.copyfile(cap / "solve.sh", work / "cap" / "solve.sh")
        argv = ["docker", "run", "--rm", "--network", "none", "--tmpfs", "/tmp:rw,size=64m",
                "-v", f"{work}:/w:ro", "-v", f"{app}:/app", "-w", "/app",
                "-e", f"PATH={M.PATH}", "-e", "HOME=/tmp", "-e", "LANG=C.UTF-8", "-e", "LC_ALL=C.UTF-8",
                "-e", "PYTHONUTF8=1", "-e", "PYTHONDONTWRITEBYTECODE=1",
                image, "bash", "-c", ENTRY]
        p = subprocess.run(argv, capture_output=True, text=True, timeout=300)
        return p.returncode, p.stdout
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--image", required=True)
    ap.add_argument("--only", default=None)
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
    if a.work:
        pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    root = pathlib.Path(tempfile.mkdtemp(prefix="k40-dk2-", dir=a.work))
    try:
        npass = nfail = mism = rediff = 0
        for c in cases:
            rc, out = run_case(M, cap, root, c, a.image)
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

#!/usr/bin/env python3
"""Advisory probe (not a battery module): build a_man's two fixtures and print the reference and the A21/A22
mutant result per fixture, so the class each mutant prints is on record. Reads the frozen counter's MUTANTS
table and the frozen tool; builds nothing inside the lane.

  python3 probe_manifest_views.py --lane DIR --module FILE --scratch DIR
"""
import argparse
import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--module", required=True)
    ap.add_argument("--scratch", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    C = load(lane / "plans/round40_c1_verify.py", "counter")
    mod = load(pathlib.Path(a.module).resolve(), "a_man")
    root = pathlib.Path(a.scratch).resolve()
    shutil.rmtree(root, ignore_errors=True)
    root.mkdir(parents=True)
    ctx = C.Ctx(lane, root)
    built = []
    for k, fx in enumerate(mod.FIXTURES):
        d = root / f"f{k:03d}"
        d.mkdir()
        built.append((fx, d, [str(t) for t in fx["build"](ctx, d)]))
    src = (lane / "plans/anchor_digest_check.py").read_text()
    variants = {"reference": src}
    for mid in ("A21", "A22"):
        row = next(m for m in C.MUTANTS if m[0] == mid)
        variants[mid] = src.replace(row[6], row[7], 1)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(root),
               GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null")
    for name, text in variants.items():
        (root / f"v-{name}.py").write_text(text)
    for fx, d, argv in built:
        print(f"FIXTURE {fx['fid']} expect={fx['expect']} defects={fx['defects']} argv={argv}")
        for name in variants:
            r = subprocess.run([sys.executable, str(root / f"v-{name}.py"), *argv], cwd=str(d), env=env,
                               capture_output=True, text=True)
            print(f"  {name:9s} rc={r.returncode} classes={sorted(C.classes('anchor', r.stdout))} "
                  f"last={r.stdout.strip().splitlines()[-1] if r.stdout.strip() else '-'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

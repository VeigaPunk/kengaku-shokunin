#!/usr/bin/env python3
"""Diagnostics for the p910 fixture family (not part of the C1 claim).

  python3 positive_control.py --lane <clone> --work <scratch>

1. Genuine-package positive control for P10: the round-35 package bytes + the lane's .gitignore,
   staged, run with `--rerun`. Prints the gate's clause lines so the reader can see whether the
   re-run clause ever returns `ok` anywhere in the frozen battery.
2. .gitignore counterfactual: builds the p910-receipt-one-byte fixture, runs the reference gate to
   create the byte-code cache, then removes the staged .gitignore from a copy and re-runs, so the
   dependency the module docstring claims can be observed instead of taken on faith.
"""
import argparse
import importlib.util
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
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    c = load(lane / "plans/round37_c1_verify.py", "k37_counter")
    p910 = load(lane / "plans/battery37/p910.py", "k37_p910")
    r36 = c.load_r36(lane)
    ctx = c.Ctx(lane, r36)
    root = work / "diag"
    shutil.rmtree(root, ignore_errors=True)
    gate = root / "gate.py"
    gate.parent.mkdir(parents=True)
    gate.write_text((lane / c.GATE_REL).read_text())

    def build(fid, d):
        for fx in p910.FIXTURES:
            if fx["fid"] == fid:
                return fx, list(fx["build"](ctx, d))
        raise SystemExit(f"no fixture {fid}")

    # 1. genuine package with --rerun
    d = root / "genuine-rerun"
    d.mkdir()
    ctx.genuine_package(d)
    p910._ignore_rule(ctx, d)
    ctx.git_add(d)
    argv = p910._argv(d, rerun=True)
    r = subprocess.run([sys.executable, str(gate), *argv, "--spec", str(ctx.spec_path)],
                       capture_output=True, text=True)
    print("== genuine package + --rerun (positive control for P10) ==")
    print(f"exit={r.returncode}")
    for line in r.stdout.splitlines():
        if c.CLAUSE_LINE.match(line):
            print("  " + line)
    # 2. .gitignore counterfactual on a P10 fixture
    d = root / "nocache"
    d.mkdir()
    fx, argv = build("p910-receipt-one-byte", d)
    first = subprocess.run([sys.executable, str(gate), *argv, "--spec", str(ctx.spec_path)],
                           capture_output=True, text=True)
    pyc = sorted(p.as_posix() for p in d.rglob("__pycache__/*"))
    print("== p910-receipt-one-byte ==")
    print(f"run1 exit={first.returncode} clause_lines={[l.split()[0] + ':' + l.split()[1] for l in first.stdout.splitlines() if c.CLAUSE_LINE.match(l)]}")
    print(f"byte-code files created={len(pyc)} {pyc[:2]}")
    d2 = root / "noignore"
    shutil.copytree(d, d2, symlinks=True)
    (d2 / ".gitignore").unlink()
    argv2 = [t.replace(str(d), str(d2)) for t in argv]
    second = subprocess.run([sys.executable, str(gate), *argv2, "--spec", str(ctx.spec_path)],
                            capture_output=True, text=True)
    print(f"run2 (same bytes, .gitignore removed) exit={second.returncode}")
    for line in second.stdout.splitlines():
        if c.CLAUSE_LINE.match(line) and line.split()[0] in ("P9", "P10"):
            print("  " + line)
    return 0


if __name__ == "__main__":
    sys.exit(main())

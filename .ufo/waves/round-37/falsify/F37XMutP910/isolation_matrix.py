#!/usr/bin/env python3
"""Isolation matrix for the four p910 fixtures.

For the four p910 fixtures (plus a genuine package run with `--rerun`, which is NOT in the frozen
battery: diagnostic only), print the reference result and, per frozen mutant of the clauses those
fixtures declare (P1, P2, P9, P10), which fixtures the mutant flips. A fixture that reacts to a
mutant of a clause it does not declare would not be isolating one defect.

  python3 isolation_matrix.py --lane <clone> --work <scratch>
"""
import argparse
import importlib.util
import pathlib
import shutil
import sys

IDS = ("p910-not-a-git-repo", "p910-receipt-deleted", "p910-probe-exits-1", "p910-receipt-one-byte")
WANT = ("M01", "M02", "M03", "M39", "M40", "M41", "M42", "M43")


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
    c = load(lane / "plans/round37_c1_verify.py", "k37_counter")
    p910 = load(lane / "plans/battery37/p910.py", "k37_p910")
    gate_src = (lane / c.GATE_REL).read_text()
    if c.sha256(lane / c.GATE_REL) != c.GATE_SHA256:
        print("gate not at freeze digest", file=sys.stderr)
        return 2
    r36 = c.load_r36(lane)
    ctx = c.Ctx(lane, r36)
    root = pathlib.Path(a.work).resolve() / "iso"
    shutil.rmtree(root, ignore_errors=True)
    root.mkdir(parents=True)
    gdir = root / "gates"
    gdir.mkdir()
    ref_gate = gdir / "ref.py"
    ref_gate.write_text(gate_src)
    built = []
    for fid in IDS:
        fx = next(f for f in p910.FIXTURES if f["fid"] == fid)
        d = root / "fx" / fid
        d.mkdir(parents=True)
        built.append((fx, d, list(fx["build"](ctx, d))))
    # genuine package with --rerun: a candidate positive control, deliberately outside the battery
    d = root / "fx" / "genuine-rerun(DIAG)"
    d.mkdir(parents=True)
    ctx.genuine_package(d)
    p910._ignore_rule(ctx, d)
    ctx.git_add(d)
    built.append(({"fid": "genuine-rerun(DIAG)", "expect": "accept", "defects": []},
                  d, p910._argv(d, rerun=True)))
    ref = {}
    for fx, d, argv in built:
        res = c.run_gate(ref_gate, ctx.spec_path, argv)
        ref[fx["fid"]] = res
        print(f"REF {fx['fid']:28s} rc={res[0]} defects={','.join(sorted(res[1])) or '-'}")
    for mid, clause, label, old, new in c.MUTANTS:
        if mid not in WANT:
            continue
        assert gate_src.count(old) == 1, mid
        mg = gdir / f"{mid}.py"
        mg.write_text(gate_src.replace(old, new, 1))
        flips = [fx["fid"] for fx, d, argv in built
                 if c.run_gate(mg, ctx.spec_path, argv) != ref[fx["fid"]]]
        print(f"MUT {mid} {clause:3s} flips={','.join(flips) or '-'}  -- {label}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

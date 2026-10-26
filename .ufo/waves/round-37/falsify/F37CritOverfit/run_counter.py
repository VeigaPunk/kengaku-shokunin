#!/usr/bin/env python3
"""Run the overfit gate through the round-37 C1 counter's own reference path.

Three receipts, all produced by importing plans/round37_c1_verify.py from a clean clone of the tip:

  A. genuine gate, `--only M01` (the counter's own battery path): must print
     BATTERY fixtures=64 wrong=0 renamed_disagree=0.
  B. the same, with the overfit gate swapped in as the reference gate (module.GATE_REL /
     module.GATE_SHA256 monkeypatched to the overfit file): the BATTERY line must be identical,
     which is exactly the claim "matches every declaration".
  C. per-fixture comparison of the two gates' (exit code, DEFECT set) over the counter-built fixtures
     and over the counter's renamed copies, plus a comparison against the landing receipt's per-fixture
     lines.

No lane file is written; nothing outside the scratch dir is created.

Usage: python3 run_counter.py --lane CLONE --work SCRATCH/work3 --gate SEATDIR/overfit_gate.py
       --receipt LANE/.ufo/waves/round-37/integrate/measure-final.txt
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import pathlib
import re
import shutil
import sys


def load(lane):
    spec = importlib.util.spec_from_file_location("k37", lane / "plans/round37_c1_verify.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def invoke(k37, argv):
    """Call the counter's main() with argv (it parses sys.argv), capturing stdout."""
    old_argv, buf = sys.argv, io.StringIO()
    try:
        sys.argv = ["round37_c1_verify.py"] + argv
        with contextlib.redirect_stdout(buf):
            rc = k37.main()
    finally:
        sys.argv = old_argv
    return rc, buf.getvalue()


def battery_line(out):
    for line in out.splitlines():
        if line.startswith("BATTERY "):
            return line
    return None


def receipt_rows(path):
    rows = {}
    for line in pathlib.Path(path).read_text().splitlines():
        m = re.match(r"^FIXTURE (\S+) expect=(\S+) declared=(\S+) observed_rc=(\d+) observed_defects=(\S+) (\S+)$",
                     line)
        if m:
            rows[m.group(1)] = (int(m.group(4)), frozenset() if m.group(5) == "-" else frozenset(m.group(5).split(",")))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--gate", required=True)
    ap.add_argument("--receipt", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    gate = pathlib.Path(a.gate).resolve()
    work.mkdir(parents=True, exist_ok=True)
    (work / "A").mkdir(exist_ok=True)
    (work / "B").mkdir(exist_ok=True)
    k37 = load(lane)

    print("=== A genuine gate, counter battery path ===")
    rcA, outA = invoke(k37, ["--lane", str(lane), "--only", "M01", "--work", str(work / "A")])
    print(battery_line(outA), "| exit", rcA)
    print("MUTANTS:", [l for l in outA.splitlines() if l.startswith("MUTANTS")][0])

    print("=== B overfit gate as the reference gate ===")
    orig_rel, orig_sha = k37.GATE_REL, k37.GATE_SHA256
    k37.GATE_REL = str(gate)
    k37.GATE_SHA256 = hashlib.sha256(gate.read_bytes()).hexdigest()
    try:
        rcB, outB = invoke(k37, ["--lane", str(lane), "--work", str(work / "B")])
    finally:
        k37.GATE_REL, k37.GATE_SHA256 = orig_rel, orig_sha
    print([l for l in outB.splitlines() if l.startswith("GATE ")][0])
    print(battery_line(outB), "| exit", rcB)
    print("MUTANTS:", [l for l in outB.splitlines() if l.startswith("MUTANTS")][0])
    wrong = [l for l in outB.splitlines() if l.endswith("WRONG") or "DISAGREES" in l]
    print("WRONG/DISAGREE lines:", len(wrong))
    for l in wrong[:5]:
        print("  ", l)

    print("=== C per-fixture cross-check (gate vs genuine, incl. renamed copies) ===")
    r36 = k37.load_r36(lane)
    ctx = k37.Ctx(lane, r36)
    fixtures = k37.r36_fixtures(r36) + k37.battery37_fixtures(lane / k37.BATTERY_REL)
    gdir = work / "C"
    gdir.mkdir(exist_ok=True)
    ref = gdir / "ref.py"
    ref.write_text((lane / k37.GATE_REL).read_text())
    receipts = receipt_rows(a.receipt)
    mism = ren = 0
    missing = []
    for i, fx in enumerate(fixtures):
        d = gdir / "fx" / f"f{i:03d}"
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
        argv = list(fx["build"](ctx, d))
        want = k37.run_gate(ref, ctx.spec_path, argv)
        got = k37.run_gate(gate, ctx.spec_path, argv)
        nd = gdir / "ren" / f"q{(len(fixtures) - i) * 7919 % 100003:05d}"
        if nd.exists():
            shutil.rmtree(nd)
        shutil.copytree(d, nd, symlinks=True)
        nargv = [t.replace(str(d), str(nd)) for t in argv]
        ngot = k37.run_gate(gate, ctx.spec_path, nargv)
        ok = got == want
        rok = ngot == want
        mism += not ok
        ren += not rok
        if not ok or not rok:
            print(f"MISMATCH {fx['fid']} genuine={want} overfit={got} renamed={ngot}")
        if fx["fid"] not in receipts:
            missing.append(fx["fid"])
        elif receipts[fx["fid"]] != want:
            print(f"RECEIPT-DIFF {fx['fid']} receipt={receipts[fx['fid']]} observed={want}")
    print(f"CROSSCHECK fixtures={len(fixtures)} overfit_mismatches={mism} renamed_mismatches={ren} "
          f"receipt_rows={len(receipts)} unlisted={len(missing)}")
    return 0 if (mism == 0 and ren == 0 and not missing and not wrong) else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""F37XMutP8 N1 probe: is `!= 1` -> `> 1` an equivalent mutant or a genuine defect the frozen battery
never exercises? Three packages are built from the genuine round-35 bytes:

  a) control            untouched (must accept under both gates)
  b) zero-index-row     the entry's corpus/README.md index row deleted, entry file kept (P8 zero-row case)
  c) unindexed-entry    the index row deleted AND the entry file removed (no set-equality fallback)

For each: reference result, N1 result, and the P8 detail line the gate prints (which branch fired).
"""
from __future__ import annotations

import argparse
import importlib.util
import pathlib
import shutil
import subprocess
import sys

OLD = "if len(rows) != 1:"
NEW = "if len(rows) > 1:"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location("kengaku_r37_c1", lane / "plans/round37_c1_verify.py")
    c = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c)
    gate_src = (lane / c.GATE_REL).read_text()
    assert gate_src.count(OLD) == 1
    r36 = c.load_r36(lane)
    ctx = c.Ctx(lane, r36)
    gates = work / "gates"
    gates.mkdir(exist_ok=True)
    ref_gate, n1_gate = gates / "ref.py", gates / "n1.py"
    ref_gate.write_text(gate_src)
    n1_gate.write_text(gate_src.replace(OLD, NEW, 1))

    name = pathlib.PurePosixPath(ctx.spec["entry"]).name
    needle = f"| `knowledge/{name}` |"

    def build(label, drop_row, drop_file):
        d = work / label
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
        ctx.genuine_package(d)
        if drop_row:
            readme = d / ctx.spec["readme"]
            lines = readme.read_text().splitlines()
            hits = [i for i, l in enumerate(lines) if l.startswith(needle)]
            assert len(hits) == 1, hits
            del lines[hits[0]]
            readme.write_text("\n".join(lines) + "\n")
        if drop_file:
            (d / ctx.spec["entry"]).unlink()
        ctx.git_add(d)
        return ["package", "--root", str(d), "--require-clean-tree"]

    def detail(gate, argv):
        r = subprocess.run([sys.executable, str(gate), *argv, "--spec", str(ctx.spec_path)],
                           capture_output=True, text=True)
        return [l for l in r.stdout.splitlines() if l.startswith("P8 ")]

    cases = [("a-control", False, False), ("b-zero-index-row", True, False),
             ("c-unindexed-entry", True, True)]
    for label, drop_row, drop_file in cases:
        argv = build(label, drop_row, drop_file)
        ref, n1 = c.run_gate(ref_gate, ctx.spec_path, argv), c.run_gate(n1_gate, ctx.spec_path, argv)
        differs = "DIFFERS" if ref != n1 else "same"
        print(f"{label}: ref={ref} n1={n1} -> {differs}")
        print(f"  ref-P8: {detail(ref_gate, argv)}")
        print(f"  n1-P8 : {detail(n1_gate, argv)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""F37XMutP8 detail probe: the P8 line each new mutant produces on (a) the genuine package and (b) the
p8-index-row-missing-sid fixture, next to the reference line. Evidence for the kill attribution.
"""
from __future__ import annotations

import argparse
import importlib.util
import pathlib
import shutil
import subprocess
import sys

MUTANTS = [
    ("N2", 'elif not all(sid in rows[0] for sid in p.spec["rows"]):',
     'elif not any(sid in rows[0] for sid in p.spec["rows"]):'),
    ("N3", 'elif not all(sid in rows[0] for sid in p.spec["rows"]):',
     'elif not all(sid in rows[0] for sid in list(p.spec["rows"])[:1]):'),
    ("N4", 'INDEX_ROW = re.compile(r"^\\|\\s*`(knowledge/[^`]+\\.md)`\\s*\\|")',
     'INDEX_ROW = re.compile(r".*?(knowledge/[^`]+\\.md)")'),
]


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
    r36 = c.load_r36(lane)
    ctx = c.Ctx(lane, r36)
    gdir = work / "gates"
    gdir.mkdir(exist_ok=True)
    gates = {"ref": gdir / "ref.py"}
    gates["ref"].write_text(gate_src)
    for mid, old, new in MUTANTS:
        assert gate_src.count(old) == 1, mid
        gates[mid] = gdir / f"{mid}.py"
        gates[mid].write_text(gate_src.replace(old, new, 1))

    def detail(gate, argv):
        r = subprocess.run([sys.executable, str(gate), *argv, "--spec", str(ctx.spec_path)],
                           capture_output=True, text=True)
        return [l for l in r.stdout.splitlines() if l.startswith("P8 ")]

    generic = work / "genuine"
    if generic.exists():
        shutil.rmtree(generic)
    generic.mkdir(parents=True)
    ctx.genuine_package(generic)
    ctx.git_add(generic)
    gargv = ["package", "--root", str(generic), "--require-clean-tree"]

    bdir = lane / c.BATTERY_REL
    p8fx = [fx for fx in c.battery37_fixtures(bdir) if fx["fid"] == "p8-index-row-missing-sid"][0]
    sid_dir = work / "missing-sid"
    if sid_dir.exists():
        shutil.rmtree(sid_dir)
    sid_dir.mkdir(parents=True)
    sargv = list(p8fx["build"](ctx, sid_dir))

    for label, argv in (("genuine-package", gargv), ("p8-index-row-missing-sid", sargv)):
        print(f"[{label}] tuple ref={c.run_gate(gates['ref'], ctx.spec_path, argv)}")
        for mid, _o, _n in MUTANTS:
            print(f"  {mid} tuple={c.run_gate(gates[mid], ctx.spec_path, argv)}")
        for name in ("ref", "N2", "N3", "N4"):
            print(f"  {name} P8: {detail(gates[name], argv)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Round-38 mined-mistake fix: does each frozen mutant's declared kill DIRECTION match what the battery can show?

Round 38 froze N21 (`sums.splitlines()` -> `sums.splitlines()[:1]` in the gate's D5 manifest lookup) as a
`silence` mutant. Restricting an `any(...)` lookup to a prefix makes the clause STRICTER, never laxer: on every
input the mutant's DEFECT set contains the reference's, so no fixture can satisfy the silence rule and the frozen
predicate `killed=22` was unreachable by any battery (wave-1 seat R38BatD5, `.ufo/waves/round-38/build/R38BatD5.md`).

This check re-uses a counter's own machinery (default `plans/round38_c1_verify.py`) and, for every frozen mutant and
every fixture of the clause's family, records which attributed directions the battery actually exhibits:

  silence  the reference prints the clause DEFECT and the mutant does not
  mirror   the reference prints the clause ok and the mutant prints it DEFECT
  main     (MAIN mutants) the reference exits 2 and the mutant exits 0/1

It prints one `DIR <id> <clause> declared=<dir> observed=<set>` line per mutant and flags `MISLABELLED` when the
declared direction is never observed but another one is. Exit 1 iff any mutant is MISLABELLED, else 0. A mutant
with no observed direction is `UNWITNESSED` (no fixture separates it yet), which is not a mislabel.

  python3 plans/mutant_direction_check.py --lane . [--counter plans/round38_c1_verify.py] [--work DIR]

Read-only on the lane; scratch under --work (default $TMPDIR via tempfile).
"""
import argparse
import importlib.util
import pathlib
import shutil
import sys
import tempfile


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--counter", default="plans/round38_c1_verify.py")
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    c = load(lane / a.counter, "kengaku_counter")
    r37 = load(lane / c.R37_REL, "kengaku_r37_c1")
    gate_src = (lane / r37.GATE_REL).read_text()
    r36 = r37.load_r36(lane)
    ctx = r37.Ctx(lane, r36)
    fixtures = r37.r36_fixtures(r36) + r37.battery37_fixtures(lane / r37.BATTERY_REL)
    fixtures += c.battery38_fixtures(lane / c.BATTERY38_REL)[0]
    root = pathlib.Path(tempfile.mkdtemp(prefix="k38-dir-", dir=a.work))
    try:
        built = []
        for i, fx in enumerate(fixtures):
            d = root / "fx" / f"f{i:03d}"
            d.mkdir(parents=True)
            built.append((fx, list(fx["build"](ctx, d))))
        gdir = root / "gates"
        gdir.mkdir()
        ref_gate = gdir / "ref.py"
        ref_gate.write_text(gate_src)
        ref = [c.run_gate(ref_gate, ctx.spec_path, argv) for _fx, argv in built]
        bad = 0
        for mid, clause, direction, _label, old, new in c.MUTANTS:
            if gate_src.count(old) != 1:
                print(f"DIR {mid} {clause} declared={direction} observed=invalid")
                continue
            mg = gdir / f"{mid}.py"
            mg.write_text(gate_src.replace(old, new, 1))
            seen = set()
            for j, (fx, argv) in enumerate(built):
                fam = c.FAMILY.get(clause, "package")
                if clause != "MAIN" and argv[0] != fam:
                    continue
                mut = c.run_gate(mg, ctx.spec_path, argv)
                for dname in ("silence", "mirror"):
                    if clause != "MAIN" and c.attributed(clause, dname, fx, argv, ref[j], mut):
                        seen.add(dname)
                if clause == "MAIN" and c.attributed(clause, direction, fx, argv, ref[j], mut):
                    seen.add(direction)
            if direction in seen:
                verdict = "ok"
            elif seen:
                verdict = "MISLABELLED"
                bad += 1
            else:
                verdict = "UNWITNESSED"
            print(f"DIR {mid} {clause} declared={direction} observed={','.join(sorted(seen)) or '-'} {verdict}")
        print(f"DIRECTIONS total={len(c.MUTANTS)} mislabelled={bad}")
        return 1 if bad else 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

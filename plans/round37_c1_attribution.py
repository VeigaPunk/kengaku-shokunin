#!/usr/bin/env python3
"""Round-37 post-hoc audit (NOT the frozen C1 rule): is every kill of the frozen C1 counter attributed?

The frozen counter `plans/round37_c1_verify.py` counts a mutant killed when ANY fixture's result
(exit code, set of clauses printing DEFECT) differs from the unmodified gate's. Wave 1 showed that rule is
satisfiable without exercising the advertised branches (`.ufo/waves/round-37/build/R37CritC1Battery.md`).
This audit re-uses the counter's own machinery and asks, per mutant, whether at least one fixture kills it
ATTRIBUTABLY:

  * the fixture declares the mutant's clause in its `defects` (or, for an unlabelled round-36 fixture, the
    reference run prints that clause as DEFECT);
  * the reference run prints the mutant's clause as DEFECT and the mutant run does not;
  * the fixture's subcommand matches the clause family (`package` for P*, `d4-line` for D4, `d5-line` for D5);
  * the mutant run's exit code is 0 or 1 (a crash or timeout is never an attributed kill).

Prints one `ATTR <mid> ...` line per mutant and `ATTRIBUTED <n>/<total> UNATTRIBUTED=<m>`; exit 0 iff every
mutant is attributed. Read-only on the lane; scratch under --work (default $TMPDIR).

  python3 plans/round37_c1_attribution.py --lane . [--work DIR]
"""
import argparse
import importlib.util
import pathlib
import shutil
import sys
import tempfile

FAMILY = {"D4": "d4-line", "D5": "d5-line"}


def load_counter(lane):
    spec = importlib.util.spec_from_file_location("kengaku_r37_c1", lane / "plans/round37_c1_verify.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    c = load_counter(lane)
    gate_src = (lane / c.GATE_REL).read_text()
    if c.sha256(lane / c.GATE_REL) != c.GATE_SHA256:
        print("SETUP gate not at its freeze digest", file=sys.stderr)
        return 2
    r36 = c.load_r36(lane)
    ctx = c.Ctx(lane, r36)
    fixtures = c.r36_fixtures(r36) + c.battery37_fixtures(lane / c.BATTERY_REL)
    root = pathlib.Path(tempfile.mkdtemp(prefix="k37-attr-", dir=a.work))
    try:
        built = []
        for i, fx in enumerate(fixtures):
            d = root / "fx" / f"f{i:03d}"
            d.mkdir(parents=True)
            built.append((fx, d, list(fx["build"](ctx, d))))
        gdir = root / "gates"
        gdir.mkdir()
        ref_gate = gdir / "ref.py"
        ref_gate.write_text(gate_src)
        ref = [c.run_gate(ref_gate, ctx.spec_path, argv) for _fx, _d, argv in built]
        attributed = 0
        for mid, clause, label, old, new in c.MUTANTS:
            mg = gdir / f"{mid}.py"
            mg.write_text(gate_src.replace(old, new, 1))
            fam = FAMILY.get(clause, "package")
            hit = None
            for j, (fx, _d, argv) in enumerate(built):
                if argv[0] != fam or clause not in ref[j][1]:
                    continue
                if fx.get("defects") is not None and clause not in fx["defects"]:
                    continue
                rc, bad = c.run_gate(mg, ctx.spec_path, argv)
                if rc in (0, 1) and clause not in bad:
                    hit = fx["fid"]
                    break
            attributed += hit is not None
            print(f"ATTR {mid} {clause} {'by=' + hit if hit else 'UNATTRIBUTED'} -- {label}")
        total = len(c.MUTANTS)
        print(f"ATTRIBUTED {attributed}/{total} UNATTRIBUTED={total - attributed}")
        return 0 if attributed == total else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

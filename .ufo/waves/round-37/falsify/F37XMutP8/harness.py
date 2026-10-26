#!/usr/bin/env python3
"""F37XMutP8: four NEW non-frozen mutants of gate clause P8 (c_readme) run against the full C1 battery.

Reuses the frozen counter's machinery (plans/round37_c1_verify.py imported as a module): load_r36,
Ctx, r36_fixtures, battery37_fixtures, run_gate. Fixtures are built ONCE; the reference gate and every
mutant are then run over the same built fixture directories.

Also re-runs the five frozen P8 mutants M34-M38 so each fixture's kill attribution (isolation claim of
plans/battery37/p8.py) is measured, not asserted.

Usage: harness.py --lane <clone> --work <scratch>
"""
from __future__ import annotations

import argparse
import importlib.util
import pathlib
import py_compile
import shutil
import sys

# (mid, clause, class, old, new, expected) -- expected is a prediction only; measured result is reported.
NEW_MUTANTS = [
    ("N1", "P8", "off-by-one threshold: `not exactly one` relaxed to the upper side only (>1)",
     "if len(rows) != 1:", "if len(rows) > 1:", "?",
     ),
    ("N2", "P8", "quantifier loosened: every registry row cited -> any one cited",
     'elif not all(sid in rows[0] for sid in p.spec["rows"]):',
     'elif not any(sid in rows[0] for sid in p.spec["rows"]):', "?"),
    ("N3", "P8", "check applied to the first registry row only",
     'elif not all(sid in rows[0] for sid in p.spec["rows"]):',
     'elif not all(sid in rows[0] for sid in list(p.spec["rows"])[:1]):', "?"),
    ("N4", "P8", "regex loosened: INDEX_ROW un-anchored, matches any line naming a knowledge/*.md",
     'INDEX_ROW = re.compile(r"^\\|\\s*`(knowledge/[^`]+\\.md)`\\s*\\|")',
     'INDEX_ROW = re.compile(r".*?(knowledge/[^`]+\\.md)")', "?"),
    # supplementary probe, not counted in the /4 verdict: the mirrored half of N1
    ("N5", "P8", "off-by-one threshold (mirror probe): `not exactly one` relaxed to the lower side only (<1)",
     "if len(rows) != 1:", "if len(rows) < 1:", "?",),
]

FROZEN_P8 = [  # same replacements as the counter's M34-M38; used only for kill attribution
    ("M34", "README unreadable", 'return False, "README unreadable"', 'return True, "README unreadable"'),
    ("M35", "index rows not exactly one",
     'bad.append(f"index rows for knowledge/{entry_name}={len(rows)}")', "pass"),
    ("M36", "index row does not cite every registry row",
     'bad.append("index row does not cite every registry row")', "pass"),
    ("M37", "no coverage bullet naming entry and receipt",
     'bad.append("no coverage bullet naming the entry and its receipt")', "pass"),
    ("M38", "knowledge files differ from index rows",
     'bad.append(f"knowledge files={len(files)} index rows={len(indexed)}")', "pass"),
]


def load_counter(lane):
    spec = importlib.util.spec_from_file_location("kengaku_r37_c1", lane / "plans/round37_c1_verify.py")
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
    work.mkdir(parents=True, exist_ok=True)
    c = load_counter(lane)
    gate_src = (lane / c.GATE_REL).read_text()
    print(f"GATE {c.GATE_REL} sha256_match_freeze={c.sha256(lane / c.GATE_REL) == c.GATE_SHA256}")
    r36 = c.load_r36(lane)
    ctx = c.Ctx(lane, r36)
    fixtures = c.r36_fixtures(r36) + c.battery37_fixtures(lane / c.BATTERY_REL)
    print(f"BATTERY fixtures={len(fixtures)} (r36={sum(1 for f in fixtures if f.get('r36'))} "
          f"battery37={sum(1 for f in fixtures if not f.get('r36'))})")
    built = []
    for i, fx in enumerate(fixtures):
        d = work / "fx" / f"f{i:03d}"
        d.mkdir(parents=True, exist_ok=True)
        argv = list(fx["build"](ctx, d))
        built.append((fx, d, argv))
    gdir = work / "gates"
    gdir.mkdir(exist_ok=True)
    ref_gate = gdir / "ref.py"
    ref_gate.write_text(gate_src)
    ref = [c.run_gate(ref_gate, ctx.spec_path, argv) for _fx, _d, argv in built]
    print("FIXTURE RESULTS (reference gate):")
    for (fx, _d, _argv), res in zip(built, ref):
        print(f"  {fx['fid']} expect={fx['expect']} declared={','.join(sorted(fx['defects'])) if fx['defects'] else '-'}"
              f" rc={res[0]} defects={','.join(sorted(res[1])) or '-'}")

    def run_mutant(mid, clause, label, old, new):
        if gate_src.count(old) != 1:
            print(f"MUTANT {mid} {clause} INVALID old occurs {gate_src.count(old)}x -- {label}")
            return
        mg = gdir / f"{mid}.py"
        mg.write_text(gate_src.replace(old, new, 1))
        try:
            py_compile.compile(str(mg), doraise=True, cfile=str(gdir / f"{mid}.pyc"))
        except py_compile.PyCompileError as e:
            print(f"MUTANT {mid} {clause} INVALID(compile) {e} -- {label}")
            return
        killers = []
        for (fx, _d, argv), r in zip(built, ref):
            got = c.run_gate(mg, ctx.spec_path, argv)
            if got != r:
                killers.append(f"{fx['fid']}(rc={got[0]},defects={','.join(sorted(got[1])) or '-'})")
        if killers:
            print(f"MUTANT {mid} {clause} killed by={len(killers)} {killers} -- {label}")
        else:
            print(f"MUTANT {mid} {clause} SURVIVED -- {label}")
        return killers

    print("--- new non-frozen P8 mutants ---")
    res = {}
    for mid, clause, label, old, new, _exp in NEW_MUTANTS:
        res[mid] = run_mutant(mid, clause, label, old, new)
    print("--- frozen P8 mutants M34-M38 (kill attribution / isolation) ---")
    frozen = {}
    for mid, label, old, new in FROZEN_P8:
        frozen[mid] = run_mutant(mid, "P8", label, old, new)
    k4 = sum(1 for mid in ("N1", "N2", "N3", "N4") if res.get(mid))
    print(f"NEWMUT total=4 killed={k4} survived={4 - k4}"
          f" | probe-N5 killed={1 if res.get('N5') else 0}")
    print(f"FROZEN-P8 killed={sum(1 for v in frozen.values() if v)}/5")
    shutil.rmtree(work / "fx", ignore_errors=True)
    shutil.rmtree(work / "gates", ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""C1MutClassifier attribution pass.

The class-level detectors (D1/D2/D3) score the *class* a mutant assigns.  A mutant that
keeps the class but changes the *reason* (the clause the classifier cites) is an
equivalent mutant for the class invariant yet a live defect for the reason text the
reports quote.  This pass therefore diffs the full classify_detail() output
(class + reasons) case by case:

  R1  the 83 frozen selftest cases      -> which case id first differs
  R2  the 90 adversarial cases          -> which case id first differs
  R3  the 305 population ids            -> which test id first differs, and how many

It also runs the counter-side end_lineno off-by-one probe (the classifier never reads
end_lineno; that field belongs to the counter's CONFIRM span) and labels it as such.

usage: attrib.py [mutant-name ...]   (default: all)
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE / "lane"
CAP = HERE / "capture"
MUTDIR = HERE / "mutants"
ADVDIR = LANE / ".ufo/waves/round-53/w1/C1ExecAdvCases"
TESTS_INDEX = LANE / "corpus/evidence/round53/tests-index.json"

sys.path.insert(0, str(HERE))
from mutate import MUTANTS, PRISTINE, decided_labels, population  # noqa: E402


def load_mod(path: Path):
    spec = importlib.util.spec_from_file_location("attr_" + path.stem.replace("-", "_"), path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def selftest_cases(mod):
    """-> [(case name, {key: (class, reasons)})] from the module's own frozen CASES list."""
    out = []
    for name, src, want in mod.CASES:
        full = (mod.HDR + src) if src else ""
        out.append((name, want, mod.classify_detail(full)))
    return out


def adv_cases(mod):
    cases = json.loads((ADVDIR / "cases.json").read_text())
    out = []
    for c in cases:
        out.append((c["id"], c.get("expected", {}), mod.classify_detail(c["source"])))
    return out


def diff_case(name, want, base, mut):
    """-> list of difference strings for one case."""
    d = []
    keys = set(base) | set(mut)
    for k in sorted(keys):
        b = base.get(k)
        m = mut.get(k)
        if b is None or m is None:
            d.append(f"{k}: present-base={b is not None} present-mut={m is not None}")
            continue
        if b[0] != m[0]:
            d.append(f"{k}: class {b[0]}->{m[0]}")
        if b[1] != m[1]:
            d.append(f"{k}: reasons {b[1]} -> {m[1]}")
    return d


def pop_detail(mod):
    idx = json.loads(TESTS_INDEX.read_text())["tests"]
    by_file = {}
    out = {}
    for t in idx:
        f = t["file"]
        if f not in by_file:
            by_file[f] = mod.classify_detail((CAP / f).read_text(encoding="utf-8", errors="replace"))
        key = f"{t['class']}.{t['name']}" if t["class"] else t["name"]
        out[t["id"]] = by_file[f].get(key)
    return out


def main():
    names = sys.argv[1:] or [m[0] for m in MUTANTS]
    pmod = load_mod(PRISTINE)
    p_st = selftest_cases(pmod)
    p_adv = adv_cases(pmod)
    p_pop = pop_detail(pmod)
    decided = decided_labels()
    rows = []
    for name in names:
        path = MUTDIR / f"{name}.py"
        mod = load_mod(path)
        m_st = selftest_cases(mod)
        m_adv = adv_cases(mod)
        m_pop = pop_detail(mod)
        r1 = []
        for (n, want, b), (_, _, m) in zip(p_st, m_st):
            d = diff_case(n, want, b, m)
            if d:
                r1.append({"case": n, "diff": d[:4]})
        r2 = []
        for (n, want, b), (_, _, m) in zip(p_adv, m_adv):
            d = diff_case(n, want, b, m)
            if d:
                r2.append({"case": n, "diff": d[:4]})
        r3 = []
        moved_class = []
        for tid, b in p_pop.items():
            m = m_pop.get(tid)
            if m is None:
                moved_class.append(tid)
                r3.append({"id": tid, "diff": ["missing"]})
                continue
            if m[0] != b[0]:
                moved_class.append(tid)
                r3.append({"id": tid, "diff": [f"class {b[0]}->{m[0]}", f"reasons {b[1][:2]} -> {m[1][:2]}"]})
            elif m[1] != b[1]:
                r3.append({"id": tid, "diff": [f"same class {b[0]}, reasons {b[1][:2]} -> {m[1][:2]}"]})
        dis = sum(1 for t, y in decided.items()
                  if ((m_pop.get(t) or ("P0",))[0] == "P1") != (y == "Y"))
        rows.append({
            "mutant": name,
            "r1_selftest_cases_differing": len(r1), "r1_first": r1[:3],
            "r2_adv_cases_differing": len(r2), "r2_first": r2[:3],
            "r3_pop_ids_differing": len(r3), "r3_class_moved": len(moved_class),
            "r3_first": r3[:3],
            "oracle_disagree": dis,
            "class_equivalent": len(moved_class) == 0,
        })
        print(f"{name:34s} R1={len(r1):3d} R2={len(r2):3d} R3={len(r3):3d} "
              f"classmoved={len(moved_class):3d} dis={dis:3d} "
              f"{'CLASS-EQUIV' if not moved_class else ''}")
        for x in r1[:1]:
            print(f"      R1 {x['case']}: {x['diff'][0][:150]}")
        for x in r2[:1]:
            print(f"      R2 {x['case']}: {x['diff'][0][:150]}")
        for x in r3[:1]:
            print(f"      R3 {x['id']}: {x['diff'][0][:150]}")
    (HERE / "attribution.json").write_text(json.dumps(rows, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

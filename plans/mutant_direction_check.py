#!/usr/bin/env python3
"""Round-39 fix of the round-38 mined-mistake fix: does each frozen mutant's declared kill DIRECTION match what
the battery can show -- with TWO independent legs, so a one-line edit to one leg cannot silence the signal?

Round 38 froze N21 (`sums.splitlines()` -> `sums.splitlines()[:1]` in the gate's D5 manifest lookup) as a
`silence` mutant. Restricting an `any(...)` lookup to a prefix makes the clause STRICTER, never laxer: on every
input the mutant's DEFECT set contains the reference's, so no fixture can satisfy the silence rule and the frozen
predicate `killed=22` was unreachable by any battery (wave-1 seat R38BatD5, `.ufo/waves/round-38/build/R38BatD5.md`).

This check re-uses a counter's own machinery (default `plans/round38_c1_verify.py`) and, for every frozen mutant and
every fixture of the clause's family, records which attributed directions the battery actually exhibits:

  silence  the reference prints the clause DEFECT and the mutant does not
  mirror   the reference prints the clause ok and the mutant prints it DEFECT
  main     (MAIN mutants) the reference exits 2 and the mutant exits 0/1

Round-38 mutation testing (`F38MutDirection` m1, m2) showed the verdict above was a single point of failure: dropping
the `mirror` observation (m1) or accepting any observation as the declared one (m2) turned the landed run green
(exit 0) with no other line changing. The fix is a second, independently written derivation of the same witness set
(`second_leg`, computed from the raw `(rc, DEFECT set, ok set)` triples, sharing no loop, no `dname` and no call into
the counter's `attributed` with the first leg). Each leg decides on its own and the printed verdict is the
stronger of the two: `MISLABELLED` from either leg is the verdict, `ok` only when both legs say `ok`, and
`LEGS-DISAGREE` when one leg cannot decide (`ok` vs `UNWITNESSED`) -- the instrument reds (exit 3) instead of
passing a mutant it cannot vouch for. A surviving mutant is a coverage finding, not permission to relabel the
frozen claim.

It prints one `DIR <id> <clause> declared=<dir> observed=<set>` line per mutant and flags `MISLABELLED` when the
declared direction is never observed but another one is (either leg suffices); `legs=<a>,<b>` is appended when the
two legs did not agree. Exit 1 iff any mutant is MISLABELLED (QUALITY Q29 unchanged); exit 3 when no mutant is
mislabelled but the instrument cannot decide -- a frozen row no longer matches the gate once (`INVALID`) or the
legs disagree without a mislabel; exit 0 otherwise. A mutant with no observed direction is `UNWITNESSED` (no
fixture separates it yet), which is not a mislabel -- unchanged round-38 policy.
A setup failure (work parent missing, unreadable counter, a counter of another list) exits 2, never 1 or 3.

  python3 plans/mutant_direction_check.py --lane . [--counter plans/round38_c1_verify.py] [--work DIR]

`--counter` must expose the round-38 list surface (`battery38_fixtures`, `attributed`, `FAMILY`, 6-column
`MUTANTS` rows); a counter with a different list -- e.g. `plans/round39_c1_verify.py`, whose fixtures load in a
child process and whose rows carry a witness column -- exits 2 naming the missing surface, never an AttributeError.

Read-only on the lane; scratch under --work (default $TMPDIR via tempfile), removed on exit.
"""
import argparse
import importlib.util
import pathlib
import shutil
import sys
import tempfile

FAMILY = {"D4": "d4-line", "D5": "d5-line"}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def second_leg(clause, direction, fx, argv, ref, mut):
    """Independent derivation of the directions this fixture witnesses for `clause`.

    Built from the raw `(rc, DEFECT set, ok set)` triples of the reference and mutant runs only: it does not call
    the counter's `attributed`, shares no collection loop with the first leg and names no `dname`. Deliberately
    redundant -- the first leg's `silence`/`mirror` branches can be edited away and this leg still reports.
    """
    sub = FAMILY.get(clause)
    if sub is not None and argv[0] != sub:
        return ()
    if clause == "MAIN":
        if fx.get("expect") == "error" and ref[0] == 2 and mut[0] in (0, 1):
            return (direction,)
        return ()
    if ref[0] not in (0, 1) or mut[0] not in (0, 1):
        return ()
    declared = set(fx["defects"]) if fx.get("defects") is not None else set(ref[1])
    found = []
    if clause == "RUN":
        if any(c in ref[1] and c not in mut[1] for c in declared):
            return ("silence", "mirror")
        return ()
    if clause in ref[1] and clause not in mut[1] and clause in declared:
        found.append("silence")
    if clause in ref[2] and clause in mut[1]:
        found.append("mirror")
    return tuple(found)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--counter", default="plans/round38_c1_verify.py")
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    try:
        c = load(lane / a.counter, "kengaku_counter")
        missing = [n for n in ("R37_REL", "battery38_fixtures", "attributed", "FAMILY", "MUTANTS") if not hasattr(c, n)]
        rows = [m for m in getattr(c, "MUTANTS", ()) if len(m) != 6]
        if missing or rows:
            print(f"SETUP counter {a.counter} is not a round-38-list counter: missing={','.join(missing) or '-'} "
                  f"non_6_tuple_rows={len(rows)}; this check reads the round-38 MUTANTS rows "
                  f"(id, clause, dir, adv, old, new) and its battery38 loader only", file=sys.stderr)
            return 2
        r37 = load(lane / c.R37_REL, "kengaku_r37_c1")
        gate_src = (lane / r37.GATE_REL).read_text()
        r36 = r37.load_r36(lane)
        ctx = r37.Ctx(lane, r36)
        fixtures = r37.r36_fixtures(r36) + r37.battery37_fixtures(lane / r37.BATTERY_REL)
        fixtures += c.battery38_fixtures(lane / c.BATTERY38_REL)[0]
        root = pathlib.Path(tempfile.mkdtemp(prefix="k38-dir-", dir=a.work))
    except (OSError, AttributeError, ImportError) as e:
        print(f"SETUP {type(e).__name__}: {e}", file=sys.stderr)
        return 2
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
        mis = split = invalid = 0
        for mid, clause, direction, _label, old, new in c.MUTANTS:
            if gate_src.count(old) != 1:
                print(f"DIR {mid} {clause} declared={direction} observed=invalid INVALID")
                invalid += 1
                continue
            mg = gdir / f"{mid}.py"
            mg.write_text(gate_src.replace(old, new, 1))
            seen = set()
            other = set()
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
                other.update(second_leg(clause, direction, fx, argv, ref[j], mut))
            # leg 1: the round-38 rule, kept verbatim so a one-line edit to it stays measurable
            if direction in seen:
                first = "ok"
            elif seen:
                first = "MISLABELLED"
            else:
                first = "UNWITNESSED"
            # leg 2: the same question answered from the independent derivation; never shares leg 1's branch
            if direction in other:
                second = "ok"
            elif other:
                second = "MISLABELLED"
            else:
                second = "UNWITNESSED"
            if "MISLABELLED" in (first, second):
                # either leg finding the mislabel is the mislabel: one destroyed leg cannot silence it
                verdict = "MISLABELLED"
                mis += 1
            elif first == second:
                verdict = first
            else:
                # ok vs unwitnessed only: the instrument cannot decide, which is not a verdict about the mutant
                verdict = "LEGS-DISAGREE"
                split += 1
            observed = seen | other
            print(f"DIR {mid} {clause} declared={direction} observed={','.join(sorted(observed)) or '-'} {verdict}"
                  + ("" if first == second else f" legs={first},{second}"))
        print(f"LEGS mutants={len(c.MUTANTS)} disagree={split} invalid={invalid}")
        print(f"DIRECTIONS total={len(c.MUTANTS)} mislabelled={mis}")
        return 1 if mis else (3 if (split or invalid) else 0)
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

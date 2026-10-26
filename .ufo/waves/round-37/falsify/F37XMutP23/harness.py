#!/usr/bin/env python3
"""F37XMutP23 (round-37 wave-2 critic): four NEW, non-frozen mutants of the P2/P3 branch of
`plans/pkg_gate.py`, run against the full round-37 battery.

Reuses the frozen counter's machinery (imported as a module, not copied):
load_r36, Ctx, r36_fixtures, battery37_fixtures, CLAUSE_LINE, GATE_SHA256, sha256.

Fixtures are built ONCE; every gate (reference, the four new mutants, the seven frozen M02-M08 as a
harness anchor) runs over the identical built fixture directories, and each sweep parallelises over
fixtures so no two gate runs ever share one directory (P10's probe runs with cwd=root).

  harness.py LANE WORK
"""
from __future__ import annotations

import concurrent.futures
import importlib.util
import pathlib
import py_compile
import re
import subprocess
import sys

P23 = ("p23-p2-receipt-deleted", "p23-p2-receipt-byte", "p23-p3-heading-renamed",
       "p23-p3-seven-texts", "p23-p3-seven-locations", "p23-p3-two-word-quote")

# (id, clause, label, old, new) — new, not in round37_c1_verify.MUTANTS.
NEW = [
    ("X1", "P3", "min_quotes lowered by one (off-by-one threshold)",
     'len(texts) >= rules["min_quotes"]',
     'len(texts) >= rules["min_quotes"] - 1'),
    ("X2", "P3", "min_distinct_locations '>=' -> '>'",
     'len(locs) >= rules["min_distinct_locations"]',
     'len(locs) > rules["min_distinct_locations"]'),
    ("X3", "P3", "word-range check applied to the first quote row only",
     'short = [q.text[:30] for q in p.quotes if not lo <= q.words <= hi]',
     'short = [q.text[:30] for q in p.quotes[:1] if not lo <= q.words <= hi]'),
    ("X4", "P3", "bad-rows count off-by-one ('any bad row' -> 'more than one bad row')",
     "if p.bad_rows:",
     "if len(p.bad_rows) > 1:"),
]


# supplementary probes: same clause, reported separately from the required four.
SUPP = [
    ("Y1", "P3", "quote table parsed with only its first data row",
     "for line in rows[1:]:  # rows[0] is the header",
     "for line in rows[1:2]:  # rows[0] is the header"),
    ("Y2", "P3", "upper word bound off-by-one (hi -> hi+1)",
     "if not lo <= q.words <= hi]", "if not lo <= q.words <= hi + 1]"),
    ("Y3", "P3", "min_quotes '>=' -> '>' (equality boundary)",
     'len(texts) >= rules["min_quotes"]', 'len(texts) > rules["min_quotes"]'),
    ("Y4", "P3", "QUOTE_ROW quote text loosened, an empty quote parses",
     "“(.+?)”", "“(.*?)”"),
    ("Y5", "P3", "no-section branch reordered behind the bad-rows branch (unreachable)",
     "    if p.quote_section is None:\n        return False, \"no '## Located quotes' section\"\n"
     "    if p.bad_rows:\n        return False, f\"unparsed_rows={len(p.bad_rows)} first={p.bad_rows[0][:70]!r}\"",
     "    if p.bad_rows:\n        return False, f\"unparsed_rows={len(p.bad_rows)} first={p.bad_rows[0][:70]!r}\"\n"
     "    if p.bad_rows and p.quote_section is None:\n        return False, \"no '## Located quotes' section\""),
    ("Y6", "P3", "bad-rows count off-by-one upward ('more than two')",
     "if p.bad_rows:", "if len(p.bad_rows) > 2:"),
    ("Z1", "P2", "receipt digest compared on the first 8 hex digits only (expected INERT: avalanche)",
     'return got == want, f"receipt_sha256=',
     'return got[:8] == want[:8], f"receipt_sha256='),
]


def run(gate, spec_path, argv):
    r = subprocess.run([sys.executable, str(gate), *argv, "--spec", str(spec_path)],
                       capture_output=True, text=True, timeout=900)
    bad = frozenset(m.group(1) for m in map(COUNTER.CLAUSE_LINE.match, r.stdout.splitlines())
                    if m and m.group(2) == "DEFECT")
    return r.returncode, bad, r.stdout


COUNTER = None


def main():
    global COUNTER
    lane = pathlib.Path(sys.argv[1]).resolve()
    work = pathlib.Path(sys.argv[2]).resolve()
    c1 = COUNTER = load_counter_for(lane)
    r36, Ctx = c1.load_r36(lane), c1.Ctx
    ctx = Ctx(lane, r36)
    gate_src = (lane / "plans" / "pkg_gate.py").read_text()
    frozen = c1.sha256(lane / "plans" / "pkg_gate.py") == c1.GATE_SHA256
    print(f"LANE {lane}\nGATE_SHA256 {c1.sha256(lane / 'plans' / 'pkg_gate.py')} frozen={frozen}")
    if not frozen:
        return 2
    fixtures = c1.r36_fixtures(r36) + c1.battery37_fixtures(lane / "plans" / "battery37")
    print(f"BATTERY fixtures={len(fixtures)} p23={sum(f['fid'] in P23 for f in fixtures)}")

    root = work / "run"
    if root.exists():
        import shutil
        shutil.rmtree(root)
    built = []
    for i, fx in enumerate(fixtures):
        d = root / "fx" / f"f{i:03d}"
        d.mkdir(parents=True)
        argv = list(fx["build"](ctx, d))
        assert argv and argv[0] in ("package", "d4-line", "d5-line") and "--spec" not in argv, fx["fid"]
        built.append((fx, d, argv))
    gdir = root / "gates"
    gdir.mkdir()
    ref_gate = gdir / "ref.py"
    ref_gate.write_text(gate_src)

    def sweep(gate, label):
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
            futs = [ex.submit(run, gate, ctx.spec_path, argv) for _fx, _d, argv in built]
            return [f.result() for f in futs]

    ref = sweep(ref_gate, "ref")
    wrong = []
    for (fx, _d, _argv), res in zip(built, ref):
        want_rc = 0 if fx["expect"] == "accept" else 1
        declared = fx.get("defects")
        ok = res[0] == want_rc and (declared is None or res[1] == frozenset(declared))
        if fx["expect"] == "accept":
            ok = ok and not res[1]
        if not ok:
            wrong.append((fx["fid"], fx["expect"], declared, res[0], sorted(res[1])))
    print(f"BATTERY_CHECK wrong={len(wrong)}")
    for w in wrong:
        print(f"  WRONG {w}")
    print("P23_DECLARATION_TABLE")
    for i, (fx, d, argv) in enumerate(built):
        if fx["fid"] not in P23:
            continue
        res = ref[i]
        print(f"  {fx['fid']} declared={','.join(sorted(fx['defects']))} rc={res[0]} "
              f"observed={','.join(sorted(res[1])) or '-'} rerun={'--rerun' in argv}")
        for line in res[2].splitlines():
            if re.match(r"^P[234] (ok|DEFECT) ", line):
                print(f"    {line}")

    def evaluate(mid, clause, label, old, new):
        if gate_src.count(old) != 1:
            print(f"NEWMUT {mid} {clause} INVALID old occurs {gate_src.count(old)}x -- {label}")
            return None
        mg = gdir / f"{mid}.py"
        mg.write_text(gate_src.replace(old, new, 1))
        try:
            py_compile.compile(str(mg), doraise=True, cfile=str(gdir / f"{mid}.pyc"))
        except py_compile.PyCompileError as e:
            print(f"NEWMUT {mid} {clause} INVALID compile -- {label}: {e}")
            return None
        res = sweep(mg, mid)
        changed = [built[j][0]["fid"] for j in range(len(built)) if (res[j][0], res[j][1]) != (ref[j][0], ref[j][1])]
        if changed:
            print(f"NEWMUT {mid} {clause} killed by={','.join(changed)} -- {label}")
        else:
            print(f"NEWMUT {mid} {clause} SURVIVED (0 of {len(built)} fixtures differ) -- {label}")
        return {built[j][0]["fid"]: (res[j][0], sorted(res[j][1])) for j in range(len(built))}, changed

    print("--- frozen anchor M02-M08 (harness agreement with the frozen counter) ---")
    anchor = {}
    for mid, clause, label, old, new in c1.MUTANTS:
        if clause not in ("P2", "P3"):
            continue
        r = evaluate(mid, clause, label, old, new)
        if r:
            anchor[mid] = set(r[1])
    print("--- new mutants ---")
    survivors = 0
    killed = 0
    for mid, clause, label, old, new in NEW:
        r = evaluate(mid, clause, label, old, new)
        if r is None:
            continue
        if r[1]:
            killed += 1
        else:
            survivors += 1
    print(f"NEWMUTANTS total={len(NEW)} killed={killed} survived={survivors}")
    print("--- supplementary probes (not part of the required four) ---")
    for mid, clause, label, old, new in SUPP:
        evaluate(mid, clause, label, old, new)

    print("--- p23 isolation matrix: frozen P2/P3 mutant x p23 fixture (K = result changed) ---")
    p23ids = [f for f in P23]
    print("  mutant  " + "  ".join(f[:22] for f in p23ids))
    for mid in ("M02", "M03", "M04", "M05", "M06", "M07", "M08"):
        if mid not in anchor:
            continue
        row = [("K" if p in anchor[mid] else ".") for p in p23ids]
        print(f"  {mid}      " + "  ".join(f"{c:<22}" for c in row))
    return 0


def load_counter_for(lane):
    spec = importlib.util.spec_from_file_location("k37c1", lane / "plans" / "round37_c1_verify.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


if __name__ == "__main__":
    sys.exit(main())

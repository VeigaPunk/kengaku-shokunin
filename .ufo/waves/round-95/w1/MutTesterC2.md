# MutTesterC2 — scoped findings (Kengaku round 95, wave 1)

Mutation test of `plans/round95_c2_counter.py` (sha256 `2fc2e7f0a1c26599…`) and
`plans/round95_false_gate_census.py` (sha256 `38fed2c23d46792e…`) at T
`afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239`, both equal to the frozen table at F. 20 single-site
counter mutants scored by the pristine census with `--counter <mutant>` (survivor = census prints
`PREDICATE R95-C2 pass`, rc 0), 7 single-site census mutants scored at T against the committed T
receipt and the two committed P2 control receipts. Baseline byte-reproduces
`.ufo/waves/round-95/L1/c2-tip.txt`; restoration re-run byte-identical; lane clone read-only
throughout. Full evidence: `.ufo/waves/round-95/w1/MutTesterC2/` (`report.md`, `receipts/`,
`mutants/`, `manifest.json`, `final_verdicts.json`).

Result: counter 6/20 killed, **14 survived**; census 1 killed at T (XM2), 1 killed by the
committed T receipt (XM6), 2 killed only by committed P2 control receipts (XM1, XM3),
**3 equivalence survivors** (XM4, XM5, XM7). No R95-C2 verdict at T is flipped; per the frozen
rule these route to round 96.

FINDING MUTC2-1 major — 13/20 counter mutants byte-identical at T and killed by no committed control: W1/W4/W5 gating removal (CM01-03), pred_ok multiplicity (CM05), CNE summary strictness (CM07), W3 probe acceptance `<=15`/rc-drop/predicate-drop (CM04, CM13-15), W1b tuple (CM17), W4 broken==0 (CM19), fixture refresh (CM16); the census observes only the W2 aggregate, the honest leg, and designated-red loss.
FINDING MUTC2-2 minor — W2 fixtures outside (census DESIGNATED ∪ W5 targets) are removable with only the unasserted `fixtures=` echo changing (CM06 executed on `w2-unrelated`, survived; class: `w2-intact`, `w2-unrelated`, `w2-edit-revert`, `w2-lying-table`); conversely census-undesignated `w2-second-block` is W5-load-bearing and its removal was killed (CM20, honest W5 leg).
FINDING MUTC2-3 major — census `designated_red` is fabricated-not-measured at T: `dred = 1` mutant byte-identical at T and satisfies the frozen predicate; killed only by the P2 do-nothing receipt (`designated_red=0` vs mutant 14, receipts `XM1-designated-forced.out` vs `controls/c2-census-do-nothing-r94-counter.txt`).
FINDING MUTC2-4 major — census honest-pass clause dead at T: dropping `honest == "pass"` from `ok` is byte-identical at T and satisfies the predicate; killed only by the P2 at-P1 receipt (`PREDICATE pass` rc 0 vs receipt fail rc 1, `XM3-honest-dropped.out` vs `controls/c2-census-at-P1.txt`).
FINDING MUTC2-5 minor — census row-sha check (XM4), population `!=` check (XM5) and PASS_LINE polarity (XM7) unobserved by any committed control (equivalence survivors).
FINDING MUTC2-6 info — receipt fields outside the frozen predicate (7 HONEST echo lines, `fixtures=20 ok=20`, `killed=10`) are recorded but asserted nowhere; XM6 and CM06 contradict the committed receipt byte-wise while satisfying the predicate.
FINDING MUTC2-7 info — validation: 6/20 counter + 4/7 census mutants killed; baseline byte-reproduces all three committed census receipts; restoration re-run byte-identical; lane clean at T before and after.

Harness note: battery.py first ran XM1/XM3's "at T" jobs at P1 (rev/counter leak); corrected
dedicated T runs are the `-T` receipts and `final_verdicts.json` is built from those; the
misaddressed P1 receipts double as the XM1/XM3 kill evidence.

Paths written:
- .ufo/waves/round-95/w1/MutTesterC2.md (this file)
- .ufo/waves/round-95/w1/MutTesterC2/report.md
- .ufo/waves/round-95/w1/MutTesterC2/{receipts,mutants}/ (33 census-run receipts; 27 mutant files)
- .ufo/waves/round-95/w1/MutTesterC2/{manifest.json,final_verdicts.json,verdicts.json,meta.json,battery.py,extra_runs.py}

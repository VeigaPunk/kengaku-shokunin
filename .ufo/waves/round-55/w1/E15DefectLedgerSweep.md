# E15DefectLedgerSweep — scoped findings (round-55 lesson input)

Measured 2026-10-30 on a clean shared clone of tip `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`.
Full evidence and commands: `E15DefectLedgerSweep/report.md` and
`E15DefectLedgerSweep/open-rows.md` beside this file.

## Verdict on the Q23 ledger at the tip

`python3 plans/defect_ledger.py --lane <clone>` exits 0 and prints, verbatim:

```
R34-D1 status=closed observed=pass agree=yes untracked=0
R34-D2 status=closed observed=pass agree=yes committed_mirror_paths=0
R34-D3 status=closed observed=pass agree=yes listed=6 evaluator_listed=True bad=0
R34-D4 status=closed observed=pass agree=yes correction_lines=1
R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True
rows=5 closed=5 observed_pass=5 mismatches=0
PREDICATE C2 pass
```

`corpus/defects.jsonl` open rows at tip: **0 of 5** (all R34 rows closed since round 35,
commit `dfcd294c`). Every named check was re-run by the ledger itself at the tip: 5 pass,
0 `agree=NO`, 0 closed-mismatches. Nothing to add for open rows — the set is empty.

## The r52-repair carry — exact state (discrepancy named)

The carry (refused E3 patch's order-check regression + masked K7 control) is **not a row of
`corpus/defects.jsonl`** and has **no check function** in `plans/defect_ledger.py`; it is an
open obligation in prose only:

- `corpus/lessons/round-54-verifier-spotcheck.md:123` (obligation 5, "stay open until fixed"),
- `SCORECARD.md:2373` ("Planned (round 55)": carry until fixed),
- `corpus/lessons/round-54.md:33` (Mistakes `unsafe-rider-integration`, evidence `w1/R4R52Fix.md`),
- `corpus/QUALITY.md:1168-1169` (Q44 refusal ruling).

Also absent from sibling `corpus/routed-findings.jsonl` (31 open rows; none name it). Its
executable proxy — registry row `round52-c2`'s self-test
(`python3 plans/round52_c2_registry.py --lane . --selftest`) — is green at tip
(`cases=3 failures=0`, exit 0) but still covers only clean/missing/incomplete; the K5 decoy
and K7 entry-missing controls and the negated-flag / false-selftest fixture classes remain
unexercised (`corpus/lessons/round-52.md:58`, `plans/round-52-claims.md:325-326`). The
production counter stays intentionally unchanged (`plans/round-55-claims.md:150`); full run at
tip still shows the R55-C1 before-surface (`MISSING 2`, exit 1). Round-55 reconstruction seats
R11R52Carry / RV3R52PatchAnatomy (dispatch :412, :662) had not yet written outputs when
measured.

## For the lesson

State to record: defects ledger fully green at the tip with zero open rows; the r52 carry is a
prose-carried obligation whose would-be check remains the 3-fixture r52 selftest — entering it
as a Q23 row is lane-side work blocked by the R39-R3 ledger pin, not this wave's.

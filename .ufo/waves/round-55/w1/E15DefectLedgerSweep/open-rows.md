# Open routed-defect rows at the round-55 tip — E15DefectLedgerSweep

Measured: 2026-10-30, clean shared clone of lane tip `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`
(freeze commit; clone under seat scratch, since deleted). Ledger instrument:
`plans/defect_ledger.py` (frozen round-35 C2 counter; reads `corpus/defects.jsonl`, re-runs every
row's named check forever; Q23 of `corpus/QUALITY.md`).

## Verbatim ledger run (item 1 capture)

Command: `python3 plans/defect_ledger.py --lane <clone>`

```
R34-D1 status=closed observed=pass agree=yes untracked=0
R34-D2 status=closed observed=pass agree=yes committed_mirror_paths=0
R34-D3 status=closed observed=pass agree=yes listed=6 evaluator_listed=True bad=0
R34-D4 status=closed observed=pass agree=yes correction_lines=1
R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True
rows=5 closed=5 observed_pass=5 mismatches=0
PREDICATE C2 pass
```

Exit code: **0**. The frozen round-35 predicate line (`rows=5 closed=5 observed_pass=5
mismatches=0`, `PREDICATE C2 pass`) is met at the tip.

## Table — every `corpus/defects.jsonl` row with status `open`

**There are none.** `corpus/defects.jsonl` holds exactly 5 rows (`wc -l = 5`), all opened round 34,
all `status: closed` since round 35 (ledger commit `dfcd294c`). Full row set for the record:

| id | class | check (defect_ledger.py fn) | ledger status | observed at tip | agree |
|---|---|---|---|---|---|
| R34-D1 | uncommitted-round-work | `r34_d1` | closed | pass (`untracked=0`) | yes |
| R34-D2 | committed-scratch-bloat | `r34_d2` | closed | pass (`committed_mirror_paths=0`) | yes |
| R34-D3 | receipt-claims-unbacked-manifest | `r34_d3` | closed | pass (`listed=6 evaluator_listed=True bad=0`) | yes |
| R34-D4 | scorecard-misattribution | `r34_d4` | closed | pass (`correction_lines=1`) | yes |
| R34-D5 | false-refusal-reason | `r34_d5` | closed | pass (`erratum_lines=1 r35_mistake_row=True`) | yes |

Open-row verification loop (seat item 3) is therefore **vacuous**: zero open rows → zero open-row
checks to re-run; zero `agree=NO` lines; no closed-mismatch anywhere. Evidence pointer for the
whole table: the verbatim run above, re-runnable as `python3 plans/defect_ledger.py --lane .`.

## The r52-repair carry (order-check regression + masked K7 control) — named exactly

**Discrepancy with the seat premise: the carry is NOT an open row of `corpus/defects.jsonl`, and
never has been.** It has no `id`, no `check` function in `plans/defect_ledger.py` (CHECKS =
`r34_d1`…`r34_d5` only), and no ledger state to re-run. `git log --all -- corpus/defects.jsonl`
shows the file touched only by rounds 34–35 (5 R34 rows; pinned against new rows by
`plans/ledger_tip.py`, itself pinned by `plans/round40_c1_verify.py:98` — recorded as routed row
R39-R3, status `blocked`). It is also absent from the sibling ledger
`corpus/routed-findings.jsonl` (85 rows, 31 `status: open`; `grep -i 'r52\|K7\|order-check
regression\|masked K7'` → zero hits) which belongs to `plans/routed_open.py`, not to
`defect_ledger.py`.

What the carry actually is at the tip — an **open obligation carried in prose**, at four loci:

1. `corpus/lessons/round-54-verifier-spotcheck.md:123` — spot-check obligation 5: "Carry r52
   repair: the refused E3 patch's order-check regression and masked K7 control stay open until
   fixed; production r52 counter intentionally unchanged this round."
2. `SCORECARD.md:2373` — "### Planned (round 55)": "Carry r52 repair until its order-check
   regression and masked K7 control are fixed."
3. `corpus/lessons/round-54.md:33` — Mistakes row `unsafe-rider-integration` (evidence
   `w1/R4R52Fix.md`): "Refused E3's proposed r52 patch: it makes order-check red and K7's
   unrelated failure masks the missing guard."
4. `corpus/QUALITY.md:1168-1169` — Q44 ruling: "The proposed r52 repair is refused:
   round-54/w1/R4R52Fix.md demonstrates an order-check regression and a masked K7 test."

Named check (the executable proxy the carry would pin if ever entered per Q23): the production
r52 counter's declared self-test, registry row `round52-c2` (`SKILL.md:636`),
`python3 plans/round52_c2_registry.py --lane . --selftest`. Observed at the tip (clone):

```
SELFTEST ok clean-fixture
SELFTEST ok missing-fixture
SELFTEST ok incomplete-fixture
SELFTEST cases=3 failures=0
EXIT=0
```

Current state: **still open, unchanged**. The selftest remains exactly the 3-fixture set
(clean/missing/incomplete) — the round-52 lesson's recorded gap stands (`corpus/lessons/round-52.md:58`:
"the C2 selftest has 3 fixtures … and none for the negated-flag or the false-selftest control,
so the parser class this row names is not exercised by `--selftest`"); the span-scoped negation
fix and the unfrozen mutation controls K5 (decoy table) / K7 (entry-missing) stay carried, not
claimed (`plans/round-52-claims.md:325-326`). The refused patch's two demonstrated defects
(`.ufo/waves/round-54/w1/R4R52Fix.md`): P1 patched counter falsely turns the green `order-check`
row red (old entry exit 0 → patched exit 1); P2 new K7 selftest passes even with ENTRY-MISSING
removed from verdict logic because unrelated MISSING failures mask the mutation. The production
counter is intentionally untouched this round (`plans/round-55-claims.md:150`), and the carry is
being reconstructed as evidence by seats R11R52Carry / RV3R52PatchAnatomy
(`.ufo/waves/round-55/w1-dispatch.json:412,662`) — neither had written outputs under
`.ufo/waves/round-55/w1/` at measurement time.

Full-counter context at tip (same command without `--selftest`): `ADVERTISED total=79`,
`REGISTERED total=77`, `MISSING 2` = `plans/round54_c1_anchor.py`, `plans/round54_c2_entrytruth.py`,
`PREDICATE R52-C2 fail`, exit 1 — byte-for-byte the R55-C1 before-surface
(`.ufo/waves/round-55/claims/c1-before.txt`).

## Bottom line

- Open rows in `corpus/defects.jsonl` at tip 80afa613: **0 of 5**; ledger green, exit 0.
- Still-open / closed-mismatch tally: **0 mismatches**; no closed row regressed.
- Named discrepancy: the r52-repair carry is an open obligation in spot-check/SCORECARD/lesson/
  QUALITY prose, **not** a defects-ledger row; its executable proxy
  (`round52_c2_registry.py --selftest`) is green at tip with the known 3-fixture coverage gap,
  i.e. the carry's underlying defects (order-check regression risk, masked K7 control) remain
  unexercised by any committed check — exactly as recorded when the patch was refused.

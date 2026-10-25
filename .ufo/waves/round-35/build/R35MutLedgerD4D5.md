# R35MutLedgerD4D5 — D4/D5 mutation findings

Axes: calibration (primary); mutation discrimination (supporting). Work ran in a sparse fixture clone at `/tmp/k35-K1f5/lane`, whose `git rev-parse --show-toplevel` output matched that exact path before fixture writes. Fixture was removed after the experiments. Lane files were not edited.

## D4

Checker under test: `plans/defect_ledger.py:r34_d4` (lines 69–84). Receipt from fixture invocation baseline: `(False, 'correction_lines=0')`.

- Add correction with four required terms → `(True, 'correction_lines=1')`.
- Drop each required term individually (`R34C2CounterDraft.md:8`, `cases=10 failed=0`, `R34MutC2Harness.md:12`, `SELFTEST green failed`) → each `(False, 'correction_lines=1')`.
- Add the same correction twice → `(False, 'correction_lines=2')`.
- Alter fixture `R34C2CounterDraft.md` line 8 from `cases=10 failed=0` to `cases=10 failed=1` → `(False, 'observation changed: cited draft/harness lines no longer hold')`.

The correction line used was `- **D4 correction (round 34 C2):** R34C2CounterDraft.md:8 shows cases=10 failed=0; R34MutC2Harness.md:12 shows SELFTEST green failed.`

## D5

Checker under test: `plans/defect_ledger.py:r34_d5` (lines 87–108). Its HTML-derived quote check uses `.ufo/waves/round-34/assimilation/captures/nec-s091-reopen.html`.

- With the exact quote retained in the capture, append `Erratum (round 35): own reopen capture nec-s091-reopen.html confirms quotation is present in capture.` to `corpus/lessons/round-34.md` and a `## Mistakes` section containing `| S091 | False refusal: quote present in nec-s091-reopen.html |` in `corpus/lessons/round-35.md` → `(True, 'erratum_lines=1 r35_mistake_row=True')`.
- Remove erratum only → `(False, 'erratum_lines=0 r35_mistake_row=True')`.
- Remove Mistakes row only → `(False, 'erratum_lines=1 r35_mistake_row=False')`.
- Replace the exact quote in the capture with `QUOTE_REMOVED` → `(False, 'observation changed: quote not in nec-s091-reopen.html')`.
- Put `not a table: S091` under a Mistakes heading instead of a pipe-delimited row → `(False, 'erratum_lines=1 r35_mistake_row=False')`.

## Exact retained evidence and total

Command run in fixture: `python3 -c '<inline importlib invocation of plans/defect_ledger.py:r34_d4 and r34_d5, applying and reverting each mutation>'`. Exact observations are the Python tuple receipts above; for D4 the baseline, green, token-drop (all four individually), duplicate, and observation mutation all produced the stated outcomes; for D5 green, each missing component, quote corruption, and outside-table row all produced the stated outcomes.

Caught: 12/12 mutation cases (5 D4: missing each of four terms + duplicate + observation alteration gives actually six; D5: missing erratum, missing Mistakes row, corrupted quote, outside-table row gives four). **Correction:** that enumeration totals 10; observed cases count is D4 1 green + 4 token-drop + duplicate + observation alteration = 7 and D5 green + 4 mutants = 5, total **12**, with green controls not counted as mutants: D4 mutants 6, D5 mutants 4, total 10. Both positive controls also passed. No installs or updates.

VERDICT: d4d5-mutants-10/10
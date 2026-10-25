# CritSourceTruth — round28 C2 critic (author-side)

Seat: KengakuR28.CritSourceTruth-2 (UFO-FSD critic, read-only). Scope: C2 literal references vs. true citation
support and the exact 13-row / 35-path frozen boundary. Advice only; not outside closure, not a round verdict.
Dated boundaries: baseline b9b24796277020d1b9b01923b45313d6a565e664 (round27 final), prereg
f0ba09be0f3066daba2134b943d973ad1588f34a, observation date 2026-10-21. I opened no external sources; every claim
below rests on lane files at those revisions.

## Strongest falsifiable objection

**The literal contract forces a false-provenance used-by repair for S050. It also falsifies F5 at baseline.
The second mismatch was computable from frozen inputs before implementation and is not "already disclosed".**

- Baseline knowledge `corpus/knowledge/extraction-policy-comparison.md:18` reads "inspect_ai `pattern()` (S058,
  correcting S050) takes a first regex hit". This is a supersession mention, not a use of S050 as support.
- The prereg (`plans/round-28-claims.md` C2 contract) says "historical/supersession mentions included" and
  "Cited rows must be `mined` and list every citing frozen path".
- Baseline `corpus/SOURCES.md:72`, row S050: status `mined`; used-by is only `corpus/lessons/round-27.md`;
  the immutable teaches cell still says "no hit is invalid_response_format", which is the blanket reason
  that S058 corrects.
- Round27's admitted decision, in `corpus/lessons/round-27.md:159`: "S050 stays lesson-only as a superseded
  reason, not silently passed as accurate". Repeated at `:203`.
- So the delivered checker must report S050 `missing_used_by=[corpus/knowledge/extraction-policy-comparison.md]`
  on the baseline. The only allowed-cell repair adds that knowledge path to S050's used-by. That:
  1. reverses an admitted round27 provenance boundary;
  2. links the knowledge file to a row whose immutable teaches cell is the superseded, inaccurate claim.
  That is exactly the gap between a literal reference and citation support that C2 says it does not measure.
- F5 ("S038 allowed-cell repair suffices for all13 frozen rows", p=.55, "other rows uninspected") is false
  at baseline. It was a frozen-input fact, not an uncertain forecast. It should be scored as a miss with
  this cause, not reused as calibration evidence.

## Decisive evidence (independent scratch recompute; not the production checker)

Scratch: `.ufo/waves/round-28/scratch/CritSourceTruth/baseline-recompute.json` and `SOURCES.base.md`. These
were derived with `git show b9b2479:<path>`, the population.json `reference_pattern`, and Registry rows
(all 11 columns).

| row | status | citing frozen files | missing used-by |
|---|---|---|---|
| S038 | queued | attribution-interval-calibration.md | same (disclosed) |
| S050 | mined | extraction-policy-comparison.md | **same (undisclosed in prereg)** |
| S049, S051–S059 | mined | extraction-policy-comparison.md | none |
| S060 | rejected | none | none (uncited, allowed) |

## Secondary calibration finding on the boundary

- **The 35 paths are the whole baseline knowledge tree.** The sets are equal: `git ls-tree b9b2479 corpus/knowledge`
  lists 35 files, with 0 extra and 0 missing.
- **Only 2 of the 35 files contain any of the 13 IDs.** `git grep` at the baseline found them only in
  attribution-interval-calibration.md (S038) and extraction-policy-comparison.md (S049–S059 except S050's
  support use).
- **The effective population is 13 (row, file) citation pairs.** These cover 12 cited rows plus 1 uncited
  rejected row. The other 33 files are zero-reference controls.
- **Reports should state that denominator.** "35 knowledge paths checked" should not read as 35 files of
  citation coverage.
- **IDs outside knowledge are out of the frozen population by design.** Lessons, README and evidence files
  that cite the same IDs are excluded. That is not a defect, but it is a limitation to state.

## Impacted axes

- **Calibration8:** F5 is a mis-specified forecast; the literal-coverage result conflicts with an admitted
  round27 provenance decision.
- **Novelty/coverage:** no impact; C1 is separable and untouched by this objection.

## Smallest safe correction

These steps go to L1, recorded as dated author-side amendments before final counting. No post-hoc
contract exemption.

1. Keep the literal contract and the checker unchanged.
2. Do not add `extraction-policy-comparison.md` to S050's used-by as a "repair". Report the final tree as:
   S038 repaired (only after the source is reopened), S050 a persisting, disclosed literal-mention mismatch.
   Expected exit1 with one finding.
3. Alternatively, if L1 chooses the used-by edit, it must explicitly record three things in the round28
   lesson:
   - that the edit reverses `round-27.md:159/203`;
   - that this used-by entry records a corrective mention, not support;
   - that S050's teaches cell remains superseded by S058.
   It also must not count toward M65's "allowed-cell repair as the only delta".
4. Score F5 as missed, with cause "S050 computable at baseline". Report C2 denominators as 2 citing files,
   13 row-file pairs, and 33 zero-reference controls.

## Limitations

- I did not run the delivered `registry_check.py`; it was absent from the worktrees at review time, and checks
  are out of my scope. The table is my independent recompute and should be compared at integration.
- No semantic audit of the other 12 citations.
- No S038 reopen.
- No installs.

## Final scoped verdict

**PARTIAL.** C2's frozen boundary holds exactly at 13 rows and 35 paths. Under the declared literal contract
it is falsifiable and recomputable. But "S038 drift is the expected mismatch" and F5 are wrong at baseline,
and the natural S050 repair would create false provenance unless it is handled as in the correction above.

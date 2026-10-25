# Round 25 — attribution score-phase reconstruction

Scope: `plans/attrib_probe.py` and the frozen P1 receipts only. LSP was unavailable (`read xd://lsp` returned “No such tool”); source claims below are grounded in direct source reads, not semantic LSP results. No runtime or endpoint was invoked.

## Reconstructed contract

- **Prediction:** trial commands extract response features and call `score_obs` before GT is read (`plans/attrib_probe.py:566-575`). Weighted tell-overlap, categorical and band matches accumulate per-leg scores; highest score wins, ties choose the first leg in frozen roster order. A non-200 with no matching error tell is assigned roster-last (`:439-513`). The feature extraction includes headers, echo, usage/tokens, timing/stream shape, ID, status/error wording, and (v2+) body schema/ID fields (`:278-434`).
- **GT:** after trials, `cmd_score` parses journal REQUEST/leg events and joins requests by body length, stream flag, and timestamp window; it first uses `[t0-1s,t0+3s]`, then a ±5s fallback (`:883-938`). Matched chains with an OK leg label GT as the first OK leg / `gt_class=served`; all-fail chains label the last attempted leg / `relay-last-fail`. A matched request with no leg lines is excluded (`:939-963`).
- **Correct:** equality of prediction and GT; reported table `YES/NO` is stored prediction == GT (`:994-1003`). The summary accuracy recomputes a prediction from stored features and compares it to GT (`:965-973`). The base denominator is all rows in `scored`, not only correct rows.

## Exclusion / selection findings

- Current source excludes only a trial with no request candidate (`UNMATCHED`) or a matched request with no leg lines (`NO-LEG-LINES`); it does **not** test correctness before adding a row to `scored` (`:939-971`). There is no current `AMBIGUOUS` exclusion branch: when multiple candidates remain, the join takes the earliest unused request (`:909-938`).
- The historical r21 implementation receipt proves this was once hazardous: two earlier score blocks have 20 `UNMATCHED` each, and a later debug block excludes T06/T10 as `AMBIGUOUS(2)` (`attrib-r21-impl-ds-trials.log:130-159,176-220,222-266`). Its adjudication declares only the last block authoritative and says the greedy one-to-one fix recovered 20/20 with 0 excluded (`:268-335`). The two ambiguous rows were present and correct in that final block (`:280,284`; final summary `:297-312`). These debug exclusions are not P1 rows.
- **`err` has two meanings.** A trial class `err` is the deliberately generated error-path request, not a client capture exception: r21 impl-GLM scores both such rows (T21/T22, both YES; `attrib-r21-impl-glm-trials.log:169-173`). Separately, capture exceptions populate `obs.error` (`plans/attrib_probe.py:267-275`); producers print “excluded from accuracy denominator” but still serialize them (`:578-596`). `cmd_score` loads every record and has no `error` check before matching/scoring (`:871-879,908-963`). **[INFERENCE]** A capture-exception record could therefore still be scored if journal REQUEST and leg lines match it; otherwise it falls into the ordinary unmatched/no-leg exclusion. No `ERROR:` capture-exception lines occur in the nine P1 receipts (literal search result: no matches).
- Forced/stream per-target verdicts use the on-target subset, but this is separate from base accuracy: all `scored` rows enter the base denominator; off-target rows are also reported in the coverage distribution (`:1009-1036`). Do not substitute these target-only subsets for C1 accuracy.

## Frozen P1 receipt counts

P1 selects the LAST close-scoring block; no block means zero scored and a trial-only receipt. Identical tables count once (`plans/round-25-claims.md:28-32`). Counts below are authoritative P1 rows; “—” means no close-scoring block, not an observed zero-exclusion score.

- `attrib-r21-ds-trials.log`: trial-only, P1 n=0; scorer explicitly not run (`:174-176`). Exclusions: —.
- `attrib-r21-glm-trials.log`: trial-only, P1 n=0; the 22-trial run has no GT block (`:141-152`). Exclusions: —.
- `attrib-r21-impl-ds-trials.log`: last block 20/20 correct; 0 `UNMATCHED` / `AMBIGUOUS` / `NO-LEG-LINES` (`:268-312`). Superseded debug blocks: 40 `UNMATCHED` across two blocks and 2 `AMBIGUOUS` (`:130-159,176-220,222-266`); excluded from P1 by the receipt’s own last-block rule (`:316-335`).
- `attrib-r21-impl-glm-trials.log`: 22/22 correct; 0 excluded (`:142-188`); includes both `err`-class trials, not filtered.
- `attrib-r22-legs.log`: last block 20/20 correct; 0 excluded (`:312-362`).
- `attrib-r22-legs-hyper.log`: trial-only, P1 n=0; scorer explicitly not run (`:219-227`). Exclusions: —.
- `attrib-r22-opencode-trials.log`: 20/20 correct; 0 excluded (`:204-254`), but its full trial table is identical to the selected `attrib-r22-legs.log` table (`:212-231` vs `:320-339`); count it once, not twice.
- `attrib-r23-stream.log`: last block 30/30 correct; 0 excluded (`:258-320`). Its overall `score_summary` verdict is FAIL because the separate opencode-go on-target clause has n=0, not because accuracy failed (`:300-320`).
- `attrib-r23-stream-trials.log`: trial-only, P1 n=0; 30 trials completed with no journal GT read (`:418,421-437`). Exclusions: —.

**P1 deduplicated total: 92 scored rows, 92 correct; 0 exclusions in the authoritative scored sample.** The 20-row r22 duplicate is removed; the four trial-only receipts contribute no scored rows. The only observed hard-trial exclusion is the superseded r21 ambiguous debug block; the final authoritative re-match restores those trials. No final P1 evidence shows an incorrect trial removed for being incorrect.

VERDICT: Final P1 accuracy rows show no correctness-based selection, but matcher-debug exclusions and the unimplemented `obs.error` denominator promise are real audit hazards; C1 must use the final close block, deduplicate the r22 pair, and retain all scored rows regardless of result.

Installs: none.
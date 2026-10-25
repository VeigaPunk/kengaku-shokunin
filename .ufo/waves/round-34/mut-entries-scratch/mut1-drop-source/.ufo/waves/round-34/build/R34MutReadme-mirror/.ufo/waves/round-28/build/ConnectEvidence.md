# ConnectEvidence — round 28 connector report (author-side advice)

- seat: `KengakuR28.ConnectEvidence-2` (role: connector). Read-only; wrote only this report. No scratch files.
- writer of every inspected artifact: not this seat. This report is advice; under QUALITY Q14 a connector's overlap advice is not a Q10 source/number re-read, and under R6 it is not non-author evidence.
- Inputs at lane master `f0ba09b`; I checked that `git diff b9b2479 HEAD -- corpus/` is empty, so the corpus is at the baseline. sha256 values:
  `plans/round-28-claims.md` 8b2e237a…85a5f, `corpus/QUALITY.md` d02f798c…1657, `corpus/SOURCES.md` b1a74eb5…c62e,
  `plans/fixtures/r28/webarena/config_files/test.raw.json` 7b50386f…37652, `…/evaluation_harness/evaluators.py` e23edb39…0c22.
- No sources were opened, no network access, and no upstream code was imported or executed. JSON was parsed with stdlib `json`; the evaluator was read as text. No tools were installed or updated.

## Axes

- C1 novelty (legacy), mapped to canonical coverage/constructs, currently 7.
- C2 calibration, currently 8.

Both scores are held. Nothing below argues for repricing either one.

## Evidence

### E1 — C2 baseline has a second cited-row mismatch besides S038

I recomputed literal mentions over the 35 frozen paths in `plans/fixtures/r28/registry/population.json`, using its `reference_pattern`. I compared those against the used-by cells of `corpus/SOURCES.md` under `## Registry` (11 columns).

| row | status | frozen citing files | used-by contains the citing file? |
|---|---|---|---|
| S038 (SOURCES.md:60) | queued | `corpus/knowledge/attribution-interval-calibration.md` (line 144) | no; used-by is `—` |
| S050 (SOURCES.md:72) | mined | `corpus/knowledge/extraction-policy-comparison.md` (line 18: "inspect_ai `pattern()` (S058, correcting S050)") | **no**; used-by is only `corpus/lessons/round-27.md` |
| S049, S051–S059 | mined | `extraction-policy-comparison.md` | yes |
| S060 (SOURCES.md:82) | rejected | none | not applicable (an uncited rejected row is not an error) |

The prereg makes the S050 mention count: "Every standalone `S[0-9]{3,}` mention in those paths counts literally (historical/supersession mentions included)" (claims line 25). It also requires that cited rows "list every citing frozen path" (line 25).

So at baseline, the literal contract has at least two failing rows: S038 (queued and missing its citing file) and S050 (mined but missing its citing file). This is my recomputation, not the delivered `registry_check.py`, which has not landed in any of the three writer clones I checked.

- F4 (≥1 mismatch, p=.95) is consistent with this.
- F5 ("S038 allowed-cell repair suffices for all13 frozen rows, p=.55", line 41) is contradicted by E1, assuming the delivered checker implements the declared contract. Record this as the forecast's outcome. Do not edit the forecast.

### E2 — C1 has a matching structural shape: a declared field that no routed scorer reads

I parsed all 812 tasks in `test.raw.json`. Evaluator-type sets:

| evaluator-type set | tasks |
|---|---|
| string_match | 325 |
| program_html | 282 |
| program_html + url_match | 129 |
| url_match | 66 |
| string_match + url_match | 10 |

That is 5 sets (F2). Other counts: `program_html` has 651 targets, 105 of them with an empty locator. `string_match` reference-answer keys are must_include 176, fuzzy_match 118, exact_match 45.

`evaluator_router` (evaluators.py:361–372) only builds evaluators for the declared `eval_types`. `URLEvaluator` is the only reader of `reference_url` (evaluators.py:213). Exactly **1/812** tasks has a nonempty `reference_url` but no `url_match`:

- Task 247 (`shopping_admin`, `string_match`, fuzzy_match `"N/A"`). Its `reference_url` is the prose "Valorie doesn't have a email in the system" (test.raw.json:7832).
- The N/A branch passes only `string_note` ("There is no negative review for Zoe products") to `ua_match` (evaluators.py:159–162).
- So this task carries two different unachievability rationales, and the scorer can only see one of them.

Control: all 36 nonempty `string_note` fields belong to the 36 N/A tasks, so none of them is unread. Task 247 is not in the frozen 16-task sample; the only N/A task in the sample is 791.

Under the prereg this is an observation and a limitation, not a benchmark FAIL: "weak proxies are described as limitations, not invented benchmark FAILs" (line 17).

A related but separate shape: 9 `url_match` tasks (174–182) have no `url_note` and rely on the implicit default `"GOLD in PRED"` (evaluators.py:215). That is an implicit default, not an unread field, and I don't count it as the same pattern.

## The shared failure mode, without merging the claims

In both instruments, a relation is written down at one end and the other end is maintained separately by hand. A check that reads only the authored end passes even when the other end disagrees.

- C2: the knowledge file says "S050". The registry's reverse index (used-by) is a hand-written cell, not derived from the mentions, so it fell behind.
- C1: the task config declares a target field (`reference_url`). Whether anything consumes it depends on a separate hand-written list (`eval_types`), so the field can exist with no consumer.

This is a structural analogy only. The two populations, causes and counting commands stay separate (claims line 11; R13). Nothing here says the WebArena annotators and the lane registry fail for the same reason, and the analogy does not define a second research method.

## Proposed move (one, bounded)

Each instrument derives its incidence set from the authored end and diffs it against the maintained end. Each does this inside its own population and reports results under its own denominator.

- C1, `benchmark_spec_audit.py`: add an inventory row "declared eval-field present but not consumed by any declared eval_type". It reads only the JSON fields and the router's static `case` arms, parsed from the AST, never executed. Expected count on the pinned snapshot: 1 (task 247), with its `string_note`/`reference_url` disagreement listed as a limitation. The prereg already asks for "schema compatibility for each declared eval type" (line 17), so this is an additional inventory row in that audit, not a new claim.
- C2, `registry_check.py`: no new logic. Make sure the baseline run reports S050's `missing_used_by=[corpus/knowledge/extraction-policy-comparison.md]` as well as S038.
  - Any S050 repair falls under "Repair only after reopening its original source" (line 9). That means reopening the pinned inspect_ai `_pattern.py` URL in SOURCES.md:72, then appending only to the used-by cell. Immutable cells stay unchanged.
  - The M65 delta must then name two rows, not one, or explicitly disposition S050 as left open.

### Axes affected

- C1 coverage/constructs: one more construct is covered (field-consumption completeness) with no score change.
- C2 calibration: a forecast that would otherwise miss is resolved honestly, and a silent S038-only repair is blocked. The score is held.

## Strongest no-axis-harm risk

The main risk is that the analogy gets used as shared evidence. Two ways that could happen:

1. Someone builds one "edge-completeness" check, or a joint statistic, over both populations.
2. The C1 task-247 finding gets cited to explain the C2 S050 drift, or the reverse.

Either would break R13 and the two-way revert test (claims line 11). It would also turn a structural parallel into a causal claim.

There is a second risk on calibration. Calling S050 a "new discovery" that earns credit, or using it to retro-justify F5, would overstate it. It is a contract consequence that the prereg's own forecast flagged as uncertain ("other rows uninspected").

A third risk on C1: reporting task 247 as an invalid task would break line 17. It is a data inconsistency inside one N/A task, and a browser-level check never happened.

## Verification for the integrator (L1)

1. On the baseline export, `python3 plans/registry_check.py --json` should list S050 with `missing_used_by` containing `corpus/knowledge/extraction-policy-comparison.md`. If it doesn't, the checker diverges from the claims line 25 contract.
2. Two-way revert: C2 counts must not move when the C1 paths are reverted, and the C1 field-consumption count (1) must not move when the C2 paths are reverted.
3. The oracle writer should re-derive the count of nonempty `reference_url` without `url_match` independently and get 1 (task 247).
4. The S050 repair delta should be the used-by cell only, after a recorded reopen.

## Limitations

- These are counts from my own stdlib parses, not from the delivered tools. None of the three writer clones contained `registry_check.py` or `benchmark_spec_audit.py` when I checked; their porcelain status was empty.
- The literal matching is regex-only. It cannot tell whether a mention is a correction or a support claim.
- E2 shows the scorer cannot read the field. It does not establish which rationale is correct for task 247.
- None of this is source-truth validation, a semantic citation check, or a browser-level check.

## Verdict

**PASS** for this connector proposal: the evidence, the bounded move and the risk are delivered. This is not a round PASS. It does not affect C1 or C2 admission, and it is not non-author closure. The F5 forecast is likely to resolve false, contingent on the delivered checker.

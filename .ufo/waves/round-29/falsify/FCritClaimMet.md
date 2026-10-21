writer: KengakuR29-2.FCritClaimMet-2

# FCritClaimMet — is C1, as frozen in the prereg, actually met by the integrated state?

Seat: KengakuR29-2.FCritClaimMet-2 (UFO-FSD critic, read-only leaf). Lane master 56fd949a6478342531e61f4feecb4a685d831640.
Prereg: plans/round-29-claims.md (108 lines). Scratch: .ufo/waves/round-29/scratch/falsify/FCritClaimMet/.
Production source: **read**, but only AFTER `rederive.py` (my independent re-derivation) had been written and run. I am a
critic seat, not an oracle seat; my re-derivation saw the `--json` output's field names, so it counts as supporting evidence
only and does not stand in for the prereg's independent oracle.
Tools: none installed or upgraded. I used only the stdlib (python3), no pacman, no REA devices.

## Attack

C1 has four legs: 2436 projections, occurrence/field provenance, the output-index versus task_id mapping, and
"independent oracle agreement". The prereg also requires 9 Required-output bullets (lines 62–71), a list of selftest
cases (lines 73–77) and an oracle plus hand-case file (lines 79–82). I checked each item against the observed outputs.
The strongest counterexample is that the oracle-agreement leg and the errors hand-case file are absent from the
integrated state. The numeric surface holds up: everything I re-derived matched.

## Commands run (lane root, all read-only; outputs in scratch)

| command | exit | observation |
|---|---|---|
| `python3 plans/config_projection.py --summary` | 0 | `TOTAL findings=0 exit=0`; `diff` against corpus/evidence/round29-calibration/build-summary.txt differs only by that receipt's appended line 48 `exit=0` |
| `python3 plans/config_projection.py --json > out.json` | 0 | sha256 c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630 = build-json-sha256.txt = candidate-freeze-v1.json `json_output_sha256` |
| `python3 plans/config_projection.py --selftest` | 0 | `SELFTEST clean cases=20 …` (same 20 names as build-selftest.txt) |
| `sha256sum plans/config_projection.py` | 0 | 5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3 = freeze `instrument` pin = mutation-witness control |
| `python3 plans/config_projection.py` (no flag) | 0 | prints the summary |
| `… --bogus` / `… --summary --json` | 2 / 2 | argparse usage error |
| `python3 scratch/…/rederive.py out.json` | 0 | `MISMATCHES: 0` (see below) |
| `python3 scratch/…/mutants.py` (on /tmp copies) | 0 | reproduces all 4 mutation-witness.txt lines (see below) |
| `sha256sum` of the 4 pinned inputs | 0 | manifest f6390b92…bf87, profiles 90fdc34d…e018, generator 45ddba7b…21cd, raw 7b50386f…7652, all equal to the pins |

## Independent re-derivation (rederive.py, written before I read the production source)

I re-derived these from the prereg text, the generator lines 11–16/20–23 and the pinned bytes: population counts,
original occurrences by token, tasks_with_token, index equality, the set of 1435 (offset, token) occurrence pairs plus a
JSON-pointer resolution check, and, for each of the 3 profiles, the step counts, projected-text sha256, parsed count,
string-leaf count, remaining tokens, changed leaves by category/template/token, tasks by token, changed_task_count,
multi-occurrence leaves and `//` junctions. Every one equals the instrument's `--json` (0 mismatches). For all 2436
per-task records I also compared task_id, output_index, output_filename, index_equals_task_id, would_be_file_sha256,
projected_task and the full changed_leaves list, field by field: 0 value mismatches.
Other observed facts: tokens inside JSON object keys = 0, provenance pointer mismatches = 0, and the raw file is ASCII
(880776 bytes = 880776 codepoints).
For the url_field/non_url_field split I used a key-name rule (`start_url`, `url`, `reference_url`). It gives the same 1355/61.

## Required output, prereg lines 62–71

| # | prereg item | status | evidence |
|---|---|---|---|
| R1 (l.63) | 812 tasks, distinct IDs, 3 profiles, 2436, no hidden exclusions | MET | `POPULATION {"distinct_task_ids": 812, "input_task_count": 812, "profile_count": 3, "task_profile_projections": 2436, …}`; `task_population_invalid` guard requires ids == range(812) (config_projection.py:274) |
| R2 (l.64) | per-profile raw replacement counts by token | MET | `steps[].applied_replacements` 385/336/281/300/0/133 per profile; re-derived |
| R3 (l.64) | source text / projection digests | MET | `raw_text_sha256` 7b50386f… (top level, not repeated per profile); `projected_text_sha256` per profile 2aec098e… / 54cf9833… / 49bbee2e…; re-derived |
| R4 (l.64) | parsed task count | MET | `parsed_task_count=812` ×3 |
| R5 (l.65) | changed string leaves by JSON path and category | MET, with a label caveat (D3) | per-template counts plus per-leaf `json_pointer`; category is path-only (config_projection.py:38–39) |
| R6 (l.65) | remaining known placeholders | MET | `remaining_known_tokens_text` / `_decoded` all 0 ×3; other markers `__last_url__` 65, `__page__` 12 reported at population level |
| R7 (l.66–67) | per task/profile: task_id, ordinal/filename, exact projected object, changed leaf paths with original/projected values | MET as a JSON value; key order is lost (D4) | 2436 records with keys changed_leaves, index_equals_task_id, output_filename, output_index, projected_task, task_id, would_be_file_sha256 |
| R8 (l.68) | named Unicode-codepoint offsets | MET | field `original_input_codepoint_offset`; LIMIT line names codepoints, not bytes; selftest `codepoint_offsets_and_key_token` asserts offset 16 against 18 UTF-8 bytes |
| R9 (l.69–70) | ordered replacement behavior, index==task_id on frozen input, shuffled-ID hand witness | PARTIAL (D2) | `INDEX {"index_equals_task_id": 812, "violations": 0}`, `steps` in source order. The witness runs only as a selftest assertion (`hand_index_r29_index_shuffled_ids_1_0`); its filename/task_id values appear in no output or receipt |
| R10 (l.71) | separate occurrence, leaf and task counts | MET | 1435 occurrences, 1416 leaves (13 with >1 occurrence) and 812 tasks, each under its own key; selftest `units_not_pooled` |

## Selftest, prereg lines 73–77 (selftest() at config_projection.py:385–521)

| requirement | status | case / line |
|---|---|---|
| CLI-exposed | MET | `--selftest` flag (l.530) |
| isolated | MET | CLI cases run in `tempfile.TemporaryDirectory` copies (l.474); hand fixtures are only read |
| six token replacements | MET | `six_tokens_and_non_url_field` asserts `[2]*6` (l.396) |
| non-URL fields | MET | same case: `intent` changed, category 6/6 (l.397–398) |
| overlapping field contexts | MET by interpretation; no case carries this name | each token sits in both `start_url` and `intent` of one task (l.393). No case puts two *distinct* tokens in one leaf (the frozen data has 0 such leaves: sum of by-token = 1416 = leaf count) |
| exact order and later-token cascade | MET | `hand_cascade_order_R29_ORDER_CASCADE_01` checks per-step hits and that the mapping-order mutant differs (l.436–442); `source_order_swap` (l.462) |
| missing/non-string map entry | MET at unit level | `profile_map_errors` calls `check_values` directly (l.427–434). Not reachable from the CLI because profiles.json is hash-pinned and a tamper exits as `snapshot_tampered` first |
| UTF-8/escaped source text | MET for raw text | `codepoint_offsets_and_key_token` (é), `escaped_token_not_replaced` (`\u005f\u005f`) (l.407–418). Runs on str input; no non-ASCII *bytes* go through the `.decode("utf-8")` path |
| quotes/backslashes → decode failure, not repair | MET (findings) | `quote_backslash_decode_failure_and_escape_semantics` (l.420–425) |
| index-versus-ID | MET | `hand_index_…` (l.453–458) |
| missing/tampered input, coherent rebinding | MET (findings and exits) | `cli_snapshot_tampered`, `cli_input_missing`, `cli_coherent_rebinding`, `cli_manifest_tampered`, all asserting exit 2 (l.481–519) |
| post-read replacement witness | MET | 3 `post_read_replacement_*` cases patch `Path.read_bytes` (l.502–517) |
| inputs/expected values persisted | MET | inline literals plus the 3 adopted hand fixtures |
| "test findings and exits checked" (l.76–77) | PARTIAL (D5) | exits are asserted only in the 4 `cli_*` cases. The in-process cases (`projection_json_invalid`, `known_token_remaining`, `token_outside_string_value`, `profile_*`) assert finding ids but never the exit code |
| no exhaustive-mutation claim | MET | the draft and receipts make no such claim |

## C1-level legs and the oracle/hand-case contract (prereg lines 10–14, 79–82, 100)

| leg | status | evidence |
|---|---|---|
| 2436 projections | MET | R1, re-derived |
| occurrence/field provenance | MET | 1435 records; offset set and pointer resolution re-derived with 0 mismatches |
| output-index vs task_id | MET (frozen) / PARTIAL (witness output, D2) | R9 |
| **independent oracle agreement** | **UNMET in integrated state (D1)** | no oracle or comparison receipt under corpus/evidence/round29-calibration/ (6 files: build-json-sha256, build-selftest, build-summary, instrument-before, mutation-witness, sources-before); corpus/lessons/round-29.md (untracked) M88: "including all three executors (production tool, oracle, hand-case file never written)" (11 words). The falsify spec lists FOracleText/FOracleLeaf/FOracleProvenance/FOracleIndex, but none of their reports was in .ufo/waves/round-29/falsify/ at 2026-10-21T16:51:53Z. The build-wave "2436/2436 structural equality" (build/R29ContractSerialized.md:222) predates the instrument and compares two hand computations (same file, l.145–148) |
| hand-case file with "transforms/errors/order and output index values" (l.82) | PARTIAL (D6) | the adopted fixtures cover transforms (url-only), order (cascade) and index (shuffled IDs); no hand file holds **error** cases. Quote/backslash expectations exist only inline in selftest (l.420–425) |
| hand cases "must disclose where that alternative is not equivalent" (l.43–44) | PARTIAL (D6) | cascade-order.case.json says nothing about decoded-leaf (non-)equivalence; no quote/backslash hand file exists |
| failing wrong URL-only or wrong-order witness before the control counts (l.100) | MET; receipt not reproducible as stored (D7) | mutation-witness.txt; reproduced by me (below) |

### Mutation reproduction (mutants.py, /tmp copies; mutants written by me, not the receipt's unpersisted ones)
```
control: selftest exit 0 SELFTEST clean cases=20 … | summary exit 0 ['TOTAL findings=0 exit=0'] findings=[]
wrong_order_reversed: selftest exit 1 AssertionError | summary exit 0 ['TOTAL findings=0 exit=0'] findings=[]
url_only_substitution: selftest exit 1 AssertionError | summary exit 1 ['TOTAL findings=6 exit=1'] findings=['known_token_remaining', 'leaf_change_unexplained']
index_by_task_id: selftest exit 1 AssertionError | summary exit 0 ['TOTAL findings=0 exit=0'] findings=[]
```
All four lines match the receipt's exits and TOTAL lines. My first index mutant crashed with a TypeError rather than
being killed; after the fix it is killed by an AssertionError.

## Mismatches and defects

**D1. Oracle-agreement leg absent (C1 leg unmet).** Location: corpus/evidence/round29-calibration/ (no oracle file); prereg
l.81, "Main compares every required metric and per-task object, not only totals." (11 words). Value: 0 oracle receipts and
0 Main comparison receipts. Classification: **fixable gap, pending the wave**, not an instrument defect. My re-derivation
gives 0 mismatches, so I found no counterexample to agreement. Smallest safe correction: land the FOracle* reports, then
one Main comparison receipt over every R1–R10 metric and all 2436 per-task objects at instrument sha 5673405e… and
JSON sha c8da0c5a…, before any SCORECARD row.

**D2. The shuffled-ID (and cascade) witness values are never emitted.** Location: prereg l.69–70 ("with a shuffled-ID hand
witness showing the upstream enumerate-index behavior;", 10 words); config_projection.py:520 prints case names only.
Value: build-selftest.txt contains `hand_index_r29_index_shuffled_ids_1_0` but no `config_files/0.json → task_id 1` record.
Classification: **fixable defect (observability)**. Correction: have `--selftest` print the witness records it already
asserts (filename to task_id, the per-step cascade texts) and re-capture build-selftest.txt.

**D3. The `non_url_field` label versus value shape.** Location: config_projection.py:38 ("Category is strictly the JSON path,
never the value shape or the `sites` metadata.", 14 words); draft webarena-config-projection.md:56 ("Global text
replacement reaches non-URL fields.", 6 words). Value: 60 of the 61 `non_url_field` leaves are single token-prefixed URL
strings (regex `^__TOKEN__/\S*$`). The 61st, /66/eval/reference_answer_raw_annotation, is two comma-joined token URLs.
Under the prereg's value wording (l.46 "URL-valued fields"; l.106 "F3 global replacement changes at least one
non-URL-valued field, p=.7;", 10 words), the count is 0. The untracked lesson M89 discloses this, but the frozen candidate
does not. Also, l.56–57 reads "61 changed leaves are `must_include` answer strings and one raw annotation", which can be
read as 62; the actual split is 60 + 1 = 61. Classification: **fixable defect in candidate wording**. The instrument's
path rule is a declared tradeoff and stays. Correction: one clause at draft l.56: "path category; all 61 values are
token-prefixed URL strings (60 `must_include`, 1 annotation)".

**D4. `--json` loses key order in `projected_task`.** Location: config_projection.py:541 `sort_keys=True`; prereg l.66
"exact projected task object". Value: 812/812 records per profile have sorted top-level keys, while the raw order is
`['sites', 'task_id', 'require_login', …]`. `would_be_file_sha256` is computed before sorting and matches my
insertion-order `json.dumps(indent=2)` for all 2436, so byte identity is preserved by digest but cannot be reconstructed
from the output. Classification: **tradeoff** (oracle comparison is by parsed value, see build/R29SimplifyOutputSize.md:96).
Correction: add a LIMIT line saying keys are sorted in `--json` and that the would-be file bytes are bound only by
`would_be_file_sha256`.

**D5. Selftest exits not checked for in-process findings.** Location: prereg l.76–77 ("test findings and exits checked.",
5 words); config_projection.py:420–434 assert ids only. Value: 0 exit assertions for `projection_json_invalid` (an exit-1
class), `known_token_remaining`, `token_outside_string_value` and `profile_*` (exit-2 class). Classification: **fixable
defect (small)**. Correction: in those cases also assert `int(bool(findings)) == 1`, and assert that the `Unevaluable`
path maps to 2 (as `main()` does at l.535–536).

**D6. The hand-case file lacks errors and domain disclosure.** Location: prereg l.82 ("An independent hand-case file contains
exact expected transforms/errors/order and output index values.", 12 words) and l.43–44; plans/fixtures/r29/hand/ (4
files). Value: 0 hand files with expected errors; 0 decoded-leaf non-equivalence statements. Classification: **fixable
gap** (crash loss per M88). Correction: a second-writer `errors.case.json` with the quote/backslash/control-char inputs and
their expected `projection_json_invalid` results plus the decoded-leaf divergence (build/R29ContractSerialized.md §6
already measured those values), consumed by selftest.

**D7. The mutation receipt is not self-reproducing.** Location: corpus/evidence/round29-calibration/mutation-witness.txt (6
lines). It has no mutant patches, commands or writer, and no other non-scratch file references its producer. Value:
reproduced independently above, so the claim stands. Classification: **fixable defect (provenance)**. Correction: persist
the 3 mutant diffs and the command beside the receipt.

**D8 (minor). Internal inconsistency in the draft.** Location: draft l.36 "identical per profile except digests". The
junction count differs (697 / 0 / 0, draft l.48), as do values and stimulus text. Classification: **fixable wording**.
Correction: "except digests and the `//` junction count".

Not defects, recorded for completeness: running with no flag prints the summary with exit 0. Prereg l.55 "CLI usage2" is
honored for unknown and conflicting flags (exit 2). WIKIPEDIA has 0 occurrences and order is invisible on the frozen data;
both are disclosed at draft l.59–64. SCORECARD is untouched (`git diff --stat ed26bdf 56fd949` lists no SCORECARD).

## Impacted axes

C1 completeness (oracle leg: D1, D6), the provenance/observability of witnesses (D2, D7), the candidate's claim precision
and F3 scorability (D3, D8), and exit-contract coverage (D5). Correctness of the 2436 projections themselves: no defect
found (0 mismatches across all metrics and all per-task objects).

[INFERENCE] If the FOracle* items land with full per-object agreement, and D2/D3/D5/D6 receive their one-line fixes,
nothing I found would block C1. Today the frozen claim's "independent oracle agreement" is not yet observed.

VERDICT: PARTIAL

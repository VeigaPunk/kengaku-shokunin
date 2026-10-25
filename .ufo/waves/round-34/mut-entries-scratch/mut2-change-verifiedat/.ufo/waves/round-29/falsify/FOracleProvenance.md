writer: KengakuR29-2.FOracleProvenance-2

# FOracleProvenance — occurrence-provenance oracle attack on the integrated r29 projection

## Axes (godspeed)
independence (no production source read) · coverage (6 tokens × 1435 occurrences × 6 fields + 3 population fields + offset semantics) · mismatch precision (exact token/offset/field values) · reproducibility (scanner + captured outputs + digests in scratch).

## Independence statement (observed)
- I did NOT read, grep, or import `plans/config_projection.py` source at any point. Every file I read is listed below; the instrument was exercised only as `python3 plans/config_projection.py --json|--summary` (allowed read-only mode), and only its captured stdout was consumed.
- Token contract derived from pinned generator bytes, not from the instrument: `plans/fixtures/r29/generate_test_data.py` lines 11–16 are the six `raw.replace("TOKEN", VAR)` calls; extracted ordered tokens `['__GITLAB__', '__REDDIT__', '__SHOPPING__', '__SHOPPING_ADMIN__', '__WIKIPEDIA__', '__MAP__']` (scan.py output `tokens_in_order=...`).

## Pinned input facts (observed)
- `plans/fixtures/r28/webarena/config_files/test.raw.json`: bytes=880776, codepoints=880776 (strict UTF-8 decode), nonascii_codepoints=0, backslashes=1335, sha256=7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652 — equals the manifest's declared pin; parses under stdlib `json.loads`.
- Top level: list of 812 task objects.

## Attack design (scratch files, all sha256 observed)
Scratch dir `.ufo/waves/round-29/scratch/falsify/FOracleProvenance/`:
- `scan.py` sha256 7952fde60d2011b2a889d0b583ae919701746351b36780249bca4827ca70e98f — my own oracle: hand-written recursive-descent JSON scanner (no `json` module for structure; stdlib used only to decode key strings and to sanity-check well-formedness), per-string token find-loops (overlap-stepping), JSON-pointer construction with RFC 6901 `~0`/`~1` escaping, root-array index as task_index, key-vs-value role from grammar position, task-relative path templates in two renderings (`templates_of`, scan.py:84–97; `emit`, scan.py:99–109), independent whole-text flat census, cp-vs-byte probe on a synthetic UTF-8 fixture, multiset + field-level comparison, population verification.
- `instrumentjson` sha256 c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630 (3,881,050 bytes stdout of `--json`, rc=0, stderr 0 bytes); `instrumenttxt` sha256 5ce5cb0f91ad279d446a475de757b9aa4a5b67a4b02df8d9aeac0d01be74636f (6,914 bytes stdout of `--summary`, rc=0, stderr 0 bytes); `oracle_findings.txt` sha256 130d53045e898396b21e868832042655975cee626640af55c2d300746e366a83 (final run transcript).

## Comparison results (observed counts, units separated)
Occurrence unit — my flat census == my structural census == instrument, per token:
`__GITLAB__` 385, `__REDDIT__` 336, `__SHOPPING__` 281, `__SHOPPING_ADMIN__` 300, `__WIKIPEDIA__` 0, `__MAP__` 133; total occurrences 1435 both sides (`instrument_record_count=1435 my_record_count=1435`).
Record-level: `multiset_exact_match=True`, `records_only_in_instrument=0 records_only_in_mine=0`, `field_or_membership_mismatches=0` over all six fields (token, original_input_codepoint_offset, json_pointer, string_role, task_index, path_template). Instrument task_index range 0..811 (None count 0); offset range 172..880440 (None count 0); string_role: value 1435, key 0, both sides. Pointer convention (absolute, root array index included, e.g. `/44/start_url`) agrees on all 1435 records.
Task unit — `tasks_with_token`: mine {385→204, 336→128, 281→192, 300→182, 0→0, 133→128} == instrument `--json` population == `--summary` `TASKS_WITH_TOKEN` line (all six values equal; `json_vs_summary_population_agree=True`).
Role unit — `occurrence_roles` `{'value': 1435}` matches mine in both outputs.
Token unit — `original_occurrences_by_token` matches my flat census for all six tokens in both outputs.
Leaf unit (adjacent cross-check, not my assigned fields): distinct leaves from my provenance records by template {must_include[] 60, program_html[].url 338, reference_answer_raw_annotation 1, reference_url 205, start_url 812}, total 1416 == instrument `changed_leaves_by_path_template` (identical across all 3 profiles) and summary `changed_leaf_count=1416`; leaves with multiple occurrences: mine any-token=13, same-token=13 == instrument `changed_leaves_with_multiple_occurrences=[13]`. No occurrence/leaf/task pooling detected.

## Mismatches — exact locations and values
1. Zero mismatches in the six scoped provenance fields and three population fields (final comparison, `ORACLE_RESULT=AGREE`, scan.py EXIT=0).
2. One oracle-side convention divergence found and resolved (observed): my first run rendered `path_template` with a dot before brackets (`eval.program_html.[].url`); the instrument uses merged brackets (`eval.program_html[].url`). First run: `records_only_in_instrument=398 records_only_in_mine=398 field_or_membership_mismatches=398`, all 80 retained printed lines were path_template-only FIELD diffs of the url template; the findings file was overwritten by the rerun, so the residual 318 lines are not retained — [INFERENCE] they were the same bracket-diff on the 60 `must_include[]` occurrences plus url records, consistent with 338+60=398 array-containing occurrences in my final template census. After adopting merged-bracket rendering in my oracle: `instrument_matches_merged_bracket_style=1435/1435`. This is a rendering convention in my scanner, not an instrument defect; semantic leaf identity (pointer, task_index) agreed on all 1435 records in both runs.
3. Internal accounting quirk in my own script output (`dot_style=1037 other=-1037`): records without array segments satisfy both style predicates; oracle-internal, not an instrument claim.

## Offset semantics: codepoints, not bytes (observed + disclosed limit)
- All 1435 instrument offsets satisfy `text[off:off+len(token)] == token` under codepoint indexing (`instrument_offsets_not_landing_on_token_in_codepoint_space=0`).
- Limit: the pinned raw is pure ASCII (0 non-ASCII codepoints), so byte and codepoint offsets coincide numerically on this input; no pinned datum can discriminate byte vs codepoint indexing. Prereg names the requirement (quote, 12 words by `wc -w`): "raw occurrence provenance uses clearly named Unicode-codepoint offsets, NOT claimed byte offsets". Instrument `--json` LIMIT line likewise names codepoint offsets in the original raw text.
- Discriminative probe on my own synthetic fixture `{"a":"é__MAP__","é__MAP__":"x"}` (scratch only, not a pinned input): my scanner reports the value occurrence at codepoint offset 7 (byte offset would be 8) — my oracle is cp-based; the instrument's claim is consistent with, but not independently falsifiable by, this ASCII input.
- Escape safety: flat whole-text census and structural in-string census produce identical per-token offset lists, so no occurrence straddles an escape sequence or sits outside a JSON string; duplicate object keys: 0.

## Commands (exact)
- `python3 plans/config_projection.py --json` (cwd lane root) → rc 0, stdout 3881050 B, sha256 c8da0c5a…; stderr 0 B.
- `python3 plans/config_projection.py --summary` → rc 0, stdout 6914 B, sha256 5ce5cb0f…; stderr 0 B. `TOTAL findings=0 exit=0` in output.
- `python3 .ufo/waves/round-29/scratch/falsify/FOracleProvenance/scan.py` → first run EXIT=3 (convention mismatch state, as designed), final run EXIT=0, `ORACLE_RESULT=AGREE`.

## Environment / tooling record
No tools installed or upgraded (stdlib Python only; no pacman, uv, cargo, npm, or pip commands executed). No REA MCP devices used. No credentials, env values, or private URLs recorded. No fleet-repo mutation beyond my scratch dir and this report.

## Risks / limits
- Byte-vs-codepoint discrimination is vacuous on the pinned ASCII input (disclosed above); a non-ASCII pinned input would be needed to close it fully.
- The prereg prescribes provenance "by JSON path" without fixing a path rendering; I verified semantic leaf identity on every record and matched the instrument's bracket rendering 1435/1435. [INFERENCE] any downstream consumer parsing `path_template` strings should treat the rendering as instrument-defined, not contract-defined.
- First-run mismatch detail (318 of 398 lines) not byte-retained; totals and the 80-line sample are retained in this transcript and summarized above.

## Verdict basis (scoped to this item)
The falsification attack executed end-to-end: independent token contract from generator bytes, own structural scanner over the full 880,776-codepoint text, exhaustive occurrence mapping (1435/1435 records), offset-semantics check, and population verification across both instrument outputs. Every scoped field agreed; no defect found in occurrence provenance. This is a scoped result, not a round admission.

VERDICT: PASS

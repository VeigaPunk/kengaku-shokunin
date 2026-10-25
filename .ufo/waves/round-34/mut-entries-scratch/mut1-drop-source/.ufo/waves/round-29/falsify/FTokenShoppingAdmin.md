writer: KengakuR29-2.FTokenShoppingAdmin-2

# FTokenShoppingAdmin — independent `__SHOPPING_ADMIN__` census attack (round 29, post-crash falsify)

Lane root: /home/vgpnk/Projects/shokunin/kengaku-shokunin (lane master 56fd949a6478342531e61f4feecb4a685d831640).
Item under attack: the `__SHOPPING_ADMIN__` rows of `plans/config_projection.py --summary` and their
JSON counterparts, including the `__SHOPPING__` / `__SHOPPING_ADMIN__` substring-overlap question.

## Independence

I did **not** read, import, decompile or inspect `plans/config_projection.py` source. I derived every
count from the pinned generator bytes (`plans/fixtures/r29/generate_test_data.py`), the prereg text
(`plans/round-29-claims.md` lines 35-36), the pinned raw JSON, and `plans/fixtures/r29/profiles.json`;
I then compared only against the instrument's `--summary` stdout and `--json` output. The instrument
was executed read-only. No production file was modified; all scripts and outputs live in
`.ufo/waves/round-29/scratch/falsify/FTokenShoppingAdmin/`.

Pin checks (observed):
- raw input `plans/fixtures/r28/webarena/config_files/test.raw.json`: bytes 880776, decoded chars 880776,
  ASCII true, CR count 0, sha256 `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`
  — equals the `manifest.json` entry.
- my `--json` capture: 3881050 bytes, sha256 `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`
  — equals `json_output_sha256` in `.ufo/waves/round-29/candidate-freeze-v1.json`, so the bytes compared
  below are the frozen ones.

No tool installs or upgrades were needed or made (python3 3.14.8 stdlib, coreutils, preinstalled jq).

## Attacks and observations

Instrument runs: `python3 plans/config_projection.py --summary` (exit 0, 47 lines; line 47 is
`TOTAL findings=0 exit=0`) and `python3 plans/config_projection.py --json` (exit 0, 3881050 bytes,
hash above). Summary text captured at `.ufo/waves/round-29/scratch/falsify/FTokenShoppingAdmin/summary.txt`.

### 1. Global literal count in the raw text

Script: `census.py` (sha256 `d084f9f205a0a5b40862e6f175f09ff7e94083ba311fc2e0ebd5be8e2107c750`),
command `python3 census.py > census.out` (exit 0).

- `text.count("__SHOPPING_ADMIN__")` = **300**; sum over the six tokens = 1435.
- Independent tool cross-check: `grep -o '__SHOPPING_ADMIN__' test.raw.json | wc -l` = 300.
- Every `__X__` marker form in the file: `__GITLAB__` 385, `__REDDIT__` 336,
  `__SHOPPING__` 281, `__SHOPPING_ADMIN__` 300, `__WIKIPEDIA__` 0, `__MAP__` 133,
  plus non-token `__last_url__` 65 and `__page__` 12.
- Instrument: summary line 9 `ORIGINAL_OCCURRENCES_BY_TOKEN` reports 300; JSON
  `/population/original_occurrences_by_token/__SHOPPING_ADMIN__` = 300. **Match.**

### 2. Tasks carrying the token

- My dump-based count over the 812 parsed top-level objects: **182** tasks.
- `jq -c '.[]' test.raw.json | grep -c '__SHOPPING_ADMIN__'` = 182 (second implementation).
- Raw-slice attribution via my own JSON scanner agrees: 182 distinct task indices.
- `task_id` values are all ints, equal `0..811` exactly (812/812), so index and task_id cannot diverge
  for this count.
- Instrument: summary line 10 `TASKS_WITH_TOKEN` reports 182; JSON
  `/population/tasks_with_token/__SHOPPING_ADMIN__` = 182. **Match.**

### 3. Decoded leaves carrying the token

`census.py` walks all 10869 decoded string leaves of the raw JSON (independent structural walk):
- leaves containing `__SHOPPING_ADMIN__` = **300**; occurrences inside leaves = 300; tasks = 182.
- No leaf contains the token more than once (multi-occurrence leaves in the file: 13, all
  `__REDDIT__`/`__SHOPPING__`; list printed by `census.py`).
- Instrument: summary line 20/31/42 `changed_leaves_by_token` reports 300 in each of
  `distinct_origins`, `path_prefix`, `trailing_slash_sensitivity`; JSON per-profile
  `changed_leaves_by_token.__SHOPPING_ADMIN__` = 300. **Match.**

### 4. Per-profile applied replacements

`census.py` replays the pinned order GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP as
literal `str.replace` over the whole raw text, exactly as the generator bytes specify, using each
profile's `values` from `profiles.json`, and records the count observed at the step:

- `__SHOPPING_ADMIN__` replacements: **300** under each of the three profiles
  (`distinct_origins`, `path_prefix`, `trailing_slash_sensitivity`).
- Stepwise invariance: the remaining `__SHOPPING_ADMIN__` count is 300 after the GITLAB, REDDIT and
  SHOPPING passes, then 0 after its own pass; no earlier replacement creates or destroys the token.
- Projected text contains the SHOPPING_ADMIN profile value exactly 300 times in each profile; my
  projected-text sha256 values reproduce the instrument's three `projected_text_sha256` values
  (`2aec098e…`, `54cf9833…`, `49bbee2e…`).
- Instrument: summary lines 16/27/38 `applied_replacements` report 300 per profile; JSON
  per-profile `steps[name=SHOPPING_ADMIN].applied_replacements` = 300. **Match.**

### 5. Overlap by substring logic (`__SHOPPING__` vs `__SHOPPING_ADMIN__`)

- Pairwise substring matrix over all six tokens produced no pair where one token is a substring of
  another; explicit check `"__SHOPPING__" in "__SHOPPING_ADMIN__"` → `False`.
- Arithmetic witness: `text.count("__SHOPPING__")` 281 + `text.count("__SHOPPING_ADMIN__")` 300
  = 581, and `text.count("__SHOPPING")` (bare family prefix) = 581, so the 281 is entirely the
  `__SHOPPING__` form and does not include the 300 ADMIN form.
- Decoded-leaf overlap: leaves carrying both `__SHOPPING__` and `__SHOPPING_ADMIN__` = **0**.
  The instrument's per-leaf `tokens` arrays across all 812 tasks in each profile are singletons
  only (`__GITLAB__` 385, `__REDDIT__` 323, `__SHOPPING__` 275, `__SHOPPING_ADMIN__` 300,
  `__MAP__` 133, sums 1416 = `changed_leaf_count`), i.e. its per-token leaf counts are a partition
  and no double count is possible.
- Consequence checked, not assumed: because SHOPPING_ADMIN has 300 occurrences in 300 distinct
  leaves, "leaves carrying" and "occurrences" coincide for this token; the instrument reports the
  same number where its own semantics distinguish them.

### 6. Occurrence-level provenance (offset, pointer, task, template)

Script: `compare.py` (sha256 `dce7eff4a22337d85ef8f06cc8e004ba06ed454d4477b898a8e2c09820aece34`).
It re-parses the raw bytes with its own scanner (consumed 880776 of 880776 bytes), enumerates every
literal token occurrence in the raw text, attributes each to its containing string-literal span, and
builds `(offset, json_pointer, task_index, path_template)` tuples; then compares to
`/occurrence_provenance`.

- My occurrence entries: 1435, all in string values; key strings carrying any token: 0.
- Per token comparison, `extra_in_mine` / `missing_in_mine`: 0 / 0 for every one of the six tokens
  (GITLAB 385, REDDIT 336, SHOPPING 281, SHOPPING_ADMIN 300, WIKIPEDIA 0, MAP 133).
- `compare.py` final line: `TOTAL mismatched fields above: 0`.
- SHOPPING_ADMIN specifics, all identical on both sides: 300 entries, offsets monotonic, first
  offset 172 at `/0/start_url`, last offset 855286 at `/790/start_url`, 182 distinct tasks,
  templates `start_url` 182, `eval.program_html[].url` 90, `eval.reference_url` 28.
- Task-granularity check: for each of 812 tasks × 3 profiles, the sorted SHOPPING_ADMIN
  `changed_leaves[].json_pointer` list equals my independently built raw pointer list — 0 diffs,
  300 leaves per profile.
- Per-task occurrence distribution (mine): 88 tasks ×1, 82 ×2, 5 ×3, 4 ×4, 1 ×5, 2 ×6
  = 182 tasks, 300 occurrences; pointer lists above show the instrument collapses none of these.

### 7. Corroborating adjacent rows (same summary block)

- `changed_tasks_by_token.__SHOPPING_ADMIN__` = 182 in all three profiles (summary lines 21/32/43)
  equals my 182 carrying tasks. **Match.**
- `remaining_known_tokens_text` / `remaining_known_tokens_decoded` for SHOPPING_ADMIN = 0 per profile
  (summary lines 22-23, 33-34, 44-45). My post-replacement
  text/decoded counts are also 0. **Match.**
- `tokens_followed_by_slash` 697: my per-token count of occurrences immediately followed by `/`
  is GITLAB 225, REDDIT 232, SHOPPING 110, SHOPPING_ADMIN 125, MAP 5, WIKIPEDIA 0; sum 697.
  SHOPPING_ADMIN's 125 split: 175 occurrences followed by `"`, 125 followed by `/`. **Match.**
- Candidate table statement "sum 834, distinct 812": my sum of the six carrying-task counts is 834
  and their union is 812 of 812 tasks. **Match** (supporting, not the primary target).

### 8. Shadowed/synthetic contamination checks

- Duplicate-key shadowing could make a text-level count exceed a decoded-leaf count. A strict
  `json.loads(..., object_pairs_hook=...)` over the whole raw document raised no duplicate-key
  condition: the file has none, and my raw occurrence count (300) equals my decoded-leaf occurrence
  count (300), so no SHOPPING_ADMIN occurrence is hidden in an overwritten value.
- Profile values are synthetic and inert: none of the 18 values in `profiles.json` contains any of
  the six tokens or even an underscore, so replacements cannot create token occurrences that would
  inflate a later step's `applied_replacements`.
- Instrument stderr for the `--json` run: 0 bytes.

## Mismatches

**None.** Every SHOPPING_ADMIN field listed above (300 raw occurrences, 182 tasks, 300 decoded
leaves, 300 applied replacements per profile, 300 changed leaves per profile, 182 changed tasks per
profile, 0 remaining, 1435 total occurrence-provenance rows, all offsets/pointers/templates) matches
between my independent derivation and the frozen instrument output at the exact values above. No
location/value pair was found to report.

## Scope and inference

Observed: all counts, hashes, offsets, line numbers and comparison outputs above.

[INFERENCE] Because SHOPPING_ADMIN never repeats inside a single decoded leaf and no token is a
substring of another, the instrument's "occurrences" and "leaves" semantics cannot diverge for this
token on this input; that removes the one class of off-by-count ambiguity this item targeted.

[INFERENCE] The 13 multi-occurrence leaves are entirely REDDIT/SHOPPING, so the instrument's lower
`changed_leaves_by_token` values for those tokens (323, 275) are consistent with leaf-counting, not
with a lost occurrence; this is corroborating evidence for the SHOPPING_ADMIN row's semantics but is
not itself a claim about those tokens beyond the observed pointer equality.

This verdict covers only the `__SHOPPING_ADMIN__` census and its overlap arithmetic on the pinned
bytes. It does not validate other token semantics, per-file output hashes, hand fixtures,
runtime/scoring effects, or any deployment claim.

VERDICT: PASS

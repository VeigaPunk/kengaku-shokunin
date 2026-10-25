writer: KengakuR29-2.FPathRefUrl-2
seat: KengakuR29-2.FPathRefUrl-2 (leaf member; read-only; no subagents, no REA devices)
item: FPathRefUrl — attack the changed-leaf count and JSON-path category for template `eval.reference_url`
scope: round 29 integrated lane master 56fd949a6478342531e61f4feecb4a685d831640; instrument `plans/config_projection.py`
date: 2026-10-21

# Attack

Independent enumeration and re-derivation for the single template `eval.reference_url`:

1. authenticate the pinned inputs and bind the instrument output to them;
2. parse the pinned raw task file myself and enumerate **every** leaf at `eval.reference_url`
   (string, empty, non-string, token-bearing, token occurrences per token);
3. independently project the raw **text** with my own six sequential replacements per frozen
   profile, parse it, walk the result, and diff leaves against my walk of the raw parse —
   then derive `changed_leaves_by_path_template` and `changed_leaves_by_category` using the
   prereg rule (url_field = `start_url`, `eval.reference_url`, `eval.program_html[].url`;
   everything else non_url_field; strictly by JSON path);
4. compare all per-task changed-leaf records in `--json` (not only the `eval.reference_url`
   subset) against my independent records, including `original`, `projected`, `tokens`,
   `json_pointer`, `path_template`, `category`;
5. sample five changed `eval.reference_url` leaves per profile from `--json`, print
   original→projected, and re-derive each by hand from the decoded leaf with the same frozen
   profile values;
6. verify the 217 `eval.reference_url` provenance entries (offset slice, leaf containment);
7. check `--summary` text against the `--json` records and against the build receipts.

All experiments were read-only. My scripts and captures live only under
`.ufo/waves/round-29/scratch/falsify/FPathRefUrl-2/`; experiments needed no writes outside
`/tmp` and that scratch directory. No production file, fixture, corpus, SOURCES, SCORECARD,
lane jj state, lane Git index or candidate was written. No git write command was run (read-only
file reads and the instrument only).

## Independence statement

**I did not read or import `plans/config_projection.py` source.** I read only the prereg text
(`plans/round-29-claims.md`), the pinned generator bytes
(`plans/fixtures/r29/generate_test_data.py`, 838 bytes, 27 lines / 22 non-blank),
`plans/fixtures/r29/manifest.json`, `plans/fixtures/r29/profiles.json`, and the pinned raw file
`plans/fixtures/r28/webarena/config_files/test.raw.json`. My oracle implements the six sequential
`str.replace` calls on the raw text, its own `json.loads`, its own leaf walk and its own
path-template naming. The comparator consumes only the instrument's stdout (`--summary`,
`--json`). I did not inspect the instrument's implementation or its selftest.

## Tools

No tool installed or upgraded (python3 3.14 stdlib only; no pacman transactions).

# Observed facts

## Input authentication (sha256sum and one byte count)

| input | sha256 | size |
|---|---|---|
| `plans/fixtures/r29/manifest.json` | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` | 1,061 B |
| `plans/fixtures/r29/generate_test_data.py` | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` | 838 B |
| `plans/fixtures/r29/profiles.json` | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` | 1,391 B |
| `plans/fixtures/r28/webarena/config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | 880,776 B |

Generator bytes contain the six tokens at character offsets 271, 315, 359, 407, 467, 517 in
order GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP — matching the prereg order.

Instrument output capture:

| command | exit | observed |
|---|---|---|
| `python3 plans/config_projection.py --summary` | 0 | 47 lines, 6,914 bytes, sha256 `5ce5cb0f91ad279d446a475de757b9aa4a5b67a4b02df8d9aeac0d01be74636f`; two runs byte-identical; final line `TOTAL findings=0 exit=0` |
| `python3 plans/config_projection.py --json` | 0 | 3,881,050 bytes, sha256 `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`; identical to `corpus/evidence/round29-calibration/build-json-sha256.txt` |

`--json` binds `raw_text_sha256` = `7b50386f…`, `manifest_sha256` = `f6390b92…`, and `inputs`
digests equal to the table above. Live `--summary` equals
`corpus/evidence/round29-calibration/build-summary.txt` line-for-line except a literal trailing
`exit=0` line in the receipt (receipt 48 lines vs live 47); every metric line is identical.

## Raw leaf census at `eval.reference_url` (independent, units named)

812 leaves, one per task (`"reference_url"` key parent path is `/eval` in all 812 tasks;
812 raw key literals = 812 parsed keys):

- 805 JSON strings + 7 JSON `null` (tasks 118, 356, 369, 370, 371, 372, 373);
- of the 805 strings: 599 empty `""`, 1 non-URL prose value (task 247, 8 words,
  `Valorie doesn't have a email in the system`), and **205 token-bearing leaves**;
- 205 token-bearing leaves are 205 distinct tasks; token **occurrences** = 217:
  `__GITLAB__` 49, `__REDDIT__` 83, `__SHOPPING__` 52, `__SHOPPING_ADMIN__` 28,
  `__WIKIPEDIA__` 0, `__MAP__` 5;
- 7 of the 205 leaves are multi-occurrence (REDDIT: 3 leaves ×2, 3 ×3, 1 ×4 = 12 extra
  occurrences over 7 leaves); all 205 originals begin with the token (no scheme precedes it).

## Per-profile result (independent vs instrument)

My raw-text projection digests equal the instrument's `projected_text_sha256` exactly for all
three profiles: `2aec098e5705c98c7f7977a4eb8962aa455c2224d078dbfe4c1fc113e7c707f4`
(distinct_origins), `54cf98337dc6751d9453ee069ff26bb3836698518527cf8683c85bf66744744b`
(path_prefix), `49bbee2e827791b79f42858ac78637704adaa7e36f1cb3a9268563e8df3e01b2`
(trailing_slash_sensitivity).

| metric (units) | independent | `--summary` | `--json` records |
|---|---|---|---|
| leaves at `eval.reference_url` (leaves) | 812 | — | 812 leaves per profile walked |
| token-bearing leaves (leaves) | 205 | — | 205 changed ref records |
| changed leaves, template `eval.reference_url` (leaves) | 205 per profile | 205 per profile | 205 per profile |
| changed leaves, category `url_field` (leaves) | 1355 = 812 start_url + 205 ref + 338 program_html[].url | 1355 | 1355 |
| changed leaves, category `non_url_field` (leaves) | 61 = 60 must_include + 1 annotation | 61 | 61 |
| all changed leaves (leaves) | 1416 per profile | 1416 | 1416 |
| changed tasks (tasks) | 812 | 812 | 812 |
| multi-occurrence changed leaves (leaves) | 13 | 13 | 13 |
| string leaves (leaves) | 10869 | 10869 | 10869 |

Reference-leaf-only checks in each profile: every token-bearing leaf is in the changed set
(0 missing), no changed ref record lacks a token (0 extra), every ref record has
`json_pointer = /<task>/eval/reference_url`, `path_template = eval.reference_url`,
`category = url_field` (0 pointer/category anomalies), and no other JSON path carries a
`reference_url` key.

Record-level equality: for each profile the instrument's 1,416 changed-leaf records equal my
independently derived records as multisets of (task index, pointer, path template, category,
original, projected, token set) — 1,416 vs 1,416, **0 differences**; the 205 `eval.reference_url`
records are included. Leaf-level replacement equivalence (applying the six replacements to the
decoded original leaf) matched the instrument's projected value for every changed leaf in every
profile (0 mismatches).

## Category is genuinely path-derived on this input

All 60 changed `eval.program_html[].required_contents.must_include[]` leaves project to absolute
`http://…invalid…` URLs yet are reported `non_url_field`; the single changed
`eval.reference_answer_raw_annotation` leaf (task 66, two REDDIT occurrences in one value) also
projects to URLs and is `non_url_field`. So the observed split follows the declared JSON-path
predicate, not value shape: a value-based classifier would have produced 1,415 url_field / 1
non_url_field instead of the observed 1,355 / 61. For `eval.reference_url` itself the category is
`url_field` in all 205 records in all three profiles.

## Sample: five changed `eval.reference_url` leaves per profile, original → projected, hand re-derived

All 15 rows compare equal to my hand replacement of the decoded original with that profile's six
values (script `scratch/falsify/FPathRefUrl-2/sample.py` and the same picks in
`scratch/.../samples.json`; `ALL_EQUAL True N 15`).

| profile | task | original | projected (= hand) |
|---|---|---|---|
| distinct_origins | 258 | `__GITLAB__/explore` | `http://gitlab.invalid:10101/explore` |
| distinct_origins | 601 | `__REDDIT__/f/nyc` | `http://reddit.invalid:10102/f/nyc` |
| distinct_origins | 653 | `__SHOPPING__/contact` | `http://shopping.invalid:10103/contact` |
| distinct_origins | 676 | `__SHOPPING_ADMIN__/sales/order/` | `http://shopping-admin.invalid:10104/sales/order/` |
| distinct_origins | 380 | `__MAP__/search?query=bars%20near%20Carnegie%20Music%20Hall` | `http://map.invalid:10106/search?query=bars%20near%20Carnegie%20Music%20Hall` |
| path_prefix | 258 | `__GITLAB__/explore` | `http://gitlab.invalid:10201/prefix/explore` |
| path_prefix | 601 | `__REDDIT__/f/nyc` | `http://reddit.invalid:10202/prefix/f/nyc` |
| path_prefix | 653 | `__SHOPPING__/contact` | `http://shopping.invalid:10203/prefix/contact` |
| path_prefix | 676 | `__SHOPPING_ADMIN__/sales/order/` | `http://shopping-admin.invalid:10204/prefix/sales/order/` |
| path_prefix | 380 | `__MAP__/search?query=bars%20near%20Carnegie%20Music%20Hall` | `http://map.invalid:10206/prefix/search?query=bars%20near%20Carnegie%20Music%20Hall` |
| trailing_slash_sensitivity | 258 | `__GITLAB__/explore` | `http://gitlab.invalid:10301//explore` |
| trailing_slash_sensitivity | 601 | `__REDDIT__/f/nyc` | `http://reddit.invalid:10302//f/nyc` |
| trailing_slash_sensitivity | 653 | `__SHOPPING__/contact` | `http://shopping.invalid:10303//contact` |
| trailing_slash_sensitivity | 676 | `__SHOPPING_ADMIN__/sales/order/` | `http://shopping-admin.invalid:10304//sales/order/` |
| trailing_slash_sensitivity | 380 | `__MAP__/search?query=bars%20near%20Carnegie%20Music%20Hall` | `http://map.invalid:10306//search?query=bars%20near%20Carnegie%20Music%20Hall` |

The `//` in the last profile is the declared trailing-slash stimulus, not URL normalization: the
raw token is followed by `/`, so the written profile value's trailing `/` and the raw `/` are
adjacent. Instrument and hand derivation agree on every character.

Extra multi-occurrence probe (not one of the five): task 604's `eval.reference_url`
`__REDDIT__/f/deeplearning |OR| __REDDIT__/f/MachineLearning |OR| __REDDIT__/f/singularity`
projects to three replaced occurrences in one leaf in every profile, counted once as a changed
leaf, with the instrument's `tokens` field `["__REDDIT__"]` (deduplicated) and `original`
retaining all three literals (record equality above).

## Provenance for `eval.reference_url`

`--json` `occurrence_provenance` holds 217 `eval.reference_url` entries, exactly the independent
per-(task, token) occurrence multiset (same 217 pairs, by token 49/83/52/28/0/5). Every entry has
`string_role = value`, `json_pointer = /<task>/eval/reference_url`, and
`raw_text[offset:offset+len(token)] == token`; each offset also sits inside the decoded leaf's raw
literal at the leaf's value start (0 bad, 0 non-start). Entry order is grouped by token in the
replacement order, then ascending within a group; the prereg claims no ordering, so this is an
observation only. Total raw token occurrences 1,435 (= full-text count), and the sum of token
occurrences over parsed string values is also 1,435, i.e. no token occurrence hides in a key or a
shadowed duplicate key inside `eval.reference_url` (812 raw `"reference_url"` literals = 812
parsed keys).

## Unit reconciliation (leaves vs occurrences vs tasks)

1,435 occurrences − 1,416 changed leaves = 19 same-token repeats: `eval.reference_url` 12
(217−205), `start_url` 6 (818−812), annotation 1 (2−1). The 13 multi-occurrence leaves are
`eval.reference_url` 7 + `start_url` 5 (807×1, 4×2, 1×3) + annotation 1. Distinct-token overlaps
do not occur, which is why the instrument's per-token changed-leaf counts sum exactly to 1,416.

# Mismatches

**None.** No location or value mismatch was found between the independent enumeration and the
instrument's `--summary` / `--json` for template `eval.reference_url` (changed-leaf count 205 per
profile; category `url_field` 205/205; global category split 1,355/61), nor between the summary
text and the JSON records, nor between the live output and the build receipts.

Probes that would have produced a mismatch but did not: a token-bearing ref leaf missing from the
changed set; a changed ref record without a token; a ref pointer/category/template anomaly; a
token occurrence in a key or duplicate key; a non-string, empty or prose ref leaf changing; a
leaf-level replacement divergence; a summary number not reproducible from `--json`; a digit
difference in the projected-text digest; a provenance multiset or offset error.

# Inference

- [INFERENCE] The equality of projected-text digests to my own raw-text projection and the
  0-mismatch leaf-level equivalence are jointly sufficient for the numbers above to be
  text-faithful on this ASCII, escape-free input; they would not by themselves establish
  faithfulness for inputs containing JSON escapes, which the prereg explicitly declares outside
  the benign profile domain.
- [INFERENCE] Because every prose/empty/null ref leaf is unchanged and every token-bearing ref
  leaf changes, the 205 count is not sensitive to any judgment about URL validity of the leaf
  value; it is exactly the token-bearing-leaf count.
- [INFERENCE] The category output is consistent with the path-based predicate; the
  must_include counterfactual shows a value-based predicate would have reported a different
  split (1,415/1), so the observed 1,355/61 supports path-based classification.

# Residual unknowns

- I did not inspect `plans/config_projection.py` source, so I cannot state how it implements the
  path template or category internally; I only compared its outputs.
- I did not audit `--selftest`, the hand fixtures, mutation witnesses, the candidate text, or the
  S070–S073 rows; those belong to other items.
- I tested only the pinned raw input and the three frozen profiles; I constructed no adversarial
  synthetic input (no escaped-token or duplicated-key cases beyond confirming absence in the
  pinned bytes).
- `--json`'s `would_be_file_sha256` and index-mapping fields were not re-derived here (outside
  this item's scope); the `eval.reference_url` subset of the per-task objects was compared in full.

VERDICT: PASS

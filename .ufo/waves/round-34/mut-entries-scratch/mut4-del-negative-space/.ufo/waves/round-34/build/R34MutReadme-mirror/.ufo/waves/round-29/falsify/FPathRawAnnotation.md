writer: KengakuR29-2.FPathRawAnnotation-2

# FPathRawAnnotation-2 — changed-leaf count and JSON-path category for `eval.reference_answer_raw_annotation`

## Attack

Target: instrument `plans/config_projection.py` (sha256
`5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3`) under lane master
`56fd949a6478342531e61f4feecb4a685d831640`, metric `changed_leaves_by_path_template` for template
`eval.reference_answer_raw_annotation` and its contribution to `changed_leaves_by_category`
(`url_field` = `start_url`, `eval.reference_url`, `eval.program_html[].url`; all else `non_url_field`).
Attack: independently enumerate every raw task leaf at that path, identify which contain a pinned token,
count changed leaves per profile, and compare with `--summary` and `--json`; then re-derive the changed
leaf values by hand.

Independence: I did **not** read or import `plans/config_projection.py` source. I used only the prereg
text (`plans/round-29-claims.md`), the pinned generator bytes, the pinned raw/profile JSON, and the
instrument's stdout (`--summary`, `--json`). My re-derivation is
`.ufo/waves/round-29/scratch/falsify/FPathRawAnnotation-2/independent.py`; its stdout is
`run.txt`, and the instrument's captured JSON is `proj.json`.

## Authenticated inputs (observed)

```
f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87  plans/fixtures/r29/manifest.json
7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652  plans/fixtures/r28/webarena/config_files/test.raw.json
45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd  plans/fixtures/r29/generate_test_data.py
90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018  plans/fixtures/r29/profiles.json
c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630  my rerun of `--json`
```

The rerun digest equals the freeze pin `candidate-freeze-v1.json` and `corpus/evidence/round29-calibration/build-json-sha256.txt`,
so the compared output bytes are the frozen ones. Raw file: 880,776 bytes, ASCII, zero CR, zero duplicate
JSON keys, 29,604 lines, 812 tasks.

## Independent census at the path (observed)

Python `json.loads` of the pinned raw bytes, then a full string-leaf walk (root task array excluded from
the path template):

- tasks: 812; distinct `task_id`: 812; `output_index == task_id` 812/812.
- leaves at `eval.reference_answer_raw_annotation`: **332** (all `str`); the literal key occurs 332 times
  in the raw text. **480 tasks have no such key** (first: 44, 45, 46, 102, 103; their `eval` objects carry
  `eval_types`, `program_html`, `reference_answers`, `reference_url`, and sometimes `string_note`/`url_note`).
- token-bearing leaves at this path: **1**, task index/task_id 66, json_pointer
  `/66/eval/reference_answer_raw_annotation`, raw line **2126**, containing `__REDDIT__` **2** times
  (codepoint offsets 61888 and 61968; raw slice at each offset equals `__REDDIT__`).
- no other `__[A-Za-z_]+__` marker appears in any leaf at this path (marker census over all 332 leaves:
  `{'__REDDIT__': 2}`); no leaf at this path is a URL field by the stated strict path rule.
- no alternate encoding or casing hides an occurrence: `\u005f` sequences 0, standalone `REDDIT` outside
  the token 0, `__Reddit__`/`__reddit__` 0; projected trees retain 0 of all six known tokens in all profiles.
- total string leaves (all paths): **10869**, equal to the instrument's `string_leaf_count`; no leaf was
  added or hidden by the instrument's walk.

Faithful projection re-derived from the generator bytes
(`plans/fixtures/r29/generate_test_data.py:11-16`, order GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN,
WIKIPEDIA, MAP, then `json.loads` at `:20`) applied sequentially to the serialized text:

| profile | changed leaves at this template | unchanged present leaves | absent tasks | changed leaf total | url_field | non_url_field |
|---|---|---|---|---|---|---|
| distinct_origins | 1 | 331 | 480 | 1416 | 1355 | 61 |
| path_prefix | 1 | 331 | 480 | 1416 | 1355 | 61 |
| trailing_slash_sensitivity | 1 | 331 | 480 | 1416 | 1355 | 61 |

Non-URL total decomposes exactly as 60 `eval.program_html[].required_contents.must_include[]` leaves +
1 `eval.reference_answer_raw_annotation` leaf; URL total as 812 `start_url` + 205 `eval.reference_url` +
338 `eval.program_html[].url`; 1355 + 61 = 1416.

## Instrument output compared (observed)

`python3 plans/config_projection.py --summary` (exit 0, `TOTAL findings=0 exit=0`), lines 19/30/41:

```
PROFILE distinct_origins changed_leaves_by_path_template={"eval.program_html[].required_contents.must_include[]": 60, "eval.program_html[].url": 338, "eval.reference_answer_raw_annotation": 1, "eval.reference_url": 205, "start_url": 812}
PROFILE distinct_origins changed_leaves_by_category={"non_url_field": 61, "url_field": 1355}
```

The `path_prefix` and `trailing_slash_sensitivity` lines (30/31 and 41/42) are numerically identical for
these metrics. `--summary` and `--json` agree on every template and category count for all three profiles
(checked programmatically).

`--json` per-task records: exactly **1** changed leaf with `path_template == eval.reference_answer_raw_annotation`
in each of the 3×812 task records (3/2436 projections); each is `/66/eval/reference_answer_raw_annotation`
with `category = non_url_field` and `tokens = ['__REDDIT__']`. `occurrence_provenance` has exactly **2**
entries for this path, both task_index 66, offsets 61888 and 61968, pointer
`/66/eval/reference_answer_raw_annotation`; both offsets slice to `__REDDIT__` in the original text.
Task record: `output_index` 66, `output_filename` `config_files/66.json`, `index_equals_task_id` true.

## Sampled changed leaves, re-derived by hand

The requested five changed leaves at this template per profile do not exist: the changed-leaf population
at this template is exactly **1** per profile (task 66), so all three profile variants are enumerated below
rather than sampled. Original (raw line 2126):

```
__REDDIT__/f/books/59396/apple-books-has-a-free-audiobook-of-a-christmas-carol, __REDDIT__/f/books/17445/i-just-finished-reading-the-hobbit-to-my-6-year-old-daughter
```

Hand rule: substitute the profile's REDDIT value for both occurrences; no other token touches this leaf.

| profile | REDDIT value | hand-derived projected value | equals `--json` projected |
|---|---|---|---|
| distinct_origins | `http://reddit.invalid:10102` | `http://reddit.invalid:10102/f/books/59396/apple-books-has-a-free-audiobook-of-a-christmas-carol, http://reddit.invalid:10102/f/books/17445/i-just-finished-reading-the-hobbit-to-my-6-year-old-daughter` | yes |
| path_prefix | `http://reddit.invalid:10202/prefix` | `http://reddit.invalid:10202/prefix/f/books/59396/apple-books-has-a-free-audiobook-of-a-christmas-carol, http://reddit.invalid:10202/prefix/f/books/17445/i-just-finished-reading-the-hobbit-to-my-6-year-old-daughter` | yes |
| trailing_slash_sensitivity | `http://reddit.invalid:10302/` | `http://reddit.invalid:10302//f/books/59396/apple-books-has-a-free-audiobook-of-a-christmas-carol, http://reddit.invalid:10302//f/books/17445/i-just-finished-reading-the-hobbit-to-my-6-year-old-daughter` | yes |

The trailing-slash double slash is the expected profile stimulus seam, not a repair or normalization. The
hand derivation was produced by direct `str.replace` on the retrieved original value (no instrument code),
and it equals the instrument's `projected` field for all three profiles.

## Exhaustive cross-check beyond the sample

Rather than only sampling, I compared my independent projection against every changed leaf the instrument
reports: for each profile, 1416 (json_pointer, path_template, category, tokens, original, projected)
records against my own text-level projection and tree diff. Results: **0 mismatches**; projected-text
sha256 equals the instrument's per profile (`2aec098e…`, `54cf9833…`, `49bbee2e…`); all 812 tasks parse in
each profile; all key sequences are unchanged (tokens occur only inside string values). Unit separation
also matches: this leaf has 2 token occurrences but 1 changed leaf; it is one of the instrument's 13
`changed_leaves_with_multiple_occurrences`, and `changed_leaves_by_token["__REDDIT__"]` is 323 leaves
versus 336 raw occurrences (the 13-leaf multi-occurrence gap), both reproduced independently.

## Mismatches

None. Specifically:
- changed-leaf count at `eval.reference_answer_raw_annotation`: instrument 1 per profile = independent 1
  per profile (raw token-bearing leaves 1; absent-key tasks 480 are not leaves and are not counted as
  changed);
- JSON-path category: instrument assigns the leaf to `non_url_field`; the strict path rule does the same,
  and the non-URL total 61 = 60 `must_include` + 1 annotation both ways;
- occurrence/leaf units: 2 occurrences vs 1 leaf is reported as such (provenance 2 entries; template 1);
- `--summary` and `--json` agree; the JSON bytes match the frozen sha256.

Non-mismatch observations worth recording: (a) the template exists in only 332/812 raw tasks, so any
future wording implying 812 leaves at this path would be wrong, but no compared instrument metric or
candidate number makes that claim: candidate draft line 44 states this template contributes 1 changed
leaf, and build report `.ufo/waves/round-29/build/R29Task590.md:206` states 332 leaves (1 changed); (b) the strict
category rule calls this URL-shaped annotation `non_url_field`, which is the declared rule, not a defect;
(c) [INFERENCE] the 480 missing keys reflect the upstream dataset's per-eval-type shape, not an instrument
exclusion, since the independent all-path string-leaf total equals the instrument's 10869.

## Residual unknowns

- Runtime scorer treatment of the annotation is outside this item and unread; this verdict covers only
  count/category consistency of the projection output.
- The raw file is ASCII, so codepoint and byte offsets coincide here; this item cannot distinguish the
  two offset definitions (the summary discloses the ASCII/inert case).
- No tool install/upgrade was needed; no pacman or other transaction was run.

VERDICT: PASS

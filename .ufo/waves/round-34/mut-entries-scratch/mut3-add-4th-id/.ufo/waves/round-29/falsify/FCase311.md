writer: KengakuR29-2.FCase311-2

# FCase311 — per-task falsification of raw task_id 311 under all three profiles

Lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Attacks claim C1
(`plans/round-29-claims.md`) at one unit: the exact projected object, changed leaves and would-be file
digest for raw `task_id` 311 in each of the 3 frozen profiles. Read-only leaf: no production, fixture,
corpus, SOURCES, SCORECARD or candidate file was touched. All experiments were written under
`.ufo/waves/round-29/scratch/falsify/FCase311-2/` and `/tmp/r29f311/`. No installs and no upgrades, so no
tool row; interpreter was `Python 3.14.8`.

**Independence statement (required):** I did **not** open, read or import `plans/config_projection.py`
source at any point; the instrument was only executed and its `--summary` / `--json` / `--selftest`
stdout consumed. My derivation uses the prereg text, the pinned generator bytes, the pinned raw file and
the pinned profiles only. After my own checks were complete I read sibling report `falsify/FCase500.md`
for report shape and for its generator-execution oracle technique; none of its numbers were reused here.
I did not read the knowledge candidate draft.

## Observed: pinned inputs (my `hashlib.sha256` over the lane files)

| file | sha256 | vs manifest |
|---|---|---|
| `plans/fixtures/r29/generate_test_data.py` | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` | match |
| `plans/fixtures/r28/webarena/config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | match |
| `plans/fixtures/r29/profiles.json` | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` | match |
| `plans/fixtures/r29/manifest.json` | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` | equals `--json.manifest_sha256` |

Generator read as inert bytes (`nl -ba`, 27 lines): lines 11–16 are the six `raw.replace` calls in the
manifest order GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP; line 20 is `json.loads(raw)`;
line 21 iterates `enumerate(data)`; lines 22–23 write `config_files/{idx}.json` via `json.dump(item, f, indent=2)`.
Whole raw file: 880776 bytes, 880776 codepoints, non-ASCII bytes 0, CR count 0.

## Observed: the raw unit (own `json.JSONDecoder.raw_decode` scan of the original text)

- Raw list position 311, `task_id` 311, span codepoints `[286827, 287694)` = 867 characters,
  source lines 9699–9727 (1-based). `task_id`s in the file are exactly `0..811` in order (my scan).
- 12 keys: `sites`, `task_id`, `require_login`, `storage_state`, `start_url`, `geolocation`,
  `intent_template`, `instantiation_dict`, `intent`, `require_reset`, `eval`, `intent_template_id`.
- Exactly **1** token occurrence inside the span: `__GITLAB__` at codepoint 286981 (source line 9706,
  column 19, 1-based), inside `"start_url": "__GITLAB__"`. Zero `__REDDIT__`, `__SHOPPING__`,
  `__SHOPPING_ADMIN__`, `__WIKIPEDIA__`, `__MAP__`, `__last_url__`, `__page__` in the span.
- `eval.reference_url` is the empty string; `eval.program_html` is empty; `eval.reference_answers.exact_match`
  is `Erik Linder-Norén` reached through the source escape `\u00e9`; `storage_state`
  `./.auth/gitlab_state.json`; `sites` `["gitlab"]`; `intent_template_id` 323.

## Observed: my derivation vs the instrument record at `output_index` 311 (3 profiles)

Profile GITLAB values: `http://gitlab.invalid:10101` / `http://gitlab.invalid:10201/prefix` /
`http://gitlab.invalid:10301/`. My derivation applies the six text replacements in manifest order to the
whole raw text, parses, and deep-diffs leaf sets (equal leaf sets between original and projected objects).

| field | distinct_origins | path_prefix | trailing_slash_sensitivity |
|---|---|---|---|
| `/311/start_url` original | `__GITLAB__` | `__GITLAB__` | `__GITLAB__` |
| `/311/start_url` projected, my derivation | `http://gitlab.invalid:10101` | `http://gitlab.invalid:10201/prefix` | `http://gitlab.invalid:10301/` |
| my changed-leaf count | 1 | 1 | 1 |
| instrument `changed_leaves` count | 1 | 1 | 1 |
| `category` / `path_template` / `tokens` | `url_field` / `start_url` / `["__GITLAB__"]` | same | same |
| `json_pointer` | `/311/start_url` | same | same |
| `output_index` / `task_id` / `output_filename` / `index_equals_task_id` | 311 / 311 / `config_files/311.json` / true | same | same |
| `would_be_file_sha256` instrument | `6bc804f5979ee0d948ac85aebee3c957d2aa8571b62900daf6196e9136485b2d` | `42c4ca2b6de84d35acacb4fe98171dbf4b487e50a57ef83119119beec62369a3` | `26e48262ceb8a775c445158b0ede2c87675a3288f85da1f7383c53e81781dc90` |
| same sha, my `json.dumps(item, indent=2)` | identical | identical | identical |
| same sha, **executed pinned generator** | identical | identical | identical |
| file bytes / trailing newline | 828 / none | 835 / none | 829 / none |
| leftover six markers in file / any `//` in file | 0 / 0 | 0 / 0 | 0 / 0 |

All 12 compared fields agree for all 3 profiles (36/36 comparisons, script `compare311.py`). The
instrument `projected_task` is dict-equal to my independently parsed projected object in all 3 profiles
(12 keys each), and to the object parsed from the generator's own `config_files/311.json`.

## Observed: executed-upstream oracle (independence beyond the instrument)

Copies only, under `/tmp/r29f311/<profile>/`: pinned generator bytes + pinned raw file in `config_files/`,
a two-file stub package `browser_env/` whose `env_config.py` holds that profile's six values, `PYTHONPATH`
pointed at the stub, cwd at the copy. For each of the 3 profiles: exit 0, empty stderr, 814 directory
entries in `config_files/` (812 index files + `test.json` + the copied `test.raw.json`),
`config_files/311.json` sha256 equal to the instrument's `would_be_file_sha256` above,
`config_files/test.json` sha256 equal to that profile's `projected_text_sha256`
(`2aec098e…`, `54cf9833…`, `49bbee2e…`), parsed `311.json` equal to `projected_task`, zero remaining
`__…__` markers. The generated `311.json` carries exactly 2 escaped `\u00e9` sequences, 0 raw UTF-8 bytes
for `é`, and is pure ASCII: decoding `\u00e9` and re-dumping with `ensure_ascii=True` restores the source
escape bytes, so projection does not perturb this non-ASCII annotation.

## Observed: aggregate cross-checks that bound this unit

`--summary`, `--json`, `--selftest`: exit 0 each. `--json` (`findings` empty) byte sha256
`c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`, equal to
`corpus/evidence/round29-calibration/build-json-sha256.txt`, so what I attacked is the build-wave
artifact. `--selftest` reports `SELFTEST clean cases=20` and exit 0.

My independent full-file reproduction of every record and aggregate (script `fullcmp2.py`): **38328
equality checks, 0 failures**, covering for all 812 tasks × 3 profiles the projected object, changed-leaf
set/values/tokens/category/path-template, `output_filename`, `index_equals_task_id`,
`would_be_file_sha256`, JSON-pointer resolvability of every reported leaf against the projected array,
plus per-profile `changed_leaf_count` 1416, `changed_task_count` 812, `string_leaf_count` 10869,
categories `{url_field: 1355, non_url_field: 61}`, 5 path templates
(`start_url` 812, `eval.program_html[].url` 338, `eval.reference_url` 205, `must_include[]` 60,
`eval.reference_answer_raw_annotation` 1), `changed_leaves_by_token`
385/323/275/300/133, `changed_leaves_with_multiple_occurrences` 13, applied replacements
385/336/281/300/0/133 per step, and `projected_text_sha256`.

Occurrence provenance: 1435 rows, all `string_role` `value`, grouped contiguously by replacement step
(GITLAB 385, REDDIT 336, SHOPPING 281, SHOPPING_ADMIN 300, MAP 133, WIKIPEDIA 0 rows); for every row
`raw[offset:offset+len(token)]` equals the token and the offset lies inside that `task_index`'s span
(0 mismatches); per-task row counts equal my raw-span token counts for all 812 tasks (min 1, max 12);
task 311 has exactly 1 row, offset 286981, pointer `/311/start_url`.

## Findings that qualify the claim (no mismatch, but novelty-bearing)

1. **Key-order trap (corroborated independently).** The record's `projected_task` is emitted key-sorted
   while the generator preserves raw order; my insertion-order dump reproduces the reported hash, my
   sorted-key dump gives `37b76497a5554d7d17292200ba21c5a6f63539e46f74ad31a4515fc964de2b73` and a
   trailing-newline dump gives `b80c681b8d380da6653ea81b3a804bdc671a472d00622090784b3b88b1aa6788`,
   neither equal to the reported `6bc804f5…`. Byte identity is carried only by `would_be_file_sha256`; a
   consumer re-serializing `projected_task` from the record would report a false mismatch.
   [INFERENCE] presentation property, not a projection error.
2. **Provenance rows are ordered by replacement step, not by document position.** Task 681's rows begin
   with `must_include/1` at offset 692104 before its `start_url` at 691212; 13 tasks have
   non-increasing within-task offsets for this reason. Task 311 is single-row, so its record is
   unaffected; a consumer walking provenance as a document-order stream would mis-locate rows.
3. **Codepoint-vs-byte offsets are unobservable on the pinned input.** The raw file is pure ASCII
   (880776 bytes = 880776 codepoints); for task 311 the prefix has 286981 bytes and 286981 codepoints.
   The claim's codepoint-offset requirement is therefore exercised only by the selftest case
   `codepoint_offsets_and_key_token`, not by any pinned-data row.
4. **This unit cannot discriminate the order or positional-naming axes.** `task_id` equals array index
   for all 812 items, so index 311 = `task_id` 311 and a task_id-keyed implementation would agree. My
   decoded-leaf-rewrite oracle equals sequential text replacement for all 812 tasks in all 3 profiles
   (0 differing tasks), no token is a substring of another token, and no profile value contains a token,
   so the frozen corpus cannot distinguish replacement-order implementations at all; that evidence rests
   on the selftest hand case `hand_cascade_order_R29_ORDER_CASCADE_01`.
5. **Multi-occurrence multiplicity is not a per-leaf field.** Task 311 has one occurrence in one leaf, so it
   cannot show this; for comparison, task 66's `eval/reference_answer_raw_annotation` leaf lists
   `tokens` `["__REDDIT__"]` while carrying 2 occurrences, visible only as 2 provenance rows on the same
   pointer. A record-only reader cannot tell 1 from 2 occurrences without cross-referencing
   `occurrence_provenance`.
6. **Trailing-slash junction count is unit-irrelevant here.** Task 311's `start_url` is a bare token, so
   under the trailing-slash profile the generated file contains no `//` at all; I did not independently
   recompute the corpus-wide 697 junction total, and this unit contributes no junction.

## Your two specific questions

- **Non-URL field change: none** for task 311. The raw-vs-projected deep leaf diff is exactly the single
  `/311/start_url` leaf in each profile, and that field is URL-valued by name; `storage_state`, `sites`,
  `intent`, `eval.reference_url` (empty), `eval.program_html` (empty) and both annotation strings are
  unchanged. For scale, my independent census reproduces 61 non-URL-field leaves per profile, split as
  `must_include[]` 60 + `reference_answer_raw_annotation` 1 (task 66); filtered to `/311/` the set is empty.
- **Multi-occurrence leaf: none** for task 311 — 1 occurrence, 1 leaf, `tokens` length 1. Corpus-wide my
  count of leaves holding more than one occurrence is 13 (tasks 66, 431, 432, 433, 434, 435, 604, 608,
  609, 625, 681, 682, 683, occurrences 2–4 each), equal to the instrument's 13; none under `/311/`.

## Unresolved gaps / scope of this verdict

- I did not read the instrument source, so the internal `url_field` vs `non_url_field` rule is unaudited;
  task 311's only changed leaf is URL-valued by field name and does not stress that rule.
- Task 311 exercises the minimal path: one token, one leaf, no eval URL, no non-URL field, no quote or
  backslash, no cascade, no multi-occurrence; the candidate's quote/backslash, cascade and
  index-shuffled disclosure branches are not exercised by this unit.
- One `task_id` × 3 synthetic profiles of an offline projection; no deployment, runtime, task-validity or
  model claim is tested.

Mismatches found: none, in any compared field, across all three profiles; the executed pinned generator
independently reproduces every reported byte identity for this unit.

VERDICT: PASS

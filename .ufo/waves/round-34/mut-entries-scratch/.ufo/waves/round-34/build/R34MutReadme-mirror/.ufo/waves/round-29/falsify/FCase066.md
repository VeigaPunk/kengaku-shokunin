writer: KengakuR29-2.FCase066-2

# FCase066 — per-task attack on raw task_id 66 under all three frozen profiles

Lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Attacks claim C1
(`plans/round-29-claims.md`, "One declared claim", lines 7-13) at one unit: the exact projected
object, every changed leaf, the output ordinal/filename and the would-be file digest for raw
`task_id` 66 in each of the 3 frozen profiles. Read-only leaf: no production, fixture, corpus,
SOURCES, SCORECARD, candidate or lane jj/Git index file was touched. No tool installs or upgrades,
so there is no tool/version row. All write-side experiments ran on copies under `/tmp/f66`.

**Independence statement (required):** I did **not** read, open or import
`plans/config_projection.py` source at any point. Inputs read: the prereg TEXT
(`plans/round-29-claims.md`), the pinned generator bytes, the pinned raw JSON, `profiles.json`,
`manifest.json`, the candidate draft paragraph quoted below for wording, and instrument
`--json`/`--summary`/`--selftest` **output only**. My derivation is my own script
(`.ufo/waves/round-29/scratch/falsify/FCase066/derive66.py`, written this seat), plus execution of
the pinned generator bytes themselves as a second, independent oracle.

## Observed: pin integrity before any derivation

`sha256sum plans/fixtures/r29/generate_test_data.py plans/fixtures/r29/profiles.json
plans/fixtures/r28/webarena/config_files/test.raw.json plans/fixtures/r29/manifest.json`:

| file | sha256 | vs manifest |
|---|---|---|
| `r29/generate_test_data.py` | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` | match |
| `r28/webarena/config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | match |
| `r29/profiles.json` | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` | match |
| `r29/manifest.json` | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` | equals `--json.manifest_sha256` |

`--json.inputs` repeats those three hashes exactly; `--json.upstream_revision` is
`dce04686a56253aefba7b18a4fa0937cf1dc987b`. Raw file: 880776 bytes, 880776 codepoints, delta 0;
non-ASCII codepoints 0; CR count 0; tabs 0. Generator contract re-read from bytes: line 5
`from browser_env.env_config import *`; lines 11-16 six global `raw.replace` calls in order GITLAB,
REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP; line 20 `data = json.loads(raw)`; line 21
`for idx, item in enumerate(data)`; line 23 `json.dump(item, f, indent=2)` into
`config_files/{idx}.json`. This matches `--json.source_contract` field for field
(replace_steps lines 11..16, parse_line 20, enumerate_loop_line 21, env_config_star_import_line 5,
per_task_filename_template `config_files/{idx}.json`).

## Observed: the raw unit (own scanner, `json.JSONDecoder.raw_decode` over the original text)

- Raw list position 66, `task_id` 66, span codepoints `[60828, 62094)`, length 1266.
- 12 top-level keys (raw order: `sites`, `task_id`, `require_login`, `storage_state`, `start_url`,
  `geolocation`, `intent_template`, `instantiation_dict`, `intent`, `require_reset`, `eval`,
  `intent_template_id`); `eval` has 6 keys; `sites` = `["reddit"]`; `storage_state` =
  `./.auth/reddit_state.json`; `require_login` true; `require_reset` false; `intent_template_id` 17.
- Exactly 3 `__REDDIT__` occurrences inside the span, at codepoint offsets 60981, 61888, 61968.
  Verified by slicing: `raw_text[o:o+10] == "__REDDIT__"` for all three; following characters are
  `",\n ` (start_url) and `/f/b` (both annotation occurrences). Zero occurrences of `__GITLAB__`,
  `__SHOPPING__`, `__SHOPPING_ADMIN__`, `__WIKIPEDIA__`, `__MAP__`, `__last_url__`, `__page__` in
  the span. The 62094-char span ends `  "intent_template_id": 17\n  }`, i.e. the bracket closes the
  object.
- `start_url` = `__REDDIT__` exactly (1 occurrence). `eval.reference_url` = `""` and
  `eval.program_html` = `[]`, so neither changes.
- `eval.reference_answer_raw_annotation` holds the token twice, joined by the literal `, `:
  `__REDDIT__/f/books/59396/apple-books-has-a-free-audiobook-of-a-christmas-carol, __REDDIT__/f/books/17445/i-just-finished-reading-the-hobbit-to-my-6-year-old-daughter`.
- `eval.reference_answers.must_include` holds the same two paths under the concrete origin
  `http://www.reddit.com`. Observed equality: replacing the token in the annotation with
  `http://www.reddit.com` yields exactly `", ".join(must_include)` (True). These two `must_include`
  leaves carry no token, so the generator leaves them at the public origin.

## Observed: my derivation vs the record, per profile

Derivation: concatenate the six replacements in generator order on the raw text, `json.loads`,
take list position 66, `json.dumps(item, indent=2)`, sha256. Oracle: run the pinned
`generate_test_data.py` bytes unmodified in `/tmp/f66/run_<profile>/` with a stub
`browser_env/env_config.py` holding that profile's six values (cwd = copy of `scripts/`).

| unit | distinct_origins | path_prefix | trailing_slash_sensitivity |
|---|---|---|---|
| profile REDDIT value | `http://reddit.invalid:10102` | `http://reddit.invalid:10202/prefix` | `http://reddit.invalid:10302/` |
| `/66/start_url` projected (mine, record, oracle agree) | `http://reddit.invalid:10102` | `http://reddit.invalid:10202/prefix` | `http://reddit.invalid:10302/` |
| `/66/eval/reference_answer_raw_annotation` projected | both paths under `http://reddit.invalid:10102` | both under `…:10202/prefix` | both under `…:10302/` with `//f/books/…` |
| my deep-diff changed leaves | 2 | 2 | 2 |
| record `changed_leaves` count | 2 | 2 | 2 |
| `would_be_file_sha256`, record | `59c3f4be74f15eb7c4b8af8480723d9db77e6264cd425726a4e03c2252cff6d3` | `3e9f2ade43df0d51e11cdf49af07abe8d03945b526c28b21449d7edaedb00721` | `7a44cd0f4cce43c77348672af9e60739014dd34ec49ff3e06da0622683d2c9a1` |
| sha256 of my dump | identical | identical | identical |
| sha256 of executed generator file | identical | identical | identical |
| file bytes | 1251 | 1272 | 1254 |
| `config_files/test.json` sha256 = record `projected_text_sha256` | `2aec098e5705c98c7f7977a4eb8962aa455c2224d078dbfe4c1fc113e7c707f4` | `54cf98337dc6751d9453ee069ff26bb3836698518527cf8683c85bf66744744b` | `49bbee2e827791b79f42858ac78637704adaa7e36f1cb3a9268563e8df3e01b2` |

Every generator run exited 0 and produced 814 `config_files/` entries (812 index files + generated
`test.json` + the copied input `test.raw.json`); `config_files/66.json` is byte-identical to my
dump in all three profiles, and has no trailing newline. Cross-profile deep diff of the projected task at 66 is exactly those 2 leaves in
all three pairwise comparisons.

Per-task record, all three profiles: `task_id` 66, `output_index` 66, `output_filename`
`config_files/66.json`, `index_equals_task_id` true, `projected_task` equal to my parsed object
(12 keys, no additions/removals), `changed_leaves` pointers `/66/start_url` (`category`
`url_field`, `path_template` `start_url`) and `/66/eval/reference_answer_raw_annotation`
(`category` `non_url_field`, `path_template` `eval.reference_answer_raw_annotation`), `tokens`
`["__REDDIT__"]` on both, `original`/`projected` strings equal to the pre/post values above. No
derived changed leaf is missing from the record; the record lists no leaf my diff does not find.

## Observed: occurrence provenance for task 66

`--json.occurrence_provenance` filtered to `task_index == 66` returns exactly 3 rows, all
`string_role` `value`: offsets 60981 (`/66/start_url`), 61888 and 61968
(`/66/eval/reference_answer_raw_annotation`); each row's token slice in the original text equals
`__REDDIT__`. 3 rows = 3 span occurrences = my count; there are no provenance rows for task 66 at
any other offset. The offsets are codepoint offsets (Python `str` indexing verifies the slices);
because the file is pure ASCII, the same numbers are also byte offsets, so this input cannot
distinguish the two units (limitation 5 of `--json`, "the pinned raw file is ASCII without carriage
returns", is factually true: 0 non-ASCII codepoints, 0 CR).

## Observed: the two asked-for classes

- **Non-URL field change:** exactly one for task 66 — `/66/eval/reference_answer_raw_annotation`,
  `category` `non_url_field`, changed in every profile. Its *value* is URL text (two
  `scheme://host/path` answers), so the label must be read as field-role, not value shape: the same
  instrument labels a `…/required_contents/must_include[]` leaf `non_url_field` although its
  `projected` value is `http://reddit.invalid:10102/f/space/134164/…`. The task-66
  `must_include` leaves are URL-shaped but unchanged (concrete origin above). Draft wording —
  "Global text replacement reaches non-URL fields." — is true only under that field-role reading;
  it is not a statement that the changed values lack URLs. This is a labeling ambiguity, not a
  projection mismatch.
- **Multi-occurrence leaf:** `/66/eval/reference_answer_raw_annotation` holds **2** occurrences of
  the same token. The per-task record exposes only the deduplicated `tokens` list, so multiplicity
  is visible only by joining `occurrence_provenance` (2 rows, same pointer, different offsets) or
  the profile aggregate (`changed_leaves_with_multiple_occurrences` 13). My independent population
  count of changed leaves with >1 occurrence is exactly 13 (2 occurrences: 8 leaves, 3: 4, 4: 1),
  and task 66 is one of the eight; 0 leaves carry two *different* tokens, so `tokens` dedup hides
  only repeats. The two task-66 occurrences are both followed by `/`, so they produce the
  `…:10302//f/books/…` double slash under the trailing profile and contribute 2 of the 697
  `tokens_followed_by_slash` / `value_slash_then_raw_slash_junctions`.

## Aggregate cross-checks (all equal, units named)

`--summary` exit 0, 0 findings; `--json.findings` empty; `--selftest` exit 0
(`SELFTEST clean cases=20 …`). My independent counts: string leaves 10869 = `string_leaf_count`;
occurrences by token 385/336/281/300/0/133 = `original_occurrences_by_token`; task carriers per
token 204/128/192/182/0/128 (sum 834) = `tasks_with_token`; changed leaves per token
385/323/275/300/0/133 (sum 1416) = `changed_leaves_by_token`; changed leaves by template
start_url 812, `eval.program_html[].url` 338, `eval.reference_url` 205,
`eval.program_html[].required_contents.must_include[]` 60,
`eval.reference_answer_raw_annotation` 1 (task 66 only; 332 tasks carry the field, 480 do not);
changed tasks 812; `tokens_followed_by_slash` 697; `index_equals_task_id` 812 with 0 violations and
0 duplicate ids; per-profile `tasks` list length 812, 3 profiles, 2436 projections; profile
`values` equal the pinned `profiles.json` maps.

## Observations that qualify the unit but do not falsify it

1. **`projected_task` is stored key-sorted, so it cannot reproduce its own digest.** For index 66,
   `json.dumps(record.projected_task, indent=2)` hashes to `58633d98f639390826c27b6e9eac05e3e14124b523ce77086e73a931d2c90b6c`,
   not the record's `59c3f4be…`; the generator's file preserves raw key order (`sites` first) and
   matches the record digest. The `--json` emitter is evidently key-sorted (stored profile `values`
   order is `GITLAB, MAP, REDDIT, …`, while `profiles.json` order is `GITLAB, REDDIT, SHOPPING,
   SHOPPING_ADMIN, WIKIPEDIA, MAP`). [INFERENCE] Byte faithfulness rests on
   `would_be_file_sha256` alone; re-serializing `projected_task` would yield a false mismatch.
2. **`json_pointer` is document-scoped, not task-scoped.** `/66/start_url` resolves against the
   812-element projected array, not against `projected_task`, whose root has no `"66"` key. A
   consumer resolving the pointer against the per-task object will fail. Report-only convention
   note; the same convention is used by provenance rows.
3. **Index-vs-task_id is degenerate here.** 0 of 812 tasks has `task_id != index` and there are 0
   duplicate ids, so this unit cannot discriminate positional naming from `item["task_id"]`
   naming; the draft already discloses this ("Positional output naming is invisible on the frozen
   order.").
4. **Mixed origins survive faithfully.** Task 66's two `must_include` answers keep
   `http://www.reddit.com/...` while `start_url` and the annotation use the profile origin. Across
   the whole raw file only 7 string leaves begin `http(s)://` (task 66 `must_include[0]`,
   `must_include[1]`; task 256 `exact_match` and annotation `web.cmoa.org`; task 412 `must_include[1]`
   `www.apache.org`; task 448/449 `instantiation_dict.url`), and the instrument correctly reports
   none of them as changed. The draft's operational rule says to
   "check every non-URL changed leaf (`must_include`, annotations) is intended", but does not
   mention these *unchanged* concrete-origin answer leaves; [INFERENCE] a reader could mistake the
   synthetic profiles for an all-synthetic reference-answer space. This is a source property the
   projection reproduces, not a projection error.
5. **Profile order is inert on these bytes.** No profile value contains any of the six tokens, so
   reversing the replacement order changes nothing on real data; task 66's outcome is not evidence
   for or against the ordered-replacement rule (the hand cascade case carries that duty).

## Unresolved gaps / scope

- I did not read the instrument source, so the internal rule that assigns `url_field` vs
  `non_url_field` and the exact definition of "multiple occurrences" are unaudited beyond the
  output-consistency checks above; both definitions are consistent with every output I tested,
  including the `must_include` example that shows the label is field-role based.
- Task 66 exercises no quote/backslash, escaped-token, multi-token or cascade leaf, no `sites`
  consumption question beyond the unchanged `["reddit"]`, and no `program_html` context.
- Scope: one `task_id` × 3 synthetic profiles of an offline projection. No deployment, runtime,
  scorer, task-validity or model claim is tested.

Mismatches found: none. All 3 profiles agree on `projected_task`, both changed leaves
(pointer/category/original/projected/tokens), `output_filename`, `output_index`,
`index_equals_task_id`, `would_be_file_sha256`, and all 3 provenance offsets; the executed
generator reproduces the digest byte for byte.

VERDICT: PASS

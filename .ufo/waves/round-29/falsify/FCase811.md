writer: KengakuR29-2.FCase811-2

# FCase811 — raw task_id 811, all three frozen profiles

Scope: one task end-to-end. Independent re-derivation of the projected object and changed leaves for
raw `task_id` 811 under `distinct_origins`, `path_prefix`, `trailing_slash_sensitivity`, compared
field-by-field with the instrument record at `output_index` 811 in
`python3 plans/config_projection.py --json`.

Independence: I did **not** open, read, copy or import `plans/config_projection.py`. I only executed
it read-only (`--summary`, `--json`) and consumed its stdout. Derivation used: the round-29 prereg
text, the pinned generator bytes
(`plans/fixtures/r29/generate_test_data.py`, sha256 `45ddba7b…21cd`), the pinned manifest, the pinned
`profiles.json`, and the pinned raw bytes. My scripts live only in
`.ufo/waves/round-29/scratch/falsify/FCase811/` (`oracle811.py`, `edges811.py`, `oracle811.out`).
No production, fixture, corpus, SOURCES, SCORECARD or candidate file was written or edited. No tool
install or upgrade; python3 3.14.8 stdlib only.

## 1. What the generator bytes require (observed)

`plans/fixtures/r29/generate_test_data.py`:
- lines 11–16, six sequential text replacements on the whole serialized file:
  `raw = raw.replace("__GITLAB__", GITLAB)` … `raw = raw.replace("__MAP__", MAP)`; order GITLAB,
  REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP (lines 11,12,13,14,15,16).
- line 20 `data = json.loads(raw)` — parse the **projected text**, not per-leaf rewrite.
- lines 21–23 `for idx, item in enumerate(data):` then
  `with open(f"config_files/{idx}.json", "w") as f:` / `json.dump(item, f, indent=2)` — filename and
  ordinal come from enumerate position; per-task bytes are `json.dump(... indent=2)` with defaults
  (`ensure_ascii=True`, no sort, no trailing newline).

Pinned input facts I re-measured: raw file 880776 bytes = 880776 codepoints, ASCII, 0 CR, 29605
lines, sha256 `7b50386f…7652` (equals instrument `raw_text_sha256` and manifest pin); manifest
sha256 `f6390b92…7f87` equals instrument `manifest_sha256`. Parsed list length 812; `task_id`
sequence is exactly 0…811 (so the last item is index 811). Raw token census
`__GITLAB__`385, `__REDDIT__`336, `__SHOPPING__`281, `__SHOPPING_ADMIN__`300, `__WIKIPEDIA__`0,
`__MAP__`133; total 1435. No token appears inside a JSON key (regex scan of `"…TOKEN…":` found none),
so replacement cannot rename keys.

Raw task 811 occupies lines 29571–29604, item starts at codepoint 879808. It contains exactly two
token occurrences, both `__GITLAB__`: `start_url` (line 29574) and
`eval.program_html[0].url` (line 29592). Token census inside the raw item is `{'__GITLAB__': 2}` and
zero for all other tokens; the item has 0 backslash escapes, no `"` inside values, no `__last_url__`
or `__page__` markers. Raw item `eval.reference_url` is `""` and `reference_answers` is `null`.

## 2. Independent derivation (my oracle)

Per profile: decode pinned bytes → six `str.replace` in generator order → `json.loads` → take element
811 → structural walk of raw item vs projected item, collecting every changed string leaf with
pointer, path template, token occurrences, original, projected. File name from the generator
template; `index_equals_task_id` from `item["task_id"] == 811`; `would_be_file_sha256` from
`json.dumps(item, indent=2)` (upstream `json.dump` defaults) encoded UTF-8.

Cross-check that the projection text is exactly the six-replace pipeline: my projected-text sha256
equals the instrument's for all three profiles — `2aec098e5705c98c7f7977a4eb8962aa455c2224d078dbfe4c1fc113e7c707f4`
(distinct_origins), `54cf98337dc6751d9453ee069ff26bb3836698518527cf8683c85bf66744744b` (path_prefix),
`49bbee2e827791b79f42858ac78637704adaa7e36f1cb3a9268563e8df3e01b2` (trailing_slash_sensitivity).

## 3. Derived record for output_index 811 (my values; all three profiles)

| field | distinct_origins | path_prefix | trailing_slash_sensitivity |
|---|---|---|---|
| output_index | 811 | 811 | 811 |
| task_id | 811 | 811 | 811 |
| output_filename | `config_files/811.json` | `config_files/811.json` | `config_files/811.json` |
| index_equals_task_id | true | true | true |
| changed leaves | 2 | 2 | 2 |
| start_url projected | `http://gitlab.invalid:10101` | `http://gitlab.invalid:10201/prefix` | `http://gitlab.invalid:10301/` |
| program_html[0].url projected | `http://gitlab.invalid:10101/dashboard/issues?scope=all&state=opened&assignee_username=byteblaze` | `http://gitlab.invalid:10201/prefix/dashboard/issues?scope=all&state=opened&assignee_username=byteblaze` | `http://gitlab.invalid:10301//dashboard/issues?scope=all&state=opened&assignee_username=byteblaze` |
| would_be_file_sha256 | `18523f7571d37e19d04195967faaa61d5e464262fa6003a926ad046871068cb0` | `aa9f1251c5f0d5e929a20b42fce1156818196ef113f0053fac94be99ba233942` | `9a5314366f406ee278b95d9428f5b08df5542d521972a4f696b1d5e927803203` |
| would-be file bytes (indent=2) | 970 | 984 | 972 |

Changed-leaf rows (identical in all three profiles except `projected`; original text is the same):
- `/811/start_url`, template `start_url`, category `url_field`, tokens `["__GITLAB__"]`,
  original `__GITLAB__`, one occurrence.
- `/811/eval/program_html/0/url`, template `eval.program_html[].url`, category `url_field`,
  tokens `["__GITLAB__"]`, original
  `__GITLAB__/dashboard/issues?scope=all&state=opened&assignee_username=byteblaze`, one occurrence.

Trailing-slash profile's `…:10301//dashboard…` double slash is the faithful consequence of
`"__GITLAB__/dashboard…"` → value ending in `/` + raw `/`; my text pipeline reproduces it exactly,
so the record shows no URL normalization/slash repair for this item. path_prefix shows plain
concatenation with no path de-duplication.

Unchanged in the projected item: `sites`, `task_id`, `require_login`, `storage_state`,
`geolocation`, `intent_template`, `instantiation_dict` (including integer `issue: 404`), `intent`,
`require_reset`, `eval.eval_types`, `eval.reference_answers` (null), `eval.reference_url` (`""`),
`program_html[0].locator`, `must_include[0]`, `intent_template_id` 999. My structural walk asserts
key order and list lengths match and compares the full object; the projected object equals the
instrument's `projected_task` exactly (deep equality true for all three profiles).

## 4. Field-by-field comparison against the instrument record

`python3 plans/config_projection.py --json > /tmp/r29_fcase811_json.json` (exit 0; stdout sha256
`c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`; a second run produced the same
sha256 and exit 0). `--summary` exit 0, `TOTAL findings=0 exit=0`.

Compared at `profiles.<profile>.tasks[811]`, per profile, against my derivation: `projected_text_sha256`,
`parsed_task_count` (812), `output_index` (811), `task_id` (811), `index_equals_task_id` (true),
`output_filename`, full `projected_task` deep equality, `would_be_file_sha256`, leaf count, and every
leaf field (`json_pointer`, `path_template`, `category`, `original`, `projected`, `tokens`).
Result: **0 mismatches** (`oracle811.out`: `=== MISMATCHES: 0 ===`, exit 0). Every value in the
instrument record for output_index 811 is reproduced exactly from the pinned bytes.

Adjacent integrity checks that bear on "is tasks[811] really task 811": in each profile the
instrument's task array has 812 entries, `output_index` equals its array position for all 812
(0…811), `task_id` equals 0…811 in order, no duplicate `output_index`, and `tasks[811]` carries
`output_index` 811 / `task_id` 811. The two `occurrence_provenance` rows for `task_index` 811
(offsets 879919 and 880440, both `__GITLAB__`) are real token starts at lines 29574 and 29592 and are
ordered; globally the claimed 1435 (offset, token) pairs equal the multiset of 1435 regex token
positions in the raw text, with 0 duplicate offsets.

## 5. Non-URL field changes at task 811: none observed

Task 811's only two changed leaves are `start_url` and `eval.program_html[0].url`, both URL fields,
and both are reported `url_field`. No non-URL leaf changes for this item in any profile. This is an
observed absence, not an unexamined area: the same walk enumerates 61 non-URL leaf changes elsewhere
in the frozen input (60 under `eval.program_html[].required_contents.must_include[]`, 1 under
`eval.reference_answer_raw_annotation`, e.g. `/66/eval/reference_answer_raw_annotation` and
`/552/.../must_include/0`), all reported `non_url_field`.

Note on the category rule (observed, not a mismatch for this item): the instrument classifies by
field role, not by value shape. All 61 `non_url_field` leaves begin with a token and are URL-shaped
text (e.g. `__REDDIT__/f/space/134164/…`), while the URL field roles `start_url`,
`eval.program_html[].url`, `eval.reference_url` account for all 1355 `url_field` leaves. A
value-shape oracle I first tried classified all 1416 as `url_field` and therefore disagreed on those
61. At task 811 the two rules agree, so no leaf of this task is sensitive to the distinction. The
instrument's rule is consistent with the record's own `*_field` naming and with the prereg wording
"changed string leaves by JSON path and category" (prereg line 65).

## 6. Multi-occurrence leaves at task 811: none observed

Each of task 811's two changed leaves contains exactly one token occurrence. My independent census
of the frozen input finds 13 multi-occurrence changed leaves, none at task 811: task 66
`/eval/reference_answer_raw_annotation` (`__REDDIT__`×2), tasks 431–435 `/start_url`
(`__SHOPPING__`×3,×2,×2,×2,×2), tasks 604, 608, 609, 625, 681, 682, 683 `/eval/reference_url`
(`__REDDIT__`×3,×2,×3,×2,×3,×4,×2). That matches the instrument's
`changed_leaves_with_multiple_occurrences` = 13 and its per-token leaf counts (sum 1416 = 385+323+275+300+0+133;
`__REDDIT__` 323 leaves vs 336 occurrences, the 13 extra occurrences sitting inside 8 REDDIT leaves;
no leaf contains two different tokens). At tasks 66/431/682 the instrument's `tokens` list holds each
distinct token once while `original` shows 2/3/4 occurrences — the per-occurrence evidence lives in
`occurrence_provenance` (globally 1435 rows, verified equal to actual token positions), so
occurrence, leaf and task units stay separate in the way prereg lines 65–66 require.

## 7. Boundary probes specific to task 811 (observed)

- Index 811 is the **last** of 812 tasks, at file end (item 879808…, file 880776); an off-by-one in
  enumerate, in the filename template, or in trailing-newline handling would surface here. The record
  reports ordinal/filename 811 / `config_files/811.json`, and the digest matches a serialization with
  no trailing newline (970/984/972 bytes), so no such off-by-one is present.
- `would_be_file_sha256` is the per-task file, not the whole projected `test.json`: the matched
  digests are for the ~1 KB item; digests of the raw item (compact, sorted, indent=2) and of the
  filename string do not match the instrument value (checked, all false), while
  `json.dumps(projected_item, indent=2)` matches in all three profiles.
- `index_equals_task_id` is trivially true here (raw order is 0…811), so this item cannot exercise
  the shuffled-ID witness; it can only confirm the frozen-file equality. Not a gap for my item.
- Task 811 contains no quote/backslash/escape text, so this item cannot distinguish serialized-text
  replacement from a decoded-leaf rewrite — both coincide here.

## 8. Remaining unknowns / limits of this attack

- Not tested by this item: shuffled-ID index behavior, quote/backslash JSON-decode failure paths,
  multi-occurrence leaf payload shape for task 811 (none exists), non-URL change at 811 (none exists).
- Category classification semantics were inferred from observed assignments over the frozen input
  (all 61 non-URL rows are content-predicate fields); I did not inspect the implementation, so the
  exact rule is [INFERENCE] from the data, though its effect at task 811 is nil either way.
- The raw file is ASCII, so codepoint offsets and byte offsets coincide; the "codepoint, not byte"
  claim cannot be discriminated on this input, only its values verified.

## 9. Commands (all read-only; outputs quoted above)

```
sha256sum plans/fixtures/r29/manifest.json plans/fixtures/r29/generate_test_data.py \
  plans/fixtures/r29/profiles.json plans/fixtures/r28/webarena/config_files/test.raw.json
python3 plans/config_projection.py --summary        # exit 0, TOTAL findings=0 exit=0
python3 plans/config_projection.py --json > /tmp/r29_fcase811_json.json   # exit 0
python3 .ufo/waves/round-29/scratch/falsify/FCase811/oracle811.py         # exit 0, MISMATCHES: 0
python3 .ufo/waves/round-29/scratch/falsify/FCase811/edges811.py
```

Observed fact summary: for raw `task_id` 811, the instrument's record at `output_index` 811 in all
three profiles agrees exactly with an independent derivation from pinned bytes — projected object,
both changed-leaf pointers with categories/tokens/original/projected, `output_filename`
`config_files/811.json`, `index_equals_task_id` true, and `would_be_file_sha256`
`18523f75…8cb0` / `aa9f1251…3942` / `9a531436…3203`. Zero mismatches; no non-URL change and no
multi-occurrence leaf at this task; no finding against the instrument.

VERDICT: PASS

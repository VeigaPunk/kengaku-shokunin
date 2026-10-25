writer: KengakuR29-2.FCase700-2

# FCase700 — end-to-end attack on raw task_id 700 (3 profiles)

Scope: one raw task (`data[700]`, task_id 700) derived by hand/own script from the pinned generator
bytes, the pinned raw file and `profiles.json`, then compared field-by-field with the record at
`output_index` 700 of every profile of the integrated instrument. Independent re-derivation and
oracle work. I did **not** read or import `plans/config_projection.py` source; I only executed it
(`--json`, `--summary`, `--selftest`, `--help`, and one `--root` probe) and read its stdout. I did
read the knowledge draft `.ufo/waves/round-29/drafts/webarena-config-projection.md`, the hand
fixtures and two build receipts (`build-json-sha256.txt`, `build-selftest.txt`) — none is the
instrument source.

## Attack surface named

Axes attacked at index 700: (A1) exact projected object, (A2) changed-leaf set/pointers/categories/
tokens/original/projected, (A3) `output_filename`, (A4) `index_equals_task_id`, (A5)
`would_be_file_sha256`, (A6) non-URL field changes, (A7) multi-occurrence leaves, plus the
corpus-wide aggregate claims that a single-index record must agree with. Method: a hand reading of
the 27-line generator (star import line 5; ordered replacements lines 11–16; parse line 20;
enumerate/dump lines 21–23) plus two independent oracles — (O1) my own re-implementation of the six
ordered literal replacements over the raw text, and (O2) executing the pinned generator itself in a
`/tmp` copy with a stub `browser_env.env_config` carrying the profile values.

## Pinned inputs actually used (digests recomputed)

- `plans/fixtures/r28/webarena/config_files/test.raw.json` — 880776 bytes,
  sha256 `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` (matches manifest).
- `plans/fixtures/r29/generate_test_data.py` — sha256
  `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` (matches manifest).
- `plans/fixtures/r29/profiles.json` — sha256
  `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` (matches manifest).
- `plans/fixtures/r29/manifest.json` — 1061 bytes, sha256
  `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87`, equal to the instrument's
  own `manifest_sha256` field.

## Raw task 700, as observed in the bytes

`data[700]` (segment is 2227 chars, from `"task_id": 700,` to `"task_id": 701,`): `sites`
`["shopping_admin"]`, `task_id` 700, `require_login` true, `storage_state`
`./.auth/shopping_admin_state.json`, `start_url` `"__SHOPPING_ADMIN__"`, `geolocation` null,
`intent_template` "Draft a new marketing price rule for {{topic}} that offers {{rule}} for all
customers", `instantiation_dict` {topic, rule}, `intent` present with no token, `require_reset`
false, `eval` with `eval_types` [url_match, program_html], `reference_answers` null,
`reference_url` `"__SHOPPING_ADMIN__/sales_rule/promo_quote"`, five `program_html` entries whose
`url` values are all `"last"`, `url_note` "GOLD in PRED", `intent_template_id` 258.

Token inventory of the segment: exactly two `__…__` matches, both `__SHOPPING_ADMIN__`
(`re.findall(r"__[A-Za-z_]+__", seg)`). Both sit in string values, one per leaf; no `__last_url__`
or `__page__` marker occurs at 700. Occurrence codepoint offsets in the original text:
721933 (`/700/start_url`, preceding text `ng_admin_state.json",\n    "start_url": "`) and 722496
(`/700/eval/reference_url`, preceding `answers": null,\n      "reference_url": "`). Both match
`raw_text[off:off+18] == "__SHOPPING_ADMIN__"`.

## Independent derivation (O1) and generator execution (O2)

O1: my script substitutes the six tokens in manifest order GITLAB, REDDIT, SHOPPING,
SHOPPING_ADMIN, WIKIPEDIA, MAP over the raw text, parses, and diffs every leaf pointer against the
raw parse. O2: I copied the pinned generator and raw file to `/tmp/fc700gen`, wrote
`/tmp/fc700gen/browser_env/env_config.py` with the six profile values and an empty `browser_env`
package, and ran `python3 scripts/generate_test_data.py` with `PYTHONPATH=/tmp/fc700gen`, once per
profile (exit 0, empty stderr).

Derived projection of task 700 (identical under O1 and O2; emitted object deep-equals the record's
`projected_task`, and the emitted file ends `...intent_template_id": 258\n}` with no trailing
newline):

| profile | `start_url` | `eval.reference_url` |
|---|---|---|
| distinct_origins | `http://shopping-admin.invalid:10104` | `http://shopping-admin.invalid:10104/sales_rule/promo_quote` |
| path_prefix | `http://shopping-admin.invalid:10204/prefix` | `http://shopping-admin.invalid:10204/prefix/sales_rule/promo_quote` |
| trailing_slash_sensitivity | `http://shopping-admin.invalid:10304/` | `http://shopping-admin.invalid:10304//sales_rule/promo_quote` |

Exactly two leaves change per profile; every other leaf of the object (including `intent`, the five
`program_html[].url` `"last"` values, all `locator` strings and `must_include` "fall discount") is
byte-identical to the raw object.

## Field-by-field comparison with the `output_index` 700 record

| field | instrument value | independent value | agree |
|---|---|---|---|
| `output_index` | 700 in all 3 profiles | ordinal 700 | yes |
| `task_id` | 700 in all 3 | `data[700].task_id` 700 | yes |
| `projected_task` | full object | O1 and O2 object, deep-equal (0 diffs, all three) | yes |
| `changed_leaves` | 2 entries/profile, pointers `/700/start_url`, `/700/eval/reference_url` | 2 entries, same pointers | yes |
| `changed_leaves[].category` | `url_field`, `url_field` | both leaves are URL fields | yes |
| `changed_leaves[].path_template` | `start_url`, `eval.reference_url` | same | yes |
| `changed_leaves[].tokens` | `["__SHOPPING_ADMIN__"]` each | same single token, one occurrence each | yes |
| `changed_leaves[].original` | `"__SHOPPING_ADMIN__"`; `"__SHOPPING_ADMIN__/sales_rule/promo_quote"` | same | yes |
| `changed_leaves[].projected` | table above | same | yes |
| `output_filename` | `config_files/700.json` | enumerate position 700 per generator line `config_files/{idx}.json` | yes |
| `index_equals_task_id` | true | `data[700].task_id` == 700 | yes |
| `would_be_file_sha256` | `0fa307f1…abfa5` / `4e314596…32267` / `1d4e0749…683a634` | emitted `config_files/700.json` (2163 / 2177 / 2165 bytes) sha256 identical | yes |

Full digests: distinct_origins `0fa307f119db72c31eca04b28d95ac06596a80fed4cdef8b1b69dc7e6a7abfa5`;
path_prefix `4e314596179cdae1ab3b27e4957f1018d9de47f5db5ecc069ae198f891732267`;
trailing_slash_sensitivity `1d4e0749d9571f21e6b5624881b0c8a7ccd2628986e04101954cff95d683a634`.
The profile `projected_text_sha256` values also equal the `config_files/test.json` sha256 emitted by
the generator (`2aec098e…c707f4`, `54cf9833…744744b`, `49bbee2e…f3e01b2`).

## Non-URL field change at 700: none

`changed_leaves` at index 700 contains only `category: url_field` entries in all three profiles.
The corpus-wide 61 non-URL changed leaves lie at other indices — 66, 552, 553, 554, 555, 562, 563,
564, 565, 566, 681–688 (60 `must_include` leaves plus one `reference_answer_raw_annotation`); none
is at 700, and my independent diff reproduces that split (`url_field` 1355, `non_url_field` 61).

## Multi-occurrence leaf at 700: none

Both leaves at 700 hold exactly one token occurrence. The corpus-wide 13 multiple-occurrence leaves
are `/66/eval/reference_answer_raw_annotation`, `/431/start_url` (3 SHOPPING), `/432`–`/435/start_url`
(2 each), `/604` (3), `/608` (2), `/609` (3), `/625` (2), `/681` (3), `/682` (4), `/683` (2)
(eval/reference_url unless stated). None is `/700/…`. The occurrence-vs-leaf arithmetic closes:
REDDIT 336 occurrences vs 323 changed leaves (+13 from eight multi-leaves holding 21 occurrences)
and SHOPPING 281 vs 275 (+6 from five multi-leaves holding 11).

## Corpus-wide agreement (supporting oracle, not extra scope)

O1 reproduces, for all 812 indices × 3 profiles: every `would_be_file_sha256` (2436/2436), every
`changed_leaves` pointer set and original/projected pair, `changed_leaf_count` 1416,
`changed_task_count` 812, `string_leaf_count` 10869, `changed_leaves_by_category`,
`..._by_path_template`, `..._by_token`, `changed_leaves_with_multiple_occurrences` 13,
`projected_text_sha256`, `tokens_followed_by_slash` 697 (225/232/110/125/0/5 per token),
`__last_url__` 65, `__page__` 12, and the per-token `tasks_with_token` 204/128/192/182/0/128.
`--json` is deterministic (two runs, sha256 `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`,
3881050 bytes, equal to receipt `corpus/evidence/round29-calibration/build-json-sha256.txt`);
`--summary` exit 0 with `TOTAL findings=0`; `--selftest` exit 0 with `cases=20`.

## Mismatches

None. No field of the index-700 record in any profile disagrees with the independent derivation, and
no changed leaf is missing, extra, mis-categorised or mis-valued.

## [INFERENCE]-free caveats (observed, not mismatches)

- C1 — display ordering. `projected_task` in `--json` is key-sorted (`eval, geolocation, …`) while
  the generator preserves parse order (`sites, task_id, …`); nested objects likewise
  (`instantiation_dict` shown as rule, topic). Consequence: `sha256(json.dumps(record["projected_task"],
  indent=2))` is `5d82dca60430cc567b5f7c4d8fe9c45cb7698d99707ec5cfa6cf2a719faceac3` /
  `4e14d1bd8ee4cf5dfc1481a79ff0ff9e335b9ed27ed4c02225373ac2f80ca204` /
  `d5e466afbc3ae41ff8e604d4a0d174b91ebb041607a1e3c514d929e428b8ae64`, none equal to the record's
  `would_be_file_sha256`. The stored hash is the faithful one (O2 reproduces it), so this is an
  output-presentation gap for consumers who recompute from `projected_task`, not a wrong value.
- C2 — pointer root. `changed_leaves[].json_pointer` is absolute to the parsed array (`/700/start_url`);
  it resolves in the projected full-array parse to the recorded `projected` value but does not
  resolve inside the standalone `projected_task` object.
- C3 — mapping non-discriminating at 700. All 812 raw items satisfy `task_id == ordinal`, so
  `index_equals_task_id: true` at 700 is forced by the population, not evidence about the enumerate
  rule. A black-box probe with a re-pinned shuffled copy was refused: `--root /tmp/fc700root --json`
  (raw copy with ids 5/700 swapped and its manifest digest updated) returned
  `findings [{"id": "manifest_tampered"}]`, exit 2, no profile records. The enumerate rule is
  exercised only by the instrument's hand fixture `index-shuffled-ids.fixture.json` and selftest
  case `hand_index_r29_index_shuffled_ids_1_0`.
- C4 — offset units untested at 700. The raw file is ASCII (0 bytes >127, 0 CR); its 49 `\u` escapes
  all decode to non-ASCII and sit in 47 leaves elsewhere, so codepoint and byte offsets coincide
  throughout; 721933 and 722496 are consistent with both readings. Task 700 has no non-ASCII leaf.
- Note: the instrument's own limitation line calls the locale-encoding difference inert because the
  raw file is ASCII without carriage returns. I verified both properties on the pinned bytes; at 700
  the text-replacement path therefore has no newline/encoding hazard.

## Commands run (exact, with units)

Working copies live under `/tmp`; production read only.

1. `python3 plans/config_projection.py --json > /tmp/fc700_all.json` → exit 0, 3881050 bytes,
   sha256 `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`; repeat piped to
   `sha256sum` gave the same digest.
2. `python3 plans/config_projection.py --summary` → exit 0, `TOTAL findings=0`; `INDEX
   {"index_equals_task_id": 812, "violations": 0}`.
3. `python3 plans/config_projection.py --selftest` → exit 0, `SELFTEST clean cases=20`.
4. `python3 .ufo/waves/round-29/scratch/falsify/FCase700/derive.py` → per-profile 2 changed leaves
   (`/start_url`, `/eval/reference_url`) and the three would-be-file digests quoted above.
5. `cd /tmp/fc700gen && PYTHONPATH=/tmp/fc700gen python3 scripts/generate_test_data.py` (once per
   profile, after rewriting `browser_env/env_config.py`) → exit 0, empty stderr; `config_files/700.json`
   is 2163 / 2177 / 2165 bytes with the three recorded digests; `config_files/` holds 814 `.json`
   files (812 per-index plus `test.json` and my copied `test.raw.json`).
6. `python3 plans/config_projection.py --root /tmp/fc700root --json` (shuffled, re-pinned copy) →
   exit 2, `findings [{"id": "manifest_tampered"}]`.

## Reproducibility of this attack

Scripts and outputs in `.ufo/waves/round-29/scratch/falsify/FCase700/` (`derive.py`, `oracle.py`,
`compare.py`, `compare2.py`, `derive_out.json`); generator run tree `/tmp/fc700gen`; shuffled probe
tree `/tmp/fc700root`; instrument JSON at `/tmp/fc700_all.json`. No production file, fixture, corpus
row, SCORECARD or candidate was modified; no git write command was run. No tool was installed or
upgraded (python3 stdlib only).

VERDICT: PASS

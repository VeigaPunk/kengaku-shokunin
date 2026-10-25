writer: KengakuR29-2.FCase205-2

# FCase205 — independent projection of raw task_id 205 (three profiles)

Item attacked: the claim-C1 per-task projection record for **raw task_id 205** in every profile of
`plans/config_projection.py --json`, compared field-by-field against a derivation from the pinned
generator bytes, the pinned raw task file and the frozen profiles. Lane master under attack
56fd949a6478342531e61f4feecb4a685d831640; lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

## Independence (declared)

- I did **not** read, grep, import or open `plans/config_projection.py`. Source was used only as an
  opaque CLI (`--json`, `--summary`, `--selftest`). My oracle derives from the round-29 prereg text,
  the 838-byte pinned generator, `profiles.json` and `test.raw.json` — nothing else.
- No tool was installed or upgraded; no pacman transaction was run. No linter/formatter was run.
- Scratch: `.ufo/waves/round-29/scratch/falsify/FCase205-2/`; all generator simulation ran on copies
  under `/tmp/f205/`. No production/fixture/corpus/SOURCES/SCORECARD/candidate file was written; no
  git write command was issued (only `ls`, `find`, `sha256sum`, `grep` reads).

## Pins re-verified (observed)

| file | sha256 | matches manifest |
|---|---|---|
| `plans/fixtures/r29/manifest.json` | `f6390b92…bf87` | self |
| `plans/fixtures/r29/generate_test_data.py` | `45ddba7b…21cd` | yes |
| `plans/fixtures/r28/webarena/config_files/test.raw.json` | `7b50386f…7652` | yes |
| `plans/fixtures/r29/profiles.json` | `90fdc34d…e018` | yes |

Raw file: 880 776 bytes, 880 776 codepoints, pure ASCII, no `\r`, 812 list elements,
`task_id[i] == i` for all 812.

## Upstream contract, re-derived from the 838-byte source

Six global text replacements on the serialized raw text, in this order, then a parse, then an
`enumerate`-position output filename (lines 11–16, 20–23):

- L11 `raw = raw.replace("__GITLAB__", GITLAB)` (quote, 4 words)
- L12–L16 REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP
- L20 `data = json.loads(raw)`; L21 `for idx, item in enumerate(data):` (quote, 5 words)
- L23 `json.dump(item, f, indent=2)` → `config_files/{idx}.json`, no trailing newline,
  `ensure_ascii` default (True), key order = source order.
- Instrument `source_contract` lines 5/20/21/11–16 and its `output_index` = `enumerate position,
  not item task_id` (quote, 5 words) agree with my independent line count.

## My derived 205 record, all three profiles (oracle)

Raw item 205 (`task_id` 205) has 12 string leaves; exactly one contains a token, once:
`/start_url` = `__GITLAB__/a11yproject/a11yproject.com`. All other leaves are token-free:
`/sites/0` `gitlab`, `/storage_state` `./.auth/gitlab_state.json`, `/intent_template`,
`/instantiation_dict/user`, `/instantiation_dict/date`, `/intent`, `/eval/eval_types/0`,
`/eval/reference_answers/must_include/0`, `/eval/reference_url` ``, `/eval/string_note` ``,
`/eval/reference_answer_raw_annotation` `1`.

| profile | projected `/start_url` (mine) | changed leaves | category | tokens | out file |
|---|---|---|---|---|---|
| distinct_origins | `http://gitlab.invalid:10101/a11yproject/a11yproject.com` | 1 | url_field | `__GITLAB__` | `config_files/205.json` |
| path_prefix | `http://gitlab.invalid:10201/prefix/a11yproject/a11yproject.com` | 1 | url_field | `__GITLAB__` | `config_files/205.json` |
| trailing_slash_sensitivity | `http://gitlab.invalid:10301//a11yproject/a11yproject.com` | 1 | url_field | `__GITLAB__` | `config_files/205.json` |

`would_be_file_sha256` (mine, from a real `json.dump(item, f, indent=2)` file write, 743 bytes):
`24a4e07069402714b344834579a5bb704d528ae4727f44b2710bbad248b4d7dd` (distinct_origins),
`fe364d14fc64964b97d2191ff14195df6b9cf0775c2e0459170d5eaf716b0e05` (path_prefix),
`453a87ccce0bef26e6be2166dde17647dac2a1e930b7d957ed79e87cbcaef2e7` (trailing slash).
`index_equals_task_id` true (position 205, `task_id` 205). The trailing-slash double slash is the
raw `__GITLAB__/` junction, not normalization; instrument stimulus text: `synthetic trailing '/' on
all six values; a token followed by '/' becomes '//' by design` (quote, 16 words).

## Field-by-field comparison at `output_index` 205

Command: `python3 plans/config_projection.py --json` → exit 0, 3 881 050 bytes stdout,
sha256 `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`; a second run produced
the identical digest and an identical parsed tree. `findings: []`.

| field compared (205) | instrument | mine | result |
|---|---|---|---|
| `task_id` | 205 | 205 | match |
| `output_index` | 205 | 205 | match |
| `output_filename` | `config_files/205.json` | `config_files/205.json` | match |
| `index_equals_task_id` | `true` | `true` | match |
| `projected_task` | full object | deep-equal to my parse of the projected text | match, all 3 |
| `changed_leaves` (n) | 1 | 1 | match, all 3 |
| `.json_pointer` | `/205/start_url` | same leaf; instrument prefixes list index | match |
| `.category` | `url_field` | url-valued field | match |
| `.path_template` | `start_url` | `start_url` | match |
| `.original` | `__GITLAB__/a11yproject/a11yproject.com` | identical | match |
| `.projected` | three values in table above | identical | match, all 3 |
| `.tokens` | `["__GITLAB__"]` | identical | match |
| `would_be_file_sha256` | three digests above | identical | match, all 3 |

**No mismatch found at output_index 205 in any profile.** Beyond 205 I also re-derived all 812×3
records to be sure 205 is not special-cased: `output_index`, `output_filename`, `task_id`,
`index_equals_task_id`, `projected_task`, `changed_leaves` (pointer/original/projected/tokens) and
`would_be_file_sha256` matched on all 2 436 records, 0 mismatches.

## Non-URL field change at 205

**None.** Item 205 changes only `/start_url`, a URL-valued field. Dataset-wide the non-URL category
is not empty (instrument 61, mine 61): 60 `eval.program_html[].required_contents.must_include[]`
leaves and 1 `eval.reference_answer_raw_annotation` (index 66). Classification is by field name
(`url`, `start_url`, `reference_url` → url_field), so 338 `eval.program_html[].url` leaves are
url_field and the 60 URL-containing `must_include` strings are non_url_field — consistent labelling,
and irrelevant to 205's single unambiguous leaf.

## Multi-occurrence leaf at 205

**None** — one occurrence of one token. Dataset-wide instrument `changed_leaves_with_multiple_occurrences`
= 13 in every profile, and my independent census also yields 13: indices 66 (`…/eval/reference_answer_raw_annotation`,
2×REDDIT), 431 (3×SHOPPING), 432/433/434/435 (2×SHOPPING), 604 (3×), 608 (2×), 609 (3×), 625 (2×),
681 (3×), 682 (4×), 683 (2×) — all REDDIT `|OR|`/`|AND|` compound URL strings in `eval/reference_url`
and `start_url`. Units kept separate: 1 435 raw occurrences → 1 416 changed leaves
(GITLAB 385/385, REDDIT 336/323, SHOPPING 281/275, SHOPPING_ADMIN 300/300, WIKIPEDIA 0/0, MAP 133/133);
`changed_leaves_by_token`, `changed_tasks_by_token` and `applied_replacements` reproduce exactly.

## Occurrence provenance at 205

One entry: `{json_pointer: "/205/start_url", path_template: "start_url", string_role: "value",
task_index: 205, token: "__GITLAB__", original_input_codepoint_offset: 189243}`.
`raw[189243:189243+10] == "__GITLAB__"` and `raw[189253] == "/"` — the source of the trailing-slash
`//`. All 1 435 provenance entries slice-verify, and their sorted offsets equal an independent regex
scan of the raw text (1 435 occurrences). Caveat: the file is pure ASCII, so codepoint offsets and
byte offsets coincide here; the instrument limitation `offsets are Unicode codepoint offsets in the
ORIGINAL raw input text, never byte offsets or step-input offsets` (quote, 17 words) is therefore not
falsifiable from this input. [INFERENCE] a non-ASCII fixture would be required to discriminate it;
selftest lists a `codepoint_offsets_and_key_token` case.

## End-to-end reproduction (strongest check)

I re-ran the generator faithfully on `/tmp` copies (text-mode read, universal newlines, the six
replacements in order, `json.dump(item, f, indent=2)`), per profile:

- 3/3 whole-file `test.json` sha256 matched the instrument's `projected_text_sha256`
  (`2aec098e…`, `54cf9833…`, `49bbee2e…`);
- **2 436/2 436** `would_be_file_sha256` matched, including 205 (743-byte file);
- `sort_keys=True` does **not** reproduce them (key order preserved); `ensure_ascii=False` does not
  reproduce task 0's digest (`9533088e…`, non-ASCII leaf `'Quest Lumaflex™ Band'`), confirming the
  upstream default. Item 205 is all-ASCII, so at 205 alone both ascii modes coincide — at 205 that
  dimension is undiscriminated, though the dataset-wide check discriminates it.

## Loops closed, and residual limits

- 1 435 text occurrences = 1 435 decoded-leaf occurrences ⇒ no `\u`-escaped tokens; no duplicate JSON
  keys; zero keys contain `__` (all occurrences have role `value`) ⇒ for these six ASCII values,
  text-level substitution and decoded-leaf substitution are provably equivalent on this input. The
  file does contain escapes (49 `\u`, 1 274 `\"`, 12 `\n`), but **none of the 1 416 changed leaves
  contains a quote, backslash or control character**, so the escape-boundary divergence the prereg
  flags is inert here (and inert for 205).
- 697/1 435 occurrences are followed by `/`; the trailing profile reports
  `value_slash_then_raw_slash_junctions: 697`, and 205 contributes exactly 1. Other profiles 0.
- `string_leaf_count` 10 869 equals my recursive census; `parsed_task_count` 812 per profile;
  `remaining_known_tokens_text`/`_decoded` all 0 (F2 shape); `__last_url__` 65 and `__page__` 12
  occurrences retained as non-env markers (my counts 65/12, on 55 and 9 tasks).
- Index-vs-ID is **not separable at 205**: every raw `task_id` equals its list position, so a record
  keyed by index and one keyed by id are indistinguishable for this task; the record carries both
  fields. Hand fixture `plans/fixtures/r29/hand/index-shuffled-ids.fixture.json` exists and selftest
  lists `hand_index_r29_index_shuffled_ids_1_0`; my item did not exercise it.
- Naming/type observation (not a value error): `index_mapping.index_equals_task_id` is the integer
  count 812 while the per-task field of the same name is a boolean; the denominator is
  `population.input_task_count` 812 and `violations` is `[]`.
- Read-only behaviour: on a `/tmp` copy, `--json` and `--selftest` created no `test.json`, no
  `config_files/` and no `.pyc`; the lane has no `plans/config_files` and no `test.json` file. The
  lane's `plans/__pycache__/config_projection.cpython-314.pyc` (mtime 2026-10-21 13:49:19) is not
  attributable to either CLI mode per that copy test, so it came from a process that imported the
  module. [INFERENCE]
- Not evaluated by this item: selftest semantics, mutation coverage, source-row wording, candidate
  text, and any non-205 projection detail beyond the corroborating global equality run.

## Observed facts vs inference

Observed: pins, item-205 leaves, three projections, three file digests, three whole-file digests,
2 436/2 436 per-task equality, 1 435/1 435 provenance slices, 13 multi-occurrence leaves, 61 non-URL
leaves, determinism of two `--json` runs, exit 0 for `--json`/`--summary`/`--selftest`
(`SELFTEST clean cases=20`, `TOTAL findings=0 exit=0`).
[INFERENCE]: pyc attribution; that a non-ASCII fixture is needed to observe codepoint-vs-byte offsets;
consumer impact of the provenance `task_index`-only key on a shuffled input.

VERDICT: PASS

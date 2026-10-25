writer: KengakuR29-2.FCase000-2

# FCase000 — raw task_id 0 across all three frozen profiles

**Attack.** Claim C1 (`plans/round-29-claims.md`, prereg landed `31934e5`, baseline
`ed26bdf5`) at one unit: independently derive the exact projected object, changed leaves, output
filename, index mapping and would-be file digest for raw `task_id` 0 under all 3 frozen profiles,
then compare field-by-field with the record at `output_index` 0 in
`python3 plans/config_projection.py --json`. Also report any non-URL field change and any
multi-occurrence leaf, at this unit and at corpus scale where that bears on the claim.

Lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; integrated revision
`56fd949a6478342531e61f4feecb4a685d831640`. Read-only leaf: production, fixtures, corpus,
SOURCES, SCORECARD and the candidate were not touched. All write experiments ran under
`/tmp/r29f000`; my scripts and captures live only in
`.ufo/waves/round-29/scratch/falsify/FCase000/`.

**Independence statement (required).** I did **not** read, open or import
`plans/config_projection.py` source at any point; my target is its `--summary`/`--json` **output**.
I read the prereg text in full, the pinned generator bytes, the pinned manifest/profiles/raw data,
and candidate draft lines 55–57 for claim wording. Sibling reports
`falsify/FCase500.md` / `falsify/FCase640.md` were read only after my task-0 derivation had
already matched the instrument; neither contains task-0 values. FCase500's mention of executing
the pinned generator prompted an extra check, which I then built and verified independently for
task 0 (below).

## Observed: pinned inputs

`sha256sum plans/fixtures/r29/manifest.json plans/fixtures/r29/generate_test_data.py plans/fixtures/r29/profiles.json plans/fixtures/r28/webarena/config_files/test.raw.json`

| file | sha256 | vs pin |
|---|---|---|
| `r29/manifest.json` | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` | equals `--json.manifest_sha256` |
| `r29/generate_test_data.py` | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` | equals manifest |
| `r29/profiles.json` | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` | equals manifest |
| `r28/webarena/config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | equals manifest and `--json.raw_text_sha256` |

Generator contract as inert bytes (27 lines): star import line 5; six `raw.replace` calls lines
11–16 in order GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP; whole-text write lines
17–18; `data = json.loads(raw)` line 20; `for idx, item in enumerate(data)` line 21;
`json.dump(item, f, indent=2)` line 23 into `config_files/{idx}.json` (line 22). Quoted literals
with programmatic word counts: `raw = raw.replace("__SHOPPING_ADMIN__", SHOPPING_ADMIN)` (4 words),
`json.dump(item, f, indent=2)` (3), `config_files/{idx}.json` (1). Raw file: 880776 bytes =
880776 codepoints, 0 CR bytes, ASCII-only.

## Observed: raw unit (own `json.JSONDecoder.raw_decode` over the original text)

- List position 0, `task_id` 0, span codepoints `[4,803)`, 799 characters, 12 object keys.
- Exactly **1** token occurrence in the span: `__SHOPPING_ADMIN__` in `start_url` at codepoint
  offset **172** (`raw[172:190]` slices the token; context `"start_url": "__SHOPPING_ADMIN__",`).
  No `__GITLAB__`, `__REDDIT__`, `__SHOPPING__`, `__WIKIPEDIA__`, `__MAP__`, `__last_url__` or
  `__page__` in the span. `reference_url` is `""`; `program_html` is `[]`; `eval` holds the
  escaped non-ASCII `\u2122` (twice) unrelated to any token.
- All 812 ids are exactly `range(812)` (int), distinct, so `output_index` 0 = `task_id` 0.

## Method

1. `scratch/falsify/FCase000/oracle000.py` (own code, no production import): apply the six
   replacements to the serialized raw text in pinned order, parse the projected text, walk both
   parsed objects with my own JSON-pointer leaf walk, hash the projected text, and hash
   `json.dumps(item, indent=2)` for the upstream per-item file.
2. Byte-level oracle: execute the **pinned generator bytes** at
   `/tmp/r29f000/<profile>/generate_test_data.py` with cwd there, `config_files/test.raw.json`
   copied from the pin, and a stub `browser_env/env_config.py` holding only the six synthetic
   `*.invalid` profile values (no real `env_config`, no credentials). Command per profile:
   `cd /tmp/r29f000/<profile> && PYTHONPATH=/tmp/r29f000/<profile> python3 generate_test_data.py`.
3. `scratch/falsify/FCase000/census.py`: re-derive all 3×812 records and compare every field,
   type-strict (`json.dumps(..., sort_keys=True)` equality), plus every leaf and digest.
4. Instrument runs: `--summary` once and `--json` twice, exit 0 each time; `findings` `[]`.

## Observed: field-by-field, index 0 (all three profiles)

| field | distinct_origins | path_prefix | trailing_slash_sensitivity |
|---|---|---|---|
| `start_url` projected value | `http://shopping-admin.invalid:10104` | `http://shopping-admin.invalid:10204/prefix` | `http://shopping-admin.invalid:10304/` |
| `projected_task` vs my parsed object | type-strict equal | type-strict equal | type-strict equal |
| `changed_leaves` count | 1 | 1 | 1 |
| pointer / template / category | `/0/start_url` / `start_url` / `url_field` | same | same |
| `original` | `__SHOPPING_ADMIN__` | `__SHOPPING_ADMIN__` | `__SHOPPING_ADMIN__` |
| `projected` | as above | as above | as above |
| `tokens` | `["__SHOPPING_ADMIN__"]` | same | same |
| `output_index` / `task_id` / `index_equals_task_id` | `0` / `0` / `true` | same | same |
| `output_filename` | `config_files/0.json` | same | same |
| `would_be_file_sha256` (instrument) | `9533088e31781047e4c4f3b9cafe02f734aaaa3fb9c47ebc29176bd8d6a6e5e6` | `763bf0c4401bf3254837b81903d3a271908c16339040a77ee492f349ab028b67` | `a5b767ca8ae59deca86fb5c9366aa77f8fafbb139ab10eca0a6671c4b2db2018` |
| same sha, my `json.dumps(item, indent=2)` | identical | identical | identical |
| same sha, executed pinned generator `config_files/0.json` | identical | identical | identical |
| generated `0.json` byte-identical to my would-be text | yes (758 B) | yes (765 B) | yes (759 B) |
| generated `test.json` sha = `projected_text_sha256` | match | match | match |

Additional byte facts: full projected-text sha256 are
`2aec098e5705c98c7f7977a4eb8962aa455c2224d078dbfe4c1fc113e7c707f4` (distinct_origins),
`54cf98337dc6751d9453ee069ff26bb3836698518527cf8683c85bf66744744b` (path_prefix) and
`49bbee2e827791b79f42858ac78637704adaa7e36f1cb3a9268563e8df3e01b2`
(trailing_slash_sensitivity), each equal to the sha256 of the generated `test.json`.
Generated `0.json` is not newline-terminated and writes the trademark as
`\u2122` (ensure_ascii default), matching `would_be_file_sha256`; generated `test.json` sizes
905171 / 915216 / 906606 bytes equal the projected-text byte lengths. Upstream wrote 812 index
files plus `test.json` per profile (813 artifacts; my directory also held the copied input).
`--json` was reproduced byte-identically on rerun, sha256
`c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`, equal to
`corpus/evidence/round29-calibration/build-json-sha256.txt`.

Occurrence provenance for this unit is exactly one row:
`{"json_pointer": "/0/start_url", "original_input_codepoint_offset": 172,
"path_template": "start_url", "string_role": "value", "task_index": 0,
"token": "__SHOPPING_ADMIN__"}`, reproduced by my independent scan.

## Observed: corpus-scale cross-check (bounds this unit)

- All **2436** records (812 × 3) match my independent re-derivation type-strict: object, all
  `changed_leaves` fields, `output_filename`, `output_index`, `task_id`, `index_equals_task_id`,
  `would_be_file_sha256`. `census.py` printed `PROBLEMS 0`.
- Profile aggregates equal mine on every key: `projected_text_sha256`; changed leaves 1416;
  changed tasks 812; string leaves 10869; categories `url_field` 1355 / `non_url_field` 61;
  path templates (`start_url` 812, `eval.program_html[].url` 338, `eval.reference_url` 205,
  `must_include[]` 60, `reference_answer_raw_annotation` 1); `changed_leaves_by_token`
  (`__GITLAB__` 385, `__REDDIT__` 323, `__SHOPPING__` 275, `__SHOPPING_ADMIN__` 300,
  `__WIKIPEDIA__` 0, `__MAP__` 133); `changed_tasks_by_token`; remaining tokens 0/0; multi-occurrence
  13; applied replacements 385/336/281/300/0/133; `tokens_followed_by_slash` 697.
- Unit distinction holds: occurrence 1435 → leaf 1416 (19 collapsed extra occurrences), so
  `__REDDIT__` 336 occurrences vs 323 attributed leaves and `__SHOPPING__` 281 vs 275; my
  first-token-in-order leaf attribution reproduces both exactly. Counts are not pooled.

## Observed: your two specific questions

- **Non-URL field change at task 0: none.** Its single projected leaf is `start_url`
  (`url_field`). Nothing named or valued as non-URL changes.
- **Multi-occurrence leaf at task 0: none.** One occurrence in one leaf;
  `/0/...` is not in the 13-leaf set.
- Corpus scale (independent, per-profile identical): 61 `non_url_field` leaves =
  `must_include[]` 60 + `reference_answer_raw_annotation` 1. **Every one of the 61 originals and
  projected values is URL-shaped**: 60 are single URL strings (`__REDDIT__/…`, `__GITLAB__/…`);
  the one annotation (task 66) is two comma-joined Reddit URLs and is *also* a multi-occurrence
  leaf (2 occurrences). The 13 multi-occurrence leaves are
  `/66/eval/reference_answer_raw_annotation`, `/431`, `/432`, `/433`, `/434`, `/435` (`start_url`),
  `/604`, `/608`, `/609`, `/625`, `/681`, `/682`, `/683` (`eval/reference_url`) with 2–4
  occurrences each.
- Independent occurrence-context census over all 1435 occurrences (walking parsed string leaves):
  token at string start 1416; after ` |AND| ` 6; after ` |OR| ` 12; after `, ` 1; **0 preceded by
  an alphanumeric character**. The 1435 occurrences enumerated through parsed string leaves equal
  the 1435 raw-text occurrences, so none sits in a key or structural text; leaf walk shows 0
  disappearance/extra anywhere. Every token occurrence is a URL origin (string start or after a
  URL-list separator), never mid-prose.

## Qualifications (no mismatch found, but novelty-bearing)

1. **`non_url_field` is a field-name category, not a value category.** The candidate says
   “Global text replacement reaches non-URL fields.” (6 words) and “61 changed leaves are
   `must_include` answer strings and one raw annotation” (11 words) (draft lines 56–57); prereg F3 says
   “F3 global replacement changes at least one non-URL-valued field, p=.7” (10 words, line 106).
   Observed: all 61 changed values are URL text, and no occurrence sits in non-URL prose.
   [INFERENCE] Under a *value* reading (“a field whose value is not a URL”), F3 is false (0 such
   changes); under the field-name reading it is true but tautological here. A URL-fields-only
   re-implementation would still miss these 61 leaves, so the candidate's operational point
   (hand witness `url-only`) stands; only the “non-URL” label needs that disambiguation, and F3
   should not be scored as evidence that substitution alters non-URL content.
2. **Index 0 is the minimal case and cannot discriminate the hard paths.** Changed-leaf counts
   over 812 tasks: 1 leaf ×374, 2 ×364, 3 ×45, 4 ×11, 5 ×3, 6 ×4, 7 ×5, 8 ×1, 9 ×1, 10 ×1,
   11 ×2, 12 ×1; 18 tasks carry a non-URL-named leaf; 13 carry a multi-occurrence leaf; 790 use
   exactly one token; 0 have index ≠ task_id. Task 0 is a single bare URL token, so it cannot
   distinguish text-vs-decoded replacement (no escapes), replacement order/cascade (no value
   contains a token), quote/backslash repair, multi-occurrence or non-URL behavior, or positional
   vs `task_id` naming. The corpus-scale 2436-record check above is what actually bounds the
   instrument; the unit itself is structurally the easiest case.
3. **`changed_leaves[].json_pointer` is document-rooted, not record-rooted.** For every leaf
   (4248 = 1416 × 3) the pointer's first component equals `output_index`, and for every
   provenance row (1435) it equals `task_index`. But the record also carries `projected_task`,
   which is the per-item object: resolving `json_pointer` `/0/start_url` against
   `projected_task` raises `KeyError: '0'`. The convention is consistent but undocumented in
   `--summary`, `limitations`, interface text or the candidate (grep found no mention).
4. **Display order loses byte order.** `--json` emits `projected_task` key-sorted (`eval` first)
   while upstream writes source order (`sites` first). For index 0, sha256 of the displayed
   object re-serialized with `indent=2` is
   `823a9a7fd4ca2b16ae5d6e0c7966f22584691845bdb675832ad56983085aebcd`, not
   `9533088e…e5e6`; the executed generator's file is source-ordered and does match
   `would_be_file_sha256`. [INFERENCE] Presentation-only; an object-equality comparator (per
   prereg: compare every per-task object) is unaffected, a byte comparator on the displayed
   object would false-mismatch.

## Mismatches

None. Compared families × profiles: `projected_task` (type-strict), `changed_leaves`
(pointer/category/path_template/tokens/original/projected), `output_filename`, `output_index`,
`task_id`, `index_equals_task_id`, `would_be_file_sha256`, profile `projected_text_sha256`,
occurrence provenance — 9 × 3 agreements, zero disagreements. No non-URL change and no
multi-occurrence leaf exists at this unit.

## Unresolved / scope

- I did not read the instrument source, so its internal category rule is unaudited; the output is
  exactly consistent with field-name classification on this population.
- Real `browser_env.env_config` values, deployment configs, runtime scoring, task validity and
  model behavior are outside this item; the executed-generator check used synthetic `*.invalid`
  values only.
- Scope: one `task_id` × 3 synthetic profiles of an offline projection; the verdict is for this
  item, not a round admission.

Tool installs/upgrades: none (python3 3.14 stdlib only; no pacman, no network).

VERDICT: PASS

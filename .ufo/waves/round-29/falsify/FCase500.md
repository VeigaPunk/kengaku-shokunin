writer: KengakuR29-2.FCase500-2

# FCase500 — per-task falsification of raw task_id 500 under all three profiles

Lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Attacks claim C1
(`plans/round-29-claims.md`) at one unit: the exact projected object, changed leaves and would-be
file digest for raw `task_id` 500 in each of the 3 frozen profiles. Read-only leaf: no production,
fixture, corpus, SOURCES, SCORECARD or candidate file was touched. No installs, so no tool row.

**Independence statement (required):** I did **not** read, open or import
`plans/config_projection.py` source at any point. I read only the prereg TEXT
(`plans/round-29-claims.md`), the pinned generator bytes, the pinned raw data, the pinned
profiles/manifest, the build receipts under `corpus/evidence/round29-calibration/`, and the
candidate draft lines quoted below for claim wording. My comparison target is instrument
`--json` / `--summary` / `--selftest` **output only**. All byte-level experiments ran on copies
under `/tmp/r29f500`.

## Observed: pinned inputs (sha256, `sha256sum` under `plans/fixtures/…`)

| file | sha256 | vs manifest |
|---|---|---|
| `r29/generate_test_data.py` | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` | match |
| `r28/webarena/config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | match |
| `r29/profiles.json` | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` | match |
| `r29/manifest.json` | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` | equals `--json.manifest_sha256` |

Generator contract, read as inert bytes (27 lines): line5 `from browser_env.env_config import *`; lines11–16 six
`raw.replace` calls in order GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP; line17–18 writes the
whole `test.json`; line20 `json.loads(raw)`; lines21–23 `enumerate` + `json.dump(item, f, indent=2)` into
`config_files/{idx}.json`. Whole raw file: 880776 bytes, 880776 codepoints, CR count 0, non-ASCII bytes 0.

## Observed: the raw unit (own scanner, `json.JSONDecoder.raw_decode` over the original text)

- Raw list position 500, `task_id` 500, span codepoints `[465271,466310)`, 1039 characters.
- `start_url` = `__SHOPPING_ADMIN__`; `eval.program_html[0].url` =
  `__SHOPPING_ADMIN__/sales/order/commentsHistory/order_id/301/active_tab/order_shipments/`;
  `storage_state` = `./.auth/shopping_admin_state.json`; `sites` = `["shopping_admin"]`;
  `intent_template_id` 284; 12 keys total.
- Exactly 2 token occurrences inside the span, both `__SHOPPING_ADMIN__`, at codepoint offsets
  465441 and 465986 (independently re-found from the span start; identical to
  `occurrence_provenance` entries for `task_index` 500). Zero `__GITLAB__`, `__REDDIT__`,
  `__SHOPPING__`, `__WIKIPEDIA__`, `__MAP__`, `__last_url__`, `__page__` in the span.
- Textual consequence: `__SHOPPING__` (step 3) cannot consume this token. Applying only step 3 to the
  whole file leaves 300 `__SHOPPING_ADMIN__` markers; applying only step 4 leaves 281 `__SHOPPING__`
  markers. Task 500's two occurrences are consumed at step 4 (`applied_replacements.SHOPPING_ADMIN` = 300).

## Observed: my derivation vs instrument, field by field (3 profiles)

Profile value used in each case: `SHOPPING_ADMIN` = `http://shopping-admin.invalid:10104` /
`http://shopping-admin.invalid:10204/prefix` / `http://shopping-admin.invalid:10304/`.

| field | distinct_origins | path_prefix | trailing_slash_sensitivity |
|---|---|---|---|
| `/500/start_url` projected | `http://shopping-admin.invalid:10104` | `http://shopping-admin.invalid:10204/prefix` | `http://shopping-admin.invalid:10304/` |
| `/500/eval/program_html/0/url` projected | `http://shopping-admin.invalid:10104/sales/order/commentsHistory/order_id/301/active_tab/order_shipments/` | `http://shopping-admin.invalid:10204/prefix/sales/order/commentsHistory/order_id/301/active_tab/order_shipments/` | `http://shopping-admin.invalid:10304//sales/order/commentsHistory/order_id/301/active_tab/order_shipments/` |
| my deep-diff leaf count | 2 | 2 | 2 |
| instrument `changed_leaves` count | 2 | 2 | 2 |
| categories | both `url_field` | both `url_field` | both `url_field` |
| path_templates | `start_url`, `eval.program_html[].url` | same | same |
| tokens per leaf | `["__SHOPPING_ADMIN__"]` | same | same |
| `output_filename` | `config_files/500.json` | same | same |
| `output_index` / `index_equals_task_id` | 500 / true | 500 / true | 500 / true |
| `would_be_file_sha256` instrument | `413ed9017600bd9cb2a91024589873f9961b29f256163c2e8b1f5c2c52d125b1` | `46781de74a1a98a7308fe08603b6d383beab165b1710e975246f733fee1f5ccd` | `bf0f64c6620a072dd2e8599b01f60e0baef39663cf0f44d1fa81801d17574f56` |
| same sha, my `json.dump(item, indent=2)` | identical | identical | identical |
| same sha, **executed pinned generator** | identical | identical | identical |
| file bytes | 1001 | 1015 | 1003 |

Every comparison above is equality; `original` values in each record equal the full pre-projection
leaf strings, and `projected` equals the full post-projection leaf. Cross-profile diff of
`projected_task` for `/500/*` is exactly those 2 leaves in both comparisons (distinct vs path, distinct
vs trailing). All 12 keys of `projected_task` equal my independently parsed projected object.

**Oracle beyond the instrument (new for this unit):** the instrument never executes upstream. I ran the
pinned generator bytes themselves in `/tmp/r29f500/run_<profile>/` under a stub
`browser_env/env_config.py` holding each profile's six values, `sys.path` pointed at the stub package,
cwd at the work copy. Result per profile: exit 0, 814 directory entries in `config_files/` (812 index
files + generated `test.json` + the copied input `test.raw.json`), `config_files/500.json` bytes sha256
equal to the instrument's `would_be_file_sha256` above, parsed
object equal to `projected_task`, and `config_files/test.json` sha256 equal to the profile's
`projected_text_sha256` (`2aec098e…`, `54cf9833…`, `49bbee2e…`, full digests in the table above and in
`--summary` lines 17/28/39). No leftover marker of any of the eight `__…__` strings in the generated
500 file. The generated file has no trailing newline.

## Observed: your two specific questions

- **Non-URL field change: none** for task 500. Raw-vs-projected deep leaf diff is exactly the two
  `/500/start_url` and `/500/eval/program_html/0/url` leaves; both are URL-shaped by field name. `sites`
  and `storage_state` are unchanged — the underscore-free substring `shopping_admin` occurs twice in
  the span, once in `sites` and once in `storage_state`, and the token occurs zero times inside `storage_state`, so
  the substitution is token-scoped, not site-name-scoped. For scale: my independent global diff gets 61
  non-URL-field leaves per profile, matching the instrument's 61, which it splits as `must_include[]` 60
  + `reference_answer_raw_annotation` 1; none of them under `/500/`.
- **Multi-occurrence leaf: none** for task 500 — each of its 2 leaves holds exactly 1 occurrence, so
  `changed_leaves_by_token.__SHOPPING_ADMIN__` = 300 = its occurrence count 300 (no hidden
  multiplicity for this token anywhere). Globally 13 leaves hold >1 occurrence (e.g.
  `/604/eval/reference_url` holds three `__REDDIT__`); filtered for prefix `/500/` the set is empty.

## Observed: aggregate cross-checks that bound this unit (all equal)

- `--summary`, `--json`, `--selftest`: exit 0 each; `findings` empty; `index_mapping.violations` empty.
- `string_leaf_count` 10869 = my independent count of string leaves in the parsed raw (10869).
- Occurrence totals by token 385/336/281/300/0/133 = my independent text counts; provenance rows
  total 1435 (1435 occurrences across 812 distinct `task_index` values = `tasks_with_any_token` 812).
- My leaf-with-token counts from provenance (385/323/275/300/133) equal
  `changed_leaves_by_token` (385/323/275/300/133); my global changed-leaf total is 1416 = instrument.
- `tokens_followed_by_slash` 697 = my independent 697; task 500 contributes exactly **1** of them, the
  `program_html[0].url` seam that becomes `//` under the trailing-slash profile; its bare `start_url`
  token contributes 0.
- Determinism: `--json` sha256 `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630` reproduced
  byte-identically on rerun, under `LC_ALL=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0`, and with
  `--root <lane>` invoked from `/tmp`; identical to `corpus/evidence/round29-calibration/build-json-sha256.txt`.

## Findings that qualify the claim (no mismatch, but novelty-bearing)

1. **Key-order trap.** Instrument `--json.projected_task` is emitted key-sorted (`eval`, `geolocation`,
   … , `task_id`), while the generator's file preserves raw order (`sites`, `task_id`, …). Serializing
   `projected_task` in instrument order gives sha256 `c940efdc12d56dbf293dc1bc5a3ecc8f17f3807b655ffb60f42684a819ea2b07`,
   not `413ed901…`. Byte faithfulness is carried by `would_be_file_sha256` only; a consumer comparing a
   re-serialized `projected_task` would report a false mismatch. [INFERENCE] This is a presentation
   property, not a projection error, and the instrument's own sha is correct.
2. **Count units differ by design.** `applied_replacements` counts text occurrences (REDDIT 336,
   SHOPPING 281) while `changed_leaves_by_token` counts leaves (323, 275). For task 500's token both are
   300, so this unit cannot show the difference.
3. **Index-vs-task_id is degenerate on this population.** Independently: 0 of 812 tasks has
   `task_id != index`, 0 duplicate ids, so index 500 = `task_id` 500. This case cannot discriminate
   positional naming from `item["task_id"]` naming; the candidate already discloses this
   (`drafts/webarena-config-projection.md` line 61). The instrument's `index_equals_task_id` = 812 and
   empty `violations` are consistent with that.
4. **Profile values are inert to later steps:** none of the 18 profile values contains `__` or an
   internal `//`, so no later-token cascade or accidental scheme doubling arises from the values
   themselves for this unit.

## Unresolved gaps / scope of this verdict

- I did not read the instrument source, so its internal rule for assigning `url_field` vs
  `non_url_field` is unaudited; task 500's two leaves are URL-shaped by name and do not stress it.
- Task 500 holds no quote, backslash, multi-token or cascade leaf, so the candidate's
  quote/backslash and later-token-cascade disclosure branches are not exercised here.
- Scope: one `task_id` × 3 synthetic profiles of an offline projection; no deployment, runtime,
  task-validity or model claim is tested.

Mismatches found: none, in any of the four compared dimensions, across all three profiles.

VERDICT: PASS

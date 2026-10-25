writer: KengakuR29-2.FCase101-2

# FCase101 — raw task_id 101 projected under all 3 frozen profiles

Scoped attack on one task/profile record: derive task 101's projected object and changed
leaves independently, then compare field-by-field with the `--json` record at output_index
101 in each profile. Lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; all paths
below are relative to it unless stated.

## Independence disclosure

I did **not** read or import `plans/config_projection.py` source. I read only instrument
**output**: `--help`, `--summary` (captured to
`.ufo/waves/round-29/scratch/falsify/FCase101/summary.txt`), and `--json` (captured to
`.ufo/waves/round-29/scratch/falsify/FCase101/instrument.json`, sha256
`c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`, 3881050 bytes).
Derivation source = prereg text (`plans/round-29-claims.md`), pinned generator bytes,
pinned manifest/profiles/raw. My oracle is `scratch/falsify/FCase101/oracle101.py`
(output `oracle101.json`); the full-document census is
`scratch/falsify/FCase101/census.py` (output `census.json`). No REA devices, no
delegation, no writes outside my scratch dir and this report.

## Authenticated inputs (observed)

`sha256sum` over lane files:

- `plans/fixtures/r29/manifest.json` → `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87`
- `plans/fixtures/r29/generate_test_data.py` → `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd`
- `plans/fixtures/r29/profiles.json` → `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018`
- `plans/fixtures/r28/webarena/config_files/test.raw.json` → `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`

Instrument echoes the same digests in `inputs`, `raw_text_sha256`, `manifest_sha256`.
Raw text: 880776 bytes = 880776 Unicode codepoints, ASCII-only (0 codepoints >127), so
codepoint and byte offsets coincide on this pin. Independent JSON decode with a
duplicate-key hook found 0 duplicate keys in the whole document.

## Independent derivation (observed)

Generator contract from its bytes: global text replacements in order at lines 11–16
(GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP; MAP at line 16:
`raw = raw.replace("__MAP__", MAP)` — 4 words, counted by `str.split`), then `json.loads`
(line 20), then per-index write `json.dump(item, f, indent=2)` (line 22, 3 words, no
trailing newline) to `config_files/{idx}.json` (line 22).

Oracle procedure: read raw text once; apply the six replacements sequentially in source
order using `profiles.json` values; `json.loads`; take parse position 101; walk string
leaves of raw item 101 and projected item 101; emulate the generator's per-task file write
to a `/tmp` copy with `json.dump(..., indent=2)` and hash the resulting bytes.

Raw task 101: object span codepoints 93506–94343, lines 3241–3270. Exactly one placeholder
occurrence inside it, at codepoint 93634 (line 3248, column 19), token `__MAP__`, leaf
`/start_url`, text `"start_url": "__MAP__"` (2 words). Raw `task_id` = 101, raw index = 101.

Per-profile sequential step counts (my replay): GITLAB 385, REDDIT 336, SHOPPING 281,
SHOPPING_ADMIN 300, WIKIPEDIA 0, MAP 133 — sum 1435. Profile values contain no `__…__`
token, so no later-token cascade and order is inert for these three profiles; the source
order is nonetheless reproduced exactly, and `__SHOPPING__` is not a substring of
`__SHOPPING_ADMIN__` (checked).

## Field-by-field comparison at output_index 101 (observed)

Record keys per profile: `changed_leaves`, `index_equals_task_id`, `output_filename`,
`output_index`, `projected_task`, `task_id`, `would_be_file_sha256`; each profile's `tasks`
list has 812 records with 812 distinct `output_index` values.

| compared field | distinct_origins | path_prefix | trailing_slash_sensitivity |
|---|---|---|---|
| `output_index` / `task_id` | 101 / 101 | 101 / 101 | 101 / 101 |
| `index_equals_task_id` | true | true | true |
| `output_filename` | `config_files/101.json` | same | same |
| changed leaf count | 1 | 1 | 1 |
| pointer / path_template / category | `/101/start_url` / `start_url` / `url_field` | same | same |
| `original` | `__MAP__` | `__MAP__` | `__MAP__` |
| `projected` | `http://map.invalid:10106` | `http://map.invalid:10206/prefix` | `http://map.invalid:10306/` |
| `tokens` | `["__MAP__"]` | `["__MAP__"]` | `["__MAP__"]` |
| `would_be_file_sha256` | `e9d6ea798747ed9ed38231b79cd6aba97e973f0b305749e199acce9745f56e73` | `3150efc5ca6865a691acf330800fd57f576e8ae7a48d43eba90eacabd6fcc982` | `184b12644ee3f33b81efd2bb6ba8ab1a04e7ac946d66684293f2c7de94cc28f8` |
| oracle emulated file sha256 / size | same / 796 B | same / 803 B | same / 797 B |
| `projected_text_sha256` (= oracle) | `2aec098e5705c98c7f7977a4eb8962aa455c2224d078dbfe4c1fc113e7c707f4` | `54cf98337dc6751d9453ee069ff26bb3836698518527cf8683c85bf66744744b` | `49bbee2e827791b79f42858ac78637704adaa7e36f1cb3a9268563e8df3e01b2` |
| `projected_task` vs raw item diff | exactly `/start_url` | exactly `/start_url` | exactly `/start_url` |

`would_be_file_sha256` matches the generator-faithful write (no newline; emulated file
bytes end `6\n}`, i.e. no trailing newline). Each emulated file's bytes were produced by
`json.dump(item, f, indent=2)` on the projected item, not by hashing the instrument's
`projected_task` rendering. `projected_task` is deep-equal to `json.loads(projected_text)[101]`
in all three profiles; the only differing leaf against the raw item is `/start_url`, with
the expected profile value. `changed_leaves` entries in the record equal my derived leaf
records (pointer, category, original, projected, tokens) in all three profiles.

Raw-occurrence provenance for task 101: exactly 1 entry,
`{"json_pointer": "/101/start_url", "original_input_codepoint_offset": 93634,
"path_template": "start_url", "string_role": "value", "task_index": 101,
"token": "__MAP__"}`. My independent span map (iterative `raw_decode`) places codepoint
93634 inside item 101's span and at the `__` of `__MAP__`; total provenance entries 1435,
equal to the raw occurrence sum.

## Mismatches

None. Every field named in the assignment (projected_task, changed_leaves
pointer/category/token/original/projected, output_filename, index_equals_task_id,
would_be_file_sha256) and the added checks (per-profile projected text digest, occurrence
offset, per-task file bytes/size) agreed for all 3 profiles. `--json` exited 0 with
`findings: []`; `--summary` exited 0 with `TOTAL findings=0 exit=0`.

## Non-URL changes and multi-occurrence leaves (observed)

- Task 101: **no non-URL field change**, and **no leaf with more than one occurrence**;
  its single changed leaf is the URL-valued `start_url` with one `__MAP__`.
- Document-wide (my independent census, same in all 3 profiles): 1416 changed leaves,
  812 changed tasks; 1355 URL-field leaves (start_url 812, `eval.reference_url` 205,
  `eval.program_html[].url` 338) and 61 non-URL-field leaves (60
  `required_contents.must_include[]`, 1 `eval.reference_answer_raw_annotation`).
- 13 multi-occurrence leaves: `/66/eval/reference_answer_raw_annotation` (2×REDDIT),
  `/431/start_url` (3×SHOPPING), `/432`–`/435/start_url` (2×SHOPPING each),
  `/604` (3×REDDIT), `/608` (2), `/609` (3), `/625` (2), `/681` (3), `/682` (4),
  `/683` (2×REDDIT) at `/eval/reference_url`. Extras over leaves: REDDIT 13, SHOPPING 6.
  None is index 101.
- Unit note: the per-task `tokens` list is de-duplicated per leaf, so
  `len(tokens)` is not an occurrence count — e.g. `/604/eval/reference_url` has 3
  `__REDDIT__` occurrences but record `tokens` `["__REDDIT__"]`. Occurrence multiplicity is
  preserved independently in `population.original_occurrences_by_token` (REDDIT 336,
  SHOPPING 281; sum 1435), in the 1435-entry `occurrence_provenance`, and in the per-profile
  `steps[].applied_replacements`. The instrument's units therefore stay separate
  (1435 occurrences vs 1416 leaves vs 812 tasks vs 2436 projections), and the leaf/task
  aggregates (`changed_leaves_by_token` 323/275, `changed_tasks_by_token`,
  `tasks_with_token` 204/128/192/182/0/128) are leaf- or task-counts, not occurrence counts.
  For task 101 the single token element equals its single occurrence, so this choice has no
  effect on the attacked record.

Other independent cross-checks that matched the instrument: `string_leaf_count` 10869;
812 distinct task IDs (0–811, so `task_id == index` for every item); `tokens_followed_by_slash`
697 (GITLAB 225, REDDIT 232, SHOPPING 110, SHOPPING_ADMIN 125, MAP 5); non-token markers
`__last_url__` 65 and `__page__` 12; changed leaves 1416 / categories 1355+61 / path-template
tallies in all profiles; stimulus observations 0 junction for distinct/path-prefix profiles and
697 for trailing-slash profile (consistent with the 697 tokens followed by `/`).

## Index versus task_id

Record `output_index` 101 and `task_id` 101 coincide; the frozen raw file has
`task_id == index` for all 812 items, so task 101 alone cannot discriminate index-based
from task_id-based filename attribution. The record's `output_filename` uses the index
position (`config_files/101.json`), matching the generator's enumerate loop; discrimination
on shuffled IDs belongs to the hand-witness path, not this item. [INFERENCE] On this pinned
input the two mappings are observationally identical.

## Tools, installs, writes

No installs or upgrades (python3 3.14 stdlib, `sha256sum`, `grep`; no pacman). Writes:
this report and files under `.ufo/waves/round-29/scratch/falsify/FCase101/` only; the
generator-emulation write ran on `/tmp/fcase101/`. The instrument was run read-only;
it wrote no `config_files/test.json` and no per-task files: no `config_files/` directory
exists at the lane root or under `plans/` (both `ls` failed), and `git status --porcelain`
lists no such paths.

## Remaining unknowns

- [INFERENCE] None specific to task 101. Broader questions outside this item
  (shuffled-ID hand witness, mutation/selftest adequacy, candidate prose) were not tested
  here and are not claimed.

VERDICT: PASS

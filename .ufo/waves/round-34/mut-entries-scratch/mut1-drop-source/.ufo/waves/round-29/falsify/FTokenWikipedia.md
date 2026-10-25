writer: KengakuR29-2.FTokenWikipedia-2

# FTokenWikipedia — independent `__WIKIPEDIA__` census vs instrument output

Seat `KengakuR29-2.FTokenWikipedia-2` (leaf; no delegation, no subagents). Date 2026-10-21.
Scope: the `__WIKIPEDIA__` census of round-29 claim C1 only — raw-text occurrences, tasks carrying
the token, decoded leaves, per-profile applied replacements and changed-leaf/changed-task attribution,
plus the `sites`-derived-counting question. No production edit, no fixture edit, no score/calibration
claim, no round admission.

**Independence statement.** I did **not** read, `cat`, `grep` or import `plans/config_projection.py`.
I ran it read-only (`--summary`, `--json`, `--selftest`) and compared only its stdout. Everything below
was derived from the prereg text, the pinned generator bytes, the pinned raw JSON, the pinned
`profiles.json`, and my own stdlib scripts in
`.ufo/waves/round-29/scratch/falsify/FTokenWikipedia/` (`census2.py` 19,221 bytes, plus outputs named in
§7). The only operation touching the production file besides execution was `wc -c` (size only).

## 1. Attack and headline

Independent literal census of `__WIKIPEDIA__` on the pinned raw 812-task file:
**0 raw occurrences, 0 decoded leaves, 0 keys, 0 tasks, 0 applied replacements in each of the 3
profiles.** The instrument reports the same zero on every required surface. No numeric mismatch was
found for this token; §6 reports two mismatches elsewhere in the integrated census material and one
latent path-encoding defect.

Observed raw file: 880,776 bytes = 880,776 codepoints, pure ASCII (0 bytes >127), sha256
`7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` (matches manifest pin).

Generator step 5 of 6 is line 15:
`raw = raw.replace("__WIKIPEDIA__", WIKIPEDIA)` (quote, 4 words by `split()`, run and counted).
It is executed but matches nothing in this input.

## 2. Independent census (mine) vs instrument output

Commands run (lane root): `python3 plans/config_projection.py --summary`, `--json`, `--selftest`
(exit 0 each; `findings: []`), then `python3 .ufo/.../FTokenWikipedia/census2.py` (exit 0).

| Surface (instrument location) | mine | instrument |
|---|---:|---:|
| `summary` `ORIGINAL_OCCURRENCES_BY_TOKEN.__WIKIPEDIA__` | 0 | 0 |
| `summary` `TASKS_WITH_TOKEN.__WIKIPEDIA__` | 0 | 0 |
| decoded leaf occurrences / decoded leaves carrying | 0 / 0 | 0 (implied; per-task records below) |
| dict **keys** carrying the token | 0 | `occurrence_roles {"value": 1435}` (no key role) |
| `PROFILE <p> applied_replacements.WIKIPEDIA`, 3 profiles | 0, 0, 0 | 0, 0, 0 |
| `PROFILE <p> changed_leaves_by_token.__WIKIPEDIA__` | 0, 0, 0 | 0, 0, 0 |
| `PROFILE <p> changed_tasks_by_token.__WIKIPEDIA__` | 0, 0, 0 | 0, 0, 0 |
| `PROFILE <p> remaining_known_tokens_{text,decoded}.__WIKIPEDIA__` | 0 ×6 | 0 ×6 |
| projected text occurrences of `wikipedia.invalid` | 0, 0, 0 | no such field |
| projected task objects containing token or `wikipedia.invalid` | 0 of 2436 | 0 of 2436 |

All-token census agrees too (so the zero is not a cherry-picked field): raw
`{GITLAB 385, REDDIT 336, SHOPPING 281, SHOPPING_ADMIN 300, WIKIPEDIA 0, MAP 133}`,
identical decoded counts, task presence `{204,128,192,182,0,128}`. Every `__X__` marker in the raw text
is exactly `{__GITLAB__ 385, __REDDIT__ 336, __SHOPPING__ 281, __SHOPPING_ADMIN__ 300, __MAP__ 133,
__last_url__ 65, __page__ 12}`; there is no sixth environment token.

## 3. Why the zero cannot be a hidden variant

- Case-sensitive counts in the raw text: `WIKIPEDIA` 0, `Wikipedia` 0, `__WIKIPEDIA` 0, `WIKIPEDIA__` 0,
  `__wiki` 0. Case-insensitive `wikipedia` = 23, all equal to the complete value `wikipedia`.
- File is ASCII-only, so fullwidth/lookalike codepoints cannot exist (0 non-ASCII bytes).
- Descriptor-level: any escape-composed occurrence needs literal `WIKIPEDIA` in the text (0) or the
  token in decoded values (0). Both directions closed.
- Upstream identity: live fetch of the manifest URLs at revision `dce04686` returns
  `test.raw.json` 880,776 bytes sha256 `7b50386f…537652` and `generate_test_data.py` 838 bytes sha256
  `45ddba7b…921cd` — byte-identical to the pins. The absent token is a property of upstream
  `dce04686`, not of a lane-side fixture edit.

## 4. Tasks whose `sites` metadata lists `wikipedia` (the requested trap check)

23 tasks: 97, 265–268, 424–430, 556–561, 737–741. All 23 carry a token, but never `__WIKIPEDIA__`:
17 carry one `__MAP__` (`/start_url`), 6 carry two `__GITLAB__` (`/start_url` and
`/eval/program_html/0/url`). Site census vs token census:

| site name | tasks listing it | tasks carrying its token |
|---|---:|---:|
| wikipedia | 23 | 0 |
| reddit | 129 | 128 |
| shopping_admin | 184 | 182 |
| gitlab | 204 | 204 |
| shopping | 192 | 192 |
| map | 128 | 128 |

The instrument's `TASKS_WITH_TOKEN` tracks the **token** column, not the site column (wikipedia 0 vs 23).
Direct per-task proof from `--json` (`profiles.distinct_origins.tasks[i]`): task 791 has
`sites ["gitlab","reddit"]` and exactly one changed leaf `('/791/start_url', ['__GITLAB__'])`; tasks 759
and 760 have `sites ["map","shopping_admin"]` and one changed leaf each `('/759…','/760…/start_url',
['__MAP__'])`; all 23 wikipedia-site records list only `__MAP__` or `__GITLAB__`. `sites` is byte-identical
in all 2436 `projected_task` objects (0 differences), and no `json_pointer` or `path_template` in the
provenance or changed-leaf output points into a `sites` array. The instrument therefore does not derive
any token count from `sites`.

## 5. Stronger-than-summary agreement checks

- Occurrence provenance: 1435 entries; my independently scanned `(offset, token, task_index)` multiset is
  equal to the instrument's exactly (0 missing, 0 extra). Every
  `original_input_codepoint_offset` slices the raw text to exactly its `token` (0 failures). Every
  `json_pointer` resolves and its leaf occurrence count equals the number of provenance rows for that
  leaf (0 problems). Offsets lie in 172…880440 and 880440+13 ≤ 880776.
- Provenance order is grouped by replacement step (GITLAB→REDDIT→SHOPPING→SHOPPING_ADMIN→MAP), ascending
  within each group; there is no WIKIPEDIA group because there are no entries. No order requirement was
  violated; this is a presentation observation.
- Per-profile: my sequential six-`str.replace` replay (count taken on the evolving text immediately
  before each step) gives step counts `[385,336,281,300,0,133]` for all three profiles, equal to
  `profiles.<p>.steps[*].applied_replacements`. Projected-text sha256 identical to the instrument:
  `2aec098e…707f4` / `54cf9833…44744b` / `49bbee2e…3e01b2`.
- Per-task objects: all 812 × 3 = 2436 records agree on `output_index`, `output_filename`,
  `task_id`, `index_equals_task_id`, full `projected_task`, and `would_be_file_sha256`
  (my independent `json.dumps(task, indent=2)` bytes) — 0 mismatches. `index == task_id` for 812/812.
- Changed leaves: all 1416 × 3 records agree on `json_pointer`, `original`, `projected`,
  `path_template`, `tokens` — 0 mismatches. Aggregates agree: 1416 leaves, 812 changed tasks,
  `changed_leaves_with_multiple_occurrences` 13, categories `{url_field 1355, non_url_field 61}`.
  The name-keyed `changed_leaves_by_token` is a leaf-presence count (my presence computation matches
  385/323/275/300/0/133 exactly), distinct from occurrence counts (385/336/281/300/0/133) and task
  counts (204/128/192/182/0/128).
- Determinism/read-only: two `--json` runs both sha256 `c8da0c5a…b34630`; two `--summary` runs both
  `5ce5cb0f…6e36f`; no file written under `plans/` (only `test.raw.json` exists in the r28 config dir);
  `git status --porcelain plans/` showed no modification to pinned inputs.
- Input digests recomputed: all three `inputs` entries, `manifest_sha256`
  `f6390b92…817bf87`, and `raw_text_sha256` match my own hashes.

## 6. Mismatches found (exact location and value)

**M-1 (instrument census): none.** No instrument field disagrees with my independent values.

**M-2 (evidence prose, round-29 build report).**
`.ufo/waves/round-29/build/R29TokenWikipedia.md` line 72:
“Totals: 1,435 raw occurrences across 1,416 distinct leaves (19 leaves carry two occurrences: 13 REDDIT,
6 SHOPPING)”.
Observed from the pinned bytes: **13** leaves carry more than one occurrence — 8 carry exactly 2, 4 carry
3, 1 carries 4. 19 is the **extra-occurrence** count (1435 − 1416). Leaf presence is 8 REDDIT-bearing
and 5 SHOPPING-bearing; the stated 13/6 are the extra *occurrence* attributions (REDDIT 13, SHOPPING 6),
not leaf counts. The instrument's own `changed_leaves_with_multiple_occurrences: 13` agrees with the
bytes, so the report sentence — not the instrument — is wrong. This is unit pooling of exactly the kind
the prereg forbids ("do not pool units", 4 words by `split()`).

**M-3 (evidence prose, minor).** Same report line 134 lists `__SHOPPING_ADMIN__` among the tokenized
`start_url` values of the 23 wikipedia-site tasks. Observed: 17 × `__MAP__` and 6 × `__GITLAB__`, no
`__SHOPPING_ADMIN__`. The sentence has an ellipsis, so this is an imprecision rather than a hard
contradiction.

**M-4 (latent schema defect, not triggered).** The instrument's `json_pointer` strings are not RFC 6901
escaped. The raw document contains 14 string leaves under dict keys that themselves contain `/` — tasks
363, 364, 365, 366, 367, 761, 762 at `instantiation_dict` keys `location/address_1` and
`location/address_2` (e.g. `/363/instantiation_dict/location/address_1`). Naive resolution of such a
pointer raises `KeyError: 'location'`; the escaped form `location~1address_1` resolves to
`'Carnegie Mellon University'`. None of these 14 leaves contains a token, so no emitted provenance or
changed-leaf pointer is affected on this population (0 collisions). The defect is latent: a token under
such a key would produce an unresolvable/ambiguous path in the claim's "changed string leaves by JSON
path" output.

## 7. Exact commands and scratch artifacts

- `python3 plans/config_projection.py --summary` → 47 lines, exit 0; 17 lines mention `WIKIPEDIA`, all
  values 0. `python3 plans/config_projection.py --json` → 3,881,050 bytes, exit 0, `findings: []`.
- `python3 plans/config_projection.py --selftest` → exit 0, one line, `SELFTEST clean cases=20`,
  including `hand_cascade_order_R29_ORDER_CASCADE_01` (that fixture's
  `expected_after_each_source_step` contains a dynamically inserted `__WIKIPEDIA__/probe` and expects
  one WIKIPEDIA-step hit; [INFERENCE] the clean selftest exercises the WIKIPEDIA step there, not on the
  812-task population).
- Scratch (all written under the assigned scratch dir): `summary.txt`, `summary2.txt`, `json.out.json`,
  `json2.out.json`, `census.txt`, `census2.py`, `census2.out.txt`, `wikipedia_contexts.txt`,
  `sites_vs_tokens.txt`, `extra_checks.txt`, `selftest.txt`.
- Tooling: no installs, no upgrades, no pacman/service actions. Two read-only HTTPS GETs of the public
  pinned URLs in `plans/fixtures/r29/manifest.json` (raw.githubusercontent.com, revision `dce04686`) to
  verify upstream byte identity; no credentials, auth state or private URLs touched. No REA MCP device
  used. No production/fixture/corpus/SOURCES/SCORECARD/candidate file edited.

## 8. Unknowns kept open

- I did not read the production source, so I cannot state how the instrument extracts the six-step
  contract; only its output was tested. [INFERENCE] WIKIPEDIA's presence in
  `source_contract.replace_steps` (line 15) and in all six token dictionaries is consistent with a
  contract-driven token set rather than a scan of the raw data.
- The pinned input is ASCII, so codepoint and byte offsets coincide here; this input cannot distinguish
  a codepoint-offset implementation from a byte-offset one.
- Whether other upstream config splits contain `__WIKIPEDIA__` was not opened (one raw file exists in
  the fixture tree).

## 9. Scoped conclusion

The instrument's `__WIKIPEDIA__` census is exactly correct and provably not site-derived: zero raw
occurrences, zero tasks, zero decoded leaves, zero applied replacements under all three profiles, zero
changed leaves/tasks attributed to the token, zero residual occurrences, and the WIKIPEDIA profile value
never enters any of the 2436 projected task objects. The only defects found are outside the instrument's
numbers: a falsified leaf/occurrence unit sentence in the round-29 Wikipedia build report (M-2), a minor
enumeration imprecision (M-3), and a latent unescaped-JSON-Pointer schema defect that no token occurrence
triggers on this population (M-4).

VERDICT: PARTIAL

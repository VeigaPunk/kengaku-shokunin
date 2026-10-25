writer: KengakuR29-2.FTokenMap-2

# FTokenMap — independent `__MAP__` census attack (round 29 post-crash falsify)

## What this attacks

The one declared claim C1 requires "per-profile raw replacement counts by token" and
"occurrence/field provenance" over the pinned raw 812-task file under 3 frozen synthetic profiles.
This item attacks only the `__MAP__` slice of that census: literal occurrences in the raw text,
tasks carrying them, decoded string leaves carrying them, per-profile applied replacements and
changed leaves/tasks, plus cross-token overlap by substring logic. No other claim dimension is
touched.

Independence: I did not read or import `plans/config_projection.py`. Every input was one of: the
prereg text `plans/round-29-claims.md`, the pinned generator bytes, the pinned profiles/manifest,
the pinned raw task file, and the instrument's `--summary`/`--json` **output**. Production source
reads: 0.

## Pinned inputs (observed, `sha256sum`)

| file | sha256 | size |
|---|---|---|
| `plans/fixtures/r28/webarena/config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | 880,776 bytes |
| `plans/fixtures/r29/generate_test_data.py` | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` | 838 bytes |
| `plans/fixtures/r29/profiles.json` | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` | 1,391 bytes |
| `plans/fixtures/r29/manifest.json` | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` | 1,061 bytes |

Raw file facts observed independently: 0 CR bytes, 29,604 LF, 0 non-ASCII bytes, parses as a
812-element JSON array; `task_id == index` for all 812 elements.

## Probe design (own code)

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FTokenMap/independent_census.py`
(stdlib only) does, without importing production code:

1. Derives the six token/name steps from the generator TEXT by regex, gets lines 11–16, and matches
   the manifest `replacement_order` names.
2. Counts literal occurrences by `str.count`, by lookahead-overlapping regex, and via external
   `grep -o`/`grep -bo`; counts occurrences in decoded values and JSON keys separately.
3. Parses the raw text with its own recursive JSON parser that records every string value's raw
   span, JSON pointer, path template and top-level task index (this is how occurrence offsets and
   pointers are checked, not assumed).
4. Replays the six sequential `text.replace(token, value)` steps per profile, records the count at
   each step, parses the projected text, and diffs every leaf against the original.
5. Re-implements the per-leaf rewriting oracle independently and compares it to the text-level
   projection (benign synthetic-profile domain).
6. Compares all of the above against `--summary` lines and every `--json` record/per-task object.

## Results — `__MAP__` census vs instrument

All values observed; "I" = independent, "inst." = instrument output.

| metric | I | inst. | location | match |
|---|---|---|---|---|
| raw-text literal occurrences | 133 | 133 | summary `ORIGINAL_OCCURRENCES_BY_TOKEN` | yes |
| decoded string leaves carrying it | 133 | (`changed_leaves_by_token` 133) | summary `PROFILE * changed_leaves_by_token` | yes |
| occurrences inside decoded leaves | 133 | — | derived | — |
| occurrences in JSON keys | 0 | `OCCURRENCE_ROLES {"value": 1435}` | summary | yes |
| leaves with 2+ `__MAP__` | 0 (hist `{1:133}`) | n/a | — | — |
| tasks carrying it | 128 | 128 | summary `TASKS_WITH_TOKEN` | yes |
| per-task occurrence histogram | `{1:123, 2:5}` | n/a | derived from per-task objects | — |
| path templates carrying it | `start_url` 128, `eval.reference_url` 5 | same via `changed_leaves_by_path_template`/provenance | json per-task `changed_leaves` | yes |
| category of MAP leaves | `url_field` 133, `non_url_field` 0 | `changed_leaves_by_category` consistent | json | yes |
| applied replacements (3 profiles) | 133 / 133 / 133 | 133 / 133 / 133 | summary `PROFILE * applied_replacements` | yes |
| changed leaves by token (3 profiles) | 133 / 133 / 133 | 133 / 133 / 133 | summary | yes |
| changed tasks by token (3 profiles) | 128 / 128 / 128 | 128 / 128 / 128 | summary | yes |
| remaining `__MAP__` text / decoded | 0 / 0 ×3 | 0 / 0 ×3 | summary `remaining_known_tokens_*` | yes |
| projected text sha256 ×3 | `2aec098e…c707f4`, `54cf9833…744b`, `49bbee2e…01b2` | identical ×3 | json `projected_text_sha256` | yes |

The 5 double-occurrence tasks are exactly tasks 377–381, which carry the token in `start_url`
(exact value `__MAP__`) *and* in `eval.reference_url` (prefix form, e.g.
`__MAP__/search?query=restaurants%20near%20CMU%20ArtPark%20Lab`). 123 tasks carry it once, each in
`start_url`, whose distinct original value is the single string `__MAP__`. The 133 changed-leaf
pointer set is identical under all three profiles.

## Results — per-task objects, provenance, file bytes

- Per-task `projected_task` equality: 812 × 3 = 2436/2436 identical to my independent text
  projection; `changed_leaves` entries (pointer, template, category, original, projected, token
  order) 2436/2436 task records identical → 0 mismatches.
- Leaf-rewriting oracle: 0 failures over all changed leaves in all 3 profiles (so within the frozen
  benign domain, decoded-leaf rewriting and text-level projection agree, MAP included).
- Provenance: 133 `__MAP__` entries, all unique, sorted by offset, decoding back to `__MAP__`; the
  tuple set (task_index, pointer, template, offset) is exactly equal to my raw-scanner set (no
  missing, no extra). Offsets are exactly the `grep -bo` byte offsets (`6238, 7404, 8467, 9643,
  15442, …`, count 133) and span `6238` (task 7, `/7/start_url`) to `826335` (task 767,
  `/767/start_url`).
- `would_be_file_sha256`: 2436/2436 equal `sha256(json.dumps(item, indent=2))` with dict key order
  taken recursively from the **original raw task** and no trailing newline; 0/2436 with a trailing
  newline. Task 0 example: instrument `9533088e31781047e4c4f3b9cafe02f734aaaa3fb9c47ebc29176bd8d6a6e5e6`,
  raw-key-order hash identical; printed-key-order hash `823a9a7f…` differs. See "resolved
  observation" below.

## Overlap / substring logic

- No token is a substring of another token (substring matrix over all ordered pairs is empty).
- The prefix `__SHOPPING__` is **not** a substring of `__SHOPPING_ADMIN__` (§ literal check
  returns False). The combined prefix `__SHOPPING` occurs 581 times in raw text, yet the instrument
  reports `applied_replacements` `SHOPPING` = 281 and `SHOPPING_ADMIN` = 300; after the SHOPPING
  step my replay shows `__SHOPPING_ADMIN__` still 300 and `__MAP__` still 133. Prefix-agnostic
  counting is therefore excluded by observation.
- No profile value contains `__`, contains any token, or creates `__MAP__` at a concatenation
  boundary; every earlier step leaves the `__MAP__` stage count at 133 (all six steps, all three
  profiles). MAP is last, so there is no later-token cascade into it.
- `__MAP__` appears only as the exact token: `__MAP` 133, `MAP__` 133 (both only inside the token),
  bare `MAP` outside `__MAP__` 0, `__MAPS__`/`__map__`/`__Map__` 0; non-token markers
  `__last_url__` 65 and `__page__` 12 match `OTHER_MARKERS_NOT_ENV_TOKENS`.
- Self-overlap ambiguity: non-overlapping count 133 == lookahead-overlapping count 133, so
  `str.replace`/`str.count` and any overlapping reading agree on this input.
- Next character after each token: `"` 128, `/` 5; raw slash-follow sites total 697, matching
  `tokens_followed_by_slash` 697 and the trailing-slash profile's
  `value_slash_then_raw_slash_junctions` 697 (MAP contribution 5, all in tasks 377–381). Trailing
  profile therefore yields the documented double slash, e.g. task 377
  `http://map.invalid:10306//search?query=restaurants%20near%20CMU%20ArtPark%20Lab`; no
  normalization is silently applied.

## Mismatches

None. Every compared `__MAP__` metric and every compared per-task object/provenance entry matched.

Resolved adjacent observation (not a mismatch): my first pass flagged all 2436
`would_be_file_sha256` values as unreproducible. Root cause was mine: `--json` prints object keys in
sorted order, while upstream `json.dump(item, f, indent=2)` follows the raw task's insertion order
(observed raw order begins `sites, task_id, require_login, …`). Re-serializing in raw key order
reproduces all 2436 digests exactly. [INFERENCE] the JSON emitter sorts keys (`sort_keys=True`);
observed fact is that printed order is sorted and the digest matches raw order. Consequence for
verifiers: reproducing per-index file bytes from `projected_task` as printed in `--json` yields a
different digest; the emitted `would_be_file_sha256` is the correct raw-order byte digest.

## Discriminating-power limits (observed, scoped)

1. For `__MAP__`, `changed_leaves_by_token` cannot distinguish leaf semantics from occurrence
   semantics because every MAP leaf holds exactly one occurrence (133 leaves, 133 occurrences).
   The leaf semantics is corroborated indirectly: my leaf census gives `REDDIT` 323 leaves/336
   occurrences and `SHOPPING` 275/281, which equal the instrument's changed-leaf counts and differ
   from its applied-replacement counts; the instrument's 13
   `changed_leaves_with_multiple_occurrences` also equals my 13 multi-token leaves
   (distribution `{2:8, 3:4, 4:1}`, exactly the REDDIT/SHOPPING extras 13+6 = 19 occurrences over
   13 leaves).
2. The raw file is ASCII-only, so codepoint offsets equal byte offsets; this input cannot
   discriminate a codepoint claim from a byte claim. The field name is
   `original_input_codepoint_offset` and the values equal `grep -bo` offsets exactly, which is the
   strongest statement this input supports.
3. MAP's applied count is order-invariant here (no prior value contains the token and no prior
   token overlaps it), so the output cannot prove the count is measured at the MAP step rather than
   from the original text. Both readings agree at 133 on all three profiles.
4. Per-task equality is content equality; the printed object's key order is normalized as described
   above. No MAP consequence.

## Commands and outputs (exact)

- `sha256sum plans/fixtures/r29/manifest.json …` → the four digests in the table above.
- `python3 plans/config_projection.py --summary` → exit 0; lines compared include
  `ORIGINAL_OCCURRENCES_BY_TOKEN {…, "__MAP__": 133}`, `TASKS_WITH_TOKEN {…, "__MAP__": 128}`,
  `PROFILE <p> applied_replacements {…, "MAP": 133}`,
  `PROFILE <p> changed_leaves_by_token {…, "__MAP__": 133}`,
  `PROFILE <p> changed_tasks_by_token {…, "__MAP__": 128}` for `distinct_origins`, `path_prefix`,
  `trailing_slash_sensitivity`; `TOTAL findings=0 exit=0`.
- `python3 plans/config_projection.py --json > /tmp/r29map.json` → exit 0, 3,881,050 bytes,
  `findings: []`.
- `python3 …/scratch/falsify/FTokenMap/independent_census.py census_out.json` → `mismatches: []`,
  `task_object_mismatch_count: 0`, `leaf_entry_mismatch_count: 0`,
  `provenance_map_missing_from_mine: []`, `provenance_map_extra_in_mine: []`,
  `provenance_sorted_by_offset: true`, `provenance_offset_redecode: true`,
  `would_be_file_sha256` raw-order matches 2436/2436 (second pass).
- `grep -o '__MAP__' <raw> | wc -l` → 133; `grep -c '__MAP__' <raw>` → 133;
  `grep -bo '__MAP__' <raw>` first offsets `6238, 7404, 8467, 9643, 15442`.
- `jq '[.[] | [.. | strings | select(contains("__MAP__"))] | length] | add' <raw>` → 133;
  `jq '[.[] | select(any(..; (type=="string") and (contains("__MAP__"))))] | length'` → 128.

## Tooling

No package installs or upgrades; no pacman transaction run (host transactions paused). Observed
preinstalled tools: `python3 3.14.8`, `jq` resolving to `jaq 3.1.1`, `grep` = `pi-uu-grep 0.2.0`.
Both external tools were used only as independent triangulation of the Python census.

Quote discipline: every quoted span in this report is ≤4 whitespace-delimited words (longest is
the generator replacement line at 4 words; full instrument lines were parsed programmatically and
are reported as values, not quoted).

## Observed vs inference

- Observed: every count, hash, offset, pointer, per-task object and per-leaf value in the tables
  and command outputs above, plus the zero-mismatch comparisons from the script run.
- [INFERENCE]: only the claim that the JSON emitter uses key sorting (from observed sorted printed
  order plus raw-order digest reproduction); and the reading that unchanged MAP semantics are
  order-invariant (derived from the observed constant stage counts).

VERDICT: PASS

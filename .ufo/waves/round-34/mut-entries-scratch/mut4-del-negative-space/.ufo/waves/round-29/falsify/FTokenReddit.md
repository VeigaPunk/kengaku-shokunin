writer: KengakuR29-2.FTokenReddit-2
seat: KengakuR29-2.FTokenReddit-2 (read-only falsify leaf, round 29)
item: attack the __REDDIT__ census of plans/config_projection.py against the pinned raw task file
production-source disclosure: I did NOT read or import plans/config_projection.py source. I derived all
counts from the prereg text, the pinned generator bytes, the pinned raw JSON and profiles.json, and
compared only against the instrument's `--summary` / `--json` STDOUT (plus its README-free CLI behaviour).
No production, fixture, corpus, SOURCES, SCORECARD, candidate or git state was modified. No tools were
installed or upgraded (python3 3.14 stdlib only).

## Commands and evidence

All commands run from /home/vgpnk/Projects/shokunin/kengaku-shokunin; outputs kept in
.ufo/waves/round-29/scratch/falsify/FTokenReddit/:

- `python3 plans/config_projection.py --summary` → summary.txt (47 lines), exit 0, findings=0.
- `python3 plans/config_projection.py --json` → projection.json, exit 0, sha256
  c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630.
- `python3 .ufo/waves/round-29/scratch/falsify/FTokenReddit/census.py` → census-out.txt, exit 0,
  86 OK checks, FAILS: 0.
- pinned byte digests re-measured in census-out.txt lines 2–5:
  generator 45ddba7b…921cd (838 B), raw 7b50386f…37652 (880776 B), profiles 90fdc34d…94e018 (1391 B),
  manifest f6390b92…17bf87 (1061 B). All equal the prereg/manifest pins.
- determinism: current `--json` sha256 c8da0c5a…b34630 equals corpus/evidence/round29-calibration/
  build-json-sha256.txt; current `--summary` stdout lines equal build-summary.txt lines 1–47
  (receipt has one extra trailing `exit=0` line).

## Attack 1 — literal occurrence count in raw text

Own count on the raw 880776-byte ASCII text, three independent methods, all 336:
`str.count("__REDDIT__")` = 336; every-position `startswith` scan = 336 (so 0 overlapping-start
positions); regex lookahead = 336. Near-miss forms `___REDDIT` and `REDDIT___` = 0.

Instrument comparison: summary.txt line 9 `ORIGINAL_OCCURRENCES_BY_TOKEN {"__REDDIT__": 336, …}` and
projection.json `population.original_occurrences_by_token["__REDDIT__"]` = 336. MATCH.

## Attack 2 — decoded leaf and task census

Own independent JSON leaf walk (dict/list/str, no production helper), over 812 tasks /
10869 string leaves:

| unit | own value | instrument value | source |
|---|---|---|---|
| __REDDIT__ occurrences (decoded) | 336 | 336 | summary L9; json population |
| decoded leaves carrying __REDDIT__ | 323 | 323 | summary L20 changed_leaves_by_token |
| tasks carrying __REDDIT__ | 128 | 128 | summary L10 TASKS_WITH_TOKEN; L21 changed_tasks_by_token |

Reddit occurrence distribution by path (own): start_url 114, eval.program_html[].url 85,
eval.reference_url 83 (71 leaves), eval.program_html[].required_contents.must_include[] 52,
eval.reference_answer_raw_annotation 2 (1 leaf) = 336 occurrences / 323 leaves. No __REDDIT__
occurrence in intent, intent_template, reference_answer, reference_answers or sites; none in any object key.

Tasks: provenance task indices are 128 distinct values; every task index equals its decoded list
position (`all task_id == index` = True over 812; first 0, last 811).

## Attack 3 — per-profile applied replacements

Own replay of the generator's sequential `raw.replace` order from manifest.json
(GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP) with each profile's values:

| profile | own REDDIT applied | instrument applied_replacements["REDDIT"] |
|---|---|---|
| distinct_origins | 336 | 336 (summary L16) |
| path_prefix | 336 | 336 (summary L27) |
| trailing_slash_sensitivity | 336 | 336 (summary L38) |

All six keys match per profile too (385, 336, 281, 300, 0, 133). Count of literal `__REDDIT__`
after the preceding GITLAB replacement is still 336; no profile value contains `__`, so no
earlier/later replacement can create or consume a REDDIT token. Own projected-text sha256 equals the
instrument's per profile: 2aec098e…c707f4, 54cf9833…4744b, 49bbee2e…e01b2. Own parsed task count 812
per profile. MATCH.

## Attack 4 — changed leaf/task attribution (not just totals)

For each of 3 profiles × 812 tasks I diffed every original leaf against my own projected leaf and
compared the resulting list (json_pointer, original, projected, tokens, path_template) with the
instrument's `profiles[*].tasks[*].changed_leaves`: 812/812 equal per profile (0 mismatches).
`projected_task` objects equal for 812/812 per profile. `would_be_file_sha256` equals
sha256(json.dumps(task, indent=2)) with default ensure_ascii for 812/812 (with ensure_ascii=False,
31 tasks would differ — the instrument matches the generator's `json.dump(item, f, indent=2)`).
output_index, `config_files/<i>.json`, and task_id equal for 812/812.
Per-profile `changed_leaves_by_token`/`changed_tasks_by_token` equal to my leaf/task counters,
including REDDIT 323/128 in all three profiles and the zero-count WIKIPEDIA key.

## Attack 5 — occurrence provenance (offset and field)

Own span-tracking JSON parser over the raw text (records each string literal's pointer, raw inner span
and decoded value; 10869 spans, decoded document identical to json.loads):

- 336 provenance entries for __REDDIT__, offsets exactly the 336 own occurrence offsets, strictly
  increasing, no duplicates, and text[offset:offset+10] == "__REDDIT__" for all 336.
- every offset lies inside a string value; `string_role` is value for all 336; 0 in keys/structural text.
- pointer derived from the containing string span equals `json_pointer` for all 336.
- task_index equals the pointer's first array index for all 336; 323 distinct pointers, 128 distinct tasks.
- `path_template` counts from provenance equal the decoded occurrence counts above, including the
  2 vs 1 split at task 66 /eval/reference_answer_raw_annotation (offsets 61888 and 61968, raw lines
  2126 col 43 and col 123).
- anchors: first REDDIT occurrence offset 26080 (line 872 col 19, /27/start_url); last 779761
  (line 26171 col 19, /735/eval/program_html/0/url); task 682 has 4 occurrences in
  /682/eval/reference_url at raw line 23423.

MATCH; no missing, extra, duplicated, misattributed or non-value occurrence.

## Attack 6 — substring overlap with other tokens

- No one of the six tokens is a substring of another (pairwise test over all 30 ordered pairs = none).
  In particular `__SHOPPING__` is not inside `__SHOPPING_ADMIN__` (that token continues `_ADMIN__`,
  not `__`): raw counts are `__SHOPPING__` 281, `__SHOPPING_ADMIN__` 300, and prefix `__SHOPPING`
  581 = 281 + 300 exactly. Replacing SHOPPING before SHOPPING_ADMIN leaves 300 SHOPPING_ADMIN tokens.
- No decoded leaf carries two distinct tokens (0), so `changed_leaves_by_token` is a strict partition;
  its six values sum to 1416 == changed_leaf_count. REDDIT accounts for 323 of those leaves.
- No token appears in any JSON key; no token occurrence overlaps another occurrence of itself
  (scan == str.count for all six tokens).
- Instrument summary lines L20 (leaves 323), L16 (applied 336), L10 (tasks 128) are mutually consistent
  with these independent unit counts.

## Unit-separation check (the only place a reader could misread a "mismatch")

336 REDDIT occurrences sit in 323 leaves because 8 leaves hold multiple REDDIT occurrences with counts
[2,3,2,3,2,3,4,2] = 21 occurrences (315 single-occurrence leaves + 21 = 336; excess 13). The instrument's
`changed_leaves_with_multiple_occurrences` = 13 counts 13 leaves across all tokens (8 REDDIT + 5
SHOPPING), not 13 extra occurrences (the excess total is 19 = 13 REDDIT + 6 SHOPPING). The instrument
reports occurrences (336), changed leaves (323) and tasks (128) in separately named fields; treating
323 as an occurrence count would be a reader error, not a projection error.

## Mismatches

None. Every compared REDDIT value and every derived aggregate, per-task changed-leaf record, digest,
offset, pointer, task index and role matched between my independent derivation and the instrument's
`--summary`/`--json` output. No mismatch locations to report.

## Observed facts vs inference; residual scope

Observed: all counts, digests, offsets, pointer/task mapping, per-task projections and unit relations
above, from pinned bytes and instrument stdout.
[INFERENCE] Because the pinned raw file is pure ASCII without CR, Unicode-codepoint offsets equal byte
offsets here; the "codepoint, never byte" disclosure (summary.txt line 5) is therefore not empirically
discriminated by this input, though it is consistent. [INFERENCE] The frozen data cannot discriminate
SHOPPING vs SHOPPING_ADMIN replacement order (their occurrence sets are disjoint), matching the
candidate's own "order is invisible on the frozen profiles" note; order was taken from manifest.json and
generator line 12, not inferred from this census. The census covers only __REDDIT__ on the frozen
812-task file under the three pinned profiles; it says nothing about task validity, scoring, runtime
configs or any other round-29 claim.

VERDICT: PASS

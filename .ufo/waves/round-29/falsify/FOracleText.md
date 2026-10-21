writer: KengakuR29-2.FOracleText-2
item: FOracleText — independent oracle attack on C1's integrated projection output (round 29)

## Godspeed axes
1. oracle independence (never read/import production source), 2. diff coverage (all 2436 records × all fields, not totals), 3. evidence exactness (files/lines/commands/units), 4. zero-scope-harm (read-only leaf).

## Attack method and independence
- I did NOT read or import `plans/config_projection.py`. Production source was never opened; the instrument was only executed (`--summary`, `--json`) and its OUTPUT compared. [OBSERVED]
- Oracle `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FOracleText/oracle.py` (25,916 B, stdlib only, Python 3.14.8) derives everything from: prereg TEXT (`plans/round-29-claims.md`), pinned generator BYTES (`plans/fixtures/r29/generate_test_data.py`), `plans/fixtures/r29/profiles.json`, `plans/fixtures/r28/webarena/config_files/test.raw.json`, `plans/fixtures/r29/manifest.json`.
- Contract re-derivation: regex over generator bytes finds six ordered `raw.replace` steps at lines 11–16, order GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP (e.g. line 11: `raw = raw.replace("__GITLAB__", GITLAB)` — 6 words), `json.loads(raw)` line 20, `enumerate` line 21, filename template `config_files/{idx}.json`. Token/name mapping and profile values come from profiles.json `values`. Manifest self-hash checked against the persisted prereg constant `f6390b92…87bf`; each input digest checked against its manifest record. [OBSERVED]
- Projection: each pinned input read exactly once; per profile the six `str.replace` steps are applied to the serialized raw text in generator order (applied count = occurrences of the token in the step's input text), then `json.loads`. Change detection: my own lockstep recursive leaf walk of parsed-original vs parsed-projected trees with RFC 6901 JSON pointers (`~`/`/` escaped); `path_template` = dotted path with `[]` on iterated arrays, task index excluded; `category`: leaf whose last string segment is in {`start_url`,`url`,`reference_url`} = `url_field`, else `non_url_field` — defined a priori from URL-valued field semantics, not from instrument numbers. Provenance: my own character-level JSON string-literal scanner over the raw text yields literal spans + pointer context; token occurrences searched in the raw slice so offsets are codepoint offsets in the ORIGINAL text. Per-task `would_be_file_sha256` = sha256 of `json.dumps(item, indent=2)` reproducing the generator's per-index `json.dump(item, f, indent=2)`. [OBSERVED]
- Domain boundary: offline textual substitution over the three frozen synthetic *.invalid profiles only; upstream code parsed as inert text, never executed; no env/auth/network. Decoded-leaf rewriting used only as a cross-check: on all 1416 changed leaves × 3 profiles the decoded-leaf rewrite equals the text-level sequential replacement (1416/1416/1416), so text-view and leaf-view agree inside this frozen benign domain; quote/backslash and later-token-cascade hand cases remain outside this equivalence claim, consistent with the prereg's disclosure duty. [OBSERVED]

## Commands executed (all exits observed)
- `python3 plans/config_projection.py --summary` → exit 0 (6,914 B stdout, 0 B stderr)
- `python3 plans/config_projection.py --json > instrument-json.json` → exit 0 (3,881,050 B, 0 B stderr)
- `python3 scratch/falsify/FOracleText/oracle.py --json` → exit 0 (5,095,126 B); `oracle findings == []`
- `python3 scratch/falsify/FOracleText/oracle.py --diff instrument-json.json` → exit 1 because 1 disagreement (by design; report below)
All artifacts under `.ufo/waves/round-29/scratch/falsify/FOracleText/`: `oracle.py`, `oracle-json.json`, `instrument-json.json`, `instrument-summary.txt`, `diff-report.txt`. [OBSERVED]

## Compared-object counts (units kept separate)
- task/profile records compared: 2436 (812 × 3) — per record: `output_index`, `output_filename`, `task_id`, `index_equals_task_id`, `would_be_file_sha256` (5 scalar fields = 12,180 comparisons) + deep `projected_task` equality (2436 recursive compares) + `changed_leaves` list equality.
- changed string leaves compared: 4248 (1416 × 3), each on pointer/original/projected/path_template/category + token multiset (25,488 field comparisons).
- occurrence-provenance rows compared: 1435 (token, pointer, codepoint offset, path_template, role, task_index).
- profile metric blocks: 3 × 14 metrics + 3 × 6 steps (name/token/applied).
- hashes/revisions: manifest self, raw text, 3 input digests, 3 projected-text digests, 2436 would-be-file digests, upstream revision = 2445 comparisons. [OBSERVED]

## Agreement result (independent re-derivation vs instrument output)
Full agreement on: population block (input tasks 812, distinct ids 812, projections 2436, tasks-with-any-token 812; occurrences by token 385/336/281/300/0/133; tasks-by-token 204/128/192/182/0/128; roles value 1435; other markers `__last_url__` 65, `__page__` 12; tokens-followed-by-slash 697); index violations 0; all 1435 provenance rows (multiset-identical, including codepoint offsets); per profile parsed 812, string leaves 10,869, changed leaves 1416 (url_field 1355 / non_url_field 61; by template must_include 60, program_html[].url 338, reference_answer_raw_annotation 1, reference_url 205, start_url 812), changed tasks 812, multiple-occurrence leaves 13, by-token leaves 385/323/275/300/0/133, remaining six tokens 0 (text and decoded), projected-text sha256 `2aec098e…c707f4` / `54cf9833…744744b` / `49bbee2e…3e01b2`, steps 385/336/281/300/0/133, junction observations 0/0/697, purposes; all 2436 projected tasks deep-equal; all 2436 would-be-file digests equal; source-contract facts equal (lines 11–16, 20, 21, filename template); manifest/raw/input digests equal. `index==task_id` holds for every one of the 2436 records in my derivation and record-level fields matched instrument output on all of them; task_id lists are identical across the three profiles, so the property is profile-invariant. [OBSERVED]

## Disagreements (complete list — 1)
1. `index_mapping.index_equals_task_id`: oracle 2436 vs instrument 812. Unit divergence, not a factual conflict: I count task/profile records (2436, all true); the instrument reports 812, i.e. input-task units (its population block counts distinct task ids in the same unit). Both datasets agree the property holds on every record (violations empty in both; all 2436 record-level comparisons matched). [INFERENCE] the instrument's intended unit is input tasks — its source may not be read under this item's independence rule. The prereg's own instruction to "distinguish replacement occurrence counts, changed-leaf counts and task counts; do not pool units" (13 words, counted programmatically) makes this a disclosure-worthy reporting-semantics difference, not a projection defect. No wrong value, no wrong task object, no missing exclusion found.

## Notes (presentational, not disagreements)
- Provenance row ORDER differs: instrument is token-major then offset-sorted; mine is document-offset order; multisets identical. [OBSERVED]
- Instrument-only wording fields with no oracle counterpart: `stimulus_class` per profile (3 strings), LIMITS lines. Oracle-only diagnostics with no instrument counterpart: `decoded_leaf_equivalent_changes` (1416 × 3), `followed_by_slash` in provenance rows, `raw_is_ascii` true. [OBSERVED]

## Oracle self-bugs found and fixed during the run (transparency)
1. `proj_tree.values()` tuple-unpack typo (ValueError) — fixed. 2. Stale loop variable used token `__MAP__` instead of the row's token in the scanner/tree cross-check, producing one false `scanner_tree_disagreement` finding — fixed; rerun has zero oracle findings. 3. Initial diff flagged my own oracle-only diagnostic field as a mismatch — reclassified as note. Rerun after fixes is the reported result. [OBSERVED]

## Tooling installs
None. stdlib Python 3.14.8 sufficed; no pacman/uv/cargo/npm transactions performed (host pacman pause respected). [OBSERVED]

## Risks / limits
- The 812-vs-2436 unit divergence cannot be resolved against the instrument's source under this item's independence rule; a maintainer reading the source may confirm the unit in one minute.
- Oracle independence is one-seat: my category/pointer/template conventions were defined a priori and happened to match the instrument's output; a convention I shared by accident with the instrument would not be caught by this design (mitigated by deriving them from field semantics, not from observed numbers).

No blockers. Files changed: only `scratch/falsify/FOracleText/*` (oracle + captured outputs) and this report.

VERDICT: PASS

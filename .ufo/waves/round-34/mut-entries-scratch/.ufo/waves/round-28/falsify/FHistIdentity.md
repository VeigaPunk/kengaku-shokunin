# FHistIdentity — independent 812-ID census replay and audit field comparison

Seat: KengakuR28.FHistIdentity (reviewer, leaf member — no subagents). Round-28 falsification wave.
Scope: independent numeric replay of the pinned `test.raw.json` (812 distinct IDs 0–811,
duplicate/missing/unexpected accounting, hidden-exclusion check), then read-only `--json` run of
`plans/benchmark_spec_audit.py` compared field-by-field. No import of `benchmark_spec_audit.py` or
`plans/fixtures/r28/benchmark_oracle.py` in my census; no upstream code execution; `-B` (bytecode
disabled). Candidate cross-check: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`
SHA256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` (verified, matches freeze).

## Environment / inputs

- Raw input `plans/fixtures/r28/webarena/config_files/test.raw.json`: 880776 bytes, sha256
  `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`. This matches the value recorded
  inside `plans/fixtures/r28/webarena/manifest.json` (upstream_revision
  `dce04686a56253aefba7b18a4fa0937cf1dc987b`); the audit additionally pins manifest and selection digests.
- `selected-task-ids.json` sha256 `5f7eea2e6868553dbda4d7a4be491b3cbaaeb532f1c44dfb9fb40006ff3ed17a`,
  matching the `SELECTION_SHA256` constant in the audit source.
- Tool installs: none (stdlib `python3` only; `python3 --version` is the system interpreter; pacman untouched).
- Scratch evidence: `.ufo/waves/round-28/scratch/FHistIdentity/` (`census.py`, `census.json`, `audit.json`).

## Method

1. My own census (`scratch/FHistIdentity/census.py`, stdlib `json`/`collections` only) parses the raw
   file directly: ID multiset accounting (positions, duplicates, missing vs `range(812)`, unexpected),
   eval-type set AND ordered histograms, site-set histogram, (sorted sites × sorted eval-types) strata
   with per-stratum minimum and first-16 lexicographic selection, login/reset flags, string operator
   keys, url rules, program_html target count, html operators (exact_match precedence — replicated
   rule), locator classes, target URL classes, malformed-`func` URL and empty-`|OR|`-alternative probes.
2. `python3 -B plans/benchmark_spec_audit.py --json > scratch/FHistIdentity/audit.json` (read-only;
   the tool only reads fixtures and prints). Compared every metrics field, all three ID lists, the
   selected-ID list, findings, and all 812 per-task records including `raw_task` equality.

## Exact commands and observed outputs

```
$ python3 -B .ufo/waves/round-28/scratch/FHistIdentity/census.py .ufo/waves/round-28/scratch/FHistIdentity/census.json
WROTE .ufo/waves/round-28/scratch/FHistIdentity/census.json
task_count=812 distinct=812 min=0 max=811 dup=0 missing=0 unexpected=0 exact0811=True
eval_type_sets={'program_html': 282, 'program_html,url_match': 129, 'string_match': 325,
                'string_match,url_match': 10, 'url_match': 66}
strata=27 selected=[389, 590, 132, 173, 44, 552, 681, 791, 556, 356, 7, 377, 759, 424, 97, 399]
string_ops={'exact_match': 45, 'fuzzy_match': 118, 'must_include': 176} targets=651
html_ops={'exact_match': 188, 'must_include': 463} locators={'full_page': 105, 'helper': 22, 'javascript': 524}
url_classes={'helper': 75, 'last': 238, 'navigation': 338}
login={'true': 812} reset={'false': 812} url_rules={'GOLD in PRED': 205}
```

```
$ python3 -B plans/benchmark_spec_audit.py --json > .ufo/waves/round-28/scratch/FHistIdentity/audit.json
audit_exit=0
```

Field diff (19 comparisons, exact-equality including nested dicts):

```
AGREE task_count=812  distinct_task_ids=812  site_eval_strata=27  selected_count=16
AGREE program_html_targets=651
AGREE eval_type_sets {program_html:282, program_html,url_match:129, string_match:325, string_match,url_match:10, url_match:66}
AGREE eval_type_orders (identical; ordered forms surface url_match,program_html:129)
AGREE site_sets {gitlab:180, gitlab,reddit:18, gitlab,wikipedia:6, map:109, map,shopping_admin:2,
                 map,wikipedia:17, reddit:106, reddit,shopping:5, shopping:187, shopping_admin:182}
AGREE login_flags {true:812}  reset_flags {false:812}
AGREE string_operators {exact_match:45, fuzzy_match:118, must_include:176}
AGREE url_rules {GOLD in PRED:205}   html_operators {exact_match:188, must_include:463}
AGREE locator_classes {full_page:105, helper:22, javascript:524}
AGREE target_url_classes {helper:75, last:238, navigation:338}
AGREE selected_task_ids [389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399]
AGREE duplicate_task_ids []  missing_task_ids []  unexpected_task_ids []
MISMATCHES 0
findings []   tasks_records 812   schema_statuses {SCHEMA_COMPATIBLE: 812}
```

Per-record fidelity check (hidden exclusion / silent drop / reorder probe):

```
record_mismatches: []
records: 812  all raw_task preserved: True
record_order_is_file_order: True   # tasks[i].task_id == i for all i; audit preserves file order
persisted selection == audit selection == my selection (all three equal)
```

Independently derived probes that also came back empty in my census:
`non_int_task_id_positions=[]`, `empty_url_alternative_positions=[]`, `unsupported_locators=[]`,
`malformed_func_urls=[]`, `targets_with_both_ops=[]` (no target carries both exact_match and
must_include, so the precedence rule is never exercised on this population),
`na_fuzzy_without_string_note=0`. Audit `findings: []` is consistent with all of these.

## Candidate cross-check (`webarena-task-spec-audit.md`, frozen bytes)

Candidate's "Observed static inventory" table vs my replay: 812/812 IDs 0–811 no
missing/duplicate/unexpected ✓; five evaluator-type sets with the same five counts (325/282/66/10/129) ✓;
27 strata / 16 cases ✓ and the persisted 16 IDs listed in candidate order equal my strata minimums ✓;
string operators 45/176/118 ✓; 651 targets = 188 exact + 463 must_include ✓; locator 105/524/22 ✓;
target URL classes 238/338/75 ✓; "schema findings 0" ✓ (audit exit 0, empty findings).
Internal sums verified: eval sets sum 812; site sets sum 812; url_rules 205 = 66+10+129 tasks;
locators sum 651; url classes sum 651. All candidate numbers in scope reproduce exactly.

## Findings

- **None blocking.** Zero field mismatches between my independent census and the delivered audit;
  zero record-level losses; ID accounting exact (0–811 complete, no duplicates/extras).
- **Observation (accurate but silent in the inventory surface):** `reset_flags {false: 812}` and
  `login_flags {true: 812}` mean every pinned task requires login and none requires reset. The
  numbers are emitted correctly in `--json` and agree with my replay, but `--summary` does not print
  flag histograms and the candidate prose never states the uniform reset=false/login=true facts.
  Not a defect under the claim's contract (flags are inventoried, not interpreted); noted for L1's
  prose decision only.
- **Residual risk:** (a) my census shares the same `json.load` representation as the audit, so a
  hypothetical duplicate JSON object key inside a task object would be invisible to both; the raw
  file is pinned by sha256 so the risk is representational only. (b) `classify_locator` and the
  exact_match-precedence rule are replicated from the audit text — agreement proves the audit is
  self-consistent and matches the candidate, not that the upstream scorer semantics are identical
  (explicitly disclaimed by the audit itself). (c) Stratum-key lexicographic ordering was verified
  only by equality of the emitted selection with both the persisted file and my own sort.

## Tooling

No installs or updates. `python3` (system stdlib only), `-B` to keep bytecode disabled. All writes
confined to `.ufo/waves/round-28/scratch/FHistIdentity/` and this report. Production untouched.

VERDICT: PASS

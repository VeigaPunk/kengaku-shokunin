# FHistEvalTypes — independent evaluator-type-set histogram replay

Seat: `KengakuR28.FHistEvalTypes` (falsify wave, round 28). Scope: independent numeric
replay of the complete `eval_type_sets` / `eval_type_orders` histogram, distinguishing
multi-type combinations from the 3 atomic types, then field-by-field comparison with
`benchmark_spec_audit.py --json` and the frozen candidate's table.

## Inputs

- Raw: `plans/fixtures/r28/webarena/config_files/test.raw.json` (880,776 bytes).
  Observed SHA-256 `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`
  — byte-identical to `plans/fixtures/r28/webarena/manifest.json` pin
  (`files["config_files/test.raw.json"].sha256`, upstream revision `dce04686…` 2025-11-26).
- Candidate audited: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`,
  observed SHA-256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8`
  — matches the frozen hash in the assignment. Canonical
  `corpus/knowledge/webarena-task-spec-audit.md` does not exist (verified: `ls` →
  "No such file or directory"), consistent with not-yet-admitted.

## Exact commands and observed outputs

### Independent stdlib census (no oracle import)

Script: `.ufo/waves/round-28/scratch/FHistEvalTypes/census.py` (pure stdlib
`json`/`collections`/`hashlib`; derives all grouping rules from the raw JSON alone —
it does not import `benchmark_spec_audit.py` or `benchmark_oracle.py`).

```
$ python3 .ufo/waves/round-28/scratch/FHistEvalTypes/census.py
raw_sha256 7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652
task_count 812 top_level_type list
== eval_type_sets (sorted-set key) ==
  'program_html': 282
  'program_html,url_match': 129
  'string_match': 325
  'string_match,url_match': 10
  'url_match': 66
distinct_eval_type_sets 5 ; sum_sets 812
== eval_type_orders (declared-order key) ==
  'program_html': 282 ; 'string_match': 325 ; 'string_match,url_match': 10
  'url_match': 66 ; 'url_match,program_html': 129
distinct_eval_type_orders 5
== atomic membership ==
  program_html: 411 ; string_match: 335 ; url_match: 205
== combination vs single ==
  single_type_tasks=673 combination_tasks=139 empty_set_tasks=0
distinct_(sorted_sites,sorted_evaltypes)_strata 27
anomaly_count 0 ; missing_eval_field []
```
(Full stdout: `.ufo/waves/round-28/scratch/FHistEvalTypes/census.out.txt`.)

### Second independent implementation (jq, no Python oracle)

```
$ jq -r '[.[].eval.eval_types | sort | join(",")] | group_by(.) | map({key: .[0], n: length})' \
    plans/fixtures/r28/webarena/config_files/test.raw.json
[{"key":"program_html","n":282},{"key":"program_html,url_match","n":129},
 {"key":"string_match","n":325},{"key":"string_match,url_match","n":10},
 {"key":"url_match","n":66}]
$ jq -r '[.[].eval.eval_types | join(",")] | group_by(.) | map({key: .[0], n: length})' …
[{"key":"program_html","n":282},{"key":"string_match","n":325},
 {"key":"string_match,url_match","n":10},{"key":"url_match","n":66},
 {"key":"url_match,program_html","n":129}]
$ jq -r '[.[].eval.eval_types[] | type] | unique' …            → ["string"]
$ jq -r '[.[].eval.eval_types[]] | unique' …                   → ["program_html","string_match","url_match"]
$ jq -r '[.[] | select((.eval.eval_types|unique|length) < (.eval.eval_types|length))]|length' → 0
$ jq -r '[.[] | select(.eval == null)] | length' …             → 0
$ jq -r '[.[] | select(.eval.eval_types == null or (.eval.eval_types|length)==0)]|length' → 0
$ jq -r '[.[].eval.eval_types | length] | group_by(.) | map({size:.[0],n:length})' …
  → [{size:1, n:673},{size:2, n:139}]
```
(Full stdout: `.ufo/waves/round-28/scratch/FHistEvalTypes/jq.out.txt`. jq = jaq 3.1.1.)

### Instrument under test (read-only run)

```
$ python3 plans/benchmark_spec_audit.py --json > …/scratch/FHistEvalTypes/audit.json ; exit=0
metrics.eval_type_sets  = {"program_html":282,"program_html,url_match":129,
                           "string_match":325,"string_match,url_match":10,"url_match":66}
metrics.eval_type_orders= {"program_html":282,"string_match":325,
                           "string_match,url_match":10,"url_match":66,
                           "url_match,program_html":129}
task_count=812 distinct_task_ids=812 site_eval_strata=27 selected_count=16
program_html_targets=651 findings=[] 
selected_task_ids=[389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399]
```

## Comparison result — every relevant field

| field | independent stdlib | independent jq | audit --json | agreement |
|---|---|---|---|---|
| eval_type_sets (5 keys, counts) | identical | identical | identical | YES |
| eval_type_orders (5 keys, counts) | identical | identical | identical | YES |
| task_count / set-histogram sum | 812 / 812 | 812 | 812 | YES |
| site_eval_strata | 27 (derived from scratch) | — | 27 | YES |
| combination task IDs (139) | min-per-stratum list reproduced | — | selected 16 = first-16 stratum mins | YES |

Every one of the 27 stratum minimums from my own census matches `selected_task_ids`
truncated to 16 (sorted strata, per-stratum min ID), consistent with the
sort-(sorted-site-set, sorted-eval-type-set) rule in `plans/round-28-claims.md`.

## Combination vs atomic distinction (my added axis)

- Atomic-only tasks: 673. Combination tasks: 139, exhaustively
  `task_ids 173–182` (`string_match,url_match` ×10) and `590–699,805–809`
  (`url_match,program_html` ×129). No triples; no empty/invalid/duplicate/unknown
  `eval_types` anywhere in the 812 rows.
- Membership counts: `string_match` ∈335 tasks, `url_match` ∈205, `program_html` ∈411;
  memberships sum to 951 = 673·1 + 139·2 (closed under pair combinations).
- All 129 `program_html+url_match` tasks declare order `["url_match","program_html"]`
  (verified: 129 tasks where declared order ≠ sorted order). So the sorted-label set
  histogram and the declared-order histogram genuinely differ in key spelling while
  agreeing in count — the candidate's "sorted labels for grouping; ordered histograms
  preserve execution order" is literally true and material (composite executes in
  list order per S062:348–352,361–374; here url_match runs before program_html).

## Candidate cross-check (frozen bytes, SHA-256 above)

- Table line 102: `string_match325, program_html282, url_match66,
  string_match+url_match10, program_html+url_match129` — all five values match the
  replayed histogram exactly; "+" spelling maps to sorted-set keys.
- Line 103: `27 /16` strata/selected — matches.
- Line 105: `651` page-content targets — independently recounted
  (Σ len(program_html) where declared) = 651 — matches `program_html_targets`.
- Line 107: `schema findings 0` — audit `findings=[]`, exit 0 — matches.
- Line 58/persisted IDs — match my independently derived stratum minimums.
- C1 context claim "5 evaluator-type sets" — matches `distinct_eval_type_sets 5`.

## Residual notes (not defects on pinned input)

1. `audit_tasks` increments `counts["eval_type_sets"]`/`["eval_type_orders"]`
   unconditionally (line 84–85) even when `eval_types` fails validation, unlike
   `site_sets` guarded by `sites_ok` — a malformed row could add a phantom "" bucket
   on other inputs. On the pinned population this path is unreachable (0 anomalies),
   so all published counters are exact.
2. `eval_type_orders` is emitted in `--json` but not printed by the default
   human-readable summary; numeric content identical either way.
3. Agreement is author-side independent implementation (two fresh derivations vs the
   instrument), not outside closure — as scoped.

## Verification performed

Own lane allowed probes only: stdlib census script, jq pipelines, read-only
`benchmark_spec_audit.py --json` (no imports, no upstream code, no mutations of
production/fixtures/lane state). Scratch artifacts:
`.ufo/waves/round-28/scratch/FHistEvalTypes/{census.py,census.out.txt,jq.out.txt,audit.json}`.
No tools installed; no installs needed (python3 stdlib + existing jaq 3.1.1).

## Finding

No defect found in scope. The complete evaluator-type-set histogram
(`string_match`325, `program_html`282, `url_match`66, `string_match+url_match`10,
`program_html+url_match`129; 5 distinct sets summing to 812; 673 single-type vs 139
combination tasks; 5 distinct declared orders; 27 site/evaluator strata) is exactly
reproduced by two independent replays and matches every candidate mention.

VERDICT: PASS

# FHistSelection — independent numeric replay of the first-16 stratum minimum-ID vector

Seat: KengakuR28.FHistSelection · Wave: round-28 falsification · Date: 2026-10-21
Scope: exact ordered vector `first16 lexicographic (sorted site-set, sorted eval-type-set)
strata → minimum task_id`, plus every adjacent metric the candidate quotes. No random or
representative inference. Author-side independent implementation only; no production edits.

## Inputs re-read

- Draft under review: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`
  `sha256 = 77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` — matches the
  frozen hash in the wave goal. Canonical path `corpus/knowledge/webarena-task-spec-audit.md`
  is still **absent** (not admitted).
- Raw input: `plans/fixtures/r28/webarena/config_files/test.raw.json`
  `sha256 = 7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` — matches
  `manifest.json` pinned entry.
- Persisted selection: `plans/fixtures/r28/webarena/selected-task-ids.json`
  `sha256 = 5f7eea2e6868553dbda4d7a4be491b3cbaaeb532f1c44dfb9fb40006ff3ed17a` — matches the
  script's `SELECTION_SHA256` constant.
- Selection rule (claims line 19): "form (sorted site set, sorted evaluator-type set), sort
  the tuples lexicographically, take minimum task_id from each, retain first16 groups."

## Method — two independently written implementations, zero shared code

1. `scratch/FHistSelection/independent_census.py` — stdlib `json`/`collections` only;
   stratum predicate, gating, and counters re-derived from the claims prose, NOT copied
   from `benchmark_spec_audit.py` or `benchmark_oracle.py` (neither was opened or imported).
2. Pure `jaq 3.1.1` pipeline — a third-party jq implementation, a disjoint code path:
   `group_by` on `[sites|sort, eval_types|sort]`, `sort_by`, `[.[].sid]|min`.

Command 1 (stdlib census):
```
PYTHONDONTWRITEBYTECODE=1 python3 .ufo/waves/round-28/scratch/FHistSelection/independent_census.py \
  > .ufo/waves/round-28/scratch/FHistSelection/census.json
```
Command 2 (jaq):
```
jq -n --rawfile j plans/fixtures/r28/webarena/config_files/test.raw.json '
  ($j|fromjson) as $t
  | [ $t[] | {sid:.task_id, key:[(.sites|sort), (.eval.eval_types|sort)]} ]
  | group_by(.key) | sort_by(.[0].key)
  | {n_strata:length, first16_mins:[.[0:16][]|[.[].sid]|min], all27_mins:[.[]|[.[].sid]|min]}'
```
Command 3 (audit, read-only):
```
PYTHONDONTWRITEBYTECODE=1 python3 plans/benchmark_spec_audit.py --json  # exit=0
PYTHONDONTWRITEBYTECODE=1 python3 plans/benchmark_spec_audit.py --summary  # exit=0
```

## Observed outputs — the vector itself

All three derivations (stdlib census, jaq group_by, `audit --json.selected_task_ids`)
return the identical ordered vector:

```
[389, 590, 132, 173, 44, 552, 681, 791, 556, 356, 7, 377, 759, 424, 97, 399]
```

This equals (a) `selected-task-ids.json` verbatim, (b) candidate line 60's persisted list,
(c) claims line 19's list. The complete 27-minimum vector is also reproduced identically:
`…, 399, 595, 27, 671, 118, 653, 21, 158, 423, 676, 0, 157` — strata count 27, so the
`first16` truncation is a real cut (11 strata excluded), not a trivial identity.

## Member-set verification (min actually attained, not assumed)

Complete member ID sets were enumerated per stratum; every claimed minimum is the true
minimum of the full member list, not a sampled value:

| stratum (sorted key) | size | claimed min | observed min |
|---|---|---|---|
| gitlab / program_html | 88 | 389 | 389 |
| gitlab / program_html,url_match | 23 | 590 | 590 |
| gitlab / string_match | 43 | 132 | 132 |
| gitlab / string_match,url_match | 10 | 173 | 173 |
| gitlab / url_match | 16 | 44 | 44 |
| gitlab,reddit / program_html | 9 | 552 | 552 |
| gitlab,reddit / program_html,url_match | 8 | 681 | 681 |
| gitlab,reddit / string_match | 1 | 791 | 791 |
| gitlab,wikipedia / program_html | 6 | 556 | 556 |
| map / program_html | 15 | 356 | 356 |
| map / string_match | 89 | 7 | 7 |
| map / url_match | 5 | 377 | 377 |
| map,shopping_admin / program_html | 2 | 759 | 759 |
| map,wikipedia / program_html | 12 | 424 | 424 |
| map,wikipedia / string_match | 5 | 97 | 97 |
| reddit / program_html | 37 | 399 | 399 |

Lexicographic edge cases exercised and consistent across implementations: prefix ordering
(`["gitlab"],["program_html"]` before `["gitlab"],["program_html","url_match"]`), and
`"map,shopping_admin"` sorts under `"map"` — task 759's stratum sits inside the first 16
while all pure-`shopping` strata fall at positions 20+. Confirmed: 192 tasks carry the
`shopping` site; none is selected — candidate's "shopping site is omitted" holds.

## Field-by-field comparison (independent census vs `audit --json`)

```
selection_vector_equal true   task_count true (812)      distinct_task_ids true (812)
site_eval_strata true (27)    selected_count true (16)   program_html_targets true (651)
eval_type_sets true           eval_type_orders true      site_sets true
string_operators true         url_rules true             html_operators true
locator_classes true          target_url_classes true    login_flags true (812×true)
reset_flags true (812×false)  missing/duplicate/unexpected_ids empty; findings [] empty
```

Concretely the agreed counters are: eval_type_sets `{program_html:282,
program_html,url_match:129, string_match:325, string_match,url_match:10, url_match:66}`;
eval_type_orders `{program_html:282, string_match:325, string_match,url_match:10,
url_match:66, url_match,program_html:129}` (order differs from set only in the
url_match,program_html group); site_sets `{gitlab:180, gitlab,reddit:18,
gitlab,wikipedia:6, map:109, map,shopping_admin:2, map,wikipedia:17, reddit:106,
reddit,shopping:5, shopping:187, shopping_admin:182}`; string_operators
`{exact_match:45, fuzzy_match:118, must_include:176}`; html_operators
`{exact_match:188, must_include:463}`; locator_classes `{full_page:105, helper:22,
javascript:524}`; target_url_classes `{helper:75, last:238, navigation:338}`;
url_rules `{GOLD in PRED:205}`. Every figure in the candidate's observed-inventory table
(lines 99–108) reproduces exactly.

## Silent-exclusion probes (would a malformed task be dropped from stratification?)

jq probes over all 812 tasks: 0 non-integer task_ids, 0 boolean ids, 0 bad `sites`, 0
non-object `eval`, 0 bad `eval_types` lists, 0 duplicate eval_types, 0 eval_types outside
the known set, 0 non-bool require_login/require_reset, 0 empty intents. Stratification
excludes nothing — the 27-stratum partition covers the full population, so the vector is
a census artifact, not a filtered subset.

## Receipt cross-checks

- `corpus/evidence/round28-calibration/build-acceptance/audit-current.stdout` is
  **byte-identical** (cmp, 1,787,838 bytes) to my fresh `--json` run — the candidate's
  "working-tree measurement" is reproducible bit-for-bit.
- `corpus/evidence/round28-calibration/audit-summary.txt` equals my `--summary` output
  modulo a trailing `exit=0` echo line in the stored receipt (capture artifact, content
  identical).
- `plans/fixtures/r28/benchmark_oracle.py` was not opened, imported, or executed;
  agreement here is genuine independent-author replay.

## Findings

None against the numeric claims. The ordered vector, all 27 stratum minimums, stratum
sizes, member sets, site/evaluator histograms, and every candidate-quoted counter are
exactly reproduced by two disjoint implementations and byte-identical stored receipts.

Residual observations (non-numeric, informational):
1. The candidate cites receipt `build-acceptance/audit-current.stdout` without its
   `corpus/evidence/round28-calibration/` prefix; a lane-root `build-acceptance/` does
   not exist. Path is resolvable only as relative to the first receipt's directory.
   Trivial citation ambiguity, not a defect.
2. Candidate text "the shopping site is omitted" is literally true for the `shopping`
   site-set but task 759's stratum is `map,shopping_admin` — `shopping_admin` does appear
   in the selection. The phrasing is accurate as written; only worth noting so no reader
   generalizes it to all shopping-related site sets.
3. Ordering semantics verified only over string tuples where Python tuple sort and jaq
   array sort coincide; both are element-wise lexicographic, so the claim "lexicographic"
   is faithfully implemented.

## VERDICT: PASS

Independent author-side replay reproduces the exact ordered 16-ID vector, the full
27-stratum minimum sequence, and every adjacent metric; `audit --json` reruns are
deterministic and byte-identical to stored receipts. No falsification survives on this
slice. Canonical candidate `corpus/knowledge/webarena-task-spec-audit.md` remains
unadmitted; the reviewed bytes are the frozen draft at the SHA256 above.

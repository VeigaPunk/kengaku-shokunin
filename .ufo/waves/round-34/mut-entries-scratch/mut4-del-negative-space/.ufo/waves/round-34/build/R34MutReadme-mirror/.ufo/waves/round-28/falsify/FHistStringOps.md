# FHistStringOps — independent replay: string-match operator denominators and N/A branch counts

Seat: `KengakuR28.FHistStringOps` (reviewer, falsification wave 64). Date 2026-10-21.
Scope: task-count denominators for `exact_match`/`must_include`/`fuzzy_match` and N/A
conditional branch counts in `plans/fixtures/r28/webarena/config_files/test.raw.json`,
replayed independently, then compared against `python3 plans/benchmark_spec_audit.py --json`
and the frozen candidate `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`
(SHA256 77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8).

## Method

Independent census: `.ufo/waves/round-28/scratch/FHistStringOps/census.py` — stdlib
`json`/`hashlib`/`collections` only. It does NOT import `benchmark_spec_audit.py`,
`benchmark_oracle.py`, or any upstream webarena code; the raw JSON is parsed as data.
A second independent implementation path used `jaq 3.1.1` (jq-compatible) filters on
the same bytes. Commands and outputs below; full evidence in
`.ufo/waves/round-28/scratch/FHistStringOps/census.json` and `census.stdout`/`audit.json`.

## Exact commands and observed outputs

Input identity (matches `manifest.json` `config_files/test.raw.json`):

```
$ sha256sum plans/fixtures/r28/webarena/config_files/test.raw.json
7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652   (880776-byte file per manifest)
```

Own census (`PYTHONDONTWRITEBYTECODE=1 python3 .ufo/waves/round-28/scratch/FHistStringOps/census.py`):

```
task_count 812
string_match_tasks 335
tasks_with_exact_match 45
tasks_with_must_include 176
tasks_with_fuzzy_match 118
other_reference_answer_operators {}
reference_answer_keysets {'exact_match': 45, 'fuzzy_match': 114, 'fuzzy_match/must_include': 4, 'must_include': 172}
na_branch_tasks_total 36 distinct 36
na_by_operator {'fuzzy_match': 36}
fuzzy_na_keysets {'fuzzy_match': 36}
fuzzy_na_with_sibling_operators []
fuzzy_non_na 82
fuzzy_value_types {'list': 82, 'str': 36}
operator_cooccurrence {'exact_match': 45, 'fuzzy_match': 114, 'fuzzy_match/must_include': 4, 'must_include': 172}
```

Denominator edge cases (stdlib probe):

```
reference_answers w/o string_match: []
string_match w/o reference_answers: []
N/A inside list values: []
string_match combined with other eval types: [173..182]   (10 tasks, string_match+url_match set)
```

Audit replay (`python3 plans/benchmark_spec_audit.py --json`, exit=0, findings=0):

```
metrics.string_operators: {'exact_match': 45, 'fuzzy_match': 118, 'must_include': 176}
audit records fuzzy_match=="N/A" tasks: 36  (ids begin 22, 24, 101, 115, 166 ...)
audit N/A keysets: {('fuzzy_match',)}
metrics.eval_type_sets: {'string_match': 325, 'string_match,url_match': 10, ...}  -> 335 string tasks, agrees
```

Second parser (jaq 3.1.1) on the same bytes:

```
grouped operator keys over string_match tasks: exact_match 45, fuzzy_match 118, must_include 176
count(.eval.reference_answers.fuzzy_match == "N/A") = 36
unique keysets of those tasks = [["fuzzy_match"]]
```

## Findings vs audit --json and candidate

| quantity | my census | audit --json | candidate claim | verdict |
|---|---|---|---|---|
| tasks with `exact_match` key | 45 | `string_operators.exact_match` 45 | "exact_match45" (:104) | agree |
| tasks with `must_include` key | 176 | `string_operators.must_include` 176 | "must_include176" (:104) | agree |
| tasks with `fuzzy_match` key | 118 | `string_operators.fuzzy_match` 118 | "fuzzy_match118" (:104) | agree |
| "operators can coexist" (:104) | 4 tasks declare fuzzy_match+must_include; total 339 operator declarations / 335 string tasks | same counters (per-key increments) | explicit coexistence note | agree, candidate is not misleading |
| N/A conditional branch | 36 tasks, all `fuzzy_match`, all sole key | 36 records, sole keyset {fuzzy_match} | :47–48 "all N/A tasks in the pinned population use only that approach" | agree — verbatim verified |
| string_match task denominator | 335 (325 sole + 10 with url_match) | eval_type_sets 325+10 | not explicitly stated; consistent with :102 | consistent |

Notes, not defects:

- The audit counts `reference_answers` keys only when `eval_types` contains
  `string_match`; the edge-case probe shows no task declares `reference_answers`
  without `string_match` and none declares `string_match` without
  `reference_answers`, so no silent denominator exclusion exists in this population.
- No task carries `N/A` as a list element under any operator; all 36 N/A values are
  the bare string under `fuzzy_match` with no sibling operator, so the exact-N/A
  bypass branch (S062:152–163) is the only scored path for those 36 tasks —
  matching the candidate's "only that approach" claim.
- `metrics` does not emit a standalone N/A counter; the N/A population is carried
  in per-task records and the `na_fallback` scorer-contract fact. Candidate prose
  is the aggregation layer here and its claim is exactly supported.
- Tasks 173–182 (10 tasks) carry `string_match` alongside `url_match`; both the
  census and audit include them in the 335 denominator — no drift.

No numeric disagreement found. Author-side independent implementation agrees on
every in-scope field; this is author-side agreement, not outside closure.

VERDICT: PASS

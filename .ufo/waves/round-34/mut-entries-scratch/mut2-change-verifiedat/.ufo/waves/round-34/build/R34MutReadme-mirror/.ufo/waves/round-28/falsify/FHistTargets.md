# FHistTargets — independent numeric replay of program_html target/task counts

Seat: `KengakuR28.FHistTargets` (falsifier, author-side). Date: 2026-10-21.
Scope: replay every `program_html` target count and task count in `plans/benchmark_spec_audit.py`
against `plans/fixtures/r28/webarena/config_files/test.raw.json` (880,776 B) with an independent
stdlib implementation; verify target conjunction/branch precedence; then diff read-only `--json`
output. No production or oracle code was imported or executed other than the assigned read-only
`--json` run. Bytecode disabled (`PYTHONDONTWRITEBYTECODE=1 python3 -B`) on every invocation.

## Method and independence

- Own census: `.ufo/waves/round-28/scratch/FHistTargets/independent_census.py` — a fresh stdlib-only
  script (`json`/`collections`/`functools`) written from the raw JSON and from the pinned upstream
  semantics in `evaluation_harness/evaluators.py` read as data. It does **not** import
  `plans/benchmark_spec_audit.py` or `plans/fixtures/r28/benchmark_oracle.py`. Selection order was
  re-implemented with a hand-rolled element-wise lexicographic comparator (`cmp_tuples`), not the
  production `sorted(strata.items())`.
- Second oracle: one-shot `jaq 3.1.1` pipelines against the same bytes
  (`.ufo/waves/round-28/scratch/FHistTargets/jq-crosscheck.txt`).
- Production comparator: `python3 -B plans/benchmark_spec_audit.py --json` exit 0, stdout captured
  to `scratch/FHistTargets/audit-json.stdout` (1,787,838 B), stderr empty. Read-only by inspection
  of `main()`: parse → `read_snapshot` (hash-verify fixtures, in-memory `audit_tasks`) → print.
- Input identity re-verified: `sha256sum` of `test.raw.json` =
  `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`, equal to
  `manifest.json` `files["config_files/test.raw.json"].sha256`; manifest =
  `c78b1478…23a6dd`, selected-task-ids.json = `5f7eea2e…d17a`, matching the constants the
  instrument pins. `upstream_revision` = `dce04686a56253aefba7b18a4fa0937cf1dc987b`.

## Exact commands

```
PYTHONDONTWRITEBYTECODE=1 python3 -B .ufo/waves/round-28/scratch/FHistTargets/independent_census.py
    > scratch/FHistTargets/independent-census.json        # exit 0
PYTHONDONTWRITEBYTECODE=1 python3 -B plans/benchmark_spec_audit.py --json
    > scratch/FHistTargets/audit-json.stdout              # exit 0
jq '.metrics, .findings, .selected_task_ids, …' audit-json.stdout
jq '[.[] | select(.eval.eval_types | index("program_html")) | .eval.program_html | length] | add' test.raw.json
# plus per-class jq selects recorded in scratch/FHistTargets/jq-crosscheck.txt
```

## Observed outputs — three implementations agree on every field

| metric | my census | `jaq` | audit `--json` | verdict |
|---|---|---|---|---|
| task_count | 812 | 812 | 812 | match |
| distinct_task_ids / id range | 812 / 0–811, no missing/duplicate/unexpected | — | 812, lists empty | match |
| tasks declaring `program_html` | 411 (282 sole + 129 with url_match) | 411 | 411 implied by sets 282+129 | match |
| `program_html_targets` total | 651 | 651 | 651 | match |
| tasks w/o type but non-empty list | 0 | 0 | (none possible; findings empty) | match |
| eval_type_sets | program_html 282, program_html+url_match 129, string_match 325, string_match+url_match 10, url_match 66 | — | identical | match |
| eval_type_orders | identical 5-entry histogram incl. order `url_match,program_html` 129 | — | identical | match |
| target_url_classes | last 238, navigation 338, helper 75 | 238 / 338 / 75 | identical | match |
| locator_classes | full_page 105, javascript 524, helper 22 | 105 / 524 / 22 | identical | match |
| html_operators (effective) | exact_match 188, must_include 463 | 188 / 463 | identical | match |
| required_contents key shapes | both keys 0, neither key 0, non-dict 0 | group_by: only `{exact_match}`×188 + `{must_include}`×463 | (findings empty) | match |
| string_operators | exact_match 45, must_include 176, fuzzy_match 118 | — | identical | match |
| url_rules | `GOLD in PRED` 205 | — | identical | match |
| site_sets (9) / login / reset | identical / true 812 / false 812 | — | identical | match |
| site_eval_strata / selection | 27 / min-id list = [389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399] = `selected-task-ids.json` | — | 27 / same 16 IDs | match |
| findings | no anomalies (own schema walk) | — | `[]` | match |

Per-task replay (own diff loop over production `tasks[]` vs raw JSON, all 812):
`raw_task` byte-equal in every record; `task_id`, `eval_types`, `reference_answers`,
`reference_approach_order`, and `program_html` echoes all exact — 0 diffs; all 812 records
`SCHEMA_COMPATIBLE`; production per-task `len(program_html)` histogram equals my own
`{1:291, 2:57, 3:44, 4:2, 5:9, 6:2, 7:3, 8:1, 10:2}` (sums to 411 tasks / 651 targets; min 1, max 10).

## Target conjunction / branch precedence — verified against pinned source

Read `evaluators.py:244-333` (HTMLContentEvaluator) as data:

- **Targets are ANDed**: `score = 1.0`, per-target `score *=` (`:261,:310,:327`). My census
  re-derives this contract; the audit counts targets per task without flattening them — consistent.
- **`exact_match` precedes `must_include`**: source uses `if "exact_match" in … elif "must_include"
  in …` (`:305/:312`). The instrument's `operator = "exact_match" if "exact_match" in required else
  "must_include" if …` is a faithful mirror. Verified non-vacuous hazard-free: the population
  contains **0** targets with both keys and **0** with neither, so precedence order cannot
  misattribute any emitted count (188+463=651 covers all targets).
- **`must_include` semantics**: elements ANDed, each element's `" |OR| "`-split alternatives ORed
  (`:315-327`). Own census (not an emitted production field): 815 `must_include` elements across the
  463 targets, 5 elements carrying `|OR|` (11 alternatives) — tasks {431,750,751,755,756}, none in
  the selected 16; consistent with the candidate's claim that the sample omits OR-alternative checks.
- **`prep_actions`**: 10 targets in tasks {699–703}, none in the selected 16 — consistent with
  "omits … preparation actions".
- **URL class**: `== "last"` skips navigation; `startswith("func")` is the helper/`eval` branch
  (`:263-266,:271`); else `goto`. Both instrument and my census classify identically;
  0 malformed `func`-without-colon URLs observed.
- **Locator class**: `""`→full page (`:276`), `document.`/`[...document.`→JS (`:279-280`),
  `func:`→helper (`:296`), else `raise` — matches `classify_locator`; 0 unsupported/invalid locators.
- **Composite**: `EvaluatorComb` `score *=` in declared order (`:348-352`) — "targets multiply" in
  the candidate is accurate; 139 two-type tasks all order `url_match` before `program_html`
  (order histogram preserved, not just sorted sets).

## Candidate cross-check (`drafts/webarena-task-spec-audit.md`, SHA256 77e19d5b…20a8 — verified)

Candidate "Observed static inventory" lines 101-107 were rechecked against my replay: 812/812 IDs,
5 eval-type sets {325, 282, 66, 10, 129}, 27 strata, 16 cases, string operators {45,176,118},
651 targets, effective operators 188+463, locators {105,524,22}, url classes {238,338,75},
schema findings 0 — **every figure reproduced exactly**. Case-table claims about omitted
OR-alternatives/prep_actions/helper paths confirmed against population.

## Findings

1. No defect found in scope. All `program_html` target counts, task counts, histograms, selection,
   and per-task echoes reproduce under two independent implementations plus a jq pass.
2. Residual (out of scope, informational): effective-operator assignment is proven faithful to the
   upstream `if/elif` precedence, but the population happens to contain zero both-key targets, so
   precedence errors could not have manifested in this population even if the instrument's order
   were wrong — it isn't; the code reads `exact_match` first exactly like the source.

## Tool installs

None. Used pre-installed `python3 3.14.8` (stdlib only) and `jaq 3.1.1`. No pacman/host changes.

VERDICT: PASS

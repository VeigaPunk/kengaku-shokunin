# FHistSiteSets — independent replay of site-set counts and site/evaluator strata

Seat: KengakuR28.FHistSiteSets (author-side falsifier, leaf). Scope: site-set
histogram, 27 (sorted site set, sorted evaluator-type set) strata, deterministic
16-task selection, selected-sample shopping omission. Read-only over production;
no upstream code executed; `benchmark_spec_audit.py` and `benchmark_oracle.py`
never imported — my census is a separate stdlib implementation.

## Inputs and digest pinning (all verified before any count)

Command: `sha256sum` over the four pinned files; observed:

- `config_files/test.raw.json` sha256 `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`, 880776 bytes — equals manifest entry.
- `manifest.json` sha256 `c78b1478c5cb18dd7621723023e7ff15342401c72fc04a939a8d4d290323a6dd` — equals `MANIFEST_SHA256` in the instrument.
- `selected-task-ids.json` sha256 `5f7eea2e6868553dbda4d7a4be491b3cbaaeb532f1c44dfb9fb40006ff3ed17a` — equals `SELECTION_SHA256`.
- Frozen candidate `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md` sha256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` — equals the dispatch-pinned value.
- `upstream_revision` dce04686a56253aefba7b18a4fa0937cf1dc987b per manifest.

## Independent implementation (mine)

`.ufo/waves/round-28/scratch/FHistSiteSets/independent_site_census.py` — pure
stdlib `json`/`hashlib`/`collections`; parses `test.raw.json` directly; derives
site tuples, per-site occurrences, eval-type tuples, strata dict with member
task_ids, and replays the selection rule. Full output:
`.ufo/waves/round-28/scratch/FHistSiteSets/census.json`. Command:

```
PYTHONDONTWRITEBYTECODE=1 python3 .ufo/waves/round-28/scratch/FHistSiteSets/independent_site_census.py > .ufo/waves/round-28/scratch/FHistSiteSets/census.json   # exit 0
```

### My observed values

- task_count 812; distinct task_ids 812; IDs 0–811 contiguous (no missing, no duplicates, none outside range).
- **10 distinct site sets, total 812** (no task dropped): gitlab 180 · gitlab,reddit 18 · gitlab,wikipedia 6 · map 109 · map,shopping_admin 2 · map,wikipedia 17 · reddit 106 · reddit,shopping 5 · shopping 187 · shopping_admin 182.
- Per-site occurrences (multi-site tasks counted per site, sum 860 > 812): gitlab 204, map 128, reddit 129, shopping 192, shopping_admin 184, wikipedia 23.
- **5 distinct eval-type sets, total 812**: program_html 282 · program_html,url_match 129 · string_match 325 · string_match,url_match 10 · url_match 66.
- **27 strata, population 812, 0 skipped tasks** — every task has a valid nonempty sites list, valid nonempty eval_types list, and int task_id, so the site-set histogram population equals the strata population.
- Full stratum table (sites + eval_types → size, min task_id):

| sites | eval_types | size | min |
|---|---|---|---|
| gitlab | program_html | 88 | 389 |
| gitlab | program_html,url_match | 23 | 590 |
| gitlab | string_match | 43 | 132 |
| gitlab | string_match,url_match | 10 | 173 |
| gitlab | url_match | 16 | 44 |
| gitlab,reddit | program_html | 9 | 552 |
| gitlab,reddit | program_html,url_match | 8 | 681 |
| gitlab,reddit | string_match | 1 | 791 |
| gitlab,wikipedia | program_html | 6 | 556 |
| map | program_html | 15 | 356 |
| map | string_match | 89 | 7 |
| map | url_match | 5 | 377 |
| map,shopping_admin | program_html | 2 | 759 |
| map,wikipedia | program_html | 12 | 424 |
| map,wikipedia | string_match | 5 | 97 |
| reddit | program_html | 37 | 399 |
| reddit | program_html,url_match | 58 | 595 |
| reddit | string_match | 11 | 27 |
| reddit,shopping | program_html,url_match | 5 | 671 |
| shopping | program_html | 47 | 118 |
| shopping | program_html,url_match | 10 | 653 |
| shopping | string_match | 88 | 21 |
| shopping | url_match | 42 | 158 |
| shopping_admin | program_html | 66 | 423 |
| shopping_admin | program_html,url_match | 25 | 676 |
| shopping_admin | string_match | 88 | 0 |
| shopping_admin | url_match | 3 | 157 |

- Selection replay (lexicographic stratum order, min task_id, first 16): `[389, 590, 132, 173, 44, 552, 681, 791, 556, 356, 7, 377, 759, 424, 97, 399]` — **exactly equals persisted `selected-task-ids.json`**. The 16th stratum (`reddit`/`program_html`, min 399) is the cutoff; `reddit`+`program_html,url_match` (min 595) and all later strata are excluded.
- **Shopping omission confirmed**: sites across the 16 selected tasks = {gitlab, map, reddit, shopping_admin, wikipedia}; `shopping` alone occurs in 0 selected tasks (it would first appear via `reddit,shopping` at stratum 19, min 671). Amendment 1's "selected sample omits the shopping site" is accurate.
- Adjacent replays (same census): require_login = bool True ×812, require_reset = bool False ×812; eval_type raw-order histogram {program_html 282, string_match 325, string_match,url_match 10, url_match 66, url_match,program_html 129} — the 129 composite tasks all declare `url_match` before `program_html` in raw order.

## Comparison command (production audit, read-only)

```
PYTHONDONTWRITEBYTECODE=1 python3 plans/benchmark_spec_audit.py --json > .ufo/waves/round-28/scratch/FHistSiteSets/audit-output.json   # exit 0
```

Observed: `findings: []`; `metrics.task_count 812`, `distinct_task_ids 812`,
`site_eval_strata 27`, `selected_count 16`, `program_html_targets 651`;
`selected_task_ids` identical to my replay; `duplicate/missing/unexpected` all `[]`.

Field-by-field results:

- `metrics.site_sets` = my 10-entry histogram exactly (same keys, same counts).
- `metrics.eval_type_sets` and `metrics.eval_type_orders` = my sorted and raw-order histograms exactly.
- `metrics.login_flags {true:812}` / `reset_flags {false:812}` = my independent flag census.
- **Strata**: audit emits no explicit stratum table, so I rebuilt strata from its own per-task `tasks[]` records (`sorted(r["sites"])`, `sorted(r["eval_types"])`): all 27 groups match my member lists, sizes, and minima field-by-field (`strata_field_by_field_equal: True`), and the audit's selection equals my replay.
- Audit `--json` exit 0 with zero findings; `--summary` line reports consistent totals (task_count=812, site_eval_strata=27, program_html_targets=651, findings=0, exit=0).

## Candidate cross-check

Candidate `webarena-task-spec-audit.md` (sha256 77e19d…): prints "812 /812,
IDs0–811, no missing/duplicate/unexpected"; evaluator-type sets
325/282/66/10/129; "27 /16" strata/selected; "the shopping site is omitted"
(:61). Every stated site-set/strata/selection-adjacent number agrees with my
independent census. The candidate prints no per-site-set histogram, so no
site-set count inside it could contradict my replay.

## Findings

None. No numeric disagreement, no silent task exclusion (strata population =
site-set population = 812, 0 skipped), no selection drift, no overstatement of
the shopping omission (the sample does contain `shopping_admin`, and the
candidate/Amendment say only `shopping` is omitted — accurate).

## Limitations of this replay

Site-set/strata/selection fields only; `program_html_targets` 651 and
locator/operator classes were observed consistent but are other seats' scopes.
Numeric agreement is an author-side independent implementation, not outside
closure. No production files mutated; scratch artifacts under
`.ufo/waves/round-28/scratch/FHistSiteSets/`.

VERDICT: PASS

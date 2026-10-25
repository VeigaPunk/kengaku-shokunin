# RevSamplePopulation — frozen16 sampling rule vs whole-812 census

- Seat: `KengakuR28.RevSamplePopulation-2` (reviewer, leaf, read-only w.r.t. production tree)
- Date: 2026-10-21
- Scope: `plans/round-28-claims.md` (C1 interface, lines 13–21) vs pinned snapshot `plans/fixtures/r28/webarena/` at upstream `dce04686a56253aefba7b18a4fa0937cf1dc987b`.
- Method: stdlib `json`/AST-free data read of `test.raw.json`; manual read of `evaluators.py` and `helper_functions.py` as data. No upstream code executed, imported, or evaled; no benchmark sites contacted. No installs performed (all needed tooling already present; pacman paused per lane rules).
- Integrity: `sha256sum` of all four snapshot files matches `manifest.json` exactly (`test.raw.json` 7b50386f…, `evaluators.py` e23edb39…, `helper_functions.py` ec758da4…, `LICENSE` c71d239d…). Treating snapshot as authentic per contract §C1.

## 1. Verdict on the frozen16 rule itself — PASS (deterministic, reproducible)

Recomputed from `test.raw.json`: keying each task by `(sorted(set(sites)), sorted(eval_types))` yields **27 distinct strata**. Sorting the 27 tuples lexicographically, taking `min(task_id)` per stratum, and retaining the first 16 produces exactly `[389, 590, 132, 173, 44, 552, 681, 791, 556, 356, 7, 377, 759, 424, 97, 399]` — identical to `selected-task-ids.json`. The declared rule is honest, deterministic, and reproducible by an independent reimplementation.

Population facts (all directly observed): 812 tasks; `task_id` contiguous 0–811, no duplicates, no missing IDs; site census shopping_admin 184, map 128, shopping 192, reddit 129, gitlab 204, wikipedia 23; eval-type census string_match 335, url_match 205, program_html 411 (non-exclusive); `require_login=True`/`require_reset=False`/`geolocation=None` on all 812 — these flags are stratification-inert and should be reported as constant, not per-stratum differentiators.

## 2. Coverage limits — the claim's own numbers, made precise

| Measure | Value | Note |
|---|---|---|
| Strata total | 27 | observed |
| Strata with a selected case | 16 | frozen16 |
| **Missing strata** | **11** | 40.7% of strata have no case report |
| Tasks in covered strata | 369 | 45.4% — but only 16 tasks get case reports |
| Tasks in missing strata | **443** | **54.6%** |
| Missing site (whole site, 0 cases) | **shopping** (192 tasks, 23.6%) | all 4 shopping-only strata missing: min-IDs 118 (ph, n=47), 653 (ph+url, n=10), 21 (sm, n=88), 158 (url, n=42) |
| Missing eval-type *set* patterns | none | all 5 eval-type sets occur inside the 16 covered strata; the 11 missing strata reuse covered eval-type sets |
| Missing site-set patterns | `(shopping)`, `(reddit,shopping)`, `(shopping_admin,url_match)`, `(shopping_admin,program_html+url)`, `(shopping_admin,string)`, `(reddit,program_html+url)`, `(reddit,string)` | 7 combos never seen by a case report |
| Cut boundary | mid-`reddit` | frozen16 ends at `('reddit',('program_html',))` (min 399, n=37); groups 17+ start `('reddit',('program_html','url_match'))` (min 595, n=58) — the cut is alphabetical position, not coverage |

### Feature-level gaps (what zero case reports ever exercise)

- `program_html` target `url` starting `func:` — **65 tasks, 75 occurrences, 0 in covered strata at all** (concentrated in shopping/shopping_admin/reddit+shopping). This is the `eval(func)` dynamic-URL path (`evaluators.py:263–266`); the frozen16 cannot even statically name which helper it calls for these tasks.
- `program_html` `locator` starting `func:` — 14 tasks / 22 occurrences; 9 tasks sit in covered strata (481–485 gitlab `gitlab_get_project_memeber_role`; 576–579) but **no selected task uses it**. Only sampled `locator` classes: `empty` (389,552,556) and `document.*` JS.
- `prep_actions` key — 5 tasks (699–703), all in the missing `('shopping_admin',('program_html','url_match'))` stratum.
- `required_contents.must_include` ` |OR| ` alternation — 5 tasks (431,750,751,755,756); 4 in covered strata, **none selected**.
- `reference_answers.must_include` ` |OR| ` — exactly 1 task (386), in missing `(shopping,string)` stratum. Note `StringEvaluator.__call__` does **not** split `|OR|` in `reference_answers` (only `program_html.required_contents` does, `evaluators.py:316`) — a static audit should flag whether 386's `|OR|` is intended as alternation (it will be matched literally).
- `url_note` absent — 9 tasks (174–182), covered `(gitlab,(string,url))` stratum, none selected; scorer defaults to `"GOLD in PRED"` (`evaluators.py:215`), so absence is legal but the case reports never demonstrate the default branch.
- Within-stratum feature diversity: selected groups carry 1–8 distinct feature signatures each (e.g. `shopping/program_html` has 8 distinct signatures; gitlab/program_html has 7 while selected task 389 exercises 1). Single-min-ID-per-stratum samples the lowest-ID signature only — signature skew is systematic (e.g. task 398 has 4 program_html targets vs 389's 1).

### Uniform (non-informative) dimensions
`require_login`, `require_reset`, `geolocation` constant; all 812 `start_url` contain `__X__` placeholders (GITLAB 196, SHOPPING 198, SHOPPING_ADMIN 182, MAP 128, REDDIT 114) — every task is a template; literal URL reachability is unverifiable statically. `sites` lists are unsorted in 29 tasks (e.g. 681 `["reddit","gitlab"]`) and `eval_types` unsorted in 129 (`("url_match","program_html")`) — audit must normalize before keying or it silently creates phantom strata.

## 3. Source-anchored scorer contract (from pinned `evaluators.py`/`helper_functions.py`, as data)

| Declared `eval_types` member | Fields the scorer actually reads | Failure modes reachable from spec alone |
|---|---|---|
| `string_match` | `eval.reference_answers` (dict; keys `exact_match`=str, `must_include`=list[str], `fuzzy_match`=list[str] or literal `"N/A"`); `intent`; `eval.string_note` **only** on the `fuzzy_match=="N/A"` fallback (`evaluators.py:150–163`); `reference_answers` ignored if absent→score 1.0 | unknown `reference_answers` key silently ignored; `must_include` non-list → `assert` (l.143); N/A branch without `string_note` → KeyError; single-element `must_include` triggers word_tokenize path (l.103–109) — 98 tasks |
| `url_match` | `eval.reference_url` (required, `.split(" \|OR\| ")` l.213); `eval.url_note` optional default `"GOLD in PRED"`; any other `url_note` value → `ValueError` l.239 | `reference_url: null` → AttributeError (7 tasks carry `reference_url: null`: 118, 356, 369–373 — all legal today because they are `program_html`-only) |
| `program_html` | `eval.program_html` list; each target `url` (`"last"` | literal | `func:…`), `locator` (`""` | `document.*`/`[...document.*` | `func:…`), `required_contents` with exactly one of `exact_match`/`must_include`; optional `prep_actions` | unknown locator prefix → `ValueError` l.301; required_contents neither op → `ValueError` l.330; `eval(func)` at l.266/l.299 — static audit MUST treat these as opaque names, not execute |
| unknown `eval_types` value | — | `evaluator_router` raises `ValueError` l.372 — an instrument-detectable schema violation |

Combination semantics: `EvaluatorComb` multiplies scores (l.348–352) — any zero factor → total zero; no partial credit. `StringEvaluator` reads `trajectory[-1]["answer"]` — the answer-bearing-final-action contract is runtime, invisible to spec audit.

## 4. What a static task-spec inventory **cannot** prove (do not upgrade these to findings)

1. **Semantic answer correctness** — `reference_answers` strings are ground truth by fiat; audit can only check shape.
2. **`func:`/`eval()` outcomes** — helper return values require live shopping/gitlab/reddit backends (e.g. `shopping_get_latest_order_url`, `reddit_get_post_url`); a static audit can name the referenced helper but not its result.
3. **LLM-judge verdicts** — `fuzzy_match`/`ua_match` outcomes are nondeterministic remote calls; only their *trigger conditions* are auditable.
4. **Placeholder resolution** — `__GITLAB__` etc. resolve via `browser_env.env_config` (not in snapshot); whether a task's start URL exists is unverifiable.
5. **Runtime page conformance** — whether JS locators return non-empty, whether `must_include` strings occur on the target page, whether gold URLs are reachable: all runtime facts.
6. **Auth semantics** — `storage_state` presence/naming is checkable; whether the state actually authenticates is not. (Observed semantic anomaly worth a *case-report note*, not a verdict: tasks 759–760 `(map,shopping_admin)` carry `storage_state: null` while `require_login: True`.)
7. **Task achievability / validity** — explicitly out of claim scope; field presence must never be counted as validity (e.g. unachievable-by-design fuzzy-N/A tasks: 36; every one verified to carry `eval.string_note` for the ua_match fallback — schema-complete ≠ achievable).
8. **Dead metadata** — task 723 carries a top-level `string_note` ("has no submissions in subreddit iphone13") that the scorer never reads alongside a different `eval.string_note` ("does not have any submissions in iphone13"). Report as metadata anomaly, not scorer defect.
9. **Score independence of eval_types ordering** — multiplication is commutative, but audit should still normalize; 129 tasks order `url_match` before `program_html`.
10. **The 43 tasks without `instantiation_dict`** (44, 45, 96, 97, 117, …) — `__X__` substitution may come from env_config constants rather than per-task dict; absence is not a defect per se.

## 5. Hand-expected cases for `benchmark_spec_audit.py --selftest` (concrete fixtures)

Schema-level (expected values hard-coded):
- S1 minimal valid `string_match` task → clean pass; assert `tasks_total=1`, `duplicates=[]`, `strata_count=1`.
- S2 duplicate `task_id` (two tasks, same id) → `duplicates=[id]` reported; still inventories both.
- S3 `eval_types: ["tea_timer"]` → instrument finding `unknown_eval_type` (maps to router ValueError l.372), NOT a benchmark FAIL.
- S4 `string_match` with `reference_answers.must_include: "abc"` (str not list) → schema-incompatible finding citing assert l.143.
- S5 `string_match` + `fuzzy_match: "N/A"` and missing `eval.string_note` → finding `fuzzy_na_without_string_note`.
- S6 `url_match` with `reference_url: null` → finding `null_reference_url`; same key present-but-null must be distinguished from absent.
- S7 `program_html` target with `locator: "window.foo()"` (not document./func:/"") → finding `unknown_locator_prefix` (ValueError l.301).
- S8 `program_html` target `required_contents: {"regex": "x"}` → finding `unknown_required_contents_op` (ValueError l.330).
- S9 `url_note: "EXACT"` → finding `unknown_url_note` (only `"GOLD in PRED"` or absent legal).
- S10 `program_html` declared in eval_types but key absent/null/[] → finding `declared_eval_without_payload` (mirrors observed-clean property: 0/812 today).

Semantic/edge (audit must describe, never FAIL):
- E1 unsorted `sites`/`eval_types` → normalization proven by asserting a `["reddit","gitlab"]`+`["url_match","program_html"]` task lands in the same stratum as sorted twins (real corpus has 29+129 such tasks).
- E2 `func:` locator/`func:` URL task → parsed and named (e.g. `gitlab_get_project_memeber_role`) with an explicit "opaque-runtime" annotation; MUST NOT execute (no `eval()` in audit code — AST-parse only).
- E3 `|OR|` in `reference_url` → alternates counted; `|OR|` inside `reference_answers.must_include` → flagged `literal_or_in_reference_answers` (scorer does not split there — task 386 precedent).
- E4 multi-target `program_html` (up to 10 targets exist: tasks with target counts 0–10; distribution 0:401·1:291·2:57·3:44·4:2·5:9·6:2·7:3·8:1·10:2) → all targets audited, count reported.
- E5 `prep_actions` target → recorded as JS-prep step, marked runtime-opaque.
- E6 snapshot corruption → flip one byte → exit2 `snapshot_tampered`; missing file → exit2 `input_missing`; hash check must precede all counting (contract line 15).
- E7 empty `reference_answers: {}` on a `string_match` task → documented score-1.0-vacuous property (no such task in 812; selftest proves the audit detects rather than crashes).
- E8 task with top-level `string_note` alongside `eval.string_note` (723 pattern) → reported `top_level_string_note_dead_key` informational.

## 6. Required code/output checks recommended for the delivered audit

- `--summary` MUST print: total 812, duplicate-id list (empty), stratum table of all 27 rows `(min_id, n, site_set, eval_set, selected?)`, covered-strata task count 369 / missing 443, absent-site list `[shopping]`, and the feature-coverage table showing which scorer paths have zero selected case (`ph_url:func`, `ph_loc:func`, `prep_actions`, `ph_must_include |OR|`, `refans_must_include |OR|`, `url_note-absent`, single-item `must_include` tokenize branch, `fuzzy_match=="N/A"` branch covered only by task 791).
- Selection MUST be re-derived and compared to `selected-task-ids.json`; mismatch → exit2, never silent drift.
- Per-task JSON MUST carry per-scorer schema-verdict (compatible / instrument-finding) with file:line anchors (e.g. `evaluators.py:143`), plus `unchecked` list naming runtime-only facts.
- Denominators printed for every aggregate (e.g. "must_include single-item: 98/335 string_match tasks").
- Independent oracle (per contract l.21): recompute strata/selection/feature census by hand-written jq/python one-offs — my recomputation above already matches; integration must reproduce these numbers exactly.
- `--selftest` MUST be CLI-level with the S1–S10/E1–E8 fixtures above (hand-expected), plus corpus-drift guard: any change to `test.raw.json` bytes → exit2 before counting.

## 7. Residual risk / gaps

- Selection rule pins min-ID per stratum; lowest-ID task can be unrepresentative *within* its stratum (feature-signature diversity 1–8 per stratum). Mitigation is disclosure, already present in claim text ("deliberately bounded/nonrepresentative"), but case reports should state their stratum's `n` and internal signature count.
- My `sites`/`storage_state`/`require_login` semantic notes (759–760 null state; 723 duplicate note) are static observations; runtime impact unverified by design.
- I did not open the upstream repository — all facts are from the pinned snapshot whose hashes verify against the lane manifest; upstream URLs cited in `manifest.json` (accessed 2026-10-21 per manifest).

## Scoped verdict

**PASS** — the frozen16 selection rule is exactly as claimed: deterministic, reproducible, correctly persisted (16/16 IDs match recomputation; 27 strata census verified). **Bounded**: the sample deliberately omits 11/27 strata (443/812 tasks), the entire `shopping` site, and six scorer-relevant feature classes (`func:` URLs, `func:` locators in selected tasks, `prep_actions`, both `|OR|` forms, `url_note` default branch, reference-answers `|OR|`); the claim's own "bounded/nonrepresentative" language is accurate and must stay attached to every aggregate derived from the 16 cases. No defect in the rule itself; the required disclosure is a coverage table exactly as specified in §6. This is a scoped verdict on the sampling rule + whole-population census only, not a round-level PASS.

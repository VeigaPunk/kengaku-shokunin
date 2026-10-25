# FTask044 — author-side falsification of BUILD case44 (WebArena task_id 44)

Seat: KengakuR28.FTask044 (leaf scout, read-only over production). Round 28, C1 only.
Static text/source audit; no upstream import/execution, no browser, no benchmark-site request,
no scorer run, no delegation, no installs. All scratch/output only in this report; production
tree unmodified (verified by the byte hashes below before analysis).

## 1. Inputs and identity

| object | absolute path (lane root /home/vgpnk/Projects/shokunin/kengaku-shokunin) | sha256 |
|---|---|---|
| build case44 | `.ufo/waves/round-28/build/Task044.md` | `1aae7a8169a104efbbcd6e1a19e15f18c5c7b8b3b6b77847219a38b9b823df1a` |
| frozen candidate | `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md` | `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` |
| raw task spec | `plans/fixtures/r28/webarena/config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` |
| evaluators | `plans/fixtures/r28/webarena/evaluation_harness/evaluators.py` | `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22` |
| helpers | `plans/fixtures/r28/webarena/evaluation_harness/helper_functions.py` | `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275` |
| audit instrument | `plans/benchmark_spec_audit.py` | `f72a856929b4c6aeacae53d8224e0d199b0867d85a2ab729e70641f22d551eb8` |

Candidate bytes equal `.ufo/waves/round-28/candidate-freeze.json`; fixture hashes equal
`plans/fixtures/r28/webarena/manifest.json` (revision dce04686…, opened 2026-10-21).
Canonical admission target is `corpus/knowledge/webarena-task-spec-audit.md`;
it is **absent** from the tree at audit time (draft-only), as the wave contract states.

## 2. Independent re-derivation (before comparing to instrument/oracle)

Derived with stdlib `json` only from the raw file; instrument and `benchmark_oracle.py` not
consulted until after these numbers were fixed.

- 812 tasks, IDs exactly 0–811, 0 duplicates; 27 (sorted site-set, sorted eval-type-set) strata.
- Task 44 stratum `(("gitlab",), ("url_match",))` has exactly 16 members:
  `44,45,46,102,103,104,105,106,156,258,339,340,341,342,343,357`; minimum = 44.
- `selected-task-ids.json` = `[389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399]`;
  recomputing "sort strata lexicographically, take each group's minimum, first 16" reproduces
  this list exactly; 44 is the **fifth** entry.
- `intent_template_id: 303` occurs once (task 44 only).
- `dashboard/todos` occurs exactly once in the whole raw file (line 1426, task 44); no other
  task's `reference_url` contains it.
- Task 44 block is lines **1408–1431** exactly: L1419 intent, L1422–1424 eval_types,
  L1426 reference_url, L1428 url_note; all other fields as the build states
  (`sites=["gitlab"]`, `require_login=true`, `storage_state="./.auth/gitlab_state.json"`,
  `start_url="__GITLAB__"`, `geolocation=null`, `require_reset=false`,
  `reference_answers=null`, `program_html=[]`, `instantiation_dict={}`).

All build §"Inputs" and §"Sample membership" numbers are correct.

## 3. Build claim → pinned source line verification

| build claim | actual pinned location | result |
|---|---|---|
| `url_match` → `URLEvaluator()` `evaluators.py:367-368` | L367 `case "url_match":`, L368 append | verified |
| `URLEvaluator.__call__` never reads trajectory, L177-241 | def at 177; return score at 241; `trajectory` unused in body | verified |
| `clean_url` strip trailing `/` L187-190, applied L212 | 187–190, 212 | verified |
| `parse_url` L192-197; `base = netloc + path` L195 | 192–197; 195 | verified |
| `ref_urls.split(" |OR| ")` L213-214 | 213–214 | verified |
| rule read L215-216 (`GOLD in PRED`) | 215–216 | verified |
| `base_score = any(ref_base_path in pred_base_paths)` L220-227 | 220–227 | verified |
| `query_score` loop L228-235 | 228–235 | verified |
| substring at L223 (not list membership/equality) | 223, `pred_base_paths` is a `str` | verified |
| `EvaluatorComb` product L348-352 | 348 `score=1.0` … 352 `return score`, `score *= cur_score` L351 | verified |
| `llm_fuzzy_match`, `llm_ua_match` imported evaluators.py:21-22 | L21–22 | verified |
| `PseudoPage` helper_functions.py:211-221 | class 211 … `return getattr(self, attr)` 221; `self.url` set in `__init__` 212–214 | verified |
| `GITLAB` import helper_functions.py:9-11 | 9 `from browser_env.env_config import (`, 10 `ACCOUNTS,`, 11 `GITLAB,` | verified |
| no `__GITLAB__` in `evaluation_harness/*.py` | recursive grep exit 1 (no match) | verified |
| substitution/page selection absent from pinned files | manifest pins only raw JSON, evaluators, helpers, LICENSE | verified |

The N/A/fuzzy and HTML rows of the candidate (S062:80–94, 134, 98–111/142–149, 150–169,
152–163, 159, 187–239, 199–235, 258–333, 271–301, 333, 348–352, 361–374; S063:146–173,
176–208) also resolve to the stated lines in the pinned bytes (checked; no discrepancy).

## 4. Operator re-execution (stdlib copy of the pinned functions, no upstream import)

Reference `http://h:8023/dashboard/todos` (ref_queries empty):

| prediction | base | query | score | control purpose |
|---|---|---|---|---|
| `http://h:8023/dashboard/todos` | 1.0 | 1.0 | **1.0** | nominal pass |
| `http://h:8023/dashboard/todos?state=done&type=MergeRequest` | 1.0 | 1.0 | **1.0** | query ignored |
| `http://h:8023/dashboard/todos#x` | 1.0 | 1.0 | **1.0** | fragment ignored |
| `http://h:8023/dashboard/todosXYZ` | 1.0 | 1.0 | **1.0** | suffix over-extension |
| `https://h:8023/dashboard/todos` | 1.0 | 1.0 | **1.0** | scheme ignored |
| `http://h:8023/dashboard/todos/` | 1.0 | 1.0 | **1.0** | trailing slash ignored |
| `http://h:8023/dashboard/todo` | 0.0 | 1.0 | **0.0** | one-character boundary (decisive) |
| `http://h:8023/x/dashboard/todos/1` | 0.0 | 1.0 | **0.0** | prefix position matters |
| `http://h:8023/users/sign_in` | 0.0 | 1.0 | **0.0** | redirect failure |
| `https://evil.example/h:8023/dashboard/todos` | 1.0 | 1.0 | **1.0** | netloc is not field-compared (extra control) |

**Decisive boundary/control:** with identical netloc/query/scheme held fixed, `/dashboard/todo`
scores 0.0 while `/dashboard/todosXYZ` scores 1.0. This proves the predicate is substring
containment over `netloc+path`, not path equality — exactly the build's operator claim, and its
"checked/unchecked" division follows. The last row is a genuine over-acceptance edge the build
does not enumerate: any prediction whose `netloc+path` embeds the reference host:port string
passes (a foreign-host path such as `/h:8023/dashboard/todos`). It is entailed by the build's own
"Python substring test" statement and does not contradict the audit; it is an additional control,
not a falsification.

## 5. Checked / unchecked clause audit (case 44 only)

Confirmed against pinned source: final URL only; scheme, fragment, query and trailing slash
ignored; rendered content, HTTP status, filter (`state`), user identity beyond `storage_state`,
final answer, trajectory, side effects and `require_reset=false` not inspected; path
over-extension passes. `URLEvaluator` has no answer/content/trajectory read; the config declares
`program_html=[]` and `reference_answers=null`, so no helper or LLM judge is reachable
(`eval_types=["url_match"]` routes only `URLEvaluator`). The build's separation of
"static mapping PASS" from "runtime validity undetermined" is source-faithful; no site, runner,
GitLab version/redirect or tab-selection evidence was claimed.

One non-material wording defect: build §"Observed operator semantics" says "`parse_url` returns
one `str` (L192-197)". The function returns a `(base_path, query)` 2-tuple; only `base_path` is a
`str`. The derived conclusion (L223 is a substring test because `pred_base_paths` is a `str`) is
correct, so this is a phrasing precision issue, not a false claim about scorer behavior.

## 6. Candidate case-specific language vs source

- Table cell "44,552,681,791 … URL-only navigation" — accurate for task 44 (`url_match` only,
  `program_html=[]`, no answers, no judge).
- "selected cases … omit … OR-alternative content checks" — independently verified: none of the
  16 selected tasks has ` |OR| ` in `program_html.required_contents`. Task 681 does carry
  ` |OR| ` in `reference_url`; that is URL-alternative behavior, which the candidate's URL
  paragraph separately describes, not a content check. No overreach.
- Candidate does not assert task 44 is invalid or valid at runtime; its only task-44 statement is
  the URL-only navigation boundary. No claim exceeds the pinned source.
- All 16 named case reports exist under `.ufo/waves/round-28/build/` (Task007/044/097/132/173/
  356/377/389/399/424/552/556/590/681/759/791.md), each with a verdict/runtime-evidence section;
  the candidate's "16 case audits" and report-path table are accurate.

## 7. Numeric claims (candidate C1 and case-relevant)

Independent census (my own code) matches the candidate exactly: 812 tasks / 812 distinct /
5 evaluator-type sets (325, 282, 66, 10, 129) / 27 strata / 16 selected / 651 program_html
targets / html operators 188 exact_match + 463 must_include / string operators 45 exact_match,
176 must_include, 118 fuzzy_match / locator classes 105 full-page, 524 JavaScript, 22 helper /
target URL classes 238 last, 338 navigation, 75 helper.

CLI probes (read-only, `PYTHONDONTWRITEBYTECODE=1`): `benchmark_spec_audit.py --summary` exit 0,
findings=0, same counters; `--selftest` exit 0 with exactly 21 cases, including
`cli_snapshot_pin`, `cli_manifest_pin`, `cli_missing_input`, `scorer_product_mutation`.
The separately authored `plans/fixtures/r28/benchmark_oracle.py` agrees on every metric and the
selected-ID list; per its own header this is independent logic, **not** independent authorship —
I do not upgrade it to outside evidence. (No production writes; reads only.)

## 8. Findings

1. **No substantive falsification.** Every intent→target/operator/unchecked clause and every
   numeric/source-line claim in BUILD case44 is supported by the pinned bytes. Confidence: high
   (line-exact source reads plus independent recomputation and probe).
2. **Non-material (F1):** the `parse_url` "returns one `str`" phrasing in Task044 §"Observed
   operator semantics" should read "returns `(base_path: str, query: dict)`"; conclusion holds.
3. **Additional boundary (F2), not a contradiction:** foreign-host path embedding
   (`https://evil.example/h:8023/dashboard/todos`) scores 1.0 because netloc is part of the
   substring rather than a compared field; useful as an extra over-acceptance control if the
   case is cited.
4. **Remaining unknowns** are exactly the build's: substituted `__GITLAB__`, unpinned runner/page
   selection (`PseudoPage`), live GitLab todos route/redirects under valid/expired storage state,
   tab hand-off, rendered content, and side-effect observation. None is resolvable statically and
   none was attempted.

## 9. Verdict

**VERDICT: PASS** — for the scoped BUILD case44 static intent→evaluator audit and the candidate's
task-44/URL-contract language only. The audit's static claims are completely supported by the
pinned snapshot at dce04686…; its runtime-validity status remains undetermined, as the case
itself states. This is not a round-level PASS and does not close C1 admission
(`corpus/knowledge/webarena-task-spec-audit.md` is not admitted; candidate remains frozen at
`77e19d5b…20a8`).

Observed commands: `sha256sum` of inputs/candidate/instrument; stdlib `json`/`urllib.parse`
censuses and the URL probe (temporary shell, no files written); `grep`/`awk` line anchoring in
the three pinned files; `python3 plans/benchmark_spec_audit.py --summary` and `--selftest`;
`python3 plans/fixtures/r28/benchmark_oracle.py` (comparison only, after independent derivation).
No installs or updates. No production/scratch artifact other than this report.

# FTask389 — author-side falsification of BUILD case389 (WebArena task_id 389)

Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
Target under test: `.ufo/waves/round-28/build/Task389.md` (writer `KengakuR28.Task389-2`),
SHA256 recomputed 2026-10-21 = `d79116250cda04aac633f914b43db1b4b0e278c9df20d93afe4764fa7874c8c1`.
Raw case: `plans/fixtures/r28/webarena/config_files/test.raw.json`, task_id 389, JSON object
lines `12073–12109`.
Frozen candidate: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, SHA256 recomputed
2026-10-21 = `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` (equals
`candidate-freeze.json`).
Canonical candidate: `corpus/knowledge/webarena-task-spec-audit.md` — **not admitted**; the file is
absent from the tree and was never opened or edited by this seat. It is named here only as the
prospective target.
Scope: case 389 only. No other of the 16 cases, no C2/registry work, no production edit, no delegation.

## 0. Method and provenance

- Read-only over production. No installs or updates (tool log: none). No browser, no benchmark-site
  request, no upstream Python import/execution, no REA MCP, no scorer or production-instrument run.
- Commands on the pinned snapshot only: `sha256sum`, `nl -ba`, `grep -n`, `sed -n`, and stdlib-only
  `python3` (`json.load`, counting, string classification), `PYTHONDONTWRITEBYTECODE=1`.
- Scratch evidence (mine): `.ufo/waves/round-28/scratch/FTask389/census.txt`, SHA256
  `d2855d82299840b623bad6118dd44f358a73e6e301c91d6a6dff61ea44cb4837`.
- The census re-derives JSON aggregate counts directly; it does not import
  `plans/benchmark_spec_audit.py`, `plans/fixtures/r28/benchmark_oracle.py`, or any scorer module.

Pin (every recomputed value equals `plans/fixtures/r28/webarena/manifest.json`, opened 2026-10-21;
upstream revision `dce04686a56253aefba7b18a4fa0937cf1dc987b`):

| file | full SHA256 | bytes |
|---|---|---|
| `config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | 880776 |
| `evaluation_harness/evaluators.py` | `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22` | 13264 |
| `evaluation_harness/helper_functions.py` | `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275` | 7565 |
| `LICENSE` | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` | 11357 |

The build's three truncated digests are correct suffixes (`…37652`, `…00c22`, `…e275`); no digest
defect. The three upstream URLs in the build table are the manifest URLs, not re-fetched by this seat.

Source URLs (manifest, snapshot opened 2026-10-21, not re-fetched): the raw task quote above is from
`https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json`
and the evaluator quote from
`https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py`.

## 1. Raw case-389 facts (observed, line-exact)

| field | value | line |
|---|---|---|
| object open | `{` | 12073 |
| sites | `["gitlab"]` | 12074–12076 |
| task_id | 389 | 12077 |
| require_login / storage_state | `true` / `./.auth/gitlab_state.json` | 12078 / 12079 |
| start_url / geolocation | `__GITLAB__` / `null` | 12080 / 12081 |
| intent_template | `Post "{{content}}" for the merge request related to {{mr}} in {{repo}} project` | 12082 |
| instantiation_dict | `mr="octovisuals page"`, `repo="primer/design"`, `content="Thanks, working on reviews"` | 12083–12087 |
| intent | `Post "Thanks, working on reviews" for the merge request related to octovisuals page in primer/design project` | 12088 |
| require_reset | `false` | 12089 |
| eval | `{` … `}` | 12090–12107 |
| eval_types | `["program_html"]` | 12091–12093 |
| reference_answers / reference_url | `null` / `""` | 12094 / 12095 |
| program_html target | url `__GITLAB__/primer/design/-/merge_requests/450`, locator `""` | 12098 / 12099 |
| required_contents | `must_include: ["Thanks, working on reviews"]` | 12100–12104 |
| intent_template_id / object close | 348 / `},` | 12108 / 12109 |

The intent quote (16 words) is at `test.raw.json:12088` in the manifest-pinned revision above,
accessed 2026-10-21. The operator quote `selected_element = html.unescape(selected_element)` is
`evaluators.py:303`.

## 2. Scorer trace — every build anchor re-read on pinned bytes

| build claim | build anchor | actual location | status |
|---|---|---|---|
| router maps `program_html` to `HTMLContentEvaluator()` | L369–370 | 369 `case "program_html":`, 370 `evaluators.append(HTMLContentEvaluator())` | exact |
| `EvaluatorComb` multiplies scores | L348–352 | 348 `score = 1.0`, 349 loop, 350 call, 351 `score *= cur_score`, 352 return | exact |
| URL is not `func`, so the `eval()` branch is skipped | L263–266 | 263 `if target_url.startswith("func"):` … 266 `eval(func)` | exact |
| URL is not `"last"`, so `page.goto` + fixed sleep | L271–273 | 271 `if target_url != "last":`, 272 `page.goto(target_url)`, 273 `time.sleep(3)` | exact |
| empty locator reads `page.content()` | L276–277 | 276 `if not locator.strip():`, 277 `selected_element = page.content()` | exact |
| normalization `html.unescape` | **L302** | **303** `selected_element = html.unescape(selected_element)`; 302 is blank | **wrong by one line (D2)** |
| `must_include` split on `" \|OR\| "`, `tokenize=False` | L312–327 | 312 `elif "must_include"`, 316 `content.split(" \|OR\| ")`, 319–323 call with `tokenize=False`, 327 product | exact |
| `must_include` substring after `clean_answer` | L98–111 | 99–100 clean both, 103–109 tokenize branch, 111 `return float(clean_ref in clean_pred)` | exact |
| `clean_answer` strip/one quote pair/lower | L80–86 | 81 strip, 82–85 one outer quote pair, 86 `return answer.lower()` | exact |
| `__call__` body has no trajectory read | L248–333 | 248 `def __call__(`, body to 333; `trajectory` only a parameter | exact |
| LLM helpers unreachable | helper L146, L176 | 146 `def llm_fuzzy_match`, 176 `def llm_ua_match` | exact |
| `PseudoPage` delegates attributes | helper L211–221 | 211 class, 216 `__getattr__`, 219 `getattr(self.original_page, attr)` | exact |
| `HTMLContentEvaluator` class | **L245–333** (compact row) | **244** class, 245 docstring; 333 last body line | **wrong start (D3)** |

Re-derived contract: one target; no `func` URL; `page.goto` the hard-coded MR URL; `sleep(3)`;
empty locator → `page.content()`; `html.unescape`; `must_include` with a single non-OR element
`"Thanks, working on reviews"`; `clean_answer` lowercases both sides; a single Boolean any() multiplied
into score 1.0. Net: score 1.0 iff the lowercased unescaped serialized DOM contains
`thanks, working on reviews`, else 0.0 **on a completed evaluation**. This reproduces the build's net
contract. Precision note N1: `page.goto`, page access, config-read and beartype failures raise through
`EvaluatorComb` rather than yielding 0.0; the build's "Otherwise score = 0.0" is unqualified.

## 3. Independent census (raw JSON only; no alternate oracle imported)

| build/candidate claim | recomputed | result |
|---|---|---|
| 812 raw tasks, 812 distinct, IDs 0–811, no missing/duplicate | 812 / 812 / min 0 / max 811 / `[]` / `[]` | match |
| all 812 tasks `require_reset: false` | 812/812 `false` | match |
| 27 site/evaluator strata | 27 | match |
| first stratum `(('gitlab',), ('program_html',))`, 88 tasks, min 389 | 88, min 389 | match |
| 389 is selection #1; selected IDs `389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399` | first-16 minima reproduce the list exactly; fixture equals it | match |
| 117 program_html targets in that stratum; 63 empty-locator + `must_include` | 117; 63 (and all 63 empty-locator targets use `must_include`) | match |
| template 348 = 389 plus siblings 390,391,392,393; siblings use one identical last-note locator with `exact_match`; 389 alone empty-locator/`must_include` | template ids `[389,390,391,392,393]`; 390–393 locator byte-identical, values `lgtm`/`close because non reproducible`/`Good idea`/`lgtm`; 389 as stated | match |
| candidate: 651 page-content targets; 188 `exact_match` + 463 `must_include`; 0 both-key | 651; 0/188/463 | match |
| candidate: locator classes 105 full-page / 524 JavaScript / 22 helper | 105/524/22 (sum 651) | match |
| candidate: URL classes 238 `last` / 338 navigation / 75 helper | 238/338/75 (sum 651) | match |
| candidate: evaluator-type sets 325/282/66/10/129 | identical histogram (sum 812) | match |
| candidate: string operators 45 `exact_match` / 176 `must_include` / 118 `fuzzy_match`, may coexist | 45/176/118; 4 tasks carry more than one | match |
| candidate: all N/A tasks use only that approach | 36 N/A tasks, 36 single-approach | match |
| candidate: selected cases omit helper URL/locator, prep actions, OR alternatives | selected 16: 0 `func:` URLs, 0 `func:` locators, 0 `prep_actions`, 0 `" \|OR\| "` values | match |
| candidate: shopping site omitted from selection | no `('shopping',)` task among the 16 (`map+shopping_admin` is present, not shopping) | match |
| candidate: raw tasks 812 / 5 evaluator-type sets / 27 strata / 16 cases / 651 targets; selftest 21 | audit-summary.txt and audit-current.stdout JSON reproduce 812/812/27/16/651; audit-selftest.stdout `cases=21`, exit0 (receipt read, not executed) | match |

`__GITLAB__` occurs 0 times in `evaluators.py`, 0 in `helper_functions.py`, 385 times in
`test.raw.json`; the build's "not substituted anywhere in evaluators.py" is exact.

## 4. Defects found in `build/Task389.md`

- **D1 — record range is wrong at the start.** "Task record (raw JSON lines 12077–12109)" starts at
  `task_id`; the JSON object opens at **12073** and the `sites` field that the section lists is
  **12074–12076**, outside the cited range. Full object span is 12073–12109.
- **D2 — `html.unescape` anchor.** The build cites **L302**; line 302 is blank and the operation is
  **303**. The sibling `build/Task590.md` line 47 cites 303, and the pinned source agrees.
- **D3 — `HTMLContentEvaluator` start.** The build's compact row cites **L245–333**; the class is
  defined at **244** (L245 is its docstring). The trace table's `L248–333` is the `__call__` body and
  is exact. The candidate itself and `build/Task590.md` use 244–333; `audit-current.stdout`
  `contract_anchors` also records line 244.
- **D4 — sibling comparison is not source-qualified (boundary, not runtime invalidity).** The
  template-348 sibling locator reproduced verbatim by the build is
  `document.querySelector('[id="notes-list"').lastElementChild…`: the selector literal has one `[`
  and **no `]`** (raw JSON lines 12136, 12171, 12206, 12241). The candidate records the same
  bracket-imbalance class for tasks 356/759/424 and explicitly says it "does not infer browser
  rejection from bracket counting; engine parsing/runtime DOM is untested"
  (`webarena-task-spec-audit.md:83–84`). Task389's "389 uses a weaker check than its siblings"
  comparison therefore rests on sibling predicates whose selector is source-malformed, without
  restating that caveat. This is a resolvable qualification, not a claim that 389 or its siblings are
  runtime-invalid. (A heuristic pass over 431 quoted `querySelector('…')` arguments finds 204 with
  imbalanced selector strings, so this is a population-wide anomaly class, not a unique 389 fact.)

Precision notes, not verdict-affecting:

- **N1** (see §2): the net contract's "Otherwise score = 0.0" omits exception propagation for
  navigation/config/page failures.
- **N2**: "No LLM judge dependency and no helper HTTP API dependency for this task" is true on the
  scoring path, but import-time dependencies still exist: `helper_functions.py` imports `requests`
  (L6) and `generate_from_openai_chat_completion` (L18–20), and `evaluators.py` imports the helpers
  (L18–27). `build/Task590.md` line 50 records this import-time distinction; Task389 does not.

## 5. Decisive boundary / controls

- **B1 — the decisive validity boundary is phrase pre-existence under `require_reset: false`.** With
  no before/after diff in `HTMLContentEvaluator`, the whole-page `must_include` makes a no-op pass if
  the reset-state MR 450 DOM already carries the phrase; conversely a correct post can miss the fixed
  3 s window. The build lists both as unproven and makes baseline absence plus a no-op negative control
  the first gates. That is the correct decisive control set; neither side is statically decidable.
- **B2 — missing sibling-selector control.** For the comparative claim, the decisive control is a
  sanctioned local selector-parse of the exact sibling string (`document.querySelector('[id="notes-list"')`)
  on a scratch page — no benchmark-site traffic. If it throws, the JS branch's `except` sets
  `selected_element = ""` and `exact_match` scores 0, which would invert "weaker than siblings". Per
  the lane's own doctrine this seat does **not** infer that outcome from bracket counting, and the
  probe was not run (no browser actions). The build should either record the anomaly and this control
  or drop the stronger-control framing.
- **B3 — positive/negative controls are adequate.** Posting the phrase should score 1.0; no action,
  a different MR, typed-but-unsubmitted text, or the phrase only in an edited description probe
  over-acceptance; the build states expected 0 except for the description case, which it correctly
  labels over-acceptance rather than invalidity.

## 6. Candidate case-specific language vs source

Candidate mentions bearing on 389 (frozen-draft line numbers):

- line 60, selected-ID list — reproduces exactly from the pinned raw JSON under the registered rule.
- line 62, selected cases omit helper URL/locator, `prep_actions`, and OR alternatives — verified for
  all 16 selected tasks (0/0/0/0).
- line 70, case-table boundary "comment/page state" for 389 — supported: the predicate checks a phrase
  anywhere in the page DOM, not comment-ness or novelty, exactly as `Task389.md` §"Checked vs
  unchecked" states.
- line 35, page-content row `S062:258–333 … unescapes HTML, applies exact_match before must_include;
  targets multiply` — each clause re-read on the pinned bytes (258 targets read, 303 unescape,
  305/312 precedence, 327/351 product) and supported.
- line 83–84 bracket-counting caveat — correctly refuses runtime inference; the same caveat is what
  makes D4 a qualification rather than a defect claim.
- The candidate's `HTMLContentEvaluator:244–333` (line 1) is the correct range; the build's L245 is
  the outlier.

No candidate sentence about case 389 turns an unobserved runtime condition into success/failure, and
no candidate case-389 number exceeds or misstates the pinned source. The defects D1–D3 are in the
build case report's citation layer, not in the candidate.

## 7. Unresolved (not claimed)

- Reset-state DOM of `primer/design` MR 450; whether the phrase pre-exists there.
- MR 450's title/description and whether it is uniquely the "octovisuals page" MR.
- GitLab client render latency vs the fixed 3 s sleep; whether notes are client-rendered at all.
- The `__GITLAB__` substitution value and the generated per-task config actually fed to the scorer.
- Sibling selector engine behavior (B2) and sibling task validity.
- Whether the trajectory ends with a stop action, and any harness-level exception handling outside the
  pinned evaluator.
- No browser, site request, scorer run, or production-instrument run by this seat; the 21-case selftest
  and exit0 receipts are producer claims read from `corpus/evidence/round28-calibration/`, not rerun.

## Verdict

Semantic case audit: **PASS** — the intent→target→operator→unchecked-clause mapping for 389 reproduces
from the hash-verified pinned bytes, and every case-specific number (88, 389-min, 117, 63, 812, 3 s,
template-348 membership) and every candidate 389 number/counter is independently confirmed.
Citation/boundary layer: **partial** — D1 (record range 12077 vs object 12073–12109), D2
(`html.unescape` 302 vs 303), D3 (`HTMLContentEvaluator` 245 vs 244), and D4 (sibling selector
unqualified) are real, resolvable defects. Because not every source-line claim is exact, PASS is
withheld for the citation layer.

Canonical candidate `corpus/knowledge/webarena-task-spec-audit.md` is not admitted; the frozen draft
`77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` was re-verified at report time.

VERDICT: PARTIAL

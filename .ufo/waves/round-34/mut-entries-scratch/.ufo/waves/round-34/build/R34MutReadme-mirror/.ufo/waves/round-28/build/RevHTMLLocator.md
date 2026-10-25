# RevHTMLLocator-2 — HTMLContentEvaluator locator/JS-evaluation review (C1 scoped)

- Writer/seat: KengakuR28.RevHTMLLocator-2 (reviewer, author-side). Judged axis: novelty.
- Scope: `HTMLContentEvaluator` locator classes, empty-locator path, JS-evaluation path, and the static-vs-runtime boundary for the new audit (`plans/benchmark_spec_audit.py`). In scope only; no blanket round verdict.
- Pinned source (manifest-verified basis): `plans/fixtures/r28/webarena/evaluation_harness/evaluators.py` sha256 `e23edb39…00c22`; `helper_functions.py` sha256 `ec758da4…e275`; `config_files/test.raw.json` sha256 `7b50386f…7652`; upstream revision `dce04686a56253aefba7b18a4fa0937cf1dc987b`.
- Upstream source openings (access date 2026-10-21; manifest records raw.githubusercontent.com URLs): evaluators.py, helper_functions.py, test.raw.json — opened as snapshot files; ≤25-word located quotes inline below. No network contact made by this seat.
- Observed commands: `python3` census/inspection one-liners over `test.raw.json` (read-only JSON load, never upstream-code execution); `grep` over `plans/benchmark_spec_audit.py` and sibling build reports; `wc -l`; `find`/`glob` for wave layout. No installs; no production builds/tests/linters run mid-flight.
- Upstream code was treated as data throughout: `eval`/`page.evaluate` call sites were read, never run.

## 1. Source-anchored contract of `HTMLContentEvaluator.__call__` (evaluators.py:248–333)

Per `eval.program_html[]` target, `score=1.0` multiplied by each target score:

| Key | Guard (line) | Semantics |
|---|---|---|
| `url` | `target_url.startswith("func")` (263) — note: **no colon** | Splits on literal `"func:"`, replaces `__last_url__` with `page.url` verbatim, then Python `eval(func)` (266). Unguarded: a `NameError`/`SyntaxError`/network `requests` exception **crashes the whole evaluation**, not just the target. |
| `url` | `!= "last"` → `page.goto(target_url); time.sleep(3)` (271–273) | Unguarded `goto`; fixed 3 s settle (upstream TODO admits hack). Placeholder URLs (`__GITLAB__` etc.) must already be host-substituted by config preprocessing — the evaluator never substitutes them. |
| `locator` | `not locator.strip()` (276) | `page.content()` — **full serialized HTML**, not rendered text. Unguarded: navigation-dead page crashes. |
| `locator` | `startswith("document.")` or `startswith("[...document.")` (279–281) | Optional `prep_actions[]` each run as `page.evaluate(f"() => {prep_action}")` inside `try/except: pass` — failures silently ignored (282–287). Main locator runs `str(page.evaluate(f"() => {locator}"))` inside `try/except` → `""` on any exception (288–294). Fails closed. |
| `locator` | `startswith("func:")` (296) | Splits `"func:"`, replaces `__page__` → `page`, Python `eval(func)` — module scope: `page` bound (call-site param), helper names bound (imports 18–27), but **`__last_url__` is NOT replaced in locators** (asymmetric with the url path). Unguarded: crash propagates. |
| `locator` | else | `raise ValueError("Unknown locator")` (301) — a single malformed locator crashes evaluation mid-loop after earlier `page.goto` navigation mutations. |
| post | `html.unescape(selected_element)` (303) | Unescape applied to *every* branch incl. `page.content()` HTML and `str(list)` reprs. |
| `required_contents` | `"exact_match"` → `StringEvaluator.exact_match(ref, pred)` (305–310) | `clean_answer`: strip, strip one matched pair of `'` or `"`, lowercase (80–86). |
| | `elif "must_include"` → per-element split on `" \|OR\| "`, `any(must_include(tokenize=False))` (312–327) | `tokenize` hardwired **False** → lowercase **substring** containment; `|OR|` semantics is alternation of full candidates. An `|OR|` inside a ref never means literal text. |
| | else | `raise ValueError` (330–332). |

## 2. Branch census over the pinned 812-task population (JSON-derived, not AST-of-source)

651 `program_html` targets across 411 tasks (`eval_types` containing `program_html`).

- target `url`: `last` 238; site-placeholder navigation 338 (`__GITLAB__` 132, `__SHOPPING_ADMIN__` 90, `__REDDIT__` 85, `__SHOPPING__` 31); `func:` 75 (`func:reddit_get_post_url('__last_url__')` 65 on tasks 600–675 band; `func:shopping_get_latest_order_url()` 10 on tasks 436–510 band).
- `locator`: JS 524 (`document.` 519, `[...document` 5 on tasks 615–619 — `.map(...).join(' ')` string coercion), empty 105, `func:` 22 (all `gitlab_get_project_memeber_role`/`shopping_get_sku_latest_review_{rating,author}`).
- `required_contents`: `must_include` 463, `exact_match` 188, zero targets with both keys, zero extra keys. `must_include` list lengths 1–12 (median 1); literal `|OR|` used in exactly 5 refs (tasks 431, 750, 751, 755, 756 — none selected).
- `prep_actions`: 10 targets, all tasks 699–703 target indexes 3–4, all JS locators, all the same shopping-admin `.admin__collapsible-title` click.
- Selected-16 `program_html` users: 356 (3 targets), 389, 399, 424, 552, 556, 590 (3), 681, 759 (3) — 16 targets total; none use `func:` url/locator or `prep_actions`. Placeholder navigation urls appear in 389/552/556; `__GITLAB__`/`__REDDIT__` placeholders also appear inside `must_include` strings (552×5, 681×1) which are likewise preprocessor-dependent.
- Population edge cases for the audit: zero whitespace-prefixed locators; zero `func`-prefixed-but-not-`func:` urls; zero empty-locator+`exact_match`; zero HTML entities inside required refs; zero `__page__`/`__last_url__` misplacement (all 12 `__page__` occurrences are in `func:` locators; all `__last_url__` in `func:` urls).

## 3. Static AST vs running DOM — what the audit's "SCHEMA_COMPATIBLE" can and cannot assert

Provable statically (as implemented): required keys present, `locator`/`url`/`required_contents` types, locator belongs to one of the three dispatchable prefix classes, `required_contents` has a supported operator and value type, `prep_actions` is `list[str]`, `eval_types` known, population/ID/strata counts, deterministic selection equality.

Not provable statically — each remains a runtime/liveness unknown and must stay in case-report "unchecked" lists:

1. **Selector parseability by the browser's CSS engine.** Concrete specimen: `'[name="route_from"'` / `'[name="route_to"'` / `'[id="sidebar_content"'` — attribute selectors missing the closing `]`, present verbatim in raw JSON for tasks 356, 369–373, 424–430, 737–741, 757–767 (24+ targets; selected: 356, 424, 759). If `querySelector` throws, evaluators.py:292–294 converts it to `""` → `must_include` fails → **task permanently scores 0**. Whether Chromium tolerates the unclosed bracket is a browser-engine fact, undecidable from JSON+AST. Sibling reports Task356/Task424/Task759 flagged the same specimen independently.
2. **DOM existence/mutation at eval time.** `div#content select.routing_engines` option order (exact_match `"1"`), `.submission__inner`, `.block.start_date` presence — depends on deployed site build and the agent's final page state.
3. **`page.evaluate` result kind.** `page.evaluate` returning an element/undefined yields `JSHandle`/`None`; `str()` then produces a preview/`"None"` string — `must_include: ["none"]` would false-positive on `None`; no population task does this today, but schema cannot exclude it.
4. **`page.goto` success + 3 s sufficiency** for the 338 placeholder-navigated targets; also **whether the placeholder was substituted at all** — `page.goto("__GITLAB__/…")` raises `net::ERR` outside the guarded JS branch → crash, not fail-closed.
5. **`func:` helper liveness**: `shopping_get_*` issue live `requests` to `SHOPPING`/`SHOPPING_ADMIN` with admin creds and `assert status_code == 200` (helper_functions.py:52–56, 68–71, 85–88); `gitlab_get_project_memeber_role` itself does two `page.evaluate`s inside its own `try/except` → `""` (117–141). Network reachability/auth are runtime facts.
6. **`eval` resolution scope**: `eval(func)` uses module globals — only names imported at evaluators.py:18–27 resolve; AST can enumerate callables (audit could add this check) but JSON alone cannot.
7. **LLM judge paths** are unreachable inside `program_html` (`llm_fuzzy_match`/`llm_ua_match` only serve `StringEvaluator.fuzzy_match`/`ua_match`); static audit correctly notes external-LLM outcome unverified.
8. **Task validity**: presence of fields never shows the task is achievable/fair (e.g., 759 hardcodes "Boston" as Sophia Young's city — a data-currency assumption the JSON cannot validate). Field presence is schema, not truth.

## 4. Review of `plans/benchmark_spec_audit.py` HTML/locator handling

Verified-correct mirroring:

- `classify_locator` (audit 27–34) reproduces source branch order exactly: strip-empty→`full_page`, `document.`/`[...document.`→`javascript`, `func:`→`helper`, else `unsupported`. Matches evaluators.py:276–301 including the whitespace-only edge.
- `exact_match`-precedence comment (audit 127–128) faithfully mirrors the source `if/elif` (305/312).
- `prep_actions` shape check (audit 136) exceeds the source contract in a safe direction (source runs each entry blindly inside try/except; non-string entries are schema findings, not false negatives).
- `target_url_classes` navigation bucket (audit 116) correctly lumps placeholder+literal urls.
- `audit` only inspects `program_html` targets when `"program_html" ∈ eval_types` — matches `evaluator_router` (361–370): a stray `program_html` key without the eval_type is dead config; correct not to count.

Findings (severity order; all scoped to C1 audit quality, none rise to instrument-bug-blocking):

1. **MEDIUM — `target_url` classifier uses `url.startswith("func")` but the source splits `"func:"`.** Audit line 116 counts any url starting `func` as `helper`, but evaluators.py:264 does `split("func:")[1]` — a url like `"functional/x"` would be classified `helper` by the audit yet hit the `IndexError`-crashing `eval` path, or (without `func:`) be treated as a navigation url by the code? — No: the source guard is *also* `startswith("func")` (263), so a `funcX` url enters the func branch and then `split("func:")` lacks the delimiter → `[1]` IndexError → evaluation crash. So audit behavior matches source dispatch; the gap is that the audit does **not flag the latent crash** the source would produce. Recommend: keep `target_url_classes` as-is but add a schema finding `target_url_func_malformed` when `url.startswith("func") and not url.startswith("func:")`. Population incidence today: 0 (all 75 are `func:`), so this is a robustness check for the contract, not a count fix.
2. **LOW — no selftest cases exercise the three locator classes end-to-end.** `hand_html` (200–204) covers only `full_page` + `unsupported`. Missing hand-expected cases (see §5 for concrete additions): `func:`-locator classification, `document.`/`[...document` classification, whitespace-only locator → `full_page` (strip semantics), non-string locator → `locator_invalid`, `prep_actions` non-list/non-string → `prep_actions_invalid`, `required_contents` non-dict → `required_contents_invalid`, `exact_match` non-string value → `html_operator_value_invalid`. Current selftest cannot regress-cover half the dispatch table.
3. **LOW — `program_html_targets` metric counts locator-classified targets only** (`sum(counts["locator_classes"])`), so a non-string locator target would be undercounted vs the oracle's `len(targets)` (benchmark_oracle.py:32,36). Zero divergence on the pinned population (all 651 locators are strings); worth a comment or a `program_html_target_rows` metric independent of locator validity to keep oracle reconciliation robust under mutations.
4. **LOW — `eval`/`func:` reachability is schema-checked but never name-checked against the AST imports.** The audit parses evaluators.py for anchors (171–174) but does not cross-check that `func:` strings in task JSON name resolvable helpers. A cheap static win: extract `func:` call heads from task specs (65+10+22 occurrences) and verify the callee names appear in the `from evaluation_harness.helper_functions import (…)` set — all present today (`reddit_get_post_url`, `shopping_get_latest_order_url`, `gitlab_get_project_memeber_role`, `shopping_get_sku_latest_review_author`, `shopping_get_sku_latest_review_rating`). This is AST-of-source (allowed static evidence), not DOM truth.
5. **OBSERVATION — unguarded-call taxonomy.** The audit cannot express "crash vs fail-closed" per path; recommend case-report template rows record: JS-locator path = fail-closed (`""`), `func:` url/locator = crash-propagating, `goto`/`page.content` = crash-propagating, `prep_actions` = swallow-and-continue. This is the single most load-bearing semantic distinction for interpreting any future benchmark FAIL claims.

No defect found that would invalidate published counts; the 651/524/105/22 and 238/338/75 numbers my independent JSON census produced match the audit's intended metric keys.

## 5. Hand-expected schema/semantic cases recommended for `--selftest` (miniature fixtures)

Schema probes (`audit_tasks` level):

1. `{"url":"func:get_x('__last_url__')","locator":"","required_contents":{"must_include":["a"]}}` → no finding; `target_url_classes.helper==1`, `locator_classes.full_page==1`.
2. `{"url":"funcx","locator":"","required_contents":{"exact_match":"a"}}` → expected NEW finding `target_url_func_malformed` (if §4.1 adopted); currently must assert only class `navigation`? — under present code `url.startswith("func")` is True so `helper`; either way a test pins the contract.
3. `"locator":" document.querySelector('x').value"` (leading space) → `locator_unsupported` + source would `raise ValueError`; documents strip-vs-startswith asymmetry.
4. `"locator":"   "` → `full_page`.
5. `"locator":"func:gitlab_get_project_memeber_role(__page__, 'u')"` → `helper`; `__page__` placement check if added.
6. `"prep_actions": "document.x.click()"` (string not list) → `prep_actions_invalid`.
7. `"required_contents":{"exact_match":1}` → `html_operator_value_invalid`.
8. `"required_contents":{"exact_match":"a","must_include":["b"]}` → counted as `exact_match` only (precedence pin).
9. `{"url":"last","locator":"","required_contents":{"other":["x"]}}` → `html_operator_unsupported`.
10. Target `"locator"` missing key → `locator_invalid` (present code path, untested).

Semantic expectations for the 16 case reports (hand-derived from §1 contract; each is a *predicate trace*, not a DOM truth):

- 356 T1 `selectedIndex`→`str(evaluate)` `"1"` `exact_match` after `clean_answer` lower-case: passes only if engine dropdown index is literally 1. T2/T3 `route_from`/`route_to` `.value` → `must_include` substrings; **conditional on the unclosed-`]` selector being parsed** (§3.1) — record as conditional-pass predicate.
- 389/552/556 `url` placeholders → `page.goto` post-substitution, `page.content()` full HTML vs `must_include` lists; 552 also needs `__REDDIT__` substituted **inside ref strings** — a preprocessing assumption worth one line.
- 399 `.user-bio__biography.outerText` `exact_match "I am a robot"` → post-`clean_answer` comparison is case-insensitive `"i am a robot"`; note `html.unescape` on rendered text.
- 590 `.block.start_date` must_include `"Jan 16, 2030"` — literal year 2030 vs intent's 1/16/2023: flag as intent/ref tension (schema-valid, semantics questionable), do not count as validity.
- 681 `.submission__inner` must_include `"gan implementation"` AND `"__GITLAB__/eriklindernoren/PyTorch-GAN"` — the `__GITLAB__` inside a ref requires substitution for the check to be meaningful.
- 615–619-style `[...document` spread locators → `str(page.evaluate)` yields the `.join(' ')` string; cite as the only non-scalar-coercion JS path.

## 6. Required code/output checks recommended at integration (not run mid-flight)

- `python3 plans/benchmark_spec_audit.py --summary` → exit code and `locator_classes`/`target_url_classes`/`html_operators` histograms equal the §2 census (651 targets; `{"document…"}` 524 split as javascript, full_page 105, helper 22; urls last 238 / helper 75 / navigation 338; operators must_include 463 / exact_match 188).
- `--json` → `selected_task_ids` equals persisted `[389, 590, 132, 173, 44, 552, 681, 791, 556, 356, 7, 377, 759, 424, 97, 399]`; `findings` empty → exit 0.
- `--selftest` → add §5 cases; assert exit 0 and printed case list includes new names.
- Independent oracle (`plans/fixtures/r28/benchmark_oracle.py`) vs audit metrics must reconcile; note oracle's `program_html_targets` = raw target count vs audit's locator-counted variant (§4.3) — equal today, divergent under a non-string-locator mutant.
- Tamper controls: flip one byte in `test.raw.json` scratch copy → `snapshot_tampered` exit 2; mutate `selected-task-ids.json` → `selection_tampered`.
- Mutant probe worth one mutation test: inject `{"url":"last","locator":"window.alert(1)","required_contents":{"exact_match":"x"}}` into a scratch task → audit must emit `locator_unsupported`; inject `"func"` (no colon) url → pins §4.1 behavior.

## 7. Residual risk & verification gaps

- Browser parseability of the 24 unclosed-attribute selectors (affecting selected 356/424/759) is undetermined by any static means; if Chromium throws, these tasks are unpassable — a benchmark-observation candidate, gated on a future permitted dynamic check, never to be asserted from this audit.
- Whether the task-runner config pipeline substitutes `__GITLAB__`/`__REDDIT__`/etc. everywhere (urls, ref strings, `reddit_get_post_url` inputs) lives outside the pinned files; `browser_env` config code was intentionally not opened for this audit (fixture scope). The audit's placeholder census is literal, not a substitution guarantee.
- `str(page.evaluate(…))` of non-string JS results (numbers like `selectedIndex`, the 615–619 joins) is assumed per Playwright sync-API semantics; not verified against a live page — recorded as unverified library behavior.
- Static audit intentionally does not import `playwright`/`browser_env`; no dependency resolution was attempted.

## Verdict

**PASS (scoped)** — `HTMLContentEvaluator`'s locator dispatch, empty-locator full-page path, `func:` Python-eval paths, `|OR|`/`must_include`/`exact_match` operators, and the audit's schema checks were cross-verified against the pinned source and the 812-task JSON; audit classification logic faithfully mirrors the upstream dispatch (one MEDIUM robustness gap §4.1, three LOW gaps §4.2–4.4, all non-count-affecting on the pinned population). Static inventory cannot prove browser selector parseability, DOM presence, navigation/API liveness, or task validity — the 24-task unclosed-selector stratum is flagged as a runtime-conditional benchmark observation, not a static FAIL. This verdict covers only the HTMLContentEvaluator contract slice of C1; it is not a round-level or benchmark-validity verdict.

Limitations carried: no dynamic/browser evidence; sibling seat reports (Task356/Task424/Task759) cover per-case predicate detail; placeholder-substitution mechanism outside pinned fixture scope.

# FTask759 — author-side falsification of BUILD case759 (WebArena task_id 759)

Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
Target under test: `.ufo/waves/round-28/build/Task759.md`
Raw case: `plans/fixtures/r28/webarena/config_files/test.raw.json`, task_id 759, lines 27352–27404
Frozen candidate: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`
Candidate SHA256 (recomputed 2026-10-21): `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` — equals the frozen value.
Canonical candidate `corpus/knowledge/webarena-task-spec-audit.md` is **not admitted** (read as the named prospective target only; file not present/edited).
Scope: case 759 only, static source bytes. No C2, no other case, no production edit.

## 0. Method and provenance

- Read-only over production. No installs/updates (tool log: none). No browser opened, no benchmark-site request, no upstream Python imported or executed, no REA MCP.
- Commands on the pinned snapshot only: `sha256sum`, `wc -c`, `python3` (`json.load` + line-numbered text print), `grep -n`, `sed -n`, `find`.
- Static disagreement is reported as such. Runtime-validity claims are left unresolved; no scorer/browser run was performed.

Pin (all recomputed values equal `manifest.json`):

| file | full SHA256 | bytes |
|---|---|---|
| `config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | 880776 |
| `evaluation_harness/evaluators.py` | `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22` | 13264 |
| `evaluation_harness/helper_functions.py` | `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275` | 7565 |
| `LICENSE` | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` | 11357 |

Upstream URL (manifest, opened 2026-10-21): `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json`. `LICENSE` is Apache-2.0 (`Apache License` / `Version 2.0` present). The build's truncated digests `7b50386f…02537652`, `e23edb39…00c22`, `ec758da4…e275` all match the full hashes above.

## 1. Raw case-759 facts (observed, line-exact)

| field | value | line |
|---|---|---|
| task block open / close | `{` … `},` | 27352 / 27404 |
| sites | `["map","shopping_admin"]` | 27353–27356 |
| task_id | 759 | 27357 |
| require_login / require_reset | true / false | 27358 / 27368 |
| start_url | `__MAP__` | 27360 |
| intent (also the authored quote) | "Show me the route and driving time from the city where my E-commerce customer Sophia Young lives to New York City" | 27367 |
| eval_types / reference_answers / reference_url | `["program_html"]` / null / `""` | 27370–27372 / 27373 / 27374 |
| intent_template_id | 42 | 27403 |

Target objects (corrected ranges; the build's §4 ranges are wrong, see D1):

| # | range | url | locator | required_contents |
|---|---|---|---|---|
| T1 | 27376–27382 | `last` | `document.querySelector("div#content select.routing_engines").selectedIndex` (27378) | `exact_match "1"` (27380) |
| T2 | 27383–27391 | `last` | `document.querySelector('[name="route_from"').value` (27385) | `must_include ["Boston"]` (27388) |
| T3 | 27392–27400 | `last` | `document.querySelector('[name="route_to"').value` (27394) | `must_include ["New York"]` (27397) |

No `prep_actions`, no `func:` locator, no `func` URL, no OR list element (`" |OR| "`) anywhere in the case.

## 2. Scorer path (observed, all anchors verified)

`evaluators.py` (sed ranges re-numbered and checked one by one):

- Router `356–374`; `program_html` at `369–370` appends only `HTMLContentEvaluator`. `EvaluatorComb.__call__` `342–353` starts at 1.0 and multiplies (`351`). With one evaluator, task score = HTML score.
- `HTMLContentEvaluator.__call__` `248–333`: `targets = ...` at 258; score 1.0 at 259; `func` URL branch `263–266` guarded by `target_url.startswith("func")` (false because all urls are `last`); goto+sleep `271–273` guarded by `target_url != "last"` (false); `document.` branch `279–294`; `str(page.evaluate(f"() => {locator}"))` at 289; `except Exception: selected_element = ""` at `292–294`; `html.unescape` at 303.
- `exact_match` `305–310` → `StringEvaluator.exact_match` `90–94` → `clean_answer` `80–86` (strip, one quote pair, lowercase). `must_include` `312–327` splits each element on `" |OR| "` (316) and calls `StringEvaluator.must_include(tokenize=False)` `98–111` (lowercased `clean_ref in clean_pred`).
- `StringEvaluator` class `71–170`; routed pre-clean of `pred` at 134. No helper/LLM path is reachable from this case; `helper_functions` is reached only by the import block `18–27`.

Consequence: the case score is the product of three deterministic DOM predicates; **any** `page.evaluate` exception substitutes `""` and then fails closed (0), so the task can be scored 0 by selector parsing alone, independently of agent behavior.

## 3. Intent → predicate completeness

Every intent element is mapped; nothing in the authored intent is silently dropped.

| intent element | check | unchecked remainder |
|---|---|---|
| "driving" mode | T1 engine `selectedIndex == "1"` via exact_match on `str(...)` | what index 1 means; whether a route was computed with it |
| origin "city where my E-commerce customer Sophia Young lives" | T2 `route_from`.value contains "boston" (case-insensitive substring) | that Boston is Sophia Young's city; which Boston; whether `shopping_admin` was consulted |
| destination "New York City" | T3 `route_to`.value contains "new york" | "City" not enforced ("New York State"/"New York Ave" pass) |
| "show me the route" | none | rendered directions/route/result panel/URL |
| "driving time" | none | displayed duration; also no answer string (`reference_answers: null`) |

The build's §4 table contains all five rows plus the template lines; that mapping is complete and source-correct. The 1.0-iff-all-three statement is correct (multiplicative product).

## 4. Independent numeric/census checks (derived from raw JSON, no production import)

| claim | source of claim | independent result |
|---|---|---|
| 17 `routing_engines` targets, 11 expect `"1"`, 6 expect `"2"` | build §5 | exact: 11×`{exact_match:"1"}`, 6×`{exact_match:"2"}`; the six are 761 and 763–767 |
| 762 is a driving-options task expecting `"1"` | build §5 | yes ("using driving options") |
| template 42 = 757, 758, 759, 760; all three-target | build §2 | exact; all four use `exact_match "1"` and two unclosed selectors each |
| stratum `(('map','shopping_admin'),('program_html',))` = {759,760}; 759 minimum | build §2 | exact; only tasks 759/760 have both sites |
| frozen selection rule → 16 IDs | build §2, candidate | 27 strata, sorted minima reproduce `selected-task-ids.json` **exactly**; 759 is the 13th of 16, minimum of {759,760} |
| candidate metrics 812/5 sets/27/651/188+463/105+524+22/238+338+75/45+176+118 | candidate §Observed | all exact: IDs 0–811 no gaps; sets 325/66/282/10/129; 651 targets; 188 and 463 with zero overlap; locators 105/524/22; URLs 238/338/75; 45/176/118 (4 tasks have fuzzy+must coexistence) |
| candidate: selected cases omit func locator/URL, prep_actions, OR alternatives | candidate §case audits | exact for all 16 (no witnesses) |
| candidate: "the shopping site is omitted" | candidate §case audits | literal site id `shopping` absent; selected union = {gitlab, map, reddit, shopping_admin, wikipedia} (wording caveat D4) |
| candidate: Task356/759/424 have unclosed attribute-selector brackets | candidate §disagreements | exact and **discriminating**: 214 unbalanced selector locators in 119 tasks; among the 16 selected cases the intersection is exactly {356 (2), 424 (1), 759 (2)} |

## 5. Defects found in the build report

**D1 (real, bibliographic). The §4 "Target (raw line)" ranges are wrong for all three targets.**
Corrected: T1 `27376–27382` (build: 27377–27382), T2 `27383–27391` (build: 27383–27390), T3 `27392–27400` (build: 27391–27398). T3's stated range even begins on T2's closing brace and ends on the `]` of T3's list. The individually cited anchor lines (locator 27378/27385/27394; operator 27380/27388/27397) are all exact, so no semantic conclusion depends on the broken ranges.

**D2 (minor, unsourced descriptor).** §5 calls the front-end "Map (OpenStreetMap-style)". The pinned snapshot contains no map config/HTML (only `__MAP__` in raw tasks); "OpenStreetMap" is not established by pinned bytes. It is descriptive and non-load-bearing, and no case predicate depends on it.

**D3 (terminology, not an error).** §4 writes `String(selectedIndex)`; the code is Python `str()` of the Playwright result. Identical for the numeric `1`; no behavioral difference.

**D4 (wording caveat).** Candidate "the shopping site is omitted" is true for the WebArena site id `shopping`, but the selected set does contain `shopping_admin` (759/760). A reader could over-read this as "e-commerce omitted"; not a factual error.

Not defects after checking: "every target has url `last`, so the `func:` eval is skipped" is causal but sound (`"last".startswith("func")` is false); the 3-second sleep and goto are indeed skipped; "any exception becomes empty" matches `292–294`.

## 6. Decisive boundary / controls

**Boundary B1 — the unclosed-selector fork (case-specific and decisive).** T2/T3 selectors omit the closing `]` (`[name="route_from"`, `[name="route_to"`). Under the pinned code, if the browser rejects the selector, `querySelector` throws, the handler at `292–294` sets `""`, and both `must_include` checks fail ⇒ score 0 for **every** trajectory. If Chromium accepts it, the two `.value` substrings are checked ⇒ a trajectory that only types the two city names and sets engine index 1 reaches 1.0 without computing or rendering any route or driving time. The build states this fork and does not resolve it; that refusal is correct, and the fork is the case's only decisive validity boundary. It is **unresolved here** (no browser permitted).

**Control C1 — selection representativeness.** Independent recomputation of the 27 strata minima yields exactly the persisted 16 IDs, with 759 the minimum of the only map+shopping_admin program_html stratum {759,760}. The audited case is the intended representative, not a non-selected or duplicate task; 760 differs in its reference literals (Allentown / Hoboken, New Jersey), so the audit is not a duplicate-map.

**Control C2 — inferred engine index.** The 17-target census (11×"1" for route/driving variants; 6×"2" for 761/763–767 walking/walkway variants; none expecting "0") is a population-wide structural control that supports — but does not prove — index 1 = driving. The build marks it `[INFERENCE]`; that label is warranted.

**Control C3 — bracket-defect precision.** Population-wide the unclosed pattern appears in 214 locators / 119 tasks, but among the 16 selected cases only {356, 424, 759}; this exactly matches the candidate's named trio and shows the audit case was not selected to manufacture a defect.

## 7. Candidate case-specific language vs source

The candidate mentions 759 in: (a) the case-table row "route inputs not duration"; (b) "Task356/759/424: the locators contain unclosed attribute-selector brackets in source"; (c) the persisted selected-ID list. All are supported by pinned bytes (a: three targets are engine index + two input-field substrings, no duration/DOM-route predicate; b: verified both; c: verified). Its adjacent meta-claims — helper line cites `146–173`, `176–208`, `161–173`, `196–208`; `StringEvaluator:71–170`, `URLEvaluator:173–241`, `HTMLContentEvaluator:244–333`, `combination/router:336–374`; N/A assignment at 159 — are also line-exact on the pinned bytes. No case-759-specific candidate sentence turns an unobserved runtime condition into success/failure; the candidate explicitly says bracket rejection is not inferred and runtime DOM is untested.

## 8. Unresolved (not claimed)

- Chromium/Playwright parse outcome for `[name="route_from"` / `[name="route_to"` (B1).
- Whether Sophia Young's `shopping_admin` city is Boston at evaluation time (`require_reset: false`).
- Map build's option order/labels at index 1.
- `route_from`/`route_to` values after map-click vs typed entry.
- Which page/tab the (unpinned) run loop passes for two-site tasks.
- Whether a route/duration was actually rendered.
- Production instrument `benchmark_spec_audit.py` was **not** run by this seat; schema-findings 0 and selftest-21 remain producer claims, not re-exercised. The JSON-derivable counters above were recomputed independently from raw bytes.

## Verdict

Semantic case audit: **PASS** — every target, operator, unchecked clause, line anchor, and numeric claim reproduces from the pinned bytes; the candidate's 759 language does not exceed source. Bibliographic metadata: three §4 target ranges in `build/Task759.md` are off by one line each (D1); one unsourced descriptor (D2).

VERDICT: PARTIAL

# Task759 — WebArena task_id 759 static intent→evaluator case audit

Writer/seat: KengakuR28.Task759-2 (read-only scout, author-side advice; not outside non-author closure).
Scope: C1 only, case 759 of the frozen 16-ID selection. No C2 content.
Final scoped verdict: **PASS** for the static case mapping deliverable. Task validity itself: **UNDETERMINED** (neither valid nor invalid; runtime evidence listed in §6 is required).

## 1. Inputs and provenance

Snapshot root: `plans/fixtures/r28/webarena` (upstream `dce04686a56253aefba7b18a4fa0937cf1dc987b`, per `manifest.json`). Local sha256 recomputed and equal to manifest values:

| File | sha256 | Manifest URL (opened 2026-10-21 per manifest) |
|---|---|---|
| `config_files/test.raw.json` | `7b50386f…02537652` | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json |
| `evaluation_harness/evaluators.py` | `e23edb39…00c22` | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py |
| `evaluation_harness/helper_functions.py` | `ec758da4…e275` | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/helper_functions.py |

Access: local pinned snapshot read 2026-10-21; this seat did not contact the URLs or any benchmark site.

Located quotes (≤25 words, data only):
- `test.raw.json:27367`: "Show me the route and driving time from the city where my E-commerce customer Sophia Young lives to New York City"
- `evaluators.py:289`: `selected_element = str(page.evaluate(f"() => {locator}"))`
- `evaluators.py:271`: `if target_url != "last":`

Observed commands (all read-only, on local data; upstream Python was never imported or executed): `sha256sum` on the three files; `python3` `json.load` of `test.raw.json` to extract task 759, its stratum, template-42 siblings and `routing_engines` targets; `grep -n` and `sed -n` for line anchors. No tools were installed or updated.

## 2. Task facts (`test.raw.json:27352–27404`)

| Field | Value | Line |
|---|---|---|
| sites | `["map","shopping_admin"]` | 27353 |
| require_login / require_reset | `true` / `false` | 27358 / 27368 |
| start_url | `__MAP__` | 27360 |
| intent_template_id | 42 | 27403 |
| eval_types | `["program_html"]` | 27370–27372 |
| reference_answers / reference_url | `null` / `""` | 27373 / 27374 |

Stratum `(("map","shopping_admin"),("program_html",))` contains exactly `[759, 760]`, so 759 is the minimum ID and matches the frozen selection rule. Template 42 siblings are 757, 758, 759 and 760, and all four share the same three-target shape.

## 3. Scorer path (pinned `evaluators.py`)

- Router (`356–374`): `program_html` routes to `HTMLContentEvaluator` only (`369–370`). No `StringEvaluator` or `URLEvaluator` runs. `EvaluatorComb` multiplies the scores (`348–352`).
- `HTMLContentEvaluator.__call__` (`248–333`): the score starts at 1.0 and is multiplied by each target. Every target has `url: "last"`, so the `func:` URL `eval` (`263–266`) is skipped and so is `page.goto` plus the 3-second sleep (`271–273`). The locator runs on whatever `page` the harness passes in at the end.
- Every locator starts with `document.`, so it runs through `page.evaluate` (`279–294`). There are no `prep_actions`. Any exception becomes `""`, which fails closed. The result then goes through `html.unescape` (`303`).
- `exact_match` (`305–310`) calls `StringEvaluator.exact_match` (`90–94`), which compares `clean_answer` on both sides: strip, remove one pair of surrounding quotes, lowercase (`80–86`).
- `must_include` (`312–327`): each list item is split on `" |OR| "`. `StringEvaluator.must_include(tokenize=False)` (`98–111`) does a lowercase substring test.
- `helper_functions.py`: task 759 calls none of it. It has no `func:` URL or locator, and no `llm_fuzzy_match`/`llm_ua_match`, so there is no LLM judge. The file is only reached through the import at `evaluators.py:18–27`.

## 4. Case table: intent → operator/target

| # | Intent element | Target (raw line) | Locator | Operator / reference | What passes | Not checked |
|---|---|---|---|---|---|---|
| T1 | "driving" mode | 27377–27382 | `document.querySelector("div#content select.routing_engines").selectedIndex` (27378) | `exact_match "1"` (27380) | `String(selectedIndex)` equals `"1"` | What option 1 means: the option order and labels are not in the snapshot. Whether a route was actually computed with that engine. |
| T2 | origin is "the city where my E-commerce customer Sophia Young lives" | 27383–27390 | `document.querySelector('[name="route_from"').value` (27385) | `must_include ["Boston"]` (27388) | `"boston"` is a lowercase substring of the from-field value | That Boston really is Sophia Young's city in the live shopping_admin data (the value is hard-coded). Which Boston it is; any string containing "boston" passes. Whether the agent consulted shopping_admin at all. |
| T3 | destination "New York City" | 27391–27398 | `document.querySelector('[name="route_to"').value` (27394) | `must_include ["New York"]` (27397) | `"new york"` is a substring of the to-field value | "City" is not enforced: "New York State" or "New York Ave, …" also pass. |
| — | "show me the route" | none | — | — | — | No check of the rendered directions, the route line, the result panel, or the URL. |
| — | "driving time" | none | — | — | — | No check of the displayed duration and no answer-string check (`reference_answers: null`). |

The task scores 1.0 only if T1, T2 and T3 all score 1.

## 5. Dynamic state and judge dependencies

- **shopping_admin database:** the "Boston" ground truth assumes the customer record for Sophia Young at evaluation time. With `require_reset: false`, it can drift if the shared environment changes. [INFERENCE]
- **Map (OpenStreetMap-style) front-end DOM:** the scorer depends on the `div#content select.routing_engines` element, its option order (index 1), and inputs named `route_from` and `route_to` in the deployed map build.
  - Sibling evidence (static): across all 17 `routing_engines` targets, 11 expect `"1"` for route or driving intents (including 762 "using driving options") and 6 expect `"2"` for walking intents (761, 763–767). This is consistent with index 1 being the car engine. [INFERENCE: label not observed]
- **Field-value semantics:** T2 and T3 read the raw `.value` of the input fields. If the map front-end puts coordinates or a geocoder name without "Boston" into the field (for example after setting an endpoint by clicking or dragging on the map), a correct route would score 0. [INFERENCE]
- **Selector syntax:** both T2 and T3 selectors lack the closing `]`. 759 shares this with every template-42 sibling. Whether Chromium accepts the unclosed attribute selector at end of input is not proven here; if it does not, the exception handler at `292–294` sets `""` and the task can never be passed. [INFERENCE; runtime check required]
- **Which page is scored:** this is a two-site task, so `page` must be the map tab at the end. Which tab the harness passes is set outside the snapshot (run loop not pinned).
- **Judges:** there is no LLM judge and no helper/API call. Scoring is deterministic given the final DOM.

## 6. Runtime evidence required before declaring valid or invalid

1. The shopping_admin customer record for Sophia Young (city) in the reset environment image.
2. The deployed map build's `select.routing_engines` option list, showing the label at index 1.
3. A Chromium/Playwright result for `querySelector('[name="route_from"')`: element or SyntaxError.
4. The map front-end's `route_from`/`route_to` values after typed and after map-click endpoint entry, once the route is computed.
5. Which page or tab the pinned run loop passes to the evaluator in multi-site tasks.
6. Trajectory evidence that a route and duration were rendered. The scorer does not check this.

## 7. Potential validity limitation (task-specific, not a proven defect)

Task 759's score depends only on two input-field substrings and one dropdown index.
- **Possible false positive:** typing "Boston" and "New York", then selecting engine index 1 without computing or showing a route or driving time, could pass. Neither the shopping_admin lookup nor the actual route is verified.
- **Possible false negative:** coordinate-filled fields, a different engine order, or strict-selector rejection would score a correct route as 0.

## 8. Limitations of this report

- This is static source evidence only, not browser-level truth. No upstream execution and no site contact.
- The `[INFERENCE]` items are unverified.
- The sibling-index pattern is structural correlation, not endorsement (Q13).
- No new source row and no knowledge admission.

Verdict: **PASS** (scoped static case-759 mapping complete); task validity **UNDETERMINED** pending §6.

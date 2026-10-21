# Task424 — WebArena task_id 424 intent→scorer case audit (round28 C1, author-side)

Writer/seat: KengakuR28.Task424-2 (read-only scout seat). Author-side advice only; not outside, non-author closure.
Scope: one task (424) from the frozen selection; static source reading of the pinned snapshot only. No upstream code was executed, imported, or evaluated. No benchmark site was contacted and no browser action was taken.
Scratch evidence: `.ufo/waves/round-28/scratch/Task424/census.txt`. It holds a stdlib JSON parse of the data file and sha256 values.

## Snapshot identity (verified against `plans/fixtures/r28/webarena/manifest.json`, upstream `dce04686a56253aefba7b18a4fa0937cf1dc987b`)

| file | sha256 (observed = manifest) |
|---|---|
| config_files/test.raw.json | 7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652 |
| evaluation_harness/evaluators.py | e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22 |
| evaluation_harness/helper_functions.py | ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275 |

## Source openings (accessed 2026-10-21; local pinned copy, URL from manifest)

| ref | URL | located quote (≤25 words) | scope |
|---|---|---|---|
| raw | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json | L13337: `"locator": "document.querySelector('[id=\"sidebar_content\"').outerText",` | task 424 record, L13317–13346 |
| eval | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py | L271: `if target_url != "last":` ; L293–294: `# the page is wrong, return empty` / `selected_element = ""` | router, EvaluatorComb, HTMLContentEvaluator, StringEvaluator helpers |
| help | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/helper_functions.py | L211: `class PseudoPage:` | imports and PseudoPage only; no helper function is reached by task 424 |

## Task record (raw L13317–13346)

- intent (L13326): "Find the page of the place where Mr. Rogers was filmed on the map." Template 371 (L13346): "Find the page of {{description}} on the map." The description is "the place where Mr. Rogers was filmed".
- sites `["wikipedia","map"]`; start_url `__MAP__` (L13320); require_login `true` (L13318); storage_state `null` (L13319); require_reset `false`; geolocation `null`.
- eval_types `["program_html"]` (L13329–13331); reference_answers `null` (L13332); reference_url `""` (L13333).
- program_html has one target. url `"last"` (L13336). The locator is shown above (L13337). required_contents is `{"must_include": ["Pittsburgh"]}` (L13338–13340).

## Case table (intent → evaluator operator/target)

| # | intent element | scorer path (exact anchor) | operator / target | checked? |
|---|---|---|---|---|
| 1 | Whole task scored by the program_html type | `evaluator_router` eval L356–374; `case "program_html"` L369–370 → `HTMLContentEvaluator()` | one evaluator; `EvaluatorComb` product L348–352 | yes, the score is the product of one factor |
| 2 | "…on the map": final page state | L262 `target_url = target["url"]` = `"last"`; L263–266 `func:` branch not taken; L271–273 `goto`+`sleep(3)` skipped | evaluates the agent's final `page` as is, with no navigation and no wait | final page only |
| 3 | "Find the page of …": the selected place's sidebar | L279–281 `document.` branch; L282–287 `prep_actions` absent; L289 `str(page.evaluate(f"() => {locator}"))` | JS `document.querySelector('[id="sidebar_content"').outerText` | text of the element with id `sidebar_content`, as rendered |
| 4 | Evaluation failure | L290–294 `except Exception: selected_element = ""` | JS error or null element gives empty text (fails closed) | an empty result scores 0 |
| 5 | Text normalization | L303 `html.unescape`; `clean_answer` L80–86 (strip, strip one pair of surrounding quotes, lowercase) on both ref and pred | case-insensitive | — |
| 6 | "the place where Mr. Rogers was filmed" | L312–327 `must_include`; L316 split on ` |OR| ` (none present); L319–323 `must_include(ref, pred, tokenize=False)` → L111 `clean_ref in clean_pred` | raw substring `"pittsburgh"` in the lowercased sidebar text | substring only |
| 7 | Agent's final answer string | StringEvaluator (L71–170) is not routed (no `string_match`); `reference_answers` is null | none | **unchecked** |
| 8 | Final URL | URLEvaluator (L173–241) is not routed; `reference_url` is `""` | none | **unchecked** |
| 9 | Use of the wikipedia site (listed in `sites`) | no evaluator reads trajectory or site history | none | **unchecked** |
| 10 | Helper functions / LLM judge | helper imports eval L18–27; `llm_fuzzy_match` help L146, `llm_ua_match` help L176 are unreachable; no `func:` url or locator | none | no judge dependency |
| 11 | `page` type | beartype `page: Page \| PseudoPage` eval L252; help L211–221 overrides only `.url` and delegates `evaluate` | `evaluate` runs on the original page | n/a (`url` is unused because target is `"last"`) |

## Checked vs unchecked properties

- **Checked:** at score time, the final page has an element with `id="sidebar_content"`, and its `outerText`, case-folded and HTML-unescaped, contains the substring `pittsburgh`.
- **Unchecked:** the agent's answer text and stop action content, the final URL, and whether the shown object is a specific place. The scorer cannot tell a search-results list, a directions panel, a city or relation page, an unrelated feature whose address mentions Pittsburgh, or a WQED/studio feature apart. Wikipedia use, the trajectory, and intermediate steps are also unchecked. Matching is case-insensitive and not on word boundaries, so any longer token that contains "pittsburgh" also passes.
- **Intent-vs-target granularity:** the intent asks for "the page of the place", but the target accepts any sidebar text that mentions a city. [INFERENCE] The commonly cited filming location, WQED studios, is inside Pittsburgh, so a correct specific page would likely pass. A coarser page would pass too. This is permissiveness, not a proven defect.

## Dynamic state / runtime dependencies

1. A live OSM-style map instance at the URL that replaces `__MAP__` in the generated configs. The generation step is not in the snapshot, so this is unverified.
2. The map front-end must render a DOM element `id="sidebar_content"`. That id is a property of the deployed map software and is not in the snapshot ([INFERENCE]).
3. The geocoder/search and feature data on that instance must include a Pittsburgh-tagged result.
4. `outerText` depends on rendering. Hidden descendants are excluded, and a non-rendered element falls back to textContent ([INFERENCE] from the HTML spec; not opened this round).
5. Timing: url `"last"` skips the 3-second sleep (L271–273). If the sidebar fills asynchronously when evaluation runs, the text may be stale or partial.
6. No LLM judge, no helper API, and no login state is used by the scorer. `require_login: true` with `storage_state: null` is shared by all 128 map tasks (scratch census) and is not read by evaluators.py.

## Task-specific potential validity limitation (not a proven defect)

The locator's CSS selector string is `[id="sidebar_content"`. It has an opening `[` but no closing `]` (raw L13337, byte-exact in the census). Whether it works depends on the browser's selector parser:

- **If the browser tolerates the unclosed block** (CSS Syntax treats EOF inside a simple block as a recoverable parse error; [INFERENCE], spec not opened this round), the locator selects the sidebar and the case works as described above.
- **If `querySelector` throws `SyntaxError`**, L292–294 turns the error into `""`. Every trajectory then scores 0, so the task would be unsolvable. It would fail closed, never pass falsely.

The same selector appears in all 12 `sidebar_content` tasks (369–373, 424–430), and template 371 covers 424–430. A rough bracket-count scan, kept in scratch and not part of the audit tool, flags many other locators with the same unclosed-attribute pattern across about 114 task IDs. [INFERENCE] A pattern that widespread suggests the authors' Chromium/Playwright stack tolerated it, but that is not evidence. The second limitation is the permissive substring target (table rows 6–9).

## Runtime evidence required before declaring 424 valid or invalid

1. The browser/Playwright versions actually pinned, plus an offline, non-benchmark test showing whether `document.querySelector('[id="x"')` returns the element or throws in that engine.
2. The deployed map front-end's DOM, confirming `id="sidebar_content"` exists and holds the place-details panel.
3. A reference trajectory's final-page `outerText` showing "Pittsburgh" present after asynchronous loading, plus one wrong-place control (such as a non-Pittsburgh feature page) scoring 0.
4. Whether the intended place has a distinct feature page on that instance's data. Without that, the "specific place" granularity cannot be assessed.

None of these were collected, because site contact and browser execution are forbidden this round.

## Commands observed

- `sha256sum` on the three snapshot files (they match the manifest).
- `jq`/`python3` stdlib `json.load` on the raw data file: task 424 extraction, siblings with `sidebar_content`, template 371 members, and a bracket-count scan. These parse data only; no upstream code was imported or run.
- `grep`/`sed` reads of the evaluators.py and helper_functions.py line ranges cited above.
- No installs or updates.

## Limitations

- This is static reading only. Browser-level selector behavior, the DOM, data, and timing are [INFERENCE] or unresolved.
- The `__MAP__` substitution and the runner (`run.py`, `browser_env`) are not in the snapshot.
- The HTML and CSS specs were not opened as sources this round, so the claims about `outerText` and unclosed-block behavior are labeled inference.
- The roughly 114-task scan is a crude heuristic and not an instrument count.
- This is one deliberately chosen case. It says nothing about task validity in general.

## Verdict

**PASS (scoped):** the static intent→evaluator mapping for task 424 is complete and source-anchored. The scorer path is fully determined: `program_html` → `HTMLContentEvaluator`, final page, the sidebar locator, case-insensitive substring `pittsburgh`, and no judge or helper.
**Task validity: UNRESOLVED.** Runtime evidence items 1–4 are required first. The unclosed selector bracket and the city-level substring target are disclosed as potential limitations, not defects.

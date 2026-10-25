ATTACKS: round-28 C1 case audit `build/Task424.md` (raw task_id 424, WebArena pinned snapshot) against frozen candidate `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md` SHA256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` and upstream revision `dce04686a56253aefba7b18a4fa0937cf1dc987b`
Seat KengakuR28.FTask424 (leaf, author-side). Read-only over production; no source/candidate/lane edit. No upstream import/exec/eval, no scorer run, no browser, no benchmark-site request. Scratch: `.ufo/waves/round-28/scratch/FTask424/census.txt`. Installs: none.

## 1. Identity reopened

Manifest row values equal observed bytes; all three source hashes and LICENSE verify (the draft hash also equals the assigned one; canonical `corpus/knowledge/webarena-task-spec-audit.md` is absent, i.e. not admitted).

| file | bytes / lines | sha256 observed = manifest |
|---|---|---|
| config_files/test.raw.json | 880776 / 29604 | 7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652 |
| evaluation_harness/evaluators.py | 13264 / 374 | e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22 |
| evaluation_harness/helper_functions.py | 7565 / 221 | ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275 |
| LICENSE | 11357 | c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4 |
| draft candidate | 12405 | 77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8 |

Task 424 occupies raw L13312 (opening brace) through L13347 (closing brace): sites L13313–L13316, task_id L13317, require_login L13318, storage_state L13319, start_url L13320, geolocation L13321, intent_template L13322, instantiation_dict L13323–L13325, intent L13326, require_reset L13327, eval L13328, eval_types L13329–L13331, reference_answers L13332, reference_url L13333, program_html L13334, url L13336, locator L13337, required_contents L13338–L13340, intent_template_id L13346.

## 2. Intent → predicate replay — every one of the 11 case rows verifies

All anchors were re-opened at the byte level in the pinned copies (not the candidate's restatement). "V" = claim matches source.

| row | case claim | observed source | result |
|---|---|---|---|
| 1 | router L356–374, `case "program_html"` L369–370 → HTMLContentEvaluator; one evaluator; product L348–352 | L356 `def evaluator_router`, 369–370 program_html→`HTMLContentEvaluator()`, 348–352 `score *=` loop | V |
| 2 | L262 `target_url` = "last"; 263–266 `func:` branch not taken; 271–273 goto/sleep skipped | 262 `target_url: str = target["url"]`, 263 `startswith("func")`, 271 `if target_url != "last":`, 272 goto, 273 sleep(3) | V |
| 3 | 279–281 `document.` branch; 282–287 prep_actions absent; 289 evaluate | 279–281 condition, 282 `if "prep_actions" in target:`, 288–289 try/evaluate. Target dict keys are exactly url/locator/required_contents → no prep_actions | V |
| 4 | L290–294 `except Exception: selected_element = ""`; empty → 0 | 290–291 `if not selected_element: selected_element = ""`; 292 `except Exception:`; 294 `selected_element = ""`; `must_include` → 0.0 (control below) | V behavior; anchor over-wide (F2) |
| 5 | L303 unescape; clean_answer L80–86 strip/one quote pair/lower, both ref and pred | 303 `html.unescape`, 81–86 exactly those steps, applied at 99–100 | V |
| 6 | 312–327 must_include; 316 split `" \|OR\| "`; 319–323 tokenize=False; L111 substring | 312 `elif "must_include"`, 316 `content.split(" \|OR\| ")`, 319–323 call, 111 `float(clean_ref in clean_pred)`; content has no OR | V |
| 7 | StringEvaluator L71–170 not routed; reference_answers null | class 71, `__call__` ends 170; eval_types only program_html; L13332 null | V |
| 8 | URLEvaluator L173–241 not routed; reference_url "" | class 173, return 241; L13333 `""` | V |
| 9 | no evaluator reads trajectory/site history | routed HTMLContentEvaluator never touches `trajectory`; EvaluatorComb only forwards it at 350 | V |
| 10 | helper imports eval L18–27; llm_fuzzy_match L146 / llm_ua_match L176 unreachable; no `func:` url or locator | 18–27 import block; def 146 and def 176; url "last", locator starts "document." | V (call-level; see F4/import note) |
| 11 | beartype page L252; PseudoPage L211–221 url only, evaluate delegated | 252 `page: Page \| PseudoPage`; 211–221 `__getattr__` delegates all but `url` | V |

The rest of the case's checked/unchecked split is source-true: the routed operator is `must_include(ref="Pittsburgh", pred=outerText, tokenize=False)` after unescape + clean; `reference_answers`/`reference_url` and the trajectory are never consulted.

## 3. Population and numeric claims

Independently derived from the raw JSON (no production instrument, no oracle import):

- 812 tasks / 812 distinct IDs, IDs 0–811, no duplicate/missing.
- evaluator-type sets: string_match 325, program_html 282, url_match 66, string_match+url_match 10, program_html+url_match 129 (sum 812, 5 sets).
- 27 strata; first-16 minima reproduce the persisted order exactly: 389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399. Task 424 is the true minimum of stratum (map,wikipedia)×(program_html); `selected-task-ids.json` matches.
- page-content targets 651; effective operators exact_match 188 + must_include 463; locator classes full-page 105 / JavaScript 524 / helper 22; target-URL classes last 238 / navigation 338 / helper 75.
- string approach task counts exact_match 45 / must_include 176 / fuzzy_match 118.
- Task-424-local claims: 128 map tasks, all `require_login: true` and `storage_state: null`; exactly 12 `sidebar_content` tasks (369–373, 424–430) with one distinct locator string; `intent_template_id 371` = 424–430; one program_html target; required_contents exactly `{"must_include": ["Pittsburgh"]}`.
- The "about 114 task IDs" bracket heuristic reproduces exactly under the plain unbalanced-bracket rule: 209 locator occurrences / 114 distinct task IDs / 27 distinct locator strings, every one an unclosed `querySelector('[name=...`-style attribute selector. (A stricter "attribute selector truncated at EOF" definition gives 89 IDs; the case's "rough/about" wording covers the plain count.)

Candidate metrics re-derived independently all match the candidate's table (651, 188+463, 105/524/22, 238/338/75, 45/176/118, 812/812, 27/16).

## 4. Decisive boundary/control

Ref, `"Pittsburgh"`. Predicate hand-reimplemented from L80–86/L98–111 only (upstream never imported or executed):

| final sidebar text | cleaned pred | score |
|---|---|---|
| `""` (missing element / JS error path) | `""` | 0 |
| `"Pittsburgh"` / `"pittsburgh"` | contains | 1 |
| `"Pittsburgh, Pennsylvania"` / `"Fort Pitt — Pittsburgh"` | contains | 1 |
| `'"Pittsburgh"'` (outer quotes) | contains | 1 |
| `"&#80;ittsburgh"` (after html.unescape) | contains | 1 |
| `"  Pittsburgh\n"` | contains | 1 |
| `"Pittsburg"` (wrong spelling) | absent | 0 |
| `"WQED Studios"` (correct place name, no city) | absent | 0 |
| `"Mr. Rogers' Neighborhood studio"` | absent | 0 |
| `"NotPittsburgh"` (no word boundary) | contains | 1 |

Decisive consequence: the graded predicate is neither necessary nor sufficient for "the page of the place where Mr. Rogers was filmed". A correct place whose sidebar omits the city fails; arbitrary text containing the substring passes. This independently confirms the case's "substring only" row, its unchecked "whether the shown object is a specific place", and the candidate's task-424 boundary "sidebar text not place identity". The case does not exceed source here.

Second boundary: the selector `[id="sidebar_content"` has no closing `]`. In the world where the engine throws, L292–294 converts the error to `""` and every trajectory scores 0 (unsolvable, never falsely passing); in the world where the engine tolerates the unclosed block, the city-substring predicate above applies. In neither world is place identity checked, so the candidate's boundary holds unconditionally. The case correctly labels engine behavior unobserved and demands runtime evidence; I did not test a browser (forbidden), so this remains unresolved and is not scored as a defect.

Sharpening (not a contradiction): because `url` is `"last"` and no URL/string evaluator is routed, the final page's origin is never verified; "on the map" is enforced only by `start_url` before the episode and by the incidental presence of a `sidebar_content` element. The case covers this through rows 2/8 and the "final URL" unchecked item, but never states the origin consequence in one sentence.

## 5. Findings — citation/provenance defects in the case (no predicate-map change)

- **F1 (must-fix pointer; LOW severity, no semantic effect).** The section header and the source-openings table both give "Task record (raw L13317–L13346)", yet the section's first bullet cites `sites ["wikipedia","map"]`. The `sites` field is at L13313–L13316 and the record opens at L13312; L13317 is `"task_id": 424`. Correct range: L13312–L13347 (fields L13313–L13346). A reader checking the stated range cannot verify `sites`.
- **F2 (LOW).** Row 4 anchors "L290–294 `except Exception: selected_element = ""`". L290–291 is the separate `if not selected_element: selected_element = ""` coercion; the `except` is L292–294. The case itself cites L292–294 correctly later, and the behavioral claim (empty → 0) is right.
- **F3 (LOW).** "Template 371 (L13346): \"Find the page of {{description}} on the map.\"" — L13346 is `"intent_template_id": 371`; the template string is L13322. Only the pointer is ambiguous; the value and ID are correct.
- **F4 (provenance inconsistency; LOW).** The helper source-opening row declares the opened scope as "imports and PseudoPage only", but row 10 cites `llm_fuzzy_match` L146 and `llm_ua_match` L176. Both lines are correct at those numbers, so either the file was opened past PseudoPage (scope statement false) or the numbers were taken second-hand (not a first-hand opening). Either way the row's own evidence statement is inconsistent with its citation. Separately, `evaluators.py` L18–27 imports `helper_functions`, which itself imports `llms.providers.openai_utils` (helper L18–20): task 424 makes no judge call, but the scorer module has an import-level reach to the judge utility; "no judge dependency" should be read as "no judge call".
- **F5 (evidence-location gap; LOW).** The "rough bracket-count scan, kept in scratch" is not present in the cited scratch artifact (`.ufo/waves/round-28/scratch/Task424/census.txt`, 1209 B, holds only the task extraction, sibling lists, and three hashes). The number itself is correct and reproducible (114 distinct/209 occurrences), so this is a persistence claim, not a numeric error.

All remaining L-references in the case (18, 71, 80, 111, 146, 173, 176, 211, 252, 262, 263, 271, 279, 282, 289, 292, 293, 303, 312, 316, 319, 348, 356, 369, 13318, 13319, 13320, 13326, 13329, 13332, 13333, 13336, 13337, 13338) resolve to the claimed content at the exact stated lines.

## 6. Candidate-wise check

- Candidate row "759,424,97,399 | … sidebar text not place identity" is fully supported by the task-424 source and by the control table.
- Candidate sentence "Task356/759/424: the locators contain unclosed attribute-selector brackets in source" is true for the 424 leg (L13337); the candidate does not infer browser rejection.
- Candidate selection/metric provenance for 424 (registered lexicographic rule, persisted IDs, 16 audits, 651 targets) reproduces exactly.
- No case-specific candidate language exceeds source. The candidate's "not a validity verdict" framing matches the case's "Task validity: UNRESOLVED".

## 7. Not done / residual unknowns

No browser engine test of the unclosed selector; no live map DOM, no deployed `sidebar_content` element, no geocoder/feature data, no reference trajectory, no wrong-place runtime control, no scorer execution. The runner (`run.py`, `browser_env`) and `__MAP__` substitution are not in the snapshot, so evaluator-invocation state (whether the harness re-navigates before scoring) is outside the pinned bytes. These are exactly the runtime items the case lists; none is silently converted into a task-validity claim by this report.

VERDICT: PARTIAL — every intent→predicate/operator/unchecked claim in `build/Task424.md` and every population number, including task 424's selection, reproduces from the pinned bytes, and the candidate's 424 row is exactly supported; but the case contains four bounded source-line/provenance inaccuracies (F1 record range excludes `sites`; F2 over-wide `except` anchor; F3 template pointer; F4 declared helper opening scope contradicted by L146/L176 citations) plus one unpersisted heuristic (F5), so it is not yet source-exact as written. None of these changes the predicate map, the case's scoped PASS, or the unresolved task-validity status; F1 and F4 should be corrected before the case is cited as source-anchored.

# FTask399 — author-side falsification of BUILD case399 (WebArena task_id 399)

Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
Target under test: `.ufo/waves/round-28/build/Task399.md` (SHA256 `c5f23b04b0bde192309d125dfc5eabdf06e1d93dd22e51189de3d8ed9d957e8d`)
Raw case: `plans/fixtures/r28/webarena/config_files/test.raw.json`, task_id 399, true block lines **12461–12493** (build says 12464–12497)
Frozen candidate: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`
Candidate SHA256 (recomputed 2026-10-21): `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` — equals the frozen value.
Canonical candidate `corpus/knowledge/webarena-task-spec-audit.md` is **not admitted** (path absent; read as the named prospective target only, never edited).
Scope: case 399 only, static source bytes. No C2, no other case, no production edit.

## 0. Method and provenance

- Read-only over production. No installs/updates (tool log: none). No browser opened, no benchmark-site request, no upstream Python imported or executed, no REA MCP.
- Commands against the pinned snapshot only: `sha256sum`, `wc -l`, `grep -n`, `sed -n`, `find`, and standalone `python3 -B` JSON loads/line prints (bytecode disabled). The production instrument was **not** run by this seat; its receipts were read, and the counters below were recomputed from raw bytes by independent logic.
- LSP: the `lsp` device is **not mounted in this seat** (`xd://lsp` -> "No such tool"; mounted-device list contains no `lsp`). No `definition`/`references`/`hover`/`type_definition`/`implementation` trace was possible, so this unavailability is recorded rather than an empty cold result treated as absence. Literal `grep -n`/`sed -n`/`json.load` is the fallback; it is structural evidence, not semantic proof.
- Static disagreement is reported as such. Runtime-validity claims are left unresolved; no scorer/browser run was performed.

Pin (all recomputed values equal `manifest.json`):

| file | full SHA256 | bytes |
|---|---|---|
| `config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | 880776 |
| `evaluation_harness/evaluators.py` | `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22` | 13264 |
| `evaluation_harness/helper_functions.py` | `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275` | 7565 |
| `LICENSE` | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` | 11357 |

Upstream URL (manifest, `opened` 2026-10-21): `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json`. The build's truncated digests `7b50386f…37652`, `e23edb39…00c22`, `ec758da4…7e275` all match the full hashes above. License text is Apache-2.0.

## 1. Raw case-399 facts (observed, line-exact)

The build's raw block bounds are wrong; the corrected block is:

| field | value | line |
|---|---|---|
| task block open / close | `{` … `},` | **12461 / 12493** |
| sites | `["reddit"]` | 12462–12464 |
| task_id | `399` | 12465 |
| require_login | `true` | 12466 |
| storage_state | `./.auth/reddit_state.json` | 12467 |
| start_url | `__REDDIT__` | 12468 |
| geolocation | `null` | 12469 |
| intent_template | `Change my reddit bio to "{{content}}"` | 12470 |
| instantiation_dict | `{"content": "I am a robot"}` | 12471–12473 |
| intent (authored quote) | `Change my reddit bio to "I am a robot"` | **12474** |
| require_reset | `false` | 12475 |
| eval block | `{` … `},` | 12476–12491 |
| eval_types | `["program_html"]` | 12477–12479 |
| reference_answers | `null` | 12480 |
| reference_url | `""` | 12481 |
| program_html list | one target | 12482–12490 |
| target url | `__REDDIT__/user/MarvelsGrantMan136` | 12484 |
| target locator | `document.querySelector(".user-bio__biography").outerText` | 12485 |
| required_contents | `{"exact_match": "I am a robot"}` | 12486–12488 |
| intent_template_id | `6` | 12492 |

No `prep_actions`, no `func:` locator, no `func` URL, no `|OR|` list element, no `string_note`, no second `program_html` target. Task 400 opens at 12494.

## 2. Scorer path (observed, all anchors re-checked one by one)

`evaluators.py`:

- Router `356–374`; `program_html` at `369–370` appends only `HTMLContentEvaluator`. `eval_types` is read at 361; dispatch is `string_match` 365–366, `url_match` 367–368, `program_html` 369–370.
- `EvaluatorComb.__call__` `341–352`: `score = 1.0` (348), then multiply by each evaluator (349–351). With one evaluator and one target, the task score is exactly `{0.0, 1.0}`.
- `HTMLContentEvaluator.__call__` `248–333`: config `255–256`; `targets` 258; `score` 260; `for target in targets` 261; `target_url` 262; `func` URL branch 263–266 (not taken: the URL begins `__REDDIT__`, not `func`); locator 268; goto+sleep 271–273 (taken: `target_url != "last"`); full-page branch 276–277 (not taken); `document.` branch 279–294; `str(page.evaluate(...))` 289; falsy-to-empty 290–291; exception-to-empty 292–294; `html.unescape` 303; exact_match gate **305–310**; `must_include` `312–327` (unreachable because the gate is an `elif`); unknown-contents `ValueError` 329–332.
- `StringEvaluator.exact_match` `90–94` → `clean_answer` `80–86`: `strip()`, remove one surrounding pair of `'` or `"`, then `.lower()`; both reference and prediction go through it. `must_include` `98–111` lowercases and does substring containment; tokenization requires the caller flag AND a one-character cleaned reference (103–109).
- Import block `18–27`; `reddit_get_post_url` at `23`, defined helper `97–112`; `llm_fuzzy_match` `146–173`; `llm_ua_match` `176–208`. None is reached by task 399: no `func:` URL/locator, no `fuzzy_match`, no `ua_match`. **No LLM judge dependency.**
- `page.goto` (272) is outside the `try` at 288; a navigation failure raises out of the evaluator rather than taking the selector-exception path. The build does not claim otherwise, but its failure-mode row covers only the missing-element branch.

Every build claim in §Evaluator path is correct except the line anchors recorded in §5.

## 3. Intent → predicate completeness

| intent element | check | unchecked remainder |
|---|---|---|
| "Change my reddit bio …" | navigate to `__REDDIT__/user/MarvelsGrantMan136` (fixed URL) and read the first `.user-bio__biography` element's `outerText` | that the logged-in account is MarvelsGrantMan136; that the agent performed the change; causality/action; side effects on other fields/posts/other users; raw stored value vs rendering; any later matching element |
| "… to "I am a robot"" | `lower(strip_quotes(strip(unescape(outerText)))) == "i am a robot"` | case, one wrapping quote pair, surrounding whitespace and HTML entities are absorbed; interior whitespace/punctuation remain significant |
| "my" | nothing verifies ownership; the target URL hardcodes the account | the `storage_state` account identity is outside the pinned snapshot |

The build's §Checked/Unchecked rows reproduce this exactly. Its pre-satisfied-state and absent-selector risks are direct consequences of the code and are correctly left unresolved.

## 4. Independent numeric/census checks (derived from raw JSON, no production import)

| claim | source of claim | independent result |
|---|---|---|
| 812 raw tasks / 812 distinct IDs / IDs 0–811 | candidate, build | exact: `len=812`, IDs 0–811, no duplicates, no missing, no unexpected |
| evaluator-type sets 325/282/66/10/129 | candidate | exact: `string_match` 325, `program_html` 282, `url_match` 66, `string_match+url_match` 10, `program_html+url_match` 129 |
| 27 strata / 16 selected IDs | candidate, build | exact: 27 site/eval strata; sorted-minima selection reproduces `[389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399]` exactly, including 399 last |
| `(["reddit"],["program_html"])` has 37 tasks, min 399 | build | exact: 37 tasks; minimum task_id 399 |
| template 6 = tasks 399–403, same URL/locator/exact_match, different content, reset false | build | exact: five tasks; five distinct content strings; all `require_reset: false` |
| zero `require_reset: true` in 812 | build | exact: 0 true, 812 false, 0 absent |
| 651 page-content targets; 188 exact + 463 must_include; no overlap | candidate | exact: 651 targets, 188/463, zero targets with both, zero with neither |
| locator classes 105 full-page / 524 JavaScript / 22 helper | candidate | exact, sums to 651 |
| target URL classes 238 last / 338 navigation / 75 helper | candidate | exact, sums to 651 |
| string operator task counts 45 exact / 176 must_include / 118 fuzzy | candidate | exact |
| selftest 21 cases, exit 0 | candidate | receipt `build-acceptance/audit-selftest.stdout` says `SELFTEST clean cases=21 …`; not rerun by this seat |
| alternate oracle agrees on every metric and selected ID | candidate | `audit-alternate.stdout` matches every metric and the 16 IDs; its own header says `alternate implementation, not author-independent` — the candidate's disclosure is accurate |
| selected cases omit helper/prep/OR branches | candidate | exact for all 16 selected IDs: no `func` URL, no `func:` locator, no `prep_actions`, no `|OR|` element |

Raw task preservation: `audit-current.stdout` task 399 contains a complete `raw_task` that is value-equal under Python `==` to the fixture object (same 12 keys, same nested values; byte identity is not claimed because the audit output is a reserialization); `reference_approach_order` is `null` for 399 (no string approaches). No field is lost.

## 5. Defects found in the build report

**D1 (real, bibliographic, decisive). The task-record range is wrong and crosses the task boundary.**
Build: `test.raw.json lines 12464–12497`. Correct: **12461–12493**. Line 12464 is the closing `],` of task 399's `sites` array (the record starts three lines earlier); lines **12494–12497** are task 400's opening `{`, `"sites": [`, `"reddit"`, `],` (task 400's `task_id` is at 12498). The cited interval therefore both misses the first three lines of 399 and includes the first four lines of the next task. This is a boundary error, not a cosmetic offset.

**D2 (real, bibliographic, decisive). The intent anchor and eval range are wrong.**
Build: intent at `L12478`; eval at `L12480–12495`. Correct: intent at **12474**; eval block at **12476–12491**. `sed -n '12478p'` returns `        "program_html"` (an `eval_types` element), not the intent. Line 12480 is `"reference_answers": null`, so the eval range misses `"eval": {` and `eval_types`, and line 12495 is task 400's `"sites": [`. The build's own provenance sentence says anchors come from literal `grep -n`; `grep -n '"intent": "Change my reddit bio' plans/fixtures/r28/webarena/config_files/test.raw.json` returns 12474, so the stated method cannot produce the stated anchor from the pinned bytes. The quoted text is correct; its location is not.

**D3 (minor, bibliographic). The operator quote anchor is off by one.**
Build: `evaluators L304: if "exact_match" in target["required_contents"]:`. Line 304 is blank; the gate is at **305**, and the operator block is 305–310. The build's range `L304–310` still contains the block, so only the quote-location claim fails. Likewise `L259–261` for the target loop begins on a blank line (the `targets = …` assignment is 258; the `for` is 261) — imprecision, not a false block claim.

**D4 (minor, unsourced descriptor, non-load-bearing).** The build calls the deployed front-end "Reddit (Postmill)" and "Live Postmill DOM". The pinned bytes contain zero occurrences of `Postmill`/`postmill`; the platform identity comes from general WebArena background knowledge, not S061–S063. The build's limitations mark Postmill *rendering* as `[INFERENCE]`, but not the platform name. No 399 predicate depends on it.

**D5 (minor gap, not a false claim).** The failure-mode row covers the selector exception only. `page.goto` at 272 is outside the `try` at 288, so a navigation error is a distinct phase (uncaught) rather than `""`/score 0. The build never says otherwise, but its unchecked list does not enumerate this branch; the candidate's `scorer_contract.failure_phases` does distinguish `dynamic_helper_or_navigation_error`.

Not defects after checking: the pre-satisfied-state limitation is correct (the evaluator ignores `trajectory`, navigates to a fixed profile URL, and reads persisted state; `require_reset` is false and siblings 400–403 rewrite the same field); "no LLM judge dependency" is correct; the one-evaluator/one-target score set `{0,1}` is correct; `must_include` is unreachable because the `exact_match` gate is an `elif`; falsy `""` becomes `""` and missing element becomes `""`, both scoring 0.

## 6. Decisive boundary / controls

**B1 — task-boundary control (decisive, bibliographic).** The build's cited record interval fails the boundary test: `sed -n '12494,12497p'` yields task 400's opening `{`, `"sites": [`, `"reddit"`, `],`, and `12464` is already inside 399. A citation that claims to bound task 399 but contains task 400's identity lines is falsified independently of any semantic reading. True bounds: **12461–12493**.

**B2 — quote-location control (decisive, bibliographic).** `sed -n '12478p'` returns `"program_html"`; `sed -n '304p'` returns an empty line. The two "located quotes" attached to those lines cannot be reproduced at the stated locations; the texts are at 12474 and 305. The third quote (`evaluators L86: return answer.lower()`) is exact.

**C1 — pre-satisfied / no-op boundary (case-specific, unresolved).** `HTMLContentEvaluator` never reads the trajectory; it navigates to `__REDDIT__/user/MarvelsGrantMan136` and reads `.user-bio__biography.outerText`. With `require_reset: false`, a no-op trajectory scores 1 iff the initial bio already normalises to `i am a robot`; on a fresh state it should score 0. Siblings 400–403 write the same profile field with different content, so order/reset policy matters. The build states this and correctly refuses a validity verdict without runtime evidence. This control cannot be exercised here (no browser/site).

**C2 — selection control.** Independent recomputation of the 27 strata minima gives exactly the persisted 16 IDs; 399 is the minimum of the 37-task `(("reddit",), ("program_html",))` stratum and the 16th selected. The audited case is the intended representative, not a duplicate or an unselected task; template 6's other four tasks use different content strings.

**C3 — operator control.** The `exact_match` gate is reached first (305) and `must_include` is skipped (312 `elif`); one target multiplies once (310) under one evaluator (348–351). Both sides pass through `clean_answer` (80–86), so the effective predicate is exactly `lower(strip_quotes(strip(unescape(outerText)))) == "i am a robot"`. The build's normalisation description is source-exact.

## 7. Candidate case-specific language vs source

The candidate names 399 in exactly two places:

- Selection list (candidate line 60): `389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399` — supported by the raw census and `selected-task-ids.json`.
- Case-table row (candidate line 73): `759,424,97,399 … route inputs not duration, sidebar text not place identity, unit spelling, final profile text` — the 399 boundary "final profile text" is supported: the scorer navigates to the fixed profile URL and reads rendered `outerText` after load; it checks no action, duration, or route. It does not exceed source.

The candidate's own anchors are line-exact on the pinned bytes: `S061 task0:18–28` (task 0's eval block, observed at 18–28); `S062 StringEvaluator:71–170`, `URLEvaluator:173–241`, `HTMLContentEvaluator:244–333`, `combination/router:336–374`; `S063 fuzzy/UA:146–208`; N/A assignment at 159. Its metrics (812/5 sets/27/16/651/188+463/105+524+22/238+338+75/45+176+118) all reproduce; `audit-alternate.stdout` agrees on every metric and ID; `audit-selftest.stdout` records 21 cases.

The candidate's meta-claim that "Each task has an author-side, source-anchored intent→predicate audit" is only **partially** supported for 399: the predicate content is fully supported, but the referenced `build/Task399.md`'s explicit raw-line citations (D1/D2) are not. This also touches the C1 case-report contract: `plans/round-28-claims.md` line 19 requires every case report to record "task intent, exact evaluator targets/operators, what is checked, what remains unchecked, source location, and uncertainty." Task399.md records all six, but its `source location` cells are the wrong bytes for the raw record/intent/eval (and one evaluator quote), so that element is not satisfied for 399 even though the semantic map is. No case-399-specific candidate sentence turns an unobserved runtime condition into a confirmed success or failure; the candidate's own caveats about runtime state, judge branches and non-representative selection are preserved.

## 8. Unresolved (not claimed)

- The generated per-task config with `__REDDIT__` actually substituted, and the `browser_env/env_config.py` account mapping (outside the pinned snapshot), so `page.goto`'s real URL and the logged-in identity are unverified.
- Whether `.auth/reddit_state.json` authenticates as MarvelsGrantMan136.
- Deployed Postmill DOM: exactly one `.user-bio__biography`, its rendering/markdown/entity transform, and whether the selector is accepted.
- No-op control on a freshly reset image (initial bio must not normalise to `i am a robot`); positive control via the standard edit-biography UI; negative control with different text.
- Reset/order policy across template tasks 399–403 and any other task touching the same profile.
- Behaviour of the (unpinned) run loop when `page.goto` raises.
- Production instrument `benchmark_spec_audit.py` was **not** run by this seat; selftest-21 and alternate-oracle agreement remain receipt claims. The JSON-derivable counters above were recomputed independently from raw bytes.
- The candidate's instrument-property claim (JSON/Python-AST parsing only, no upstream import/execute, no benchmark-site network) was not re-audited here; only the case-399 output, the summary, the selftest receipt and the alternate receipt were read.

## Verdict

Semantic case audit for task 399: **PASS** — every target, operator, unchecked clause, and numeric claim reproduces from the pinned bytes; the candidate's 399 language ("final profile text") does not exceed source; no LLM judge is reachable.

Bibliographic evidence: the raw record range is shifted +3 at the start and +4 at the end (and includes task 400's opening), the intent anchor is +4, the eval range is wrong at both ends, and the operator quote anchor is off by one. The build's stated `grep -n` provenance cannot produce these anchors from the pinned bytes.

VERDICT: PARTIAL

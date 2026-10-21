# Task399 — case audit (round 28, C1, author-side)

Writer/seat: `KengakuR28.Task399-2` (scout, read-only leaf). Author-side advice, not outside closure.
Scope: one pinned WebArena task (task_id 399) — static intent→evaluator mapping only. No upstream execution, import, eval, browser action, or benchmark-site contact. Installs/updates: none.

## Inputs (hash-verified against `plans/fixtures/r28/webarena/manifest.json`, upstream `dce04686a56253aefba7b18a4fa0937cf1dc987b`)

| File (lane-relative under `plans/fixtures/r28/webarena/`) | sha256 (observed = manifest) | Upstream URL (manifest `opened` 2026-10-21) |
|---|---|---|
| `config_files/test.raw.json` (812 entries) | `7b50386f…37652` | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json |
| `evaluation_harness/evaluators.py` (374 lines) | `e23edb39…00c22` | …/dce04686…/evaluation_harness/evaluators.py |
| `evaluation_harness/helper_functions.py` (221 lines) | `ec758da4…7e275` | …/dce04686…/evaluation_harness/helper_functions.py |

I read the local pinned snapshot, not the live URLs. Access date 2026-10-21 refers to the manifest's opening.

Observed commands (read-only): `jq '.[]|select(.task_id==399)'`, `jq length` → 812, `sha256sum` on the three files, `grep -n` for line anchors, `jq` for the stratum minimum and sibling-template queries listed below.

## Task record (`test.raw.json` lines 12464–12497)

- sites `["reddit"]`; `require_login: true`; `storage_state: "./.auth/reddit_state.json"`; `start_url: "__REDDIT__"`; `require_reset: false`; `intent_template_id: 6`.
- intent (L12478): `Change my reddit bio to "I am a robot"` (template `Change my reddit bio to "{{content}}"`, content `I am a robot`).
- eval (L12480–12495): `eval_types ["program_html"]`, `reference_answers null`, `reference_url ""`, one program_html target:
  `url "__REDDIT__/user/MarvelsGrantMan136"`, `locator "document.querySelector(\".user-bio__biography\").outerText"`, `required_contents {"exact_match": "I am a robot"}`.
- Selection check: 399 is the minimum task_id of stratum (`["reddit"]`, `["program_html"]`) (37 tasks in that stratum, `jq` observed min 399). It matches the last entry in `selected-task-ids.json`.
- Sibling template: template 6 = tasks 399–403. All five use the same URL, locator, and `exact_match` operator, with different content strings, and all have `require_reset: false`. Across all 812 tasks, zero have `require_reset: true`.

## Evaluator path (exact anchors, `evaluators.py`)

| Step | Anchor | Behaviour for task 399 |
|---|---|---|
| Route | L356–374, `case "program_html"` L369–370 | Only `HTMLContentEvaluator()`. String and URL evaluators are not built, so `reference_answers: null` and `reference_url: ""` are never read. |
| Combine | `EvaluatorComb` L336–352 | Product of one evaluator, so the score is in {0.0, 1.0}. |
| Target loop | L259–261 | One target. |
| URL | L262–266 | Does not start with `func`, so the `eval` branch is not taken. `__REDDIT__` is a raw placeholder that the harness substitutes outside this snapshot. |
| Navigate | L271–273 | `page.goto(target_url)` then fixed `time.sleep(3)`. There is no wait-for-selector. |
| Locator | L279–294 | Starts with `document.`. No `prep_actions`. `str(page.evaluate("() => document.querySelector(\".user-bio__biography\").outerText"))`. If the element is missing, the call throws and is caught, giving `""` (L292–294). Falsy output also gives `""` (L290–291). |
| Unescape | L303 | `html.unescape(selected_element)`. |
| Operator | L304–310 | `StringEvaluator.exact_match(ref="I am a robot", pred=selected_element)`. The `must_include` branch (L312) is unreachable because of the `elif`. |
| Normalisation | `clean_answer` L80–86; `exact_match` L90–94 | Both sides are `strip()`ped, one surrounding pair of `'` or `"` is removed, then both are `lower()`ed, then compared with `==`. |

`helper_functions.py`: none of its functions run for 399. There is no `func:` URL or locator, and no `fuzzy_match`/`ua_match`, so `llm_fuzzy_match` (L146–173) and `llm_ua_match` (L176–208) are never reached. **No LLM judge dependency.** The `reddit_get_post_url` import (`evaluators.py` L23; defined at helper L97–112) is not used by this task.

Located quotes (≤25 words, from the pinned snapshot):
- raw L12478: `"intent": "Change my reddit bio to \"I am a robot\""`
- evaluators L304: `if "exact_match" in target["required_contents"]:`
- evaluators L86: `return answer.lower()`

## Compact case table (for L1)

| Field | Task 399 |
|---|---|
| Intent | Set the logged-in user's Reddit (Postmill) biography to `I am a robot`. |
| Evaluator types | `program_html` only, scored by `HTMLContentEvaluator`. |
| Target / operator | `__REDDIT__/user/MarvelsGrantMan136`; first `.user-bio__biography` element's `outerText`; `exact_match` against `I am a robot`. |
| Effective predicate | `lower(strip_quotes(strip(unescape(outerText)))) == "i am a robot"`. |
| Checked | Rendered bio text of the first matching element on MarvelsGrantMan136's profile page, as seen through the evaluating `page` session after load plus 3 s. Interior whitespace and punctuation are significant. |
| Unchecked | (a) That "my" account equals MarvelsGrantMan136. The identity in `reddit_state.json` is not in the snapshot. (b) How the change was made (settings form or another route) and the trajectory itself. (c) Side effects: other profile fields, posts, other users. (d) Raw stored value versus rendered value. Case, surrounding whitespace, one wrapping quote pair, and any markup removed by rendering are all invisible to the check. (e) Any `.user-bio__biography` element after the first. |
| Normalisation leniency | Case-insensitive. `"I AM A ROBOT"`, ` i am a robot `, and `"i am a robot"` (quoted) all score 1. |
| Dynamic-state dependencies | Live Postmill DOM and CSS class name; persisted DB state of the bio; placeholder substitution of `__REDDIT__`; the session from `storage_state`; page load timing (fixed 3 s sleep). `require_reset: false`, and sibling tasks 400–403 write the same field. |
| Judge dependencies | None (no LLM, no helper API calls). |
| Failure mode on missing element | Silent `""`, so score 0. A broken selector cannot be told apart from an agent failure in the score alone. |
| Static schema compatibility | Compatible. The routed type is known, the required keys are present, and the `exact_match` key is handled. |

## Task-specific potential validity limitation (not a proven defect)

**Pre-satisfied state / order dependence.** The check reads persisted profile state, not the agent's action, and `require_reset` is false. If MarvelsGrantMan136's bio already normalises to `i am a robot` when evaluation starts, a no-op agent scores 1. That can happen if an earlier run of 399 was not reset, or if the image is seeded that way. The reverse risk: if the selector is absent in the deployed Postmill version, every agent scores 0 silently. A secondary limitation: the "my" bio (intent) and the hardcoded account (target) are tied only by an unobserved assumption about `storage_state`. The case-insensitive, render-level comparison is lenient but consistent with the intent; I do not count it as a defect.

## Runtime evidence required before calling 399 valid or invalid (none collected here; not permitted)

1. The generated per-task config (the substituted `__REDDIT__` and its account mapping) and the `browser_env/env_config.py` `ACCOUNTS["reddit"]` value, both outside this snapshot.
2. Confirmation that `.auth/reddit_state.json` authenticates as MarvelsGrantMan136.
3. A no-op control on a freshly reset image: the initial bio does not normalise to `i am a robot`, so the score is 0.
4. A positive control: setting the bio through the standard edit-biography UI scores 1. A negative control: different text scores 0.
5. DOM evidence: `/user/MarvelsGrantMan136` renders exactly one `.user-bio__biography` once a bio is set, and the rendering transform (markdown/escaping) is known.
6. Harness reset or ordering policy across template tasks 399–403 and any other tasks that touch the same account profile.

## Limitations of this report

- Only static source reading of three pinned files. `browser_env`, `llms`, the config-generation step, and the Postmill code were not available or not opened.
- Statements about Postmill rendering (markdown, CSS text-transform effects on `outerText`) are **[INFERENCE]** and do not change the predicate, because lowercasing absorbs case changes.
- No LSP server applies to JSON/Python data opened this way. Anchors come from literal `grep -n`/`jq` and direct reads, which is structural evidence, not semantic proof.
- Q13 structural evidence is not endorsement. No source row or knowledge admission is proposed.

## Verdict

**PASS (scoped):** the static intent→evaluator mapping for task 399 is complete, deterministic, and schema-compatible, with no judge dependency.
**Task validity: UNDETERMINED.** It needs runtime items 1–6 above. This is not a blanket round PASS and not a benchmark-defect finding.

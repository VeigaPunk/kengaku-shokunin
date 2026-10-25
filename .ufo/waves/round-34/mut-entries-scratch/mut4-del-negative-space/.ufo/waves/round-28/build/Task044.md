# Task044: WebArena task_id 44 case audit (C1, static, author-side)

Writer/seat: KengakuR28.Task044-2 (scout, read-only). Round 28 claim C1 only (novelty, legacy, mapped to canonical coverage/constructs). This is author-side advice, not outside non-author closure. I did not execute or import upstream code, contact any site, run a browser, delegate, or install tools.

## Inputs (pinned snapshot, sha256 matches `plans/fixtures/r28/webarena/manifest.json`)

| File | sha256 | Upstream URL @ dce04686a56253aefba7b18a4fa0937cf1dc987b (manifest `opened` 2026-10-21) |
|---|---|---|
| `config_files/test.raw.json` | 7b50386f…37652 | `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686…/config_files/test.raw.json` |
| `evaluation_harness/evaluators.py` | e23edb39…00c22 | `…/evaluation_harness/evaluators.py` |
| `evaluation_harness/helper_functions.py` | ec758da4…5e275 | `…/evaluation_harness/helper_functions.py` |

I read the local pinned copies on 2026-10-21. I checked their identity by sha256 against the manifest; I did not re-fetch the URLs. Sample membership: task 44 is the minimum task_id in stratum `(["gitlab"], ["url_match"])`. That stratum holds 16 tasks in the raw file: 44, 45, 46, 102–106, 156, 258, and others. Task 44 is the fifth entry in `selected-task-ids.json`.

## Task spec (`config_files/test.raw.json` lines 1408–1431)

Located quotes (25 words or fewer):

- L1419: `"intent": "Check out my todos",`
- L1422–1424: `"eval_types": [ "url_match" ],`
- L1426: `"reference_url": "__GITLAB__/dashboard/todos",`
- L1428: `"url_note": "GOLD in PRED"`

Other fields:

- `sites=["gitlab"]`, `require_login=true`, `storage_state="./.auth/gitlab_state.json"`, `start_url="__GITLAB__"`, `require_reset=false`.
- `reference_answers=null`, `program_html=[]`, `instantiation_dict={}`, `intent_template_id=303`.
- Template 303 has only this one task. Task 44 is the only task in all 812 whose `reference_url` contains `dashboard/todos`.

## Intent → evaluator mapping (case table)

| # | Intent element | Eval type → class (source) | Operator | Target | Checked? |
|---|---|---|---|---|---|
| 1 | "my todos" (destination page) | `url_match` → `URLEvaluator()` (`evaluators.py:367-368`) | `GOLD in PRED` (L215-216). `pred = clean_url(page.url)` strips trailing `/` (L187-190, L212). Base = `netloc + path` (L195). `base_score = any(ref_base_path in pred_base_paths)` (L220-227) | `__GITLAB__/dashboard/todos`, split on ` \|OR\| ` (one alternative) (L213-214) | Yes: the final `page.url` host+path must contain `<gitlab-netloc>/dashboard/todos` as a substring |
| 2 | (no query constraint) | same | `query_score` loop over `ref_queries` (L228-235) | Reference has no query, so the loop is empty and `query_score = 1.0` | Effectively unchecked: the prediction's query string is ignored |
| 3 | "Check out" (view or review) | none | none | none | Unchecked: no answer, content, or trajectory check |
| 4 | Combination | `EvaluatorComb` product (L348-352) | single factor | none | Score is binary, {0.0, 1.0} |

Observed operator semantics, from the source plus a stdlib-only `urllib.parse` probe (no upstream import). `parse_url` returns one `str` (L192-197), so at L223 `ref_base_path in pred_base_paths` is a Python substring test, not list membership or equality. For a reference netloc `h:8023`, the probe gave:

- **Pass (1.0):** `/dashboard/todos`, `/dashboard/todos?state=done&type=MergeRequest`, `/dashboard/todos#x`, `/dashboard/todosXYZ`, and the `https` variant (scheme is not compared).
- **Fail (0.0):** `/users/sign_in`, `/dashboard/todo`, `/x/dashboard/todos/1`.

## Checked vs unchecked

**Checked:**

- The final page URL's netloc+path contains the substituted reference host+path.
- That check ignores scheme, fragment, query, and a trailing slash.

**Unchecked:**

- Rendered content. Nothing verifies that the todo list loaded or was non-empty, or that the HTTP status was 200.
- Which todo filter was shown. Pending and done are not distinguished because `?state=` is ignored.
- Which user's todos were shown. Identity rests only on `storage_state`.
- The agent's final answer and the trajectory. `URLEvaluator.__call__` never reads `trajectory` (L177-241).
- Absence of side effects. For example, marking todos done would not be detected, and `require_reset=false`.
- Path over-extension. Any suffix after `todos` passes.

## Dynamic state and judge dependencies

- **No LLM judge.** `llm_fuzzy_match` and `llm_ua_match` are imported (`evaluators.py:21-22`) but unreachable for this task: only `URLEvaluator` is routed.
- **No helper function is used.** `PseudoPage` (`helper_functions.py:211-221`) can override `.url` if the runner passes one. The runner is not in the pinned snapshot.
- **Runtime state the score depends on:**
  - The live GitLab instance at the `__GITLAB__` base.
  - A valid `.auth/gitlab_state.json` session. If it is expired, GitLab presumably redirects to `/users/sign_in`, which scores 0 [INFERENCE].
  - Which page or tab the runner hands over as `page` at episode end.
- **Unpinned code paths.** Neither the `__GITLAB__` placeholder substitution nor the page selection appears in the pinned files: `grep` finds no `__GITLAB__` in `evaluation_harness/*.py`. `helper_functions.py:9-11` imports `GITLAB` from the unpinned `browser_env.env_config`. Both are unresolved gaps.

## Potential validity limitation (task-specific; not a proven defect)

"Check out my todos" is a navigation-only intent, scored solely by substring containment on host+path with the query ignored. Two consequences:

1. **Over-acceptance.** Any filtered todo view, such as done items or a type filter, earns full credit, and so does any path extending `/dashboard/todos`. Side effects are never inspected.
2. **Under-acceptance.** An agent that reached the todo list in a tab other than the one handed to the evaluator, or saw the list through a different GitLab route, would score 0. Whether this happens depends on the unpinned runner [INFERENCE].

Neither consequence has been shown to change any recorded outcome.

## Runtime evidence required before calling task 44 valid or invalid

1. The substituted `reference_url`, the pinned runner, and its page-selection logic: which tab, and whether `PseudoPage` is used.
2. The GitLab version's actual todos route, plus redirect behavior under valid and expired `storage_state`.
3. Scored trajectories showing the final `page.url` together with what was rendered, including at least one filtered or over-extended URL and one alternate-tab case.
4. A check of whether any state mutation occurred during passing runs.

None of this was gathered: site contact and execution are forbidden in this round.

## Verdict

**PASS** for the scoped static audit. The intent → `url_match` operator and target mapping, the checked/unchecked properties, the dynamic dependencies, and the source anchors are fully traced from the pinned sources.

The task's runtime validity is **undetermined**: it is neither valid nor invalid, pending the runtime evidence listed above. This verdict covers case 44 only and is not a round-level PASS.

Observed commands: one `python3` stdlib JSON read of the raw file (task 44, template-303 siblings, `dashboard/todos` matches, gitlab strata counts); `sha256sum` of the three inputs; `sed -n 1408,1432p`; `grep` for `__GITLAB__`, `storage_state`, `require_login`, and `GITLAB` in the harness; and the stdlib `urllib.parse` probe above. No installs or updates.

## Clarification (2026-10-21, appended on KengakuR28 request; original bytes above unchanged)

Correction to the wording in the case table, row 1, and in "Observed operator semantics". `parse_url` (`evaluators.py:192-197`) returns a tuple `(base_path, query)`, not "one `str`". At L218, `pred_base_paths, pred_query = parse_url(pred)` unpacks that tuple, so `pred_base_paths` is bound to the `str` `base_path`. Because of that binding, `ref_base_path in pred_base_paths` (L223) is a substring test. The operator semantics, the probe results, and the scoped verdict are unchanged. No new checks were run and no sources were fetched for this clarification.

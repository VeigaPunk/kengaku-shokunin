# Round 28 C1 case report — WebArena task 590

Writer/seat: `KengakuR28.Task590-2` (scout, read-only, author-side). Axis: novelty → canonical coverage/constructs. Not outside closure.
Scope: one pinned static task specification plus the scorer code it routes to. No upstream code was executed or imported, no benchmark site was contacted, and no browser action was taken.

## Inputs and integrity (observed)

Local snapshot `plans/fixtures/r28/webarena/`. Upstream revision `dce04686a56253aefba7b18a4fa0937cf1dc987b` (`manifest.json`). Upstream URLs come from the manifest. The local copies were opened on 2026-10-21; no network fetch was made.

| File | sha256 (observed by `sha256sum`) | Matches manifest |
|---|---|---|
| `config_files/test.raw.json` | `7b50386f…02537652` | yes |
| `evaluation_harness/evaluators.py` | `e23edb39…b77e00c22` | yes |
| `evaluation_harness/helper_functions.py` | `ec758da4…26997e275` | yes |

Commands run (read-only):

- `sha256sum` over the three files. Full digests: `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`, `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22`, `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275`. All three equal the manifest values.
- `python3 -c json.load(...)`: this parses the JSON as data only. It does not import any upstream module. It was used to extract task 590, its template-339 siblings, and the stratum count.
- `grep -n` for line anchors.

Source openings (located quotes, ≤25 words, access date 2026-10-21):

- S061 candidate, raw tasks: <https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json> line 19587: `"intent": "Create a milestone for the upcoming event of product launch starting on 1/16/2023 and ending on 1/30/2023"`. Scope: task 590 intent only.
- S062 candidate, scorer: <https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py> lines 222–223: `ref_base_path in pred_base_paths`. Scope: the URL GOLD-in-PRED operator.
- S063 candidate, helpers: <https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/helper_functions.py> lines 211–213: `class PseudoPage: def __init__(self, original_page: Page, url: str): self.url = url`. Scope: page type only; task 590 invokes no helper function.

## Task spec (observed, `test.raw.json` lines 19576–19627)

- Site `gitlab`. `require_login: true`, with `storage_state ./.auth/gitlab_state.json`. `require_reset: false`.
- `start_url __GITLAB__/primer/design`.
- Template 339: `"Create a milestone for the upcoming {{event}} starting on {{start_date}} and ending on {{end_date}}"`. The template is filled with event=`event of product launch`, start=`1/16/2023`, end=`1/30/2023`.
- `eval_types ["url_match","program_html"]` (19590–19592). `reference_answers null`, so no string match is run and no LLM judge is used.
- `reference_url "__GITLAB__/primer/design/-/milestones"` (19595), with `url_note "GOLD in PRED"` (19625).
- There are three `program_html` targets, all with `url: "last"` (19598, 19607, 19616):
  1. Locator `document.querySelector("#content-body").outerText`; `must_include ["product launch"]` (19599, 19602).
  2. Locator `document.querySelector('.block.start_date').outerText`; `must_include ["Jan 16, 2030"]` (19608, 19611).
  3. Locator `document.querySelector('.block.due_date').outerText`; `must_include ["Jan 30, 2030"]` (19617, 19620).
- Stratum: (`["gitlab"]`, `["program_html","url_match"]`) has 23 tasks, and 590 is the minimum ID in it. This agrees with the frozen selection rule.

## Intent → evaluator mapping (case table for L1)

| # | Intent element | Evaluator / operator (anchor) | Target | Checked | Unchecked / weak proxy |
|---|---|---|---|---|---|
| R | Combination | `evaluator_router` builds `[URLEvaluator, HTMLContentEvaluator]` (evaluators.py 361–372). `EvaluatorComb` multiplies the scores (348–352). | — | Both parts must score 1.0. The result is binary. | The final answer string and the trajectory steps are never inspected. |
| U | "milestone" in project primer/design | `URLEvaluator`, GOLD in PRED (173–241). `clean_url` only strips a trailing `/` (187–190). `parse_url` builds netloc+path and the query (192–197). `base_score = any(ref_base_path in pred_base_paths)` (220–227). There is no reference query, so `query_score` stays 1.0 (228–235). | `__GITLAB__/primer/design/-/milestones` (the substituted host) | The final `page.url` netloc+path contains the reference string. | `pred_base_paths` is a single `str` from `parse_url`, so `in` is a **substring** test, not list membership. Any final URL under `…/primer/design/-/milestones…` passes, including the list page, `/new`, and any existing milestone. The check does not show that a milestone was created. |
| H1 | event = "event of product launch" (milestone title) | `HTMLContentEvaluator` (244–333): `url "last"` means no navigation (271). The `document.` locator is run through `page.evaluate` (279–289); exceptions or empty output become `""` (290–294). `html.unescape` is applied (303). `must_include` splits on ` \|OR\| ` (none here) and calls `StringEvaluator.must_include(tokenize=False)` (312–327). `clean_answer` strips and lowercases (80–86), and the test is a substring test (111). | `"product launch"` anywhere in `#content-body` | The lowercased phrase appears somewhere in the main content of the final page. | The title value is not compared, so "product launch" could come from the description or other page text. The milestone's persistence, project ownership, state, and uniqueness are not checked. |
| H2 | start date "1/16/2023" | Same operator as H1 | `"Jan 16, 2030"` in `.block.start_date` | The sidebar start-date block contains `jan 16, 2030` after lowercasing. | **The required year 2030 differs from the intent's 2023.** If the selector is missing, the exception is caught and the score is 0. |
| H3 | end date "1/30/2023" | Same operator as H1 | `"Jan 30, 2030"` in `.block.due_date` | The due-date block contains `jan 30, 2030`. | Same year mismatch as H2. |
| X | Helpers | `helper_functions.py`: there is no `func:` URL or locator and no fuzzy match, so `llm_fuzzy_match`, `llm_ua_match` and `gitlab_get_project_memeber_role` are not invoked for this task. Only `PseudoPage` (211–221) is a permitted page type (evaluators.py 41). | — | — | Import-time dependencies still exist: `browser_env.env_config.GITLAB` and the `llms.providers.openai_utils` import (helper 9–20). Importing `evaluators.py` requires them, but they do not affect scoring for this task. |

## Dynamic state and judge dependencies

- **Judge:** none. The task is fully deterministic given the browser state, and no LLM is called.
- **Live state:** the scorer reads the final `page.url` and the live GitLab DOM. That DOM depends on the GitLab version (`.block.start_date`/`.block.due_date` sidebar classes), the locale and date format (`Mon D, YYYY`), the timezone, and the logged-in session (`storage_state`).
- **Placeholder substitution:** `__GITLAB__` is unsubstituted in the raw file. With the raw string, `urlparse` would give an empty netloc. The per-task config that is actually scored depends on a generation step that is not in the pinned snapshot. [INFERENCE: that step substitutes the GitLab base URL.]
- **Pre-existing and cross-task state:** `require_reset: false`. Siblings 591 and 592 target the same project with 2030 start dates. Whether `primer/design` already has a matching "product launch" milestone, or one left by an earlier run, is unknown. Because U is satisfied by any `-/milestones…` URL, navigating to an existing matching milestone would score like creating one.

## Task-specific potential validity limitation (not a proven defect)

The intent asks for 1/16/2023–1/30/2023, but H2 and H3 require "Jan 16, 2030" and "Jan 30, 2030".

From the static scorer logic, a trajectory that follows the literal intent and shows 2023 dates fails H2 and H3, because a lowercased substring `jan 16, 2030` would not appear. Passing requires dates that the intent never states.

The same shift appears in template-339 siblings 591 and 592 (intent 2023, scorer 2030, same project). Siblings 593 and 594 are internally consistent (2044 in both intent and scorer). Only 658 and 809 state 2030 in their intents. This points to a template-local instantiation drift rather than a scorer-wide convention. [INFERENCE]

## Runtime evidence required before calling 590 valid or invalid

None of this was performed here. It would require the official reset environment, run by an authorized party.

1. Confirm the per-task config that was actually scored, after substitution, has the same intent and targets as the raw file at the pinned revision. Also check whether any later upstream revision changed 590. That check was not made, because it would require a network opening.
2. Run a reference trajectory on a fresh reset that enters 1/16/2023 and 1/30/2023 literally. Record the final URL, the three `outerText` values, and the per-evaluator scores. Repeat with 2030 dates.
3. Confirm that the GitLab version's milestone page exposes `.block.start_date` and `.block.due_date` with the `Mon D, YYYY` format, and that dates are not shifted by timezone or environment clock.
4. Record the milestones on `primer/design` before the run, and run negative controls with final pages on the list page, `/new`, and a pre-existing milestone.

A run where literal 2023 entry scores 0 while 2030 entry scores 1 would demonstrate the mismatch at runtime. Without that run, this is a static observation only.

## Limitations

- This is evidence from the static spec and scorer only, not browser-level truth. The GitLab DOM behaviour is [INFERENCE].
- No upstream history, issue tracker, or WebArena-Verified release was consulted.
- One task from a deliberately non-representative frozen sample. No benchmark-wide claim.
- No tools were installed or updated.

## Verdict

**PARTIAL** (scoped to case 590).

The intent→operator mapping, the checked and unchecked properties, the dependencies, and the anchors are complete and grounded in the pinned, hash-verified sources. The task-validity question is left open pending the runtime evidence listed above. There is a concrete static intent/scorer year inconsistency (2023 vs 2030) and a substring-only URL proxy.

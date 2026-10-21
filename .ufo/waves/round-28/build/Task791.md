# Task791 — C1 case audit, WebArena task_id 791

Writer/seat: KengakuR28.Task791-2 (read-only scout, author-side advice; not outside closure).
Scope: one static case from the frozen selection (stratum `(gitlab,reddit) × (string_match)`). It is not a benchmark-wide verdict and does not establish that the task is valid or invalid.

## Inputs (pinned, local only)

These are the local snapshot files at upstream `dce04686a56253aefba7b18a4fa0937cf1dc987b`, all accessed 2026-10-21. I checked each sha256 against `plans/fixtures/r28/webarena/manifest.json` and all three matched. I did not open any upstream URL or benchmark site; the manifest records the upstream URLs.

| File | sha256 | Upstream URL (from manifest) |
|---|---|---|
| `config_files/test.raw.json` | `7b50386f…37652` | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json |
| `evaluation_harness/evaluators.py` | `e23edb39…00c22` | …/evaluation_harness/evaluators.py |
| `evaluation_harness/helper_functions.py` | `ec758da4…e275` | …/evaluation_harness/helper_functions.py |

Commands I ran, all read-only:
- `sha256sum` on the three files.
- `jq` selections over `test.raw.json`: task 791, template 84 siblings, the N/A population, and `__REDDIT__/f/<forum>` strings.
- `sed`/`nl` to get line anchors.

I did not import or execute any upstream code, and I installed nothing.

## Task spec (test.raw.json)

| Field | Value | Line |
|---|---|---|
| task_id / sites | 791 / `["gitlab","reddit"]` | 28786 / 28782 |
| login / storage / start | `require_login: true`, `./.auth/gitlab.reddit_state.json`, `__GITLAB__` | 28787–28789 |
| intent | "Make a folder named car on the gimmiethat.space repo and include a file called urls.txt that consists of the links to the 5 most recent posts from cars." | 28797 |
| instantiation | directory=`car`, subreddit=`cars`, gitlab_repo=`gimmiethat.space`; template_id 84 | 28794, 28811 |
| require_reset | `false` | 28798 |
| eval_types | `["string_match"]` | 28800–28801 |
| reference_answers | `{"fuzzy_match": "N/A"}` | 28804 |
| reference_url / program_html | `""` / `[]` | 28806–28807 |
| string_note | "the subreddit does not exist" | 28808 |
| raw annotation | `"N/A"` | 28809 |

## Evaluator mapping: intent to operator and target

How the scorer is chosen: `evaluator_router` (evaluators.py:355–374) maps `string_match` to `StringEvaluator` (line 365–366). `EvaluatorComb` multiplies the scores (346–352); here there is only one evaluator.

| Step | Operator (anchor) | Target | Effect for 791 |
|---|---|---|---|
| 1 | `pred = clean_answer(last_action["answer"])` (evaluators.py:133–134). `clean_answer` strips whitespace, strips one pair of outer quotes, and lowercases (80–86). | The agent's final stop-answer string only. | Only the text answer is read. Page, URL and repo state are not used. |
| 2 | `case "fuzzy_match"` with `value == "N/A"`, then `exact_match(ref="N/A", pred)` (150–155, 90–94). | `"n/a"` after cleaning. | A bare `N/A` (or `"n/a"`, `'N/A'`) scores 1.0 immediately. No reason is required. |
| 3 | If step 2 did not score 1, then `score = 1.0 * ua_match(intent, ref=string_note, pred)` (158–163). Note this is assignment (`=`), not multiplication. | `string_note` = "the subreddit does not exist". | The score is decided by an LLM judge. |
| 4 | `llm_ua_match` (helper_functions.py:176–208) calls `generate_from_openai_chat_completion(model="gpt-4-1106-preview", temperature=0)` (196–203). | The prompt asserts the task "is inherently unachievable" and compares the actual reason with the reported reason (184–190). | If the response contains `"different"` the score is 0.0. Otherwise `assert "same" in response` and the score is 1.0 (204–208). |

### Intent properties: checked vs unchecked

| Property implied by the intent or its unachievable framing | Checked? | Basis |
|---|---|---|
| Agent declares the task not achievable (`N/A`) | Yes. Exact match after normalisation. | evaluators.py:152–155 |
| Stated reason matches "subreddit does not exist" | Partly. Only reached when the answer is not a bare `N/A`; then the LLM judge decides. | 156–163; helper:176–208 |
| Forum `cars` really is absent on the Reddit (Postmill) instance | No. This is annotator ground truth in `string_note`; the scorer makes no site query. | test.raw.json:28808 |
| Agent did not create `car/urls.txt` or any other side effect in `gimmiethat.space` | No. There is no `program_html` or URL check, and `require_reset: false`. | 28798, 28806–28807 |
| Agent did not substitute a nearby forum and silently do the task | No, unless that shows up in the answer text the judge sees. | No state evaluator |
| Agent actually visited Reddit or GitLab | No. The trajectory is used only for its last action. | evaluators.py:133 |
| Folder name, file name, the "5 most recent" ordering, link format | Not applicable. These are only checked in the achievable siblings 552–555 (`program_html` `must_include` on `__GITLAB__/byteblaze/gimmiethat.space/-/raw/main/<dir>/urls.txt`). | sibling JSON; evaluators.py:312–327 |

## Dynamic state and judge dependencies

- **Reddit instance state.** Whether forum `cars` exists decides whether `N/A` is the correct answer. The frozen JSON cannot show the forum list.
  - Weak static hint [INFERENCE]: the 46 distinct `__REDDIT__/f/<name>` forum names that appear anywhere in the 812 tasks do not include `cars`. No other task references `cars` as a forum; the only other "car" hit is task text at line 20279 ("is car necessary", an nyc post).
  - This list comes from reference strings in tasks, not from the site's inventory, so it proves nothing about absence.
- **GitLab state.** The scorer never reads it. Any mutation persists because `require_reset: false`.
- **LLM judge.** Only reached for non-bare answers.
  - It uses the external OpenAI API with model `gpt-4-1106-preview` through `llms.providers.openai_utils` (helper_functions.py:18–20, 196–203).
  - The result depends on the model and endpoint still being available [INFERENCE: model retirement/drift is not checked here].
  - The verdict comes from substring parsing. A response containing "different" anywhere scores 0. A response with neither "same" nor "different" raises an `AssertionError`, which is an evaluator error, not a score.
- **Trajectory contract.** `trajectory[-1]` must be a stop action with an `"answer"` key (47–56, 133).

## Task-specific potential validity limitation (not a proven defect)

The task's correctness rests entirely on one unverified annotator claim: that forum `cars` does not exist (line 28808). The scorer accepts a bare `N/A` with no reason (152–155), even though the code's own comment at 156–157 says asking for a reason "should be the default as it will prevent false positive N/A". Repo side effects are never checked.

So, potentially:
- An agent that answers `N/A` without visiting Reddit gets full credit. This is a blind-abstention false positive; how likely it is depends on the agent's policy.
- If `cars` (or a case variant) does exist in the deployed snapshot, an agent that correctly completes the task and reports success scores 0.

Both outcomes depend on runtime state. Neither is shown by static evidence.

## Runtime evidence needed before calling 791 valid or invalid

1. An authoritative forum inventory for the pinned Postmill/Reddit image, showing presence or absence of `cars`, including case variants and aliases such as `Cars`.
2. That image's identity/digest, tied to the benchmark release used for scoring.
3. For reason-bearing answers: recorded judge transcripts (prompt, model ID, raw response) showing how "same"/"different" was parsed, plus a stability check at temperature 0.
4. Optionally, to judge side-effect leniency: GitLab `gimmiethat.space` state before and after a scored run.

None of this was collected; this seat is forbidden from site contact or execution.

## Compact case row for L1

| task | sites | eval_types | operator → target | checked | unchecked | dynamic deps | limitation | verdict |
|---|---|---|---|---|---|---|---|---|
| 791 | gitlab+reddit | string_match | `fuzzy_match:"N/A"` → `exact_match("n/a")` (ev:150–155); otherwise `llm_ua_match` vs string_note "the subreddit does not exist" (ev:158–163, hf:176–208) | Final-answer N/A, or judged reason | Forum absence, repo side effects, navigation, alternate-forum substitution | Reddit forum inventory; gpt-4-1106-preview judge with substring parse/assert; `require_reset:false` | Bare N/A accepted without a reason; ground truth is an unverified annotator note | PARTIAL (static only) |

Context counts (from `jq` over the frozen JSON):
- 36 of 812 tasks use `fuzzy_match: "N/A"`. All 36 are `string_match`-only.
- 791 is the only one of them on `gitlab+reddit`, and the only task in its `(gitlab,reddit) × (string_match)` stratum.
- It is the only unachievable instance of template 84; siblings 552–555 are achievable and use `program_html`.

## Final scoped verdict

**PASS** for the static mapping: intent, operator, target, anchors, and checked/unchecked properties are fully traced from pinned, hash-verified sources.

**PARTIAL** for task validity: it is undetermined without the runtime evidence above.

I make no claim of benchmark invalidity, I added no new source rows, and I admitted no knowledge.

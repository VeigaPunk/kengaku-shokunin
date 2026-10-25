# FTask791 — falsification of BUILD case 791

Seat: `KengakuR28.FTask791` (leaf, no delegation). Author-side report; no production edits.

- Target: `.ufo/waves/round-28/build/Task791.md` (writer `KengakuR28.Task791-2`).
- Frozen candidate: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, SHA256
  `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` (recomputed; matches the
  assignment).
- Canonical candidate: `corpus/knowledge/webarena-task-spec-audit.md` — **not admitted**; the path
  does not exist in this tree, so this report judges only the frozen draft bytes and the build case,
  not a canonical page.
- Pinned upstream: `plans/fixtures/r28/webarena/`, upstream revision
  `dce04686a56253aefba7b18a4fa0937cf1dc987b`.

No upstream import/execution, no benchmark-site request, no browser action, no production instrument
run. Scratch checks are independent stdlib censuses plus a small reimplementation of the pinned
string predicates (`python3 -B`, no upstream import).

## Inputs re-opened

| file | sha256 | manifest |
|---|---|---|
| `config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | match |
| `evaluation_harness/evaluators.py` | `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22` | match |
| `evaluation_harness/helper_functions.py` | `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275` | match |

All three hashes match `plans/fixtures/r28/webarena/manifest.json`; the Task791 report's truncated
hash prefixes are consistent with those full values.

## Source-verified claims (PASS)

### Raw task 791 (`config_files/test.raw.json`, lines 28782–28811)

| claim | observed | anchor |
|---|---|---|
| sites `["gitlab","reddit"]` | same | 28782–28785 |
| `task_id` 791 | same | 28786 |
| `require_login` true, storage `./.auth/gitlab.reddit_state.json`, start `__GITLAB__` | same | 28787–28789 |
| intent text | exactly `Make a folder named car on the gimmiethat.space repo and include a file called urls.txt that consists of the links to the 5 most recent posts from cars.` | 28797 |
| instantiation `car` / `cars` / `gimmiethat.space` | same (directory 28793, subreddit 28794, repo 28795) | 28792–28796 |
| `require_reset` false | same | 28798 |
| `eval_types ["string_match"]` | same | 28800–28801 |
| `reference_answers {"fuzzy_match":"N/A"}` | same | 28803–28805 |
| `reference_url ""`, `program_html []` | same | 28806–28807 |
| `string_note "the subreddit does not exist"` | same | 28808 |
| `reference_answer_raw_annotation "N/A"` | same | 28809 |
| `intent_template_id` 84 | same | 28811 |

The report's only weak anchor here is the table row "instantiation … 28794, 28811": 28794 shows
only `subreddit`; `directory` and `gitlab_repo` are at 28793 and 28795. This is an incomplete anchor,
not a false value.

### Evaluator path (all anchors verified)

- `evaluator_router` at `evaluators.py:355–374`; `string_match` → `StringEvaluator` at 365–366;
  `EvaluatorComb` at 336–352 multiplies at 348–352 (`score *= cur_score`); one evaluator only.
- `StringEvaluator.__call__` line 133 calls `get_last_action`; line 134 sets
  `pred = self.clean_answer(last_action["answer"])`; `clean_answer` at 80–86 strips whitespace, one
  outer quote pair, lowercases; `exact_match` at 90–94 cleans both sides; the `"fuzzy_match"` /
  `value == "N/A"` branch is 150–155; the fallback assignment `score = 1.0 * self.ua_match(...)` is
  158–163.
- `ua_match` (120–121) → `llm_ua_match` at `helper_functions.py:176–208`; the judge call is
  196–203 with `model="gpt-4-1106-preview", temperature=0`; the prompt is 184–190; parsing is
  204–208 (`"different"` → 0.0, else `assert "same" in response` → 1.0); the provider import is
  18–20.
- `HTMLContentEvaluator` `must_include` is 312–327; sibling JSON for 552–555 uses
  `__GITLAB__/byteblaze/gimmiethat.space/-/raw/main/<dir>/urls.txt` with concrete `must_include`
  lists (verified for all four siblings).

### Population claims (independent census)

- 812 entries, 812 distinct IDs, min 0 / max 811, no missing/duplicate IDs.
- 36 tasks have `reference_answers.fuzzy_match == "N/A"`; all 36 have `eval_types ==
  ["string_match"]` and only the `fuzzy_match` reference key.
- 791 is the only N/A task whose sorted site set is `gitlab+reddit`; the `(gitlab,reddit) ×
  (string_match)` stratum contains exactly one task (791), matching the frozen selection rule.
- `intent_template_id 84` has five tasks: 552–555 (`program_html`, concrete reference contents) and
  791 (`string_match`, N/A). "Only unachievable instance" is a fair reading of the N/A marking; the
  word "achievable" for 552–555 is an inference from their concrete references, not a runtime check
  (see F6).
- Candidate counters I independently reproduced: 27 strata; 16 selected IDs equal
  `selected-task-ids.json` in order; 651 `program_html` targets; operator presence exact_match 45 /
  must_include 176 / fuzzy_match 118; page-content 188 exact + 463 must_include; locator classes
  105 full-page / 524 JavaScript / 22 helper; URL classes 238 last / 338 navigation / 75 helper.

## Falsified claims (FAIL)

### F1 — "the 46 distinct `__REDDIT__/f/<name>` forum names that appear anywhere" is false as scoped

Independent census over the complete raw file:

- Distinct `__REDDIT__/f/<name>` names in the **whole file: 47**.
- Distinct names in the eval/reference subtrees (`reference_answers`, `reference_url`,
  `program_html`): **46**.
- Set difference: exactly `pics`. It appears only in five `start_url` values —
  `"start_url": "__REDDIT__/f/pics"` at lines 20619, 20666, 20713, 20760, 20807 — and in no
  reference string.

So the report's 46-name list is the reference-string union (consistent with its next sentence,
"This list comes from reference strings in tasks"), but the qualifier "appear anywhere in the 812
tasks" is false: anywhere = 47. The substantive conclusion — the set does not contain `cars` — holds
in both the 46-name and 47-name sets. The error is a scope/count error in an [INFERENCE] paragraph,
not a change to the task verdict.

### F2 — "the only other 'car' hit is task text at line 20279" is false

Mapping every `\bcar(s)?\b` line to its owning `task_id` in the raw file gives these counterexamples
(all outside the 791 block at 28793/28794/28797):

| task(s) | line anchors | text |
|---|---|---|
| 36, 37, 38, 39, 40 | 1173–1298 | "… can be reached in one hour by car …" |
| 151, 152, 153, 154, 155 | 4859–4992 | "minimum travel time by car from …" |
| 287 | 8999, 9001 | "… from Pittsburgh to Philadelphia by car?" |
| 601 | 20090, 20092, 20107 | "is car necessary in NYC" (intent and `must_include`) |
| 606 | 20277, 20279, 20294 | "is car necessary" (instantiation, intent, `must_include`) |
| 643 | 21764, 21768, 21783 | "racing cars" (instantiation, intent, `must_include`) |

In total 14 task IDs contain the word `car` (including 791) and 2 contain `cars` (643, 791).
Line 20279 is neither the only other "car" hit nor the only other NYC "is car necessary" task: task
601 at line 20092 has "is car necessary in NYC", and task 606 alone has three hits (20277, 20279,
20294). The narrower statement "No other task references `cars` as a forum" remains true — there is
no `__REDDIT__/f/cars`, and task 643's subreddit is `nyc` — but the "only other hit" sentence is
decisively false.

### F3–F6 — unmarked inferences / minor overreach

- **F3:** "Any mutation persists because `require_reset: false`." The pinned JSON stores the boolean;
  the reset/persistence semantics live in unpinned harness code. The report marks the forum-list
  inference [INFERENCE] but not this one.
- **F4:** "It uses the external OpenAI API." The pinned helper imports `llms.providers.openai_utils`
  and names `gpt-4-1106-preview`; the provider module/endpoint is not in the pinned fixture set.
  Model string and temperature are verified; "external OpenAI API" is an inference.
- **F5:** "`trajectory[-1]` must be a stop action." Lines 47–56 only index `trajectory[-1]` and raise
  `ValueError` on exception; the `is_bearable` line is commented out and `get_last_action` is not
  `@beartype`-decorated. The `"answer"` key is accessed at 134. The stop-action convention is upstream
  harness, not pinned source.
- **F6:** "siblings 552–555 are achievable." Their concrete `program_html` references make them
  non-N/A, but "achievable" is an inference from static content, not a runtime observation. The
  report's own final verdict is static-only, so this is a wording overreach.

## Decisive boundary/control

### C1 — exact-match boundary (independent probe)

I reimplemented `clean_answer`, `exact_match`, and the routed path of lines 134/155 from the pinned
source (own code, no upstream import, `python3 -B`). The routed path cleans the answer, then
`exact_match` cleans it a second time.

| answer string | step-2 result |
|---|---|
| `N/A`, `n/a`, ` N/A `, `N/A\n` | exact 1.0 |
| `"N/A"`, `'N/A'`, `""N/A""`, `''N/A''` | exact 1.0 (double clean at 134 and 92) |
| `'''N/A'''`, `N/A.`, `N/A!` | judge branch (0.0 at step 2) |
| `N/A because the subreddit does not exist` | judge branch |
| `The subreddit does not exist` | judge branch |
| `cars` | judge branch |

This is a decisive control for the report's central branch claim: step 2 is exact normalized equality,
not semantic equivalence; any extra token sends the answer to `llm_ua_match`, where the remote judge
decides. The report's description of the branch is correct. Its "bare N/A" phrasing is
under-inclusive (double-quoted forms also pass) but not false. It also confirms the report's "No
reason is required" and "Only reached when the answer is not a bare N/A" statements.

### C2 — census scope control

The 46/47 difference is exactly `pics` (five `start_url` lines, no reference occurrence). This shows
(a) the report's "anywhere" qualifier is wrong, and (b) the name list is a task-authored reference
subset, not a site inventory — a conclusion the report itself draws and marks [INFERENCE]. The
absence of `cars` is stable across the 46-name and 47-name sets.

### C3 — uniqueness control

The task-level car mapping in F2 is exhaustive over `\bcar(s)?\b` in the raw file. It decisively
refutes the "only other hit" sentence; no runtime evidence is needed for that text-level claim.

## Candidate-level check (frozen draft, SHA256 above)

The frozen draft mentions 791 at three places only:

- line 60: selected IDs include 791 (matches `selected-task-ids.json`);
- line 71: row `44,552,681,791 | Task044.md, Task552.md, Task681.md, Task791.md | URL-only
  navigation, fixed link set, cross-site literals, N/A exact/fallback branch`;
- line 85: "**Task173/791:** remote-judge-dependent branches remain runtime-unverified; exact N/A is
  a separate branch."

The 791 halves are supported by the pinned bytes: `exact_match` short-circuits the judge at 150–155;
the fallback enters `llm_ua_match` at 158–163, which calls `gpt-4-1106-preview` at 196–203 and
parses response keywords at 204–208; no judge request was made. The draft does **not** repeat the
build report's 46/47 census or the "only other car hit" sentence, so its 791-specific language does
not exceed source. The 173 half of the joint sentence is outside this ticket. The draft's general N/A
claims ("all N/A tasks use only that approach", "exact N/A bypasses the reason judge", "two LLM
helper branches") are all verified above. Its reproduced counters also agree with my independent
census.

## Verdict

| scope | verdict |
|---|---|
| Task791 raw task-spec mapping, evaluator anchors, checked/unchecked clauses | **PASS** |
| Task791 population counts (36/812, 1 gitlab+reddit, 1 stratum, template 84 = 5, siblings 552–555) | **PASS** |
| Task791 auxiliary census/uniqueness claims F1, F2 | **FAIL** |
| Task791 unmarked inferences F3–F6 | **PARTIAL** |
| Frozen candidate's 791-specific language | **PASS** (does not exceed source) |
| Overall build case 791 | **PARTIAL** |

The build case's central static mapping is sound and its checked/unchecked table is fully traceable.
It is not a clean PASS because two auxiliary source claims in the [INFERENCE] paragraph are false:
the forum-name count is 46 only for reference strings (47 anywhere, `pics` via five `start_url`
lines), and line 20279 is not the only other "car" hit. Those errors do not change the task's
PARTIAL (static-only) validity verdict, and the frozen candidate's 791-specific language remains
within source. L1 should treat F1/F2 as author-side report corrections, not as candidate edits.

VERDICT: PARTIAL

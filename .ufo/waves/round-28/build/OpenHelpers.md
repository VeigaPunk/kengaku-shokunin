# OpenHelpers — S063 helper-functions source opening (round 28, author-side)

Writer/seat: KengakuR28.OpenHelpers-2 (UFO-FSD scout, read-only leaf; no delegation).
Scope: open the pinned WebArena `evaluation_harness/helper_functions.py`, ground the LLM fuzzy and unachievable-reason (UA) judge prompts and how their responses are handled, record the dynamic URL and locator helper dependencies, check the license, and propose registry row S063. The registry was not edited. This is author-side advice, not outside closure.

## Opening record

- URL: https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/helper_functions.py
- Access date: 2026-10-21. HTTP 200, 7565 bytes.
- SHA-256 of the fetched upstream bytes: `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275`. This matches the expected digest, `plans/fixtures/r28/webarena/manifest.json`, and the local snapshot.
- The upstream bytes and `plans/fixtures/r28/webarena/evaluation_harness/helper_functions.py` are byte-equal (`cmp` reported no difference). Scratch copy: `.ufo/waves/round-28/scratch/OpenHelpers/helper_functions.upstream.py`.
- Located quote (19 words), `helper_functions.py:169–173`, in `llm_fuzzy_match`. It shows how the judge's response is handled:
  > `if "partially correct" in response or "incorrect" in response: return 0.0 else: assert "correct" in response return 1.0`
- Supporting anchors, cited by line only:
  - fuzzy prompt `:150–156`, ending "Conclude the judgement by correct/incorrect/partially correct."
  - model call `:161–168`
  - UA prompt `:180–190`
  - UA response handling `:204–208` (`if "different" in response: return 0.0 else: assert "same" in response`)

## License

- `plans/fixtures/r28/webarena/LICENSE` is Apache License 2.0, 11357 bytes, SHA-256 `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`.
- It is byte-equal to the LICENSE fetched from the same pinned revision (HTTP 200, `cmp` equal).
- The appendix copyright line is the unfilled template `Copyright [yyyy] [name of copyright owner]`, and `helper_functions.py` has no per-file license header.
- `NOTICE` at the pinned revision returned HTTP 404, so there is no NOTICE file to carry under Apache §4(d).
- Redistributing the snapshot inside the lane is compatible with Apache-2.0 if the LICENSE copy is kept. This is a reading of the license text, not legal advice.

## Observed facts (source's own behavior, static reading)

**Fuzzy judge (`llm_fuzzy_match`, `:146–173`)**
- The prompt is grader-framed and inserts question, reference and student answer directly into the text with no escaping (`:150–155`).
- It tells the judge that "N/A" means not achievable (`:153`).
- Call settings: `model="gpt-4-1106-preview"`, `temperature=0`, `max_tokens=768`, `top_p=1.0`, `context_length=0`, and the response is lower-cased (`:161–168`).
- The docstring says "GPT4-turbo".
- Scoring is by substring:
  - "partially correct" or "incorrect" anywhere in the response gives 0.0.
  - Otherwise the code asserts "correct" is present and returns 1.0 (`:169–173`).
  - Because "incorrect" contains "correct", the 0.0 check has to run first, and it does.

**UA judge (`llm_ua_match`, `:176–208`)**
- The prompt compares the "actual unachievable reason" with the "reported unachievable reason" and asks for 'same' or 'different' (`:180–190`).
- Call settings are identical to the fuzzy judge, including `gpt-4-1106-preview`. The docstring says "GPT-turbo", which does not match the model the code calls.
- "different" anywhere gives 0.0; otherwise the code asserts "same" and returns 1.0 (`:204–208`).

**Dynamic URL helpers**
- `shopping_get_latest_order_url` (`:38–59`):
  - Gets an admin token via `shopping_get_auth_token` (`:23–35`). That function POSTs `ACCOUNTS["shopping_site_admin"]` username and password to `{SHOPPING}/rest/default/V1/integration/admin/token` and does not check the response status.
  - Fetches `/rest/V1/orders` sorted by `created_at` DESC with page size 1, asserts HTTP 200, and builds `/sales/order/view/order_id/{increment_id}/`.
- `reddit_get_post_url` (`:97–112`):
  - Pure URL parsing that rebuilds `scheme://domain/f/{subreddit}/{post_id}/`.
  - Returns the input unchanged if the path has fewer than 4 segments or does not start with `/f`.

**Locator helpers**
- `shopping_get_sku_latest_review_author` (`:62–76`) and `shopping_get_sku_latest_review_rating` (`:79–94`) call live REST endpoints.
  - Rating asserts on `response_obj[0]` (`rating_name == "Rating"`) but returns `response_obj[-1]`'s percent. The guard checks the first review, the value comes from the last.
  - Both treat the last list element as "latest". The file does not document the API's ordering.
- `gitlab_get_project_memeber_role` (`:115–143`):
  - The name is misspelled upstream.
  - It runs two JavaScript snippets in the page, inserting `account_name` with f-strings.
  - A blanket `except Exception` returns `""`.

**Other code facts**
- `PseudoPage` (`:211–221`) overrides `url` and passes every other attribute to the wrapped page.
- No `requests` call sets a timeout.

**Dependencies not in the snapshot (unopened)**
- `browser_env.env_config` provides `ACCOUNTS` and the site base URLs.
- `llms.providers.openai_utils.generate_from_openai_chat_completion`: what `context_length=0` does is unknown.
- Imported names that each appear only once (in the import, so they are unused in this file): `GITLAB`, `MAP`, `REDDIT`, `SHOPPING_ADMIN`, `WIKIPEDIA`, `CDPSession`.

## How the scorer reaches the helpers (S062-scope cross-reference)

Supporting only; `evaluators.py` belongs to the scorer seat. SHA-256 `e23edb39…0c22` matches the manifest.

- Imports: `evaluators.py:18–27`.
- `fuzzy_match` and `ua_match` wrappers: `:114–121`.
- For each fuzzy reference, the evaluator makes a separate judge call and multiplies the results (`:164–169`).
- N/A path (`:152–163`): exact match against "N/A" first; if that fails, `score = 1.0 * ua_match(...)` against `string_note` overwrites the accumulated score instead of multiplying into it.
- Program-HTML targets:
  - A `url` starting with `func` has `__last_url__` replaced by `page.url` and is then passed to Python `eval` (`:263–266`).
  - A `locator` starting with `func:` has `__page__` replaced by `page` and is then passed to `eval` (`:296–299`).
- The helpers are therefore called by name through strings taken from the task config.

## Raw task usage counts

These counts come from parsing `config_files/test.raw.json` as JSON with stdlib only; no upstream code was imported or run. File SHA-256 `7b50386f…7652` matches the manifest.

- 812 tasks in total.
- 118 tasks have `reference_answers.fuzzy_match`:
  - 82 are non-N/A and reach `llm_fuzzy_match` once per reference.
  - 36 are `"N/A"` and reach `llm_ua_match` only if the exact match fails.
- 79 distinct tasks have at least one program-HTML target that calls a helper by string. Distinct tasks per helper:

| Helper | Called from | Tasks |
|---|---|---|
| `reddit_get_post_url` | url | 55 |
| `shopping_get_latest_order_url` | url | 10 |
| `gitlab_get_project_memeber_role` | locator | 9 (12 targets) |
| `shopping_get_sku_latest_review_rating` | locator | 5 |
| `shopping_get_sku_latest_review_author` | locator | 5 |

- In the frozen 16-task selection:
  - Task 173 (`string_match`+`url_match`) has fuzzy reference `["No, it is open"]`, so it reaches the fuzzy judge.
  - Task 791 (`string_match`) has fuzzy `"N/A"`, so it reaches the UA judge if the exact match fails.
  - None of the 16 uses a `func:` helper target.
- Auth-state paths: 684 tasks name a `storage_state` (`./.auth/shopping_admin_state.json` 182, `shopping_state` 187, `reddit_state` 111, `gitlab_state` 186, `gitlab.reddit_state` 18) and 128 have none. These are recorded as config strings only. No auth file or credential data was fetched or read, and `env_config.ACCOUNTS` was not opened.

## Inferences (not observed; marked)

- [INFERENCE] Substring scoring can misread negated wording. "not incorrect" scores 0.0 and "not different" scores 0.0. A response with none of the keywords raises `AssertionError` instead of producing a score.
- [INFERENCE] Hosted-model output at temperature 0 is not guaranteed identical across calls or model updates. The judge result is therefore not a frozen function of task plus prediction.
- [INFERENCE] The unescaped student answer inside the prompt is an untrusted-input surface for the judge. This is noted as a limitation only; no exploit was built.
- [INFERENCE] In `gitlab_get_project_memeber_role`, if the account is not found, index -1 is used. In JavaScript, `NodeList[-1]` is `undefined`, so `.outerText` throws, the blanket except catches it, and the role is `""`, which cannot be told apart from other failures.
- [INFERENCE] The dynamic URL helpers depend on live site state ("latest order" or review at scoring time) and admin credentials, so their targets cannot be statically resolved from the snapshot.

## Proposed registry rows (not entered; L1 decides)

Registry columns: id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by.

**S063 (Helpers), proposed:**

| S063 | WebArena evaluation_harness/helper_functions.py @dce04686 — https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/helper_functions.py | code | A | the file's own LLM-judge prompt/response handling and dynamic URL/locator helper code at this pin, not judge accuracy, benchmark-wide validity, unopened env_config/openai_utils, or WebArena-Verified | llm_fuzzy_match :146–173; llm_ua_match :176–208; shopping/reddit/gitlab helpers :23–143; PseudoPage :211–221; sha256 ec758da4…7e275 byte-equal to local snapshot; Apache-2.0 LICENSE c71d239d…0ab4 | fuzzy/UA judges call gpt-4-1106-preview at temperature0 and score by keyword substring (incorrect/partially correct→0, different→0; missing keyword asserts); URL/locator helpers query live site APIs or page DOM, so those targets cannot be resolved from the static snapshot | (proposed) mined | 2026-10-21 | pinned (immutable commit; recheck on re-pin) | (C1 round-28 knowledge draft path to be assigned by L1) |

Tier A covers only what this file's code itself does. Runtime claims (judge determinism, failure frequency, how the hosted model behaves) are not tier A and are not claimed. Status becomes `mined` only once an admitted knowledge file cites S063 and lists it in used-by. This row does not enter C2.

**S061 (Tasks) and S062 (Scorer).** These are other seats' openings, so I am not proposing full rows for them. What I observed:
- `test.raw.json` and `evaluators.py` match the manifest digests.
- The `evaluators.py` anchors in the cross-reference section above can serve S062.
- The raw-task helper counts above can serve S061.

## Limitations

- Static reading only: no upstream code was imported, run or `eval`ed, no benchmark site or LLM was contacted, and no browser was used. The only network calls were the three pinned GitHub raw URL fetches (helper file, LICENSE, NOTICE probe).
- `env_config.py` and `openai_utils.py` were not opened.
- The task counts depend on the pinned JSON and on the `func:` prefix test used by the scorer.
- The quote is code text, not prose. It grounds response handling; the prompt wording is cited by line rather than quoted, to stay within the 25-word limit.
- No tools were installed or updated, no pacman was used, and no REA MCP was used.

## Commands run

- `sha256sum` on the snapshot files.
- `curl -sS` of the pinned helper, LICENSE and NOTICE URLs into scratch.
- `cmp` against the local snapshot files.
- `python3` stdlib `json.load` on `test.raw.json` for counts.
- `grep -c` for import names in `helper_functions.py`.

## Verdict

PASS for this assignment's scope: the pinned helper source was opened, its digest matches and the bytes equal the local snapshot, there is one located quote of 25 words or fewer dated 2026-10-21, the license was checked, the dependencies and limits are recorded, and the S063 draft row is proposed. PARTIAL for S061/S062, which are left to their own seats; supporting anchors only. This is not a round-28 PASS and not outside closure.

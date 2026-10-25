# FRevTokenSemantics — runtime semantics of `__last_url__` and `__page__` in the pinned evaluation_harness

writer: KengakuR29-2.FRevTokenSemantics-2
date: 2026-10-21
item: Falsify integrated generated-config projection — token-semantics slice. Attack: reconstruct what `__last_url__` and `__page__` mean at runtime in the pinned evaluation_harness (static reading only) and try to falsify the integrated state's claim that they are not env tokens substituted by the generator.
godspeed axes: (1) semantic fidelity of the reconstruction, (2) byte-exactness of pins/counts, (3) mismatch coverage across the integrated round-29 state.

## Pins (sha256 computed on pinned bytes, matched against manifests)

| file | sha256 | manifest check |
|---|---|---|
| plans/fixtures/r29/generate_test_data.py | 45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd | matches r29 manifest |
| plans/fixtures/r28/webarena/config_files/test.raw.json | 7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652 | matches r28 and r29 manifests |
| plans/fixtures/r28/webarena/evaluation_harness/evaluators.py | e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22 | matches r28 manifest |
| plans/fixtures/r28/webarena/evaluation_harness/helper_functions.py | ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275 | matches r28 manifest |

Upstream revision pinned by both manifests: dce04686a56253aefba7b18a4fa0937cf1dc987b.

## Method

Static reading of pinned bytes only. Upstream code was never executed or imported; `browser_env.env_config` is not pinned and was never fetched. One experiment ran on a copy of test.raw.json under /tmp/frev-token-semantics/ (my own stdlib re-implementation of the six documented `str.replace` steps, not upstream execution). Word counts of every quote below were counted programmatically (python `str.split`) and each is ≤25 words.

## Finding 1 — runtime semantics of `__last_url__` (URL-valued, evaluation-time)

Handled only in `HTMLContentEvaluator.__call__` (evaluators.py), for `eval.program_html[*].url` fields:

- evaluators.py:263 `if target_url.startswith("func"):` (2 words)
- evaluators.py:264 `func = target_url.split("func:")[1]` (4 words)
- evaluators.py:265 `func = func.replace("__last_url__", page.url)` (4 words)
- evaluators.py:266 `target_url = eval(func)` (3 words)

`page` is the `Page | PseudoPage` argument the evaluator receives at scoring time, i.e. the final live browser page of the agent trajectory (`EvaluatorComb.__call__`, evaluators.py:339-352, passes the same `page` to every evaluator). So `__last_url__` is a runtime placeholder for the URL of the page under evaluation at the end of the episode — not a constant in the config. `PseudoPage` (helper_functions.py:211-221) carries its own override:

- helper_functions.py:212 `def __init__(self, original_page: Page, url: str):` (6 words)
- helper_functions.py:213 `self.url = url` (3 words)
- helper_functions.py:219 `return getattr(self.original_page, attr)` (5 words)

so `page.url` resolves to the pseudo-page's pinned URL when callers substitute one, else the real page's URL. The classic data use (test.raw.json:20066) is `"url": "func:reddit_get_post_url('__last_url__')"`: after substitution, `eval` calls `reddit_get_post_url(<final url>)` (helper_functions.py:97-112) which maps a subreddit-listing URL to its post URL (helper_functions.py:111 `post_url = f"{scheme}://{domain}/f/{subreddit}/{post_id}/"`, 7 words), and the evaluator then navigates:

- evaluators.py:271 `if target_url != "last":` (4 words)
- evaluators.py:272 `page.goto(target_url)` (2 words)

The unrelated string `"last"` (no token) means "keep the current page". `URLEvaluator` never touches tokens; it consumes the same final page directly: evaluators.py:212 `pred = clean_url(page.url)` (3 words).

## Finding 2 — runtime semantics of `__page__` (object reference, not a value)

Handled only in the `locator` branch of the same evaluator, for `eval.program_html[*].locator` fields:

- evaluators.py:296 `elif locator.startswith("func:"):  # a helper function` (6 words)
- evaluators.py:298 `func = func.replace("__page__", "page")` (4 words)
- evaluators.py:299 `selected_element = eval(func)` (3 words)

`__page__` is replaced by the bare Python identifier `page`; the resulting expression is `eval`'d in the evaluator's scope, binding the live page object as argument. Example (test.raw.json:15304): `"locator": "func:gitlab_get_project_memeber_role(__page__, 'abisubramanya27')"` becomes `gitlab_get_project_memeber_role(page, 'abisubramanya27')`, whose implementation (helper_functions.py:119-146) drives `page.evaluate` twice over the currently open GitLab project-members page and returns the role string. So `__page__` is metasyntactic sugar for the evaluator's in-scope `page` variable — it never expands to a URL, domain, or any env-derived string.

Token wiring is reached only via the router: evaluators.py:369 `case "program_html":` (2 words) / evaluators.py:370 `evaluators.append(HTMLContentEvaluator())` (2 words). `helper_functions.py` contains 0 occurrences of either token; `URLEvaluator` and `StringEvaluator` contain none.

## Finding 3 — the generator does not substitute these tokens (static proof + copy experiment)

Pinned generator (generate_test_data.py) reads the raw text and applies exactly six replacements, lines 11-16, e.g. line 11 `raw = raw.replace("__GITLAB__", GITLAB)` (4 words), then writes and splits positionally (lines 17-23). Byte counts of the six needle strings in the generator are 1 each; `__last_url__` and `__page__` occur 0 times in the generator file. `from browser_env.env_config import *` (line 5, 4 words) supplies only the six constants used in those calls; no other imported name is referenced.

Static disjointness: none of the six needles is a substring of `__last_url__` or `__page__`, nor vice versa, so six `str.replace` calls cannot alter those occurrences. Empirically, on the /tmp copy, applying exactly the six replacements in manifest order left `__last_url__` at 65 and `__page__` at 12 (65/12 before and after) and drove all six site tokens to 0.

## Finding 4 — occurrence census on the pinned raw (programmatic counts, not inferred)

Serialized byte counts in test.raw.json: `__last_url__` 65, `__page__` 12, `__GITLAB__` 385, `__REDDIT__` 336, `__SHOPPING__` 281, `__SHOPPING_ADMIN__` 300, `__WIKIPEDIA__` 0, `__MAP__` 133. Decoded (post-`json.loads`) string-leaf counts are identical: 65 and 12; 0 occurrences inside JSON keys. Field provenance: every `__last_url__` occurrence sits in an `eval.program_html[*].url` leaf of tasks with list indices 600-649 (50 tasks) and 671-675 (5 tasks, 10 leaves); every `__page__` occurrence sits in an `eval.program_html[*].locator` leaf of indices 481-485 (5) and 576-579 (4 tasks, 8 leaves). Neither token appears in `intent`, `start_url`, reference answers, or any other field. `__WIKIPEDIA__` = 0 means the replacement is unexercised by the frozen population.

## Finding 5 — cross-check against the integrated round-29 state

- plans/config_projection.py:29 fixes the token set to exactly the six `ORDER` names; its census counts only those as environment tokens.
- config_projection.py:451 (selftest, hand case R29-URL-ONLY-UNREAD-METADATA-01) asserts `other_double_underscore_markers == {"__last_url__": 1, "__page__": 1}` — i.e. the instrument classifies both as "other double-underscore markers", not env tokens. Consistent with Findings 3-4.
- Knowledge draft .ufo/waves/round-29/drafts/webarena-config-projection.md line 46 records "other `__…__` markers, not env tokens | `__last_url__` 65, `__page__` 12" — counts and classification both match my independent reconstruction of the pinned bytes.
- The hand fixture (plans/fixtures/r29/hand/url-only.fixture.json, raw_text tail) carries `"fixture_markers":"__last_url__ __page__"` as synthetic task metadata; the expected output (url-only.expected.json:19) passes that leaf through verbatim with `remaining_known_environment_token_occurrences: 0`. Consistent: the markers are unread metadata, not substituted values.
- Prereg plans/round-29-claims.md line 105 (F2 "remaining six known tokens 0") is six-token scoped, matching the generator's six `str.replace` steps.

## Mismatches

None found. Every checked characterization of `__last_url__` and `__page__` in the integrated state (instrument classification and selftest expectation, knowledge-draft counts, hand-fixture semantics) agrees with the independent reconstruction from pinned harness and generator bytes. The only semantic nuance the integrated artifacts do not spell out — and none of them states wrongly — is the precise split: `__last_url__` substitutes a runtime value (final page URL) inside `func:` url expressions, while `__page__` substitutes a variable name binding the live page object inside `func:` locator expressions; neither is produced or consumed by the generator.

## Provenance and disclosure

- I read production source plans/config_projection.py (grep-selected lines only: 28-32, 294-341, 378-382, 400-465) for the classification cross-check; my item is not an oracle/re-derivation item, so this is permitted. The semantics derivation itself came solely from pinned fixture bytes.
- No tools were installed or upgraded (stdlib only; pacman paused host-wide per lane contract).
- Writes: this report plus /tmp/frev-token-semantics/ scratch copy only; no production, fixture, corpus, or lane-state mutation.

VERDICT: PASS

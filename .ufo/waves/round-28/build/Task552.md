# Round 28 C1 case audit: WebArena task 552

- Writer/seat: `KengakuR28.Task552-2` (read-only scout seat, author-side advice; not outside closure)
- Scope: a static task-spec/scorer trace of one task (`task_id` 552) against the pinned snapshot. This is not a benchmark-wide verdict, a browser-level truth claim, or a validity ruling.
- Snapshot: `plans/fixtures/r28/webarena/` at upstream `dce04686a56253aefba7b18a4fa0937cf1dc987b` (`manifest.json`, opened 2026-10-21).
- No upstream code was executed, imported or evaluated. No benchmark site was contacted. No browser actions were run. No tools were installed or updated.

## Observed command

```
cd plans/fixtures/r28/webarena && sha256sum config_files/test.raw.json evaluation_harness/evaluators.py evaluation_harness/helper_functions.py
7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652  config_files/test.raw.json
e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22  evaluation_harness/evaluators.py
ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275  evaluation_harness/helper_functions.py
```

All three match the `sha256` values in `manifest.json` (lines 7, 12, 17).

## Task spec (`config_files/test.raw.json` lines 17868–17909)

| Field | Value (line) |
|---|---|
| `sites` | `["gitlab","reddit"]` (17869–17872) |
| `require_login` / `storage_state` | `true` / `./.auth/gitlab.reddit_state.json` (17874–17875) |
| `start_url` | `__GITLAB__` (17876) |
| `intent_template_id` | 84 (17908). Siblings are tasks 553–556 and the one at line 28811. |
| `intent` | "Create a folder named real_space in gimmiethat.space repo. Within it, create a file named urls.txt that contains the URLs of the 5 most recent posts from the space?" (17884) |
| `require_reset` | `false` (17885) |
| `eval_types` | `["program_html"]` (17887–17889) |
| `reference_answers` / `reference_url` | `null` / `""` (17890–17891). These are unused because `string_match` and `url_match` are not declared. |
| `program_html[0].url` | `__GITLAB__/byteblaze/gimmiethat.space/-/raw/main/real_space/urls.txt` (17894) |
| `program_html[0].locator` | `""` (17895) |
| `required_contents.must_include` | 5 strings, `__REDDIT__/f/space/{134164,134163,134162,134161,134160}/<slug>` (17897–17903) |

## Intent → evaluator operator/target mapping

| Intent component | Evaluator mechanism (anchor) | Operator / target | Checked? |
|---|---|---|---|
| Routing | `evaluator_router` builds `HTMLContentEvaluator` (`evaluators.py` 356–374, case at 369–370) and `EvaluatorComb` multiplies the scores (336–352) | One evaluator. The score is the product over targets and over `must_include` items. | Yes |
| "in gimmiethat.space repo" | The fixed target URL is `byteblaze/gimmiethat.space` (17894) | `page.goto(target_url)` and then `time.sleep(3)` (`evaluators.py` 271–273) | Indirectly. The check is pinned to namespace `byteblaze` and branch `main`. |
| "folder named real_space … file named urls.txt" | The raw-file path `-/raw/main/real_space/urls.txt` | Only implied by fetching that path. There is no folder or tree check. | Indirectly, and only as file reachability on `main` |
| "contains the URLs of the 5 most recent posts" | The empty locator takes the whole document: `selected_element = page.content()` (276–277), then `html.unescape` (303) | For each of the 5 refs: `" |OR| "` split (316), `StringEvaluator.must_include(ref, pred, tokenize=False)` (318–323), which is `clean_answer(ref) in clean_answer(pred)` after strip, outer-quote removal and `.lower()` (80–86, 98–111). The scores multiply (327). | Yes, as five case-insensitive substrings of the serialized page HTML |
| "from the space" (forum `/f/space`) | `space` is embedded in each ref string | Static literals | Only via literals. No live reddit read happens at scoring time. |
| Helper functions | None are referenced. The `url` and `locator` fields are not `func:` (263–266, 296–299). | n/a. `reddit_get_post_url` (`helper_functions.py` 97–112) exists but is not used here. | n/a |

## Checked vs unchecked properties

**Checked:**
- The raw endpoint for `main/real_space/urls.txt` returns a page whose serialized HTML contains each of the five reference strings. Matching is case-insensitive, and a reference only has to appear as a substring.

**Unchecked:**
- Count ("5"): extra URLs are not penalized, so a superset list passes.
- Order of the URLs and file format (separators, one-per-line).
- Whether `real_space` exists as a directory independently of the file.
- Commit message and author.
- The branch used, beyond the fact that `main` must serve the file. A merge request left unmerged on another branch fails.
- Whether the agent's trajectory produced the file. The evaluator ignores `trajectory` for `program_html`.
- That no other repository content was harmed.
- Live recency of reddit posts.

## Dynamic state / judge dependencies

- **No LLM judge.** `fuzzy_match` and `ua_match` are not reachable from `program_html` (305–332).
- **Placeholder substitution is outside the pinned files.** Neither `evaluators.py` nor `helper_functions.py` replaces `__GITLAB__` or `__REDDIT__`. Literal `__GITLAB__/...` is passed straight to `page.goto` (271–272). [INFERENCE] An upstream config-generation step outside this snapshot must substitute the hosts. The substituted host strings are therefore part of each reference, and the snapshot cannot resolve them.
- **GitLab state.** The repo `byteblaze/gimmiethat.space` must exist with a `main` branch. The raw endpoint must be readable from the evaluator's page, which is the agent's own `page` and inherits the `storage_state` session.
- **Reddit state.** The references freeze "5 most recent" to post IDs 134160–134164 and their slugs. This is correct only if the reddit snapshot has no newer `/f/space` posts at evaluation time, and if "most recent" means that ID/creation ordering (as opposed to sticky posts or another sort).
- **Cross-task state.** A literal grep of the other 811 intents found no task that plans to post in `/f/space`. Line 971 only reads it, and line 19870 subscribes. Other tasks do write to `gimmiethat.space`: lines 17926, 17968, 18010 and 28797 use other folders, line 26194 edits the LICENSE, and lines 18518 and 10854 concern membership. None of them targets `real_space/urls.txt`. This is grep evidence only, not semantic proof. No LSP server applies to JSON data.
- **Timing.** A fixed 3-second sleep follows navigation (273).

## Potential validity limitation (task-specific, not a proven defect)

1. **Narrow URL form with a non-exhaustive answer.** Each reference is one host plus slug serialization. A file holding semantically equivalent post identifiers fails. Examples are slugless `…/f/space/134164`, which Postmill may resolve [INFERENCE], a different host alias or scheme, or relative paths. The pinned harness has a normalizer that is not applied here (`reddit_get_post_url`, `helper_functions.py` 97–112). In the other direction, any file that contains the five strings passes, even with many extra URLs, so "the 5 most recent" is not enforced as exactly five.
2. **Stale-artifact credit.** `require_reset: false` combines with a check that reads only the end state and ignores the trajectory (the `program_html` path never reads `trajectory`). A `real_space/urls.txt` left by an earlier attempt or run would score 1.0 for a later trajectory that did nothing. [INFERENCE] Whether this occurs depends on the reset practice of the harness or operator.

## Runtime evidence required before declaring 552 valid or invalid

1. The generated per-task config for 552 after substitution, with concrete `__GITLAB__` and `__REDDIT__` values.
2. The reddit environment snapshot at reset time, showing that `/f/space` has newest posts 134164…134160 with these exact slugs, and how sticky posts or sort mode affect "most recent".
3. GitLab reset state: `byteblaze/gimmiethat.space` exists, the default branch is `main`, `real_space/` is absent at start, and the raw endpoint is reachable with the stored session.
4. An instrumented evaluator run in a sanctioned environment showing `page.content()` for:
   - a correct file (expected score 1),
   - a slugless or other-host variant (tests limitation 1),
   - a superset list,
   - a pre-seeded file with an empty trajectory (tests limitation 2).
   This is not performed here and is out of seat scope.
5. The run-order and reset policy used for reported scores.

Without items 1–5, static evidence supports only the scorer contract mapping above, not task validity.

## Compact case row (for L1)

| task_id | sites | eval_types | target | locator | operator | n refs | checked | unchecked | dyn deps | judge | limitation | anchors | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 552 | gitlab+reddit | program_html | `__GITLAB__/byteblaze/gimmiethat.space/-/raw/main/real_space/urls.txt` | `""` → `page.content()` | `must_include` (lowercase substring, product, `tokenize=False`) | 5 (`/f/space/134160–134164/<slug>`) | 5 URL strings present on the raw page on `main` | count, order, format, folder object, trajectory, live recency | host substitution outside snapshot; GitLab repo/branch/auth; reddit `/f/space` frozen top-5; `require_reset=false` | none | single URL serialization (normalizer unused) and superset passes; stale end-state credit | raw 17868–17909; evaluators 80–111, 244–333, 356–374; helper 97–112 (unused) | static mapping complete; task validity UNRESOLVED pending runtime evidence |

## Limitations

- Static parse of three pinned files only. The upstream config-generation script and the environment images are not in the snapshot.
- Statements about Chromium plain-text rendering, Postmill routing and reset practice are marked [INFERENCE].
- Cross-task interference was checked by literal grep over intents, not by semantic analysis.
- No source opening beyond the pinned local snapshot. Provenance comes from `manifest.json`, upstream `dce04686…`, accessed 2026-10-21. Quote from `evaluators.py` line 245: "Check whether the contents appear in the page".

## Final scoped verdict

**PASS** for the case-552 static intent→scorer audit: the mapping, checked and unchecked properties, dependencies, anchors and limitation are all recorded. Whether task 552 is valid stays **UNRESOLVED**, and no defect is claimed. This is not a round-level PASS.

## Erratum 2026-10-21 (appended; original bytes above unchanged, committed in 18b1922, sha256 `2c90d24c3eefbfd1fd49371627a1a7a2731c07b8a094f394c8b5a2ea0437a8c6`, 10428 bytes)

Reported by `KengakuR28` and re-verified against the pinned `test.raw.json` by grepping the `task_id` and `intent_template_id` lines. No sources were refetched and no broader checks were run.

1. **Template-84 family.** The task-spec table says siblings are "tasks 553–556 and the one at line 28811". That is wrong. Template-84 membership is **552, 553, 554, 555, 791**:
   - 552 has `task_id` at line 17873 and `intent_template_id` 84 at line 17908.
   - 553 is at 17915 / 17950.
   - 554 is at 17957 / 17992.
   - 555 is at 17999 / 18034.
   - 791 is at 28786 / 28811.

   Task 556 (`task_id` at 18041) is **template 87** (`intent_template_id` at 18082), not 84. Line 28811 is the template anchor of task 791, not a separate unnamed task. The cross-task line 28797 cited under "Dynamic state" is task 791's intent. The repo-write list there is unaffected, except that line 17926 is task 553, 17968 is 554 and 18010 is 555.
2. **Session inheritance is a runtime inference.** The statement "the evaluator's page, which is the agent's own `page` and inherits the `storage_state` session" is downgraded to **[INFERENCE]**. The pinned `HTMLContentEvaluator.__call__` (`evaluators.py` 248–254, 271–272) only shows that it calls `page.goto` on the `page` argument it is passed. Whether that page carries the agent's context or the cookies from `./.auth/gitlab.reddit_state.json` depends on runner wiring that is not in the pinned snapshot. Runtime-evidence item 3 therefore also requires the runner's page and context construction.
3. **Compact row and verdict are unchanged.** The scoped verdict stands: static mapping PASS for case 552 only, and task validity UNRESOLVED.

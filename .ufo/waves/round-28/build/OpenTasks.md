# OpenTasks — pinned WebArena raw-task source opening (round 28, C1 source-use)

Writer/seat: `KengakuR28.OpenTasks-2` (read-only scout, author-side advice — not outside non-author closure).
Opened: 2026-10-21 (UTC 13:57). Registry NOT edited; no source row admitted by this seat.
Scratch evidence: `.ufo/waves/round-28/scratch/OpenTasks/` (pinned downloads + README/LICENSE copies; data only, never executed/imported).

## Verdict

**PASS (scoped):** S061 source (pinned `config_files/test.raw.json`) was opened at its exact pinned URL. It is byte-equal to the lane snapshot and its sha256 matches the declared digest. Its dataset scope, `task_id` field and `eval` fields are grounded by a located quote plus a stdlib/jq census. S062 and S063 were also opened at their pinned URLs, and both are byte-equal to the snapshot. License: Apache-2.0, verified against both the local LICENSE and the GitHub license blob.
This is a source-opening verdict only. It is not a C1 round PASS, not a task-validity verdict, and says nothing about WebArena-Verified.

## Opening and integrity (observed)

| file @ dce04686a56253aefba7b18a4fa0937cf1dc987b | HTTP | bytes | sha256 | vs lane snapshot |
|---|---|---|---|---|
| `config_files/test.raw.json` | 200 | 880776 | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | `cmp` byte-equal; = manifest.json |
| `evaluation_harness/evaluators.py` | 200 | 13264 | `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22` | byte-equal; = manifest |
| `evaluation_harness/helper_functions.py` | 200 | 7565 | `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275` | byte-equal; = manifest |
| `LICENSE` | 200 | 11357 | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` | byte-equal; = manifest |
| `README.md` (context only, not in snapshot manifest) | 200 | — | `081c826497f9b7da4952771ee128c2215ec3532379db0fe9f7fcbd899d9c9287` | n/a |

URL base: `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/`.
GitHub API `commits/dce04686…`: committer date 2025-11-26T21:15:59Z, "Merge pull request #183 … Update README.md". `commits/main` on 2026-10-21 returned the **same SHA**, so the pin is also current upstream HEAD on the access date. The pin was not chosen as an arbitrary older revision.

Commands observed (all read-only): `curl -sS -o … -w '%{http_code} %{size_download}'`, `sha256sum`, `cmp`, `jq` field census, `grep -n`, `sed -n` on downloaded copies, `git hash-object LICENSE`, and GitHub REST `commits/<sha>`, `commits/main`, `license`, `search/repositories?q=webarena-verified`. No upstream code was executed, imported or eval'd. No benchmark site was contacted. No `.auth` file or credential was fetched.

## Located quotes (≤25 words, date 2026-10-21)

- **S061 tasks (task_id + eval fields), `test.raw.json` lines 6–7 and 18–22 (elision marked):**
  `"task_id": 0, "require_login": true, … "eval": { "eval_types": [ "string_match" ], "reference_answers": {`
  Scope: the record shape of one raw task. Every one of the 812 entries has the same 12 top-level keys, and task 723 has an extra 13th key, `string_note`.
- **S061 dataset-scope context, pinned `README.md:79`:** "After evaluating the 812 examples, reset the environment to the initial state" (12 words). Scope: the maintainer's statement of test-set size. The 812-entry count in the JSON was measured independently (below).
- **S062 scorer, `evaluators.py:363–372` (elision marked):** `for eval_type in eval_types: match eval_type: case "string_match": … case _: raise ValueError(f"eval_type {eval_type} is not supported")`
- **S063 helpers, `helper_functions.py:146–147`:** `def llm_fuzzy_match(pred: str, reference: str, question: str) -> float: """Check whether the prediction matches the reference with GPT4-turbo"""`. Line 162 adds `model="gpt-4-1106-preview"`.

## Census of S061 (jq on pinned bytes; observed)

- 812 entries, 812 unique `task_id`, min 0 / max 811 (no gaps, no duplicates); 190 unique `intent_template_id`.
- `eval_types` sets (5): string_match 325; program_html 282; program_html+url_match 129; url_match 66; string_match+url_match 10. All types are in the scorer router's closed set `{string_match, url_match, program_html}` (`evaluators.py:363–372`), so no task reaches the router's unsupported-type `ValueError`.
- `reference_answers` operators by key occurrence: must_include 176, fuzzy_match 118 (36 of them `"N/A"`, 82 lists), exact_match 45. 477 tasks have `null` reference_answers. No string_match task has null reference_answers.
- `url_note`: 196 tasks say `"GOLD in PRED"`. The rest omit it, and the scorer defaults to the same rule (`evaluators.py:215`). Seven tasks give alternative reference URLs with ` |OR| `. No url_match task has an empty `reference_url`.
- `program_html` has 651 targets in total. Their `required_contents` operators are must_include 463 and exact_match 188. Locators: 524 `document.` JavaScript, 105 empty (whole page), 22 `func:` helper calls. 14 tasks use a `func:` target URL and 5 tasks have `prep_actions`. No program_html task has an empty target list.
- Site sets (10): gitlab 180, shopping 187, shopping_admin 182, map 109, reddit 106, gitlab+reddit 18, map+wikipedia 17, gitlab+wikipedia 6, reddit+shopping 5, map+shopping_admin 2. `start_url` uses host placeholders (`__GITLAB__` 196, `__SHOPPING__` 192, `__SHOPPING_ADMIN__` 182, `__MAP__` 128, `__REDDIT__` 114) and contains no live hostnames.
- `require_login` is true for all 812 tasks, and `require_reset` is false for all 812. The README reset instruction is a separate, out-of-band step.
- **Auth-state paths:** 684 tasks name `./.auth/*_state.json` (shopping 187, gitlab 186, shopping_admin 182, reddit 111, gitlab.reddit 18). The other 128 tasks are null, and all of those are map tasks. These are relative path **strings only**: the files are not in the source snapshot and were not fetched or inspected.
- The 16 selected IDs re-derive to the plan's strata order, from (gitlab, program_html)→389 through (reddit, program_html)→399. None of the selected tasks is outside the census.

## Original versus Verified release

The opened source is the **original** web-arena-x/webarena repository at the pinned commit. `grep -i verified` returns 0 hits in `test.raw.json` and in the pinned README, so this source makes no claim about WebArena-Verified. A GitHub search returned `ServiceNow/webarena-verified` (Apache-2.0, last pushed 2026-03-08). That repo is **unopened, a lead only**, and supports nothing here. No count, scorer behavior or task judgment in this report transfers to the Verified release, and the reverse also holds.

## License (observed)

Local `plans/fixtures/r28/webarena/LICENSE` is Apache License 2.0. It is byte-equal to the pinned LICENSE, and its `git hash-object` = `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` equals the GitHub `/license` blob, which the API reports as SPDX `Apache-2.0`. The appendix still holds the template placeholder `Copyright [yyyy] [name of copyright owner]` (line 189), and the pinned README has no other license or copyright statement. [INFERENCE] Apache-2.0 §4 permits redistributing the snapshot copies with LICENSE retained. Short quotes in lane knowledge are ordinary citation. No legal opinion is offered on the data contents, such as the site content behind reference answers.

## Proposed rows (NOT admitted; L1 integrates after second-seat re-read)

Columns: id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by. Suggested `status` stays `queued` until a lesson or knowledge use lands, per the plan.

| S061 | WebArena raw test tasks — https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json | dataset | A | the original benchmark's own task-spec fields and declared evaluator targets at this pin, not task validity, solvability, live-site state or WebArena-Verified | sha256 7b50386f…37652, 880776 B; :6–7,:18–22; README:79 | 812 tasks (ids 0–811, no duplicates) across 5 eval-type sets and 10 site sets; 684 name ./.auth state paths; all require_reset false | queued | 2026-10-21 | on-release | (L1 assigns) |
| S062 | WebArena evaluators — https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py | code | A | the original scorer's own static routing and match semantics at this pin, not runtime scores or browser-level truth | sha256 e23edb39…00c22; evaluator_router :356–372; StringEvaluator :136–170; URL :212–241; HTML :258–333 | closed eval_type set with unsupported-type ValueError; GOLD-in-PRED URL rule default; multiplicative per-operator scores; HTML locators/func: targets evaluated at runtime | queued | 2026-10-21 | on-release | (L1 assigns) |
| S063 | WebArena helper functions — https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/helper_functions.py | code | A | the helpers' own declared behavior at this pin, not LLM-judge accuracy or reproducibility | sha256 ec758da4…7e275; llm_fuzzy_match :146–173; model :162; llm_ua_match :176–208 | fuzzy_match and N/A fallback call an external gpt-4-1106-preview judge in which "partially correct" scores 0; site-API helpers need live services | queued | 2026-10-21 | on-release | (L1 assigns) |

Tier A covers only each file's own content and behavior at the pin. Any claim about scorer correctness, judge reliability or benchmark difficulty needs other sources.

## Important limits

1. **Static only.** Scorer semantics are read from source text. The 118 fuzzy_match tasks, the 36 `"N/A"`→`ua_match` tasks (`evaluators.py:150–169`), the `func:` locators/URLs (22/14) and the JavaScript locators all depend on a live environment or an external LLM at runtime. Their actual outcomes are unobserved.
2. **External judge drift.** S063 pins `gpt-4-1106-preview` with temperature 0. [INFERENCE] Availability and outputs of the hosted model can change, so fuzzy-scored tasks are not reproducible from these bytes alone.
3. **Auth artefacts excluded.** `.auth/*_state.json` and `browser_env.env_config.ACCOUNTS` (imported at `helper_functions.py:9–17`) are outside the snapshot and were deliberately not fetched. The census counts path strings only.
4. **Count not quoted.** The JSON has no prose scope statement. The 812 figure is a measured census corroborated by README:79, and the README is outside the hashed manifest (its hash is recorded above).
5. **Recheck is "on-release".** The pin equals `main` as of 2026-10-21. A later upstream commit changes nothing at this pin, but it would end "pin = HEAD" as a current fact.
6. **Second seat needed.** This is one author-side seat. Quotes, line anchors and counts need an independent re-read before admission, and Q13 timing is not endorsement.

## Installs/updates

None. Pre-existing `jq` (`~/.local/bin/jq`), `curl`, `sha256sum`, `git` were used.

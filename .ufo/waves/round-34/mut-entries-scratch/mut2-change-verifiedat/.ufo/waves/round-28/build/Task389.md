# Case 389 — static task-spec / scorer audit (author-side)

Writer/seat: KengakuR28.Task389-2 (scout, read-only, leaf). Axis: novelty (legacy → canonical coverage/constructs). Author-side advice only, not outside closure.

## Inputs and integrity

Pinned snapshot `plans/fixtures/r28/webarena/` at upstream `dce04686a56253aefba7b18a4fa0937cf1dc987b` (manifest opened 2026-10-21). Local `sha256sum` matched `manifest.json` for all three files used:

| File | sha256 | Upstream URL (from manifest; not re-fetched) |
|---|---|---|
| `config_files/test.raw.json` | `7b50386f…37652` | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json |
| `evaluation_harness/evaluators.py` | `e23edb39…00c22` | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py |
| `evaluation_harness/helper_functions.py` | `ec758da4…e275` | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/helper_functions.py |

Observed commands (read-only): `sha256sum` on the three files; stdlib `python3 json.load` over `test.raw.json` to extract task 389, the template-348 siblings, the (site set, evaluator-type set) stratum, and locator/operator counts; `sed -n 12070,12110p` on the raw JSON. No upstream code imported, evaluated, or executed. No network access, no benchmark-site contact, no browser. No tool installs or updates.

## Task record (raw JSON lines 12077–12109)

- Sites `["gitlab"]`; `require_login: true`; `storage_state: ./.auth/gitlab_state.json`; `start_url: __GITLAB__`; `require_reset: false`; `intent_template_id: 348`.
- Intent (located quote): `"Post \"Thanks, working on reviews\" for the merge request related to octovisuals page in primer/design project"`.
- Eval (located quote): `"eval_types": ["program_html"]` … `"url": "__GITLAB__/primer/design/-/merge_requests/450", "locator": "", "required_contents": {"must_include": ["Thanks, working on reviews"]}`. `reference_answers: null`, `reference_url: ""`.
- Stratum: (`('gitlab',)`, `('program_html',)`) is the lexicographically first stratum. It has 88 tasks and 389 is its minimum ID, so 389 is selection #1 as `selected-task-ids.json` records.

## Intent → evaluator mapping (scorer trace)

| Step | Intent element | Scorer path / operator | Source anchor (`evaluators.py` unless noted) |
|---|---|---|---|
| 1 | Score composition | `evaluator_router` maps `program_html` to `HTMLContentEvaluator()`. `EvaluatorComb` multiplies scores, and there is only one evaluator here. | L369–370 `case "program_html": evaluators.append(HTMLContentEvaluator())`; L348–352 |
| 2 | "merge request related to octovisuals page in primer/design" | The config hard-codes the target as `__GITLAB__/primer/design/-/merge_requests/450`. The URL does not start with `func`, so the `eval()` branch is never reached. Because it is not `"last"`, the scorer runs `page.goto(target_url)` and then a fixed `time.sleep(3)`. | L263–266 (skipped), L271–273 `page.goto(target_url)` / `time.sleep(3)` |
| 3 | "for the merge request" (where to look) | The locator is empty, so the scorer reads the full serialized page DOM. | L276–277 `if not locator.strip(): selected_element = page.content()` |
| 4 | Normalization | `html.unescape` is applied to the whole page. | L302 |
| 5 | "Post \"Thanks, working on reviews\"" | The `must_include` list has one element. It is split on `" \|OR\| "` (here a single alternative), then checked with `StringEvaluator.must_include(tokenize=False)`. That function applies `clean_answer` (strip, strip one pair of outer quotes, `.lower()`) to both strings, then tests `clean_ref in clean_pred`. | L312–327; L98–111; L80–86 `return answer.lower()` |
| 6 | Not used | The trajectory, the final answer (`last_action["answer"]`), the LLM judges (`llm_fuzzy_match`/`llm_ua_match`), helper API functions, and `prep_actions` are never consulted for this task. | L248–333 (no trajectory read); `helper_functions.py` L146, L176 unreachable for 389 |

Net static contract: score = 1.0 if and only if the lowercased, HTML-unescaped full DOM of MR 450, captured about 3 s after navigation, contains the lowercased substring `thanks, working on reviews`. Otherwise score = 0.0.

## Checked vs unchecked properties

**Checked:**
- The phrase is present (case-insensitive substring) somewhere in the MR 450 page DOM after navigation plus 3 s.

**Unchecked (statically):**
- That the phrase is in a newly posted **comment/note**. Matches in the MR title, description, existing notes, sidebar, embedded JSON/data attributes, or textarea default content also count.
- That the text appeared **because of the agent's action**. There is no before/after diff, and `require_reset: false`; all 812 raw tasks have `require_reset: false`, so this flag is not unique to 389.
- The **author** of the note. The logged-in account comes from `storage_state`, but authorship is never compared.
- **Exactness and casing.** Longer text containing the phrase, or different casing, passes because both sides are lowercased.
- **Note count and side effects.** Duplicate posts, edits to the description or title, comments on other MRs, and state changes are not checked.
- That MR **450 actually is "the merge request related to octovisuals page"**. The title-to-ID resolution exists only in the config. A comment on any other MR scores 0 even if a reader could argue it fits "related to".
- The agent's final answer and stop action are unused.

## Dynamic state / judge dependencies

- **Live GitLab instance state:**
  - MR 450 must exist in `primer/design` and render its notes in the DOM within the fixed 3 s window (L273). Notes in GitLab's MR overview are client-rendered [INFERENCE: not provable from this snapshot], so the timing is a false-negative risk.
  - The initial content of MR 450 must not already contain the phrase, or the task passes trivially.
- **Session state:** the evaluator's `page` must be logged in or allowed to view the project (`require_login: true`). If the page is a `PseudoPage`, its attribute access is delegated to the real Playwright page (`helper_functions.py` L211–221).
- **Config materialization:** the `__GITLAB__` placeholder is not substituted anywhere in `evaluators.py`. A generator outside the pinned snapshot must produce the evaluated config file. This is an unresolved gap.
- **No LLM judge dependency** and no helper HTTP API dependency for this task.

## Task-specific potential validity limitation (not a proven defect)

Within its own template, 389 uses a weaker check than its siblings. Template 348 siblings 390, 391, 392 and 393 all use the last-note locator `document.querySelector('[id="notes-list"').lastElementChild.querySelector('.timeline-discussion-body').outerText` with `exact_match`. Task 389 alone uses `locator: ""` (the whole page) with `must_include`.

So 389's scorer is insensitive to *where* the phrase appears and *whether it is new*. If the reset-state MR 450 page already contains "thanks, working on reviews" in any casing (for example in an existing note or the description), a no-op agent would score 1.0. Conversely, slow note rendering past the 3 s sleep could score a correct post 0.0.

Neither outcome is shown statically. Whether the phrase pre-exists in reset-state MR 450 is unknown. The full-page plus `must_include` pattern is common in the stratum: 63 of 117 program_html targets across the 88 gitlab/program_html tasks use an empty locator with `must_include`. The outlier status is specific to template 348.

## Runtime evidence required before calling 389 valid or invalid

None of this was run by this seat; it would need a sanctioned isolated environment.

1. **Baseline absence:** capture `page.content()` of reset-state `/primer/design/-/merge_requests/450`, `html.unescape`, then lowercase, and confirm the phrase is absent. If it is present, the task is trivially satisfiable, which would be a confirmed defect.
2. **Target identity:** confirm the MR 450 title or description concerns the "octovisuals page", and that no other `primer/design` MR equally matches.
3. **Positive control:** post exactly the phrase as an MR 450 comment through the UI, then apply the scorer contract. Expect 1.0, and confirm the note is in the DOM within 3 s.
4. **Negative and specificity controls:**
   - No action: expect 0.
   - Same comment on a different MR: expect 0.
   - Phrase typed but not submitted: expect 0.
   - Phrase only in an edited description, or as a pending unsubmitted review note: these probe the unchecked "is a comment" property. A score of 1 would show over-acceptance, not necessarily invalidity.
5. **Config check:** confirm the generated config replaces `__GITLAB__` with the deployed base URL.

## Compact case row for L1

| task | stratum | intent | evaluator(s) | target | locator | operator | checked | key unchecked | dynamic deps | judge | potential limitation | runtime evidence needed | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 389 | gitlab / program_html (min of 88) | Post "Thanks, working on reviews" on the octovisuals-page MR in primer/design | `HTMLContentEvaluator` (evaluators.py L369–370, L245–333) | `__GITLAB__/primer/design/-/merge_requests/450` (hard-coded) | `""` → `page.content()` (L276–277) | `must_include`, lowercased substring, tokenize=False (L312–327, L80–86, L98–111) | phrase anywhere in MR 450 DOM after goto + 3 s | note-ness, novelty (no diff, reset=false), author, exactness/case, MR identity, side effects, final answer | live GitLab MR 450 state, client render ≤3 s, login session, `__GITLAB__` substitution outside snapshot | none | full-page substring check, weaker than template siblings 390–393 (last-note `exact_match`); possible no-op pass if phrase pre-exists, possible false negative on slow render | baseline-absence DOM capture, MR identity, positive and negative controls, config substitution | statically consistent mapping; validity UNDETERMINED |

## Remaining unknowns

- Reset-state content of MR 450 (decisive for the trivial-pass question).
- MR 450's actual title and whether it matches "octovisuals page".
- Client-side note render latency compared with the 3 s sleep.
- The config generator that substitutes `__GITLAB__`, which is outside the pinned snapshot.

## Verdict

**PASS (scoped):** the static intent-to-scorer mapping for case 389 is complete and anchored to the hash-verified pinned sources. Benchmark task validity is **UNDETERMINED** pending the runtime evidence above. This is not a round-level PASS and makes no claim of an actual task defect.

## Erratum — 2026-10-21 14:40 UTC (from KengakuR28 anchor review; original text above preserved unchanged)

Re-verified with read-only `grep -n` / `sed -n` on the hash-pinned fixtures; no refetch, no broader checks, no production/candidate edits.

1. **Record span.** The full task-389 JSON object spans `test.raw.json` **L12073–12109** (`{` at L12073, `sites` L12074–12076, `"task_id": 389` L12077, closing `}` L12109). "Task record (raw JSON lines 12077–12109)" above should read 12073–12109.
2. **`html.unescape` anchor** is `evaluators.py` **L303**, not L302 (mapping step 4).
3. **`HTMLContentEvaluator` class span** is **L244–333** (`class` L244, final `return score` L333), not L245–333 (case-row evaluator cell).
4. **Sibling-locator qualification.** The siblings' locator (e.g. `test.raw.json` L12136, L12171) is `document.querySelector('[id="notes-list"')…`: the attribute selector is **unclosed** (no `]`). Whether it resolves depends on the browser's CSS parser recovery, which is not established from this snapshot. So "389 uses a weaker check than its siblings" holds only **if** that selector actually resolves to the last note in the runtime browser. It is not established universally. If it throws, L292–294 sets `selected_element = ""` and the siblings would score 0.
5. **Exception paths are not always 0.** Only the JS-locator `page.evaluate` failure is caught, giving `""` (L292–294). For 389, a `page.goto` failure (L272) or a malformed `required_contents` would **raise**, not return 0.0. How a raised exception is scored is outside the pinned files. The "otherwise score = 0.0" in the net static contract is restricted to non-exceptional runs.
6. **Imported helper dependencies exist.** `evaluators.py` L18–27 imports from `helper_functions`, which at module level imports `requests`, `browser_env.env_config` (ACCOUNTS, GITLAB, …) and `llms.providers.openai_utils` (`helper_functions.py` L6–20). These are load-time dependencies even though no helper is reached in scoring for 389. "No LLM judge / helper API dependency" means unreached in scoring, not absent from the import graph.

Unaffected: the intent → operator/target mapping, the checked/unchecked lists, the stratum and selection figures (88 tasks, minimum ID 389; 63 of 117 targets), the runtime-evidence list, and the scoped verdict (static mapping PASS; validity UNDETERMINED). The sibling-comparison limitation is now explicitly conditional, per item 4.

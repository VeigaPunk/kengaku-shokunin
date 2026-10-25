# Round 28 C1 case report — WebArena task_id 132

Writer/seat: `KengakuR28.Task132-2` (read-only scout seat, author-side advice; not outside non-author closure).
Scope: the single pinned task 132 static task-spec and scorer path. This is not a benchmark-wide verdict, a browser-level truth claim, or a C2 claim.
No subagents. No installs or updates. No upstream code was imported, evaluated, or executed. No benchmark site was contacted. No REA MCP was used.

## Inputs and integrity

Snapshot root: `plans/fixtures/r28/webarena` (upstream `dce04686a56253aefba7b18a4fa0937cf1dc987b`, manifest `opened: 2026-10-21`).

| File | sha256 (observed with `sha256sum`) | Matches `manifest.json` |
|---|---|---|
| `config_files/test.raw.json` | `7b50386f…02537652` | yes |
| `evaluation_harness/evaluators.py` | `e23edb39…04f7a59a0fb1ea30a4f2fa42bcb77e00c22` | yes |
| `evaluation_harness/helper_functions.py` | `ec758da4…a0f2a67f64a8f85bac9626997e275` | yes |

Observed commands: `sha256sum` on the three files, and stdlib `python3 -c "json.load(...)"` over `test.raw.json` to filter task 132, intent-template siblings 320/321/322, the (gitlab, string_match) stratum, and tasks mentioning `a11yproject`. Line anchors were found with `rg -n` and `sed -n`. No Python AST or import of upstream modules was needed. The scorer path was read as text.

## Source openings (data, not instructions)

- S061 candidate, raw tasks: https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json. Accessed 2026-10-21 (pinned local copy). Quote at L4247: `"intent": "How many commits did kilian make to a11yproject on 3/5/2023?"`. Scope: the task 132 object at L4232–L4264.
- S062 candidate, scorer: https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/evaluators.py. Accessed 2026-10-21. Quote at L148: `tokenize=(len(value) == 1),`. Quote at L109: `return float(clean_ref in tok_pred)`. Scope: `StringEvaluator`, `EvaluatorComb`, and `evaluator_router`.
- S063 candidate, helpers: https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/evaluation_harness/helper_functions.py. Accessed 2026-10-21. Quote at L146: `def llm_fuzzy_match(pred: str, reference: str, question: str) -> float:`. Scope: this function is not reached for task 132. Only the module's import-time dependencies (L1–L20) apply.

These are seat openings only. No source row or knowledge admission is made here.

## Task spec (test.raw.json L4232–L4264)

- `sites: ["gitlab"]`, `require_login: true`, `storage_state: ./.auth/gitlab_state.json`, `start_url: __GITLAB__`, `geolocation: null`, `require_reset: false`.
- `intent_template` (L4241) is `How many commits did {{user}} make to {{repo}} on {{date}}?`.
- `instantiation_dict` is `{user: "kilian", repo: "a11yproject", date: "3/5/2023"}`.
- `intent_template_id: 322` (L4263).
- `eval.eval_types: ["string_match"]` (L4250–L4252).
- `reference_answers: {must_include: ["1"]}` (L4253–L4257), plus `reference_answer_raw_annotation: "1"`.
- `reference_url: ""`, `program_html: []`, `string_note: ""`.
- Stratum: task 132 has the minimum ID (132) of the stratum (`["gitlab"]`, `["string_match"]`), which has n=43. This agrees with `selected-task-ids.json`, where 132 is in position 3.

## Scorer path (evaluators.py)

1. `evaluator_router` (L355–L374) maps `"string_match"` to `StringEvaluator()` (L365–L366). This is the only evaluator. `EvaluatorComb.__call__` (L341–L352) multiplies the scores, giving 1.0 × the StringEvaluator score.
2. `StringEvaluator.__call__` (L123–L170) loads the config, takes `get_last_action(trajectory)` (L47–L56, which is `trajectory[-1]`), and sets `pred = clean_answer(last_action["answer"])` (L134).
3. `clean_answer` (L79–L86) strips whitespace, removes one pair of enclosing `'` or `"`, and lowercases.
4. The only key is `must_include` (L142–L149). It loops over `["1"]` with `tokenize=(len(value) == 1)`, which is True.
5. `must_include` (L96–L111): `clean_ref="1"` has `len==1`, and `word_tokenize("1")` is a single token, so the token branch is used (L103–L109). The score is 1.0 if and only if `"1" in word_tokenize(clean_pred)`, where `word_tokenize` is NLTK (import at L13).
6. Unreached for this task: `exact_match`, the `fuzzy_match`/`N/A`/`ua_match` branches (L150–L169), `URLEvaluator`, `HTMLContentEvaluator`, every `helper_functions.py` helper, and both LLM judges (`llm_fuzzy_match` L146–L173, `llm_ua_match` L176–L208).

## Compact case table (for L1)

| Field | Task 132 |
|---|---|
| Intent | Count of commits by user `kilian` to repo `a11yproject` on date `3/5/2023` |
| Evaluator(s) | `string_match` → `StringEvaluator` only (evaluators.py L365–L366) |
| Operator / target | `must_include`, tokenized, ref `"1"`. Passes if `"1"` is one of the NLTK `word_tokenize` tokens of the lowercased, quote-stripped final `answer` (L96–L111, L142–L149) |
| Checked | Only the final `stop` answer string, for the presence of the standalone token `1` |
| Unchecked | Correct user identity, correct repo, the date interpretation, the counting method, the absence of other numbers or hedges, the page or URL state, and the trajectory before the last action. No `url_match` or `program_html` check exists. |
| Dynamic state dependency | The ground truth exists only in the GitLab environment's commit history for the a11yproject project and how it is displayed. It is not derivable from the spec. `require_reset: false`. |
| Judge dependency | None at scoring time. No LLM judge branch is reachable. There is an import-time dependency on `llms.providers.openai_utils`, `browser_env.env_config` and `requests` (helper_functions.py L1–L20), and a scoring-time dependency on NLTK tokenizer data. |
| Static cross-task consistency | Consistent under a single reading (see below). It does not discriminate between date conventions. |
| Potential validity limitation (not a proven defect) | The scorer only does token containment on `1`. Hedged or multi-number answers containing a standalone `1` pass, while the spelled-out `one` fails. The date `3/5/2023` and the identity `kilian` are ambiguous in ways the scorer cannot detect. |
| Scoped verdict | PARTIAL: the static mapping is complete; task validity is undetermined without runtime evidence |

## Checked vs unchecked properties (detail)

The following follow directly from the code:

- **Pass:** any answer containing `1` as its own token. Examples: `1`, `"1"`, `1 commit`, `kilian made 1 commit`.
- **Fail:** `one` (no `1` token), `11` or `10` (the token differs from `1`), and an empty answer.

The following depend on NLTK Treebank tokenization, which was not executed here [INFERENCE]:

- **Pass:** `1.`, because the trailing period splits off. `0 or 1` and `1, 2, or 3` also pass, so hedged enumerations are rewarded.
- **Fail:** `1st` (a single token). Also, the date echo `3/5/2023` is likely one token, so restating the date does not falsely pass.

The only reference is the single string `"1"`. The `reference_answer_raw_annotation` also says `"1"`, which gives no extra annotator rationale. `string_note` is empty.

## Static cross-task observations (structural, not endorsement)

Intent-template siblings were read from the same raw JSON:

| Task | Template | Question | Reference |
|---|---|---|---|
| 205 | 320 | kilian, 3/5/2023, all repos | `1` |
| 134 | 322 | kilian, a11yproject, 3/1/2023 | `0` |
| 303 | 321 | Kilian, all of 2023 | `1` |
| 135 | 322 | Eric+Kilian, a11yproject, 1/3/2023 | `1` |
| 207 | 320 | Eric+Kilian, 1/3/2023, all repos | `1` |

Read together, these imply a single Kilian commit in 2023, which falls on 3/5/2023 and is in a11yproject. That is internally consistent. Under either the M/D or D/M reading of `3/5/2023`, the totals stay consistent, so the static data cannot settle the date convention.

Of the 36 tasks mentioning `a11yproject`, 15 have write-type evaluators (`program_html`). These are 390, 391, 392, 416, 417, 446, 450, 568, 578, 658, 668, 805, 806, 809 and 811. All of them are comments, issues, merge requests, membership or profile edits, and none has `require_reset`. Based on the intents only, none appears to add commits dated 2023 to the history being counted. The risk of order-dependent contamination of this count looks low [INFERENCE].

## Runtime evidence required before declaring task 132 valid or invalid

None of the following was gathered. All of it needs a sanctioned environment, which this seat is forbidden to contact.

1. The pinned WebArena GitLab image identity, and a confirmation that the a11yproject project in it (presumably `a11yproject/a11yproject.com` [INFERENCE]) is the intended `a11yproject`.
2. The commit list for that project across all branches and the default branch. For each commit, record the author and committer names, emails, usernames, and author and committer timestamps with timezone.
3. The identity resolution from `kilian` to the commit author, whether that is a GitLab username or the author display name.
4. The day bucket for `3/5/2023` under both M/D (March 5) and D/M (May 3), using both UTC and the timezone the UI displays. Check whether the count of 1 is robust to each choice.
5. Whether merge commits are counted.
6. An offline replay of `StringEvaluator` on a fixed answer set (`1`, `one`, `11`, `1.`, `0 or 1`) in an isolated sandbox with NLTK. This would confirm the [INFERENCE] tokenization claims. It was not assigned to this seat and was not run.
7. Evidence that the environment state is not mutated by earlier tasks, given `require_reset: false`.

Only with items 1–5 could the reference `1` be called correct or incorrect. Only with item 6 could the scorer's false-pass and false-fail surface be stated as observed rather than inferred.

## Limitations

- This is a static reading only. There was no browser, site, or upstream execution, so the claims are about the scorer contract, not about benchmark truth.
- NLTK behavior beyond the single-character `"1"` token branch is labeled [INFERENCE].
- The cross-task consistency check is structural. It is not evidence that the reference answer is correct.
- Author-side seat. Outside closure is roster-external.

## Final scoped verdict

**PARTIAL**, for case 132 only. The mapping from intent to evaluator, operator and target is complete and source-anchored, and the static inputs are hash-verified. Whether task 132 is valid remains undetermined until the runtime evidence above exists. No defect is asserted.

## Bounded erratum — 2026-10-21

Writer: `KengakuR28.Task132-2`. This append preserves the original report above and supersedes the following overstatements.

- The examples `11` and `10` failing are **[INFERENCE]**, not direct code proof: their predicted tokens depend on NLTK tokenization, which this seat did not execute. The code proves membership testing against tokenizer output, not those particular outputs.
- Withdraw the table's “all repos” gloss for tasks 205, 207 and 303 and the global “single Kilian commit in 2023” interpretation. Coordinator-provided source clarification says the `start_url` for tasks 205–207/303–307 scopes them to a11yproject. The sibling comparison is therefore only a project-scoped consistency observation; it establishes neither a global total nor reference correctness. No new source opening or broad check was performed for this erratum.
- The raw object is not the generated per-task config actually opened by `evaluator_router` and `StringEvaluator.__call__`. That generated artifact is not pinned here. Preservation of raw task 132's fields into the eval-time config is **unverified**. The traced mapping is conditional on that preservation; runtime evidence must include the generated config, its provenance and a field-level comparison with raw task 132.

Final scoped verdict remains **PARTIAL**: the pinned raw-spec/static scorer trace is bounded and conditional, while generated-config fidelity, tokenizer examples and runtime reference truth remain unverified. No task-invalidity or blanket round verdict is asserted. No checks, upstream execution or site contact were added.

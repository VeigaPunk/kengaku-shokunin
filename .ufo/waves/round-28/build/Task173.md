# Round 28 C1 case audit — WebArena task_id 173

Writer/seat: `KengakuR28.Task173-2` (scout, read-only, author-side). Date 2026-10-21.
Scope: one static task-spec/scorer audit of pinned upstream `dce04686a56253aefba7b18a4fa0937cf1dc987b`. No upstream code imported/executed, no benchmark site contacted, no browser action. This is author-side advice, not outside closure, and not a task-validity verdict.

## Inputs (hash-verified against `plans/fixtures/r28/webarena/manifest.json`)

| File (lane-relative under `plans/fixtures/r28/webarena/`) | sha256 (observed `sha256sum`) | Manifest URL |
|---|---|---|
| `config_files/test.raw.json` | `7b50386f…0537652` (match) | https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json |
| `evaluation_harness/evaluators.py` | `e23edb39…e00c22` (match) | …/dce04686…/evaluation_harness/evaluators.py |
| `evaluation_harness/helper_functions.py` | `ec758da4…77e275` (match) | …/dce04686…/evaluation_harness/helper_functions.py |

Opened from the local pinned snapshot (access 2026-10-21); upstream URLs not re-fetched by this seat.

## Task 173 spec (`test.raw.json` lines 5520–5550)

- sites `["gitlab"]`, `require_login: true`, `storage_state: "./.auth/gitlab_state.json"`, `start_url: "__GITLAB__"`, `require_reset: false`, `intent_template_id: 310`, `instantiation_dict: {"keyword": "better"}`.
- intent (L5533, quote): "Open my latest updated issue that has keyword \"better\" in its title to check if it is closed".
- eval (L5536–5548): `eval_types ["string_match","url_match"]`; `reference_answers {"fuzzy_match": ["No, it is open"]}` (L5541); `reference_url "__GITLAB__/byteblaze/empathy-prompts/-/issues/8"` (L5543); `program_html []`; `reference_answer_raw_annotation "Not closed"`; `string_note ""`; `url_note "GOLD in PRED"`.

## Case table (intent → evaluator operator/target)

| # | Intent component | Evaluator / operator (anchor) | Target | Checked? |
|---|---|---|---|---|
| R | Route both types | `evaluator_router` match on `eval_types` (evaluators.py L361–372) → `StringEvaluator`, `URLEvaluator`; `EvaluatorComb` multiplies scores (L348–352) | both must be 1.0 | combination: product, order string→URL |
| S1 | "check if it is closed" (answer) | `StringEvaluator.__call__`: `pred = self.clean_answer(last_action["answer"])` (L134) — strip, strip one pair of outer quotes, `lower()` (L80–86) | final stop-action answer text | yes, final answer only |
| S2 | same | `case "fuzzy_match"` (L150); value is a list, not `"N/A"`, so loop `fuzzy_match(ref, pred, intent)` per reference (L165–169) | ref `"No, it is open"`; question = task `intent` | yes, via LLM judge |
| S3 | same | `llm_fuzzy_match` (helper_functions.py L146–173): prompt "evaluate whether the answer is semantically equivalent to the reference answer"; `model="gpt-4-1106-preview"` (L162), `temperature=0`; returns 0.0 if response contains `"partially correct"` or `"incorrect"`, else `assert "correct" in response` → 1.0 (L169–173) | judge text | yes, judge-dependent |
| U1 | "Open … issue" (final page) | `URLEvaluator`: `pred = clean_url(page.url)` = `rstrip("/")` (L187–190, L212); ref split on `" |OR| "` (L213) → single ref | final `page.url` at evaluation time | yes, final page only |
| U2 | identity of the issue | `url_note` "GOLD in PRED" (L215–216); base = `netloc + path` (L192–197); `pred_base_paths, pred_query = parse_url(pred)` (L218) binds a **str**, so `ref_base_path in pred_base_paths` (L223) is a **substring** test | `<GITLAB netloc>/byteblaze/empathy-prompts/-/issues/8` | yes, as substring of netloc+path |
| U3 | — | query loop over `ref_queries` (L229–235); ref has no query → `query_score = 1.0` | none | query/fragment/scheme not checked |

## Checked vs unchecked

Checked: (a) the LLM judge labels the lowercased final answer semantically equivalent to "No, it is open" for the intent; (b) the final page's `netloc+path` contains the reference `netloc+path` as a substring.

Unchecked: that issue 8 is (still) "my" latest-updated issue with "better" in its title; the issue's live open/closed state at evaluation; which issue the agent actually opened during the trajectory (only the final URL); scheme, query and fragment; whether the agent mutated GitLab state; how "my" is interpreted (authored vs assigned) and how "keyword in title" is matched (case/substring).

## Dynamic state and judge dependencies

- State: the gold answer and gold URL are fixed constants describing a GitLab snapshot. "Latest updated" depends on issue `updated_at` ordering, and `require_reset` is `false`. In the same file, task 659 (L22398–22430, `require_reset: false`) creates an issue in the same project with the title "Integrating LLMs for better prompts" (L22406), which contains the keyword `better`. If 659 runs before 173 in a shared, unreset instance, the newest matching issue would plausibly be the new one rather than issue 8. Whether that new issue counts as "my" issue is an [INFERENCE]: it depends on the author/assignee semantics, and 659 assigns it to Roshanjossey. Tasks 175 and 180 also touch empathy-prompts, but they are read-only. Task 393 comments on a merge request, not an issue.
- Judge: the score depends on availability and behavior of the external OpenAI model `gpt-4-1106-preview` (helper_functions.py L161–168). A temperature of 0 does not make the judge deterministic. The response parser treats any occurrence of "incorrect" as 0.0, and it raises an `AssertionError` (not a 0 score) when the response lacks "correct" (L169–173).
- Placeholder: `__GITLAB__` is substituted outside the pinned files ([INFERENCE]; the generator is not in the snapshot). If the evaluator were given the raw value unsubstituted, `urlparse` would give `netloc=''` and `path='__GITLAB__/byteblaze/…'`, which would never be a substring of a real URL (scratch evidence below).

## Task-specific potential validity limitation (not a proven defect)

The "GOLD in PRED" substring test means any final URL whose `netloc+path` contains `…/empathy-prompts/-/issues/8` passes. That includes `/issues/80`–`/issues/89`, `/issues/8xx`, and sub-pages such as `/issues/8/…`. A wrong issue in the 80s or 800s would pass the URL check if it exists. Because task 659 can, without a reset, add a newer matching issue to the same project, the fixed gold `issues/8` and "No, it is open" can go stale. The substring rule can also pass, or fail, a correct agent depending on the new issue's number. Neither effect is shown to occur; both depend on runtime state.

## Runtime evidence required before any valid/invalid declaration

1. Reset-state GitLab export of `byteblaze/empathy-prompts`: issue numbers present (are any of 80–89 or 800+ present?), and for every issue whose title contains `better` (case-insensitive), its author, assignees, `updated_at` and state.
2. Instance-wide evidence of which issues "my" covers for the `gitlab_state.json` account (authored vs assigned dashboard), confirming issue 8 is the latest-updated match and is open.
3. Harness execution order and reset policy between 659 and 173 in the evaluated run (the `require_reset: false` flags alone do not decide this).
4. The substituted per-task config actually fed to the evaluator (placeholder resolution), plus the judge model's availability, version and logged responses for the scored runs.

## Observed commands (this seat)

- `python3 -c` JSON reads of `test.raw.json` (task 173, template 310 siblings 173–177, `empathy-prompts` and `better` cross-task scans), `sha256sum` of the pinned files, `grep -n` for line anchors.
- Stdlib-only language-semantics check (hand-written `urllib.parse` and `str in str` expressions plus a re-statement of the judge string rule, with hypothetical host `gitlab.invalid`, no network, no upstream import). Output: `.ufo/waves/round-28/scratch/Task173/stdlib-semantics.txt` (sha256 `d4fb776b8a3ead50510e0db88b28d51fe4418fc2f0ec7d488c3353065115633c`). It shows `…/issues/80` → contains=True, `…/issues/8/edit` → True, `…/issues/7` → False, and "not incorrect; correct" → 0.0. This is a re-derivation of semantics, not execution of `URLEvaluator`.
- Context only: sibling 178 ("latest created issue that has better") has a different gold, `a11yproject/a11yproject.com/-/issues/566`. That is consistent with "created" and "updated" differing; no inference drawn.
- No tools installed or updated. No REA MCP, no delegation.

## Limitations

Static evidence only, with no browser-level truth. The GitLab dataset state, the account identity behind `gitlab_state.json`, and the config-generation step are all unobserved. This is a bounded, nonrepresentative single case, and the sample was not randomly drawn.

## Verdict

PASS for the scoped deliverable, a static case-173 intent→operator/target audit with anchors. Task 173's validity is NOT adjudicated; it is UNDETERMINED pending runtime evidence items 1–4.

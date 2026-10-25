# FTask552 — falsification of BUILD case552 (WebArena task 552)

Seat: `KengakuR28.FTask552` (leaf, read-only, author-side). Date: 2026-10-21.
Scope: static case552 and its 552-specific candidate language only. No upstream code imported, executed
or evaled; no benchmark site contacted; no browser action; no scorer run; no production edit; no
delegation; no install.

Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

## Reviewed bytes (observed)

| artifact | path | sha256 |
|---|---|---|
| build case | `.ufo/waves/round-28/build/Task552.md` | `2c90d24c3eefbfd1fd49371627a1a7a2731c07b8a094f394c8b5a2ea0437a8c6` |
| frozen candidate draft | `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md` | `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` |
| raw tasks | `plans/fixtures/r28/webarena/config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` |
| scorer | `plans/fixtures/r28/webarena/evaluation_harness/evaluators.py` | `e23edb390c4e39b3fff97dfd456fb04f7a59a0fb1ea30a4f2fa42bcb77e00c22` |
| helpers | `plans/fixtures/r28/webarena/evaluation_harness/helper_functions.py` | `ec758da4f82e5659e95805ab23222cfd7c4a0f2a67f64a8f85bac9626997e275` |
| manifest | `plans/fixtures/r28/webarena/manifest.json` | `c78b1478c5cb18dd7621723023e7ff15342401c72fc04a939a8d4d290323a6dd` |

The candidate hash equals the context-declared `77e19d5b…20a8`; the three source hashes equal the
manifest entries (lines 7, 12, 17), and the manifest revision is
`dce04686a56253aefba7b18a4fa0937cf1dc987b`.

Independent provenance control: `curl -fsSL` of the three pinned raw URLs at revision
`dce04686a56253aefba7b18a4fa0937cf1dc987b` (raw.githubusercontent.com, 2026-10-21, read-only) produced
exactly the three hashes above, so the local fixture bytes are the pinned upstream bytes. No benchmark
host was contacted; upstream source was read as untrusted data.

Canonical target `corpus/knowledge/webarena-task-spec-audit.md` is **not admitted**; this is a review
of the frozen draft and `build/Task552.md`, not an admission and not a runtime task-validity claim.

## Method

`sha256sum`; `nl -ba | sed -n` and `grep -n` over the pinned files; stdlib `json.load` of the raw task
file for an independent task/template census. No production or alternate oracle was imported before
deriving; no upstream module was executed. Scratch receipt:
`.ufo/waves/round-28/scratch/FTask552/template84-receipt.json`.

## Case552 claims that reproduce against the pinned bytes

Raw task 552 occupies `test.raw.json:17868–17909` (task id at 17873). Every field in the case table
reproduces: `sites` 17869–17872; login/storage 17874–17875; `start_url` 17876; `intent` 17884;
`require_reset:false` 17885; `eval_types:["program_html"]` 17887–17889; `reference_answers:null`
17890; `reference_url:""` 17891; target URL 17894; empty locator 17895; five `must_include` literals
17898–17902; `intent_template_id:84` 17908.

All evaluator anchors reproduce:

| case claim | pinned source (observed) | verdict |
|---|---|---|
| `HTMLContentEvaluator` at 244–333; router 356–374, program_html case 369–370 | `evaluators.py` 244, 356, 369–370 | exact |
| `EvaluatorComb` multiplies (336–352) | 348–352 | exact |
| navigate then `time.sleep(3)` (271–273) | 271–273 | exact |
| empty locator → `page.content()` (276–277) | 276–277 | exact |
| `html.unescape` (303) | 303 | exact |
| `" \|OR\| "` split 316; `must_include(..., tokenize=False)` 318–323; product 327 | 315–327 | exact |
| `clean_answer` strip/quote/lower (80–86); substring (98–111) | 80–86, 98–111 | exact |
| no helper reference; URL/locator not `func:` (263–266, 296–299) | 263, 296–299 | exact |
| `reddit_get_post_url` (helper 97–112) unused here | helper 97–112; import only at evaluators.py:23 | exact |
| quote at evaluators.py:245 | line 245 | exact |

The checked/unchecked classification also reproduces. The scorer has one `program_html` target, an
empty locator, five literal references and no `func:`/`prep_actions`. Each reference must appear as a
lowercased substring of `page.content()`; score is the product over the five booleans. Extra URLs,
order, file format, a separate directory object, commit metadata, trajectory provenance, non-target
repository harm and live Reddit recency are not checked. The `program_html` method never reads
`trajectory`. `require_reset:false` plus end-state-only reading makes stale-artifact credit possible
(the case marks reset practice [INFERENCE]). `reference_answers:null` and `reference_url:""` are
unused because only `program_html` is routed.

The case's cross-task claims reproduce; the one false claim is the separate sibling sentence (F1).
The four other `urls.txt` writers are at
17926, 17968, 18010, 28797 (tasks 553, 554, 555, 791); 26194 edits the LICENSE; 18518 and 10854
concern membership; `real_space` occurs only in 552's own records (17880, 17884, 17894). The only
other `space`-forum tasks are 30 (read/count, intent 971) and 595 (subscribe, intent 19870); neither
creates a `/f/space` post. This stays literal-grep evidence, as the case says.

## F1 — hard falsification: the template-family "siblings" sentence is false

`build/Task552.md:26` states: “Siblings are tasks 553–556 and the one at line 28811.”

Independent extraction from the pinned raw file (receipt above) gives exactly five tasks with
`intent_template_id == 84`:

```
552 (line 17908), 553 (17950), 554 (17992), 555 (18034), 791 (28811)
```

The five occurrences of `"intent_template_id": 84` are at lines 17908/17950/17992/18034/28811;
nearest-preceding `task_id` mapping yields 552/553/554/555/791. Task 556 is **not** in this family:
its `intent_template_id` is **87** at `test.raw.json:18082`, and its `sites` are
`["gitlab","wikipedia"]` (task 556 occupies 18036–18083), i.e. the separate
`(gitlab,wikipedia) × (program_html)` stratum whose minimum ID 556 is also selected. The task at line 28811 is 791 (`task_id` at 28786, intent at 28797),
the fourth different-folder writer already cited by the case at 28797.

Two same-wave reports independently contradict the sentence:
`build/Task791.md:101` — “siblings 552–555 are achievable and use `program_html`”; and
`build/Task556.md:20` — “`task_id` 556, `intent_template_id` 87, `sites` `["gitlab","wikipedia"]`”.

Impact: the 552 intent→predicate mapping, checked/unchecked sets, dependency list and verdict do not
depend on sibling membership, so the scorer analysis itself stands. But this is a false source-line /
task-ID claim inside the very table that establishes the task record, and it contradicts the case's
own cross-task line citation (28797 = 791). For L1's resolution, the correct sentence is:
“Siblings are tasks 553–555 and task 791 at line 28811.” The error conflates file-adjacent task IDs
(553–556) with template-84 membership; 556 is template 87 and is selected in a different stratum.

This is the decisive falsifier for this seat: a byte-reproducible extraction plus cross-report
agreement separates template membership from file adjacency. It is not a runtime-invalid-task claim.

## F2 — soft finding: one unmarked runtime inference

The case's GitLab-state bullet says the raw endpoint must be readable from “the evaluator's page,
which is the agent's own `page` and inherits the `storage_state` session.” The pinned files show only
that `HTMLContentEvaluator.__call__` receives a `page` parameter (`evaluators.py:248–253`) and that
`evaluator_router` returns an `EvaluatorComb` (356–374); the runner that supplies the page, loads the
storage state and reuses the agent's context is outside the snapshot. The case's own [INFERENCE]
list (Task552.md:99) covers Chromium rendering, Postmill routing and reset practice but not this
page/session inheritance. This is a missing hedge, not a proven-false statement; the case separately
lists endpoint reachability with the stored session as required runtime evidence.

## Candidate 552-specific language check

The frozen candidate's only 552-specific characterizations are the selected-ID list at draft line 60
(552 present) and the case-table row at line 71: `44,552,681,791` → “URL-only navigation, fixed link
set, cross-site literals, N/A exact/fallback branch”. Positionally, 552 is “fixed link set”; the raw
record's five fixed `must_include` literals support that label, and the case report itself records
that supersets and substring context also pass. Adjacent reports confirm the other labels (44 URL-only
`url_match`; 681 cross-site literals; 791 N/A fuzzy branch). No 552-specific candidate language was
found to exceed the pinned source.

Independent recomputation of the candidate's population counters from the raw JSON matches the draft:
812 tasks / 812 distinct IDs 0–811; 5 evaluator-type sets; 27 strata; the exact frozen16
`[389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399]`; 651 `program_html` targets;
effective operators exact_match 188 + must_include 463; locator classes full-page 105 / JavaScript
524 / helper 22; target-URL classes last 238 / navigation 338 / helper 75; string operators
exact_match 45 / must_include 176 / fuzzy_match 118. The candidate's “shopping site omitted” is
accurate for `shopping` (192 tasks); `shopping_admin` does appear in the sample (task 759, group 12),
as expected. The instrument's `--selftest` count of 21 was not rerun here (instrument-level claim,
outside this seat's static 552 scope); no contradiction was found in the counters this seat derived.

## Decisive controls

1. **Upstream-byte control (positive):** three pinned raw URLs re-fetched at `dce04686…` hash to the
   fixture/manifest values, so the case's provenance premise is byte-true.
2. **Predicate control (positive):** raw target/refs 17894–17903 against evaluator 271–277, 303,
   312–327 reproduce the case's five-lowercased-substring product, including tokenize=False and the
   empty-locator full-page selection.
3. **Family control (falsifier):** template-84 extraction yields 552/553/554/555/791; 556 is template
   87 and 791 is the line-28811 sibling. Task552.md:26 is false as a template-family claim.
4. **Candidate-language control (positive):** “fixed link set” is supported; no 552-specific
   overreach in the frozen draft.

## Remaining unknowns (runtime, not observed)

Generated per-task config after `__GITLAB__`/`__REDDIT__` substitution; GitLab repo/branch/auth and
raw-endpoint reachability from the evaluator page; Reddit `/f/space` snapshot ordering/top-5 and slug
stability; reset/run-order practice; actual `page.content()` values and scores. The case already lists
these as required evidence and leaves task validity UNRESOLVED; none is converted to a confirmed
success/failure here.

## Verdict

**VERDICT: PARTIAL** — case552 static intent→scorer mapping, anchors, checked/unchecked properties and
cross-task greps largely reproduce, but the task-record's sibling set is false (556 is template 87;
the line-28811 sibling is 791), and one page/session-inheritance statement is an unmarked inference.

The scorer analysis itself is supported: task 552's five fixed references are checked as lowercased
substrings of the raw `main/real_space/urls.txt` page, with no folder/order/count/trajectory check.
This is not a runtime task-invalidity finding, not an admission, and not a whole-candidate approval.
Canonical candidate `corpus/knowledge/webarena-task-spec-audit.md` remains unadmitted; the frozen
draft's 552-specific language does not exceed source. No production file was edited.

Confidence: high on F1 (byte-level extraction and cross-report agreement); high on the static mapping;
runtime state remains unobserved.

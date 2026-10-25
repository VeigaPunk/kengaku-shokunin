# CritClaimScope — round 28 C1 scope critique

Writer/seat: `KengakuR28.CritClaimScope-2` (critic, read-only, author-side advice; not outside closure, not a judgment).
Scope: C1 only — the claim wording and identity for "pinned original WebArena". C2 was not examined. No broad audit.
Inputs read: `plans/round-28-claims.md` (prereg), `plans/fixtures/r28/webarena/{manifest.json,selected-task-ids.json,config_files/test.raw.json,evaluation_harness/evaluators.py,evaluation_harness/helper_functions.py}`, and `corpus/knowledge/benchmark-selection.md` plus `SKILL.md` (the only other lane files that mention WebArena; both only mention WebArena-Verified).
Scratch evidence: `.ufo/waves/round-28/scratch/CritClaimScope/` (`release.test.raw.json`, `release.helper_functions.py`, `diff-summary.txt`).

## Strongest falsifiable objection

The prereg's C1 says "offline task-spec audit of the **pinned original WebArena benchmark**" (prereg line 7). The wave goal paraphrases it as "pinned original WebArena static task-spec/scoring audit". Neither gives a date. That wording is correct in one sense: this is the original `web-arena-x/webarena` line, not WebArena-Verified. It is **false if "original" is read as the released benchmark** — the 2023-07-25 release behind arXiv 2307.13854 v1 and the paper-era scores.

The pinned snapshot is a revised state of the benchmark from more than two years after release:

- **Revision date.** Pin `dce04686` was committed 2025-11-26. The last changes reachable from it are: `test.raw.json` on 2024-03-14, `evaluators.py` on 2025-09-02, and `helper_functions.py` on 2023-12-22.
- **Task-file history.** After the release commit, `config_files/test.raw.json` changed in **19 commits** reachable from the pin (from 2023-09-11 to 2024-03-14).
- **Substantive task changes.** Comparing the release `test.raw.json` (`b454f2dc`, sha256 `4ea85923…50f3`) with the pinned one (sha256 `7b50386f…7652`): all 812 task IDs are the same. But **531/812 tasks have a different `eval` block**, and **480/812 changed substantively**, meaning in `eval_types`, `reference_answers`, `reference_url` or `program_html`. Per-field task counts are: `program_html` 412, `url_note` 72, `reference_answers` 56, `reference_url` 39, `intent` 12, `string_note` 6, `reference_answer_raw_annotation` 4, `eval_types` 3.
- **Shift toward an LLM judge.** String operators changed from `exact_match` 87 / `fuzzy_match` 77 / `must_include` 172 (release) to 45 / 118 / 176 (pin). 37 tasks moved from `exact_match` to LLM `fuzzy_match`. The pin has 36 `fuzzy_match: "N/A"` tasks for unachievable tasks; the release had 0.
- **Judge model changed.** The fuzzy judge went from `gpt-3.5-turbo` (release `helper_functions.py` L170) to `gpt-4-1106-preview` (pin L162 and L197).
- **Sample exposure.** **12/16 sampled tasks** have substantive eval changes: 389, 590, 173, 552, 681, 791, 556, 356, 377, 759, 424, 399. Task 44 has a non-substantive change. Only tasks 132, 7 and 97 are identical. Two concrete counterexamples:
  - Task 173: release `{"exact_match": "No"}`; pin `{"fuzzy_match": ["No, it is open"]}`, with `url_note: "GOLD in PRED"` added.
  - Task 791: release `{"exact_match": "N/A"}`; pin `{"fuzzy_match": "N/A"}`, now scored by the LLM.

So a reader who carries "original WebArena" to the released benchmark, or to any paper-era or leaderboard score, will get the wrong case reports for 12/16 tasks and the wrong operator and evaluator-type aggregates. Evaluator-type set sizes also differ between release and pin: `string_match` 322 vs 325, `url_match` 68 vs 66, `program_html` 283 vs 282. Historical scores can't be transferred to these specs.

## What survives (counterevidence I tested)

- The counts in F1–F3 do not depend on the revision. Both versions have 812 tasks, 5 evaluator-type sets and 27 strata. The frozen rule selects **the same 16 IDs** in both (`[389, 590, 132, 173, 44, 552, 681, 791, 556, 356, 7, 377, 759, 424, 97, 399]`).
- The four pinned file hashes I recomputed match `manifest.json` exactly.
- The prereg already disclaims new method, new model ability, actual task invalidity, contamination freedom and WebArena-Verified (prereg line 7). It also limits scorer tracing to "static evidence, not browser-level truth" (line 17). Inventory ≠ task validity ≠ model accuracy ≠ contamination audit is therefore stated explicitly. I found no wording that merges those four.
- The objection does **not** support repricing, and score 7 stays held. It is a fixable defect in naming and dating the construct. It is not a tradeoff the Rust judge must reject.

## Secondary limitations (disclose, not defects)

1. **LLM-judged scoring.** 118 pinned tasks, including sampled tasks 173 and 791, are scored by a remote `gpt-4-1106-preview` judgment (`llm_fuzzy_match` / `llm_ua_match`). "16 deterministic task-case audits" can only describe the audit's selection and procedure. Static tracing of those scorer contracts stops at an external model call, so the audit cannot settle those tasks' scoring outcomes.
2. **Shopping is unsampled.** The lexicographic first-16 rule covers 16 of 27 strata (369/812 tasks). It has **no task whose site set includes `shopping`** (192 tasks). Its only `shopping_admin` case is the two-site stratum for task 759. The prereg already says "nonrepresentative"; the C1 summary SHOULD name this site gap explicitly.

## Smallest safe correction (wording only; L1 decides; I made no production edits)

Replace "pinned original WebArena benchmark" in the C1 claim, summary and case-report headers with:

> upstream `web-arena-x/webarena` (original lineage, not WebArena-Verified) at `dce04686` (committed 2025-11-26; `test.raw.json` last changed 2024-03-14, `evaluators.py` 2025-09-02, `helper_functions.py` 2023-12-22) — a revised state, not the 2023-07-25 release commit `b454f2dc` behind arXiv 2307.13854 v1; 480/812 tasks differ substantively in eval fields from release; no paper-era or leaderboard score applies to these specs.

Optionally add commit dates and the release-vs-pin distinction to `manifest.json` or the C1 summary scope block. Mark tasks 173 and 791 as LLM-judged, with the outcome unresolved statically.

## Sources opened (access date 2026-10-21; data only, never executed)

| URL | Located quote (≤25 words) | Scope |
|---|---|---|
| https://api.github.com/repos/web-arena-x/webarena/commits/dce04686a56253aefba7b18a4fa0937cf1dc987b | "Merge pull request #183 from alzambranolu13/patch-2", committer date `2025-11-26T21:15:59Z` | Pin date |
| https://api.github.com/repos/web-arena-x/webarena/commits?path=config_files/test.raw.json&sha=dce04686… | "release commit" `b454f2dcfdc6` 2023-07-25; latest "fix typo in intent" `bb6e4c623e73` 2024-03-14 | Task-file history (19 post-release commits) |
| https://api.github.com/repos/web-arena-x/webarena/commits?path=evaluation_harness/evaluators.py&sha=dce04686… | "Fix mypy type-checking errors" `60a6ca1a5d0f` 2025-09-02 | Scorer last change |
| https://api.github.com/repos/web-arena-x/webarena/commits?path=evaluation_harness/helper_functions.py&sha=dce04686… | "use fuzzy_match for UA tasks and update ua eval prompt" `3c4dcab8163d` 2023-12-22 | Helper last change; LLM-judge shift |
| https://raw.githubusercontent.com/web-arena-x/webarena/b454f2dcfdc6/config_files/test.raw.json | task 791 `"reference_answers": {"exact_match": "N/A"}` | Release task file (sha256 `4ea85923dd3d5425913cf655f04803c75b7c8ce7a5de7088a7782d5313efabf3`) |
| https://raw.githubusercontent.com/web-arena-x/webarena/b454f2dcfdc6/evaluation_harness/helper_functions.py | L170 `model="gpt-3.5-turbo",` | Release judge model |
| pinned fixture `evaluation_harness/helper_functions.py` (= manifest URL at `dce04686`) | L162 `model="gpt-4-1106-preview",` | Pinned judge model |
| https://arxiv.org/abs/2307.13854 (via export.arxiv.org) | "Submitted on 25 Jul 2023" | Paper v1 date |

## Observed commands

- `sha256sum` on the four fixture files: all four match the manifest.
- Python stdlib `json` parsing of the pinned and release task files (inventory, strata, selection, field diff), written to `diff-summary.txt`.
- `curl` to the GitHub API, GitHub raw and arXiv (listed above).
- No upstream code was executed, imported or evaluated. No benchmark sites were contacted. No builds or tests were run. No tools were installed or updated.

## Limitations

- The commit counts per path come from the GitHub API listing reachable from the pin. Merge topology could hide parallel edits, but the release-vs-pin byte diff is the decisive evidence and doesn't depend on it.
- "Substantive" is my own field split. A `program_html` change can be a locator fix rather than a semantic change, and I did not adjudicate individual changes.
- I did not determine whether this revised state is better or worse than the release. This is not a validity judgment.

## Final scoped verdict

**PARTIAL (C1 scope wording only).** The claim's counts, selection and disclaimers survive. The undated word "original" misidentifies the pinned bytes if read as the released or paper-era benchmark. A wording and date-boundary fix closes it. This is not a verdict on round 28, C2, or task validity.

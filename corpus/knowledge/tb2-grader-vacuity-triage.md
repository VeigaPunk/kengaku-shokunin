source: S179 — https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1 — the pinned tree: which grader files exist at the pin (184 = 94 test_outputs.py + 89 test.sh + 1 verify.sh), accessed 2026-10-28
source: S180 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md — the authors' claim that every task got several hours of human and LM-assisted validation, README line 87, accessed 2026-10-28
source: S181 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/bn-fit-modify/tests/test_outputs.py — three presence-only test functions beside real checks, accessed 2026-10-28
source: S182 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/pytorch-model-recovery/tests/test_outputs.py — the grader the file-level rule mislabelled V1: presence-only test_model_file_exists beside tensor comparisons, accessed 2026-10-28
source: S183 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/torch-tensor-parallelism/tests/test_outputs.py — the second mislabelled grader: presence-only test_parallel_linear_exists beside allclose checks, accessed 2026-10-28
source: S184 — https://github.com/harbor-framework/terminal-bench-2/pull/53 — maintainers' own 2.0→2.1 test-change PR: tests "over-specified or let any solution pass", accessed 2026-10-28
source: S185 — https://www.tbench.ai/news/terminal-bench-2-1 — the official 28-of-89 revision notice, instructions "not aligned to their tests", accessed 2026-10-28
source: S186 — https://huggingface.co/datasets/zai-org/terminal-bench-2-verified — third-party review naming four tasks whose test logic let non-compliant outputs through (tier B), accessed 2026-10-28
source: S187 — https://arxiv.org/html/2605.26079v2 — ABA, an agentic audit run against the same PR #53 fixes: 14 of 21 recovered under strict matching, accessed 2026-10-28
source: S188 — https://arxiv.org/abs/2503.15223 — pass-but-wrong patches on SWE-bench: weak-oracle prior art outside Terminal-Bench, accessed 2026-10-28
source: S189 — https://testsmells.org/assets/publications/FSE2020_TechnicalPaper.pdf — tsDetect Table 1: no catalogued test smell is an assertion that only checks existence, accessed 2026-10-28
source: S190 — https://arxiv.org/html/2601.11868 — the TB2 authors' "Specificity" bar (§2.3): tests pass iff the container ends in an acceptable state, accessed 2026-10-28
verified-at: 2026-10-28
recheck: 90d — from the lane root run `python3 plans/round52_c1_grader_audit.py --lane .` and compare with the numbers below; `(cd corpus/evidence/round52/graders && sha256sum -c SHA256SUMS)` reports exactly one missing file (the operator-excluded capture); re-open S184/S185 (mutable pages) and ask whether any of the five priced tasks was revised

# Terminal-Bench 2.0 grader population: a per-test presence triage, its findings, and why its verdict is `not admitted`

## Summary

Rounds 35–46 read twelve Terminal-Bench 2.0 graders by hand, one per round. Round 52 built the first
instrument that reads **all 89** as a population: `plans/round52_c1_grader_audit.py` over 184 digest-pinned
captures at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` (S179). It splits each primary
`tests/test_outputs.py` at `^def test_` and labels each test function `P1` (asserts only that an artefact
exists), `P2` (behavioural), `P3` (content/value) or `P0` (Amendment A1 in `plans/round-52-claims.md`).

What it measured on the committed captures (`.ufo/waves/round-52/claims/c1-after.txt`): 308 test functions,
**33 `P1` in 27 tasks**, file-level classes V1 2 · V4 0 · V2 53 · V3 31 · V0 3, `CANDIDATES total=29`.
Eight never-before-read tasks carry a confirmation whose quote appears verbatim in the captured bytes
(`corpus/evidence/round52/confirmations.json`).

What it does **not** support: "the grader of task X is vacuous". Independent audits in wave 2 found no
classified task graded by presence alone — every one of the 29 candidates also has content or behaviour tests —
so the finding is a *presence-only test function inside a larger grader*, never a whole-grader weakness.

**Verdict of the claim: not admitted.** The literal frozen predicate prints `CAPTURES expected=184 present=183`
and `classified=88` of 89 because the operator excluded one capture (`sanitize-git-repo/tests/test_outputs.py`,
GitHub push protection GH013 on a fake Hugging Face token inside the upstream fixture;
`corpus/evidence/round52/graders/EXCLUDED.md`). Amendment A5's additive line `PREDICATE R52-C1-A5` passes;
the closure, not this entry, rules on whether a digest-pinned absence counts. Novelty stays 8.

## Located quotes

Opened 2026-10-28; located in the fetched bytes (receipts in the lane's wave dir, `W2ScribeSourcesRows`).

| id | quote | where |
|---|---|---|
| S190 | "A terminal bench task is considered well-specified if the unit tests will pass if and only if the container ends in an acceptable state." | §2.3 "Specificity" |
| S184 | "Tests were updated when they over-specified or let any solution pass." | PR body line 8 |
| S185 | "Some tasks had instructions that were not aligned to their tests." | "What changed" |
| S186 | "the test logic itself misjudged valid submissions or let non-compliant outputs through" | 2026.08.18 update |
| S187 | "Our trajectory audit independently recovered 14 of these 21 issues under strict matching" | v2 body line 310 |
| S182 | "Checks if the model file exists" | `pytorch-model-recovery/tests/test_outputs.py:104` |
| S183 | "Checks that the agent creates a file named parallel_linear.py in the expected directory." | `torch-tensor-parallelism/tests/test_outputs.py:20-21` |
| S181 | "Test that the sampled data from the fitted BN exists" | `bn-fit-modify/tests/test_outputs.py:14` |

## Confirmed findings (never read by this lane before round 52)

Wave-2 reader seats located each quote; the counter checks that the quote occurs in the captured grader
bytes and that the task is a candidate and was not among the twelve hand-read tasks.

| task | test (line) | located assertion | readers |
|---|---|---|---|
| bn-fit-modify | `test_bn_sample_exists` (17) | `assert bn_sample_path.exists(), …` | W2ExecConfirmA, W2ExecConfirmB, W2RevConfirmations |
| build-cython-ext | `test_repo_cloned` (33) | `assert path.exists(), …` | A, B (W2RevConfirmations cites line 35 `(path / ".git").exists()` — a repository check, not a bare presence test) |
| caffe-cifar-10 | `test_prototxt_files_exist` (51) | `assert solver_file.exists(), …` | A, B |
| cancel-async-tasks | `test_run_py_file_exists` (14) | `assert run_path.exists(), …` | A, B |
| code-from-image | `test_output_file_exists` (15) | `assert output_path.exists(), …` | A, B |
| crack-7z-hash | `test_solution_file` (8-13) | solution file exists | W2ExecConfirmC (single reader) |
| extract-elf | `test_extract_js_exists` (309-313) | extract.js exists | W2ExecConfirmC (single reader) |
| financial-document-processor | `test_directories_created` (18-28), `test_summary_csv_exists` (100-103) | directories / CSV exist | W2ExecConfirmC (single reader) |

Readers A and B read the same five tasks from the same instruction, so their agreement is a repeatability check,
not two independent minds; `crack-7z-hash`, `extract-elf` and `financial-document-processor` have one reader.

## Prior-art pricing (`corpus/evidence/round52/prior-art.md`, 14 fetched URLs, HTTP 200 on 2026-10-28)

- **Instrument**: not new as a category. The TB2 paper's own QC runs a benchmark-wide adversarial exploit agent
  and concedes "Test case quality is not assessed via objective, automated metrics" (S190's paper, §B.4/§B.5);
  ABA audits the same 89-task population by agentic audit and recovers 14 of 21 PR #53 issues (S187). What no
  fetched page describes is a *static, per-test* presence classifier with committed digests.
- **Phenomenon**: documented at class level (S184 "let any solution pass", S186, S188). The scout seat priced
  four of the five A/B tasks (`bn-fit-modify`, `build-cython-ext`, `cancel-async-tasks`, `code-from-image`)
  *phenomenon-new at weakness level* (no fetched primary names the task) and `caffe-cifar-10` *unclear*
  (its grader was publicly reviewed twice; the presence-only test survives both). The other three confirmed
  tasks are unpriced.
- Absence from 14 pages is not absence from the literature; OpenAI and OpenReview pages were unreachable
  (HTTP 403 / challenge page) and stay leads.

## What the instrument gets wrong (wave-2 attacks that landed)

- **The per-test split leaks.** It cuts only at `^def test_`, so a following helper's code and comments belong
  to the previous block. `pytorch-model-recovery::test_model_file_exists` classes `P3` (the word "in" in a comment
  matches the value vocabulary) and `torch-tensor-parallelism::test_parallel_linear_exists` classes `P2` (helper
  `_setup_process_group` absorbed). **Both tests that motivated A1 are not `P1` in the committed counter**; both
  tasks are candidates only through the file-level `V1` label A1 declared false. Independent AST audits count
  47 `P1` (W2ExecEntryDraft) and 21 definite hand-found presence-only tests in 17 tasks missing from the counter
  (W2RevEntryLesson); one counter `P1` is false (`hf-model-inference::test_model_downloaded` loads a model).
  The 33/27 figure is the committed counter's output, not ground truth.
- **The predicate is reachable without the work.** W2CritC1Reach built five routes to `PASS` (population JSON
  rewritten to a subset; a forged stub with re-pinned digest; confirmations with `confirmed:"false"`; example
  URLs as prior art). W2MutC1 killed 0 of 16 mutants by a frozen control's named leg.
- **The labels are not blind agreement.** `labels.json` agrees 30 of 30 because it is the classifier's own
  rules re-applied; it is evidence of determinism, not of validity.

## Limits

A presence test beside a value check still leaves the task graded by that check; a candidate is a place to look,
never a verdict on the task. No task here is shown reward-hackable. Terminal-Bench 2.1 revised 28 tasks; four
of the five priced tasks are absent from PR #53's 57 changed files while `caffe-cifar-10`'s grader was rewritten there and its
presence-only test survived unflagged (W2ScoutPriorArtFresh); that PR is open and mutable (S184).
`test.sh` harness plumbing (one task has a path-less pytest conjunct in `fix-code-vulnerability/tests/test.sh`)
is outside the primary-grader rules.

## Re-run

```sh
python3 plans/round52_c1_grader_audit.py --lane .      # literal predicate + A5 line; exit 1 at round 52
python3 plans/round52_c1_grader_audit.py --selftest
(cd corpus/evidence/round52/graders && sha256sum -c SHA256SUMS)   # one line missing: the excluded capture
```

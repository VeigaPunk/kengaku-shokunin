# W2RevEntryLesson — scoped findings (R52-C1 candidate-set audit)

Full report and commands: `.ufo/waves/round-52/w2/W2RevEntryLesson/report.md`. Record: `.ufo/waves/round-52/w2/W2RevEntryLesson/candidate-review.json`.

**Counter run.** `python3 plans/round52_c1_grader_audit.py --lane .` → `CANDIDATES total=29`, `PREDICATE R52-C1 fail` (exit 1). Measured by the counter, not by hand.

**Named P1 check (first ten candidates).** 9 of 10 named P1 tests exist and contain no non-presence comparison. False candidate: `hf-model-inference::test_model_downloaded` (loads a model and asserts `is not None`).

**False candidates by rule.** `pytorch-model-recovery` and `torch-tensor-parallelism` are candidates through the file-level V1 label, which amendment A1 declares false for them; they have zero counter P1 tests.

**Missed P1 tests.** Both A1-named tests are missed: `pytorch-model-recovery::test_model_file_exists` (labelled P3 by prose "in" in a comment) and `torch-tensor-parallelism::test_parallel_linear_exists` (labelled P2 because the split absorbs helper defs). Hand audit finds 21 definite misses across 17 tasks (16 not already counter P1) plus three borderline tasks. Hand arithmetic: about 42 candidate tasks under the A1 rule (45 with borderline), against 29 reported.

**Counter defects.** Test split absorbs helper defs; VALUE matches prose and loop keywords; loader calls and `is not None` are not in the vocabulary; candidacy rule is looser than A1's "≥1 P1" and feeds the CONFIRMED leg.

**Limits on novelty.** Candidate recall on the A1 examples is 0 of 2. No task is wholly presence-only: the defensible claim is "presence-only tests occur in N tasks", not grader-level vacuity. Confirmations must be checked against hand-verified P1 blocks. The prior-art leg is still absent (`PRIOR-ART ok=False urls=0`).

**Verification.** 12 primary graders are byte-identical to upstream at pin `2fd12b88` (sha256 via curl). Other captures were not checked against upstream.

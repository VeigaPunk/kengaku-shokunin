# Round 52 wave 2 — seat W2RevEntryLesson (reviewer)

Scope: independent audit of the R52-C1 counter's test-function candidate set (`plans/round52_c1_grader_audit.py`), against the captured grader bytes under `corpus/evidence/round52/graders/`. No other seat's receipts were used. No lane, sibling, fleet or `.ufo/state` file was written. No git or jj mutation was run. No tool was installed.

Findings file: `.ufo/waves/round-52/w2/W2RevEntryLesson.md`. Full machine-readable record: `.ufo/waves/round-52/w2/W2RevEntryLesson/candidate-review.json` (also copied into scratch, then scratch removed).

## Commands run

1. `python3 plans/round52_c1_grader_audit.py --lane .` (exit 1). Output in `receipts/c1-run.txt`.
2. `python3 review.py` (reviewer analysis; reads captures and the counter module via importlib; writes only to scratch). Output summary in `receipts/analysis.json`.
3. Ad-hoc read-only Python over `split_tests` / `classify_test` / `VALUE` / `PRESENCE` to list value-marker hits per test, absorbed top-level code per block, and P1-block suspicious tokens.
4. `sha256sum` on 12 captured primary graders against `curl -fsS https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/<task>/tests/test_outputs.py`. All 12 equal upstream bytes.
5. `grep -c "^def <name>("` on each named P1 test in its captured grader (1 each).

## Counter output (the candidate set under audit)

```
TASKS total=89 records=89 classified=88
CAPTURES expected=184 present=183 mismatched=0
CLASS V1=2 V4=0 V2=53 V3=31 V0=3
TESTCLASS presence_only_tests=33 tasks_with_presence_only=27
CANDIDATES total=29
CONFIRMED new=0 []
PRIOR-ART ok=False urls=0
PREDICATE R52-C1 fail
A5 ... PREDICATE R52-C1-A5 fail   (fails on CONFIRMED / PRIOR-ART legs, not on the GH013 exclusion)
```

The first ten candidate lines are `bn-fit-modify, build-cython-ext, caffe-cifar-10, cancel-async-tasks, code-from-image, crack-7z-hash, db-wal-recovery, extract-elf, financial-document-processor, hf-model-inference`.

## Result 1 — named P1 tests (first ten candidates)

Each named P1 test exists in its captured grader (grep count 1).

- 9 of 10 hold as presence-only: bn-fit-modify (3 tests), build-cython-ext (test_repo_cloned), caffe-cifar-10 (test_prototxt_files_exist), cancel-async-tasks, code-from-image, crack-7z-hash, db-wal-recovery, extract-elf, financial-document-processor. No non-presence comparison sits in the named block.
- **1 false P1: hf-model-inference::test_model_downloaded.** The block loads a model and tokenizer (`from_pretrained`), then asserts `model is not None` and `tokenizer is not None` inside try/except. The frozen VALUE vocabulary does not contain loader calls or `is not None`, so the block is labelled P1. This is a substantive load check, not a presence check. Under a correct rule the task has no P1 and drops out of the candidate set.

Sibling substance (other tests in the same grader) for the first ten: bn-fit-modify has 6 P3 tests including a KS-test sampling check; build-cython-ext has P2/P3 tests of the C extensions; caffe-cifar-10 has P2/P3 tests; cancel-async-tasks has 5 P2 concurrency tests; code-from-image, crack-7z-hash and db-wal-recovery have P3 content checks; extract-elf has a P2 reference comparison; financial-document-processor has 6 P3 tests; hf-model-inference has 3 P2 API tests.

## Result 2 — false candidates

- `pytorch-model-recovery` and `torch-tensor-parallelism` are listed with `presence_only=-`. Candidacy comes from the file-level V1 label (`candidate = bool(p1) or cls in ("V1","V4")`). Amendment A1 says that file-level label is false for these two graders and defines candidacy as at least one P1 test. The code therefore contradicts the frozen amendment text.
- `hf-model-inference` (see Result 1).

The same looser rule feeds the CONFIRMED check (leg i), so the "hardened" check is looser than A1 states. No confirmations exist yet, so the current verdict is unaffected.

## Result 3 — missed P1 tests (A1-named and others)

**A1-named, both missed by the counter:**

- `pytorch-model-recovery::test_model_file_exists`: counter P3. Body is one `assert hello_path.exists()`. The comment "Reference the directory the agent operated in (the WORKDIR in the Docker env)" is inside the block, and `\bin\b` matches its word "in".
- `torch-tensor-parallelism::test_parallel_linear_exists`: counter P2. Body is one `assert parallel_linear_path.exists()`. The split only breaks at `^def test_`, so the block absorbs `_setup_process_group`, `_cleanup_process_group`, `_test_column_parallel_linear` and `_test_row_parallel_linear`, which call `dist.` and `mp.`.

**Definite by hand (21 tests across 17 tasks; 16 tasks are not already counter P1):** circuit-fibsqrt::test_gates_file_exists; cobol-modernization::test_required_files_exist and ::test_data_files_exist; extract-moves-from-video::test_solution_file_exists; financial-document-processor::test_summary_csv_exists; fix-code-vulnerability::test_report_file_exists_example; gcode-to-text::test_hello_file_exists; merge-diff-arc-agi-task::test_git_repo_init and ::test_algo_py_exists; rstan-to-pystan::test_output_files_exist; sparql-university::test_sparql_file_exists; torch-pipeline-parallelism::test_pipeline_parallel_exists; video-processing::test_example_video_exists and ::test_test_video_exists; llm-inference-batching-scheduler::test_output_files_exist; build-pmars::test_debian_source_used and ::test_built_from_source; tune-mjcf::test_tuned_model_exists; modernize-scientific-stack::test_dependency_file_exists; plus the two A1-named tests above.

Mechanisms: prose "in" in docstrings, comments and assert messages (`\bin\b`); for-loop keyword `in`; `-> None` annotation (`>`); helper absorption by the split.

**Borderline (not counted):** make-doom-for-mips and make-mips-interpreter `test_frame_bmp_exists` (`st_size > 0` non-empty check); custom-memory-heap-crash `test_program_compiles_debug/_release` (presence-only block, compile happens in helper `compile_program`).

**Hand arithmetic (not counter output):** 27 counter P1 tasks − 1 false (hf-model-inference) + 16 new = 42 candidate tasks under the A1 rule; 45 if the three borderline tasks are included.

## Counter defects found

1. `split_tests()` breaks only at `^def test_`; helper defs and trailing module code are absorbed. 15 blocks across 10 tasks carry absorbed code; three change class because of it.
2. `VALUE` is applied to comments, docstrings, assert messages, loop keywords, `->` annotations and string literals.
3. `classify_test()` ignores loader calls and `is not None`.
4. Candidate rule uses the file-level V1/V4 label, which A1 declares false; also loosens the CONFIRMED leg.
5. `PRESENCE` misses importlib `find_spec(...)` presence checks (build-cython-ext module tests are P0).
6. Tests whose assertions live in helpers (fix-git `test_about_file`, `test_layout_file`) have no assert in their own block and are P0.

## Limits on the novelty claim

- Candidate recall on the A1 examples is 0 of 2 and on the definite set is well below 1 (the counter flags 29; hand audit yields about 42 under the A1 rule). The triage queue is not reliable as built.
- Candidacy is per-test. No classified task has all tests P0/P1, and every first-ten candidate has substantive sibling tests. A claim of grader-level vacuity is not supported; the supported observation is "presence-only tests occur in N tasks".
- Confirmations must be checked against hand-verified P1 blocks, not the counter's labels, or they check the wrong tests (hf-model-inference shows the mismatch).
- Novelty (8→9) also depends on the prior-art leg, which does not exist yet (`PRIOR-ART ok=False urls=0`).

## Verification gaps

- Only the 12 primary graders named in the first-ten list and A1 were checked against upstream bytes. The other 76 captured graders were read through the counter's extraction and my scripts, not by sha256 against upstream.
- The P1 classification of blocks involving helpers was checked by hand for the listed tests only.
- The sanitize-git-repo grader is A5-excluded and was not re-fetched, as instructed.

## Receipts

- `.ufo/waves/round-52/w2/W2RevEntryLesson/candidate-review.json`
- `.ufo/waves/round-52/w2/W2RevEntryLesson/receipts/c1-run.txt`
- `.ufo/waves/round-52/w2/W2RevEntryLesson/receipts/review.py`
- `.ufo/waves/round-52/w2/W2RevEntryLesson/receipts/analysis.json`

Scratch dir `/fast/scratch/hyaku/kengaku-r52/w2-W2RevEntryLesson/` removed before yield.

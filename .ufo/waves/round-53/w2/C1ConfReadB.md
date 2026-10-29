# C1ConfReadB — R53-C1 confirm leg, second reader (4 tasks)

Read only: the four captures (`corpus/evidence/round52/graders/<task>/tests/{test_outputs.py,test.sh}`), `p1-spec.md`, `facts.md`, `corpus/evidence/round53/tests-index.json` spans, and each task's `instruction.md` at pin 2fd12b88 (curl of the raw URL). Not read: label files, the classifier, any `C1Label*`/`C1Exec*`/`C1Crit*`/`C1Mut*` output.

Commands: `curl -sf https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/<task>/instruction.md | head -c 1500` (all four returned); a python snippet that loaded the index spans, asserted each quote is a substring of the stated line (>=20 chars) and wrote the JSON. No tools installed. Nothing run in a clone; no scratch was created.

Deliverable: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w2/C1ConfReadB/confirmations-part.json` (4 objects, all `confirmed: true`).

## Per task

All four test.sh files are identical in shape: install uv, run `pytest /tests/test_outputs.py -rA`, reward = pytest exit code (torch adds torch 2.7.0 / transformers 4.55.0). Nothing there alters a test's verdict.

### extract-moves-from-video
- Instruction: download a YouTube Zork video, transcribe all the moves the player types, and write them one per line to /app/solution.txt.
- `test_solution_file_exists` (lines 327-334): the only assertion is `Path("/app/solution.txt").exists()`. Touching the file passes. Confirmed true.
- Rest of grader: `test_solution_content_similarity` reads the file and requires Levenshtein similarity >= 90 % against a 280-line embedded SOLUTION, so the grader as a whole does check content. The weakness is the existence test only.
- Quote (line 334): `assert solution_path.exists(), f"File {solution_path} does not exist"`.

### merge-diff-arc-agi-task
- Instruction: build /app/repo from two git bundles as branch1/branch2, merge branch2 into branch1, and produce algo.py with a `map` function that generalises the example grid mappings.
- P1 tests: `test_git_repo_init` (lines 10-13, only `Path("/app/repo/.git").exists()`) and `test_algo_py_exists` (lines 34-37, only `Path("/app/repo/algo.py").exists()`). Both pass for `mkdir -p /app/repo/.git` and `touch /app/repo/algo.py`. I confirm the first as the clearest; the second is equally presence-only.
- Rest of grader: `test_both_bundles_fetched` runs `git branch -a` and checks for branch1/branch2; `test_algo_py_has_map_function` imports algo.py and checks a callable `map`; `test_algo_map_function_with_test_input` runs `map` over /tests/test.json and compares every cell. Strong content checks. Note that `mkdir /app/repo/.git` alone would fail the `git branch` test.
- Quote (line 13): `assert git_path.exists(), "Git repository does not exist in /app/repo"`.

### prove-plus-comm
- Instruction: complete the unfinished Coq induction proof of addition commutativity in plus_comm.v and compile it with coqc so plus_comm.vo exists.
- P1 tests: `test_proof_file_exists` (lines 7-8, `os.path.exists("plus_comm.v")`) and `test_compiled_proof_exists` (lines 11-14, `os.path.exists("plus_comm.vo")`). Both are path-only. The relative paths resolve against the cwd. I confirm the compiled one as the clearest, since a bare `touch plus_comm.vo` stands in for the compile step. `plus_comm.v` itself is given with the task (the instruction says the file contains a partial proof), so `test_proof_file_exists` is satisfied before the agent does anything [INFERENCE from the instruction wording; the Dockerfile is not captured].
- Rest of grader: `test_proof_contents` reads plus_comm.v and checks for `n + m = m + n`, `Proof.`, `Qed.` and no `admit`. `test_compiled_proof_content` runs `coqc plus_comm.v` and requires exit 0. Note that coqc exit 0 is a real check, but it would also pass if the agent only left the file alone and it already compiled, which the content test counters. The grader is substantive overall.
- Quote (line 12): `assert os.path.exists("plus_comm.vo"), (`.

### torch-pipeline-parallelism
- Instruction: write /app/pipeline_parallel.py with `train_step_pipeline_afab(model, inputs, targets, device, dtype)` implementing all-forward-all-backward pipeline-parallel training of LLaMA with torch.distributed.
- `test_pipeline_parallel_exists` (lines 19-28): the only assertion is `Path("/app/pipeline_parallel.py").exists()`. An empty file passes. The module-level imports (torch, transformers, `sys.path.append("/app")`) do not touch the deliverable and are installed by test.sh. Confirmed true.
- Rest of grader: `test_no_hooks_in_pipeline_parallel` reads the file and rejects hook registration (a weak negative check: an empty file passes it, but a file that exists only passes it by lacking hooks); `test_pipeline_parallel[1,2]` spawns 1 and 2 processes, imports the function from /app and compares gradients and activations (hook-instrumented) with a reference. The numeric test is a real check.
- Quote (line 26): `assert pipeline_parallel_path.exists(), (`.

## Falsification attempt
For each of the six P1 tests I looked for reachable content, command, size or value checks (helpers, fixtures, conftest, test.sh side effects, module-level code run at import). Found none; there are no fixtures or helpers on any of the six test bodies (extract-moves' `levenshtein_distance` is called only by the similarity test). Negative result: no `confirmed: false`.

Tests listed beyond the one confirmed per task: merge-diff-arc-agi-task::test_algo_py_exists; prove-plus-comm::test_proof_file_exists.

tool: none inconsistent observed.

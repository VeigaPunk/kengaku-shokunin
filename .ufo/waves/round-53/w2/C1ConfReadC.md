# C1ConfReadC — R53-C1 confirm leg, independent second reader (group C)

Reader name: `C1ConfReadC`. Tasks: `fix-code-vulnerability`, `modernize-scientific-stack`, `pytorch-model-cli`, `torch-tensor-parallelism`.
Result: 4 of 4 tasks confirmed (`confirmed: true`); no reachable content/command/value check missed in any named test.
Deliverable: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w2/C1ConfReadC/confirmations-part.json` (list of 4 objects).

## What I read (and did not)
Read in full: `p1-spec.md`, `facts.md`, and for each task `corpus/evidence/round52/graders/<task>/tests/test_outputs.py` plus `tests/test.sh`
(`find <task> -type f` shows exactly those two files per task; no conftest, no fixtures, no helper modules). Spans from
`corpus/evidence/round53/tests-index.json`. Did NOT open any label file, `plans/round53_c1_classify.py`, or any `C1Label*`/`C1Exec*`/`C1Crit*`/`C1Mut*` output.

## Commands
- `curl -sSfL https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/<task>/instruction.md -o instruction-<task>.md` for the four tasks (all exit 0; sizes 3873, 1189, 532, 1324 bytes; copies kept in my seat directory).
- A python snippet loaded `tests-index.json`, took lines `lineno..end_lineno` of each test, and asserted every quote (whitespace-normalised) occurs inside that span, length >= 20, `why` <= 30 words. Output lines: quote lines 18, 49, 15, 25.

## Per task

### `fix-code-vulnerability` — id `fix-code-vulnerability::test_report_file_exists_example` (span 13-18), the only P1 test
- Instruction asks: find the CWE vulnerability in Bottle's `/app/bottle.py`, write `/app/report.jsonl` naming the file and CWE ids, and fix `_hkey` so it raises ValueError on invalid header names.
- Test body: `report_path = Path("/app/report.jsonl")`, `assert report_path.exists(), ...`. Nothing else reachable. An empty `/app/report.jsonl` passes. confirmed: true.
- Quote (line 18): `assert report_path.exists(), f"File {report_path} does not exist"`.
- Rest of grader: `test_vul_file` parses every line as JSON and requires `/app/bottle.py`; `test_cwe_id` requires `cwe-93`; `test_hkey_basic_cases`, `test_hkey_error_cases`, `test_hkey_real_world_examples` import `_hkey` and compare values. `test.sh` additionally runs the original repo's pytest and sets reward 1 only if both runs exit 0. So the grader as a whole is strong; the weakness is confined to this one test.

### `modernize-scientific-stack` — id `modernize-scientific-stack::test_dependency_file_exists` (span 46-50), the only P1 test
- Instruction asks: port a Python 2 climate-analysis script to Python 3 (pandas, pathlib, the exact output format) and add a dependency file with numpy, pandas and matplotlib or scipy under version constraints.
- Test body: `dep_files = [...]`, `assert any(Path(f).exists() for f in dep_files)`; either listed path existing suffices. Empty `requirements.txt` passes. The instruction demands version constraints, but this test does not check them. confirmed: true.
- Quote (line 49): `assert any(Path(f).exists() for f in dep_files)`.
- Rest of grader: `test_modernized_code_runs` runs the script with subprocess, requires return code 0, both stations in the output and means -15.5 / 30.3 within 0.1. `test.sh` runs only `/tests/test_outputs.py` under uvx with pinned numpy/pandas/matplotlib/scipy.

### `pytorch-model-cli` — P1 tests `test_weights_file_exists` (12-15), `test_cli_tool_exists` (18-21), `test_prediction_file_exists` (24-27)
- Instruction asks: build an executable `cli_tool` that, given `weights.json` and `image.png`, prints the MNIST digit predicted by the model, plus `weights.json` and a `prediction.txt` holding only the predicted digit, all in `/app`.
- Clearest single test: `pytorch-model-cli::test_weights_file_exists`. Body is `Path("/app/weights.json")` + `assert weights_path.exists()`; empty file passes. confirmed: true.
- Quote (line 15): `assert weights_path.exists(), f"File {weights_path} does not exist"`.
- Other two P1 tests, same shape and also true by reading: `pytorch-model-cli::test_cli_tool_exists` (`Path("/app/cli_tool").exists()`, line 21) and `pytorch-model-cli::test_prediction_file_exists` (`Path("/app/prediction.txt").exists()`, line 27). Not in the JSON (one object per task).
- Module-level imports (`cv2`, `numpy`, `torch`, `torchvision`) are supplied by `test.sh`'s uvx line; they are environment, not deliverable code, so the path-existence reading holds.
- Rest of grader: `test_prediction_file_content` reads `/app/prediction.txt` and requires `"2"`; `test_cli_tool_executable` runs `/app/cli_tool ... /app/image.png` and requires stdout `2`; `test_cli_tool_output` compares predictions on 50 MNIST images against a hard-coded list. Strong overall.

### `torch-tensor-parallelism` — id `torch-tensor-parallelism::test_parallel_linear_exists` (span 18-25), the only P1 test
- Instruction asks: implement `ColumnParallelLinear` and `RowParallelLinear` in `/app/parallel_linear.py` that shard a master weight across ranks, and match a reference `nn.Linear` in forward output and gradients at world sizes 1, 2, 4.
- Test body: `Path("/app/parallel_linear.py")` + `assert ....exists()`; an empty file passes. The docstring claims the file is checked "in the expected directory" but the code checks only existence. confirmed: true.
- Quote (line 25): `assert parallel_linear_path.exists(), f"File {parallel_linear_path} does not exist"`.
- Rest of grader: `test_column_parallel_linear` and `test_row_parallel_linear`, each parametrised over world size {1,2,4} x bias {True,False} (12 runs), spawn processes via `mp.spawn`, import the classes and use `torch.allclose` on weights, bias, outputs and gradients. Strong overall.

## Evidence summary
Attack/confirm landed on nothing contrary: for all four named tasks I looked for helpers, fixtures, `test.sh` conditions and module-level code that would turn existence into a content check and found none in the named test's reach. The reach caveat is `fix-code-vulnerability::test.sh`, which gates reward on a second pytest run, but that gate is outside the named test function and does not change its P1 status under the spec.

Tools installed or upgraded: none. No `tool:` inconsistencies observed. No scratch directory was created (nothing to remove). Files: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w2/C1ConfReadC/confirmations-part.json` and `instruction-<task>.md` x4 in the same directory.

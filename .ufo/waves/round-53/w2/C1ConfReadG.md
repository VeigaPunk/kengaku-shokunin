# C1ConfReadG — R53-C1 confirm leg (wave 2, independent second reader)

Reader: `C1ConfReadG`. Scope: never-read presence-only candidates `llm-inference-batching-scheduler`, `path-tracing`, `sam-cell-seg`, `winning-avg-corewars`. I read only the grader captures, the pinned task instructions and the tests index. I did not open any label file, the classifier `plans/round53_c1_classify.py`, or any output of `C1Label*`, `C1Exec*`, `C1Crit*`, `C1Mut*` seats.

## Deliverable

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w2/C1ConfReadG/confirmations-part.json`
  - sha256 `8d99f44858c96327fb807e8b0ff831deace49114d7dadb3cd23f00fdbac91233`, 4 objects.
- This report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w2/C1ConfReadG.md`

## What each task asks (pinned instruction, read via curl at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`)

- `llm-inference-batching-scheduler`: write a shape-aware batching scheduler that packs LLM requests into aligned-shape batches under cost, pad-ratio and latency thresholds, and writes two plan JSONL files.
- `path-tracing`: write a C program that renders the reference scene algorithmically, under 2 KB compressed, reaching 0.99 normalised L2 similarity with the supplied PPM.
- `sam-cell-seg`: write `convert_masks.py` that uses MobileSAM on CPU to turn rectangular and polyline cell masks into non-overlapping, single-region polylines in a CSV.
- `winning-avg-corewars`: write a Core War warrior `my_warrior.red` that reaches pMARS win-rate thresholds against five opponent warriors.

## Commands run

```
curl -fsSL https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/<task>/instruction.md   (x4)
python3 (read corpus/evidence/round53/tests-index.json: lineno/end_lineno of each named id)
grep -n '<quote>' corpus/evidence/round52/graders/<task>/tests/test_outputs.py   (line of each quote)
sha256sum corpus/evidence/round52/graders/*/tests/test_outputs.py
python3 (writer + check: each quote is a substring of its own test's span lines, >= 20 chars, why <= 30 words; output written to confirmations-part.json)
```

Capture bytes read in full (`read :raw` ranges, covering every line; the default view elides the middle of long files):
- `corpus/evidence/round52/graders/llm-inference-batching-scheduler/tests/test_outputs.py` (366 lines, sha256 `80b06b7c4ba0db28832b767d48be74bb462d7f5df5798d9cb58c4f1160d96ffa`) and its `tests/test.sh`
- `corpus/evidence/round52/graders/path-tracing/tests/test_outputs.py` (115 lines, sha256 `572e68b2843191d29592faf42a405861b7958d8e894868b74c5a8886b53eb879`) and `tests/test.sh`
- `corpus/evidence/round52/graders/sam-cell-seg/tests/test_outputs.py` (286 lines, sha256 `908c4b6aa44e12b6c429c221b92eaa6b150880b9b3d74d9d5ef6869a570f4fd4`) and `tests/test.sh`
- `corpus/evidence/round52/graders/winning-avg-corewars/tests/test_outputs.py` (108 lines, sha256 `252f78e5ce87ae3cf5852f192889aef5bd693ab0a13a6bf94cbb2fdce3218e93`) and `tests/test.sh`

Test spans from `tests-index.json` and the quote line numbers, both verified by the writer:

| test id | span | quote line | confirmed |
|---|---|---|---|
| `llm-inference-batching-scheduler::test_output_files_exist` | 91–102 | 97 | true |
| `path-tracing::test_image_c_exists` | 9–16 | 15 | true |
| `sam-cell-seg::test_python_file_exists` | 147–150 | 149 | true |
| `winning-avg-corewars::test_warrior_exists` | 39–41 | 41 | true |

## Per-task reading

**`llm-inference-batching-scheduler`, `test_output_files_exist`.** The body is two `os.path.exists` assertions on `plan_b1.jsonl` and `plan_b2.jsonl` under `/app/task_file/output_data/`. It calls no helper and reads no file. Two empty touched files pass. Confirmed. The file's other tests are not presence-only: `test_input_data_integrity` checks SHA-256 of the inputs, `test_generate_and_schema` checks alignment, heads/hidden constants and the 8-shape cap, `test_solution_shape_feasibility_and_batch_consistency` and `test_solution_coverage_no_duplicates` compare request ids and shapes, and `test_performance_thresholds` runs the cost model against the thresholds. Only `test_output_files_exist` is a presence check. The weakness is that single test, not the grader.

**`path-tracing`, `test_image_c_exists`.** The body is `Path("/app/image.c").exists()` with an assertion. No helper, no content read. Confirmed. The other tests are not presence-only: `test_image_compiles` runs gcc and checks the compressed size of `image.c`, `test_no_deps` runs `gcc -H`, `test_runs_and_produces_output` runs the binary in a chroot, and `test_image_similarity` computes cosine similarity against `/app/image.ppm` with a 0.99 threshold.

**`sam-cell-seg`, `test_python_file_exists`.** The body is `Path("/app/convert_masks.py").exists()` with an assertion. No helper, no content read. Confirmed. The same pattern holds for `test_csv_output_exists` (lines 177–180, quote line 179: `output_path = Path("/app/test_output.csv")` then `assert output_path.exists()`), which I also read as presence-only; I list it here and did not put it in the JSON, per the one-clearest-test rule. The other tests are not presence-only: `test_run_script` runs `convert_masks.py` with `check=True`, `test_csv_shape_cols` compares shape and columns with `correct_output.csv`, and `test_mask_alignment` computes IoU against the reference masks, with `test_masks_are_no_longer_rect`, `test_no_polyline_overlaps`, `test_single_contiguous_mask_per_cell` and `test_coords_are_flat_lists` checking geometry and content.

**`winning-avg-corewars`, `test_warrior_exists`.** The body is `Path("/app/my_warrior.red").exists()` with an assertion. No helper, no content read. Confirmed. The file's `test_warrior_performance` runs `pmars -b -r 100` against each opponent and compares the win counts with the thresholds, and `test_opponents_integrity` checks SHA-256 of the opponent warriors. Those two are the real checks.

## Quotes (verbatim, from the capture, line numbers as above)

- `llm-inference-batching-scheduler::test_output_files_exist`, line 97: `assert os.path.exists("/app/task_file/output_data/plan_b1.jsonl"), (`
- `path-tracing::test_image_c_exists`, line 15: `image_c_path = Path("/app/image.c")`
- `sam-cell-seg::test_python_file_exists`, line 149: `output_path = Path("/app/convert_masks.py")`
- `winning-avg-corewars::test_warrior_exists`, line 41: `assert Path("/app/my_warrior.red").exists(), "my_warrior.red file not found"`

## Limits of this reading

- The reader checked each named test against its body, not against the classifier. Any other P1 test in these four files is not confirmed here; from the bodies I read, the other tests in the four files are not presence-only (their details are above).
- I did not run any grader or any pytest. The confirmation is a reading of the bodies against the P1 definition in `.ufo/waves/round-53/p1-spec.md`.
- The `reader` field is `C1ConfReadG`, which is neither a `C1Label*` seat nor an author seat.

## Tools

No tools installed or upgraded. `curl` and the Python standard library were used. No pacman, no `gh`, no token handling.

tool: none observed inconsistent.

## Cleanup

Scratch: `/fast/scratch/hyaku/kengaku-r53/C1ConfReadG/` (instruction copies and nothing else); removed before yield.

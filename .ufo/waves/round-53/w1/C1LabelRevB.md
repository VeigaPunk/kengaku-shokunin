# C1LabelRevB — round-53 C1 blind label seat B

Wave 1 (build), lane `kengaku-shokunin`, R53-C1 (novelty 8→9). Blind label seat B of 8 for the
Terminal-Bench 2.0 presence-only oracle.

## What I did

Labelled all 76 ids of shard B by **reading** the captured grader bytes, against the single frozen
definition of "presence-only" in `.ufo/waves/round-53/p1-spec.md` (read in full) and the frozen
claims in `plans/round-53-claims.md` (read in full; commit `a34838f`).

Blindness: I did **not** read, run, or ask for `plans/round53_c1_classify.py`, anything under
`.ufo/waves/round-53/w1/C1ExecClassifier*`, or any other `C1Label*` seat's directory/file. The only
files I opened under `.ufo/waves/round-53/` are `p1-spec.md`, `labels/shard-B.json` and my own
`w1/C1LabelRevB/` output directory. No classifier was written or run by me; the only script I ran
was a coverage/constraint checker over my own `labels.json` (id coverage, label alphabet, `why`
word limit, credential-shaped-string scan).

## Sources read (all under the lane, read-only)

- `corpus/evidence/round52/graders/<task>/tests/test_outputs.py` — 60 distinct capture files,
  covering all 76 shard ids. Every shard span `lineno..end_lineno` was read in full, plus the whole
  file and its same-file helpers (module-level functions, same-class methods, same-file
  `@pytest.fixture` functions) and, where the test reaches it, the sibling `tests/test.sh` in the
  same task directory.
- `corpus/evidence/round52/graders/<task>/environment/tests/test_outputs.py` where present
  (`large-scale-text-editing`; byte-identical to its `tests/` copy — checked with `diff -q`).

## Labels

Deliverable: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1LabelRevB/labels.json`
(12 784 bytes).

```
sha256(labels.json) = 49fef84e4c7b6b659c346c1dbe69389f001720c9090a1f1254a439c52d585416
```

Counts: **Y = 13, N = 63, U = 0** (76 ids, shard covered exactly: 0 missing, 0 extra, 0 duplicates).

The 13 Y ids:

| id | why it is presence-only |
|---|---|
| `bn-fit-modify::test_bn_sample_exists` | one `Path(...).exists()` |
| `build-pmars::test_built_from_source` | glob non-empty + `src_dir.exists()` + glob `*.c` non-empty |
| `cobol-modernization::test_data_files_exist` | loop of `Path(...).exists()` |
| `extract-moves-from-video::test_solution_file_exists` | one `Path(...).exists()` |
| `fix-code-vulnerability::test_report_file_exists_example` | one `Path(...).exists()` |
| `kv-store-grpc::test_protobuf_generation` | two `Path(...).exists()` |
| `large-scale-text-editing::test_apply_macros_exists` | one `APPLY_SCRIPT.exists()` |
| `llm-inference-batching-scheduler::test_output_files_exist` | two `os.path.exists` |
| `multi-source-data-merger::test_output_files_exist` | two `os.path.exists` |
| `password-recovery::test_recovery_file_exists` | one `Path(...).exists()` |
| `pytorch-model-cli::test_prediction_file_exists` | one `Path(...).exists()` |
| `rstan-to-pystan::test_output_files_exist` | loop of `os.path.exists` |
| `sam-cell-seg::test_python_file_exists` | one `Path(...).exists()` |

### Why zero U

Two ids in this shard reach a module that is **not** among the captured files, so they were the only
candidates for U:

- `llm-inference-batching-scheduler::test_output_files_exist` — the capture has
  `from .cost_model_for_tests import HEADS, HIDDEN, CostModel, align`, and
  `cost_model_for_tests.py` was not captured.
- `fix-code-vulnerability::test_hkey_basic_cases` — imports `bottle._hkey` from an uncaptured
  sibling package (`tests/bottle/`).

In both cases the **verdict does not depend** on the uncaptured bytes, so the spec's U condition
("the verdict depends on code that is not in the captured files") is not met. In the first, the
reachable code is only the two `os.path.exists` calls (the relative import is never called by this
test) → Y. In the second, the assertion is `result == expected` on a returned string — a value
comparison under any implementation of `_hkey` → N. Same reasoning for the other uncaptured
dependencies reached in this shard (`headless_terminal`, `algo.py`, `pipeline_parallel`,
`mailman.core.*`, `correct_output.csv`, `/tests/golden.sql`, `inputs/*.ics`): each one's verdict was
decidable from the captured bytes alone, so I did not use U to paper over a read.

## Hardest ids and why

All eight entries below paraphrase the captured code; no grader bytes are quoted.

1. `llm-inference-batching-scheduler::test_output_files_exist` — the capture's own module-level
   relative import points at a file that is not in the captured set. Had the test body used any of
   the imported names, the verdict would have depended on uncaptured bytes and the honest label
   would have been U; it uses none of them, so Y.
2. `build-pmars::test_built_from_source` — the only Y whose assertions are glob-derived rather
   than existence-derived. The spec lists a non-empty glob as an allowed condition, and creating
   one matching source directory with one empty source file satisfies all three assertions, so it
   is presence-only under the operational rule. It is the single Y most likely to be contested by
   another seat.
3. `custom-memory-heap-crash::test_program_compiles_release` — the test's own final assertion is an
   existence check, but it reaches the same-file compile helper, which invokes the C++ compiler
   through a subprocess. Presence-only is false because reachable code runs a command (spec
   condition 3), not because the assertion is a value check.
4. `write-compressor::test_compressed_file_exists` — symmetric trap: the assertion is an existence
   check, but the reachable same-file setup helper copies files and invokes the C compiler. N.
5. `distribution-search::test_distribution_file_exists` — the assertion sits inside a
   `try`/`except` around a NumPy load of the file, with a pytest failure call on error. An *empty*
   file makes the load raise, so the failure branch fires: creating the path does **not** satisfy
   the test → N, not Y.
6. `build-cython-ext::test_chelpers_cython_extension` — the two assertions check that an import
   spec exists and that its loader is the extension-file loader. The second is a check on the
   *loader object's* type, not on a path's existence or type, and the spec lookup imports the
   deliverable's parent package, so it fails spec condition 3 as well → N.
7. `sam-cell-seg::test_csv_shape_cols` / `sam-cell-seg::test_coords_are_flat_lists` — both parse
   CSV content and compare parsed values; the reference CSV is uncaptured, but the verdict
   (content-dependent) is decidable from the captured bytes → N, not U.
8. `install-windows-3.11::test_windows_keys_with_visual_feedback` — takes a same-file fixture
   (a constant socket path) and then runs screenshot and keystroke subprocesses and compares
   pixel-diff percentages → N.

## Commands run

```sh
# shard contents and spans
python3 -c "import json;d=json.load(open('.../labels/shard-B.json'));[print(e['id'],e['file'],e['lineno'],e['end_lineno']) for e in d]"
# per-id span verification (first/last line of every span)
python3 - <<'EOF'   # prints lines[lineno-1] and lines[end_lineno-1] for all 76 ids
EOF
# duplicate environment/ vs tests/ capture
diff -q large-scale-text-editing/tests/test_outputs.py large-scale-text-editing/environment/tests/test_outputs.py
# coverage + constraint check of my own labels.json
python3 - <<'EOF'   # ids missing/extra/dupes, label alphabet, why<=20 words, credential scan
EOF
sha256sum .../w1/C1LabelRevB/labels.json
```

Reads were done with the `read` tool on the capture paths; no git mutation, no fixture repository,
no campaign tool, no package install (see below).

## Tooling

No tool was installed or upgraded by this seat; nothing on the task needed it (the job is reading
text and writing JSON). `python3` from the base image was the only interpreter used.

## Files produced

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1LabelRevB/labels.json`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1LabelRevB.md` (this report)

Scratch: `/fast/scratch/hyaku/kengaku-r53/C1LabelRevB/` was used only for throwaway checker
scripts and was removed before this report was written. Nothing outside my seat directory and the
scratch dir was written. Neither deliverable contains a credential-shaped string: a regex scan for
the usual secret prefixes, key-pem headers and flag-brace forms came back clean, and no captured
grader bytes were copied into either file.

## Residual notes for the L1

- My shard is 63 N / 13 Y, i.e. N-leaning. Several of the Y ids are "one `exists()` in a larger
  file whose neighbours do content checks" — a classifier that reasons per-file instead of
  per-function will disagree with me on those (e.g. `bn-fit-modify`,
  `pytorch-model-cli`, `rstan-to-pystan`, `sam-cell-seg`, `password-recovery`,
  `kv-store-grpc`, `multi-source-data-merger`).
- If the L1 wants the contested-set defined before opening the labels, `build-pmars::test_built_from_source`
  is the id in my shard where I would expect a genuine cross-seat contest.

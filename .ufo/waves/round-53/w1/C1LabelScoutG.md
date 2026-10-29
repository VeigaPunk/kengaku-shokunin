# C1LabelScoutG — blind label report (kengaku round 53, wave 1, R53-C1)

Seat: blind label seat G of 8. Scope honored: I read ONLY `.ufo/waves/round-53/p1-spec.md`, my shard
`.ufo/waves/round-53/labels/shard-G.json`, and capture files under
`corpus/evidence/round52/graders/<task>/…` reached by shard entries. I did not open, run, or ask about
`plans/round53_c1_classify.py`, any `w1/C1Label*` sibling directory, any `w1/C1Exec*` directory, or any
other seat's output. No classifier was written or run. No label was tuned against anything but the spec.

## Deliverable
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1LabelScoutG/labels.json`
- sha256 = `5c939a7f2ab58427d054d5cbd4879774d6c4653e12ddfe778970265395e49c0f`

## What I did
1. Read the p1 spec (presence-only definition: Y requires ≥1 reachable assertion, every assertion
   depends only on path existence/type, no reachable subprocess/content/size/value check).
2. Read all 76 shard entries (60 distinct `tests/test_outputs.py` captures, full files, ~8.7k lines) so
   same-file helpers/fixtures reached by each test were in view (e.g. `compile_program`,
   `run_shell_command`, `_test_jump_analyzer_video`, `setup()`, `install()`, `netstat_output` fixture).
3. Labeled every id Y/N/U by the spec.

## Commands run (verbatim)
```
mkdir -p .../.ufo/waves/round-53/w1/C1LabelScoutG /fast/scratch/hyaku/kengaku-r53/C1LabelScoutG
wc -l <60 grader tests/test_outputs.py paths>        # sizing only
ls corpus/evidence/round52/graders/llm-inference-batching-scheduler/tests/
python3 - <<'EOF'  # coverage check: shard ids vs labels ids, why<=20 words, label enum, sha256
```
Coverage check output: shard ids 76, labels 76, missing [], extra [], counts {N:66, Y:10}, U absent.

## Measured numbers
- **Y = 10, N = 66, U = 0** (76 total; classifier maps N and U both to P0, so effective P0 = 66/76 = 86.8%).
- Y ids: cancel-async-tasks::test_run_py_file_exists; cobol-modernization::test_data_files_exist;
  fix-code-vulnerability::test_report_file_exists_example; large-scale-text-editing::test_apply_macros_exists;
  llm-inference-batching-scheduler::test_output_files_exist; password-recovery::test_recovery_file_exists;
  pytorch-model-cli::test_prediction_file_exists; pytorch-model-recovery::test_model_file_exists;
  sam-cell-seg::test_python_file_exists; video-processing::test_example_video_exists.
- All 10 Y are existence-only assertions with zero reachable content/command/value checks in body or
  reached helpers.

## Hardest ids and why
- `build-cython-ext::test_chelpers_cython_extension` — `importlib.util.find_spec` + loader-type assert:
  module-existence, not a filesystem-path predicate, and reach imports the deliverable's parent packages
  (`pyknotid.spacecurves`). N, but it is the closest-to-the-line N in the shard.
- `llm-inference-batching-scheduler::test_output_files_exist` — module top has a relative import of
  `cost_model_for_tests` which is NOT in the captured tests dir (checked: only `test.sh`,
  `test_outputs.py`). The verdict does not depend on that code (body is two `os.path.exists`), so per the
  spec ("imports … not reachable code") I labeled Y, not U.
- `mcmc-sampling-stan::test_posterior_beta_estimation`, `rstan-to-pystan::test_sigma_estimation_accuracy`
  — silently pass when the output file is absent, but assert content/parse when present. Empty-file touch
  fails them → N under "passes in every state in which the paths merely exist".
- `custom-memory-heap-crash::test_program_compiles_release`, `write-compressor::test_compressed_file_exists`
  — final assert is existence-only, but a reachable same-file helper (`compile_program`, `setup`) runs a
  compiler subprocess → N.
- `kv-store-grpc::test_real_grpc_server_running` — TCP `connect_ex` port check: process/network state,
  not a named filesystem path → N.
- `headless-terminal::test_cancel_command` — final assert is `not path.exists()`, but the reachable code
  imports and drives the deliverable (`HeadlessTerminal`) → N.
- `mailman::test_simple_local_delivery` — mixes an existence-only retry helper with a subject-equality
  receipt check in the same reachable closure set → N.
- `install-windows-3.11::test_network_status` — test body is substring checks, but its requested fixture
  `netstat_output` runs a subprocess with its own asserts → N.

## U policy applied
No U. Every verdict was decidable from captured bytes; no test's outcome hinged on uncaptured code
(the one uncaptured import, above, does not affect its test's assertions).

## Integrity notes
- No tool installs or upgrades were needed (none performed).
- Blindness rules respected; no violation to disclose.
- Scratch dir `/fast/scratch/hyaku/kengaku-r53/C1LabelScoutG` was unused and removed before yielding.
- No credential-shaped strings or captured grader bytes quoted (only test-code fragments, each well
  under 25 words).

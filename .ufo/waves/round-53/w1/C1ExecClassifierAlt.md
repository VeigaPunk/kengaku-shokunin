# C1ExecClassifierAlt — report (round 53 wave 1)

Blindness: read only `plans/round-53-claims.md`, `.ufo/waves/round-53/p1-spec.md`, `tests-index.json` and the round-52 grader captures.
Never opened any `C1ExecClassifier*` output, `plans/round53_c1_classify.py`, or any label file/dir. Not the counted classifier.

## What I built
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1ExecClassifierAlt/alt_classify.py` — `classify_source(src) -> {key: 'P1'|'P0'}`
(plus `classify_detail(src)` with flags / assertion kinds / effects). Method: a small abstract interpreter, not call-name matching.
Values live in {K inert const/path, E existence-only bool, N name-from-listing, L listing, LEN len(listing), LE list-of-E, T other};
`assert` / `if…: pytest.fail|raise AssertionError` / `self.assert*` are evaluated over it (guards of a fail are joined; plain `assert` is not guarded).
`.exists/.is_file/.is_dir/.is_symlink`, `os.path.exists…`, `os.access(.., os.F_OK)` -> E; listdir/glob/iterdir -> L; `x in L` -> E; `len(L)` vs 0/1 -> E, other counts -> T;
`all/any` over E elements -> E; comparison of E with E / True / False -> E. Anything else (open, subprocess, read_*, stat, getsize, any imported/unknown call, `pytest.raises`) is an **effect** that makes the test P0 on its own; a test with no assertion, or any non-E assertion, is P0.
Reach: test body, same-file module functions, `self.` methods, nested defs, same-file `@pytest.fixture` requested by argument (parametrize names -> K, tmp_path -> K, unknown param -> T).
Also run a second pass with implicit reach (autouse fixtures, setUp*) to flag verdict changes (none occurred).

Self-check: the 8 spec worked examples all give the stated class (`python3 alt_classify.py`).

## Commands
```
cd .ufo/waves/round-53/w1/C1ExecClassifierAlt && python3 alt_classify.py     # 8/8 worked examples ok
PYTHONWARNINGS=ignore python3 run_alt.py                                         # 305 tests -> alt_results.json
```
No tools installed; no scratch dir used (nothing to clean); no git/jj command run.

## Result over the 305 tests (all keys found, missing=0, all module-level; no class tests in the index)
| class | n |
|---|---|
| P1 | 53 |
| P0 | 252 |

P0 reasons: 250 effect (open 57, subprocess.run 56, read_text 26, pandas.read_csv 13, stat 5, requests.get 5, numpy.load 4, …), 1 no assertion, 1 vacuous (constant-only) assertion.
Files: `alt_results.json` (per test: cls, assertion kinds string `E/K/T`, effects, flags), `alt_labels_flat.json` (id -> P1/P0), `run_alt.py`.
alt_classify.py sha256 f103a0b5c17774db73d9b3a53272be58334cce7c60cad4dc4ab32686c96ecb80 (not frozen; not the counted classifier).

## P1 list (53)
bn-fit-modify::{test_bn_sample_exists,test_learned_dag_structure_exists,test_intervened_dag_structure_exists}; build-cython-ext::test_repo_cloned; caffe-cifar-10::test_prototxt_files_exist; cancel-async-tasks::test_run_py_file_exists; circuit-fibsqrt::test_gates_file_exists; cobol-modernization::{test_required_files_exist,test_data_files_exist}; code-from-image::test_output_file_exists; crack-7z-hash::test_solution_file; db-wal-recovery::test_recovered_json_exists; extract-elf::test_extract_js_exists; extract-moves-from-video::test_solution_file_exists; financial-document-processor::{test_directories_created,test_summary_csv_exists}; fix-code-vulnerability::test_report_file_exists_example; gcode-to-text::test_hello_file_exists; kv-store-grpc::test_protobuf_generation; llm-inference-batching-scheduler::test_output_files_exist; merge-diff-arc-agi-task::{test_git_repo_init,test_algo_py_exists}; modernize-scientific-stack::test_dependency_file_exists; mteb-leaderboard::test_result_exists; mteb-retrieve::test_result_exists; multi-source-data-merger::test_output_files_exist; openssl-selfsigned-cert::test_directory_structure; password-recovery::test_recovery_file_exists; path-tracing::test_image_c_exists; path-tracing-reverse::test_image_c_exists; prove-plus-comm::{test_proof_file_exists,test_compiled_proof_exists}; pytorch-model-cli::{test_weights_file_exists,test_cli_tool_exists,test_prediction_file_exists}; pytorch-model-recovery::test_model_file_exists; raman-fitting::test_result_file_exists; rstan-to-pystan::test_output_files_exist; sam-cell-seg::{test_python_file_exists,test_csv_output_exists}; torch-pipeline-parallelism::test_pipeline_parallel_exists; torch-tensor-parallelism::test_parallel_linear_exists; tune-mjcf::test_tuned_model_exists; video-processing::{test_example_video_exists,test_test_video_exists}; vulnerable-secret::test_results_file_exists; winning-avg-corewars::test_warrior_exists; (alt_labels_flat.json is the authoritative list).

## Test ids where I am unsure (spec holes / judgment calls)
1. **Import-only / importability tests** (spec: importing deliverable code = N, but no call; "no assertion" vs process state): `headless-terminal::test_import` (no assertion -> P0), `kv-store-grpc::test_grpc_tools_installation` (`assert False` in `except ImportError`, constant-only -> P0), `build-cython-ext::{test_ccomplexity_cython_extension,test_chelpers_cython_extension,test_cinvariants_cython_extension,test_pyknotid_core_import}` (`importlib.util.find_spec` is neither listed existence call nor content read; I treat any non-listed call as effect -> P0), `merge-diff-arc-agi-task::test_algo_py_has_map_function` (spec_from_file_location).
2. **Existence assertions preceded by calls the spec does not classify**: `headless-terminal::test_cancel_command` (asserts E, but instantiates the uncaptured deliverable class -> U -> P0), `mailman::test_mlist_exists` (assert on a zope/mailman call result -> T), `hf-model-inference::test_model_downloaded` (ETTK: mixed existence plus from_pretrained).
3. **Setup helper with subprocess/shutil reached via the test**: `write-compressor::test_compressed_file_exists` (only `.exists()` assertion, but calls `setup()` which runs `shutil.copy` + `subprocess.run` -> P0 by clause 3; a label seat reading "assertions" only would say Y).
4. **Tests with no assertion that only run a command/spawn**: `sam-cell-seg::test_run_script`, `mailman::test_simple_local_delivery`, `mailman::test_join_announce_leave_flow`, `torch-pipeline-parallelism::test_pipeline_parallel`, `torch-tensor-parallelism::{test_column_parallel_linear,test_row_parallel_linear}` — all P0 (no assertion / command), no ambiguity in verdict but the spec's "reaches no assertion" and a failing exit from spawn are the only reasons.
5. **Module-level code** (spec Reach lists only test/helpers/fixtures): P1 tests whose file has module-level side effects (sys.path.insert/append, `pytest.main`): `kv-store-grpc::test_protobuf_generation`, `modernize-scientific-stack::test_dependency_file_exists`, `torch-pipeline-parallelism::test_pipeline_parallel_exists`, `torch-tensor-parallelism::test_parallel_linear_exists`. I ignored module-level effects (value-only). If a label seat counts them the answer flips only if they treat sys.path edits as "imports of deliverable".
6. **Vacuous constant-only assertions** (`assert K`, spec silent): `fix-code-vulnerability::test_hkey_error_cases` (KKKK), `kv-store-grpc::test_grpc_protocol_handshake`, `hf-model-inference::test_model_downloaded`; in all three other effects already decide P0.
7. Spec silent: `os.path.getsize` style tests in `train-fasttext::test_model_size` (spec says N: size value; implemented as T), listing **equality** (`sorted(os.listdir(d)) == [...]`) — I evaluate as T (computed comparison) and flag it; no test in the 305 hit that branch except through effects.
8. Spec silent: `open(..., 'w')`-only writers and `Path.write_text` — I treat write_* as benign, `open` of any mode as effect.

## Spec-hole summary for the L1
- Needs a decision: is a *call to `importlib.util.find_spec`* / `shutil.which` / `os.environ` an existence check? (spec lists only path-existence forms).
- Needs a decision: does module-level code and implicit setup (autouse fixture, `setUp`, `setup()` called from inside the test) count as reach? Spec lists only helpers the test calls; I implemented literal reach + flagged. Implicit pass changed no verdict.
- Constant-only assertions: Y or N?

## Tool inconsistencies
(none observed)

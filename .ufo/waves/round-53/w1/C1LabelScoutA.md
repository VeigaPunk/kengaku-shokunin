# C1LabelScoutA — round 53 wave 1, blind label seat A (shard-A)

## What I did
Blind-labeled all 77 test functions in `kengaku-shokunin/.ufo/waves/round-53/labels/shard-A.json` by reading, per
`kengaku-shokunin/.ufo/waves/round-53/p1-spec.md` (presence-only definition, frozen at claims commit a34838f). For every id I read the
full capture file (not just the span) so same-file helpers and module-level code were traced, plus reached same-file helpers:
`compile_program`/`run_program` (custom-memory-heap-crash), `make_fragment`/`calc_tm` (dna-assembly), `_test_jump_analyzer_video`
(video-processing), `_read_polylines_csv`/`is_single_contiguous_cv2` (sam-cell-seg), `run_shell_command` (build-pmars),
`compare_file_hashes`/`hash_file` (fix-git), `filter_all_files`/`make_batches` (filter-js-from-html), `retry`/`confirm_last_reply`
(mailman). No classifier was written, run, or looked at; no other seat's directory under
`.ufo/waves/round-53/w1` was read; no other label seat's file was read. No tool was installed or upgraded (none needed); no pacman
transaction was attempted.

## Commands run
- `wc -l` over the 59 distinct capture files (8,644 lines total) to plan full-file reads.
- `read` of each capture file's full text / relevant ranges under
  `kengaku-shokunin/corpus/evidence/round52/graders/<task>/tests/test_outputs.py`.
- One `python3` coverage check: shard ids vs `labels.json` keys (missing/extra/dupes), label-value and why-length checks,
  sha256. Ran in `/fast/scratch/hyaku/kengaku-r53/C1LabelScoutA/` (deleted afterward; second inline rerun used no scratch).

## Result
File: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1LabelScoutA/labels.json`
Format: `{"seat": "C1LabelScoutA", "labels": {<id>: {"label": "Y|N|U", "why": "<=20 words"}}}`, 77 entries, exact shard coverage
(0 missing, 0 extra, 0 dupes; every why <= 20 words).

**Counts: Y = 14, N = 63, U = 0.**
**sha256(labels.json) = `32a1b20bc29613c81b4bf271b941c64ad5bf5fb93cee513a6093d8a1dac48408`**

Y ids: bn-fit-modify::test_intervened_dag_structure_exists, build-pmars::test_debian_source_used,
cobol-modernization::test_required_files_exist, code-from-image::test_output_file_exists,
merge-diff-arc-agi-task::test_git_repo_init, mteb-leaderboard::test_result_exists, path-tracing::test_image_c_exists,
path-tracing-reverse::test_image_c_exists, prove-plus-comm::test_compiled_proof_exists,
pytorch-model-cli::test_cli_tool_exists, sam-cell-seg::test_csv_output_exists, sparql-university::test_sparql_file_exists,
tune-mjcf::test_tuned_model_exists, vulnerable-secret::test_results_file_exists.

N-but-interesting (existence-looking tests that are still N by the spec — the discriminating population):
- `financial-document-processor::test_original_documents_dir_empty` — `len(iterdir())==0` is a count comparison, not name
  membership (spec allows membership, not emptiness).
- `make-mips-interpreter::test_frame_bmp_exists` — exists plus `st_size > 0` (size value).
- `polyglot-c-py::test_fibonacci_polyglot` — `os.listdir(...) == ["main.py.c"]` compares the whole listing (computed value),
  and it then runs gcc/python subprocesses.
- `build-pmars::test_debian_source_used` — the one Y that is more than a bare exists: glob non-empty (allowed by spec
  criterion 2) plus `debian_dir.exists()`.
- `build-cython-ext::test_pyknotid_core_import` / `test_cinvariants_cython_extension` — `find_spec` import-machinery state and
  loader-type checks (`SourceFileLoader` / `ExtensionFileLoader`), not path predicates; touching named paths cannot satisfy them
  (the tests name no paths). Labeled N per spec criterion 2/3; flagging as the most debatable pair, together with
  `kv-store-grpc::test_grpc_tools_installation` (`assert False` only on ImportError — import/process state).
- `headless-terminal::test_import` — no assertion at all → N.

## Hardest ids
1. `financial-document-processor::test_original_documents_dir_empty` — reads as "directory is empty", which mere path creation
   *can* satisfy, but the spec's letter makes a count comparison N; decided on the letter (count is explicitly listed under N).
2. `build-cython-ext::test_pyknotid_core_import` — spec is silent on import-machinery existence; went N because
   `isinstance(loader, ...)` is a computed-value comparison and no path is named.
3. `kv-store-grpc::test_grpc_tools_installation` — has an assertion (`assert False` in `except ImportError`), but its condition
   is process/import state, not a path predicate → N.
4. `build-pmars::test_debian_source_used` — closest positive-to-negative boundary; kept Y because `glob` non-empty is
   explicitly allowed and the only other assertion is `.exists()`.
5. `polyglot-c-py::test_fibonacci_polyglot` — full-listing equality vs membership; N either way (subprocesses follow).

## Tool inconsistencies
None observed.

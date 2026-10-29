# C1LabelRevF — round 53 wave 1, blind label seat F (reviewer)

## Scope and blindness
- Read only: `.ufo/waves/round-53/p1-spec.md` (the definition), `.ufo/waves/round-53/labels/shard-F.json` (76 ids), and the grader captures under `corpus/evidence/round52/graders/<task>/tests/test_outputs.py` for the 58 tasks in the shard. Each file was read in full (ranged reads, see tool note), including same-file helpers and fixtures.
- Did NOT read or run `plans/round53_c1_classify.py`, anything under `.ufo/waves/round-53/w1/C1ExecClassifier*`, or any `C1Label*` directory.
- Disclosure: I ran one `ls` of `.ufo/waves/round-53/w1/` (twice, names only) to find my own output directory. That listing shows sibling seat directory names. I opened no file in any other seat directory. No classifier output was seen.
- No classifier was written or run. No tool was installed or upgraded. No git or jj command was run.

## Method
Per id: the test body plus every same-file helper it reaches. Rules applied from the spec: Y only if at least one assertion exists and every assertion depends only on `.exists()`, `.is_file()`, `.is_dir()`, `os.path.exists/isfile/isdir`, or name membership in a listing. Any content read, parse, subprocess, network call, size or mode value, count, value comparison, or call into deliverable code makes it N. A test with no assertion is N. A `find_spec` or loader-class check is not one of the allowed predicates, so it is N. A directory-emptiness check depends on what the directory contains, so it is N. U was not needed: no verdict depended on uncaptured code.

## Counts
- Y: 12
- N: 64
- U: 0
- Total: 76 (matches shard, 76 unique ids, no missing or extra)

Y ids: bn-fit-modify (learned_dag_structure_exists, intervened_dag_structure_exists); circuit-fibsqrt::test_gates_file_exists; cobol-modernization::test_required_files_exist; crack-7z-hash::test_solution_file; db-wal-recovery::test_recovered_json_exists; financial-document-processor::test_summary_csv_exists; merge-diff-arc-agi-task::test_git_repo_init; mteb-leaderboard::test_result_exists; path-tracing-reverse::test_image_c_exists; pytorch-model-cli::test_cli_tool_exists; torch-tensor-parallelism::test_parallel_linear_exists.

## Hardest ids
1. `build-cython-ext::test_pyknotid_core_import` — asserts `find_spec("pyknotid")` is not None and that the loader is a `SourceFileLoader`. The loader-class test is arguably a file-type check. I labelled N because the spec's allowed predicate list does not include `find_spec`. Creating an empty package file would pass it, so this is the most contestable N.
2. `financial-document-processor::test_original_documents_dir_empty` — asserts `len([f for f in iterdir() if is_file()]) == 0`. Only membership-in-listing is exempted. A count compared to zero, and a directory that passes only when empty regardless of how it was created, make it N.
3. `nginx-request-logging::test_log_file_creation` — the only assertion is `Path.exists()`, but the body first issues `requests.get` over the network. Rule 3 makes it N.
4. `make-doom-for-mips::test_frame_bmp_exists` and `make-mips-interpreter::test_frame_bmp_exists` — existence followed by `st_size > 0`. The size check makes these N; the existence check alone would be Y.
5. `fix-code-vulnerability::test_hkey_error_cases` — imports the deliverable `bottle` module (not in the captures) and checks that `_hkey` raises `ValueError`. Deliverable-code call makes it N. It is not U, because the verdict does not depend on the missing module's contents.
6. `headless-terminal::test_send_interactive_command` and `test_shell_state_persists_between_commands` — drive a deliverable terminal module and then compare file content. N on the content comparison alone.

## Output
- File: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1LabelRevF/labels.json`
- sha256: `dbe08bbffec96a3b00e2f480fe0e66c594dc577e67d42a5cffda9d6f16dd7232`
- Format: `{"seat": "C1LabelRevF", "labels": {id: {"label", "why"}}}`; every `why` is at most 20 words.

## Commands run
- `read` of p1-spec.md and shard-F.json (ranged).
- `wc -l` on the 58 grader files (bash, fact count only).
- `mkdir -p` for the seat output directory and `/fast/scratch/hyaku/kengaku-r53/C1LabelRevF` (the scratch dir is removed before yield; nothing was written to it).
- `python3` coverage check: shard ids vs labels keys, label counts, why-length, sha256 of labels.json. Output: `shard 76 unique 76 labels 76`, `missing []`, `extra []`, `counts {'N': 64, 'Y': 12}`, `why>20 words []`.
- A `grep` on labels.json for credential-shaped strings returned no hits (the only match was an ordinary word).

## Tool notes
- tool: `read` elides the bodies of multi-line calls and also elides large spans in the default window (`[…N ln elided…]`). I re-read each file in ranged windows of about 120 lines to cover every line. Lines inside elided call bodies were covered by the window reads.
- No tool installations or upgrades.

# C1LabelScoutE — round-53 wave-1 blind label report (shard E)

## What I did
Blind-labeled all 76 shard-E test functions of the Terminal-Bench 2.0 grader captures as
presence-only Y / N / U, strictly by `.ufo/waves/round-53/p1-spec.md` (frozen at claims commit
a34838f). For every shard id I read the test span `lineno..end_lineno` in the captured grader
file plus every same-file helper or `@pytest.fixture` the body reaches transitively (e.g.
`calculate_md5` in build-pov-ray, `check_file_hash`/`compare_file_hashes` in fix-git,
`run_solution`/`verify_legal_moves`/`do_test_game` in regex-chess, `compute_md5`/
`initialize_checksums`/`compile_program` in custom-memory-heap-crash, `_load_requests`/`_load_plan`
in llm-inference-batching-scheduler, `_run` in compile-compcert, the `qemu_pid`/`cmdline`/`netstat_output`
fixtures in install-windows-3.11, and the session-scoped autouse `compile_document` fixture in
overfull-hbox). No classifier was read, written, or run; no other seat directory was opened.

## Blindness
Respected: I read only p1-spec.md, shard-E.json, and captured grader files under
`corpus/evidence/round52/graders/<task>/tests/`. I never read or ran
`plans/round53_c1_classify.py`, never listed or opened any `w1/<other-seat>` path, and did not
see any other label seat's file. Nothing was tuned against another seat.

## Exact commands
1. `read` p1-spec.md and `.ufo/waves/round-53/labels/shard-E.json` (76 entries).
2. Structure map per capture file (grep, read-only):
   `grep -E '^(def |class |@pytest\.fixture|@pytest\.mark|\s{4}def )' <capture test_outputs.py>`
3. Read each shard test's span and each reachable helper's span in
   `corpus/evidence/round52/graders/<task>/tests/test_outputs.py`.
4. Coverage check before finishing (verbatim):
   `python3 - <<'EOF' ... shard = json.load(open('.ufo/waves/round-53/labels/shard-E.json')); lab = json.load(open('.ufo/waves/round-53/w1/C1LabelScoutE/labels.json')); ... EOF`
   Output: `shard ids: 76 label keys: 76 / missing: [] / extra: [] / bad labels: {} / why>20 words: {} / counts: {'N': 63, 'Y': 13}`.

## Measured numbers
- Shard size: 76 ids.
- **Y = 13, N = 63, U = 0.**
- Y ids (13): bn-fit-modify::test_bn_sample_exists; build-cython-ext::test_repo_cloned;
  build-pmars::test_built_from_source; extract-moves-from-video::test_solution_file_exists;
  kv-store-grpc::test_protobuf_generation; log-summary-date-ranges::test_summary_file_exists;
  modernize-scientific-stack::test_dependency_file_exists;
  multi-source-data-merger::test_output_files_exist;
  openssl-selfsigned-cert::test_directory_structure;
  pytorch-model-cli::test_weights_file_exists; rstan-to-pystan::test_output_files_exist;
  video-processing::test_test_video_exists; winning-avg-corewars::test_warrior_exists.
- N reasons observed (counts): content read/parse or content equality 34; subprocess/command run
  24; value/count comparison on computed results 21 (several tests trip more than one rule).

## Hardest calls and why
- **build-pmars::test_built_from_source → Y.** Name suggests a build check, but every reachable
  assertion is presence-only: `assert source_dirs` (`glob("pmars-*")` non-empty),
  `assert src_dir.exists()`, `assert c_files` (`glob("*.c")` non-empty). Empty files satisfy all
  three; spec explicitly allows `glob` non-empty.
- **distribution-search::test_distribution_file_exists → N.** Name says "exists", but the body is
  `np.load("/app/dist.npy")` inside try/except with `pytest.fail` — a content parse; an empty
  file raises, so touch does not satisfy. Spec rule 3 names `np.load` explicitly.
- **kv-store-grpc::test_protobuf_generation → Y.** Docstring mentions the protoc compiler, but
  the reachable body is exactly two `Path(...).exists()` asserts.
- **overfull-hbox::test_no_overfull_hboxes → N.** The substring test reads `main.log` content,
  and the session-scoped autouse fixture `compile_document` runs `os.system('apt install ...')`
  and `pdflatex` — reachable code that runs commands.
- **polyglot-rust-c::test_fibonacci_polyglot → N.** The first assertion compares the full
  `os.listdir("/app/polyglot")` to `["main.rs"]` (listing equality, not mere membership), and the
  body then compiles via `os.popen` and runs the produced binaries — command runs make it N
  regardless of how the listing assert is read.
- **custom-memory-heap-crash::test_protected_files_not_modified → N.** Contains an
  existence-only branch (`pytest.fail` if missing), but the decisive assertion compares
  `compute_md5` content checksums.
- **headless-terminal::test_send_non_interactive_command → N.** The `assert path.exists()` half
  is presence-only, but the test imports the task deliverable `headless_terminal`, drives it, and
  asserts `read_text().strip() == "Hello, world!"`.
- No id required U: in every case the captured bytes (test span + same-file helpers/fixtures)
  decided the verdict.

## Files produced
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1LabelScoutE/labels.json`
- This report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1LabelScoutE.md`

## sha256 of labels.json
`549c8b6313e5824ad83d68e1dcd81a4f134b51c7686d23e9b6213e079592e266`

(coverage re-verified immediately before hashing: 76 keys exactly matching the shard, labels in
{Y,N,U}, every `why` ≤ 20 words.)

## Tooling / scratch
No tools installed or upgraded (none needed). No scratch directory was created (no temp files,
fixtures, or clones used), so nothing to clean under /fast/scratch/hyaku/kengaku-r53. No
inconsistent tool behavior observed. No git/jj commands were run anywhere. No credential-shaped
strings written.

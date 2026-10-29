# C1ConfReadA — R53-C1 CONFIRM leg, second reader (group A)

Reader name: `C1ConfReadA`. Read only: facts.md, p1-spec.md, the claims file, the four captures (`corpus/evidence/round52/graders/<task>/tests/test_outputs.py` and `test.sh`) and `tests-index.json` spans. Not read: label files, the classifier, any `C1Label*/C1Exec*/C1Crit*/C1Mut*` output.

Deliverable: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w2/C1ConfReadA/confirmations-part.json` (4 objects, all `confirmed: true`, each quote verified as a substring of one line inside the test's `lineno..end_lineno` span by a script).

Commands: `cat -n` of the four captures and test.sh; `curl -sL https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/<task>/instruction.md` for each task; a python span check; a touch-run (below). No pytest installed on host (`No module named pytest`), so I ran the test functions directly, no install made.

All four `test.sh` files are identical in shape: install uv, `uvx pytest ... /tests/test_outputs.py -rA`, reward 1 iff pytest exits 0 (so every test in the file must pass; presence tests are one conjunct of the reward).

## Per task

### cobol-modernization
- Instruction: re-implement the COBOL `/app/src/program.cbl` as `/app/program.py` so the .DAT files it produces are content-identical to the COBOL run.
- Tests in P1: `cobol-modernization::test_required_files_exist` (span 11-18; asserts only `Path("/app/program.py").exists()`) and `cobol-modernization::test_data_files_exist` (span 21-31; asserts `.exists()` of four /app/data and /app/src .DAT paths, which the task supplies). Both are loops of `assert Path(p).exists()`; no read, no command.
- Clearest (confirmed): `test_required_files_exist`, line 18, quote `assert Path(file_path).exists(), f"Required file {file_path} does not exist"`. `test_data_files_exist` is the second P1 test, listed here, not in the JSON.
- confirmed: true. An empty `/app/program.py` satisfies it.
- Rest of grader: `test_program_output` (lines 34-94) rewrites the three .DAT files, runs `python /app/program.py` three times, asserts returncode 0 and compares all three file contents to exact expected strings. Real content check; the weakness is confined to the two presence tests.

### log-summary-date-ranges
- Instruction: count ERROR/WARNING/INFO per date window (today, last 7, last 30, month-to-date, total) over /app/logs with reference date 2025-08-12 and write `/app/summary.csv` with a fixed header and 15 rows.
- Test: `log-summary-date-ranges::test_summary_file_exists`, span 27-29, line 29, quote `assert OUTPUT_FILE.exists(), f"File {OUTPUT_FILE} does not exist"`.
- confirmed: true. An empty `/app/summary.csv` passes this test.
- Rest of grader: `test_summary_structure_and_counts` parses the CSV, checks header, 15-row count and every row against hard-coded expected counts. Real content check.

### path-tracing-reverse
- Instruction: write `/app/mystery.c`, a self-contained C program (under 2k compressed) that reproduces the output of the compiled path-tracer `/app/mystery`.
- Test: `path-tracing-reverse::test_image_c_exists`, span 9-17, line 17, quote `assert image_c_path.exists(), f"File {image_c_path} does not exist"`.
- confirmed: true. An empty `/app/mystery.c` passes this test.
- Rest of grader: `test_image_compiles` runs gcc and a zlib-size bound; `test_image_similarity` runs both binaries in chroot jails and requires cosine similarity >= 0.995. Strong content/behaviour checks.

### sparql-university
- Instruction: write a SPARQL query to `/app/solution.sparql` returning full professors in EU-country university departments with a department of >10 students, with `?professorName` and `?countries`.
- Test: `sparql-university::test_sparql_file_exists`, span 22-26, line 26, quote `assert SPARQL_PATH.exists(), f"SPARQL query file {SPARQL_PATH} does not exist"`.
- confirmed: true. An empty `/app/solution.sparql` passes this test. (The module imports `rdflib` at top level; that is environment-provided via `test.sh` `-w rdflib==7.1.4` and is irrelevant to the test's assertion.)
- Rest of grader: `test_sparql_runs_without_error` reads and executes the query on the TTL graph; `test_sparql_query_results` compares the result set to four reference rows. Real content check.

## Falsification attempt (step 3)
I looked for reachable content, command or value checks the classifier might have missed in each named test: no fixtures, no helpers, no `read_text`/`open`/subprocess in any named test body (`pytest` file-level code runs only imports and constant definitions). None found: all five named tests are presence-only under p1-spec.

Touch-run (not a pytest run): copied the four captures to scratch with `/app/` rewritten to a scratch dir, created all named paths as empty files, stubbed `rdflib`, and called the five named functions directly: all five `PASS` (cobol-modernization x2, log-summary-date-ranges, path-tracing-reverse, sparql-university). The ledger-grade real pytest touch-run belongs to `C1ExecTouch*`. Scratch deleted.

Tooling: none installed or upgraded. Tool anomalies: none.

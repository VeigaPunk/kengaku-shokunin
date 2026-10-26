| # | task | class | deciding line (`tests/test_outputs.py:L`) | note | lane |
|---|---|---|---|---|---|
| 1 | `adaptive-rejection-sampler` | P1 | `:73` `result = subprocess.run(` |  |  |
| 2 | `bn-fit-modify` | F2 | `:53` `assert learned_edges == true_dag, (` |  |  |
| 3 | `break-filter-js-from-html` | O1 | `:35` `["python", "/tests/filter.py", str(filtered_path)],` |  |  |
| 4 | `build-cython-ext` | B1 | `:54` `assert isinstance(spec.loader, importlib.machinery.ExtensionFileLoader` |  |  |
| 5 | `build-pmars` | B1 | `:23` `binary = Path("/usr/local/bin/pmars")` |  | **READ** |
| 6 | `build-pov-ray` | B1 | `:15` `result = subprocess.run(` |  |  |
| 7 | `caffe-cifar-10` | B1 | `:16` `result = subprocess.run(` |  |  |
| 8 | `cancel-async-tasks` | P1 | `:19` `result = subprocess.run(` |  |  |
| 9 | `chess-best-move` | F1 | `:25` `assert sorted(move) == sorted(["g2g4", "e2e4"]), "File is wrong"` |  |  |
| 10 | `circuit-fibsqrt` | P1 | `:119` `result = subprocess.run(["/app/sim", str(n)], capture_output=True, tex` |  | **READ** |
| 11 | `cobol-modernization` | P1 | `:55` `result = subprocess.run(` |  |  |
| 12 | `code-from-image` | F1 | `:25` `assert output.strip().startswith("bee26a"), (` |  |  |
| 13 | `compile-compcert` | B1 | `:30` `assert CCOMP_PATH.exists(), f"{CCOMP_PATH} does not exist"` |  |  |
| 14 | `configure-git-webserver` | S1 | `:11` `result = subprocess.run(["bash", "/tests/verify.sh"], capture_output=T` | delegates to tests/verify.sh (not fetched here) | **READ** |
| 15 | `constraints-scheduling` | F2 | `:42` `assert m, f"Missing timestamp: {rx}"` |  | **READ** |
| 16 | `count-dataset-tokens` | F1 | `:11` `assert expected_output in actual_output, (` |  |  |
| 17 | `crack-7z-hash` | F1 | `:25` `assert content == "honeybear", (` |  |  |
| 18 | `custom-memory-heap-crash` | P1 | `:86` `cmd = ["g++", "-std=c++17", "-o", output_file] + src_files + compile_f` | grader compiles agent's edited C++ tree |  |
| 19 | `db-wal-recovery` | F2 | `:53` `assert len(data) == 11, f"Expected 11 records, got {len(data)}"` | DB task, but grader reads only recovered.json | **READ** |
| 20 | `distribution-search` | F2 | `:80` `assert kf_error <= TOL, (` |  |  |
| 21 | `dna-assembly` | F2 | `:23` `"oligotm",` |  |  |
| 22 | `dna-insert` | F2 | `:86` `assert vector2[: len(annealed_fwd)] == annealed_fwd, (` |  |  |
| 23 | `extract-elf` | P1 | `:341` `stdout=open("/app/out.json", "w"),` | runs agent extract.js, diffs against reference |  |
| 24 | `extract-moves-from-video` | F2 | `:358` `assert similarity >= 90.0, (` |  |  |
| 25 | `feal-differential-cryptanalysis` | M1 | `:24` `import attack` |  | **READ** |
| 26 | `feal-linear-cryptanalysis` | F1 | `:122` `assert c in data` | 100 expected plaintexts are constants in the grader |  |
| 27 | `filter-js-from-html` | O1 | `:222` `assert Path("/app/filter.py").exists(), "filter.py does not exist"` | agent filter.py run, result judged in selenium/Chrome |  |
| 28 | `financial-document-processor` | F2 | `:66` `assert actual_file_hashes == expected_original_documents, (` |  |  |
| 29 | `fix-code-vulnerability` | M1 | `:59` `sys.path.insert(0, bottle_path)` | imports agent-patched bottle.py |  |
| 30 | `fix-git` | F1 | `:19` `assert hash_file(path_a) == hash_file(path_b), (` | git task, but grader hashes working-tree files |  |
| 31 | `fix-ocaml-gc` | F1 | `:19` `assert "40 tests passed" in tests_contents, "Could not determine that ` |  |  |
| 32 | `gcode-to-text` | F1 | `:17` `assert hello_path.read_text().strip() == "flag{gc0d3_iz_ch4LLenGiNg}",` |  |  |
| 33 | `git-leak-recovery` | G1 | `:23` `"git",` |  | **READ** |
| 34 | `git-multibranch` | S1 | `:72` `MAIN=$(curl -sk --max-time 5 https://localhost:8443/index.html 2>/dev/` | grader writes + runs verify.sh: ssh push, then https curl |  |
| 35 | `gpt2-codegolf` | P1 | `:20` `compile_result = subprocess.run(` |  |  |
| 36 | `headless-terminal` | M1 | `:18` `from headless_terminal import HeadlessTerminal` |  |  |
| 37 | `hf-model-inference` | S1 | `:47` `response = requests.post("http://localhost:5000/sentiment", json={"tex` | plus model dir load |  |
| 38 | `install-windows-3.11` | V1 | `:21` `result = subprocess.run(["pgrep", "qemu-system"], capture_output=True,` |  |  |
| 39 | `kv-store-grpc` | S1 | `:91` `sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)` |  |  |
| 40 | `large-scale-text-editing` | P1 | `:62` `def _run(cmd, timeout=300):` |  |  |
| 41 | `largest-eigenval` | M1 | `:21` `from eigen import find_dominant_eigenvalue_and_eigenvector # noqa` | also timing assert :111 |  |
| 42 | `llm-inference-batching-scheduler` | F2 | `:178` `assert ids_req == ids_plan, msg` | plan files scored by a cost model; timecost caps :328/:337 |  |
| 43 | `log-summary-date-ranges` | F1 | `:49` `assert actual_row == expected_row, (` |  |  |
| 44 | `mailman` | S1 | `:89` `with smtplib.SMTP("localhost", 25) as server:` |  |  |
| 45 | `make-doom-for-mips` | P1 | `:17` `process = subprocess.Popen(` | runs agent vm.js (node), reads stdout + frame.bmp |  |
| 46 | `make-mips-interpreter` | P1 | `:17` `process = subprocess.Popen(` | same grader shape as make-doom-for-mips |  |
| 47 | `mcmc-sampling-stan` | P1 | `:12` `["R", "--slave", "-e", "library(rstan); packageVersion('rstan')"],` |  |  |
| 48 | `merge-diff-arc-agi-task` | G1 | `:22` `["git", "branch", "-a"], cwd="/app/repo", capture_output=True, text=Tr` |  |  |
| 49 | `model-extraction-relu-logits` | P1 | `:46` `os.popen("python3 /app/steal.py").read()` |  |  |
| 50 | `modernize-scientific-stack` | P1 | `:21` `result = subprocess.run([sys.executable, str(script_path)],` |  |  |
| 51 | `mteb-leaderboard` | F1 | `:15` `assert lines[0].strip() == expected, "result.txt contains unexpected v` |  |  |
| 52 | `mteb-retrieve` | F1 | `:15` `assert lines[0].strip() == expected, "result.txt contains unexpected v` |  |  |
| 53 | `multi-source-data-merger` | F2 | `:22` `assert len(df) == 4` |  |  |
| 54 | `nginx-request-logging` | S1 | `:22` `response = requests.get("http://localhost:8080", timeout=2)` |  |  |
| 55 | `openssl-selfsigned-cert` | F2 | `:24` `# Verify key is 2048 bits` |  |  |
| 56 | `overfull-hbox` | P1 | `:67` `assert "Overfull \\hbox" not in log_content, (` | reads LaTeX log of grader-run compile of agent main.tex |  |
| 57 | `password-recovery` | F1 | `:18` `assert "8XDP5Q2RT9ZK7VB3BV4WW54" in guesses, "Password not found"` |  |  |
| 58 | `path-tracing-reverse` | P1 | `:60` `subprocess.run("cd /tmp; mkdir -p /jail_orig; cp mystery /jail_orig/; ` |  |  |
| 59 | `path-tracing` | P1 | `:37` `assert len(zlib.compress(open("/app/image.c").read().encode())) < 2100` |  |  |
| 60 | `polyglot-c-py` | P1 | `:30` `py_result = subprocess.run(` |  |  |
| 61 | `polyglot-rust-c` | P1 | `:30` `rust_result = subprocess.run(` |  |  |
| 62 | `portfolio-optimization` | M1 | `:39` `import portfolio_optimized_c` | imports a built C extension + speedup assert :129 |  |
| 63 | `protein-assembly` | F2 | `:42` `assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx, (` |  | **READ** |
| 64 | `prove-plus-comm` | P1 | `:30` `compile_result = subprocess.run(` |  |  |
| 65 | `pypi-server` | S1 | `:37` `uninstallcmd, capture_output=True, text=True, check=True` |  |  |
| 66 | `pytorch-model-cli` | P1 | `:19` `cli_path = Path("/app/cli_tool")` |  |  |
| 67 | `pytorch-model-recovery` | W1 | `:98` `assert torch.allclose(agent_weights[key], true_weights[key]), (` |  |  |
| 68 | `qemu-alpine-ssh` | V1 | `:25` `"sshpass",` |  |  |
| 69 | `qemu-startup` | V1 | `:56` `os.popen("expect -f run.exp").read()` |  |  |
| 70 | `query-optimize` | D1 | `:36` `con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)` |  |  |
| 71 | `raman-fitting` | F2 | `:36` `assert x0_correct and gamma_correct and A_correct and offset_correct, ` |  |  |
| 72 | `regex-chess` | F2 | `:13` `fen = re.sub(pattern, repl, fen)` | grader applies agent's regex list; pattern-valued |  |
| 73 | `regex-log` | F2 | `:90` `assert matches == expected_dates, f"Expected {expected_dates}, but got` |  | **READ** |
| 74 | `reshard-c4-data` | P1 | `:107` `["uv", "run", COMPRESS_SCRIPT, TEST_INPUT_DIR, TEST_OUTPUT_DIR],` |  |  |
| 75 | `rstan-to-pystan` | F2 | `:56` `assert os.path.exists(file_path), f"Required output file not found: {f` |  |  |
| 76 | `sam-cell-seg` | P1 | `:171` `# Execute the command as a subprocess` |  |  |
| 77 | `sanitize-git-repo` | G1 | `:62` `repo = git.Repo("/app/dclm")` |  |  |
| 78 | `schemelike-metacircular-eval` | P1 | `:17` `cmd, capture_output=True, text=True, input=input_data, timeout=10` |  |  |
| 79 | `sparql-university` | F2 | `:79` `assert result_set == reference_set, (` |  |  |
| 80 | `sqlite-db-truncate` | F1 | `:31` `assert score > 6, "Did not load data correctly"` | constants in grader |  |
| 81 | `sqlite-with-gcov` | B1 | `:13` `["sqlite3", ":memory:", "SELECT sqlite_version();"],` |  |  |
| 82 | `torch-pipeline-parallelism` | M1 | `:16` `sys.path.append("/app")` |  |  |
| 83 | `torch-tensor-parallelism` | M1 | `:15` `sys.path.append("/app")` |  |  |
| 84 | `train-fasttext` | W1 | `:30` `assert accuracy > ACCURACY_THRESHOLD` |  |  |
| 85 | `tune-mjcf` | F2 | `:67` `assert np.allclose(final_state, final_state_ref, atol=atol), (` |  |  |
| 86 | `video-processing` | P1 | `:17` `"""Helper for running jump_analyzer.py and validating outputs.` |  |  |
| 87 | `vulnerable-secret` | F1 | `:22` `assert content == expected_flag, f"Expected {expected_flag}, but got {` |  |  |
| 88 | `winning-avg-corewars` | P1 | `:59` `result = subprocess.run(` |  |  |
| 89 | `write-compressor` | P1 | `:15` `subprocess.run(["gcc", "-o", "decomp2", "decomp.c"], check=True)` |  |  |
import re,collections
LANE={"circuit-fibsqrt","constraints-scheduling","protein-assembly","regex-log","configure-git-webserver","build-pmars","git-leak-recovery","db-wal-recovery","feal-differential-cryptanalysis"}
R=[ # task, class, regex for deciding line, note
("adaptive-rejection-sampler","P1",r"subprocess\.run\(",""),
("bn-fit-modify","F2",r"assert learned_edges == true_dag",""),
("break-filter-js-from-html","O1",r"/tests/filter\.py",""),
("build-cython-ext","B1",r"ExtensionFileLoader",""),
("build-pmars","B1",r"/usr/local/bin/pmars",""),
("build-pov-ray","B1",r"subprocess\.run\(",""),
("caffe-cifar-10","B1",r"subprocess\.run\(",""),
("cancel-async-tasks","P1",r"subprocess\.run\(",""),
("chess-best-move","F1",r'assert sorted\(move\)',""),
("circuit-fibsqrt","P1",r'\["/app/sim"',""),
("cobol-modernization","P1",r"subprocess\.run\(",""),
("code-from-image","F1",r"startswith\(\"bee26a\"\)",""),
("compile-compcert","B1",r"CCOMP_PATH\.exists",""),
("configure-git-webserver","S1",r"/tests/verify\.sh","delegates to tests/verify.sh (not fetched here)"),
("constraints-scheduling","F2",r"Missing timestamp",""),
("count-dataset-tokens","F1",r'expected_output in actual_output',""),
("crack-7z-hash","F1",r'content == "honeybear"',""),
("custom-memory-heap-crash","P1",r'cmd = \["g\+\+"',"grader compiles agent's edited C++ tree"),
("db-wal-recovery","F2",r"len\(data\) == 11","DB task, but grader reads only recovered.json"),
("distribution-search","F2",r"kf_error <= TOL",""),
("dna-assembly","F2",r'"oligotm"',""),
("dna-insert","F2",r"vector2\[: len\(annealed_fwd\)\]",""),
("extract-elf","P1",r'/app/out\.json',"runs agent extract.js, diffs against reference"),
("extract-moves-from-video","F2",r"similarity >= 90\.0",""),
("feal-differential-cryptanalysis","M1",r"import attack",""),
("feal-linear-cryptanalysis","F1",r"assert c in data","100 expected plaintexts are constants in the grader"),
("filter-js-from-html","O1",r'filter\.py"\)\.exists',"agent filter.py run, result judged in selenium/Chrome"),
("financial-document-processor","F2",r"actual_file_hashes == expected_original_documents",""),
("fix-code-vulnerability","M1",r"sys\.path\.insert\(0, bottle_path\)","imports agent-patched bottle.py"),
("fix-git","F1",r"hash_file\(path_a\) == hash_file\(path_b\)","git task, but grader hashes working-tree files"),
("fix-ocaml-gc","F1",r"40 tests passed",""),
("gcode-to-text","F1",r"flag\{gc0d3",""),
("git-leak-recovery","G1",r'"git",',""),
("git-multibranch","S1",r"MAIN=\$\(curl","grader writes + runs verify.sh: ssh push, then https curl"),
("gpt2-codegolf","P1",r"compile_result = subprocess",""),
("headless-terminal","M1",r"from headless_terminal import HeadlessTerminal$",""),
("hf-model-inference","S1",r'requests\.post\("http://localhost:5000',"plus model dir load"),
("install-windows-3.11","V1",r'"pgrep", "qemu-system"',""),
("kv-store-grpc","S1",r"socket\.socket",""),
("large-scale-text-editing","P1",r"def _run\(cmd",""),
("largest-eigenval","M1",r"from eigen import","also timing assert :111"),
("llm-inference-batching-scheduler","F2",r"ids_req == ids_plan","plan files scored by a cost model; timecost caps :328/:337"),
("log-summary-date-ranges","F1",r"actual_row == expected_row",""),
("mailman","S1",r"smtplib\.SMTP",""),
("make-doom-for-mips","P1",r"subprocess\.Popen\(","runs agent vm.js (node), reads stdout + frame.bmp"),
("make-mips-interpreter","P1",r"subprocess\.Popen\(","same grader shape as make-doom-for-mips"),
("mcmc-sampling-stan","P1",r'\["R", "--slave"',""),
("merge-diff-arc-agi-task","G1",r'\["git", "branch", "-a"\]',""),
("model-extraction-relu-logits","P1",r"os\.popen\(\"python3 /app/steal\.py",""),
("modernize-scientific-stack","P1",r"sys\.executable, str\(script_path\)",""),
("mteb-leaderboard","F1",r"lines\[0\]\.strip\(\) == expected",""),
("mteb-retrieve","F1",r"lines\[0\]\.strip\(\) == expected",""),
("multi-source-data-merger","F2",r"len\(df\) == 4",""),
("nginx-request-logging","S1",r'requests\.get\("http://localhost:8080"',""),
("openssl-selfsigned-cert","F2",r"2048 bit",""),
("overfull-hbox","P1",r'Overfull',"reads LaTeX log of grader-run compile of agent main.tex"),
("password-recovery","F1",r"8XDP5Q2RT9ZK7VB3BV4WW54",""),
("path-tracing-reverse","P1",r"chroot /jail_orig",""),
("path-tracing","P1",r'zlib\.compress',""),
("polyglot-c-py","P1",r"py_result = subprocess",""),
("polyglot-rust-c","P1",r"rust_result = subprocess",""),
("portfolio-optimization","M1",r"import portfolio_optimized_c","imports a built C extension + speedup assert :129"),
("protein-assembly","F2",r"flag_idx < donor_idx",""),
("prove-plus-comm","P1",r"compile_result = subprocess",""),
("pypi-server","S1",r"installcmd, capture_output",""),
("pytorch-model-cli","P1",r'cli_path = Path\("/app/cli_tool"\)',""),
("pytorch-model-recovery","W1",r"torch\.allclose\(agent_weights",""),
("qemu-alpine-ssh","V1",r'"sshpass"',""),
("qemu-startup","V1",r"expect -f run\.exp",""),
("query-optimize","D1",r"sqlite3\.connect",""),
("raman-fitting","F2",r"x0_correct and gamma_correct",""),
("regex-chess","F2",r"re\.sub\(pattern, repl, fen\)","grader applies agent's regex list; pattern-valued"),
("regex-log","F2",r"assert matches == expected_dates",""),
("reshard-c4-data","P1",r'"uv", "run", COMPRESS_SCRIPT',""),
("rstan-to-pystan","F2",r"Required output file not found",""),
("sam-cell-seg","P1",r"Execute the command as a subprocess",""),
("sanitize-git-repo","G1",r"git\.Repo\(",""),
("schemelike-metacircular-eval","P1",r"cmd, capture_output=True, text=True, input",""),
("sparql-university","F2",r"result_set == reference_set",""),
("sqlite-db-truncate","F1",r"score > 6","constants in grader"),
("sqlite-with-gcov","B1",r'"sqlite3", ":memory:"',""),
("torch-pipeline-parallelism","M1",r'sys\.path\.append\("/app"\)',""),
("torch-tensor-parallelism","M1",r'sys\.path\.append\("/app"\)',""),
("train-fasttext","W1",r"accuracy > ACCURACY_THRESHOLD",""),
("tune-mjcf","F2",r"np\.allclose\(final_state, final_state_ref",""),
("video-processing","P1",r"jump_analyzer\.py",""),
("vulnerable-secret","F1",r"content == expected_flag",""),
("winning-avg-corewars","P1",r"result = subprocess\.run",""),
("write-compressor","P1",r'"gcc", "-o", "decomp2"',""),
]
names=[l.strip() for l in open("dirs.txt")]
assert sorted(names)==sorted(r[0] for r in R),(set(names)^set(r[0] for r in R))
CN={"F1":"file: constant/answer compare","F2":"file: computed/pattern/structured check","P1":"agent program/source executed by grader","M1":"agent module imported in grader process","B1":"built/installed artefact in image","S1":"service / network endpoint","V1":"VM / emulator","G1":"repository history/state","D1":"database queried","W1":"model/weights artefact","O1":"browser-in-the-loop"}
rows=[];cnt=collections.Counter();cov=collections.Counter();bad=[]
for t,c,rx,n in R:
    L=open(f"t/{t}.py").read().split("\n")
    hit=[i for i,l in enumerate(L,1) if re.search(rx,l)]
    if not hit: bad.append(t);continue
    i=hit[0];q=re.sub(r"\s+"," ",L[i-1].strip())[:70].replace("|","\\|")
    cnt[c]+=1
    if t in LANE: cov[c]+=1
    rows.append((t,c,i,q,n))
print("BAD",bad)
out=["| # | task | class | deciding line (`tests/test_outputs.py:L`) | note | lane |","|---|---|---|---|---|---|"]
for k,(t,c,i,q,n) in enumerate(rows,1):
    out.append(f"| {k} | `{t}` | {c} | `:{i}` `{q}` | {n} | {'**READ**' if t in LANE else ''} |")
open("table.md","w").write("\n".join(out))
h=["| class | meaning | tasks | lane-read |","|---|---|---|---|"]
for c in CN:
    h.append(f"| {c} | {CN[c]} | {cnt[c]} | {cov[c]} |")
open("hist.md","w").write("\n".join(h))
print("\n".join(h)); print(sum(cnt.values()), len([c for c in cnt if cnt[c]]))
for c in CN: print(c,[r[0] for r in rows if r[1]==c])

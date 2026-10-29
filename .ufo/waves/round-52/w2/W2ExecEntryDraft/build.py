import json,re,ast,sys
sys.path.insert(0,'/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans')
import round52_c1_grader_audit as A
from pathlib import Path
lane=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
G=lane/'corpus/evidence/round52/graders'
pop,records,exp,pres,mm,cands,sums=A.collect(lane)
astrows=json.load(open('ast_all.json'))
astp1={}
for t,n,c,a,s,e in astrows:
    if a=='P1': astp1.setdefault(t,[]).append((n,s,e))
# manual: what the rest of the grader checks (read from captured bytes)
OTHER={
'bn-fit-modify':"6 non-presence tests: learned_dag.csv/intervened_dag.csv column names + non-empty, learned/intervened edge sets == true_dag, sampled CSV columns, 10k rows x 5 cols and a kstest p>=0.001 on the sampled data.",
'build-cython-ext':"Beyond test_repo_cloned: numpy==2.3.0, importlib spec checks that pyknotid core and three Cython extensions load as ExtensionFileLoader, numeric checks of chelpers/ccomplexity/cinvariants (python vs cython), example usage values (alexander_polynomial, determinant), and a subprocess run of the repo's own tests.",
'caffe-cifar-10':"caffe --version == 1.0.0; model file exists and >100000 bytes; solver contains solver_mode:CPU and max_iter:500; Makefile.config CPU_ONLY:=1; training log has Iteration 500 / loss / accuracy; re-runs caffe test and checks accuracy >0.45 and within 0.05 of training accuracy.",
'cancel-async-tasks':"5 behavioural tests that subprocess-run /app/run.py and count 'Task started/finished/Cleaned up' markers, a >=6 s elapsed bound for max-concurrency, and SIGINT cancellation at/below/above the limit.",
'code-from-image':"test_output_is_correct: output.txt stripped startswith 'bee26a' plus a second multi-line assert on the content.",
'crack-7z-hash':"test_solution_content: /app/solution.txt content == 'honeybear'.",
'db-wal-recovery':"6 content tests on /app/recovered.json: valid list, id/name/value schema+types, sorted by id, exactly 11 records with expected ids and per-record values (WAL updates 1,2 and inserts 6-11), no duplicate ids, WAL-decrypted records present.",
'extract-elf':"test_output_matches_reference: gcc-compiles a reference, runs node extract.js and the reference script, compares the JSON memory maps value-by-value and requires a match percentage threshold.",
'financial-document-processor':"6 content tests: sha256 hashes of files moved into /app/invoices and /app/other equal the originals, summary.csv exists/headers/11 rows/per-row total_amount and VAT within 0.01, /app/original documents dir empty. test_summary_csv_exists is a second presence-only AST-P1 test the counter misclassified as P3.",
'hf-model-inference':"NOT presence-only: test_model_downloaded asserts the directory exists AND loads AutoModelForSequenceClassification/AutoTokenizer from it (from_pretrained). Other tests hit the Flask API on 0.0.0.0:5000 (sentiment endpoint values/types, 400 error handling).",
'kv-store-grpc':"proto file content strings (service KVStore, rpc GetVal/SetVal, messages); grpc importable; server.py defines class Server; port listening; live gRPC handshake and SetVal/GetVal round-trips returning 999/42/100.",
'large-scale-text-editing':"4 further tests: macro script is well-formed (tokens/macros/:wq), runs under vim (returncode 0, expected.csv generated), input.csv sha256 == expected, keystroke total <200 with non-empty distinct macros.",
'log-summary-date-ranges':"test_summary_structure_and_counts: header == [period,severity,count] and every row equals EXPECTED_ROWS.",
'mteb-leaderboard':"test_data_matches: result.txt has exactly one line equal to the expected answer string.",
'mteb-retrieve':"test_data_matches: result.txt has exactly one line equal to the expected answer string.",
'multi-source-data-merger':"test_merged_data_exact_values (4 users, ids, name/email/created_date for 101 and 104) and test_conflict_report_values (total_conflicts, user_101 conflict values and selected).",
'openssl-selfsigned-cert':"key permission<=0600 and '2048 bit'; cert CN/org strings and 365-day validity; combined PEM has PRIVATE KEY+CERTIFICATE and openssl exit 0; verification file strings/dates/fingerprint regex; the python verification script runs and prints expected stdout.",
'password-recovery':"test_password_match: '8XDP5Q2RT9ZK7VB3BV4WW54' is among the lines of recovered_passwords.txt (substring/membership check, non-empty).",
'path-tracing':"image.c compresses to <2100 bytes, compiles, has no /app/ deps, runs and writes reconstructed.ppm, and pixel similarity >=0.99 to the reference.",
'path-tracing-reverse':"mystery.c compresses to <2100 bytes, compiles; runs original binary and recompiled binary in chroot jails and requires image similarity >=0.995.",
'prove-plus-comm':"plus_comm.v contains 'n + m = m + n', 'Proof.', 'Qed.', no 'admit'; coqc compile returncode 0. Relative paths: the two exists tests resolve against the pytest cwd.",
'pytorch-model-cli':"test_prediction_file_content (== '2'), test_cli_tool_executable (output '2') and test_cli_tool_output (many-image prediction comparison).",
'pytorch-model-recovery':"Counter shows presence_only=-; the candidate flag comes only from file-level V1. test_model_file_exists (lines 103-108) is presence-only (AST P1) but labelled P3 by the counter (docstring comment word 'in'). Sibling tests: weights unchanged (torch.allclose), model loads weights, state dict keys/values match except output_layer, agent MSE loss < true model loss. So the grader as a whole is NOT presence-satisfiable.",
'raman-fitting':"test_G_Peak and test_2D_Peak: results.json x0/gamma/amplitude/offset each within tolerance of expected.",
'sam-cell-seg':"test_run_script executes /app/convert_masks.py via subprocess (check=True), then CSV shape/columns, mask-no-longer-rectangular, mask alignment, no polyline overlaps, one contiguous mask per cell, flat-list coords.",
'torch-tensor-parallelism':"Counter shows presence_only=- (file-level V1 only). test_parallel_linear_exists (lines 18-25) is presence-only (AST P1) but labelled P2 because split_tests folds the following helper defs (dist.init_process_group) into its block. The two real tests (lines ~187/~203, parametrised over bias/world_size) mp.spawn gloo processes and torch.allclose-compare ColumnParallelLinear/RowParallelLinear weights, bias and outputs; counter labels them P0 (assert lives in the _test_* helper).",
'vulnerable-secret':"test_results_file_contains_secret_flag (content == expected flag) and format (starts FLAG{, ends }, len>10).",
'winning-avg-corewars':"opponent hash integrity; test_warrior_performance runs pmars battles and requires win rate >= threshold.",
'write-compressor':"Setup compiles decomp.c with gcc; decompressor run on data.comp must reproduce original stdout exactly; compressed size <= max bytes.",
}
rows=[]
for t in cands:
    r=records[t]; body=(G/r['grader']).read_text(errors='replace'); L=body.split('\n')
    tests=r['tests']; cmap={x['test']:x['class'] for x in tests}
    ap=astp1.get(t,[])
    p1ev=[]
    for n,s,e in ap:
        q=next((l.strip() for l in L[s-1:e] if re.search(r'\bassert\b',l)),None)
        qline=next((s+i for i,l in enumerate(L[s-1:e]) if re.search(r'\bassert\b',l)),None)
        p1ev.append({'test':n,'def_line':s,'end_line':e,'assert_line':qline,'quote':q,'counter_class':cmap[n]})
    verified=bool(p1ev)
    cnt_p1=r['presence_only_tests']
    dis=[]
    if set(cnt_p1)!={x['test'] for x in p1ev}:
        missed=sorted({x['test'] for x in p1ev}-set(cnt_p1)); false=sorted(set(cnt_p1)-{x['test'] for x in p1ev})
        if missed: dis.append({'kind':'counter-missed-presence-only','tests':missed})
        if false: dis.append({'kind':'counter-false-P1','tests':false})
    rows.append({'task':t,'grader':'corpus/evidence/round52/graders/'+r['grader'],'sha256':r['sha256'],'bytes':r['bytes'],'lines':len(L),'test_count':r['test_count'],
     'counter_file_class':r['class'],'counter_P1_tests':cnt_p1,'independent_P1_tests':p1ev,'verified_presence_only_test':verified,
     'other_tests':[{'test':x['test'],'counter_class':x['class']} for x in tests if x['test'] not in {p['test'] for p in p1ev}],
     'what_else_grader_checks':OTHER[t],
     'whole_grader_verdict':'not vacuous: a test-level finding only; the grader as a whole also checks content/behaviour' ,
     'counter_disagreement':dis})
# extra population-wide disagreements
extra=[]
for t,n,c,a,s,e in astrows:
    if (c=='P1')!=(a=='P1') and t not in cands:
        extra.append({'task':t,'test':n,'def_line':s,'counter_class':c,'independent_class':a})
out={'schema':'w2-W2ExecEntryDraft candidate audit','counter_output':{'candidates':len(cands),'P1_tests':33,'tasks_with_P1':27},
 'independent_method':'ast: top-level test_ function bodies whose only assertions are exists/is_file/is_dir calls (no comparison, no other call except Path/join/str/setup()); line numbers 1-based in captured bytes',
 'candidates':rows,
 'non_candidate_counter_misses':extra}
json.dump(out,open('candidate-audit.json','w'),indent=1)
print(len(rows),sum(r['verified_presence_only_test'] for r in rows),[ (r['task'],r['counter_disagreement']) for r in rows if r['counter_disagreement']])
print(len({e['task'] for e in extra}),sorted({e['task'] for e in extra}))

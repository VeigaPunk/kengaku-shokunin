import json, shutil, subprocess, os, re, hashlib
from pathlib import Path
LANE=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
FX=Path('/fast/scratch/hyaku/kengaku-r52/w2-W2RevClassifierImpl/fx')
COUNTER=LANE/'plans/round52_c1_grader_audit.py'
G=LANE/'corpus/evidence/round52/graders'
def fresh(name):
    d=FX/name
    if d.exists(): shutil.rmtree(d)
    (d/'corpus/evidence').mkdir(parents=True)
    shutil.copytree(LANE/'plans', d/'plans')
    shutil.copytree(LANE/'corpus/evidence/round52', d/'corpus/evidence/round52')
    shutil.copytree(LANE/'corpus/knowledge', d/'corpus/knowledge')
    return d
def run(d):
    out=subprocess.run(['python3',str(COUNTER),'--lane',str(d)],capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    keep=[l for l in (out.stdout+out.stderr).splitlines() if re.match(r'(TASKS|CAPTURES|CONFIRMED|  REJECTED|PRIOR-ART|LABELS|PREDICATE|A5 |Traceback|\w+Error)',l)]
    return out.returncode, keep
def conf(d, rows): (d/'corpus/evidence/round52/confirmations.json').write_text(json.dumps(rows,indent=1))
def pa(d, text): (d/'corpus/evidence/round52/prior-art.md').write_text(text)
def has(task,quote,grader):
    t=(G/grader).read_text(errors='replace'); assert quote in t, (task,quote)
    return True
GR={'mteb-leaderboard':'mteb-leaderboard/tests/test_outputs.py','multi-source-data-merger':'multi-source-data-merger/tests/test_outputs.py',
    'pytorch-model-recovery':'pytorch-model-recovery/tests/test_outputs.py','torch-tensor-parallelism':'torch-tensor-parallelism/tests/test_outputs.py',
    'password-recovery':'password-recovery/tests/test_outputs.py'}
Q={'mteb-leaderboard':'def test_result_exists','multi-source-data-merger':'def test_output_files_exist',
   'pytorch-model-recovery':'hello_path = Path("/app/model.pt")','torch-tensor-parallelism':'parallel_linear_path = Path("/app/parallel_linear.py")',
   'password-recovery':'def test_recovery_file_exists'}
for k in Q: has(k,Q[k],GR[k])
has('x','assert',GR['mteb-leaderboard']); print('quotes verified verbatim in captured bytes')
PA_OK="fixture-only URLs: https://example.org/fx-a https://example.org/fx-b https://example.org/fx-c\n"
VALID=[{"task":"mteb-leaderboard","quote":Q['mteb-leaderboard'],"reader":"R2","confirmed":True},
       {"task":"multi-source-data-merger","quote":Q['multi-source-data-merger'],"reader":"R2","confirmed":True}]
results={}
def case(name, setup, note):
    d=fresh(name); setup(d); rc,lines=run(d); results[name]=(rc,lines)
    print(f'=== {name}: {note}  exit={rc}')
    for l in lines: print('   ',l)
# F0 baseline
case('F0-base', lambda d: None, 'live state reproduction (no receipts)')
# F1 confirmed as string "false"
case('F1-false-string', lambda d: (conf(d,[{"task":"mteb-leaderboard","quote":Q['mteb-leaderboard'],"reader":"R2","confirmed":"false"},{"task":"multi-source-data-merger","quote":Q['multi-source-data-merger'],"reader":"R2","confirmed":"false"}]), pa(d,PA_OK)), 'both readers wrote confirmed:"false" (string)')
# F2 one-token quote
case('F2-one-token-quote', lambda d: (conf(d,[{"task":"mteb-leaderboard","quote":"assert","reader":"R2","confirmed":True},{"task":"multi-source-data-merger","quote":"assert","reader":"R2","confirmed":True}]), pa(d,PA_OK)), 'quote = bare keyword "assert", no located line')
# F3 candidate via file-level V1 only (A1 says no presence-only test)
case('F3-V1-only-candidate', lambda d: (conf(d,[{"task":"pytorch-model-recovery","quote":Q['pytorch-model-recovery'],"reader":"R2","confirmed":True},{"task":"torch-tensor-parallelism","quote":Q['torch-tensor-parallelism'],"reader":"R2","confirmed":True}]), pa(d,PA_OK)), 'two tasks admitted only via file-level V1; their per-test P1 set is empty')
# F4 read-set deletion
def f4(d):
    (d/'corpus/knowledge/tb2-password-recovery-grader.md').unlink()
    conf(d,[{"task":"password-recovery","quote":Q['password-recovery'],"reader":"R2","confirmed":True},{"task":"multi-source-data-merger","quote":Q['multi-source-data-merger'],"reader":"R2","confirmed":True}]); pa(d,PA_OK)
case('F4-delete-knowledge-entry', f4, 'delete the lane knowledge entry for password-recovery (a P1 task the lane read) -> counted as never-read')
def f4c(d):
    conf(d,[{"task":"password-recovery","quote":Q['password-recovery'],"reader":"R2","confirmed":True},{"task":"multi-source-data-merger","quote":Q['multi-source-data-merger'],"reader":"R2","confirmed":True}]); pa(d,PA_OK)
case('F4-control-entry-present', f4c, 'control: same receipts, entry present -> must reject')
# F5 legitimate new entry named by convention blocks a true confirmation
def f5(d):
    (d/'corpus/knowledge/tb2-mteb-leaderboard-grader.md').write_text('# new entry (fixture)\n')
    conf(d,VALID); pa(d,PA_OK)
case('F5-new-entry-convention', f5, 'L1 writes entry tb2-mteb-leaderboard-grader.md citing a valid confirmation')
# F6 prior-art spellings + no verdicts
case('F6-prior-art-spellings', lambda d: (conf(d,VALID), pa(d,"Primary: https://github.com/harbor-framework/terminal-bench-2\nSame: https://github.com/harbor-framework/terminal-bench-2/\nSame: <https://github.com/harbor-framework/terminal-bench-2>\nNo verdict is written anywhere in this file.\n")), 'one repo, three spellings (slash, angle brackets), no per-finding verdict')
# F7 population shrink
def f7(d):
    p=d/'plans/round52-tasks.json'; pop=json.loads(p.read_text())
    pop['tasks'].pop('sanitize-git-repo'); pop['capture_population'].pop('sanitize-git-repo')
    pop['task_count']=88; pop['capture_file_count']=182
    p.write_text(json.dumps(pop)); conf(d,VALID); pa(d,PA_OK)
case('F7-shrunk-population', f7, 'population JSON edited to 88 tasks / 182 captures; counter never checks 89/184')
# F8 digest self-consistency (tamper bytes + rewrite SHA line)
def f8(d):
    tgt='mteb-leaderboard/tests/test_outputs.py'; f=d/'corpus/evidence/round52/graders'/tgt
    f.write_bytes(f.read_bytes()+b'\n# tampered in fixture\n'); new=hashlib.sha256(f.read_bytes()).hexdigest()
    s=d/'corpus/evidence/round52/graders/SHA256SUMS'; s.write_text(re.sub(r'^[0-9a-f]{64}(  \./'+re.escape(tgt)+')$', new+r'\1', s.read_text(), flags=re.M))
    conf(d,VALID); pa(d,PA_OK)
case('F8-tamper-and-rewrite-sha', f8, 'graded bytes edited, matching SHA256SUMS line rewritten')
# F8b duplicate SHA line: last line wins
def f8b(d):
    tgt='mteb-leaderboard/tests/test_outputs.py'; f=d/'corpus/evidence/round52/graders'/tgt
    f.write_bytes(f.read_bytes()+b'\n# tampered 2\n'); new=hashlib.sha256(f.read_bytes()).hexdigest()
    s=d/'corpus/evidence/round52/graders/SHA256SUMS'; s.write_text(s.read_text()+f'{new}  ./{tgt}\n')
    conf(d,VALID); pa(d,PA_OK)
case('F8b-duplicate-sha-line', f8b, 'original SHA line left stale; appended duplicate line carries new digest')
# F9 A5 laundering via a non-population EXCLUDED entry
def f9(d):
    fake='made-up-task/tests/test_outputs.py'
    s=d/'corpus/evidence/round52/graders/SHA256SUMS'; s.write_text(s.read_text()+('ab'*32)+f'  ./{fake}\n')
    (d/'corpus/evidence/round52/graders/EXCLUDED.md').write_text(
      "Excluded path: `corpus/evidence/round52/graders/"+fake+"`\nsha256: `"+('ab'*32)+"`\n")
    conf(d,VALID); pa(d,PA_OK)
case('F9-A5-fake-exclusion', f9, 'EXCLUDED.md names a non-population absent path with a self-written digest; sanitize still absent, no exclusion of it')
# F10 labels silently dropped
def f10(d):
    rows=[{"task":"mteb-leaderboard","class":"V3"},{"task":"multi-source-data-merger","class":"V3"},{"task":"password-recovery","class":"P1"},{"task":"password-recovery","class":"P1"},{"task":"mteb-leaderboard","class":"V3"}]
    (d/'corpus/evidence/round52/labels.json').write_text(json.dumps(rows))
case('F10-labels-drop', f10, 'two rows with out-of-vocabulary label, one duplicate row')

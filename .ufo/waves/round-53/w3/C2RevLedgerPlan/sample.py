import concurrent.futures, json, os, pathlib, re, subprocess, time
root=pathlib.Path('/fast/scratch/hyaku/kengaku-r53/C2RevLedgerPlan')
lane=root/'lane'
out=pathlib.Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/C2RevLedgerPlan')
rows=json.loads((lane/'plans/round53-tipstate.json').read_text())['rows']
reds=['adoption-check','anchor-digest-check','round28-census','round46-c3','state-assertion-check']
greens=['attrib-probe','benchmark-spec-audit','catalog-probe','config-projection','hermetic-grader']
def run(name):
 d=root/name
 subprocess.run(['git','clone','-q','--shared',str(lane),str(d)],check=True)
 top=subprocess.check_output(['git','-C',str(d),'rev-parse','--show-toplevel'],text=True).strip()
 assert top==str(d)
 tmp=root/('tmp-'+name);tmp.mkdir()
 env={k:v for k,v in os.environ.items() if not re.search(r'TOKEN|KEY|SECRET|PASSWORD|^OP_|SSH_AUTH_SOCK|COOKIE',k,re.I)}
 env['TMPDIR']=str(tmp)
 argv=rows[name]['argv'];t=time.monotonic()
 try:
  p=subprocess.run(argv,cwd=d,env=env,capture_output=True,text=True,timeout=900)
  rc=p.returncode; output=p.stdout+p.stderr
 except subprocess.TimeoutExpired:
  rc='TIMEOUT';output='sampling timeout'
 assert len(output.encode())<=1048576
 (out/(name+'.txt')).write_text(output)
 return {'row':name,'argv':argv,'cwd':str(d),'exit':rc,'declared_exit':rows[name]['exit'],'evidence_present':rows[name].get('evidence','') in output,'seconds':round(time.monotonic()-t,2)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 result=list(pool.map(run,reds+greens))
(out/'sample-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
from collections import defaultdict
fragments=defaultdict(list)
for name,row in rows.items():
 if 'evidence' in row: fragments[row['evidence']].append(name)
print('DUPLICATE_FRAGMENTS',json.dumps({k:v for k,v in fragments.items() if len(v)>1}))
print('RED_WORD_COUNTS',json.dumps({n:len(r['reason'].split()) for n,r in rows.items() if r['state']=='red'}))
print('CROSS_SAMPLE_FRAGMENTS',json.dumps({n:[other for other in reds+greens if other!=n and r['evidence'] in (out/(other+'.txt')).read_text()] for n,r in rows.items() if 'evidence' in r}))

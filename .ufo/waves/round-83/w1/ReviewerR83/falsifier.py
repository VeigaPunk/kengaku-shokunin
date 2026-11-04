import ast, hashlib, json, os, pathlib, subprocess, sys
L=pathlib.Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
S=pathlib.Path('/fast/scratch/hyaku/kengaku-r83/ReviewerR83')
O=L/'.ufo/waves/round-83/w1/ReviewerR83'
O.mkdir(parents=True,exist_ok=True)
os.environ['TMPDIR']=str(S/'tmp')
base='614f00559c75155ec100e945b3e8257b14fb7496'
freeze='6f076679931367d540c3897a4eafa0eca752e1d4'
rel='corpus/evidence/round52/graders/code-from-image/tests/test_outputs.py'
def blob(rev,path):
 return subprocess.run(['git','-C',str(L),'show',rev+':'+path],capture_output=True,check=True).stdout
subject=blob(base,rel); table=blob(freeze,'plans/round83-cases.json')
(S/'subject.py').write_bytes(subject)
names=[n.name for n in ast.parse(subject).body if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')]
runner='''import json,runpy,sys,traceback
try:
 ns=runpy.run_path('/subject.py')
except Exception as e:
 print(json.dumps({'phase':'setup','type':type(e).__name__}));sys.exit(2)
try:
 ns[sys.argv[1]]()
 print(json.dumps({'phase':'graded','outcome':'P','type':None}))
except (AssertionError,FileNotFoundError) as e:
 print(json.dumps({'phase':'graded','outcome':'F','type':type(e).__name__,'lines':[f.lineno for f in traceback.extract_tb(e.__traceback__) if f.filename=='/subject.py']}))
except Exception as e:
 print(json.dumps({'phase':'graded','outcome':'D','type':type(e).__name__}));sys.exit(2)
'''
(S/'runner.py').write_text(runner)
rows=[];host_before=pathlib.Path('/app').exists()
def run(app,name,subject_path=None):
 cmd=['bwrap','--unshare-all','--die-with-parent','--new-session','--ro-bind','/usr','/usr','--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64','--proc','/proc','--dev','/dev','--tmpfs','/tmp','--ro-bind',str(app),'/app','--ro-bind',str(subject_path or S/'subject.py'),'/subject.py','--ro-bind',str(S/'runner.py'),'/runner.py','--clearenv','--setenv','PATH','/usr/bin','--setenv','PYTHONDONTWRITEBYTECODE','1','--','/usr/bin/python3','-I','/runner.py',name]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=15)
 try:r=json.loads(p.stdout)
 except Exception:r={'phase':'launcher','stdout':p.stdout,'stderr':p.stderr}
 return {'argv':cmd,'rc':p.returncode,'result':r,'stderr':p.stderr}
for c in json.loads(table)['cases']:
 app=S/c['id'];app.mkdir()
 if c['content'] is not None:(app/'output.txt').write_bytes(c['content'].encode('utf-8'))
 legs=[run(app,n) for n in names]
 observed='/'.join(x['result'].get('outcome','D') for x in legs)
 rows.append({'id':c['id'],'predicted':c['predicted'],'observed':observed,'legs':legs})
 print('CASE',c['id'],'predicted='+c['predicted'],'observed='+observed)
# Additional adversarial fixtures, not additions to the frozen scoring table.
app=S/'permission-object';app.mkdir();(app/'output.txt').mkdir()
rows.append({'attack':'directory-output','expected':'P/D','legs':[run(app,n) for n in names]})
(S/'badsubject.py').write_text("raise FileNotFoundError('import/setup sentinel')\n")
rows.append({'attack':'setup-FileNotFoundError','expected_rc':2,'leg':run(app,names[0],S/'badsubject.py')})
result={'axes':['coverage','calibration'],'subject_sha256':hashlib.sha256(subject).hexdigest(),'table_sha256':hashlib.sha256(table).hexdigest(),'base':base,'freeze':freeze,'functions':names,'host_app_before':host_before,'host_app_after':pathlib.Path('/app').exists(),'frozen_cases':8,'mismatches':sum(x['predicted']!=x['observed'] for x in rows[:8]),'rows':rows}
(O/'independent-falsifiers.json').write_text(json.dumps(result,indent=2)+'\n')
(O/'falsifier.py').write_bytes(pathlib.Path(__file__).read_bytes())
print('SUMMARY mismatches='+str(result['mismatches'])+' host_app_before='+str(host_before)+' host_app_after='+str(result['host_app_after']))

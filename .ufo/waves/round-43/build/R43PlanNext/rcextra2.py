import os, sys, json, pathlib, shutil, subprocess, importlib.util, re, tempfile, concurrent.futures as cf
S=pathlib.Path(os.environ['S']); lane=S/'lane'
sys.path.insert(0,str(S)); import mut_harness as mh
C="/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
spec=importlib.util.spec_from_file_location('rcmod', str(lane/'plans/round_close.py')); rc=importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)
src,ms=mh.mutants(str(lane/'plans/round_close.py'),'round_close')
want={(m['line'],m['desc']) for m in ms}
W=S/'wrc2'; shutil.rmtree(W, ignore_errors=True); W.mkdir()
def fx(root, extra=None):
    root.mkdir(parents=True); rc.build_fixture(root, lane, "gate: P10 DEFECT receipt unreadable", 'receipt-last')
    if extra: extra(root)
    return str(root)
def git(r,*a): subprocess.run(['git','-C',str(r),'-c','user.name=f','-c','user.email=f@l',*a],check=True,capture_output=True)
# D1 foreign-round receipt named in claims
def foreign(r):
    (r/'corpus/evidence/round38').mkdir(parents=True); (r/'corpus/evidence/round38/zz-probe.txt').write_text("CASE c01 observed=PASS predicted=PASS\n")
    c=r/'plans/round-39-claims.md'; c.write_text(c.read_text()+"\nOld: `corpus/evidence/round38/zz-probe.txt`\n"); git(r,'add','-A'); git(r,'commit','-q','-m','foreign')
F1=fx(W/'d1'/'lane', foreign)
rc.FIXTURE_CLAIMS='# Round 39 — b-only\n\nRun log: `corpus/evidence/round39/git-leak-probe.txt`\n'
F4=fx(W/'d4'/'lane')
# D2 census only in cwd/scripts
(W/'d2cwd/scripts').mkdir(parents=True); shutil.copy(C, W/'d2cwd/scripts/sources-census.sh')
F2=fx(W/'d2'/'lane')
# D3 census in lane's parent
(W/'d3/scripts').mkdir(parents=True); shutil.copy(C, W/'d3/scripts/sources-census.sh'); F3=fx(W/'d3'/'lane')
ER=str(W/'d2cwd')
def mkwork():
    w=pathlib.Path(tempfile.mkdtemp(dir=W)); (w/'A-excused-p10').write_text('x'); t=w/'tgt'; t.mkdir(); (w/'B-executed-p10').symlink_to(t)
    (w/'C-receipt-first').symlink_to(w/'nonexistent'); d=w/'D-receipt-uncommitted'; d.mkdir(); (d/'junk').write_text('j'); return str(w)
FIL=W/'afile'
class D:
    def __init__(s,n,args,env=None,cwd=None,work=False): s.n=n;s.args=args;s.env=env or {};s.cwd=cwd;s.work=work
dets=[D('only-evidence-path-claims',['--lane',F4,'--round','39','--census',C]),D('foreign-round-receipt',['--lane',F1,'--round','39','--census',C]),
 D('census-from-cwd',['--lane',F2,'--round','39'],cwd=str(W/'d2cwd')),
 D('census-lane-parent',['--lane',F3,'--round','39']),
 D('selftest-preseeded-work',['--lane',str(lane),'--census',C,'--selftest'],work=True),
 D('selftest-reused-work-twice',['--lane',str(lane),'--census',C,'--selftest'],work='twice')]
def norm(s): return re.sub(r'/fast/scratch/\S*|/tmp/\S*|\d+\.\d+s|round-close-selftest-\S*','<p>',s)
def run(pyfile,d):
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',**d.env); env.pop('SHOKUNIN_ROOT',None) if 'SHOKUNIN_ROOT' not in d.env else None
    args=list(d.args)
    if d.work:
        w=mkwork(); args+=['--work',w]
        if d.work=='twice':
            subprocess.run(['python3',pyfile,*args],capture_output=True,env=env,timeout=120)
    try:
        p=subprocess.run(['python3',pyfile,*args],capture_output=True,text=True,env=env,cwd=d.cwd,timeout=120)
        return (p.returncode,norm(p.stdout+p.stderr))
    except subprocess.TimeoutExpired: return ('TIMEOUT','')
refp=str(lane/'plans/round_close.py')
ref=[run(refp,d) for d in dets]; ref2=[run(refp,d) for d in dets]
print('REF-STABLE',ref==ref2)
for d,r in zip(dets,ref): print('REF',d.n,r[0],r[1].strip().split('\n')[-1][:90])
def job(i):
    m=ms[i]; dd=W/f'm{i}'; dd.mkdir(); f=dd/'round_close.py'; f.write_bytes(src[:m['a']]+m['new']+src[m['b']:])
    k=[f"{d.n}:{r0[0]}>{r[0]}" for d,r0 in zip(dets,ref) for r in [run(str(f),d)] if r!=r0]
    shutil.rmtree(dd); return i,k
res=json.load(open(S/'rc_now2.json'))
cand=[i for i,m in enumerate(ms) if m['line']==122]+[i for i,m in enumerate(ms) if any(o['line']==m['line'] and o['desc']==m['desc'] and o['status'] in('survived','witnessed') for o in res)]
with cf.ThreadPoolExecutor(10) as ex:
    for i,k in ex.map(job,cand):
        o=[o for o in res if o['line']==ms[i]['line'] and o['desc']==ms[i]['desc']][0]
        print(ms[i]['line'],ms[i]['desc'],o['status'],'| extra:',k)

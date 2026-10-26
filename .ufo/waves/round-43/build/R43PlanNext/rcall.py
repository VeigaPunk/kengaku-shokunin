import os, sys, json, pathlib, shutil, subprocess, importlib.util, re, concurrent.futures as cf
S=pathlib.Path(os.environ['S']); lane=S/'lane'
sys.path.insert(0,str(S)); import mut_harness as mh
C="/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
spec=importlib.util.spec_from_file_location('rcmod', str(lane/'plans/round_close.py')); rc=importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)
src,ms=mh.mutants(str(lane/'plans/round_close.py'),'round_close')
W=S/'wrc'; shutil.rmtree(W, ignore_errors=True); W.mkdir()
def fx(name, shape='receipt-last', mod=None):
    r=W/name; r.mkdir(); rc.build_fixture(r, lane, "gate: P10 DEFECT receipt unreadable", shape)
    if mod: mod(r)
    return str(r)
F_ok=fx('ok')
F_norecdisk=fx('rec-deleted-on-disk', mod=lambda r:(r/'corpus/evidence/round39/git-leak-probe.txt').unlink())
F_noorder=fx('no-order-tool', mod=lambda r:(r/'plans/order_check.py').unlink())
F_nosrc=fx('no-sources', mod=lambda r:(r/'corpus/SOURCES.md').unlink())
EMPTY=W/'emptydir'; EMPTY.mkdir(); FILE=W/'afile'; FILE.write_text('x')
L=str(lane)
LIVE=[('live-r40',['--lane',L,'--round','40','--census',C],{}),('live-r41',['--lane',L,'--round','41','--census',C],{}),('live-r39',['--lane',L,'--round','39','--census',C],{}),('live-r99',['--lane',L,'--round','99','--census',C],{}),('live-noround',['--lane',L,'--census',C],{}),('live-census-missing',['--lane',L,'--round','40','--census','/nonexistent/c.sh'],{}),('live-lane-subdir',['--lane',L+'/plans','--round','40','--census',C],{}),('live-lane-notgit',['--lane',str(W),'--round','40','--census',C],{}),('live-r43',['--lane',L,'--round','43','--census',C],{})]
DETS=[('standing-selftest',['--lane',str(lane),'--census',C,'--selftest'],{}),
 ('selftest-no-census',  ['--lane',str(lane),'--census','/nonexistent/c.sh','--selftest'], {}),
 ('selftest-empty-lane', ['--lane',str(EMPTY),'--census',C,'--selftest'], {}),
 ('gate-ok-r39',         ['--lane',F_ok,'--round','39','--census',C], {}),
 ('gate-receipt-deleted',['--lane',F_norecdisk,'--round','39','--census',C], {}),
 ('gate-no-order-tool',  ['--lane',F_noorder,'--round','39','--census',C], {}),
 ('gate-no-sources',     ['--lane',F_nosrc,'--round','39','--census',C], {}),
 ('gate-lane-is-file',   ['--lane',str(FILE),'--round','39','--census',C], {}),
 ('gate-env-root',       ['--lane',F_ok,'--round','39'], {'SHOKUNIN_ROOT':'/home/vgpnk/Projects/shokunin'}),
 ('gate-census-dir',     ['--lane',F_ok,'--round','39','--census',str(EMPTY)], {})]+LIVE

import tempfile
def fx2(root, extra=None):
    root.mkdir(parents=True); rc.build_fixture(root, lane, "gate: P10 DEFECT receipt unreadable", 'receipt-last')
    if extra: extra(root)
    return str(root)
def git(r,*a): subprocess.run(['git','-C',str(r),'-c','user.name=f','-c','user.email=f@l',*a],check=True,capture_output=True)
# D1 foreign-round receipt named in claims
def foreign(r):
    (r/'corpus/evidence/round38').mkdir(parents=True); (r/'corpus/evidence/round38/zz-probe.txt').write_text("CASE c01 observed=PASS predicted=PASS\n")
    c=r/'plans/round-39-claims.md'; c.write_text(c.read_text()+"\nOld: `corpus/evidence/round38/zz-probe.txt`\n"); git(r,'add','-A'); git(r,'commit','-q','-m','foreign')
F1=fx2(W/'d1'/'lane', foreign)
rc.FIXTURE_CLAIMS='# Round 39 — b-only\n\nRun log: `corpus/evidence/round39/git-leak-probe.txt`\n'
F4=fx2(W/'d4'/'lane')
# D2 census only in cwd/scripts
(W/'d2cwd/scripts').mkdir(parents=True); shutil.copy(C, W/'d2cwd/scripts/sources-census.sh')
F2=fx2(W/'d2'/'lane')
# D3 census in lane's parent
(W/'d3/scripts').mkdir(parents=True); shutil.copy(C, W/'d3/scripts/sources-census.sh'); F3=fx2(W/'d3'/'lane')
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
def run(pyfile,args,env):
    try:
        p=subprocess.run(['python3',pyfile,*args],capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',**env),timeout=120); return (p.returncode,norm(p.stdout+p.stderr))
    except subprocess.TimeoutExpired: return ('TIMEOUT','')
def runx(pyfile,d):
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',**d.env)
    if 'SHOKUNIN_ROOT' not in d.env: env.pop('SHOKUNIN_ROOT',None)
    args=list(d.args)
    if d.work:
        w=mkwork(); args+=['--work',w]
        if d.work=='twice': subprocess.run(['python3',pyfile,*args],capture_output=True,env=env,timeout=120)
    try:
        p=subprocess.run(['python3',pyfile,*args],capture_output=True,text=True,env=env,cwd=d.cwd,timeout=120); return (p.returncode,norm(p.stdout+p.stderr))
    except subprocess.TimeoutExpired: return ('TIMEOUT','')
ALL=[D(n,a,e) for n,a,e in DETS[1:]]+dets   # DETS[0] = standing selftest (kept apart)
refp=str(lane/'plans/round_close.py')
STAND=DETS[0]
def runstand(f): return run(str(f),STAND[1],STAND[2])
ref_s=run(refp,STAND[1],STAND[2]); ref=[runx(refp,d) for d in ALL]
ref2=[runx(refp,d) for d in ALL]; print('REF-STABLE',ref==ref2)
def job(i):
    m=ms[i]; dd=W/f'x{i}'; dd.mkdir(); f=dd/'round_close.py'; f.write_bytes(src[:m['a']]+m['new']+src[m['b']:])
    st=run(str(f),STAND[1],STAND[2])!=ref_s
    k=[] if st else [f"{d.n}:{r0[0]}>{r[0]}" for d,r0 in zip(ALL,ref) for r in [runx(str(f),d)] if r!=r0]
    shutil.rmtree(dd); return i,st,k
out=[]
with cf.ThreadPoolExecutor(10) as ex:
    for i,st,k in ex.map(job,range(len(ms))):
        out.append(dict(line=ms[i]['line'],desc=ms[i]['desc'],selftest_kills=st,killers=k))
json.dump(out,open(S/'rc_all.json','w'),indent=1)
from collections import Counter
print('POP',len(ms),'selftest-killed',sum(o['selftest_kills'] for o in out),'selftest-survivors',sum(not o['selftest_kills'] for o in out))
for o in sorted(out,key=lambda o:(o['line'],o['desc'])):
    if not o['selftest_kills']: print(o['line'],o['desc'],'|',o['killers'] or 'UNWITNESSED')

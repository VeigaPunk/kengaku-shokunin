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
def norm(s): return re.sub(r'/fast/scratch/\S*|/tmp/\S*|\d+\.\d+s|round-close-selftest-\S*','<p>',s)
def run(pyfile,args,env):
    try:
        p=subprocess.run(['python3',pyfile,*args],capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',**env),timeout=120)
        return (p.returncode,norm(p.stdout+p.stderr))
    except subprocess.TimeoutExpired: return ('TIMEOUT','')
ref=[run(str(lane/'plans/round_close.py'),a,e) for _,a,e in DETS]
ref2=[run(str(lane/'plans/round_close.py'),a,e) for _,a,e in DETS]
print('REF-STABLE',ref==ref2)
for (n,_,_),r in zip(DETS,ref): print('REF',n,r[0],r[1].strip().split('\n')[-1][:80])
def job(i):
    m=ms[i]; d=W/f'm{i}'; d.mkdir(); f=d/'round_close.py'; new=src[:m['a']]+m['new']+src[m['b']:]
    f.write_bytes(new)
    try: compile(new.decode(),str(f),'exec')
    except SyntaxError: return i,'invalid',[]
    k=[]
    for j,((n,a,e),r0) in enumerate(zip(DETS,ref)):
        r=run(str(f),a,e)
        if r!=r0: k.append(f"{n}:{r0[0]}>{r[0]}")
    shutil.rmtree(d); return i,'x',k
out=[]
with cf.ThreadPoolExecutor(12) as ex:
    for i,st,k in ex.map(job,range(len(ms))):
        m=ms[i]; stand=any(x.startswith(('standing','live')) for x in k); wit=[x for x in k if not x.startswith(('standing','live'))]
        out.append(dict(line=m['line'],kind=m['kind'],desc=m['desc'],status='invalid' if st=='invalid' else ('killed-standing' if stand else ('witnessed' if wit else 'survived')),wit=wit))
json.dump(out,open(S/'rc_now2.json','w'),indent=1)
from collections import Counter
print('POP',len(ms),Counter(o['status'] for o in out))
for o in out:
    if o['status'] in('witnessed','survived'): print(o['line'],o['desc'],o['status'],o['wit'])

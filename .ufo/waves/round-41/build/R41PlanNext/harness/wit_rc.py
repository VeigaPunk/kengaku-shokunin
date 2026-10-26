import os, json, pathlib, shutil, subprocess, importlib.util, sys
S=pathlib.Path('/fast/scratch/hyaku/kengaku-r41/R41PlanNext'); lane=S/'lane'
C="/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
spec=importlib.util.spec_from_file_location('rcmod', str(lane/'plans/round_close.py')); rc=importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)
src=(lane/'plans/round_close.py').read_bytes()
res=json.load(open(S/'res_round_close.json'))
surv=[m for m in res['mutants'] if m['status']=='survived']
W=S/'wrc'; shutil.rmtree(W, ignore_errors=True); W.mkdir()
def fx(name, shape='receipt-last', mod=None):
    r=W/name; r.mkdir(); rc.build_fixture(r, lane, "gate: P10 DEFECT receipt unreadable", shape)
    if mod: mod(r)
    return str(r)
F_ok=fx('ok')
F_norecdisk=fx('rec-deleted-on-disk', mod=lambda r:(r/'corpus/evidence/round39/git-leak-probe.txt').unlink())
F_noorder=fx('no-order-tool', mod=lambda r:(r/'plans/order_check.py').unlink())
F_nosrc=fx('no-sources', mod=lambda r:(r/'corpus/SOURCES.md').unlink())
EMPTY=W/'emptydir'; EMPTY.mkdir()
FILE=W/'afile'; FILE.write_text('x')
DETS=[
 ('selftest-no-census',  ['--lane',str(lane),'--census','/nonexistent/c.sh','--selftest'], {}),
 ('selftest-empty-lane', ['--lane',str(EMPTY),'--census',C,'--selftest'], {}),
 ('gate-ok-r39',         ['--lane',F_ok,'--round','39','--census',C], {}),
 ('gate-receipt-deleted',['--lane',F_norecdisk,'--round','39','--census',C], {}),
 ('gate-no-order-tool',  ['--lane',F_noorder,'--round','39','--census',C], {}),
 ('gate-no-sources',     ['--lane',F_nosrc,'--round','39','--census',C], {}),
 ('gate-lane-is-file',   ['--lane',str(FILE),'--round','39','--census',C], {}),
 ('gate-env-root',       ['--lane',F_ok,'--round','39'], {'SHOKUNIN_ROOT':'/home/vgpnk/Projects/shokunin'}),
 ('gate-census-dir',     ['--lane',F_ok,'--round','39','--census',str(EMPTY)], {}),
]
def norm(s): 
    import re; return re.sub(r'/fast/scratch/\S*|\d+\.\d+s','<p>',s)
def run(pyfile, args, env):
    p=subprocess.run(['python3',pyfile,*args],capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',**env),timeout=120)
    return (p.returncode, norm(p.stdout+p.stderr))
ref=[run(str(lane/'plans/round_close.py'),a,e) for _,a,e in DETS]
for (n,_,_),r in zip(DETS,ref): print('REF',n,r[0],r[1].strip().split('\n')[-1][:90])
md=W/'m.py'
for m in surv:
    new=src[:m['a']]+m['new'].encode()+src[m['b']:]; md.write_bytes(new)
    kills=[]
    for (n,a,e),r0 in zip(DETS,ref):
        r=run(str(md),a,e)
        if r!=r0: kills.append(f"{n}:{r0[0]}>{r[0]}")
    print(m['line'],m['desc'], kills or 'UNWITNESSED')

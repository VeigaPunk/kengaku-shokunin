import importlib.util, json, os, shutil, subprocess, sys, time
from pathlib import Path
LANE=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
spec=importlib.util.spec_from_file_location('c2', LANE/'plans/round53_c2_tipstate.py')
c2=importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
root=Path('/fast/scratch/hyaku/kengaku-r53/C2RevCounter/t/w4'); shutil.rmtree(root, ignore_errors=True); root.mkdir(parents=True)

print("=== TEST I: source HEAD detached on a commit NOT on the default branch ===")
d=root/'I'; d.mkdir()
subprocess.run(['git','-C',str(d),'init','-q','-b','main'],check=True)
(d/'f.txt').write_text('v1'); subprocess.run(['git','-C',str(d),'add','-A'],check=True)
subprocess.run(['git','-C',str(d),'-c','user.email=a@b','-c','user.name=a','commit','-qm','one'],check=True)
c1=subprocess.run(['git','-C',str(d),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
(d/'f.txt').write_text('v2'); subprocess.run(['git','-C',str(d),'add','-A'],check=True)
subprocess.run(['git','-C',str(d),'-c','user.email=a@b','-c','user.name=a','commit','-qm','two'],check=True)
c2sha=subprocess.run(['git','-C',str(d),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
subprocess.run(['git','-C',str(d),'checkout','-q','--detach',c1],check=True)
print("source HEAD (detached) =", c1[:8], " main/branch tip =", c2sha[:8])
w=c2.Worker(d, root/'I_work', 0)
wh=subprocess.run(['git','-C',str(w.dir),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
print("worker clone HEAD =", wh[:8], " == source HEAD?", wh==c1, " == branch tip?", wh==c2sha)
print("worker clone f.txt content:", (w.dir/'f.txt').read_text())

print()
print("=== TEST J: git clean -fdx vs -ffdx on a nested repo ===")
d2=root/'J'; d2.mkdir()
subprocess.run(['git','-C',str(d2),'init','-q'],check=True)
(d2/'nested').mkdir(); subprocess.run(['git','-C',str(d2/'nested'),'init','-q'],check=True)
(d2/'plain.txt').write_text('x')
r=subprocess.run(['git','-C',str(d2),'clean','-q','-fdx'],capture_output=True,text=True)
print("clean -fdx rc=",r.returncode,"stderr:",r.stderr.strip()[:120])
print("  nested repo survives:", (d2/'nested'/'.git').exists(), " plain file survives:", (d2/'plain.txt').exists())
(d2/'nested2').mkdir(); subprocess.run(['git','-C',str(d2/'nested2'),'init','-q'],check=True)
r=subprocess.run(['git','-C',str(d2),'clean','-q','-ffdx'],capture_output=True,text=True)
print("clean -ffdx rc=",r.returncode,"stderr:",r.stderr.strip()[:120])
print("  nested2 repo survives:", (d2/'nested2'/'.git').exists())

print()
print("=== TEST K: git gc inside a --shared clone: does the SOURCE lose objects? ===")
d3=root/'K_src'; d3.mkdir()
subprocess.run(['git','-C',str(d3),'init','-q','-b','main'],check=True)
(d3/'f.txt').write_text('v1'); subprocess.run(['git','-C',str(d3),'add','-A'],check=True)
subprocess.run(['git','-C',str(d3),'-c','user.email=a@b','-c','user.name=a','commit','-qm','one'],check=True)
sha=subprocess.run(['git','-C',str(d3),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
clone=root/'K_clone'
subprocess.run(['git','clone','-q','--shared',str(d3),str(clone)],check=True)
print("source object still present before gc:", subprocess.run(['git','-C',str(d3),'cat-file','-e',sha],capture_output=True).returncode==0)
subprocess.run(['git','-C',str(clone),'gc','-q','--prune=now'],capture_output=True)
print("source object present AFTER gc in the shared clone:", subprocess.run(['git','-C',str(d3),'cat-file','-e',sha],capture_output=True).returncode==0)

print()
print("=== TEST L: non-int timeout_s in the ledger -> crash or graceful? ===")
def mk(root, rows, ledger_over=None):
    (root/'plans').mkdir(parents=True, exist_ok=True)
    table=["## Gate/probe registry","","| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |","|---|---|---|---|---|---|---|---|"]
    ledger={"schema":c2.SCHEMA,"base":"probe","rows":{}}
    for n,(body,ex,ev) in rows.items():
        (root/'plans'/f'{n}.py').write_text(body)
        table.append(f"| `{n}` | gate | `python3 plans/{n}.py` | `0` ok | none | none | none | kengaku |")
        e={"argv":["python3",f"plans/{n}.py"],"exit":ex,"state":"green" if ex==0 else "red","kind":"entry"}
        if ex!=0: e["evidence"]=ev; e["reason"]="a probe reason long enough to pass the ten word minimum requirement here"
        ledger["rows"][n]=e
    (root/'SKILL.md').write_text("\n".join(table)+"\n")
    if ledger_over: ledger_over(ledger)
    (root/'plans'/c2.LEDGER.split('/')[-1]).write_text(json.dumps(ledger))
G=("import sys\nprint('ok')\nsys.exit(0)\n",0,None)
lane=root/'L'; lane.mkdir(); mk(lane,{'a':G}, ledger_over=lambda l: l["rows"]["a"].update({"timeout_s":"soon"}))
try:
    rc,lines=c2.evaluate(lane, lane, root/'L_work', 1, 30, None, False)
    print("rc=",rc); print("\n".join(lines))
except Exception as e:
    print("EXCEPTION:", type(e).__name__, e)

print()
print("=== TEST M: jobs=4, two rows writing the SAME file in their separate clones ===")
W=("import os,sys\nopen('same.txt','w').write('x')\nprint('ok')\nsys.exit(0)\n",0,None)
lane2=root/'M'; lane2.mkdir(); mk(lane2,{'a':W,'b':W})
rc,lines=c2.evaluate(lane2, lane2, root/'M_work', 4, 30, None, False)
print("rc=",rc)
print("  (isolation: each worker has its own clone dir under work/w<i>/src)")

import importlib.util, json, os, shutil, subprocess, sys
from pathlib import Path
LANE=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
spec=importlib.util.spec_from_file_location('c2', LANE/'plans/round53_c2_tipstate.py')
c2=importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
root=Path('/fast/scratch/hyaku/kengaku-r53/C2RevCounter/t/w3'); shutil.rmtree(root, ignore_errors=True); root.mkdir(parents=True)
def G(): return ("import sys\nprint('ok')\nsys.exit(0)\n",0,None)

def mk(root, rows, git=False, ledger_over=None):
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
    if git:
        subprocess.run(['git','-C',str(root),'init','-q','-b','main'],check=True)
        subprocess.run(['git','-C',str(root),'add','-A'],check=True)
        subprocess.run(['git','-C',str(root),'-c','user.email=a@b','-c','user.name=a','commit','-qm','x'],check=True)
    return ledger

print("=== TEST F: detached-HEAD source -> does the worker clone track the source HEAD? ===")
lane=root/'F'; lane.mkdir(); mk(lane,{'a':G()}, git=True)
# make a second commit and check out the first commit detached (simulating a pinned tip)
subprocess.run(['git','-C',str(lane),'checkout','-q','--detach','HEAD'],check=True)
head=subprocess.run(['git','-C',str(lane),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
(lane/'plans'/'a.py').write_text("import sys\nprint('SECOND-COMMIT')\nsys.exit(0)\n")
subprocess.run(['git','-C',str(lane),'add','-A'],check=True)
subprocess.run(['git','-C',str(lane),'-c','user.email=a@b','-c','user.name=a','commit','-qm','y'],check=True)
subprocess.run(['git','-C',str(lane),'checkout','-q','--detach',head],check=True)
print("source HEAD:", head[:8], " status:", repr(subprocess.run(['git','-C',str(lane),'status','--porcelain'],capture_output=True,text=True).stdout))
w=c2.Worker(lane, root/'F_work', 0)
print("worker clone HEAD:", subprocess.run(['git','-C',str(w.dir),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()[:8])
print("worker clone HEAD == source HEAD?", subprocess.run(['git','-C',str(w.dir),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()==head)
print("worker clone a.py content first line:", (w.dir/'plans'/'a.py').read_text().splitlines()[1])

print()
print("=== TEST G: argv with ABSOLUTE lane path escapes the scratch clone ===")
lane2=root/'G_lane'; lane2.mkdir(); mk(lane2,{'a':("import sys,os\nopen(os.path.join(os.path.dirname(__file__),'..','MARKER_ESCAPED.txt'),'w').write('x')\nprint('ok')\nsys.exit(0)\n",0,None)}, git=True)
src=root/'G_src'
subprocess.run(['git','clone','-q','--shared',str(lane2),str(src)],check=True)
def over(l): l["rows"]["a"]["argv"]=["python3",str(lane2/'plans'/'a.py')]
mk(lane2,{'a':G()}, ledger_over=over)  # rewrite ledger with absolute argv
rc,lines=c2.evaluate(lane2, src, root/'G_work', 1, 30, None, False)
print("rc=",rc)
print("marker written into the LANE (escaped the clone)?", (lane2/'MARKER_ESCAPED.txt').exists())
print("marker written into the clone?", (src/'MARKER_ESCAPED.txt').exists())

print()
print("=== TEST H: does 'git clean -ffdx' remove a nested repo that 'clean -fdx' keeps? ===")
d=root/'H'; d.mkdir()
subprocess.run(['git','-C',str(d),'init','-q'],check=True)
subprocess.run(['git','-C',str(d/'nested'),'init','-q'],check=True)
(d/'plain.txt').write_text('x')
subprocess.run(['git','-C',str(d),'clean','-q','-fdx'],check=True)
print("after clean -fdx: nested repo exists:", (d/'nested'/'.git').exists(), " plain file exists:", (d/'plain.txt').exists())
subprocess.run(['git','-C',str(d),'init','-q','nested2'],check=True)
(d/'plain2.txt').write_text('x')
subprocess.run(['git','-C',str(d),'clean','-q','-ffdx'],check=True)
print("after clean -ffdx: nested2 repo exists:", (d/'nested2'/'.git').exists(), " plain2 file exists:", (d/'plain2.txt').exists())

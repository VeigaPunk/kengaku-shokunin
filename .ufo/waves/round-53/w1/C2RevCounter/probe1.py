import importlib.util, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
LANE=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
spec=importlib.util.spec_from_file_location('c2', LANE/'plans/round53_c2_tipstate.py')
c2=importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)

root=Path('/fast/scratch/hyaku/kengaku-r53/C2RevCounter/t/w1'); shutil.rmtree(root, ignore_errors=True); root.mkdir(parents=True)

def mk(root, rows, git=False):
    (root/'plans').mkdir(parents=True, exist_ok=True)
    table=["## Gate/probe registry","","| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |","|---|---|---|---|---|---|---|---|"]
    ledger={"schema":c2.SCHEMA,"base":"probe","rows":{}}
    for n,(body,ex,ev) in rows.items():
        (root/'plans'/f'{n}.py').write_text(body)
        table.append(f"| `{n}` | gate | `python3 plans/{n}.py` | `0` ok | none | none | none | kengaku |")
        e={"argv":["python3",f"plans/{n}.py"],"exit":ex,"state":"green" if ex==0 else "red","kind":"entry"}
        if ex!=0:
            e["evidence"]=ev; e["reason"]="a probe reason long enough to pass the ten word minimum requirement here"
        ledger["rows"][n]=e
    (root/'SKILL.md').write_text("\n".join(table)+"\n")
    (root/'plans'/c2.LEDGER.split('/')[-1]).write_text(json.dumps(ledger))
    if git:
        subprocess.run(['git','-C',str(root),'init','-q'],check=True)
        subprocess.run(['git','-C',str(root),'add','-A'],check=True)
        subprocess.run(['git','-C',str(root),'-c','user.email=a@b','-c','user.name=a','commit','-qm','x'],check=True)
    return ledger

G=("import sys\nprint('ok')\nsys.exit(0)\n",0,None)
R=("import sys\nprint('DEFECT x')\nsys.exit(1)\n",1,"DEFECT x")

print("=== TEST A: non-git source (no .git) -> clean=None accepted, reset no-op ===")
lane=root/'A_lane'; lane.mkdir()
mk(lane,{'a':G,'b':R})
# b writes a marker file; if reset is a no-op the marker survives into the next row on the same worker
stateful=("import os,sys\nopen('MARKER.txt','w').write('x')\nprint('ok')\nsys.exit(0)\n",0,None)
lane2=root/'A_lane2'; lane2.mkdir(); mk(lane2,{'a':stateful,'b':stateful})
rc,lines=c2.evaluate(lane2, lane2, root/'A_work', 1, 30, None, False)
print("rc=",rc); print("\n".join(lines))
print("source has .git?", (lane2/'.git').exists())

print()
print("=== TEST A2: git source, untracked+ignored file left by row 1 seen by row 2? ===")
lane3=root/'A_lane3'; lane3.mkdir(); mk(lane3,{'a':stateful,'b':stateful}, git=True)
(lane3/'ignored.txt').write_text('x')
(lane3/'.gitignore').write_text('ignored.txt\n')
subprocess.run(['git','-C',str(lane3),'add','-A'],check=True)
subprocess.run(['git','-C',str(lane3),'-c','user.email=a@b','-c','user.name=a','commit','-qm','y'],check=True)
rc,lines=c2.evaluate(lane3, lane3, root/'A_work3', 1, 30, None, False)
print("rc=",rc); print("\n".join(lines))

import importlib.util, json, os, shutil, subprocess, sys
from pathlib import Path
LANE=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
spec=importlib.util.spec_from_file_location('c2', LANE/'plans/round53_c2_tipstate.py')
c2=importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
root=Path('/fast/scratch/hyaku/kengaku-r53/C2RevCounter/t/w2'); shutil.rmtree(root, ignore_errors=True); root.mkdir(parents=True)

def mk(root, rows, git=False, ledger_over=None):
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
    if ledger_over: ledger_over(ledger)
    (root/'plans'/c2.LEDGER.split('/')[-1]).write_text(json.dumps(ledger))
    if git:
        subprocess.run(['git','-C',str(root),'init','-q'],check=True)
        subprocess.run(['git','-C',str(root),'add','-A'],check=True)
        subprocess.run(['git','-C',str(root),'-c','user.email=a@b','-c','user.name=a','commit','-qm','x'],check=True)
    return ledger

print("=== TEST B: red row with evidence key ABSENT -> crash or graceful? ===")
R=("import sys\nprint('DEFECT x')\nsys.exit(1)\n",1,"DEFECT x")
def drop_ev(l): del l["rows"]["b"]["evidence"]
lane=root/'B'; lane.mkdir(); mk(lane,{'a':("import sys\nprint('ok')\nsys.exit(0)\n",0,None),'b':R}, ledger_over=drop_ev)
try:
    rc,lines=c2.evaluate(lane, lane, root/'B_work', 1, 30, None, False)
    print("rc=",rc); print("\n".join(lines))
except Exception as e:
    print("EXCEPTION:", type(e).__name__, e)

print()
print("=== TEST C: non-git source, jobs=1, does row 2 see row 1's file? ===")
MARK=("import os,sys\nopen('MARKER.txt','w').write('x')\nprint('ok')\nsys.exit(0)\n",0,None)
lane2=root/'C'; lane2.mkdir(); mk(lane2,{'a':MARK,'b':MARK})
rc,lines=c2.evaluate(lane2, lane2, root/'C_work', 1, 30, None, False)
print("rc=",rc)
# inspect the worker clone that was removed; rerun manually to observe
w=c2.Worker(lane2, root/'C_work2', 0)
c2.run_row(w,'a',{"argv":["python3","plans/a.py"],"exit":0},30,root/'C_work2')
print("after row a, MARKER present in clone:", (w.dir/'MARKER.txt').exists())
c2.run_row(w,'b',{"argv":["python3","plans/b.py"],"exit":0},30,root/'C_work2')
print("after row b (same worker), MARKER still present:", (w.dir/'MARKER.txt').exists())
print("worker.git =", w.git)

print()
print("=== TEST D: git source, nested git repo left by row 1, does clean -fdx remove it? ===")
lane3=root/'D'; lane3.mkdir(); mk(lane3,{'a':MARK,'b':MARK}, git=True)
w=c2.Worker(lane3, root/'D_work', 0)
c2.run_row(w,'a',{"argv":["python3","plans/a.py"],"exit":0},30,root/'D_work')
# simulate a row that creates a nested repo
subprocess.run(['git','-C',str(w.dir),'init','-q','nested'],check=True)
print("nested repo exists after creation:", (w.dir/'nested'/'.git').exists())
w.reset()
print("nested repo survives git clean -fdx + reset --hard:", (w.dir/'nested'/'.git').exists())
print("MARKER survives reset (untracked plain file):", (w.dir/'MARKER.txt').exists())

print()
print("=== TEST E: argv laundering with --help while declaring kind=entry ===")
HELP=("import sys\nif '--help' in sys.argv:\n    print('usage'); sys.exit(0)\nprint('DEFECT x')\nsys.exit(1)\n",1,"DEFECT x")
lane4=root/'E'; lane4.mkdir()
mk(lane4,{'a':HELP}, ledger_over=lambda l: l["rows"]["a"].update({"argv":["python3","plans/a.py","--help"],"exit":0,"state":"green","kind":"entry"}))
rc,lines=c2.evaluate(lane4, lane4, root/'E_work', 1, 30, None, False)
print("rc=",rc); print("\n".join(lines))

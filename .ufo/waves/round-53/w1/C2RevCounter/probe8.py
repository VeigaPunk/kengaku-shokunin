import importlib.util, json, os, shutil, subprocess, sys
from pathlib import Path
LANE=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
spec=importlib.util.spec_from_file_location('c2', LANE/'plans/round53_c2_tipstate.py')
c2=importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
root=Path('/fast/scratch/hyaku/kengaku-r53/C2RevCounter/t/w8'); shutil.rmtree(root, ignore_errors=True); root.mkdir(parents=True)
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

print("=== TEST W: does TMPDIR reach the child? ===")
lane=root/'W'; lane.mkdir()
body=("import os,sys\nprint('TMPDIR_SEEN=', os.environ.get('TMPDIR'))\nprint('EXISTS=', os.path.isdir(os.environ.get('TMPDIR','')))\nsys.exit(0)\n")
mk(lane,{'a':(body,0,None)})
w=c2.Worker(lane, root/'W_work', 0)
res=c2.run_row(w,'a',{"argv":["python3","plans/a.py"],"exit":0},30,root/'W_work')
print(res['out'].strip())
print(">>> tmp dir was under the work root and removed after the row:", not (root/'W_work'/'tmp-a').exists())

print()
print("=== TEST X: argv laundering -- `python3 --help <script>` : script token present, exit 0 ===")
HELPISH=("import sys\nprint('DEFECT x')\nsys.exit(1)\n",1,"DEFECT x")
lane2=root/'X'; lane2.mkdir()
mk(lane2,{'a':HELPISH}, ledger_over=lambda l: l["rows"]["a"].update({"argv":["python3","--help","plans/a.py"],"exit":0,"state":"green","kind":"entry"}))
rc,lines=c2.evaluate(lane2, lane2, root/'X_work', 1, 30, None, False)
print("rc=",rc); print("\n".join(lines))
print(">>> entry_mismatch did NOT fire (the script token is in argv) although the instrument was never run")

print()
print("=== TEST Y: `python3 plans/a.py --selftest` style flags are not constrained either ===")
lane3=root/'Y'; lane3.mkdir()
mk(lane3,{'a':HELPISH}, ledger_over=lambda l: l["rows"]["a"].update({"argv":["python3","plans/a.py","--nonexistent-flag"],"exit":0,"state":"green","kind":"entry"}))
rc,lines=c2.evaluate(lane3, lane3, root/'Y_work', 1, 30, None, False)
print("rc=",rc); print("\n".join(lines))

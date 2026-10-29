import importlib.util, json, shutil, subprocess, sys
from pathlib import Path
LANE=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
spec=importlib.util.spec_from_file_location('c2', LANE/'plans/round53_c2_tipstate.py')
c2=importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
root=Path('/fast/scratch/hyaku/kengaku-r53/C2RevCounter/t/w13'); shutil.rmtree(root, ignore_errors=True); root.mkdir(parents=True)
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
lane=root/'L'; lane.mkdir(); mk(lane,{'a':G,'b':G})
print("=== TEST AC: --dry --only on a GOOD ledger -> exit code and printed lines ===")
rc,lines=c2.evaluate(lane, lane, root/'L_work', 4, 30, {"a"}, True)
print("rc=",rc); print("\n".join(lines))
print(">>> exit 0 and NO 'PREDICATE' line: a harness keying on exit code alone reads this as a pass")
print()
print("=== TEST AD: --only (not dry) on a GOOD ledger ===")
rc,lines=c2.evaluate(lane, lane, root/'L_work', 4, 30, {"a"}, False)
print("rc=",rc); print("\n".join(lines))

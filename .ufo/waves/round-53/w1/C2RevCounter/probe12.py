import importlib.util, json, os, shutil, subprocess, time
from pathlib import Path
LANE=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
spec=importlib.util.spec_from_file_location('c2', LANE/'plans/round53_c2_tipstate.py')
c2=importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
root=Path('/fast/scratch/hyaku/kengaku-r53/C2RevCounter/t/w12'); shutil.rmtree(root, ignore_errors=True); root.mkdir(parents=True)
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

print("=== TEST Z: FALSE PASS via state leak (non-git source, jobs=1, row a leaves a marker) ===")
# row a writes MARKER; row b exits 0 ONLY if MARKER exists (clean tree -> b exits 1 -> b is really RED)
lane=root/'Z'; lane.mkdir(); mk(lane,{'a':G,'b':G})
(lane/'plans'/'a.py').write_text("open('MARKER','w').write('x')\nprint('ok')\n")
(lane/'plans'/'b.py').write_text("import os,sys\nprint('ok')\nsys.exit(0 if os.path.exists('MARKER') else 1)\n")
led=json.loads((lane/'plans'/c2.LEDGER.split('/')[-1]).read_text())
led["rows"]["b"].update({"exit":0,"state":"green","kind":"entry"}); led["rows"]["b"].pop("evidence",None); led["rows"]["b"].pop("reason",None)
(lane/'plans'/c2.LEDGER.split('/')[-1]).write_text(json.dumps(led))
rc,lines=c2.evaluate(lane, lane, root/'Z_work', 1, 30, None, False)
print("rc=",rc); print("\n".join(lines))
print(">>> b exits 1 in a CLEAN tree but the leaked MARKER makes it 0 -> counter:", "PASS (false green)" if rc==0 else "fail")

print()
print("=== TEST AA: ledger timeout_s OVERRIDES the CLI --timeout (the ledger controls its own budget) ===")
lane2=root/'AA'; lane2.mkdir()
HANG=("import time\ntime.sleep(30)\n",0,None)
mk(lane2,{'a':HANG}, ledger_over=lambda l: l["rows"]["a"].update({"timeout_s":6}))
t0=time.time(); rc,lines=c2.evaluate(lane2, lane2, root/'AA_work', 1, 1, None, False); el=time.time()-t0
print(f"rc={rc} elapsed={el:.1f}s with --timeout=1 but ledger timeout_s=6")
print("\n".join(lines))
print(">>> the CLI timeout is ignored for rows that declare their own timeout_s")

print()
print("=== TEST AB: same, without timeout_s -> the CLI timeout DOES apply ===")
lane3=root/'AB'; lane3.mkdir(); mk(lane3,{'a':HANG})
t0=time.time(); rc,lines=c2.evaluate(lane3, lane3, root/'AB_work', 1, 1, None, False); el=time.time()-t0
print(f"rc={rc} elapsed={el:.1f}s")
print("\n".join(lines))

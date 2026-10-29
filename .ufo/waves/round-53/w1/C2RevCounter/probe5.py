import importlib.util, json, os, shutil, subprocess, sys
from pathlib import Path
LANE=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
spec=importlib.util.spec_from_file_location('c2', LANE/'plans/round53_c2_tipstate.py')
c2=importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
root=Path('/fast/scratch/hyaku/kengaku-r53/C2RevCounter/t/w5'); shutil.rmtree(root, ignore_errors=True); root.mkdir(parents=True)

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

print("=== TEST N: ledger argv with an ABSOLUTE path to the live lane (script token still matches?) ===")
live=root/'N_live'; live.mkdir(); mk(live,{'a':G})
# make a DIFFERENT script live in the live lane; clone from a pristine copy
src=root/'N_src'
shutil.copytree(live, src)
subprocess.run(['git','-C',str(src),'init','-q','-b','main'],check=True)
subprocess.run(['git','-C',str(src),'add','-A'],check=True)
subprocess.run(['git','-C',str(src),'-c','user.email=a@b','-c','user.name=a','commit','-qm','x'],check=True)
# live lane's script now DIVERGES from the clone
(live/'plans'/'a.py').write_text("import sys\nprint('LIVE-LANE')\nsys.exit(0)\n")
def over(l): l["rows"]["a"]["argv"]=["python3",str(live/'plans'/'a.py')]
mk(live,{'a':G}, ledger_over=over)
rc,lines=c2.evaluate(live, src, root/'N_work', 1, 30, None, False)
print("rc=",rc); print("\n".join(lines))
print(">>> the executed script was the LIVE lane's file, not the clone's:", 'LIVE-LANE' if 'LIVE-LANE' in str(lines) else 'cannot tell from lines')

print()
print("=== TEST O: lane SKILL.md row dropped vs source SKILL.md -> predicate passes? ===")
lane=root/'O_lane'; lane.mkdir(); mk(lane,{'a':G,'b':G})
# drop row b from the LANE's registry only (source keeps both)
srcO=root/'O_src'; shutil.copytree(lane, srcO)
subprocess.run(['git','-C',str(srcO),'init','-q','-b','main'],check=True)
subprocess.run(['git','-C',str(srcO),'add','-A'],check=True)
subprocess.run(['git','-C',str(srcO),'-c','user.email=a@b','-c','user.name=a','commit','-qm','x'],check=True)
tbl=(lane/'SKILL.md').read_text().splitlines()
(lane/'SKILL.md').write_text("\n".join([l for l in tbl if '`b`' not in l])+"\n")
rc,lines=c2.evaluate(lane, srcO, root/'O_work', 1, 30, None, False)
print("rc=",rc); print("\n".join(lines))
print(">>> lane registry rows = 1 while the source tree has 2 rows; no digest check of SKILL.md lane-vs-source")

print()
print("=== TEST P: are IGNORED files removed by the worker's reset? ===")
d=root/'P'; d.mkdir()
subprocess.run(['git','-C',str(d),'init','-q'],check=True)
(d/'.gitignore').write_text('ign/\n')
(d/'ign').mkdir(); (d/'ign'/'x.txt').write_text('x')
(d/'keep.py').write_text('print(1)')
subprocess.run(['git','-C',str(d),'add','-A'],check=True)
subprocess.run(['git','-C',str(d),'-c','user.email=a@b','-c','user.name=a','commit','-qm','x'],check=True)
w=c2.Worker(d, root/'P_work', 0)
print("ignored file present in the clone after clone:", (w.dir/'ign'/'x.txt').exists())
w.reset()
print("ignored file present after Worker.reset:", (w.dir/'ign'/'x.txt').exists())

print()
print("=== TEST Q: help laundering -- a row whose REAL entry exits 1, declared green via --help argv ===")
HELP=("import sys\nif '--help' in sys.argv:\n    print('usage'); sys.exit(0)\nprint('DEFECT x')\nsys.exit(1)\n",1,"DEFECT x")
lane2=root/'Q'; lane2.mkdir()
mk(lane2,{'a':HELP}, ledger_over=lambda l: l["rows"]["a"].update({"argv":["python3","plans/a.py","--help"],"exit":0,"state":"green","kind":"entry"}))
rc,lines=c2.evaluate(lane2, lane2, root/'Q_work', 1, 30, None, False)
print("rc=",rc); print("\n".join(lines))
print(">>> real instrument exits 1 (red) but the counter sees green and passes")

import importlib.util, json, os, shutil, subprocess, sys
from pathlib import Path
LANE=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
spec=importlib.util.spec_from_file_location('c2', LANE/'plans/round53_c2_tipstate.py')
c2=importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
root=Path('/fast/scratch/hyaku/kengaku-r53/C2RevCounter/t/w7'); shutil.rmtree(root, ignore_errors=True); root.mkdir(parents=True)
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

print("=== TEST U: argv flags pointing at the LIVE lane (absolute path in a FLAG, not the script) ===")
live=root/'U_live'; live.mkdir()
(live/'plans').mkdir(parents=True, exist_ok=True)
(live/'plans'/'a.py').write_text(
  "import sys,os\nlane=sys.argv[sys.argv.index('--lane')+1]\n"
  "print('SAW', os.path.exists(os.path.join(lane,'MARKER_LIVE')))\n"
  "sys.exit(0 if os.path.exists(os.path.join(lane,'MARKER_LIVE')) else 1)\n")
(live/'MARKER_LIVE').write_text('x')
(live/'SKILL.md').write_text("## Gate/probe registry\n\n| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |\n|---|---|---|---|---|---|---|---|\n| `a` | gate | `python3 plans/a.py --lane .` | `0` ok | none | none | none | kengaku |\n")
led={"schema":c2.SCHEMA,"base":"probe","rows":{"a":{"argv":["python3","plans/a.py","--lane",str(live)],"exit":1,"state":"red","kind":"entry",
     "evidence":"SAW True","reason":"a probe reason long enough to pass the ten word minimum requirement here"}}}
(live/'plans'/c2.LEDGER.split('/')[-1]).write_text(json.dumps(led))
src=root/'U_src'; shutil.copytree(live,src)
(live/'MARKER_LIVE').unlink()   # marker only in the LIVE lane now? no: keep, we want the flag to reach it
(live/'MARKER_LIVE').write_text('x')
shutil.rmtree(src/'MARKER_LIVE', ignore_errors=True)
subprocess.run(['git','-C',str(src),'init','-q','-b','main'],check=True)
subprocess.run(['git','-C',str(src),'add','-A'],check=True)
subprocess.run(['git','-C',str(src),'-c','user.email=a@b','-c','user.name=a','commit','-qm','x'],check=True)
rc,lines=c2.evaluate(live, src, root/'U_work', 1, 30, None, False)
print("rc=",rc); print("\n".join(lines))
print(">>> the flag made the instrument read the LIVE lane, not the scratch clone")

print()
print("=== TEST V: gc config inside a --shared clone (protects the shared object store?) ===")
d=root/'V_src'; d.mkdir()
subprocess.run(['git','-C',str(d),'init','-q','-b','main'],check=True)
(d/'f').write_text('1'); subprocess.run(['git','-C',str(d),'add','-A'],check=True)
subprocess.run(['git','-C',str(d),'-c','user.email=a@b','-c','user.name=a','commit','-qm','x'],check=True)
cl=root/'V_clone'; subprocess.run(['git','clone','-q','--shared',str(d),str(cl)],check=True)
for k in ('gc.auto','gc.pruneExpire','core.repositoryformatversion'):
    r=subprocess.run(['git','-C',str(cl),'config','--get',k],capture_output=True,text=True)
    print(f"  {k} = {r.stdout.strip()!r} (rc={r.returncode})")

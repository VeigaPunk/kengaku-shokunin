import importlib.util, json, os, shutil, subprocess, sys
from pathlib import Path
LANE=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
spec=importlib.util.spec_from_file_location('c2', LANE/'plans/round53_c2_tipstate.py')
c2=importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
root=Path('/fast/scratch/hyaku/kengaku-r53/C2RevCounter/t/w6'); shutil.rmtree(root, ignore_errors=True); root.mkdir(parents=True)
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

print("=== TEST R: lane registry REDUCED (row removed) + ledger reduced -> does the counter PASS while the TIP keeps the row? ===")
src=root/'R_src'; src.mkdir(); mk(src,{'a':G,'b':G})
subprocess.run(['git','-C',str(src),'init','-q','-b','main'],check=True)
subprocess.run(['git','-C',str(src),'add','-A'],check=True)
subprocess.run(['git','-C',str(src),'-c','user.email=a@b','-c','user.name=a','commit','-qm','x'],check=True)
lane=root/'R_lane'; lane.mkdir(); mk(lane,{'a':G,'b':G})
tbl=(lane/'SKILL.md').read_text().splitlines()
(lane/'SKILL.md').write_text("\n".join([l for l in tbl if '`b`' not in l])+"\n")
led=json.loads((lane/'plans'/c2.LEDGER.split('/')[-1]).read_text()); del led["rows"]["b"]
(lane/'plans'/c2.LEDGER.split('/')[-1]).write_text(json.dumps(led))
rc,lines=c2.evaluate(lane, src, root/'R_work', 1, 30, None, False)
print("rc=",rc); print("\n".join(lines))
print(">>> source/tip SKILL.md registry rows =", (src/'SKILL.md').read_text().count('| gate |'), " but the counter PASSED")

print()
print("=== TEST S: git prune inside a --shared clone vs the SOURCE's loose objects ===")
d3=root/'S_src'; d3.mkdir()
subprocess.run(['git','-C',str(d3),'init','-q','-b','main'],check=True)
(d3/'f.txt').write_text('v1'); subprocess.run(['git','-C',str(d3),'add','-A'],check=True)
subprocess.run(['git','-C',str(d3),'-c','user.email=a@b','-c','user.name=a','commit','-qm','one'],check=True)
sha=subprocess.run(['git','-C',str(d3),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
clone=root/'S_clone'; subprocess.run(['git','clone','-q','--shared',str(d3),str(clone)],check=True)
print("clone alternates:", (clone/'.git'/'objects'/'info'/'alternates').read_text().strip())
print("source has the commit before prune:", subprocess.run(['git','-C',str(d3),'cat-file','-e',sha],capture_output=True).returncode==0)
r=subprocess.run(['git','-C',str(clone),'prune','--expire=now'],capture_output=True,text=True)
print("prune in shared clone rc=",r.returncode, r.stderr.strip()[:200])
print("source still has the commit after prune:", subprocess.run(['git','-C',str(d3),'cat-file','-e',sha],capture_output=True).returncode==0)
print("clone still has the commit after prune:", subprocess.run(['git','-C',str(clone),'cat-file','-e',sha],capture_output=True).returncode==0)

print()
print("=== TEST T: state leak CHANGES the observed exit (non-git source, same worker) ===")
def flip(root):
    # first row creates MARKER; second row exits 1 if MARKER exists, else 0
    (root/'plans'/'a.py').write_text("open('MARKER','w').write('x')\nprint('ok')\n")
    (root/'plans'/'b.py').write_text("import os,sys\nprint('ok')\nsys.exit(1 if os.path.exists('MARKER') else 0)\n")
lane2=root/'T'; lane2.mkdir()
mk(lane2,{'a':G,'b':G})
(lane2/'plans'/'a.py').write_text("open('MARKER','w').write('x')\nprint('ok')\n")
(lane2/'plans'/'b.py').write_text("import os,sys\nprint('ok')\nsys.exit(1 if os.path.exists('MARKER') else 0)\n")
led=json.loads((lane2/'plans'/c2.LEDGER.split('/')[-1]).read_text())
led["rows"]["b"].update({"exit":0,"state":"green"}); led["rows"]["b"].pop("evidence",None); led["rows"]["b"].pop("reason",None)
(lane2/'plans'/c2.LEDGER.split('/')[-1]).write_text(json.dumps(led))
rc,lines=c2.evaluate(lane2, lane2, root/'T_work', 1, 30, None, False)
print("rc=",rc); print("\n".join(lines))
print(">>> b is declared green; the leak makes it exit 1 ->", "MISMATCH" if "MISMATCH" in str(lines) else "no mismatch (isolated)")

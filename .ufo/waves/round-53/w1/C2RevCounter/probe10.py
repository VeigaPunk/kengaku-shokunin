import importlib.util, json, re, shutil, subprocess
from pathlib import Path
LANE=Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
spec=importlib.util.spec_from_file_location('c2', LANE/'plans/round53_c2_tipstate.py')
c2=importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
rows=c2.registry_rows((LANE/'SKILL.md').read_text()); rows.pop('__dups__')
print("=== cells with MORE THAN ONE python3 invocation (first-match rule could pick the wrong script) ===")
multi=[]
for n,line in rows.items():
    cells=re.split(r'(?<!\\)\|', line.strip().strip('|'))
    entry=cells[2]
    ms=re.findall(r'python3\s+((?:plans|corpus|grader)[A-Za-z0-9_./-]*\.py|grader\.py)', entry)
    if len(ms)>1: multi.append((n,ms))
print("rows with >1 python3 script token in the entry cell:", len(multi))
for n,ms in multi: print("  ",n,ms)
print()
print("=== entry cells whose python3 script does NOT match the SCRIPT prefix set ===")
bad=[]
for n,line in rows.items():
    cells=re.split(r'(?<!\\)\|', line.strip().strip('|'))
    if 'python3' in cells[2] and not re.search(r'python3\s+((?:plans|corpus|grader)[A-Za-z0-9_./-]*\.py|grader\.py)', cells[2]):
        bad.append(n)
print("count:",len(bad), bad[:10])
print()
print("=== does every registry row's script file EXIST in the lane? ===")
miss=[s for s in (c2.row_script(l) for l in rows.values()) if s and not (LANE/s).is_file()]
print("missing script files:", len(miss), miss[:10])
print()
print("=== REAL-LANE laundering probe: --help-augmented argv passes the static legs for ALL 75 rows ===")
root=Path('/fast/scratch/hyaku/kengaku-r53/C2RevCounter/t/w10'); shutil.rmtree(root, ignore_errors=True); root.mkdir(parents=True)
(root/'plans').mkdir()
shutil.copy(LANE/'SKILL.md', root/'SKILL.md')
led={"schema":c2.SCHEMA,"base":"probe","rows":{}}
for n,line in rows.items():
    s=c2.row_script(line)
    led["rows"][n]={"argv":["python3",s,"--help"],"exit":0,"state":"green","kind":"entry"}
(root/'plans'/c2.LEDGER.split('/')[-1]).write_text(json.dumps(led))
rc,lines=c2.evaluate(root, None, None, 4, 30, None, True)
print("dry rc=",rc)
print("\n".join(lines))
print()
print(">>> static legs accept an argv whose flags differ from the registry entry cell (registry says e.g. `python3 plans/state_check.py --summary`)")

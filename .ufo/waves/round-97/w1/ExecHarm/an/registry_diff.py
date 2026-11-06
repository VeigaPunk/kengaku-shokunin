import re, subprocess, sys, json
LANE = "/fast/scratch/hyaku/kengaku-r97/ExecHarm/laneT"
BASE = "4992cd0e32b8db23ca20310deb7de12d485f8bcc"
TIP  = "f1083da60e7ff6b88f7420aae7424f7762d14700"
def show(rev, path):
    p = subprocess.run(["git","-C",LANE,"show",f"{rev}:{path}"],capture_output=True)
    if p.returncode: raise SystemExit(f"missing {path} at {rev}")
    return p.stdout.decode()
def rows(text):
    lines = text.splitlines()
    try: i = next(j for j,l in enumerate(lines) if l.startswith("## Gate/probe registry"))
    except ValueError: raise SystemExit("no registry heading")
    out = {}
    order = []
    for ln in lines[i+1:]:
        if ln.startswith("## ") and not ln.startswith("## Gate/probe registry"): break
        if not ln.startswith("|"): continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", ln)[1:-1]]
        if not cells: continue
        name = cells[0].strip("` ")
        if name in ("Gate", "---", "Name") or set(name) <= set("-: "): continue
        if name in out: raise SystemExit(f"duplicate row {name}")
        out[name] = cells; order.append(name)
    return out, order
b, bo = rows(show(BASE,"SKILL.md"))
t, to = rows(show(TIP,"SKILL.md"))
print("BASE rows", len(b), "TIP rows", len(t))
added = [n for n in to if n not in b]; removed = [n for n in bo if n not in t]
print("ADDED", len(added), added)
print("REMOVED", len(removed), removed)
kind_changes = []; other_changes = {}
for n in to:
    if n not in b: continue
    bc, tc = b[n], t[n]
    if len(bc) != len(tc):
        other_changes.setdefault("COLS",[]).append((n,len(bc),len(tc))); continue
    for idx,(x,y) in enumerate(zip(bc,tc)):
        if x != y:
            if idx == 1: kind_changes.append((n,x,y))
            else: other_changes.setdefault(idx,[]).append(n)
print("KIND changes", len(kind_changes))
from collections import Counter
print("KIND transitions", Counter((x,y) for _,x,y in kind_changes))
print("OTHER changed cells by column index:", {k:(len(v),v[:6]) for k,v in other_changes.items()})
# added rows detail
for n in added: print("NEWROW", n, "|", t[n][1], "|", t[n][2][:70])
# kind census at each rev
print("BASE kind counts", Counter(c[1] for c in b.values()))
print("TIP  kind counts", Counter(c[1] for c in t.values()))
json.dump({"added":added,"removed":removed,"kind_changes":kind_changes,
           "other":{str(k):v for k,v in other_changes.items()}},
          open("/fast/scratch/hyaku/kengaku-r97/ExecHarm/an/regdiff.json","w"), indent=1)

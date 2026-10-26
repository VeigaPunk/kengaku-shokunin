import re, pathlib, collections
ROOT=pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
CAP=ROOT/"corpus/evidence/round41/tb2-constraints-scheduling"
md=(ROOT/"corpus/knowledge/tb2-constraints-scheduling-grader.md").read_text()
sec=md.split("## Located quotes")[1].split("## Requirement map")[0]
rows=[l for l in sec.splitlines() if l.startswith("|") and "“" in l and "Quote”" not in l]
ok=0; bad=[]
for l in rows:
    m=re.search(r"\|\s*`([A-Za-z_.]+):(\d+)`\s*\|?\s*$", l); q=re.search(r"“(.*)”", l)
    if not (m and q): bad.append(("PARSE", l[:60])); continue
    f,ln=m.group(1),int(m.group(2)); quote=q.group(1); p=CAP/f
    lines=p.read_text().splitlines()
    if 1<=ln<=len(lines) and quote in lines[ln-1]: ok+=1
    else: bad.append((f"{f}:{ln}", "not at cited line"))
print(f"located quotes: {ok}/{len(rows)} byte-exact at the cited line; misses={len(bad)}")
for b in bad: print("  MISS", b)
dry=(ROOT/"corpus/evidence/round41/constraints-dry-cases-freeze.txt").read_text()
rec=(ROOT/"corpus/evidence/round41/constraints-probe.txt").read_text()
order=[l.split()[1] for l in dry.splitlines() if l.startswith("TAG ")]
cases={}; 
for l in dry.splitlines():
    if l.startswith("CASE "):
        mm=re.search(r"violates=(\S*)", l); cases[l.split()[1]]=[x for x in (mm.group(1).split(",") if mm else []) if x]
obs={l.split()[1]:[p for p in l.split() if p.startswith("tests=")][0].split("=")[1] for l in rec.splitlines() if l.startswith("CASE ")}
per=collections.defaultdict(list)
for c,vs in cases.items():
    for t in vs: per[t].append(c)
print("dry ids == receipt ids:", set(cases)==set(obs), f"({len(cases)} cases)")
for t in order:
    cids=per[t]; res={obs[c] for c in cids}
    lab="unenforced" if res=={"PPP"} else ("enforced" if "PPP" not in res else "partly")
    print(f"  {t:18s} n={len(cids):2d} {lab}")
# hard_ok on the wed-1059 state
import importlib.util
from datetime import datetime, timedelta
spec=importlib.util.spec_from_file_location("g", CAP/"test_outputs.py"); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
s=datetime(2024,1,17,10,59); print("wed-1059 _hard_ok(10:59,11:59) =", g._hard_ok(s, s+timedelta(hours=1)))

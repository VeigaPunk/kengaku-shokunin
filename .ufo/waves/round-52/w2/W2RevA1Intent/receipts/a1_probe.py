import sys, re, json
sys.path.insert(0, "lane/plans")
import round52_c1_grader_audit as c
from pathlib import Path
lane = Path("lane")
pop = json.loads((lane/"plans/round52-tasks.json").read_text())
root = lane/"corpus/evidence/round52/graders"
rows = []
for task, files in sorted(pop["tasks"].items()):
    pg = c.primary_grader(files)
    if not pg or not (root/pg).exists(): continue
    body = (root/pg).read_text(errors="replace")
    tests = c.split_tests(body)
    # module-level / non-test defs
    n_def_all = len(re.findall(r"^\s*def\s+\w+", body, re.M))
    n_test_indented = len(re.findall(r"^\s+def\s+test_", body, re.M))
    n_class = len(re.findall(r"^class\s", body, re.M))
    for name, blk in tests:
        cls = c.classify_test(blk)
        stripped = c.PRESENCE.sub(" ", blk)
        rows.append(dict(task=task, test=name, cls=cls, has_presence=bool(c.PRESENCE.search(blk)),
                         behav_hit=(m.group(0) if (m:=c.BEHAV_T.search(stripped)) else None),
                         value_hits=sorted(set(m.group(0) for m in c.VALUE.finditer(stripped))),
                         n_def_all=n_def_all, n_test_indented=n_test_indented, n_class=n_class, grader=pg))
json.dump(rows, open("rows.json","w"), indent=1)
from collections import Counter
print("tests", len(rows), Counter(r["cls"] for r in rows))
print("tasks with indented test defs:", sorted({r["task"] for r in rows if r["n_test_indented"]}))
print("tasks with class:", sorted({r["task"] for r in rows if r["n_class"]}))
# false-negative candidates: presence present but not P1
print("\n-- presence-bearing but not P1 (trigger shown):")
for r in rows:
    if r["has_presence"] and r["cls"]!="P1":
        print(r["cls"], r["task"], r["test"], "behav=",r["behav_hit"], "value=",r["value_hits"][:6])

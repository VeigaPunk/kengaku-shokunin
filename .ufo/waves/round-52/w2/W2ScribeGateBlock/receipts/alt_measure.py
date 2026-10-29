import sys, re, json
sys.dont_write_bytecode = True
sys.path.insert(0, '.')
from pathlib import Path
import c1_counter_copy as C
lane = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
pop = json.load(open(lane/'plans'/'round52-tasks.json'))
root = lane/'corpus/evidence/round52/graders'
TOP = re.compile(r"^(def |class |@|[A-Za-z_][A-Za-z0-9_]* *=)", re.M)
def split_any(body):
    # block = from def test_ to next top-level construct of any kind
    out=[]
    for m in C.TESTDEF.finditer(body):
        rest = body[m.end():]
        n = TOP.search(rest)
        end = m.end() + (n.start() if n else len(rest))
        out.append((m.group(1), body[m.start():end]))
    return out
def strip_comments_docs(block):
    block = re.sub(r'"""[\s\S]*?"""', '', block)
    block = re.sub(r'#[^\n]*', '', block)
    return block
def cls_alt(block, strip):
    b = strip_comments_docs(block) if strip else block
    if "assert" not in b: return "P0"
    s = C.PRESENCE.sub(" ", b)
    if C.BEHAV_T.search(s): return "P2"
    if C.VALUE.search(s): return "P3"
    if C.PRESENCE.search(b): return "P1"
    return "P0"
res = {"frozen":{}, "split_any_top":{}, "strip_prose":{}, "both":{}}
tot = {k:[0,set()] for k in res}
for t in pop['tasks']:
    pg = C.primary_grader(pop['tasks'][t])
    if not (root/pg).exists(): continue
    body = (root/pg).read_text(encoding="utf-8", errors="replace")
    frozen = [(n, C.classify_test(b)) for n,b in C.split_tests(body)]
    anyt = [(n, cls_alt(b, False)) for n,b in split_any(body)]
    strip = [(n, cls_alt(b, True)) for n,b in C.split_tests(body)]
    both = [(n, cls_alt(b, True)) for n,b in split_any(body)]
    for key, lst in [("frozen",frozen),("split_any_top",anyt),("strip_prose",strip),("both",both)]:
        p1 = [n for n,c in lst if c=="P1"]
        tot[key][0]+=len(p1)
        if p1: tot[key][1].add(t)
        res[key][t]=[(n,c) for n,c in lst]
for k,(n,ts) in tot.items(): print(f"{k:14s} P1_tests={n} tasks={len(ts)}")
# tasks/tests that change between frozen and both
chg=[]
for t in res['frozen']:
    a=dict(res['frozen'][t]); b=dict(res['both'][t])
    for n in a:
        if a[n]!=b.get(n): chg.append((t,n,a[n],b.get(n)))
print("changed tests (frozen->both):", len(chg))
for c in chg: print("  ",c)
json.dump({k:v for k,v in res.items()}, open('alt_measure.json','w'), indent=1)

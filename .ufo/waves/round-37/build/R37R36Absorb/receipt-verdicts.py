import ast,re
def load_src(p):
    ns={"__name__":"l","__file__":p}; exec(compile(open(p,encoding="utf-8").read(),p,"exec"),ns); return ns
cases={c[0]:c for c in load_src("plans/regex_log_probe.py")["build_cases"]()}
cap="corpus/evidence/round36/tb2-regex-log/test_outputs.py"
tree=ast.parse(open(cap,encoding="utf-8").read())
fn=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=="test_regex_matches_dates"][0]
V={}
for n in ast.walk(fn):
    if isinstance(n,ast.Assign) and getattr(n.targets[0],"id",None) in ("sample_logs","expected_dates"):
        V[n.targets[0].id]=ast.literal_eval(n.value)
text="\n".join(V["sample_logs"]); exp=V["expected_dates"]
recv={}
import re as _re
for l in open("corpus/evidence/round36/regex-log-probe.txt"):
    m=_re.match(r"case=(\S+) predicted=(\S+) observed=(\S+) match=(\S+)",l)
    if m: recv[m.group(1)]=m.group(3)
bad=[]
for name,(nm,rx,pred,req,mode) in cases.items():
    if mode!="file" or rx is None: continue
    try: got=re.findall(rx.strip(),text,ast.literal_eval("0") if False else re.MULTILINE)
    except re.error: obs="fail"
    else:
        got=[("|".join(t) if isinstance(t,tuple) else t) for t in got]
        obs="pass" if got==list(exp) else "fail"
    if obs!=recv.get(name): bad.append((name,obs,recv.get(name)))
print("file-mode cases:",sum(1 for c in cases.values() if c[4]=="file" and c[1] is not None))
print("verdict mismatches vs receipt (with .strip() as the grader does):",len(bad),bad)

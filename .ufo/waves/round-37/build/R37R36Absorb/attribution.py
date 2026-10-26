import ast, re, collections
LANE="/home/vgpnk/Projects/shokunin/kengaku-shokunin"
def load_src(p):
    ns={"__name__":"loaded","__file__":p}
    exec(compile(open(p,encoding="utf-8").read(),p,"exec"),ns); return ns
probe=load_src(LANE+"/plans/regex_log_probe.py")
cases={c[0]:(c[1],c[2]) for c in probe["build_cases"]()}
cap=LANE+"/corpus/evidence/round36/tb2-regex-log/test_outputs.py"
tree=ast.parse(open(cap,encoding="utf-8").read())
fn=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=="test_regex_matches_dates"][0]
V={}
for node in ast.walk(fn):
    if isinstance(node,ast.Assign) and getattr(node.targets[0],"id",None) in ("sample_logs","expected_dates"):
        V[node.targets[0].id]=(ast.literal_eval(node.value),[e.lineno for e in node.value.elts],node.lineno)
lines,flines=V["sample_logs"][0],V["sample_logs"][1]; expected=V["expected_dates"][0]
def vals(rx,line):
    out=re.findall(rx,line,re.MULTILINE)
    return [  ("|".join(t) if isinstance(t,tuple) else t) for t in out ]
ref={n:(cases["reference-month-aware"][0]) for n in []}
REF=cases["reference-month-aware"][0]
refv=[vals(REF,l) for l in lines]
print("REFERENCE per-line values (sample idx -> date or -):")
print("  ", {i+1:(refv[i][0] if refv[i] else '-') for i in range(25)})
for name in ["no-ip-condition","ip-octets-unbounded","ip-no-left-boundary","ip-no-right-boundary","ip-before-date-only","first-date-only","date-no-left-boundary","date-no-right-boundary","month-13-allowed","month-00-allowed","day-32-allowed","day-00-allowed"]:
    rx=cases[name][0]
    got=[vals(rx,l) for l in lines]
    flips=[(i+1,flines[i],refv[i],got[i]) for i in range(25) if refv[i]!=got[i]]
    print("\nCASE %-24s flips=%d"%(name,len(flips)))
    for idx,fl,r,g in flips: print("   L%-2d file:%-3d ref=%-18s got=%s"%(idx,fl,r or '-',g or '-'))

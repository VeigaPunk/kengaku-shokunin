import pathlib, re, subprocess
STEM=re.compile(r"[^a-z0-9]+"); CAND=re.compile(r"probe.*\.(?:txt|log)$", re.I)
def g(*a): return subprocess.run(["git","-C",".",*a],capture_output=True,check=True).stdout.decode()
plans=[p for p in g("ls-tree","-r","HEAD","--name-only","plans").splitlines() if p.endswith(".py") and "/" not in p[len("plans/"):]]
by={}
for p in plans: by.setdefault(STEM.sub("",pathlib.Path(p).stem.lower()),[]).append(p)
cands=sorted(p for p in g("ls-tree","-r","HEAD","--name-only","corpus/evidence").splitlines() if CAND.search(p.rsplit("/",1)[-1]))
print("plans_total=%d plans_stem_dup=%s" % (len(plans), {k:v for k,v in by.items() if len(v)>1}))
print("candidates=%d" % len(cands))
for c in cands:
    s=STEM.sub("",pathlib.Path(c).stem.lower()); hit=by.get(s,[])
    if hit: print("MATCH %s stem=%s scripts=%s" % (c,s,hit))
print("probe_named_plans=%s" % sorted(p for p in plans if "probe" in p))

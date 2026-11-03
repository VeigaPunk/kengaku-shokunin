import pathlib, importlib.util, re, json
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
spec = importlib.util.spec_from_file_location("gate", LANE/"plans/round63_gate_checks.py")
gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)
K = LANE/"corpus/knowledge"
KEY = re.compile(r"^(source|verified-at|recheck):")
def tsukuroi_rule(t):
    fence=None; out={"source":None,"verified-at":None,"recheck":None}
    for l in t.split("\n"):
        s=l.rstrip("\r")
        if fence:
            if s.lstrip().startswith(fence): fence=None; continue
            continue
        if s.lstrip().startswith("```") or s.lstrip().startswith("~~~"):
            fence=s.lstrip()[:3]; continue
        m=KEY.match(s)
        if m: out[m.group(1)]=s
    return all(out.values())
def chousa_rule(t):
    has={"source":False,"verified-at":False,"recheck":False}; fence=None
    for l in t.split("\n"):
        s=l.rstrip("\r")
        if fence:
            if s.lstrip().startswith(fence): fence=None; continue
            continue
        if s.lstrip().startswith("```") or s.lstrip().startswith("~~~"):
            fence=s.lstrip()[:3]; continue
        if s.startswith("## "): break
        m=KEY.match(s)
        if m: has[m.group(1)]=True
    return all(has.values())
def kumitate_rule(t):
    lines=t.splitlines(); hdr=lines[:5]
    return bool(lines[0] and lines[0].startswith("source:") and re.match(r"^source:\s*\S",lines[0])
                and any(re.match(r"^verified-at:\s*\S",l) for l in hdr)
                and any(re.match(r"^recheck:\s*\S",l) for l in hdr))
files=sorted(K.glob("*.md")); n=len(files)
def cnt(fn): return sum(1 for f in files if fn(f.read_text(errors="replace")))
kg=cnt(lambda t: not gate.trio_missing(t)); tu=cnt(tsukuroi_rule); ch=cnt(chousa_rule); ku=cnt(kumitate_rule)
print(f"CURRENT TREE  corpus/knowledge/*.md = {n}")
print(f"  GREEN kengaku round-63 trio gate : {kg}   RED {n-kg}")
print(f"  GREEN tsukuroi-style rule        : {tu}   RED {n-tu}")
print(f"  GREEN chousa-style rule          : {ch}   RED {n-ch}")
print(f"  GREEN kumitate-style rule        : {ku}   RED {n-ku}")
addend=[f.name for f in files if "## Freshness addendum (round 64)" in f.read_text(errors="replace")]
print(f"  files carrying '## Freshness addendum (round 64)': {len(addend)}")
red=[f.name for f in files if gate.trio_missing(f.read_text(errors="replace"))]
print(f"  still RED under kengaku gate: {len(red)}")
print("   ", red[:6])
# frozen list comparison
frozen=sorted(l.strip() for l in (LANE/"corpus/evidence/round64/trio-red-at-base.txt").read_text().splitlines() if l.strip())
print(f"  frozen list (29) vs current kengaku-red ({len(red)}): {'same population' if len(red)==29 and set(red)=={x.split('/')[-1] for x in frozen} else 'DIFFERENT'}")
# which entries carry addendum but are still red under kengaku gate
both=[f.name for f in files if "## Freshness addendum (round 64)" in f.read_text(errors="replace") and gate.trio_missing(f.read_text(errors="replace"))]
print(f"  addendum-bearing AND still red under kengaku gate: {len(both)}")
json.dump({"files":n,"green":{"kengaku":kg,"tsukuroi":tu,"chousa":ch,"kumitate":ku},
           "addendum_files":len(addend),"kengaku_red":len(red),"frozen_len":len(frozen)}, open("current.json","w"), indent=1)

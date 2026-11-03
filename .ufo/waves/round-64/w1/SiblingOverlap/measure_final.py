import pathlib, importlib.util, re, json, hashlib
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
spec = importlib.util.spec_from_file_location("gate", LANE/"plans/round63_gate_checks.py")
gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)
K = LANE/"corpus/knowledge"
KEY = re.compile(r"^(source|verified-at|recheck):")

def tsukuroi_rule(t):  # tools/check-knowledge-header.py: column-0, outside fences, LAST occurrence operative
    fence=None; out={"source":None,"verified-at":None,"recheck":None}
    for l in t.split("\n"):
        s=l.rstrip("\r")
        if fence:
            if s.lstrip().startswith(fence): fence=None
            continue
        if s.lstrip().startswith("```") or s.lstrip().startswith("~~~"):
            fence=s.lstrip()[:3]; continue
        m=KEY.match(s)
        if m: out[m.group(1)]=s
    return all(out.values())

def chousa_rule(t):  # tools/research-gate.sh verify-metadata: trio before the first '## ' heading
    has={"source":False,"verified-at":False,"recheck":False}; fence=None
    for l in t.split("\n"):
        s=l.rstrip("\r")
        if fence:
            if s.lstrip().startswith(fence): fence=None
            continue
        if s.lstrip().startswith("```") or s.lstrip().startswith("~~~"):
            fence=s.lstrip()[:3]; continue
        if s.startswith("## "): break
        m=KEY.match(s)
        if m: has[m.group(1)]=True
    return all(has.values())

def kumitate_rule(t):  # scripts/sources-check.mjs: source on line 1, trio in first 5 lines, presence only
    lines=t.splitlines(); hdr=lines[:5]
    return bool(lines[0] and lines[0].startswith("source:") and re.match(r"^source:\s*\S",lines[0])
                and any(re.match(r"^verified-at:\s*\S",l) for l in hdr)
                and any(re.match(r"^recheck:\s*\S",l) for l in hdr))

files=sorted(K.glob("*.md")); n=len(files)
def cnt(fn): return sum(1 for f in files if fn(f.read_text(errors="replace")))
kg=cnt(lambda t: not gate.trio_missing(t)); tu=cnt(tsukuroi_rule); ch=cnt(chousa_rule); ku=cnt(kumitate_rule)
print(f"corpus/knowledge/*.md files = {n}")
print(f"GREEN kengaku round-63 trio gate : {kg}   RED {n-kg}")
print(f"GREEN tsukuroi-style rule        : {tu}   RED {n-tu}")
print(f"GREEN chousa-style rule          : {ch}   RED {n-ch}")
print(f"GREEN kumitate-style rule        : {ku}   RED {n-ku}")

reds=[f for f in files if gate.trio_missing(f.read_text(errors="replace"))]
computed=sorted("corpus/knowledge/"+f.name for f in reds)
frozen=sorted(l.strip() for l in (LANE/"corpus/evidence/round64/trio-red-at-base.txt").read_text().splitlines() if l.strip())
print(f"\nfrozen list == recomputed red set: {computed==frozen}  (computed {len(computed)}, frozen {len(frozen)})")

ADD="\n## Freshness addendum (round 64)\n\nverified-at: 2026-11-03\nrecheck: 2027-05-01\n"
def after(fn): return sum(1 for f in reds if not fn(f.read_text(errors="replace")+ADD))
print("\nAFTER the frozen C3 append-only addendum block on all 29 red entries:")
print(f"  still RED under kengaku round-63 trio gate : {sum(1 for f in reds if gate.trio_missing(f.read_text(errors='replace')+ADD))}/29")
print(f"  still RED under tsukuroi-style rule          : {sum(1 for f in reds if not tsukuroi_rule(f.read_text(errors='replace')+ADD))}/29")
print(f"  still RED under chousa-style rule            : {sum(1 for f in reds if not chousa_rule(f.read_text(errors='replace')+ADD))}/29")
print(f"  still RED under kumitate-style rule          : {sum(1 for f in reds if not kumitate_rule(f.read_text(errors='replace')+ADD))}/29")

va_key=[f.name for f in reds if re.search(r"(?m)^verified-at:", f.read_text(errors="replace"))]
va_any=[f.name for f in reds if "verified-at" in f.read_text(errors="replace")]
print(f"\nred entries carrying a column-0 'verified-at:' KEY : {len(va_key)} {va_key}")
print(f"red entries containing the STRING 'verified-at'    : {len(va_any)} {va_any}")
json.dump({"files":n,"green":{"kengaku":kg,"tsukuroi":tu,"chousa":ch,"kumitate":ku},
           "red_set_equals_frozen":computed==frozen,"va_key":va_key,"va_any":va_any},
          open("measure_final.json","w"), indent=1)

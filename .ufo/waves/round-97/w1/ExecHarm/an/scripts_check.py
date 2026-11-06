import re, subprocess, json, hashlib
LANE="/fast/scratch/hyaku/kengaku-r97/ExecHarm/laneT"
BASE="4992cd0e32b8db23ca20310deb7de12d485f8bcc"; TIP="f1083da60e7ff6b88f7420aae7424f7762d14700"
def show(rev,path):
    p=subprocess.run(["git","-C",LANE,"show",f"{rev}:{path}"],capture_output=True)
    return p.stdout if p.returncode==0 else None
def rows(text):
    lines=text.splitlines(); i=next(j for j,l in enumerate(lines) if l.startswith("## Gate/probe registry"))
    out={}
    for ln in lines[i+1:]:
        if ln.startswith("## "): break
        if not ln.startswith("|"): continue
        cells=[c.strip() for c in re.split(r"(?<!\\)\|",ln)[1:-1]]
        if len(cells)<3: continue
        name=cells[0].strip("` ")
        if cells[1] not in ("gate","probe"): continue
        out[name]=cells
    return out
b=rows(show(BASE,"SKILL.md").decode()); t=rows(show(TIP,"SKILL.md").decode())
SCRIPT=re.compile(r"([\w./-]+\.(?:py|sh|mjs))")
BROAD=re.compile(r"self[-_]?test", re.I)
CODE=[re.compile(p) for p in (r"add_argument\(\s*[\"']--self-?test[\"']", r"add_parser\(\s*[\"']self-?test[\"']",
  r"[\"']--self-?test[\"']\s*(?:in|==|not in)\b", r"(?:\bin|==)\s*\(?[\"']--self-?test[\"']",
  r"def run_selftest\b", r"(?:==|\bin)\s*\(?[\"']self-?test[\"']")]
changed=[n for n in t if n in b and b[n][1]=="gate" and t[n][1]=="probe"]
print("changed rows", len(changed))
bad=[]; broadhits=[]; scriptchg=[]
for n in changed:
    m=SCRIPT.search(b[n][2])
    if not m: bad.append((n,"no-script")); continue
    path=m.group(1)
    sb=show(BASE,path); st=show(TIP,path)
    if sb is None: bad.append((n,"absent",path)); continue
    if st is None or hashlib.sha256(sb).digest()!=hashlib.sha256(st).digest(): scriptchg.append((n,path))
    text=sb.decode(errors="replace")
    if any(p.search(text) for p in CODE): bad.append((n,"HAS-CODE-SPELLING",path))
    elif BROAD.search(text): broadhits.append((n,path,[l.strip()[:100] for l in text.splitlines() if BROAD.search(l)][:3]))
print("rows whose BASE script HAS a code spelling (census would be wrong):", bad)
print("rows with broad word-mention only:", len(broadhits))
for h in broadhits: print("  BROAD", h)
print("scripts changed BASE->TIP among the 44:", scriptchg)
# T side: every gate row must have a spelling
missing=[]
for n,c in t.items():
    if c[1]!="gate": continue
    m=SCRIPT.search(c[2])
    if not m: missing.append((n,"no-script")); continue
    st=show(TIP,m.group(1))
    if st is None: missing.append((n,"absent",m.group(1))); continue
    if not any(p.search(st.decode(errors="replace")) for p in CODE): missing.append((n,"NO-SPELLING",m.group(1)))
print("TIP gate rows", sum(1 for c in t.values() if c[1]=="gate"), "without code spelling:", missing)
json.dump({"changed":changed,"bad":bad,"broad":broadhits,"scriptchg":scriptchg,"tip_missing":missing},
          open("/fast/scratch/hyaku/kengaku-r97/ExecHarm/an/scripts_check.json","w"),indent=1)

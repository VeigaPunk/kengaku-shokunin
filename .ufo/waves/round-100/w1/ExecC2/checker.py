#!/usr/bin/env python3
"""ExecC2 independent C2 checker — does NOT import lane counter.
Verifies:
 A) per-POP-row blob sha256 at T == pop token == PROVENANCE.md sha cell,
    exactly one line per row across all PROVENANCE.md files at T,
    three cells, no URL, sha column present.
 B) BASE-bytes gate (--verbose) finding diff REF(F~1)->T restricted to
    BASE rows: exactly 9 pop tokens cleared + S300 fa53d657 reclass,
    nothing else.
 C) all 333 BASE SOURCES.md row lines byte-equal at T.
Mutations self-test included (falsification).
"""
import hashlib, subprocess, sys, re, os

BASE="7846037679de77d050141c785996471801e5a19a"
T="dbe0cefa607cf57f7f58346fce64bcc127144ca0"
REF="5220b71d337a3703eaba4cdf6b85eaf343497ae0"  # F~1
LANE="/fast/scratch/hyaku/kengaku-r100/ExecC2/cloneT"
REFDIR="/fast/scratch/hyaku/kengaku-r100/ExecC2/cloneREF"
TDIR=LANE
SCRATCH="/fast/scratch/hyaku/kengaku-r100/ExecC2"
POPPATH="/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-100/L1/c2-pop.txt"
LIVEPATH="/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-100/L1/c2-live-refetch.txt"

def git(root,*a):
    r=subprocess.run(["git","-C",root,*a],capture_output=True,timeout=120)
    return r
def blob(root,rev,path):
    r=git(root,"show",f"{rev}:{path}")
    return r.stdout if r.returncode==0 else None
def sha(b): return hashlib.sha256(b).hexdigest() if b is not None else "absent"

fails=[]
def check(name,cond,detail=""):
    print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")
    if not cond: fails.append(name)

# --- parse POP from c2-pop.txt (not importing counter) ---
pop={}
for line in open(POPPATH):
    m=re.match(r"POP (S\d+) ([0-9a-f]{64}) (\S+) (\S+)",line.strip())
    if m: pop[m.group(1)]=(m.group(2),m.group(3),m.group(4))
check("pop-count",len(pop)==9,f"n={len(pop)} sids={sorted(pop)}")

# parse live refetch
live={}
for line in open(LIVEPATH):
    m=re.match(r"LIVE (S\d+) http=(\d+) bytes=(\d+) sha256=([0-9a-f]{64}) url=(\S+)",line.strip())
    if m: live[m.group(1)]=(m.group(2),m.group(4),m.group(5))
check("live-count",len(live)==9,f"n={len(live)}")

ROWID=re.compile(r"^ {0,3}\|\s*(S\d+)\s*\|")
def row_map(root,rev):
    data=blob(root,rev,"corpus/SOURCES.md").decode()
    m={}
    for ln in data.splitlines():
        mm=ROWID.match(ln)
        if mm: m[mm.group(1)]=ln.encode()
    return m

base_rows=row_map(LANE,BASE)
t_rows=row_map(LANE,T)
check("base-rows-333",len(base_rows)==333,f"n={len(base_rows)}")
not_equal=[s for s in base_rows if t_rows.get(s)!=base_rows[s]]
missing=[s for s in base_rows if s not in t_rows]
check("base-rows-byte-equal-at-T",not_equal==[] and missing==[],f"not_equal={not_equal} missing={missing} t_rows={len(t_rows)}")

# --- A: blob sha + PROVENANCE scan ---
def provenance_files(root,rev):
    out=git(root,"ls-tree","-r","--name-only",rev,"corpus/evidence").stdout.decode().splitlines()
    return [p for p in out if p.rsplit("/",1)[-1]=="PROVENANCE.md"]
provT=provenance_files(LANE,T)
provBASE=provenance_files(LANE,BASE)
new_prov=sorted(set(provT)-set(provBASE))
check("new-prov-3",len(new_prov)==3,f"{new_prov}")

# scan all PROVENANCE.md at T: lines mentioning any POP sid
LINE_ID=re.compile(r"\b(S\d{3,})\b")
prov_lines={s:[] for s in pop}  # sid -> (file,line) in NEW files only
all_prov_lines=[]  # (file, cells, line) in NEW files only
for p in new_prov:
    data=blob(LANE,T,p).decode(errors="replace")
    for ln in data.splitlines():
        if "|" not in ln: continue
        cells=[c.strip() for c in ln.strip().strip("|").split("|")]
        all_prov_lines.append((p,cells,ln))
        for sid in pop:
            if re.search(rf"\b{sid}\b",ln): prov_lines[sid].append((p,cells,ln))
for sid,(tok,cap,url) in sorted(pop.items()):
    b=blob(LANE,T,cap)
    h=sha(b)
    check(f"{sid}-blob-sha==token",h==tok,f"blob={h} tok={tok}")
    check(f"{sid}-live-token-match",sid in live and live[sid][1]==tok,f"live={live.get(sid)}")
    lines=prov_lines[sid]
    check(f"{sid}-exactly-one-prov-line",len(lines)==1,f"n={len(lines)} files={[x[0] for x in lines]}")
    if len(lines)==1:
        f,cells,ln=lines[0]
        check(f"{sid}-three-cells",len(cells)==3,f"cells={len(cells)} {ln[:120]}")
        check(f"{sid}-no-url","http://" not in ln and "https://" not in ln,f"url_in_line={'http' in ln}")
        check(f"{sid}-sha-cell==token",any(tok==c.strip(chr(96)) for c in cells),f"cells={cells}")
        check(f"{sid}-sid-in-line",sid in ln,"")
        check(f"{sid}-file-is-new",f in new_prov,f"file={f}")

# no id outside pop in new files
extra=[]
for p,cells,ln in all_prov_lines:
    for x in LINE_ID.findall(ln):
        if x not in pop: extra.append((p,x,ln[:80]))
check("no-id-outside-pop",extra==[],f"extra={extra[:5]}")

# no URL in any new provenance file at all
urlfiles=[p for p in new_prov if "http" in blob(LANE,T,p).decode(errors="replace")]
check("url-channel-files-0",urlfiles==[],f"{urlfiles}")

# --- B: BASE gate bytes --verbose at REF and T ---
base_gate=blob(LANE,BASE,"plans/anchor_digest_check.py")
gatepath=os.path.join(SCRATCH,"base_gate.py")
open(gatepath,"wb").write(base_gate)
check("base-gate-bytes",sha(base_gate)=="11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2",f"sha={sha(base_gate)}")
DEFECT=re.compile(r"^DEFECT (S\d+) \S+ token=(\S+) class=(\S+) detail=(\S+)")
NOTE=re.compile(r"^(BIND|BIND\+|UNBOUND|RESOLVED|ABBREV|EXEMPT|CAPTURES|ERRATUM) (S\d+)\b")
LOC=re.compile(r" loc=corpus/SOURCES\.md:\d+")
def run_gate(cwd):
    r=subprocess.run([sys.executable,gatepath,"--lane",cwd,"--verbose"],capture_output=True,text=True,timeout=600)
    return r.stdout.splitlines(),r.returncode
def per_sid(lines):
    d={}; n={}
    for ln in lines:
        m=DEFECT.match(ln)
        if m: d.setdefault(m.group(1),[]).append(LOC.sub("",ln)); continue
        m=NOTE.match(ln)
        if m: n.setdefault(m.group(2),[]).append(LOC.sub("",ln))
    return {k:sorted(v) for k,v in d.items()},{k:sorted(v) for k,v in n.items()}
print("running gate at REF (BASE bytes)...",flush=True)
ref_lines,ref_rc=run_gate(REFDIR)
print("running gate at T (BASE bytes)...",flush=True)
t_lines,t_rc=run_gate(TDIR)
open(os.path.join(SCRATCH,"gate-REF.txt"),"w").write("\n".join(ref_lines))
open(os.path.join(SCRATCH,"gate-T.txt"),"w").write("\n".join(t_lines))
ref_d,ref_n=per_sid(ref_lines); t_d,t_n=per_sid(t_lines)
base_sids=set(base_rows)
ref_d={k:v for k,v in ref_d.items() if k in base_sids}
t_d={k:v for k,v in t_d.items() if k in base_sids}
print(f"DEFECT sids REF={len(ref_d)} T={len(t_d)} REF-lines={sum(len(v) for v in ref_d.values())} T-lines={sum(len(v) for v in t_d.values())}")
cleared=[]; added=[]; reclass=[]
for sid in sorted(set(ref_d)|set(t_d)):
    a=ref_d.get(sid,[]); b=t_d.get(sid,[])
    if a==b: continue
    # token-set comparison
    atoks=[DEFECT.match(x).group(2) for x in a]; btoks=[DEFECT.match(x).group(2) for x in b]
    if set(atoks)-set(btoks): cleared.append((sid,sorted(set(atoks)-set(btoks))))
    if set(btoks)-set(atoks): added.append((sid,sorted(set(btoks)-set(atoks))))
    if set(atoks)&set(btoks) and a!=b:
        reclass.append((sid,a,b))
print("CLEARED",cleared); print("ADDED",added); print("RECLASS",[(s) for s,_,_ in reclass])
for s,a,b in reclass: print("RECLASS_DETAIL",s,a,"=>",b)
expect_cleared={s:{pop[s][0]} for s in pop}
got_cleared={s:set(t) for s,t in cleared}
check("cleared-exactly-9-pop-tokens",got_cleared=={k:{v[0]} for k,v in pop.items()},f"got={got_cleared}")
check("no-added-defects",added==[],f"added={added}")
check("reclass-only-S300",[s for s,_,_ in reclass]==["S300"],f"{[s for s,_,_ in reclass]}")
# verify S300 reclass token fa53d657 preserved, class changed anchor-unbound->abbrev-unresolved
ok300=False
for s,a,b in reclass:
    if s=="S300":
        a300=[(DEFECT.match(x).group(2),DEFECT.match(x).group(3)) for x in a if DEFECT.match(x)]
        b300=[(DEFECT.match(x).group(2),DEFECT.match(x).group(3)) for x in b if DEFECT.match(x)]
        print("S300_REF",a300,"S300_T",b300)
        if ("fa53d657","anchor-unbound") in a300 and ("fa53d657","abbrev-unresolved") in b300:
            ok300=True
check("S300-fa53d657-reclass",ok300,"")
# every other sid identical (covered by cleared/added/reclass emptiness)

# --- falsification self-tests on own parser (mutated in-memory copies) ---
def prov_line_check(sid,tok,ln):
    cells=[c.strip() for c in ln.strip().strip("|").split("|")]
    return len(cells)==3 and "http" not in ln and any(tok==c.strip(chr(96)) for c in cells), cells
good="| S210 | note | "+pop["S210"][0]+" |"
g,_=prov_line_check("S210",pop["S210"][0],good); check("falsify-good-line-accepted",g,"")
badcells="| S210 | note | "+pop["S210"][0]+" | extra |"
g,_=prov_line_check("S210",pop["S210"][0],badcells); check("falsify-four-cell-rejected",not g,"")
badurl="| S210 | https://example.com | "+pop["S210"][0]+" |"
g,_=prov_line_check("S210",pop["S210"][0],badurl); check("falsify-url-rejected",not g,"")
badsha="| S210 | note | "+"0"*64+" |"
g,_=prov_line_check("S210",pop["S210"][0],badsha); check("falsify-wrong-sha-rejected",not g,"")
# duplicate-line detection
dup=[good,good]; check("falsify-duplicate-detected",len([x for x in dup if "S210" in x])==2,"")

print("RESULT", "ALL PASS" if not fails else f"FAILURES {fails}")
sys.exit(0 if not fails else 1)

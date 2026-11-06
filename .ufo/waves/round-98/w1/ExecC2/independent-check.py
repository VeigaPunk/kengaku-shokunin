#!/usr/bin/env python3
"""Own check — no round98 counter, no frozen gate. Inputs: POP (frozen table parsed from counter source),
git show T:<path> digests, gate-T.txt BIND/DEFECT lines kept from the frozen gate run."""
import re, subprocess, hashlib
T="8e37fc65d5649bb37166fdd6b1657445a8cb55b9"
src=open("clone-T/plans/round98_c2_nested_bind.py").read()
m=re.search(r"POP: dict\[str, tuple\[str, str\]\] = \{(.*?)\n\}", src, re.S)
pop={k:(t,p) for k,t,p in re.findall(r'"(S\d+)": \("([0-9a-f]{64})", "([^"]+)"\)', m.group(1))}
print(f"POP n={len(pop)}")
srcs=subprocess.run(["git","-C","clone-T","show",f"{T}:corpus/SOURCES.md"],capture_output=True).stdout.decode()
tok=re.compile(r"sha256[ \t]+`?([0-9a-f]{64})`?")
rows={}
for line in srcs.splitlines():
    mm=re.match(r"^ {0,3}\|\s*(S\d{3,})\s*\|", line)
    if mm:
        rows.setdefault(mm.group(1),[]).extend(tok.findall(line))
bad=[(sid,rows.get(sid,[])) for sid,(token,path) in pop.items() if token not in rows.get(sid,[])]
print(f"token-in-SOURCES: {len(pop)-len(bad)}/{len(pop)}; mismatches={bad}")
mism=[]
for sid,(token,path) in sorted(pop.items(), key=lambda kv:int(kv[0][1:])):
    h=subprocess.run(["git","-C","clone-T","show",f"{T}:{path}"],capture_output=True).stdout
    d=hashlib.sha256(h).hexdigest()
    if d!=token: mism.append((sid,path,d,token))
print(f"capture digest mismatches: {len(mism)}")
for x in mism: print(x)
gate=open("gate-T.txt").read().splitlines()
binds={}
for l in gate:
    bm=re.match(r"^BIND (S\d+) capture=(\S+) by=(\S+)",l)
    if bm: binds.setdefault(bm.group(1),[]).append((bm.group(2),bm.group(3)))
ok=sum(1 for sid,(token,path) in pop.items() if (path,"provenance-row") in binds.get(sid,[]))
print(f"BIND provenance-row to expected path: {ok}/{len(pop)}")
from collections import Counter
c=Counter(l2.split()[1] for l2 in gate if l2.startswith("DEFECT "))
still=[sid for sid in pop if sid in c]
print(f"DEFECT for POP rows at T: {still}")

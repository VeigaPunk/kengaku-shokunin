#!/usr/bin/env python3
"""For each historical in-place non-mutable-cell edit, was a `supersedes S0NN —` row
ever added in any commit (same or later)?"""
import re, subprocess, sys
LANE = sys.argv[1]; P = "corpus/SOURCES.md"
COLS = ["id","source","kind","tier","scope","anchor","teaches","status","opened","recheck","used-by"]
MUT = {"status","recheck","used-by"}
ROW = re.compile(r"S\d{3,}\Z"); SUP = re.compile(r"supersedes\s+(S\d{3,})\s+—")
def git(*a): return subprocess.run(["git","-C",LANE,*a],capture_output=True,text=True)
def rows(t):
    o={}
    for l in t.splitlines():
        if not l.startswith("|"): continue
        c=[x.strip() for x in l.split("|")[1:-1]]
        if c and ROW.match(c[0]): o[c[0]]=c
    return o
commits = git("log","--reverse","--format=%H","--",P).stdout.split()
edits=[]; supers={}   # id -> list of commit index where a superseding row was added
prev={}
for n,sha in enumerate(commits):
    t = git("show",f"{sha}:{P}")
    if t.returncode: continue
    cur = rows(t.stdout)
    for rid,c in cur.items():
        if rid in prev:
            for nm,a,b in zip(COLS,prev[rid],c):
                if a!=b and nm not in MUT: edits.append((n,sha[:8],rid,nm))
        else:
            m = SUP.search(c[6]) if len(c)>6 else None
            if m: supers.setdefault(m.group(1),[]).append(n)
    prev=cur
for n,sha,rid,col in edits:
    later=[x for x in supers.get(rid,[]) if x>=n]
    print(f"EDIT {sha} {rid} {col} supersede_same_or_later={'yes@%d'%later[0] if later else 'NO'}")

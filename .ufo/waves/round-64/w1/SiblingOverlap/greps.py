#!/usr/bin/env python3
"""Sibling-overlap grep receipt — round 64 kengaku SiblingOverlap seat.

Every grep EXCLUDES the kengaku lane by its real directory name
`kengaku-shokunin/` (an earlier draft filtered on `^kengaku/`, which matches
nothing and silently let kengaku's own bytes through; this script uses the
correct prefix and is the receipt of record).
"""
import subprocess, pathlib, re, sys
ROOT = pathlib.Path("/home/vgpnk/Projects/shokunin")
LANES = sorted(p.name for p in ROOT.iterdir() if p.is_dir() and p.name.endswith("-shokunin") and p.name != "kengaku-shokunin")
PATTERNS = {
 "A_grader_corpora":  r"graders/executed|executed17|graders/SHA256SUMS|test_outputs\.py",
 "B_grader_class_census": r"network-service|grader-class|class_survey|class-survey",
 "C_grpc_kvstore":    r"grpcio|kv[._-]store|kv-store-grpc",
 "D_port_5328":       r"127\.0\.0\.1:5328|localhost:5328",
 "E_offline_replay":  r"grade\.sh|grader replay|replay the grader|offline replay",
 "F_trio":            r"\btrio\b|provenance.trio",
 "G_escape_finding":  r"DETAIL escape|finding id .ESCAPE",
}
INC = ("*.md","*.txt","*.py","*.mjs","*.sh")
print("lanes scanned (kengaku excluded):", len(LANES))
print(", ".join(LANES))
for name, pat in PATTERNS.items():
    hits = []
    for lane in LANES:
        d = ROOT/lane
        for inc in INC:
            r = subprocess.run(["grep","-rIlE","--include="+inc,pat,str(d)],capture_output=True,text=True)
            for line in r.stdout.splitlines():
                hits.append((lane, line.replace(str(ROOT)+"/","")))
    lanes_with = sorted({l for l,_ in hits})
    print(f"\n=== {name}  pattern={pat}")
    print(f"  files with hits: {len(hits)}  in lanes: {lanes_with if lanes_with else 'NONE'}")
    for lane, path in hits[:12]:
        print(f"    {lane}/{path.split('/',1)[1]}")
    if len(hits) > 12: print(f"    ... +{len(hits)-12} more")

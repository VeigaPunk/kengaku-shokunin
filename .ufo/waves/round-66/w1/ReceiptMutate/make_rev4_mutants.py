#!/usr/bin/env python3
"""Mutants for rev4 (b131e66e): the declaration scan skips any line whose first
token is LEG or ENV.

e1: declaration text carried in a `LEG … frag=` field (an exempt family).
e2: declaration text carried in an `ENV …` line (an exempt family).
"""
import pathlib
import re

FIX = pathlib.Path("/fast/scratch/hyaku/kengaku-r66/ReceiptMutate/fixtures")
RE = re.compile(r"(?i)(fabricat|nothing ran|no driver run|no live[- ]run data)")

c3 = (FIX / "c3-escalation-plus-banners-and-probe.txt").read_text().splitlines()
decl = [l for l in c3 if RE.search(l)]
header = []
for line in c3:
    if line.startswith("GRADER "):
        break
    header.append(line)
assert len(header) == 2 and header == decl[:2], (header, decl[:2])
body = [l for l in c3 if l not in header]

decl_text = "FABRICATED RECEPT - contains NO live-run data, no driver run produced this file"
e1 = []
for line in body:
    if line.startswith("LEG G1 1 "):
        line = line + " " + decl_text
    e1.append(line)
(FIX / "e1-declaration-inside-leg-frag.txt").write_text("\n".join(e1) + "\n")
hits = [l for l in e1 if l.split(" ", 1)[0] not in ("LEG", "ENV") and RE.search(l)]
print("e1 lines=%d non_exempt_hits=%d exempt_hits=%d"
      % (len(e1), len(hits), len([l for l in e1 if l.split(" ", 1)[0] in ("LEG", "ENV") and RE.search(l)])))

e2 = []
for line in body:
    if line.startswith("ENV G1 "):
        line = line + " " + decl_text
    e2.append(line)
(FIX / "e2-declaration-inside-env-line.txt").write_text("\n".join(e2) + "\n")
hits2 = [l for l in e2 if l.split(" ", 1)[0] not in ("LEG", "ENV") and RE.search(l)]
print("e2 lines=%d non_exempt_hits=%d" % (len(e2), len(hits2)))

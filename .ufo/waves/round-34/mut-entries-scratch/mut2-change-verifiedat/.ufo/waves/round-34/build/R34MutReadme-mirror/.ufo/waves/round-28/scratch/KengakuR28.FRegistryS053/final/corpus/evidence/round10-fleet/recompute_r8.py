#!/usr/bin/env python3
"""Recompute r8 SUMMARY from committed results.jsonl + FIX-O blast radius."""
import json, collections

P = "/home/vgpnk/projects/shokunin/kengaku-shokunin/corpus/evidence/round8-horizon/results.jsonl"
recs = [json.loads(l) for l in open(P)]
print("total", len(recs))

meta = [r for r in recs if r.get("cell") == "meta"]
withraw = [r for r in recs if "raw" in r]
print("meta-cell records:", len(meta), "| records with raw:", len(withraw))

by = collections.defaultdict(dict)
for r in recs:
    if "ok" in r and "pid" in r and "turn" in r:
        by[(r["cell"], r["pid"])][r["turn"]] = r

cells = sorted({c for c, _ in by})
for cell in cells:
    pids = sorted({p for c, p in by if c == cell})
    passes = sum(1 for p in pids if by[(cell, p)][max(by[(cell, p)])]["ok"])
    print(f"{cell}: {passes}/{len(pids)}")

# stored SUMMARY: A-INC 7/10, A-MONO 0/10, A-CKPT 1/10, B-corrupt-plain 3/8,
# B-corrupt-hint 3/8, B-clean-plain 6/8, B-clean-hint 6/8,
# C-conflict 4/4, C-benign 1/4, C-norule 4/4, C-MONO 4/4
claim = {"A-INC": 7, "A-MONO": 0, "A-CKPT": 1, "B-corrupt-plain": 3, "B-corrupt-hint": 3,
         "B-clean-plain": 6, "B-clean-hint": 6, "C-conflict": 4, "C-benign": 1,
         "C-norule": 4, "C-MONO": 4}
bad = []
for cell, want in claim.items():
    if cell.startswith("C-"):
        rs = [r for r in recs if r["cell"] == cell and "ok" in r]
        passes = sum(1 for r in rs if r["ok"])
        if passes != want:
            bad.append((cell, want, passes, len(rs)))
        continue
    pids = sorted({p for c, p in by if c == cell})
    passes = sum(1 for p in pids if by[(cell, p)][max(by[(cell, p)])]["ok"])
    if passes != want:
        bad.append((cell, want, passes, len(pids)))
print("SUMMARY mismatches:", bad if bad else "none — stored SUMMARY reproduces")

# finish=stop and parse stats over raw-carrying records
stops = collections.Counter(r.get("finish") for r in recs if "raw" in r)
print("finish reasons:", dict(stops))
pf = sum(1 for r in recs if "raw" in r and r.get("got") is None)
print("got=null (parse-fail):", pf)

# FIX-O blast radius: ok &= not over_repair -> flips where ok True and over_repair True
flips = [(r["cell"], r.get("rep"), r.get("pid")) for r in recs
         if r.get("ok") is True and r.get("over_repair") is True]
print("FIX-O would flip:", len(flips), flips)

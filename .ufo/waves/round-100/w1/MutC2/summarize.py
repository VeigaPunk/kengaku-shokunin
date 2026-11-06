#!/usr/bin/env python3
"""Summarise MutC2 results: verdict, failing legs, defect lines."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path("/fast/scratch/hyaku/kengaku-r100/MutC2")
RES = ROOT / "results"

rows = []
for p in sorted(RES.glob("*.json")):
    r = json.loads(p.read_text())
    if "legs" not in r:
        continue
    legs = r["legs"]
    fail = [k for k, v in legs.items() if v == "fail"]
    expect = r["expect"]
    if r["predicate"] == "pass":
        verdict = "PASS-as-expected" if expect == "PASS" or r.get("expect_pass") else "SURVIVED"
    elif r["predicate"] == "could-not-evaluate":
        verdict = "INCONCLUSIVE"
    else:
        verdict = "killed(expected)" if expect in fail else "killed(other)"
    rows.append((r["id"], r["kind"], expect, verdict, ",".join(fail) or "-", r["defects"], r["desc"]))

w = max(len(x[0]) for x in rows)
for mid, kind, expect, verdict, fail, defects, desc in rows:
    print(f"{mid:<4} {kind:<7} exp={expect:<5} {verdict:<17} fail={fail:<12} {desc}")
    for d in defects[:4]:
        print(f"      {d[:200]}")
print()
from collections import Counter
print(Counter(v for _, _, _, v, _, _, _ in rows))
print("total", len(rows))

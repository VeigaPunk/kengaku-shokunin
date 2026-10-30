#!/usr/bin/env python3
"""C1MutClassifier: why are M01-M03 equivalent?

M01/M02/M03 flip the result of join() for the {K,N}, {K,L}/{N,L} and {B,Q} pairs.
The reachability probe shows their branch bodies never execute.  This probe records
every *pair* join() is actually called with over the three corpora, so the report can
state which lattice cases are live and which are dead code.

usage: joinprobe.py
"""
from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE / "lane"
CAP = HERE / "capture"
ADVDIR = LANE / ".ufo/waves/round-53/w1/C1ExecAdvCases"
TESTS_INDEX = LANE / "corpus/evidence/round53/tests-index.json"

src = (LANE / "plans/round53_c1_classify.py").read_text()
patched = src.replace(
    "def join(a: str, b: str) -> str:\n",
    "def join(a: str, b: str) -> str:\n    __JOINS.append((a, b))\n", 1)
assert patched != src
tmp = HERE / "mutants" / "_join_probe.py"
tmp.write_text(patched)
spec = importlib.util.spec_from_file_location("join_probe", tmp)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.__JOINS = []
# the counter list must live in the module globals
src2 = patched.replace("from __future__ import annotations",
                       "from __future__ import annotations\n__JOINS = []", 1)
tmp.write_text(src2)
spec = importlib.util.spec_from_file_location("join_probe", tmp)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

adv = json.loads((ADVDIR / "cases.json").read_text())
idx = json.loads(TESTS_INDEX.read_text())["tests"]
srcs = [("selftest:" + n, (m.HDR + s) if s else "") for n, s, _w in m.CASES]
srcs += [("adv:" + c["id"], c["source"]) for c in adv]
srcs += [("pop:" + t["file"], (CAP / t["file"]).read_text(encoding="utf-8", errors="replace"))
         for t in idx]

per = Counter()
total = 0
for tag, s in srcs:
    before = len(m.__JOINS)
    try:
        m.classify_detail(s)
    except Exception as e:  # noqa: BLE001
        print("ERR", tag, e)
    for a, b in m.__JOINS[before:]:
        per[(a, b)] += 1
        total += 1

print(f"join() calls over the three corpora: {total}")
print(f"{'pair':12s} {'calls':>7s}   lattice case")
for (a, b), n in sorted(per.items(), key=lambda kv: -kv[1]):
    s = {a, b}
    if a == b:
        case = "a == b -> return a (identity)"
    elif s == {"K", "B"}:
        case = "{K,B} -> B  (MUTATED-BY? no: M-family here is {K,N}/{K,L}/{B,Q})"
    elif s == {"K", "N"}:
        case = "{K,N} -> N   <-- M01 flips this to K"
    elif s == {"K", "L"} or s == {"N", "L"}:
        case = "{K,L}/{N,L} -> L   <-- M02 flips this to N"
    elif s == {"B", "Q"}:
        case = "{B,Q} -> Q   <-- M03 flips this to B"
    else:
        case = "unmatched -> X"
    print(f"{a}+{b:<10s} {n:7d}   {case}")
missing = []
for pair in [("K", "N"), ("K", "L"), ("N", "L"), ("B", "Q")]:
    if per.get(pair, 0) == 0:
        missing.append(pair)
print(f"\nlattice pairs never joined: {missing}")
(HERE / "join-pairs.json").write_text(json.dumps(
    {"total_calls": total, "pairs": {f"{a}+{b}": n for (a, b), n in per.items()},
     "never_joined": [f"{a}+{b}" for a, b in missing]}, indent=1))

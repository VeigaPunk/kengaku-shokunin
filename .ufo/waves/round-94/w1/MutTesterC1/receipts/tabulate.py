#!/usr/bin/env python3
"""Tabulate mutant receipts vs pristine baselines.

A mutant is KILLED in a situation if its receipt differs from the pristine
baseline on any semantic line (LEGS / TARGET / DEFECT / PREDICATE / rc).
"""
import re
import sys
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r94/MutTesterC1")

SEM = re.compile(r"^(LEGS |TARGET |DEFECT |PREDICATE |rc=)")


def semantic(p: Path) -> list[str]:
    return [l for l in p.read_text().splitlines() if SEM.match(l)]


def short(defect: str) -> str:
    d = defect.replace("DEFECT ", "")
    return (d[:100] + "…") if len(d) > 100 else d


sits = [("T", "b-T"), ("FL", "b-fixture-ledger-only"), ("FS", "b-fixture-member-swap")]
base = {s: semantic(S / f"out/{b}.txt") for s, b in sits}

print("| mutant | situation | verdict | first semantic delta vs pristine |")
print("|---|---|---|---|")
rows = {}
for mdir in sorted((S / "out").glob("m*-T.txt")):
    name = mdir.stem[: -len("-T")]
    killed_sits = []
    deltas = {}
    for s, b in sits:
        f = S / f"out/{name}-{s}.txt"
        if not f.exists():
            rows[(name, s)] = "MISSING"
            continue
        got = semantic(f)
        if got == base[s]:
            rows[(name, s)] = "identical"
        else:
            rows[(name, s)] = "DIFFERS"
            killed_sits.append(s)
            for a, g in zip(base[s], got):
                if a != g:
                    deltas[s] = f"`{a.strip()[:90]}` → `{g.strip()[:90]}`"
                    break
            else:
                deltas[s] = "line-set differs"
    if killed_sits:
        print(f"| {name} | {','.join(killed_sits)} | KILLED | {'; '.join(deltas[s] for s in killed_sits)} |")
    else:
        print(f"| {name} | T,FL,FS | SURVIVES | (all receipts identical to pristine) |")

extra = [("m03m04-l5-coverage-and-l6-counts", [("T", "b-T")])]
for name, sitlist in extra:
    for s, b in sitlist:
        f = S / f"out/{name}-{s}.txt"
        if not f.exists():
            continue
        got = semantic(f)
        print(f"| {name} | {s} | {'identical' if got == base[s] else 'DIFFERS'} | {('; '.join(g.strip() for g in got))[:200]} |")

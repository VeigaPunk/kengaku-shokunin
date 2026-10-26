#!/usr/bin/env python3
"""Compare the round-40 carried direction cells with round-42's re-derived ones.
First table row per id wins; direction cell = 3 for X rows, 4 for XO rows."""
import re, sys
LANE = sys.argv[1]
def table(path, pat):
    out = {}
    for line in open(path, encoding="utf-8"):
        if not line.startswith("| "):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if cells and re.fullmatch(pat, cells[0]) and cells[0] not in out:
            out[cells[0]] = cells
    return out
anchor40 = table(f"{LANE}/.ufo/waves/round-40/falsify/F40XMutAnchor.md", r"X\d+\Z")
order40 = table(f"{LANE}/.ufo/waves/round-40/falsify/F40XMutLedgerOrder.md", r"XO\d+\Z")
wit = {}
for line in open(f"{LANE}/.ufo/waves/round-42/claims/witness-run.txt", encoding="utf-8"):
    m = re.match(r"MUTANT (X\w+) \w+ (\S+) killed by=(\S+) attributed=(\S+)", line)
    if m:
        wit[m.group(1)] = (m.group(2), m.group(3), m.group(4))
carried = ["X1","X3","X6","X7","X9","X12","X13","X14","X15","XO1","XO3","XO5","XO6","XO7"]
diff = []
for mid in carried:
    row = order40[mid] if mid.startswith("XO") else anchor40[mid]
    label = row[-2]  # direction cell: replacement cells may contain a literal pipe
    head = label.split("/")[0]
    declared, fixture, attr = wit[mid]
    same = head == declared
    if not same:
        diff.append(mid)
    print(f"CARRIED {mid} round40={label:<24} round42={declared:<10} "
          f"{'same' if same else 'DIFFERS'} fixture={fixture} attributed={attr}")
print(f"CARRIED-DIRECTIONS total={len(carried)} differ={len(diff)} ids={','.join(diff) or '-'}")

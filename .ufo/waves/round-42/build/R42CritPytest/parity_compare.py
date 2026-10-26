#!/usr/bin/env python3
"""Compare the real-pytest verdicts with the frozen receipt's per-test letters; extract the in-sandbox runtime
banner and each failing node's exception class from the saved pytest logs."""
import json
import pathlib
import re
import sys

scratch = pathlib.Path(sys.argv[1]).resolve()
receipt = pathlib.Path(sys.argv[2]).resolve()
SUF = sys.argv[3] if len(sys.argv) > 3 else ""
rows = {r["cid"]: r for r in json.loads((scratch / f"pytest-parity{SUF}.json").read_text())}

rec = {}
for line in receipt.read_text().splitlines():
    m = re.match(r"CASE (\S+) predicted=\S+ observed=\S+ tests=(\w{3}) predicted_tests=\w{3} match=\S+ "
                 r"regrade=(\S+)", line)
    if m:
        rec[m.group(1)] = (m.group(2), m.group(3))

BADGE = re.compile(r"^platform .*Python (\S+), pytest-(\S+)")
CLASS = re.compile(r"E\s+(\w+(?:Error|Exception)):")

if set(rec) != set(rows):
    print(f"SETUP receipt parsed {len(rec)} cases, driver ran {len(rows)}; cid sets differ: "
          f"{sorted(set(rows) - set(rec))} / {sorted(set(rec) - set(rows))}", file=sys.stderr)
    raise SystemExit(2)

print(f"{'case':28} {'receipt':8} {'pytest':7} {'same':5} rc1 rc2 regrade  failing-node error classes")
ok = 0
for cid, r in rows.items():
    rt, rregrade = rec[cid]
    same = rt == r["pytest"]
    ok += same
    cls = set()
    for run in (1, 2):
        for line in (scratch / f"pytest-out{SUF}" / f"{cid}.run{run}.out").read_text().splitlines():
            m = CLASS.search(line)
            if m:
                cls.add(m.group(1))
    print(f"{cid:28} {rt:8} {r['pytest']:7} {'yes' if same else 'NO':5} {r['rc'][0]}   {r['rc'][1]}   "
          f"{r['pytest2']:8} {','.join(sorted(cls)) or '-'}")
print(f"parity cases={len(rows)} same={ok} differ={len(rows) - ok}")
print(f"receipt regrade column: {sorted(set(v[1] for v in rec.values()))}")

banner = None
for line in (scratch / f"pytest-out{SUF}" / "lookup-28.run1.out").read_text().splitlines():
    m = BADGE.match(line)
    if m:
        banner = m
print(f"in-sandbox banner: python={banner.group(1)} pytest={banner.group(2)}" if banner else "in-sandbox banner: MISSING")
warn = 0
for p in sorted((scratch / f"pytest-out{SUF}").glob("*.out")):
    for line in p.read_text().splitlines():
        if "warning" in line.lower():
            warn += 1
            print(f"WARN {p.name}: {line.strip()}")
print(f"warning lines={warn}")

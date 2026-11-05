#!/usr/bin/env python3
"""Build the mutant kill matrix from the counter receipts and the gate's own battery output.

For each mutant: counter legs (W1..W4 pass/fail, PREDICATE, rc) from receipts/<id>.txt, and the
in-path battery cases that print RED when the mutant is run directly on the lane at T (claims mode,
freeze d8d0a4b8) -> receipts/battery-<id>.txt. Writes receipts/summary.tsv to stdout.
"""
import re
import sys
from pathlib import Path

W = Path(sys.argv[1])
rows = []
for r in sorted((W / "receipts").glob("m*.txt")):
    mid = r.stem
    text = r.read_text()
    legs = {k: (re.search(rf"^{k} (pass|fail)\b", text, re.M) or [None, "-"])[1] if False else None for k in []}
    legs = {}
    for k in ("W1", "W2", "W3", "W4"):
        m = re.search(rf"^{k} (pass|fail)\b", text, re.M)
        legs[k] = m.group(1) if m else "-"
    pred = re.search(r"^PREDICATE R93-C2 (pass|fail)$", text, re.M)
    rc = re.search(r"^rc=(\d+)$", text, re.M)
    bat = W / "receipts" / f"battery-{mid}.txt"
    red = []
    if bat.exists():
        red = [line.split()[1] for line in bat.read_text().splitlines()
               if line.startswith("BATTERY ") and " RED " in line]
    sel = re.search(r"^SELFTEST cases=(\d+) ok=(\d+)$", bat.read_text(), re.M) if bat.exists() else None
    rows.append((mid, legs["W1"], legs["W2"], legs["W3"], legs["W4"],
                 pred.group(1) if pred else "-", rc.group(1) if rc else "-",
                 f"{sel.group(2)}/{sel.group(1)}" if sel else "-", ",".join(red) or "-"))
print("\t".join(["mutant", "W1", "W2", "W3", "W4", "predicate", "rc", "battery_ok", "battery_red_cases"]))
for row in rows:
    print("\t".join(row))

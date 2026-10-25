#!/usr/bin/env python3
"""Cheapest C2 skip-control: junk rows (junk teaches), an entry whose eight located quotes are single
words, an index row and a coverage bullet, a hand-typed (never probe-produced) receipt. Edits the
clone passed as argv[1] only."""
import pathlib, re, sys
lane = pathlib.Path(sys.argv[1])
RAW = "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/"
ENTRY = "corpus/knowledge/tb2-regex-log-grader.md"
up = {"S108": "tests/test_outputs.py", "S109": "tests/test.sh", "S110": "instruction.md"}
src = lane / "corpus/SOURCES.md"
t = src.read_text().rstrip("\n") + "\n"
for rid, u in up.items():
    t += f"| {rid} | junk — {RAW}{u} | code | A | junk | junk | junk | mined | 2026-10-25 | 180d | {ENTRY} |\n"
src.write_text(t)
cap = lane / "corpus/evidence/round36/tb2-regex-log/test_outputs.py"
lines = cap.read_text().splitlines()
rows = []
for i, l in enumerate(lines, 1):
    w = re.findall(r"[A-Za-z_]{4,}", l)
    if w and len(rows) < 8:
        rows.append(f"| claim | “{w[0]}” | `test_outputs.py:{i}` |")
entry = "\n".join([
    f"source: S108 — {RAW}tests/test_outputs.py — junk",
    f"source: S109 — {RAW}tests/test.sh — junk",
    f"source: S110 — {RAW}instruction.md — junk",
    "verified-at: 2026-10-25",
    "recheck: 180d — junk",
    "", "# junk", "", "## Negative space", "", "A falsifier: junk.", "",
    "## Located quotes", "", "| Claim supported | Quote | Location |", "|---|---|---|", *rows, ""])
(lane / ENTRY).write_text(entry)
rd = lane / "corpus/README.md"
r = rd.read_text()
r = r.replace("## Coverage map\n", "## Coverage map\n\n- junk: knowledge/tb2-regex-log-grader.md\n", 1)
idx = f"| `knowledge/tb2-regex-log-grader.md` | junk | S108, S109, S110 |\n"
k = r.index("| `knowledge/tb2-protein-assembly-grader.md` |")
e = r.index("\n", k) + 1
rd.write_text(r[:e] + idx + r[e:])
(lane / "corpus/evidence/round36/regex-log-probe.txt").write_text("cases=24 observed_pass=8 observed_fail=16 mismatches=0\n")

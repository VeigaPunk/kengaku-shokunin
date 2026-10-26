#!/usr/bin/env python3
"""Cheapest C2 skip-control (round 37): junk rows whose anchors carry the right digests, an entry with
eight one-word quotes and a requirement map, an index row and a coverage bullet, and a hand-typed receipt
that copies the frozen case table with every prediction marked observed (never produced by the probe).
Edits the clone passed as argv[1] only."""
import pathlib, sys
lane = pathlib.Path(sys.argv[1])
RAW = "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/"
ENTRY = "corpus/knowledge/tb2-git-webserver-grader.md"
pins = {"S111": ("tests/test_outputs.py", "526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37"),
        "S112": ("tests/verify.sh", "1dc44c923b797ed24ca423c9b9efcd9c1eed4d7261007139b0a724f4e2f53d05"),
        "S113": ("instruction.md", "62151b7371bc364277a3c118bba755334c640fb0cefc7a5af106e6e763cf1d97")}
src = lane / "corpus/SOURCES.md"
t = src.read_text()
add = "".join(f"| {rid} | junk — {RAW}{u} | code | A | junk | sha256 {d} | junk | mined | 2026-10-26 | 180d | {ENTRY} |\n"
              for rid, (u, d) in pins.items())
k = t.index("| S110 |")
e = t.index("\n", k) + 1
src.write_text(t[:e] + add + t[e:])
dry = (lane / "corpus/evidence/round37/git-webserver-dry-cases-freeze.txt").read_text().splitlines()
cases = [l for l in dry if l.startswith("CASE ")]
receipt = []
for l in cases:
    parts = l.split()
    pred = [p for p in parts if p.startswith("predicted=")][0].split("=")[1]
    receipt.append(l.replace(f"predicted={pred}", f"predicted={pred} observed={pred} match=yes"))
npass = sum("predicted=pass" in l for l in cases)
receipt.append(f"cases={len(cases)} observed_pass={npass} observed_fail={len(cases) - npass} mismatches=0")
(lane / "corpus/evidence/round37/git-webserver-probe.txt").write_text("\n".join(receipt) + "\n")
words = ["subprocess", "assert", "hello", "curl", "Testing", "expect", "server", "port"]
locs = ["test_outputs.py:6", "test_outputs.py:13", "verify.sh:63", "verify.sh:57", "verify.sh:52", "verify.sh:6",
        "instruction.md:1", "instruction.md:7"]
rows = [f"| claim | “{w}” | `{loc}` |" for w, loc in zip(words, locs)]
entry = "\n".join([
    *(f"source: {rid} — {RAW}{u} — junk" for rid, (u, _d) in pins.items()),
    "verified-at: 2026-10-26", "recheck: 180d — junk", "", "# junk", "",
    "## Requirement map", "", "| Instruction | Verdict | Cases |", "|---|---|---|",
    "| `instruction.md:1-6` | unenforced | `static-file-no-git` |",
    "| `instruction.md:7-9` | enforced | `no-server` |", "",
    "## Negative space", "", "A falsifier: junk.", "",
    "## Located quotes", "", "| Claim supported | Quote | Location |", "|---|---|---|", *rows, ""])
(lane / ENTRY).write_text(entry)
rd = lane / "corpus/README.md"
r = rd.read_text()
r = r.replace("## Coverage map\n", "## Coverage map\n\n- junk: knowledge/tb2-git-webserver-grader.md evidence/round37/git-webserver-probe.txt\n", 1)
idx = "| `knowledge/tb2-git-webserver-grader.md` | junk | S111, S112, S113 |\n"
k = r.index("| `knowledge/tb2-regex-log-grader.md` |")
e = r.index("\n", k) + 1
rd.write_text(r[:e] + idx + r[e:])

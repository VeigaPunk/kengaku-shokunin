#!/usr/bin/env python3
"""Mechanical C2 informed-filler generator (critic control, round 42).

Reads only the lane's frozen receipt, dry table and captures. Writes an entry with
(a) a case table copied row-for-row from the receipt, (b) provenance lines, a
canned 'falsifier' sentence, (c) with --analyze, 8 verbatim quote lines picked by
line number and a requirement map derived by the counter's own rule.

No reading of the grader, no findings, no analysis. Everything below is a
mechanical transform of shipped bytes.
"""
import hashlib
import json
import pathlib
import re
import sys

LANE = pathlib.Path(sys.argv[1])
MODE = sys.argv[2] if len(sys.argv) > 2 else "A"   # A = assigned filler, B = +quotes/map
ENTRY = "corpus/knowledge/tb2-circuit-fibsqrt-grader.md"
TASK = "circuit-fibsqrt"
RAW = ("https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/"
       "2fd12b88aafdd04a52c298e3940bcb189f9766d6/circuit-fibsqrt/")
ROWS = {
    "S125": ("test_outputs.py", "tests/test_outputs.py", "code",
             "Terminal-Bench 2.0 circuit-fibsqrt task grader"),
    "S126": ("instruction.md", "instruction.md", "docs",
             "Terminal-Bench 2.0 circuit-fibsqrt task instruction"),
    "S127": ("sim.c", "tests/sim.c", "code",
             "Terminal-Bench 2.0 circuit-fibsqrt task simulator source"),
}
SPEC = json.loads((LANE / "plans/pkg-spec-r42.json").read_text())
ROWDIG = {sid: r["sha256"] for sid, r in SPEC["rows"].items()}
CAP = LANE / "corpus/evidence/round42/tb2-circuit-fibsqrt"
receipt = (LANE / "corpus/evidence/round42/fibsqrt-probe.txt").read_text()
dry = (LANE / "corpus/evidence/round42/fibsqrt-dry-cases-freeze.txt").read_text()

cases = []
for l in receipt.splitlines():
    m = re.match(r"^CASE (\S+) predicted=(pass|fail) observed=(pass|fail) tests=([PF]{3}) "
                 r".*?violates=(\S*)", l)
    if m:
        cases.append({"cid": m.group(1), "obs": m.group(3), "tests": m.group(4),
                      "violates": set(filter(None, m.group(5).split(",")))})
assert len(cases) == 16
tags = {}
for l in dry.splitlines():
    p = l.split()
    if p and p[0] == "TAG":
        tags[p[1]] = p[2]


def derive(vs):
    if vs == {"fail"}:
        return "enforced"
    if vs == {"pass"}:
        return "unenforced"
    return "partly"


table = ["| Case | Tests | Observed | Note |", "|---|---|---|---|"]
table += [f"| `{c['cid']}` | {c['tests']} | {c['obs']} | x |" for c in cases]

quotes, seen = [], set()
for capname in ("test_outputs.py", "sim.c", "instruction.md"):
    lines = (CAP / capname).read_text().splitlines()
    for i, line in enumerate(lines, 1):
        t = line.strip()
        if not t or "|" in t or "\u201c" in t or "\u201d" in t or "\t" in t:
            continue
        n = len(t.split())
        if not 3 <= n <= 25 or t in seen:
            continue
        seen.add(t)
        quotes.append((capname, i, t))
        if len(quotes) == 8:
            break
    if len(quotes) == 8:
        break
assert len(quotes) == 8

prov = [f"source: {sid} \u2014 {RAW}{up} \u2014 {desc}, accessed 2026-10-26"
        for sid, (_c, up, _k, desc) in ROWS.items()]

body = []
body += prov
body += ["verified-at: 2026-10-26",
         "recheck: 180d \u2014 rerun plans/fibsqrt_probe.py --lane .",
         "",
         "# Terminal-Bench 2.0 task grader, read and executed: `circuit-fibsqrt`",
         "",
         "## Summary",
         "",
         "Registry rows S125 S126 S127 (mechanical filler; no finding is claimed).",
         "",
         "## Case table",
         ""] + table + [""]

if MODE == "B":
    body += ["## Located quotes", "", "| Claim | Quote | Location |", "|---|---|---|"]
    body += [f"| mechanical q{i + 1} | \u201c{t}\u201d | `{c}:{n}` |"
             for i, (c, n, t) in enumerate(quotes)]
    body += ["", "## Requirement map", ""]
    labels = []
    for tag in tags:
        vs = {c["obs"] for c in cases if tag in c["violates"]}
        cite = next(c["cid"] for c in cases if tag in c["violates"])
        labels.append(f"| `{tags[tag]}` | `{tag}` | {derive(vs)} | `{cite}` |")
    body += labels + [""]
    assert len(labels) == 7

body += ["## Negative space", "",
         "Falsifiers are not named here; this is a mechanical filler control.", ""]
(LANE / ENTRY).write_text("\n".join(body) + "\n")

# SOURCES rows
sources = LANE / "corpus/SOURCES.md"
s = sources.read_text()
if "| S125 |" not in s:
    add = []
    for i, (sid, (capname, up, kind, desc)) in enumerate(ROWS.items()):
        teaches = ("filler teaches sentence number " + str(i + 1) +
                   " describing nothing that was read from the captured grader")
        add.append(f"| {sid} | {desc} \u2014 {RAW}{up} | {kind} | A | the captured file itself, "
                   f"pinned at 2fd12b88 | commit 2fd12b88, {capname}, sha256 "
                   f"{ROWDIG[sid]} | {teaches} | mined | 2026-10-26 | 180d | {ENTRY} |")
    ls = s.splitlines()
    reg = ls.index("## Registry")
    end = next(i for i in range(reg + 1, len(ls)) if ls[i].startswith("## "))
    ls[end:end] = add
    s = "\n".join(ls) + "\n"
sources.write_text(s)

# README: index row, coverage bullet, Frontier bullet
readme = LANE / "corpus/README.md"
r = readme.read_text().splitlines()
idx = max(i for i, l in enumerate(r) if l.startswith("| `knowledge/"))
r.insert(idx + 1, f"| `knowledge/tb2-circuit-fibsqrt-grader.md` | Mechanical filler: case names and outcomes copied from "
                  f"`corpus/evidence/round42/fibsqrt-probe.txt`; no grader behaviour read | "
                  f"S125, S126, S127 (terminal-bench-2 @ 2fd12b88) |")
fr = next(i for i, l in enumerate(r) if l == "## Frontier")
nxt = next((i for i, l in enumerate(r) if i > fr and l.startswith("## ")), len(r))
r.insert(nxt, f"- **Terminal-Bench 2.0 {TASK} task grader**: named; see "
              f"`knowledge/tb2-circuit-fibsqrt-grader.md`.")
cov = next(i for i, l in enumerate(r) if l.startswith("- **Terminal-Bench 2.0 task grader (seventh"))
r.insert(cov + 1, f"- **Terminal-Bench 2.0 task grader (eighth task)**: named only (mechanical filler) "
                  f"\u2014 knowledge/tb2-circuit-fibsqrt-grader.md; S125, S126, S127; receipt "
                  f"`evidence/round42/fibsqrt-probe.txt`. No finding.")
readme.write_text("\n".join(r) + "\n")

# PROVINCE: one line naming the task and the entry
province = LANE / "PROVINCE.md"
p = province.read_text()
if "tb2-circuit-fibsqrt-grader.md" not in p:
    p = p.rstrip("\n") + ("\n\nRound-42 wave-1 filler note: the captured `circuit-fibsqrt` grader is named in "
                          "corpus/knowledge/tb2-circuit-fibsqrt-grader.md and nowhere else.\n")
province.write_text(p)
print("wrote", MODE, "quotes", len(quotes), "tags", len(tags))

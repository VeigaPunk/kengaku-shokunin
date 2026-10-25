#!/usr/bin/env python3
import json

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/"
QUOTES = [
    ("plans/round-29-claims.md", 93, "until complete eligible second-seat source/number re-reads return on exact final bytes, writer differs,"),
    ("plans/round-29-claims.md", 94, "plain anchored VERDICT: PASS exists, and actual admitting commit includes reports/registry, entry,"),
    ("plans/round-29-claims.md", 95, "Q13 is structural only; digest/actual-commit proof separate."),
    ("plans/round-29-claims.md", 22, "Measurement revision is the branch/helper landed revision, never detached HEAD."),
    ("corpus/QUALITY.md", 101, "never cites a seat that has not returned."),
    ("corpus/QUALITY.md", 106, "Presence is not endorsement"),
    ("corpus/QUALITY.md", 117, "the checker grades the requested tree but does not discover that commit or interpret review conclusions."),
    ("corpus/lessons/round-28.md", 278, "First admitting commit df33fc83764975fd808b0945097b5d0c7aca3901 had two observed red checks,"),
    ("corpus/lessons/round-28.md", 279, "These are not represented as passes."),
    ("corpus/lessons/round-28.md", 263, "Q13 actual-commit result and report-byte pins are recorded after landing"),
    ("plans/gate_timing_check.py", 56, 'VERDICT_RE = re.compile(r"^VERDICT:\\s*(\\S.*?)\\s*$", re.MULTILINE)'),
]
rows = []
for path, line, quote in QUOTES:
    lines = open(LANE + path, encoding="utf-8").read().splitlines()
    rows.append({"path": path, "line": line, "found_on_line": quote in lines[line - 1],
                 "words": len(quote.split()), "quote": quote})
print(json.dumps(rows, indent=1))
print("all_found", all(r["found_on_line"] for r in rows), "max_words", max(r["words"] for r in rows))

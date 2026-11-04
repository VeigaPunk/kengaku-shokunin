#!/usr/bin/env python3
"""Q13 reachability probe for round 84's wave-directory naming (seat Reviewer2R84).

Read-only import of the committed checker; no production bytes are touched.
Usage: python3 q13_probe.py <output.txt>
"""
import json
import sys

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
sys.path.insert(0, LANE + "/plans")
import gate_timing_check as g  # noqa: E402

out = []
def emit(s):
    out.append(s)
    print(s)

round_number = 84
paths = [
    ".ufo/waves/round-84/w1/Reviewer2R84.md",
    ".ufo/waves/round-84/w1/Reviewer2R84/report.md",
    ".ufo/waves/round-84/w1/Reviewer2R84/report.txt",
    ".ufo/waves/round-84/wave2/Reviewer2R84.md",
    ".ufo/waves/round-84/falsify/Reviewer2R84.md",
]
emit("PATH SHAPE TESTS")
for p in paths:
    d = g.wave_directory(p, round_number)
    emit("  path=%-52s wave_directory=%-8r second_wave=%s" % (p, d, g.is_second_wave(d)))

report_text = ("Re-read corpus/knowledge/tb2-code-from-image-offline.md\n"
               "role: reviewer\n"
               "VERDICT: PASS - independent re-read\n")
entry_text = "source: S267 pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6\nwriter: KengakuR84\n"
candidate = "corpus/knowledge/tb2-code-from-image-offline.md"

for wdir in ("w1", "wave2"):
    seat = "Reviewer2R84"
    rep = f".ufo/waves/round-84/{wdir}/{seat}.md"
    tree = {
        candidate: g.TreeFile("100644", len(entry_text)),
        rep: g.TreeFile("100644", len(report_text)),
    }
    registry = json.dumps({"members": {seat: {"role": "reviewer", "agentId": "Reviewer2R84"}}})
    blobs = {candidate: entry_text, rep: report_text,
             f".ufo/waves/round-84/{wdir}/swarm-registry.json": registry}

    def read_blob(path, blobs=blobs):
        return blobs.get(path)

    members = g.load_members(round_number, tree, read_blob)
    citations = g.extract_citations(f"Q13 re-read `{rep}`")
    reports, unresolved = g.resolve_citations(citations, round_number, tree)
    reason = f"Q13 re-read `{rep}`"
    header = "## Gate\n\n| candidate | decision | reason |\n|---|---|---|\n"
    text = header + f"| `{candidate}` | **admit** | {reason} |\n"
    gate_found, admissions = g.parse_gate_admissions(text)
    result = g.audit_admission(admissions[0], round_number, tree, members, read_blob)
    emit("")
    emit("GATE SIMULATION dir=%s" % wdir)
    emit("  gate_found=%s admissions=%d" % (gate_found, len(admissions)))
    emit("  load_members -> %r" % (dict(members),))
    emit("  resolve_citations -> reports=%r unresolved=%r" % (sorted(reports), sorted(unresolved)))
    emit("  audit ok=%s" % result.ok)
    emit("  reasons=%r" % (list(result.reasons),))

# Same simulation but with the w1 member injected by hand, to isolate whether the
# failure is the registry filter or the citation filter.
wdir = "w1"
seat = "Reviewer2R84"
rep = f".ufo/waves/round-84/{wdir}/{seat}.md"
tree = {candidate: g.TreeFile("100644", len(entry_text)), rep: g.TreeFile("100644", len(report_text))}
blobs = {candidate: entry_text, rep: report_text}
def read_blob2(path):
    return blobs.get(path)
members = {(wdir, seat): g.SeatMember("reviewer", "Reviewer2R84")}
_, admissions = g.parse_gate_admissions(
    "## Gate\n\n| candidate | decision | reason |\n|---|---|---|\n"
    f"| `{candidate}` | **admit** | Q13 re-read `{rep}` |\n")
result = g.audit_admission(admissions[0], round_number, tree, members, read_blob2)
emit("")
emit("GATE SIMULATION dir=w1 with member injected manually")
emit("  load_members bypassed; audit ok=%s reasons=%r" % (result.ok, list(result.reasons)))

with open(sys.argv[1], "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")

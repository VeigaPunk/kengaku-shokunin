#!/usr/bin/env python3
"""Mutants for rev3 (06270270): the declaration scan is header-only (lines before
the first `GRADER ` line).

d3: c3 with the two declaration header lines moved to just after the GRADER line.
    Same bytes as c3 otherwise -- tests whether scope is a boundary or a bypass.
q6: committed receipt + correct PROBE line + instrument version r65-c1/0
    (independent check that a true PROBE line does not excuse a wrong header).
"""
import pathlib
import re

FIX = pathlib.Path("/fast/scratch/hyaku/kengaku-r66/ReceiptMutate/fixtures")
RE = re.compile(r"(?i)(fabricat|nothing ran|no driver run|no live[- ]run data)")

c3 = (FIX / "c3-escalation-plus-banners-and-probe.txt").read_text().splitlines()
grader_at = next(i for i, line in enumerate(c3) if line.startswith("GRADER "))
before, rest = c3[:grader_at], c3[grader_at:]
assert len(before) == 2 and all(RE.search(line) for line in before), before
d3 = [rest[0]] + before + rest[1:]          # GRADER first, declarations right after
d3hdr = d3[:next(i for i, line in enumerate(d3) if line.startswith("GRADER "))]
assert not any(RE.search(line) for line in d3hdr)
(FIX / "d3-evasion-declarations-moved-after-grader.txt").write_text("\n".join(d3) + "\n")
print("d3 lines=%d header=%r declaration_hits=%d (all below the GRADER line)"
      % (len(d3), d3hdr, len([l for l in d3 if RE.search(l)])))

com = pathlib.Path(
    "/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round65/sqlite-gcov-probe.txt"
).read_text().splitlines()
old = "# instrument plans/round65_c1_sqlite_probe.py version=r65-c1/1"
assert old in com
probe = ("PROBE sha256=f44b72834d8662cb6986e192dfbdf236daf6c99a174768294e504f7b634db4eb")
q6 = []
for line in com:
    if line == old:
        q6.append("# instrument plans/round65_c1_sqlite_probe.py version=r65-c1/0")
    else:
        q6.append(line)
    if line.startswith("AMALG "):
        q6.append(probe)
(FIX / "q6-true-probe-line-wrong-header-version.txt").write_text("\n".join(q6) + "\n")
print("q6 lines=%d probe_lines=%d header_wrong=%s"
      % (len(q6), sum(1 for l in q6 if l.startswith("PROBE ")),
         any("version=r65-c1/0" in l for l in q6)))

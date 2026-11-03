#!/usr/bin/env python3
"""Mutants aimed at the new `fabrication-declaration` check (revision 92eee57).

d1: provenance words renamed but everything else identical to c3 -> blacklist evasion.
d2: committed receipt with one live-plausible free-text fragment containing the
    blacklisted word -> false-positive surface.
Also prints the declaration-hit count of every fixture.
"""
import pathlib
import re

FIX = pathlib.Path("/fast/scratch/hyaku/kengaku-r66/ReceiptMutate/fixtures")
RE = re.compile(r"(?i)(fabricat|nothing ran|no driver run|no live[- ]run data)")

c3 = (FIX / "c3-escalation-plus-banners-and-probe.txt").read_text().splitlines()
subs = [
    ("# FABRICATED RECEPT — ClaimFalsifier-3 cheapest-path attack, contains NO live-run data",
     "# SYNTHETIC RECEPT — values transcribed from the frozen claim text, nothing executed"),
    ("# No compile, no bwrap sandbox, no driver run, no file walk produced this file.",
     "# No compile, no bwrap sandbox, no file walk: values were transcribed."),
    ('driver="fabricated - nothing ran"', 'driver="transcribed values"'),
]
out = []
used = set()
for line in c3:
    for old, new in subs:
        if old in line:
            line = line.replace(old, new)
            used.add(old)
    line = line.replace("frag=fabricated", "frag=synthetic")
    out.append(line)
assert len(used) == len(subs), used
text = "\n".join(out) + "\n"
assert not RE.search(text), [l for l in text.splitlines() if RE.search(l)]
(FIX / "d1-evasion-renamed-provenance.txt").write_text(text)
print("d1 lines=%d hits=%d" % (len(out), len([l for l in out if RE.search(l)])))

com = pathlib.Path(
    "/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round65/sqlite-gcov-probe.txt"
).read_text().splitlines()
old = ("LEG G3 3 test_gcov_enabled F exc=AssertionError "
       "frag=No .gcda files found, gcov instrumentation may not be enabled")
assert old in com
new = old + " (sqlite3 binary fabricated by harness)"
d2 = [new if l == old else l for l in com]
(FIX / "d2-false-positive-live-fragment-words.txt").write_text("\n".join(d2) + "\n")
print("d2 lines=%d hits=%d" % (len(d2), len([l for l in d2 if RE.search(l)])))

for path in sorted(FIX.glob("*.txt")):
    hits = [l for l in path.read_text().splitlines() if RE.search(l)]
    print("%-48s declaration_hits=%d %s"
          % (path.stem, len(hits), hits[0][:80] if hits else ""))

#!/usr/bin/env python3
"""C2 skip-control (informed filler): keep every structure the C2 counter parses, replace the substance.

Splices from the genuine entry: the four header lines (source x2, verified-at, recheck), the
'## Located quotes' block, the '## Requirement map' table rows, the '## Negative space' block.
Inserts false prose everywhere the gate and the counter do not read: Summary, a fabricated
'Findings' section, and false sentences inside the map's prose.
"""
import sys, pathlib

src = pathlib.Path(sys.argv[1]).read_text()
out = pathlib.Path(sys.argv[2])

def block(text, start, end):
    i = text.index(start)
    j = len(text) if end is None else text.index(end, i)
    return text[i:j]

head = "".join(l + "\n" for l in src.splitlines()[:4])
quotes = block(src, "## Located quotes", "## Requirement map")
mapsec = block(src, "## Requirement map", "## Negative space")
# keep only the table from the map section, then add false prose after it
lines = mapsec.splitlines()
tbl = [l for l in lines if l.startswith("|") and "instruction.md:" in l]
assert len(tbl) == 7, len(tbl)
neg = block(src, "## Negative space", None)

body = f"""{head}
# Terminal-Bench 2.0 task grader, read and executed: `build-pmars`

## Summary

**Informed filler (seat F38CritSkipControls).** This entry keeps the receipt, the captures, the anchor rows and
every structure the round-38 C2 counter parses, and replaces all substance with claims the receipt contradicts.
If C2 prints `checks=7 defects=0` on this file, the counter does not bind the entry's prose to its own receipt.

- The probe observed `cases=22 observed_pass=22 observed_fail=0 mismatches=0`: every frozen case passes.
- `canned-shape` was never executed, and the grader rejects a canned artefact because `ldd` lists no pMARS symbol.
- The grader reads a Debian package digest and a build log, so provenance is enforced rather than inferred.
- The oracle `solution/solve.sh` was executed inside the same sandbox and the delivered binary passes all four tests.
- `canned-x11-dlopen` is observed `fail`; `path-split` is observed `fail`; `debian-is-file` is observed `fail`;
  `results-trailing-text` is observed `fail`.
- Exit status is asserted: `test_outputs.py:15` reads `e.returncode` and requires 0.
- The captured `test_outputs.py` does not match S115; the capture is from a different upstream commit.

## What this filler changes, and what it reuses

Reused verbatim: the two `source:` lines, `verified-at`, `recheck`, the 28-row quote table, the seven requirement-map
rows with their derived labels and citations, and the `## Negative space` block. Everything above and below is
fabricated; the receipt it points at was neither edited nor regenerated.

{quotes}## Requirement map

All seven labels below are in fact `enforced`: the receipt contains no passing case that violates any instruction
line, and `plans/build_pmars_probe.py` prints the same verdict for every state it stages.

| Instruction line | Tag | Label | Receipt cases cited (violating, both directions) |
|---|---|---|---|
""" + "\n".join(tbl) + f"""

Read in the other direction, the map says nothing: three of the seven tags have no violating case at all, and the
`partly` labels were chosen from a single convenient witness each.

{neg}"""
out.write_text(body)
print(f"wrote {out} bytes={len(body)}")

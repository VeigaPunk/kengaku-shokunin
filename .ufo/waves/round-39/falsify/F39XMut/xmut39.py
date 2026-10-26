#!/usr/bin/env python3
"""F39XMut (kengaku round 39, wave 2 falsify) — extra non-frozen mutants through the FROZEN counter.

Imports plans/round39_c1_verify.py from the lane clone UNMODIFIED and appends eleven extra
(old,new) mutants (XP1a..XD5c) to its MUTANTS list in memory. The frozen M01-M07 rows are reused
verbatim as the in-run control. No lane file is edited; gate copies are written under --work only.

Run: python3 xmut39.py --lane <clone> --work <scratch>
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys

LANE = (pathlib.Path(sys.argv[sys.argv.index("--lane") + 1]) if "--lane" in sys.argv
        else pathlib.Path(__file__).resolve().parent / "lane")

_spec = importlib.util.spec_from_file_location("r39v_frozen", LANE / "plans/round39_c1_verify.py")
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)

# (id, clause, dir, advertised behaviour, provenance note, old, new) — all against plans/pkg_gate.py
# at the frozen tip; every `old` occurs exactly once in the pristine gate (verified before the run).
EXTRA = [
    ("XP1a", "P1", "silence",
     "every frozen instrument is checked against its pin, not only the first TWO [same advertising "
     "sentence as M02: package-gate row 'against a spec of pinned digests ... a stub probe dies on "
     "its digest pin']; the r35 spec carries three pins",
     "F39XMut probe; generalisation of M02's [:1] narrowing to [:2]; no battery fixture corrupts "
     "pin 3 (plans/defect_ledger.py)",
     "bad = [rel for rel, dig in pins.items() if sha256(p.root / rel) != dig]",
     "bad = [rel for rel, dig in list(pins.items())[:2] if sha256(p.root / rel) != dig]"),
    ("XP1b", "P1", "silence",
     "every frozen instrument is checked against its pin, not only the LAST [same advertising "
     "sentence as M02]",
     "F39XMut probe; order-flipped counterpart of M02's [:1] narrowing",
     "bad = [rel for rel, dig in pins.items() if sha256(p.root / rel) != dig]",
     "bad = [rel for rel, dig in list(pins.items())[-1:] if sha256(p.root / rel) != dig]"),
    ("XP3a", "P3", "silence",
     "a quote one word BELOW the spec's lower word bound is a defect [gate docstring 'quote bounds "
     "... come from --spec']",
     "F39XMut probe; lower-bound counterpart of M03 (which widens the upper bound)",
     "short = [q.text[:30] for q in p.quotes if not lo <= q.words <= hi]",
     "short = [q.text[:30] for q in p.quotes if not lo - 1 <= q.words <= hi]"),
    ("XP3b", "P3", "mirror",
     "the lower word bound is not tightened by one [gate docstring 'quote bounds ... come from "
     "--spec']",
     "F39XMut probe; strict side of the lower bound (M03 covers the lax side of the upper bound)",
     "short = [q.text[:30] for q in p.quotes if not lo <= q.words <= hi]",
     "short = [q.text[:30] for q in p.quotes if not lo + 1 <= q.words <= hi]"),
    ("XP3c", "P3", "mirror",
     "the upper word bound is not tightened by one [gate docstring 'quote bounds ... come from "
     "--spec']",
     "F39XMut probe; strict side of the upper bound",
     "short = [q.text[:30] for q in p.quotes if not lo <= q.words <= hi]",
     "short = [q.text[:30] for q in p.quotes if not lo <= q.words <= hi - 1]"),
    ("XP7a", "P7", "silence",
     "a registry row carries the pinned URL on its LAST source line, however many unpinned ones "
     "precede it [package-gate row 'SOURCES rows ... against a spec of pinned digests' (indirect, "
     "as M04)]",
     "F39XMut probe; order-flipped counterpart of M04's [0]-only narrowing",
     'if prov.get(sid) != [p.spec["raw_base"] + row["upstream"]]:',
     'if (prov.get(sid) or [""])[-1] != p.spec["raw_base"] + row["upstream"]:'),
    ("XP7b", "P7", "silence",
     "a registry row's source lines are compared as a set, so a duplicated pinned line passes "
     "[package-gate row 'SOURCES rows ... against a spec of pinned digests' (indirect, as M04)]",
     "F39XMut probe; duplicate-tolerant counterpart of M04",
     'if prov.get(sid) != [p.spec["raw_base"] + row["upstream"]]:',
     'if set(prov.get(sid) or [""]) != {p.spec["raw_base"] + row["upstream"]}:'),
    ("XP7c", "P7", "silence",
     "a registry row passes when ANY of its source lines is the pinned URL [package-gate row "
     "'SOURCES rows ... against a spec of pinned digests' (indirect, as M04)]",
     "F39XMut probe; any-of counterpart of M04",
     'if prov.get(sid) != [p.spec["raw_base"] + row["upstream"]]:',
     'if not any(u == p.spec["raw_base"] + row["upstream"] for u in (prov.get(sid) or [""])):'),
    ("XD5a", "D5", "mirror",
     "the D5 tag strip also removes empty tags <> [d5m39 erratum 'after tag-strip and whitespace "
     "removal' — the strip's charset is advertised behaviour]",
     "F39XMut probe; superset-strip counterpart of M07 (which drops the strip entirely)",
     'r"<[^>]+>"',
     'r"<[^>]*>"'),
    ("XD5b", "D5", "mirror",
     "the D5 tag strip removes only letter-led tags, leaving comments and doctypes in the flat "
     "text [d5m39 erratum 'after tag-strip and whitespace removal']",
     "F39XMut probe; subset-strip counterpart of M07",
     'r"<[^>]+>"',
     'r"</?[a-zA-Z][^>]*>"'),
    ("XD5c", "D5", "mirror",
     "the D5 tag strip is greedy across a line, eating the text between two tags [d5m39 erratum "
     "'after tag-strip and whitespace removal']",
     "F39XMut probe; over-strip counterpart of M07",
     'r"<[^>]+>"',
     'r"<.*>"'),
]

m.MUTANTS = list(m.MUTANTS) + EXTRA
m.TOTAL = len(m.MUTANTS)

if __name__ == "__main__":
    sys.exit(m.main())

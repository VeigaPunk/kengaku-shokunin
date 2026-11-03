#!/usr/bin/env python3
"""Map each round 57..62 to its SCORECARD 'Round verdict' line (nearest below the round heading)."""
import re, pathlib
sc = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/SCORECARD.md").read_text(encoding="utf-8").splitlines()
cur = None
for i, ln in enumerate(sc, 1):
    m = re.match(r"^## Round (\d+)", ln)
    if m:
        cur = int(m.group(1))
    if "Round verdict" in ln and cur in (57, 58, 59, 60, 61, 62):
        text = ln.strip()
        text = text.replace("**", "")
        print(f"round-{cur}  SCORECARD.md:{i}")
        print(f"   {text[:520]}")
        print()

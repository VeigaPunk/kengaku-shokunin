#!/usr/bin/env python3
"""Read-only demo: does a `Flip check (round N): <item> - not fired` verdict hold against the cited entry?

Rule: a `not fired` verdict naming a file is RED when the entry body (outside `## Located quotes`)
carries at least one `<item>:<line>` citation of that file with no `S1xx` co-citation on the line.
Two instances only; entry paths are passed explicitly (this is the demonstration, not the tool).
"""
import re
import sys
from pathlib import Path

LANE = Path(sys.argv[1])

# (lesson, lesson line, item regex, entry)
CASES = [
    ("corpus/lessons/round-43.md", 46, r"task\.toml",
     "corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md"),
    ("corpus/lessons/round-42.md", 215, r"README\.md",
     "corpus/knowledge/tb2-circuit-fibsqrt-grader.md"),
]


def body(entry_text):
    out, skip = [], False
    for line in entry_text.splitlines():
        if line.startswith("## Located quotes"):
            skip = True
            continue
        if skip and line.startswith("## "):
            skip = False
        if not skip:
            out.append(line)
    return out


for lesson, lineno, item, entry in CASES:
    verdict_line = (LANE / lesson).read_text().splitlines()[lineno - 1]
    lines = [ln for ln in body((LANE / entry).read_text()) if re.search(item + r":\d+", ln)]
    unbacked = [ln for ln in lines if not re.search(r"S1[0-9]{2}", ln)]
    state = "fired" if unbacked else "not fired"
    recorded = "not fired" if "not fired" in verdict_line else "fired"
    print(f"INSTANCE lesson={lesson}:{lineno} item={item} recorded={recorded} "
          f"body_hits={len(lines)} unbacked={len(unbacked)} verdict_truth={state} "
          f"{'RED' if state != recorded else 'ok'}")
    for ln in unbacked[:3]:
        print(f"  unbacked {entry}: {ln.strip()[:110]}")

#!/usr/bin/env python3
"""PROVINCE.md surface resolution audit (read-only).

Extracts backticked tokens from PROVINCE.md, classifies them, and tests existence:
- lane-internal (corpus/, plans/, lessons/, knowledge/, evidence/, .ufo/, bare lane files) -> lane root
- sibling lanes (<lane>-shokunin/...) -> fleet root
- lane-attributed bare-relative pointers (tools/, scripts/, quality/, reports/) -> the lane the
  enclosing prior-art table names (hardcoded map below, from PROVINCE.md round-38 block)
- ~/* host paths -> $HOME existence test (PROVINCE documents most as ABSENT; absence matches)
Skips commands, URLs, flags, shas, prose spans.
"""
import re
import sys
from pathlib import Path

FLEET = Path("/home/vgpnk/Projects/shokunin")
LANE = FLEET / "kengaku-shokunin"
PROV = (LANE / "PROVINCE.md").read_text()

ATTRIB = {  # bare-relative token prefix -> lane that owns it (PROVINCE.md round-38 prior-art table)
    "tools/": "tameshi-shokunin",
    ".ufo/evidence/": "tameshi-shokunin",
    "scripts/": "kumitate-shokunin",
    "quality/": "mado-shokunin",
    "reports/": "kotodama-shokunin",
}
LANE_PREFIX = ("corpus/", "plans/", "lessons/", "knowledge/", "evidence/", ".ufo/")
SIB = re.compile(r"^[a-z]+-shokunin/")
LINE = re.compile(r"^(?P<p>.+\.(?:md|py|sh|txt|json|jsonl|log|mjs|ts|toml))(:\d+(-\d+)?)(?P<rest>.*)$")


def resolve(tok):
    t = tok.strip()
    if not t or " " in t or t.startswith(("http", "$", "{{")):
        return None
    if t.startswith("~/"):
        return ("home", Path.home() / t[2:])
    if SIB.match(t):
        return ("fleet", FLEET / t)
    if t.startswith(LANE_PREFIX):
        return ("lane", LANE / t)
    for pref, lane in ATTRIB.items():
        if t.startswith(pref):
            return ("fleet", FLEET / lane / t)
    if re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.+-]*\.(md|py|sh|txt|json|jsonl|log)", t):
        return ("lane?", LANE / t)
    return None


def split_line_suffix(t):
    m = LINE.match(t)
    if m and not m.group("rest").strip(".:").startswith(":"):
        return m.group("p")
    return t


tokens = re.findall(r"`([^`\n]+)`", PROV)
ok, broken, home_absent, ambiguous = [], [], [], []
seen = set()
for tok in tokens:
    r = resolve(tok)
    if r is None:
        continue
    kind, path = r
    base = split_line_suffix(tok.strip())
    if base in seen:
        continue
    seen.add(base)
    if kind == "home":
        (home_absent if not path.exists() else ok).append((base, "absent" if not path.exists() else "present"))
        continue
    target = path
    p = Path(str(target))
    exists = p.exists()
    if exists:
        ok.append((base, kind))
    elif kind == "lane?":
        ambiguous.append(base)
    else:
        broken.append((base, kind))

print("== resolved (%d):" % len(ok))
for t, k in sorted(ok):
    print("  [%s] %s" % (k, t))
print("== UNRESOLVED (%d):" % len(broken))
for t, k in sorted(broken):
    print("  [%s] %s" % (k, t))
print("== bare lane-file tokens unresolved (ambiguous base) (%d):" % len(ambiguous))
for t in sorted(ambiguous):
    print("  %s" % t)
print("== home paths absent (%d, PROVINCE documents these as historical/absent):" % len(home_absent))
for t, s in sorted(home_absent):
    print("  %s (%s)" % (t, s))

#!/usr/bin/env python3
"""Seat path check for the drafted SKILL.md section.

For every backticked token in section.md, decide whether the depth gate would
count it as a repo-relative path (contains '/', ends in .py/.md/.json/.txt/.sh/
.lst/.yml or '/', and is not a scheme:// URL) and, for those, test -e from the
lane root. Also mirror the gate's row checks (16 rows, class names, counts).
"""
import pathlib
import re
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
SECTION = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/"
                       ".ufo/waves/round-63/w1/draft/depth/section.md")
RECEIPT = LANE / "corpus/evidence/round62/class-survey.txt"

TOKEN_RE = re.compile(r"`([^`\n]+)`")
URL_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*://")
PATH_SUFFIXES = (".py", ".md", ".json", ".txt", ".sh", ".lst", ".yml")
CLASS_RE = re.compile(r"^CLASS (\S+) count=(\d+)")

text = SECTION.read_text(encoding="utf-8")
tokens = []
seen = set()
for raw in TOKEN_RE.findall(text):
    tok = raw.strip()
    if URL_RE.match(tok):
        continue
    if "/" not in tok:
        continue
    if not (tok.endswith("/") or tok.endswith(PATH_SUFFIXES)):
        continue
    if tok in seen:
        continue
    seen.add(tok)
    tokens.append(tok)

resolved, unresolved = [], []
for tok in tokens:
    (resolved if (LANE / tok).exists() else unresolved).append(tok)

print("PATH TOKENS total=%d resolved=%d unresolved=%d"
      % (len(tokens), len(resolved), len(unresolved)))
for tok in unresolved:
    print("UNRESOLVED %s" % tok)

# --- mirror the gate's table checks -------------------------------------
receipt = {}
for line in RECEIPT.read_text(encoding="utf-8").splitlines():
    m = CLASS_RE.match(line)
    if m:
        receipt[m.group(1)] = int(m.group(2))

rows, header = [], True
for line in text.splitlines():
    if not line.startswith("|"):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if all(re.fullmatch(r":?-+:?", c.replace(" ", "")) for c in cells):
        header = False
        continue
    if header:
        header = False
        continue
    rows.append(cells)

names = [re.sub(r"[\s`]", "", r[0]) for r in rows]
count_mismatch = [(r[0], r[1], receipt.get(re.sub(r"[\s`]", "", r[0])))
                  for r in rows
                  if r[1].strip("`").isdigit()
                  and int(r[1].strip("`")) != receipt.get(re.sub(r"[\s`]", "", r[0]), -1)]
print("ROWS n=%d class_match=%s count_mismatch=%d"
      % (len(rows), set(names) == set(receipt), len(count_mismatch)))
for cm in count_mismatch:
    print("COUNT-MISMATCH row=%s cell=%s receipt=%s" % cm)
missing = set(receipt) - set(names)
extra = set(names) - set(receipt)
print("CLASS missing=%s extra=%s" % (sorted(missing), sorted(extra)))
cols = sorted({len(r) for r in rows})
print("CELL COUNTS per row: %s" % cols)

# --- per-row pointer cell: at least one path token, at least one resolves -
row_bad = []
for r in rows:
    toks = []
    for raw in TOKEN_RE.findall(" ".join(r)):
        t = raw.strip()
        if URL_RE.match(t) or "/" not in t:
            continue
        if not (t.endswith("/") or t.endswith(PATH_SUFFIXES)):
            continue
        toks.append(t)
    if not toks:
        row_bad.append((r[0], "no-path-token"))
    elif not any((LANE / t).exists() for t in toks):
        row_bad.append((r[0], "no-resolving-token"))
print("ROW POINTER problems=%d %s" % (len(row_bad), row_bad))

share = (len(resolved) / len(tokens)) if tokens else 0.0
print("SHARE %.4f (floor 0.90)" % share)
ok = (len(rows) == 16 and set(names) == set(receipt) and not count_mismatch
      and not row_bad and share >= 0.90 and not unresolved)
print("SELF-CHECK %s" % ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)

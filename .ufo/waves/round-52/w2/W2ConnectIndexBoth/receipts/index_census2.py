#!/usr/bin/env python3
"""Read-only bidirectional census of corpus/README.md, v2 (W2ConnectIndexBoth).

Direction A (README -> files): each path-like token is resolved with table/line
context: a token with '/' resolves against corpus/ then the lane root; a bare
filename resolves against the directory named in the same table row's first cell
(or the same bullet line's first dir token, else the nearest dir heading).
Tokens naming declared-external or historical locations (~/, /tmp, llm-wiki, /app,
/tests, container paths) are classed EXTERNAL and listed separately, not as dangling.

Direction B (new files -> rows): every corpus/ path added since the round-52 base
commit must be named by a README token: exactly (file), or by a token ending in '/'
that is a path prefix of the file at >= 2 components (directory row).

Writes nothing inside the lane.
"""
import glob
import os
import re
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
BASE = "30801b479e3418c11089b8586178b6960216f364"
CORPUS = os.path.join(LANE, "corpus")
README = os.path.join(CORPUS, "README.md")

with open(README, encoding="utf-8") as fh:
    text = fh.read()
lines = text.split("\n")

tok_re = re.compile(r"`([^`\n]+)`|\]\(([^)\s]+)\)")
pathish = re.compile(r"^[A-Za-z0-9_.~/*{},+\-]+$")
EXTERNAL = re.compile(r"^(~|/tmp|/home|/fast|/app|/tests|/logs|llm-wiki|\.\./\.\./|https?:|127\.0\.0\.1|arxiv\.org|hyper/|opencode-go/|/)")
EXT_OK = re.compile(r"\.(md|py|json|jsonl|txt|sh|tsv|log|sha256|adoc|c|h|ics|csv|toml|repo|out|r)$|/$")

def resolve(tok, base_dir=None):
    t = re.sub(r"[.,;:]+$", "", tok.split("#")[0].strip())
    if "{" in t:
        m = re.match(r"^(.*)\{([^}]*)\}(.*)$", t)
        alts = [m.group(1) + a + m.group(3) for a in m.group(2).split(",")]
    else:
        alts = [t]
    for a in alts:
        cands = []
        if base_dir is not None:
            cands.append(os.path.join(base_dir, a))
        cands += [os.path.join(CORPUS, a), os.path.join(LANE, a)]
        for c in cands:
            c = os.path.normpath(c)
            if "*" in c:
                if glob.glob(c):
                    return c
            elif os.path.exists(c):
                return c
    return None

heading_dir = None
rows_ok, dangling, external = [], [], []
for i, line in enumerate(lines, 1):
    hm = re.match(r"^#+\s+(.*)$", line)
    if hm:
        d = re.findall(r"`([^`]+)`", hm.group(1))
        heading_dir = d[0].rstrip("/") if d and "/" in d[0] else None
        # headings themselves are not rows
        continue
    base = None
    cells = line.split("|") if line.startswith("|") else None
    if cells:
        first = cells[1] if len(cells) > 1 else ""
        m = re.search(r"`([^`]+)`", first)
        if m and "/" in m.group(1):
            base = os.path.normpath(os.path.join(LANE, "corpus", m.group(1).rstrip("/")))
            if not os.path.exists(base):
                base = None
        # table-first-cell resolution is for the cell's own token too
    if base is None:
        # bullet line: first dir token on the line
        dm = re.search(r"`((?:[\w.\-]+/)+)`", line)
        if dm:
            cand = os.path.normpath(os.path.join(LANE, "corpus", dm.group(1)))
            base = cand if os.path.isdir(cand) else None
    if base is None and heading_dir:
        cand = os.path.normpath(os.path.join(LANE, "corpus", heading_dir))
        base = cand if os.path.isdir(cand) else None
    for m in tok_re.finditer(line):
        tok = m.group(1) or m.group(2)
        if not tok:
            continue
        t = tok.split("#")[0].strip()
        if not pathish.match(t):
            continue
        if "/" not in t and not EXT_OK.search(t):
            continue
        if EXTERNAL.match(t):
            external.append((i, t))
            continue
        if re.match(r"^[0-9a-f]{7,}$", t):
            continue
        # bare filename: resolve against row/line/heading base; else corpus-level
        bd = base
        r = resolve(t, bd)
        if r is None and "/" not in t.rstrip("/"):
            r = resolve(t, None)
        if r is None:
            dangling.append((i, t, line.strip()[:140]))
        else:
            rows_ok.append((i, t))

print("DIRECTION A (README tokens -> files)")
print(f"  resolved={len(rows_ok)} unresolved={len(dangling)} external_or_historical={len(external)}")
print("  -- UNRESOLVED (no file in corpus/ or lane root, under row/heading context):")
for i, t, ctx in dangling:
    print(f"  README.md:{i}: `{t}`   | {ctx}")
print("  -- EXTERNAL / HISTORICAL tokens:")
for i, t in external:
    print(f"  README.md:{i}: `{t}`")

# ---- Direction B
new_files = subprocess.run(
    ["git", "-C", LANE, "diff", "--name-only", "--diff-filter=A", BASE, "HEAD", "--", "corpus"],
    capture_output=True, text=True, check=True).stdout.split()
new_files = [f for f in new_files if f != "corpus/README.md"]

tokens = set()
for m in tok_re.finditer(text):
    t = (m.group(1) or m.group(2) or "").split("#")[0].strip()
    t = re.sub(r"^(\.\./)*corpus/", "", t)
    t = re.sub(r"^(\.\./)+", "", t)
    tokens.add(t)

def covered(path):
    rel = path[len("corpus/"):]
    if rel in tokens:
        return "file-row"
    parts = rel.split("/")
    for k in range(len(parts) - 1, 1, -1):  # >=2 components of directory prefix
        d = "/".join(parts[:k]) + "/"
        if d in tokens:
            return "dir-row:" + d
    return None

byd, uncovered = {}, []
for f in new_files:
    c = covered(f)
    key = "/".join(f.split("/")[:3]) + "/"
    n = byd.setdefault(key, [0, 0])
    n[0] += 1
    if c is None:
        n[1] += 1
        uncovered.append(f)
print()
print("DIRECTION B (new corpus files since base -> README rows)")
print(f"  new_corpus_files={len(new_files)} rowless={len(uncovered)}")
for k, (n, miss) in sorted(byd.items()):
    print(f"  {k}: new={n} rowless={miss}")
print("  grep of README for 'round52' / 'round-52' / 'Round-52':",
      len(re.findall(r"round-?52", text, re.I)), "hits")
for p in ["corpus/lessons/round-52.md", "corpus/SOURCES.md", "corpus/evidence/round52/prior-art.md",
          "corpus/evidence/round52/confirmations.json", "corpus/evidence/round52/labels.json"]:
    print(f"  exists {p}: {os.path.exists(os.path.join(LANE, p))}")

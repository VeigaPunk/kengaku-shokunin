#!/usr/bin/env python3
"""R29ReviewProvenance census pass 4: eval sub-key breakdown, wikipedia tasks,
duplicate-value collision at identical relative paths, offset discriminability,
escaped-token absence proof."""
import json
import re
from collections import Counter, defaultdict

RAW = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__", "__WIKIPEDIA__", "__MAP__"]
text = open(RAW, "rb").read().decode("utf-8")
data = json.loads(text)


def fmt(path):
    out = "$"
    for p in path:
        out += ("[%d]" % p) if isinstance(p, int) else ("[" + json.dumps(p) + "]")
    return out


def walk(o, path=()):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + (k,))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + (i,))


print("=== EVAL SUB-KEY BREAKDOWN OF TOKEN LEAVES ===")
cat = Counter()
vals = defaultdict(list)
for path, val in walk(data):
    if any(t in val for t in TOKENS):
        key = fmt(path[:2]) if len(path) >= 2 and path[0] == "eval" else (path[0] if len(path) > 1 else "<root>")
        cat[key] += 1
        vals[key].append((path, val))
for k, c in cat.most_common(20):
    print("  ", k, c)

print("\n=== EXAMPLE OF EACH TOKEN-BEARING LEAF SHAPE ===")
seen = set()
for path, val in walk(data):
    if any(t in val for t in TOKENS):
        shape = fmt(path[:3]) if path and path[0] == "eval" else fmt(path[:2])
        if shape in seen:
            continue
        seen.add(shape)
        print("  ", shape, "->", json.dumps(val)[:170])

print("\n=== WIKIPEDIA TASKS: sites list vs start_url ===")
wiki_tasks = []
for i, it in enumerate(data):
    if "wikipedia" in (it.get("sites") or []):
        wiki_tasks.append(i)
print("tasks listing wikipedia in sites:", len(wiki_tasks), wiki_tasks[:12])
for i in wiki_tasks[:6]:
    it = data[i]
    print("   idx", i, "task_id", it.get("task_id"), "sites", it.get("sites"),
          "start_url", json.dumps(it.get("start_url"))[:90])
print("start_url token used by wikipedia-site tasks:",
      Counter(t for i in wiki_tasks for t in TOKENS if t in data[i].get("start_url", "")))
print("all start_url values are one of the 5 present tokens:",
      all(any(t in it.get("start_url", "") for t in TOKENS) for it in data))
print("start_url exactly equal to a bare token (no path):",
      sum(1 for it in data if it.get("start_url", "") in TOKENS))

print("\n=== TASK ID / INDEX CHECK ===")
ids = [it.get("task_id") for it in data]
print("tasks", len(ids), "distinct", len(set(ids)), "index==id all", all(i == ids[i] for i in range(len(ids))))
print("ids sample", ids[:8], "...", ids[-4:])
print("ids sorted ascending?", ids == sorted(ids))
print("min/max id", min(ids), max(ids))

print("\n=== DUPLICATE VALUE COLLISION AT IDENTICAL RELATIVE PATH ===")
rel = defaultdict(set)
relall = defaultdict(list)
for path, val in walk(data):
    if isinstance(val, str) and any(t in val for t in TOKENS):
        rel[tuple(path[1:])].add(val)
        relall[tuple(path[1:])].append((path, val))
coll = {k: v for k, v in rel.items() if len(v) == 1 and len(relall[k]) > 1}
print("relative paths where ALL token-bearing occurrences share one identical value:",
      len(coll))
for k, v in list(coll.items())[:5]:
    entries = relall[k]
    print("  path", fmt(("T",) + k), "occurrences", len(entries), "value", json.dumps(list(v)[0])[:120])
    print("     first owners", [fmt(p) for p, _ in entries[:4]])

print("\n=== OCCURRENCE-COUNT vs LEAF-COUNT UNIT SEPARATION ===")
occ = 0
leaves = 0
tasks = set()
for path, val in walk(data):
    n = sum(val.count(t) for t in TOKENS)
    if n:
        leaves += 1
        occ += n
        tasks.add(path[0])
print("token occurrences (decoded)", occ, "changed leaves", leaves, "changed tasks", len(tasks))
print("occurrences - leaves (multi-occurrence excess)", occ - leaves)

print("\n=== ESCAPED-FORM TOKEN ABSENCE PROOF ===")
esc_token_pat = re.compile(r"\\u00[0-9a-fA-F]{2}" * 0)  # placeholder
# any backslash-u escape that could decode to '_' (0x5f) or letters of tokens?
us = set(re.findall(r"\\u([0-9a-fA-F]{4})", text))
print("distinct \\uXXXX escapes:", sorted(us))
print("none encode '_' (005f):", "005f" not in us)
print("none encode letters of token names:", not any(u in us for u in
      ["0047", "0052", "0045", "0054", "004d", "0050", "0041", "0044", "0049", "004f", "0043"]))

print("\n=== FIRST-OCCURRENCE RAW OFFSET WITNESSES (all 5 present tokens) ===")
for tok in TOKENS:
    k = text.find(tok)
    print("  ", tok, "cp_offset", k, "byte_offset", k, "prefix_sha",
          __import__("hashlib").sha256(text[:k].encode()).hexdigest()[:12])

print("\n=== CONTEXT LINES FOR FIRST OCCURRENCES ===")
lines = text.split("\n")
# map cp offsets to line numbers
line_starts = []
pos = 0
for ln in lines:
    line_starts.append(pos)
    pos += len(ln) + 1
for tok in TOKENS:
    k = text.find(tok)
    if k < 0:
        continue
    li = max(i for i, s in enumerate(line_starts) if s <= k)
    print("  ", tok, "line", li + 1, "col", k - line_starts[li], "->", repr(lines[li].strip()[:110]))

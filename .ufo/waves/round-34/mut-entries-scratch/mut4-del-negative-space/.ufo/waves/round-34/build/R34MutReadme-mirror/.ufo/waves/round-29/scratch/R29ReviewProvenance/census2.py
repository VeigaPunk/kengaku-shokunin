#!/usr/bin/env python3
"""R29ReviewProvenance census pass 2: decoded-vs-serialized token census,
WIKIPEDIA/MAP anomaly, escape inventory, duplicate-identical-string structure."""
import hashlib
import json
import re
from collections import Counter, defaultdict

RAW = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__", "__WIKIPEDIA__", "__MAP__"]
raw_bytes = open(RAW, "rb").read()
text = raw_bytes.decode("utf-8")
data = json.loads(text)
print("tasks", len(data))

# --- escape inventory in serialized text
esc = Counter(re.findall(r"\\(.)", text))
print("escape_kinds", dict(sorted(esc.items(), key=lambda kv: -kv[1])))
# which escapes occur inside unicode escapes
uni = re.findall(r"\\u[0-9a-fA-F]{4}", text)
print("unicode_escape_count", len(uni), "distinct", len(set(uni)))
print("sample_unicode_escapes", sorted(set(uni))[:20])
# context of the unicode escapes: print a few surrounding slices
for m in list(re.finditer(r"\\u[0-9a-fA-F]{4}", text))[:5]:
    print("  ctx", repr(text[max(0, m.start()-40):m.end()+40]))

# --- case-insensitive token search in serialized text
for tok in TOKENS:
    low = tok.lower()
    n = text.lower().count(low)
    print("ci_count", tok, n)

# --- decoded-level token census (all string leaves, decoded)
def walk(o, path=()):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + (k,))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + (i,))

dec_occ = Counter()
dec_leaf = defaultdict(list)
for path, val in walk(data):
    for tok in TOKENS:
        c = val.count(tok)
        if c:
            dec_occ[tok] += c
            dec_leaf[tok].append((path, val, c))
print("decoded_occurrences", dict(dec_occ))
for tok in TOKENS:
    leaves = dec_leaf[tok]
    tasks = set(p[0] for p, _, _ in leaves if isinstance(p[0], int))
    print("decoded token", tok, "leaves", len(leaves), "tasks", len(tasks))

# --- WIKIPEDIA hunt: what domains appear in start_url?
hosts = Counter()
for it in data:
    su = it.get("start_url", "")
    hosts[su.split("/")[0] if su else ""] += 1
print("start_url host prefixes:")
for h, c in hosts.most_common(30):
    print("   ", repr(h), c)

# wikipedia-ish evidence in the raw text
for pat in ["wikipedia", "WIKIPEDIA", "wiki"]:
    idxs = [m.start() for m in re.finditer(pat, text)]
    print("pattern", pat, "hits", len(idxs), idxs[:5])
for i in [m.start() for m in re.finditer("wikipedia", text)][:5]:
    print("   ctx", repr(text[max(0, i-60):i+60]))

# MAP token context
map_idx = [m.start() for m in re.finditer("__MAP__", text)]
print("map occurrences", len(map_idx))
print("map ctx sample:")
for i in map_idx[:5]:
    print("   ", repr(text[max(0, i-50):i+50]))

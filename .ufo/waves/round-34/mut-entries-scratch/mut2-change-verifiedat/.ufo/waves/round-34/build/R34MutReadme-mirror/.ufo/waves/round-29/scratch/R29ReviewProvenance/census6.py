#!/usr/bin/env python3
"""R29ReviewProvenance census pass 6: path templates, decoded-vs-serialized
identity, value-keyed collision magnitudes, per-token exact counts."""
import json
from collections import Counter, defaultdict

RAW = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__", "__WIKIPEDIA__", "__MAP__"]
text = open(RAW, "rb").read().decode("utf-8")
data = json.loads(text)


def walk(o, path=()):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + (k,))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + (i,))


def template(path):
    out = []
    for p in path:
        out.append("[i]" if isinstance(p, int) else p)
    # collapse consecutive [i]
    s = "$"
    prev_i = False
    for p in path:
        if isinstance(p, int):
            if not prev_i:
                s += "[i]"
            prev_i = True
        else:
            s += "[" + json.dumps(p) + "]"
            prev_i = False
    return s


print("=== PATH TEMPLATES OF TOKEN-BEARING LEAVES ===")
tmpl = Counter()
for path, val in walk(data):
    if any(t in val for t in TOKENS):
        tmpl[template(path)] += 1
for k, c in tmpl.most_common():
    print("   %-72s %d" % (k, c))
print("   TOTAL LEAVES", sum(tmpl.values()))

print("\n=== DECODED vs SERIALIZED OCCURRENCE IDENTITY ===")
ser = sum(text.count(t) for t in TOKENS)
dec = sum(sum(v.count(t) for t in TOKENS) for _, v in walk(data))
print("serialized occurrences", ser, "decoded occurrences", dec, "identical", ser == dec)

print("\n=== VALUE-KEYED COLLISION MAGNITUDE ===")
vals = Counter()
for path, val in walk(data):
    if any(t in val for t in TOKENS):
        vals[val] += 1
print("changed leaves (path-keyed)", sum(vals.values()))
print("distinct changed values (value-keyed)", len(vals))
print("leaf count if a value-keyed map is used -> 446 vs 1416; "
      "under-report magnitude", sum(vals.values()) - len(vals))
top = vals.most_common(8)
for v, n in top:
    print("   copies %3d %s" % (n, json.dumps(v)[:96]))

print("\n=== EXACT PER-TOKEN COUNTS ===")
for t in TOKENS:
    s_occ = text.count(t)
    leaves = sum(1 for _, v in walk(data) if t in v)
    tasks = len({p[0] for p, v in walk(data) if t in v})
    multi = sum(v.count(t) for _, v in walk(data)) - leaves
    print("   %-20s serialized_occ=%4d leaves=%4d tasks=%4d excess_occ_over_leaves=%d"
          % (t, s_occ, leaves, tasks, multi))

print("\n=== LEAF-VALUE TEMPLATE x TOKEN ===")
cross = Counter()
for path, val in walk(data):
    for t in TOKENS:
        if t in val:
            cross[(template(path), t)] += 1
for (tp, t), c in sorted(cross.items()):
    print("   %-24s %-70s %d" % (t, tp, c))

print("\n=== FULL-JSON STRUCTURE SHAPE (top-level keys) ===")
print("task top-level keys:", Counter(tuple(sorted(it.keys())) for it in data))
print("eval sub-keys seen:", Counter(k for it in data for k in it.get("eval", {}).keys()))

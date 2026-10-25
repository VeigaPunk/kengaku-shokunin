#!/usr/bin/env python3
"""R29ReviewProvenance census pass 5: exact witnesses for the report.

(a) eval sub-key breakdown of token-bearing leaves
(b) exact per-profile changed-leaf / changed-task / occurrence counts
(c) within-task duplicate identical values (value-keyed diff collision risk)
(d) cross-task duplicate identical token-bearing values
(e) runtime marker counts + non-collision with env tokens
(f) exact multi-occurrence leaf list
"""
import json
from collections import Counter, defaultdict

RAW = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__", "__WIKIPEDIA__", "__MAP__"]
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
RUNTIME = ["__last_url__", "__page__"]
text = open(RAW, "rb").read().decode("utf-8")
data = json.loads(text)
PROFILES = json.load(open("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/profiles.json"))


def fmt(p):
    out = "$"
    for x in p:
        out += ("[%d]" % x) if isinstance(x, int) else ("[" + json.dumps(x) + "]")
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


def proj(raw, vals):
    for n in ORDER:
        raw = raw.replace("__" + n + "__", vals[n])
    return raw


print("=== (a) TOKEN-BEARING LEAF KEY CATEGORIES (top-2 keys) ===")
cat = Counter()
for path, val in walk(data):
    if any(t in val for t in TOKENS):
        cat[fmt(path[:2])] += 1
for k, c in cat.most_common(30):
    print("   %-58s %d" % (k, c))
print("   TOTAL", sum(cat.values()))

print("\n=== (b) PER-PROFILE EXACT METRICS ===")
base_leaves = {(p, v) for p, v in walk(data) if any(t in v for t in TOKENS)}
for pname, prof in PROFILES.items():
    ptxt = proj(text, prof["values"])
    pdata = json.loads(ptxt)
    changed_leaves = 0
    changed_tasks = set()
    occ_projected_text = sum(ptxt.count(t) for t in TOKENS)
    diff_leaves = []
    for (path, ov), (path2, nv) in zip(walk(data), walk(pdata)):
        if ov != nv:
            changed_leaves += 1
            diff_leaves.append(path)
            changed_tasks.add(path[0])
    print(pname, "tasks", len(pdata), "changed_leaves", changed_leaves,
          "changed_tasks", len(changed_tasks), "env_token_occurrences_left_in_projected_text",
          occ_projected_text, "runtime_markers",
          {m: ptxt.count(m) for m in RUNTIME})
print("   BASE token-bearing leaves", len(base_leaves))

print("\n=== (c) WITHIN-TASK DUPLICATE IDENTICAL TOKEN-BEARING VALUES ===")
per_task = defaultdict(list)
for path, val in walk(data):
    if any(t in val for t in TOKENS):
        per_task[path[0]].append((path, val))
within = 0
examples = []
for t, items in per_task.items():
    c = Counter(v for _, v in items)
    dups = {v: n for v, n in c.items() if n > 1}
    if dups:
        within += 1
        if len(examples) < 5:
            for v, n in list(dups.items())[:1]:
                paths = [fmt(p) for p, vv in items if vv == v]
                examples.append((t, n, v, paths))
print("tasks containing an identical token-bearing value at 2+ paths:", within)
for t, n, v, paths in examples:
    print("   task", t, "copies", n, "value", json.dumps(v)[:110])
    print("     paths", paths[:5])

print("\n=== (d) CROSS-TASK IDENTICAL TOKEN-BEARING VALUES ===")
valcount = Counter()
for path, val in walk(data):
    if any(t in val for t in TOKENS):
        valcount[val] += 1
dup = {v: n for v, n in valcount.items() if n > 1}
print("distinct token-bearing values", len(valcount), "appearing at >1 leaf", len(dup),
      "leaves involved", sum(dup.values()))
for v, n in sorted(dup.items(), key=lambda kv: -kv[1])[:6]:
    print("   copies %3d  %s" % (n, json.dumps(v)[:100]))

print("\n=== (e) RUNTIME MARKER DETAIL ===")
print("__last_url__ occurrences", text.count("__last_url__"), "__page__", text.count("__page__"))
print("any runtime marker contains an env token substring:",
      any(t in m for m in RUNTIME for t in TOKENS))
rl = Counter()
for path, val in walk(data):
    for m in RUNTIME:
        if m in val:
            rl[fmt(path[:2])] += 1
print("runtime marker leaf categories:", dict(rl.most_common(10)))

print("\n=== (f) EXACT MULTI-OCCURRENCE LEAVES ===")
leaf_occ = Counter()
leaf_owner = {}
for t in TOKENS:
    i = 0
    while True:
        k = text.find(t, i)
        if k < 0:
            break
        i = k + 1
# leaf spans
class SP:
    def __init__(s, s_):
        s.s = s_
        s.i = 0
        s.spans = []

    def ws(s):
        while s.i < len(s.s) and s.s[s.i] in " \t\n\r":
            s.i += 1

    def str_span(s):
        st = s.i
        s.i += 1
        while s.i < len(s.s):
            if s.s[s.i] == "\\":
                s.i += 2
                continue
            if s.s[s.i] == '"':
                s.i += 1
                break
            s.i += 1
        return (st, s.i)

    def parse(s, path):
        s.ws()
        c = s.s[s.i]
        if c == "{":
            s.i += 1
            s.ws()
            if s.s[s.i] == "}":
                s.i += 1
                return {}
            o = {}
            while True:
                s.ws()
                ks = s.str_span()
                k = json.loads(s.s[ks[0]:ks[1]])
                s.ws()
                s.i += 1
                o[k] = s.parse(path + (k,))
                s.ws()
                if s.s[s.i] == ",":
                    s.i += 1
                    continue
                s.i += 1
                return o
        if c == "[":
            s.i += 1
            s.ws()
            if s.s[s.i] == "]":
                s.i += 1
                return []
            a = []
            while True:
                a.append(s.parse(path + (len(a),)))
                s.ws()
                if s.s[s.i] == ",":
                    s.i += 1
                    continue
                s.i += 1
                return a
        if c == '"':
            sp = s.str_span()
            v = json.loads(s.s[sp[0]:sp[1]])
            s.spans.append((path, sp[0], sp[1], v))
            return v
        j = s.i
        while s.s[j] not in ",]} \t\n\r":
            j += 1
        lit = s.s[s.i:j]
        s.i = j
        return json.loads(lit)


sp = SP(text)
sp.parse(())
import bisect
starts = [x[1] for x in sp.spans]
occ_by_leaf = Counter()
tok_by_leaf = defaultdict(list)
for t in TOKENS:
    i = 0
    while True:
        k = text.find(t, i)
        if k < 0:
            break
        j = bisect.bisect_right(starts, k) - 1
        path, s0, s1, v = sp.spans[j]
        occ_by_leaf[(path, s0)] += 1
        tok_by_leaf[(path, s0)].append((t, k - s0))
        i = k + 1
multi = sorted([(c, k) for k, c in occ_by_leaf.items() if c > 1], key=lambda x: (-x[0], str(x[1][0])))
print("multi-occurrence leaves:", len(multi), "excess occurrences", sum(c - 1 for c, _ in multi))
for c, (path, s0) in multi:
    print("   occ=%d %-46s token=%s inner_cp_offsets=%s" %
          (c, fmt(path), tok_by_leaf[(path, s0)][0][0],
           [o for _, o in tok_by_leaf[(path, s0)]]))

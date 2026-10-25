#!/usr/bin/env python3
"""R29ReviewProvenance census pass 3: precise witnesses.

A. leaf multiplicity (occurrences per changed leaf) with exact paths
B. duplicate identical decoded values containing tokens (value-keyed collision)
C. codepoint vs byte offset discriminability on the frozen input
D. non-URL-valued leaves carrying tokens
E. remaining runtime markers (__last_url__/__page__) after the six replacements
F. per-token leaf/task/path-category census
"""
import json
import re
from collections import Counter, defaultdict

RAW = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__", "__WIKIPEDIA__", "__MAP__"]
RUNTIME_MARKERS = ["__last_url__", "__page__"]
text = open(RAW, "rb").read().decode("utf-8")
data = json.loads(text)

# ---------- E: sequential replacement exactly as upstream source does (text-level only,
# using synthetic profile values, no upstream import)
PROFILES = json.load(open("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/profiles.json"))
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]


def upstream_replace(raw_text, values):
    for name in ORDER:
        raw_text = raw_text.replace("__" + name + "__", values[name])
    return raw_text


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


print("=== E: RUNTIME MARKERS AFTER SIX REPLACEMENTS ===")
for pname, prof in PROFILES.items():
    proj = upstream_replace(text, prof["values"])
    rem = {m: proj.count(m) for m in RUNTIME_MARKERS}
    remtok = {t: proj.count(t) for t in TOKENS}
    parsed = json.loads(proj)
    print(pname, "runtime_markers", rem, "remaining_env_tokens", remtok,
          "parsed_tasks", len(parsed))
    # cascade check: does any profile value contain another token?
    for name, v in prof["values"].items():
        for t in TOKENS:
            if t in v:
                print("   CASCADE_RISK", pname, name, v, "contains", t)

print("\n=== A: LEAF MULTIPLICITY WITNESSES (decoded leaf values) ===")
for pname, prof in PROFILES.items():
    proj = upstream_replace(text, prof["values"])
    pd = json.loads(proj)
    occ_per_leaf = []
    changed_leaves = 0
    changed_tasks = set()
    for path, val in walk(pd):
        n = sum(val.count(t) for t in TOKENS)
        if n:
            occ_per_leaf.append((n, path, val))
            changed_leaves += 1
            if isinstance(path[0], int):
                changed_tasks.add(path[0])
    hist = Counter(n for n, _, _ in occ_per_leaf)
    print(pname, "changed_leaves", changed_leaves, "occ_per_leaf_hist", dict(sorted(hist.items())),
          "changed_tasks", len(changed_tasks), "total_occ", sum(n for n, _, _ in occ_per_leaf))
    if pname == "distinct_origins":
        top = sorted(occ_per_leaf, key=lambda x: (-x[0], str(x[1])))[:6]
        for n, path, val in top:
            print("   leaf_occ", n, fmt(path), "value", json.dumps(val)[:180])

print("\n=== A2: RAW-SERIALIZED LEAF MULTIPLICITY (same leaf, N token occurrences) ===")
# map raw serialized occurrence -> owning leaf, using leaf spans from pass1 logic
class P:
    def __init__(self, s):
        self.s = s
        self.i = 0
        self.spans = []

    def ws(self):
        while self.i < len(self.s) and self.s[self.i] in " \t\n\r":
            self.i += 1

    def string_span(self):
        start = self.i
        self.i += 1
        while self.i < len(self.s):
            if self.s[self.i] == "\\":
                self.i += 2
                continue
            if self.s[self.i] == '"':
                self.i += 1
                break
            self.i += 1
        return (start, self.i)

    def parse(self, path):
        self.ws()
        c = self.s[self.i]
        if c == "{":
            self.i += 1
            self.ws()
            if self.s[self.i] == "}":
                self.i += 1
                return {}
            o = {}
            while True:
                self.ws()
                ks = self.string_span()
                key = json.loads(self.s[ks[0]:ks[1]])
                self.ws()
                self.i += 1  # colon
                o[key] = self.parse(path + (key,))
                self.ws()
                if self.s[self.i] == ",":
                    self.i += 1
                    continue
                self.i += 1
                return o
        if c == "[":
            self.i += 1
            self.ws()
            if self.s[self.i] == "]":
                self.i += 1
                return []
            a = []
            while True:
                a.append(self.parse(path + (len(a),)))
                self.ws()
                if self.s[self.i] == ",":
                    self.i += 1
                    continue
                self.i += 1
                return a
        if c == '"':
            sp = self.string_span()
            val = json.loads(self.s[sp[0]:sp[1]])
            self.spans.append((path, sp[0], sp[1], val))
            return val
        j = self.i
        while self.s[j] not in ",]} \t\n\r":
            j += 1
        lit = self.s[self.i:j]
        self.i = j
        return json.loads(lit)


p = P(text)
p.parse(())
spans = p.spans
starts = [s[1] for s in spans]
import bisect
leaf_occ = Counter()
for tok in TOKENS:
    idx = 0
    while True:
        k = text.find(tok, idx)
        if k < 0:
            break
        j = bisect.bisect_right(starts, k) - 1
        path, s0, s1, val = spans[j]
        leaf_occ[(path, s0)] += 1
        idx = k + 1
print("raw leaves touched", len(leaf_occ), "hist", dict(sorted(Counter(leaf_occ.values()).items())))
multi = [(c, k) for k, c in leaf_occ.items() if c >= 2]
multi.sort(key=lambda x: (-x[0], str(x[1][0])))
print("leaves with >=2 raw occurrences:", len(multi))
for c, (path, s0) in multi[:8]:
    val = None
    for pp, ss, ee, vv in spans:
        if pp == path and ss == s0:
            val = vv
            break
    toks = [t for t in TOKENS if t in val]
    inner = []
    for t in toks:
        k = val.find(t)
        while k >= 0:
            inner.append((t, k))
            k = val.find(t, k + 1)
    print("  occ", c, fmt(path), "tokens", toks, "decoded_inner_codepoint_offsets", sorted(inner))
    print("     value", json.dumps(val)[:240])

print("\n=== B: DUPLICATE IDENTICAL DECODED VALUES CONTAINING TOKENS ===")
val_spans = defaultdict(list)
for path, s0, s1, val in spans:
    if isinstance(val, str):
        val_spans[val].append((path, s0, s1))
dup_tok = {v: s for v, s in val_spans.items() if len(s) > 1 and any(t in v for t in TOKENS)}
print("distinct token-bearing values duplicated across spans:", len(dup_tok))
tot = sum(len(s) for s in dup_tok.values())
print("total spans involved", tot)
ex = sorted(dup_tok.items(), key=lambda kv: -len(kv[1]))[:3]
for v, s in ex:
    print("  value", json.dumps(v)[:150], "spans", len(s))
    for path, s0, s1 in s[:4]:
        print("     ", fmt(path), "span_cp", s0, s1)
# same relative path across tasks, identical value?
rel = defaultdict(set)
for path, s0, s1, val in spans:
    if isinstance(val, str) and any(t in val for t in TOKENS):
        rel[tuple(path[1:])].add(val)
multi_task_identical = {k: v for k, v in rel.items() if len(v) == 1 and True}
print("relative paths whose token-bearing values are identical everywhere they occur:", len(multi_task_identical))

print("\n=== C: CODEPOINT vs BYTE OFFSET DISCRIMINABILITY ON FROZEN INPUT ===")
print("serialized text is pure ASCII:", all(ord(ch) < 128 for ch in text))
# leaves containing a token AND non-ascii decoded chars
cnt = 0
for path, s0, s1, val in spans:
    if isinstance(val, str) and any(t in val for t in TOKENS) and any(ord(ch) > 127 for ch in val):
        cnt += 1
        if cnt <= 5:
            nb = sum(len(ch.encode("utf-8")) - 1 for ch in val if ord(ch) > 127)
            print("  leaf_with_token_and_nonascii", fmt(path), "nonascii_extra_bytes", nb,
                  "value", json.dumps(val)[:160])
print("token leaves containing non-ascii chars:", cnt)

print("\n=== D: NON-URL-VALUED LEAVES CARRYING TOKENS ===")
URLISH = ("http://", "https://", "://", "www.")
nonurl = [(path, val) for path, s0, s1, val in spans
          if isinstance(val, str) and any(t in val for t in TOKENS) and not any(u in val for u in URLISH)]
print("non-url token leaves:", len(nonurl))
cat = Counter()
for path, val in nonurl:
    cat[path[1] if len(path) > 1 else "<root>"] += 1
print("by first key:", dict(cat.most_common(12)))
for path, val in nonurl[:6]:
    print("  ", fmt(path), json.dumps(val)[:200])

print("\n=== F: PER-TOKEN PATH CATEGORY CENSUS (raw serialized) ===")
for tok in TOKENS:
    idx = 0
    cats = Counter()
    tasks = set()
    occ = 0
    while True:
        k = text.find(tok, idx)
        if k < 0:
            break
        j = bisect.bisect_right(starts, k) - 1
        path, s0, s1, val = spans[j]
        cats[path[1] if len(path) > 1 else "<root>"] += 1
        if isinstance(path[0], int):
            tasks.add(path[0])
        occ += 1
        idx = k + 1
    print(tok, "occ", occ, "tasks", len(tasks), "bykey", dict(cats.most_common(8)))

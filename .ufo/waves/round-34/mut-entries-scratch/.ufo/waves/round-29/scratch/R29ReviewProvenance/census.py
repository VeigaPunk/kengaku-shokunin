#!/usr/bin/env python3
"""R29ReviewProvenance read-only census.

Reads the pinned r28 raw WebArena test.raw.json ONCE, authenticates its bytes,
and derives raw-occurrence <-> JSON string/keypath provenance facts:
  * literal token occurrence counts in the serialized text
  * per-occurrence owning JSON string literal span, decoded value, and keypath
  * Unicode codepoint offsets vs UTF-8 byte offsets
  * leaf multiplicity (occurrences per changed string leaf)
  * duplicate identical decoded string values across distinct paths
  * key-position vs value-position occurrences
No upstream code is imported or executed; no writes outside this scratch dir.
"""
import hashlib
import json
import sys
from collections import Counter, defaultdict

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = LANE + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
EXPECTED_SHA = "7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652"
TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__", "__WIKIPEDIA__", "__MAP__"]

raw_bytes = open(RAW, "rb").read()
sha = hashlib.sha256(raw_bytes).hexdigest()
print("raw_sha256", sha, "match" if sha == EXPECTED_SHA else "MISMATCH")
text = raw_bytes.decode("utf-8")
print("byte_len", len(raw_bytes), "codepoint_len", len(text))

non_ascii = [(i, ch) for i, ch in enumerate(text) if ord(ch) > 127]
print("non_ascii_codepoints", len(non_ascii))
if non_ascii:
    print("non_ascii_first10", non_ascii[:10])
    print("non_ascii_distinct", sorted({ch for _, ch in non_ascii})[:20])

# UTF-8 byte offset of every codepoint index (prefix map)
byte_off = [0] * (len(text) + 1)
b = 0
for i, ch in enumerate(text):
    byte_off[i] = b
    b += len(ch.encode("utf-8"))
byte_off[len(text)] = b

print("has_backslash_u_escape", "\\u" in text)
print("has_backslash_escape", "\\" in text)

# ------------------------------------------------------------------ scanner
# Record every JSON string literal span in the serialized text with its path.
WS = " \t\n\r"


def scan(text):
    """Return list of (path_tuple, start, end, raw_literal) for JSON string literals."""
    spans = []
    stack = []  # entries: ('obj', pending_key) or ('arr',)
    key = None
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c == '"':
            start = i
            i += 1
            while i < n:
                if text[i] == "\\":
                    i += 2
                    continue
                if text[i] == '"':
                    break
                i += 1
            end = i + 1  # exclusive, includes closing quote
            literal = text[start:end]
            path = []
            for kind, val in stack:
                if kind == "arr":
                    path.append(val)
                else:
                    path.append(val)
            spans.append((tuple(path), start, end, literal, key))
            i = end
            # advance state after a string: decide whether it is a key or a value
            # by looking at the next significant char
            j = i
            while j < n and text[j] in WS:
                j += 1
            if j < n and text[j] == ":":
                key = json.loads(literal)
                i = j + 1
            else:
                key = None
                i = end
            continue
        if c == "{":
            stack.append(("obj", key))
            key = None
            i += 1
            continue
        if c == "[":
            stack.append(("arr", len(stack) and stack[-1][1]))
            # array index tracking handled below
            stack[-1] = ("arr_idx", 0)
            key = None
            i += 1
            continue
        if c == "}":
            if stack:
                stack.pop()
            key = None
            i += 1
            continue
        if c == "]":
            if stack:
                stack.pop()
            key = None
            i += 1
            continue
        if c == ",":
            if stack and stack[-1][0] == "arr_idx":
                stack[-1] = ("arr_idx", stack[-1][1] + 1)
            key = None
            i += 1
            continue
        if c == ":":
            key = None
            i += 1
            continue
        i += 1
    return spans


def fmt(path):
    out = "$"
    for p in path:
        if isinstance(p, int):
            out += "[%d]" % p
        else:
            out += "[" + json.dumps(p) + "]"
    return out


spans = scan(text)
print("scanned_string_literals", len(spans))

# rebuild path correctly with a cleaner second pass using an explicit parser
class P:
    def __init__(self, s):
        self.s = s
        self.i = 0
        self.spans = []

    def ws(self):
        while self.i < len(self.s) and self.s[self.i] in WS:
            self.i += 1

    def parse(self, path):
        self.ws()
        c = self.s[self.i]
        if c == "{":
            self.i += 1
            self.ws()
            if self.s[self.i] == "}":
                self.i += 1
                return {}
            obj = {}
            while True:
                self.ws()
                kstart = self.i
                assert self.s[self.i] == '"', (self.i, self.s[self.i - 30:self.i + 30])
                kspan = self.string_span()
                key = json.loads(self.s[kspan[0]:kspan[1]])
                self.ws()
                assert self.s[self.i] == ":"
                self.i += 1
                val = self.parse(path + (key,))
                obj[key] = val
                self.ws()
                if self.s[self.i] == ",":
                    self.i += 1
                    continue
                assert self.s[self.i] == "}"
                self.i += 1
                return obj
        if c == "[":
            self.i += 1
            self.ws()
            arr = []
            if self.s[self.i] == "]":
                self.i += 1
                return arr
            idx = 0
            while True:
                val = self.parse(path + (idx,))
                arr.append(val)
                idx += 1
                self.ws()
                if self.s[self.i] == ",":
                    self.i += 1
                    continue
                assert self.s[self.i] == "]"
                self.i += 1
                return arr
        if c == '"':
            sp = self.string_span()
            val = json.loads(self.s[sp[0]:sp[1]])
            self.spans.append((path, sp[0], sp[1], val))
            return val
        # literal
        j = self.i
        while self.s[j] not in ",]} \t\n\r":
            j += 1
        lit = self.s[self.i:j]
        self.i = j
        return json.loads(lit)

    def string_span(self):
        start = self.i
        assert self.s[self.i] == '"'
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


p = P(text)
data = p.parse(())
print("parsed_tasks", len(data))
print("parsed_string_leaves", len(p.spans))
print("trailing_after_parse", repr(text[p.i:p.i + 20]), "at", p.i, "of", len(text))

# ------------------------------------------------- occurrence -> leaf mapping
# For each token, find every literal occurrence in the serialized text and map it
# to the innermost string literal span that contains it.
spans_sorted = sorted(p.spans, key=lambda s: s[1])

import bisect

starts = [s[1] for s in spans_sorted]


def owner(offset):
    j = bisect.bisect_right(starts, offset) - 1
    if j < 0:
        return None
    path, s0, s1, val = spans_sorted[j]
    if s0 <= offset < s1:
        return (path, s0, s1, val)
    return None


occ_by_token = {}
occ_rows = []
for tok in TOKENS:
    idx = 0
    occs = []
    while True:
        k = text.find(tok, idx)
        if k < 0:
            break
        occs.append(k)
        idx = k + 1
    occ_by_token[tok] = occs
    print("token", tok, "serialized_occurrences", len(occs))

# global occurrence multiset (tokens are mutually non-overlapping substrings?
# __SHOPPING__ vs __SHOPPING_ADMIN__ : check)
for a in TOKENS:
    for b in TOKENS:
        if a != b and a in b:
            print("TOKEN_SUBSTRING_OVERLAP", a, "in", b)

# classify each occurrence
key_occ = []
value_occ = []
unowned = []
leaf_multi = Counter()
leaf_paths = defaultdict(set)
for tok, occs in occ_by_token.items():
    for off in occs:
        o = owner(off)
        if o is None:
            unowned.append((tok, off))
            continue
        path, s0, s1, val = o
        if isinstance(val, str) and tok in val:
            # occurrence is inside a decoded string value
            value_occ.append((tok, off, path, s0, s1, val))
            leaf_multi[(path, s0)] += 1
            leaf_paths[(path, s0)].add(tok)
        else:
            # inside a JSON key
            key_occ.append((tok, off, path, s0, s1, val))

print("occurrences_in_values", len(value_occ), "in_keys", len(key_occ), "unowned", len(unowned))
print("distinct_value_leaves_changed", len(leaf_multi))
mult = Counter(leaf_multi.values())
print("occurrence_per_leaf_histogram", dict(sorted(mult.items())))

# leaves with >1 occurrence of the SAME token, and leaves with 2 distinct tokens
same_tok_multi = 0
distinct_tok_leaf = 0
for key, cnt in leaf_multi.items():
    toks = leaf_paths[key]
    if cnt > 1 and len(toks) == 1:
        same_tok_multi += 1
    if len(toks) > 1:
        distinct_tok_leaf += 1
print("leaves_with_multiple_occurrences_of_same_token", same_tok_multi)
print("leaves_containing_more_than_one_distinct_token", distinct_tok_leaf)

# changed tasks
changed_tasks = set()
for tok, off, path, s0, s1, val in value_occ:
    changed_tasks.add(path[0] if isinstance(path[0], int) else path)
print("changed_task_count(value_occ)", len(changed_tasks))

# duplicate identical decoded string values across distinct leaf spans
val_to_spans = defaultdict(list)
for path, s0, s1, val in p.spans:
    if isinstance(val, str):
        val_to_spans[val].append((path, s0, s1))
dups = {v: s for v, s in val_to_spans.items() if len(s) > 1}
print("distinct_decoded_string_values", len(val_to_spans))
print("values_appearing_at_multiple_spans", len(dups))
tok_dups = 0
for v, s in dups.items():
    if any(t in v for t in TOKENS):
        tok_dups += 1
print("duplicate_values_containing_any_token", tok_dups)

# same path-prefix duplicate: identical string at two different tasks
if dups:
    items = sorted(dups.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:5]
    for v, s in items:
        print("DUPVALUE len_spans", len(s), "value_len", len(v), "sample_paths", [fmt(x[0]) for x in s[:4]])

# ------------------------------------------- codepoint vs byte offset delta
deltas = []
for tok, off, path, s0, s1, val in value_occ[:0]:
    pass
all_occ = [(tok, off) for tok, occs in occ_by_token.items() for off in occs]
for tok, off in all_occ:
    d = byte_off[off] - off
    if d:
        deltas.append((tok, off, byte_off[off], d))
print("occurrences_with_codepoint_byte_offset_divergence", len(deltas))
if deltas:
    print("sample_divergence", deltas[:5])
    print("max_byte_minus_codepoint_delta", max(x[3] for x in deltas))
else:
    print("max_byte_minus_codepoint_delta", 0)

# ------------------------------------------- hand witness: first occurrence each token
print("\n=== FIRST-OCCURRENCE WITNESS PER TOKEN ===")
for tok in TOKENS:
    occs = occ_by_token[tok]
    off = occs[0]
    o = owner(off)
    path, s0, s1, val = o
    print("token", tok)
    print("  codepoint_offset", off, "byte_offset", byte_off[off])
    print("  literal_span_cp", s0, s1, "byte", byte_off[s0], byte_off[s1])
    print("  path", fmt(path))
    print("  decoded_value", json.dumps(val)[:220])
    print("  occurrences_in_this_leaf", val.count(tok), "leaf_span_len_cp", s1 - s0)
    print("  occurrences_of_token_in_leaf_total", sum(1 for x in value_occ if x[0] == tok and x[2] == path))

# ------------------------------------------- hand witness: leaf with 2 occurrences
print("\n=== MULTI-OCCURRENCE LEAF WITNESS ===")
for (path, s0), cnt in sorted(leaf_multi.items(), key=lambda kv: -kv[1])[:3]:
    if cnt < 2:
        continue
    val = None
    for pp, ss, ee, vv in p.spans:
        if pp == path and ss == s0:
            val = vv
            break
    toks = leaf_paths[(path, s0)]
    print("count", cnt, "path", fmt(path), "tokens", sorted(toks))
    print("  value", json.dumps(val)[:300])
    inner = []
    for t in toks:
        k = val.find(t)
        while k >= 0:
            inner.append((t, k))
            k = val.find(t, k + 1)
    print("  decoded_inner_offsets", sorted(inner))

# ------------------------------------------- non-URL metadata leaves
print("\n=== NON-URL-VALUED LEAVES WITH TOKENS ===")
URLISH = ("http://", "https://", "://", "www.")
nonurl = []
for tok, off, path, s0, s1, val in value_occ:
    if not any(u in val for u in URLISH):
        nonurl.append((tok, off, path, val))
print("occurrence_count_in_non_url_leaves", len(nonurl))
nonurl_leaves = {(p, s) for _, _, p, _ in nonurl}
print("non_url_leaves", len(nonurl_leaves))
shown = 0
for tok, off, path, val in nonurl:
    if shown >= 8:
        break
    print("  tok", tok, "cp_off", off, "path", fmt(path))
    print("    value", json.dumps(val)[:260])
    shown += 1

# ------------------------------------------- task_id vs index
print("=== TASK ID / INDEX ===")
ids = [it.get("task_id") for it in data]
print("tasks", len(ids), "distinct_ids", len(set(ids)), "all_int", all(isinstance(x, int) for x in ids))
print("index_equals_task_id_for_all", all(i == ids[i] for i in range(len(ids))))
mism = [(i, ids[i]) for i in range(len(ids)) if i != ids[i]]
print("mismatches", len(mism), mism[:5])

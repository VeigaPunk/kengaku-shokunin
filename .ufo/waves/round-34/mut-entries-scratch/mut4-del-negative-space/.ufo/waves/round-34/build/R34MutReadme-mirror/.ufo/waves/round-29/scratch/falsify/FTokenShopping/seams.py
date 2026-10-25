#!/usr/bin/env python3
"""Seam tests for the __SHOPPING__ census. Independent of plans/config_projection.py."""
import hashlib
import json
import os
import re
from collections import Counter, defaultdict

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = os.path.join(LANE, "plans/fixtures/r28/webarena/config_files/test.raw.json")
PROF = os.path.join(LANE, "plans/fixtures/r29/profiles.json")
INST = os.path.join(LANE, ".ufo/waves/round-29/scratch/falsify/FTokenShopping/instrument.json")
TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__",
          "__WIKIPEDIA__", "__MAP__"]
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TARGET = "__SHOPPING__"

raw = open(RAW, "rb").read().decode("utf-8")
data = json.loads(raw)
inst = json.load(open(INST, "r", encoding="utf-8"))
prof = json.load(open(PROF, "r", encoding="utf-8"))


def walk(node, ptr="", tptr=""):
    """Yield (pointer, template, string) with instrument-style templates:
    list indices collapse to '[]' on the preceding segment; root index dropped."""
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk(v, ptr + "/" + k, (tptr + "." + k) if tptr else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, ptr + "/" + str(i), tptr + "[]")
    elif isinstance(node, str):
        yield ptr, tptr, node


leaves = list(walk(data))
tpl = {p: t for p, t, s in leaves}
leaf_s = {p: s for p, t, s in leaves}


def occ_in(s, tok):
    c, i = 0, 0
    while True:
        i = s.find(tok, i)
        if i < 0:
            return c
        c += 1
        i += 1


print("=== A. PROVENANCE -> LEAF ATTRIBUTION (all tokens) ===")
prov = inst["occurrence_provenance"]
by_tok = defaultdict(list)
for r in prov:
    by_tok[r["token"]].append(r)
for tok in TOKENS:
    rows = by_tok[tok]
    raw_n = occ_in(raw, tok)
    per_ptr = Counter(r["json_pointer"] for r in rows)
    bad_ptr = 0
    for ptr, n in per_ptr.items():
        if leaf_s.get(ptr, "").count(tok) != n and occ_in(leaf_s.get(ptr, ""), tok) != n:
            bad_ptr += 1
    offs_bad = sum(1 for r in rows if raw[r["original_input_codepoint_offset"]:r["original_input_codepoint_offset"] + len(tok)] != tok)
    ptrs = set(per_ptr)
    leaves_with = {p for p, s in leaf_s.items() if tok in s}
    print(tok, "rows", len(rows), "raw_count", raw_n, "match", len(rows) == raw_n,
          "distinct_ptrs", len(ptrs), "leaves_with_token", len(leaves_with),
          "ptr_set_equal", ptrs == leaves_with, "bad_ptr_multiplicity", bad_ptr,
          "bad_offsets", offs_bad)
    # multiplicity histogram
    print("   multiplicity", dict(sorted(Counter(per_ptr.values()).items())),
          "max_occ_in_leaf", max([s.count(tok) for s in leaf_s.values()] or [0]))

print("\n=== B. TARGET PROVENANCE MULTIPLICITY VS LEAF CENSUS ===")
rows = by_tok[TARGET]
per_ptr = Counter(r["json_pointer"] for r in rows)
tcensus = {p: s.count(TARGET) for p, s in leaf_s.items() if TARGET in s}
print("provenance_per_ptr == leaf_census:", dict(per_ptr) == tcensus)
diff = {p: (per_ptr.get(p), tcensus.get(p)) for p in set(per_ptr) | set(tcensus) if per_ptr.get(p) != tcensus.get(p)}
print("differences", diff)
print("target rows with string_role != value", sum(1 for r in rows if r["string_role"] != "value"))
print("target task_index == int(ptr.split('/')[1]):", all(r["task_index"] == int(r["json_pointer"].split("/")[1]) for r in rows))
print("target template agrees with my template:", all(tpl.get(r["json_pointer"]) == r["path_template"] for r in rows),
      "first", rows[0]["json_pointer"], tpl.get(rows[0]["json_pointer"]), rows[0]["path_template"])

print("\n=== C. OTHER MARKERS ===")
for m in ["__last_url__", "__page__"]:
    print(m, "raw", occ_in(raw, m), "instrument", inst["population"]["other_double_underscore_markers"].get(m),
          "decoded_leaves", sum(1 for s in leaf_s.values() if m in s))

print("\n=== D. TOKENS FOLLOWED BY SLASH / JUNCTIONS ===")
def followed_by(raws, tok, ch="/"):
    n = 0
    i = 0
    while True:
        i = raws.find(tok, i)
        if i < 0:
            return n
        j = i + len(tok)
        if j < len(raws) and raws[j] == ch:
            n += 1
        i += 1
fb = {t: followed_by(raw, t) for t in TOKENS}
print("followed_by_slash mine", fb, "sum", sum(fb.values()))
print("instrument tokens_followed_by_slash", inst["population"].get("tokens_followed_by_slash"))
print("trailing profile junction expected", sum(fb.values()),
      "instrument", inst["profiles"]["trailing_slash_sensitivity"]["stimulus_observations"])

print("\n=== E. NON-URL CHANGED LEAVES BY TOKEN (distinct_origins) ===")
vals = prof["distinct_origins"]["values"]
text = raw
for name in ORDER:
    text = text.replace("__%s__" % name, vals[name])
proj = json.loads(text)
pwalk = dict((p, s) for p, t, s in walk(proj))
nonurl = Counter()
for p, s in leaf_s.items():
    if pwalk.get(p) != s:
        if "url" not in tpl[p]:
            for tok in TOKENS:
                if tok in s:
                    nonurl[tok] += 1
print("non_url changed leaves attributed", dict(nonurl), "total", sum(nonurl.values()))
print("instrument non_url_field", inst["profiles"]["distinct_origins"]["changed_leaves_by_category"]["non_url_field"])
mustinc = Counter()
for p, s in leaf_s.items():
    if "must_include" in tpl[p] and pwalk.get(p) != s:
        for tok in TOKENS:
            if tok in s:
                mustinc[tok] += 1
print("must_include changed by token", dict(mustinc), "total", sum(mustinc.values()))
ann = [(p, s) for p, s in leaf_s.items() if "raw_annotation" in tpl[p] and pwalk.get(p) != s]
print("raw_annotation changed", [(p, s[:40], pwalk.get(p, "")[:40]) for p, s in ann])

print("\n=== F. TEMPLATE CENSUS (instrument convention) ===")
tcnt = Counter(tpl[p] for p, s in leaf_s.items() if TARGET in s)
print("TARGET leaves by template", dict(sorted(tcnt.items())))
allchg = Counter(tpl[p] for p, s in leaf_s.items() if pwalk.get(p) != s)
print("all changed by template mine", dict(sorted(allchg.items())))
print("instrument", dict(sorted(inst["profiles"]["distinct_origins"]["changed_leaves_by_path_template"].items())))
print("template_match", dict(allchg) == inst["profiles"]["distinct_origins"]["changed_leaves_by_path_template"])

print("\n=== G. TARGET LEAF DETAIL (pointer, template, occurrences, task) ===")
for p, s in leaf_s.items():
    if TARGET in s:
        print(p, tpl[p], s.count(TARGET), len(s))

print("\n=== H. CASE / VARIANT SCAN ===")
for pat in [r"(?i)__shopping__", r"(?i)__shopping_admin__", r"__SHOPPING_?__", r"_+SHOPPING_+"]:
    print(pat, len(re.findall(pat, raw)))
print("lowercase exact", raw.count("__shopping__"), "admin lower", raw.count("__shopping_admin__"))
print("occurrences of 'SHOPPING' bare", raw.count("SHOPPING"),
      "= target", raw.count(TARGET), "+admin", raw.count("__SHOPPING_ADMIN__"),
      "sum", raw.count(TARGET) + raw.count("__SHOPPING_ADMIN__"))

print("\n=== I. TOKEN VALUES CONTAIN TOKENS? ===")
for pname, pdef in prof.items():
    vs = pdef["values"]
    print(pname, {k: [t for t in TOKENS if t in v] for k, v in vs.items()})

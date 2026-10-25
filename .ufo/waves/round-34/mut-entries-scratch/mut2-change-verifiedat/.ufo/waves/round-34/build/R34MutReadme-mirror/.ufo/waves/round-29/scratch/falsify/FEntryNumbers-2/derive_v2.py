#!/usr/bin/env python3
"""Independent re-derivation of candidate v2 numbers.

Written from the S070 text contract (six ordered str.replace on the whole serialized
text, then json.loads, then enumerate) plus the pinned raw file and pinned profiles.
Does NOT read or import plans/config_projection.py.
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
RAW = ROOT / "plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF = ROOT / "plans/fixtures/r29/profiles.json"

TOK = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__", "__WIKIPEDIA__", "__MAP__"]
NM = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]

raw = RAW.read_text(encoding="utf-8")
profiles = json.loads(PROF.read_text(encoding="utf-8"))
data = json.loads(raw)

print("== population ==")
ids = [t["task_id"] for t in data]
print("input_tasks", len(data), "distinct_ids", len(set(ids)),
      "profiles", len(profiles), "task_profile_projections", len(data) * len(profiles))
print("index_equals_task_id", sum(1 for i, t in enumerate(data) if i == t["task_id"]))

print("\n== original token occurrences (literal text matches) ==")
occ = {t: raw.count(t) for t in TOK}
print(occ, "sum", sum(occ.values()))

print("\n== tasks carrying each token ==")
per_token_tasks = {}
for t in TOK:
    n = sum(1 for it in data if t in json.dumps(it, ensure_ascii=False))
    per_token_tasks[t] = n
print(per_token_tasks)

print("\n== task token-count distribution (the 790 + 22 = 834 bridge) ==")
dist = Counter()
for it in data:
    s = json.dumps(it, ensure_ascii=False)
    dist[sum(1 for t in TOK if t in s)] += 1
print("tasks by number of distinct tokens carried:", dict(sorted(dist.items())))
one = dist.get(1, 0)
two = dist.get(2, 0)
more = sum(v for k, v in dist.items() if k > 2)
print(f"one-token tasks {one}, two-token tasks {two}, >2 {more}")
print("sum of per-token task rows =", one + 2 * two + sum(k * v for k, v in dist.items() if k > 2))
print("distinct tasks with >=1 token =", sum(v for k, v in dist.items() if k > 0))
print("tasks with >=1 token =", sum(1 for it in data
      if any(t in json.dumps(it, ensure_ascii=False) for t in TOK)))

print("\n== other __..__ markers: occurrences / tasks ==")
mk = Counter()
mk_tasks = Counter()
for it in data:
    s = json.dumps(it, ensure_ascii=False)
    for m in re.findall(r"__[A-Za-z0-9_]+__", s):
        if m not in TOK:
            mk[m] += 1
            mk_tasks[m] += 1
# occurrences counted in the original raw text (not re-serialized)
raw_mk = Counter()
for m in re.findall(r"__[A-Za-z0-9_]+__", raw):
    if m not in TOK:
        raw_mk[m] += 1
print("occurrences in original raw text:", dict(raw_mk))
print("tasks carrying each marker:", dict(mk_tasks))

print("\n== leaves: changed / total / multi-occurrence ==")


def leaves(o, p=""):
    if isinstance(o, dict):
        for k, val in o.items():
            yield from leaves(val, (p + "." + k) if p else k)
    elif isinstance(o, list):
        for val in o:
            yield from leaves(val, p + "[]")
    elif isinstance(o, str):
        yield p, o


L = list(leaves(data))
print("total_string_leaves", len(L))
occ_dist = Counter()
for p, v in L:
    n = sum(v.count(t) for t in TOK)
    if n:
        occ_dist[n] += 1
print("token occurrences per token-bearing leaf:", dict(sorted(occ_dist.items())))
multi = sum(v for k, v in occ_dist.items() if k > 1)
multi_occ = sum(k * v for k, v in occ_dist.items() if k > 1)
print("leaves with >1 occurrence:", multi, "holding", multi_occ, "occurrences")
print("token-bearing leaves:", sum(occ_dist.values()))
print("total occurrences:", sum(k * v for k, v in occ_dist.items()))
print("surplus =", sum(k * v for k, v in occ_dist.items()) - sum(occ_dist.values()))

print("\n== per-profile projection ==")
for pname, pdef in profiles.items():
    vals = pdef["values"]
    text = raw
    for t, nm in zip(TOK, NM):
        text = text.replace(t, vals[nm])
    d2 = json.loads(text)
    L1 = list(leaves(data))
    L2 = list(leaves(d2))
    by_tpl = Counter()
    changed = 0
    for (p1, v1), (p2, v2) in zip(L1, L2):
        assert p1 == p2
        if v1 != v2:
            changed += 1
            by_tpl[p1] += 1
    url = sum(by_tpl[k] for k in by_tpl if k in
              ("start_url", "eval.program_html[].url", "eval.reference_url"))
    nonurl = changed - url
    # junction occurrences: value's own trailing '/' immediately followed by raw '/'
    junc = 0
    junc_tasks = set()
    for t, nm in zip(TOK, NM):
        val = vals[nm]
        if not val.endswith("/"):
            continue
        start = 0
        while True:
            i = text.find(val, start)
            if i < 0:
                break
            if text[i + len(val):i + len(val) + 1] == "/":
                junc += 1
            start = i + 1
    # tasks containing a junction: count via per-task projected text
    junc_task_ids = 0
    for t2, d in enumerate(d2):
        s = json.dumps(d, ensure_ascii=False)
        if any(s.count(vals[nm] + "/") > 0 for nm in NM if vals[nm].endswith("/")):
            junc_task_ids += 1
    rem_text = {t: text.count(t) for t in TOK}
    rem_dec = {t: sum(v.count(t) for _, v in L2) for t in TOK}
    print(f"\n-- {pname} --")
    print("parsed_tasks", len(d2), "string_leaves", len(L2), "changed_leaves", changed)
    print("changed_by_path_template", dict(sorted(by_tpl.items())))
    print("url_field", url, "non_url_field", nonurl)
    print("remaining_text", rem_text, "remaining_decoded", rem_dec)
    print("junction_occurrences", junc, "junction_tasks", junc_task_ids)
    print("profile values contain a token?", {nm: any(t in vals[nm] for t in TOK) for nm in NM})
    print("values all http:// scheme?", {nm: vals[nm].startswith("http://") for nm in NM})

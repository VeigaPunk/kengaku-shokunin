#!/usr/bin/env python3
"""Independent re-derivation of the round-29 config-projection numbers.

Derives from the pinned generator bytes + pinned raw task file + pinned profiles.
Does NOT read or import plans/config_projection.py.
"""
import json
import re
from pathlib import Path

ROOT = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
GEN = ROOT / "plans/fixtures/r29/generate_test_data.py"
RAW = ROOT / "plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF = ROOT / "plans/fixtures/r29/profiles.json"

TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__", "__WIKIPEDIA__", "__MAP__"]
# generator line 11..16 order, by source token
GEN_ORDER = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__", "__WIKIPEDIA__", "__MAP__"]
NAMES = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]

raw_text = RAW.read_text(encoding="utf-8")
profiles = json.loads(PROF.read_text(encoding="utf-8"))

print("== raw text ==")
print("raw_bytes", len(raw_text.encode()), "raw_codepoints", len(raw_text))
print("ascii_only", raw_text.isascii())
print("has_CR", "\r" in raw_text)

print("\n== original occurrences (literal text matches in original input) ==")
orig_occ = {}
for t in TOKENS:
    orig_occ[t] = raw_text.count(t)
print(orig_occ)
print("sum_orig_occ", sum(orig_occ.values()))

print("\n== all __..__ marker-like tokens in original text ==")
markers = {}
for m in re.findall(r"__[A-Za-z0-9_]+__", raw_text):
    markers[m] = markers.get(m, 0) + 1
print(markers)

print("\n== token occurrences followed by '/' in the original text ==")
follow_slash = {}
total_follow = 0
for t in TOKENS:
    c = len(re.findall(re.escape(t) + r"/", raw_text))
    follow_slash[t] = c
    total_follow += c
print(follow_slash, "total", total_follow)

orig_data = json.loads(raw_text)
print("\n== parsed original ==")
print("tasks", len(orig_data))
ids = [it["task_id"] for it in orig_data]
print("distinct_ids", len(set(ids)))
print("index_eq_task_id", sum(1 for i, it in enumerate(orig_data) if i == it["task_id"]))


def leaves(obj, path=""):
    """Yield (path_template, value) for every string leaf, with [] collapsed."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from leaves(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for v in obj:
            yield from leaves(v, f"{path}[]")
    elif isinstance(obj, str):
        yield path, obj


def template(p):
    # collapse numeric-ish path segments already collapsed to []
    return p


def path_template(p):
    return re.sub(r"\.\w+\[\]", "[]", p)


orig_leaf_list = list(leaves(orig_data))
print("string_leaves_original", len(orig_leaf_list))
print("distinct_path_templates_with_strings", len({path_template(p) for p, _ in orig_leaf_list}))

# per-profile
for pname, pdef in profiles.items():
    vals = pdef["values"]
    text = raw_text
    for tok, nm in zip(GEN_ORDER, NAMES):
        text = text.replace(tok, vals[nm])
    data = json.loads(text)
    new_leaf_list = list(leaves(data))
    # map by path+index order: compare positionally
    orig_map = {}
    for p, v in orig_leaf_list:
        orig_map.setdefault(path_template(p), []).append(v)
    new_map = {}
    for p, v in new_leaf_list:
        new_map.setdefault(path_template(p), []).append(v)
    changed_by_tpl = {}
    changed_total = 0
    multi_occ = 0
    for tpl, ovals in orig_map.items():
        nvals = new_map.get(tpl, [])
        for a, b in zip(ovals, nvals):
            if a != b:
                changed_total += 1
                changed_by_tpl[tpl] = changed_by_tpl.get(tpl, 0) + 1
                n_occ = sum(a.count(t) for t in TOKENS)
                if n_occ > 1:
                    multi_occ += 1
    url_fields = {"start_url", "eval.program_html[].url", "eval.reference_url"}
    url_n = sum(v for k, v in changed_by_tpl.items() if k in url_fields)
    non_url_n = changed_total - url_n
    remaining_text = {t: text.count(t) for t in TOKENS}
    remaining_decoded = {t: sum(v.count(t) for _, v in new_leaf_list) for t in TOKENS}
    other_markers = {}
    for m in re.findall(r"__[A-Za-z0-9_]+__", text):
        if m not in TOKENS:
            other_markers[m] = other_markers.get(m, 0) + 1
    junctions = text.count("//")
    print(f"\n-- profile {pname} --")
    print("parsed_tasks", len(data))
    print("string_leaves_projected", len(new_leaf_list))
    print("changed_leaves", changed_total, "multi_occ_leaves", multi_occ)
    print("changed_by_template", dict(sorted(changed_by_tpl.items())))
    print("url_field", url_n, "non_url_field", non_url_n)
    print("remaining_known_tokens_text", remaining_text)
    print("remaining_known_tokens_decoded", remaining_decoded)
    print("other_markers", other_markers)
    print("all_double_slash_substrings", junctions)
    print("changed_task_count", sum(1 for i, (o, n) in enumerate(zip(orig_data, data)) if o != n))
    print("index_eq_task_id", sum(1 for i, it in enumerate(data) if i == it["task_id"]))
    print("projected_text_sha256", __import__("hashlib").sha256(text.encode()).hexdigest())

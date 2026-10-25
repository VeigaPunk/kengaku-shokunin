#!/usr/bin/env python3
"""Independent read-only census of pinned r29 inputs (review seat R29ReviewLeafIdentity).

Does not import or execute upstream generator code; only reads pinned bytes.
"""
import hashlib
import json
import os
import re
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = os.path.join(ROOT, "plans/fixtures/r28/webarena/config_files/test.raw.json")
PROF = os.path.join(ROOT, "plans/fixtures/r29/profiles.json")
SRC = os.path.join(ROOT, "plans/fixtures/r29/generate_test_data.py")
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOKENS = ["__%s__" % t for t in ORDER]

out = {}
raw_bytes = open(RAW, "rb").read()
raw_text = raw_bytes.decode("utf-8")
out["raw_sha256"] = hashlib.sha256(raw_bytes).hexdigest()
out["raw_bytes"] = len(raw_bytes)
out["raw_chars"] = len(raw_text)
out["non_ascii_chars"] = sum(1 for c in raw_text if ord(c) > 127)
out["non_ascii_bytes"] = len(raw_bytes) - len(raw_text.encode("ascii", "ignore")) if out["non_ascii_chars"] == 0 else None
# byte vs codepoint divergence check
try:
    raw_text.encode("ascii")
    out["ascii_only"] = True
except UnicodeEncodeError:
    out["ascii_only"] = False
    out["first_non_ascii_codepoint"] = next(i for i, c in enumerate(raw_text) if ord(c) > 127)
    out["byte_len_prefix_to_first_nonascii"] = len(raw_text[:out["first_non_ascii_codepoint"]].encode("utf-8"))
    out["non_ascii_examples"] = sorted({c for c in raw_text if ord(c) > 127})[:20]

data = json.loads(raw_text)
out["items"] = len(data)
ids = [it.get("task_id") for it in data]
out["distinct_task_ids"] = len(set(ids))
out["all_have_task_id"] = all("task_id" in it for it in data)
out["task_id_types"] = sorted({type(i).__name__ for i in ids})
out["task_id_is_str"] = all(isinstance(i, str) for i in ids)
out["index_eq_taskid_count"] = sum(1 for idx, it in enumerate(data) if str(idx) == it.get("task_id"))
out["index_eq_taskid_mismatch_examples"] = [
    (idx, it.get("task_id")) for idx, it in enumerate(data) if str(idx) != it.get("task_id")
][:10]
out["task_id_min_max"] = (min(ids), max(ids))
# zero-padded style?
out["task_id_sample"] = ids[:5] + ids[-5:]

# raw occurrence counts per token in serialized text
counts = {}
for t, tok in zip(ORDER, TOKENS):
    counts[t] = raw_text.count(tok)
out["raw_token_occurrences"] = counts
out["raw_token_occurrence_total"] = sum(counts.values())

# any other __X__ placeholders
others = sorted({m for m in re.findall(r"__[A-Z][A-Z0-9_]*__", raw_text) if m not in TOKENS})
out["other_placeholders"] = others

# token occurrences inside JSON key names?
def walk(obj, path="$"):
    if isinstance(obj, dict):
        for k, v in obj.items():
            for t, tok in zip(ORDER, TOKENS):
                if tok in k:
                    out.setdefault("tokens_in_keys", []).append((path + "." + k, t))
            walk(v, path + "." + k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk(v, "%s[%d]" % (path, i))
    elif isinstance(obj, str):
        for t, tok in zip(ORDER, TOKENS):
            c = obj.count(tok)
            if c:
                out.setdefault("leaf_tokens", []).append((path, t, c, obj))

walk(data)
out["tokens_in_keys"] = out.get("tokens_in_keys", [])
lt = out.get("leaf_tokens", [])
out["leaves_with_tokens"] = len(lt)
out["leaf_occurrences_total"] = sum(x[2] for x in lt)
out["multi_token_leaves"] = [(p, t, c) for (p, t, c, _) in lt if c > 1][:20]
out["multi_token_leaf_count"] = sum(1 for x in lt if x[2] > 1)

# distinct leaf paths (normalized: strip [i] indices)
def norm(p):
    return re.sub(r"\[\d+\]", "[]", p)

pathcensus = {}
for (p, t, c, val) in lt:
    pathcensus.setdefault(norm(p), {"tokens": {}, "occ": 0, "sample_value": val})
    pathcensus[norm(p)]["tokens"][t] = pathcensus[norm(p)]["tokens"].get(t, 0) + 1
    pathcensus[norm(p)]["occ"] += c
out["distinct_leaf_paths"] = len(pathcensus)
out["path_census"] = pathcensus

# which top-level fields carry tokens
top = {}
for (p, t, c, v) in lt:
    key = p.split(".")[1].split("[")[0]
    top[key] = top.get(key, 0) + c
out["top_field_token_occurrences"] = top

# per-task changed leaf counts (distinct leaves) under profile distinct_origins
prof = json.load(open(PROF))
out["profile_names"] = list(prof.keys())
p0 = prof["distinct_origins"]["values"]

# projected text via global sequential replacement (faithful: serialized text)
proj_text = raw_text
per_token_repl_counts = {}
for t, tok in zip(ORDER, TOKENS):
    n = proj_text.count(tok)
    per_token_repl_counts[t] = n
    proj_text = proj_text.replace(tok, p0[t])
out["per_token_repl_counts_in_order"] = per_token_repl_counts
out["proj_text_sha256_distinct_origins"] = hashlib.sha256(proj_text.encode("utf-8")).hexdigest()
try:
    pdata = json.loads(proj_text)
    out["distinct_origins_parses"] = True
    out["distinct_origins_items"] = len(pdata)
except Exception as e:
    out["distinct_origins_parses"] = False
    out["distinct_origins_error"] = repr(e)

# compare projected parsed objects to raw parsed objects: which fields differ
def diff_leaves(a, b, path="$"):
    if type(a) is not type(b):
        yield (path, "type", a, b)
        return
    if isinstance(a, dict):
        for k in a:
            if k in b:
                yield from diff_leaves(a[k], b[k], path + "." + k)
            else:
                yield (path + "." + k, "missing_in_projected", a[k], None)
        for k in b:
            if k not in a:
                yield (path + "." + k, "added_in_projected", None, b[k])
    elif isinstance(a, list):
        if len(a) != len(b):
            yield (path, "len", len(a), len(b))
            return
        for i, (x, y) in enumerate(zip(a, b)):
            yield from diff_leaves(x, y, "%s[%d]" % (path, i))
    else:
        if a != b:
            yield (path, "value", a, b)

if out.get("distinct_origins_parses"):
    dl = list(diff_leaves(data, pdata))
    out["distinct_origins_changed_leaf_paths"] = len(dl)
    out["distinct_origins_changed_paths_norm"] = sorted({norm(d[0]) for d in dl})
    out["distinct_origins_changed_top_fields"] = sorted({d[0].split(".")[1].split("[")[0] for d in dl})
    out["distinct_origins_changed_value_examples"] = [
        (d[0], d[1], d[2], d[3]) for d in dl if d[0].endswith(".start_url") or "intent" in d[0]
    ][:8]
    # per-task changed leaf count distribution
    percount = {}
    for d in dl:
        tid = d[0].split(".")[1].split("[")[0]
        percount[tid] = percount.get(tid, 0) + 1
    out["tasks_with_any_change"] = len(percount)
    out["changed_leaf_count_histogram"] = {}
    for v in percount.values():
        out["changed_leaf_count_histogram"][str(v)] = out["changed_leaf_count_histogram"].get(str(v), 0) + 1
    out["per_task_changed_leaves_total"] = len(dl)
    # tasks whose projected task_id changed? (no)
    out["tasks_with_changed_task_id"] = sum(1 for d in dl if d[0].endswith(".task_id"))

# per-profile parse + counts
prof_summary = {}
for name, spec in prof.items():
    vals = spec["values"]
    pt = raw_text
    cnt = {}
    for t, tok in zip(ORDER, TOKENS):
        cnt[t] = pt.count(tok)
        pt = pt.replace(tok, vals[t])
    try:
        pd = json.loads(pt)
        prof_summary[name] = {
            "parses": True,
            "items": len(pd),
            "per_token_counts": cnt,
            "text_sha256": hashlib.sha256(pt.encode("utf-8")).hexdigest(),
            "bytes": len(pt.encode("utf-8")),
            "changed_leaves": len(list(diff_leaves(data, pd))),
            "changed_paths_norm": sorted({norm(d[0]) for d in diff_leaves(data, pd)}),
        }
    except Exception as e:
        prof_summary[name] = {"parses": False, "error": repr(e), "per_token_counts": cnt}
out["profile_summary"] = prof_summary

# sensitivity checks on field content (no credential/cookie stores in lane output)
sensitive = {}
for idx, it in enumerate(data[:0]):
    pass
ss = data[0].get("storage_state")
out["storage_state_type"] = type(ss).__name__
out["storage_state_sample"] = json.dumps(ss)[:400]
inst = data[0].get("instantiation_dict")
out["instantiation_dict_sample"] = json.dumps(inst)[:400]
out["eval_keys_sample"] = sorted(data[0].get("eval", {}).keys()) if isinstance(data[0].get("eval"), dict) else None
out["item0"] = json.dumps(data[0], indent=1)[:2500]

# global scan: any string values that look like cookies/credentials/tokens?
pat = re.compile(r"(cookie|secret|password|passwd|token|api_key|authorization|bearer)", re.I)
hits = {}

def walk2(obj, path="$"):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if pat.search(str(k)):
                hits.setdefault("key_hits", []).append(path + "." + str(k))
            walk2(v, path + "." + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk2(v, "%s[%d]" % (path, i))
    elif isinstance(obj, str):
        if pat.search(obj):
            hits.setdefault("value_hits", []).append((path, obj[:120]))

walk2(data)
out["sensitive_key_hits"] = hits.get("key_hits", [])[:20]
out["sensitive_key_hit_count"] = len(hits.get("key_hits", []))
out["sensitive_value_hits"] = hits.get("value_hits", [])[:20]
out["sensitive_value_hit_count"] = len(hits.get("value_hits", []))

# does raw text contain real webarena default hosts (wrong-default copy risk)?
out["raw_contains_gitlab_host"] = "gitlab" in raw_text.lower()
out["raw_hostish_sample"] = sorted(set(re.findall(r"https?://[^\"\s,]+", raw_text)))[:12]
out["raw_hostish_count"] = len(set(re.findall(r"https?://[^\"\s,]+", raw_text)))

json.dump(out, sys.stdout, indent=1, default=str)

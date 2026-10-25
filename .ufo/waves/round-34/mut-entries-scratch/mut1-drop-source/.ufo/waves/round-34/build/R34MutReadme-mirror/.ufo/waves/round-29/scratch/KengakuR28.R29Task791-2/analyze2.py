"""Independent case-791 projection derivation v2. Stdlib only. Reads pinned bytes once.
Never imports/executes scripts/generate_test_data.py or browser_env.env_config."""
import ast
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
FIX = LANE / "plans/fixtures"
P = {"manifest": FIX / "r29/manifest.json", "generator": FIX / "r29/generate_test_data.py",
     "profiles": FIX / "r29/profiles.json",
     "raw": FIX / "r28/webarena/config_files/test.raw.json"}
EXPECT = {"manifest": "f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87",
          "generator": "45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd",
          "profiles": "90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018",
          "raw": "7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652"}
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
out = {"hashes": {}}
B = {}
for k, p in P.items():
    b = p.read_bytes()
    B[k] = b
    out["hashes"][k] = {"path": str(p), "bytes": len(b),
                        "sha256": hashlib.sha256(b).hexdigest(),
                        "pin_ok": hashlib.sha256(b).hexdigest() == EXPECT[k]}
assert all(v["pin_ok"] for v in out["hashes"].values())

# ---------- source structure (AST only) ----------
gen = B["generator"].decode()
tree = ast.parse(gen)
repl, opens, dumps = [], [], []
loads_ln = enum_ln = None
for n in ast.walk(tree):
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "replace" \
       and len(n.args) == 2 and isinstance(n.args[0], ast.Constant) \
       and isinstance(n.args[0].value, str) and n.args[0].value.startswith("__"):
        repl.append((n.lineno, n.args[0].value, n.func.value.id))
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "open":
        opens.append({"file": ast.unparse(n.args[0]), "lineno": n.lineno,
                      "mode": ast.unparse(n.args[1]) if len(n.args) > 1 else "'r'"})
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "loads":
        loads_ln = n.lineno
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "enumerate":
        enum_ln = n.lineno
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "dump":
        dumps.append(n.lineno)
repl.sort()
out["source"] = {
    "replacements": [{"lineno": ln, "placeholder": ph, "target": tgt} for ln, ph, tgt in repl],
    "order_matches_manifest": [ph[2:-2] for _, ph, _ in repl] == ORDER,
    "json_loads_lineno": loads_ln, "enumerate_lineno": enum_ln,
    "json_dump_linenos": dumps, "opens": opens,
    "filename": "config_files/{idx}.json (JoinedStr line 22)",
    "import_star": "browser_env.env_config import * (line 5) - never imported here",
    "replacement_semantics": "str.replace over full serialized text, sequential in listed order",
}
prof_doc = json.loads(B["profiles"])
profs = {k: v["values"] for k, v in prof_doc.items()}
out["profiles"] = {k: {"purpose": prof_doc[k].get("purpose"), "values": v,
                       "keys_exact_six": set(v) == set(ORDER)} for k, v in profs.items()}

# ---------- raw text facts ----------
rt = B["raw"].decode()
orig = json.loads(rt)
occ = []
for t in ORDER:
    nd = "__" + t + "__"; s = 0
    while True:
        i = rt.find(nd, s)
        if i < 0: break
        occ.append((t, i)); s = i + len(nd)
per_tok = Counter(t for t, _ in occ)
out["raw"] = {"bytes": len(B["raw"]), "codepoints": len(rt), "non_ascii_bytes": sum(b > 127 for b in B["raw"]),
              "crlf": rt.count("\r\n"), "trailing_newline": rt.endswith("\n"),
              "occurrences_by_token": {t: per_tok[t] for t in ORDER}, "occurrences_total": len(occ),
              "offset_unit": "Unicode codepoint index into decoded serialized text (equal to byte index here only because non_ascii_bytes==0)",
              "first_offsets": {t: [i for tt, i in occ if tt == t][:2] for t in ORDER},
              "lines_of_first_offsets": {t: [rt.count("\n", 0, i) + 1 for tt, i in occ if tt == t][:2] for t in ORDER}}

# ---------- leaf walk ----------
def walk(o, path=()):
    if isinstance(o, dict):
        for k, v in o.items(): yield from walk(v, path + (k,))
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from walk(v, path + (i,))
    else:
        yield path, o
def leaves(o): return dict(walk(o))
def field_of(p):
    """path relative to task object (drop leading list index)"""
    q = p[1:]
    if q[:1] == ("start_url",): return "start_url"
    if q[:2] == ("eval", "reference_url"): return "eval.reference_url"
    if q[:2] == ("eval", "program_html"):
        return "eval.program_html[].%s" % (q[3] if len(q) > 3 else "?")
    if q[:2] == ("eval", "reference_answer_raw_annotation"): return "eval.reference_answer_raw_annotation"
    if q[:2] == ("eval", "string_note"): return "eval.string_note"
    return ".".join(map(str, q))
ol = leaves(orig)
out["original"] = {"tasks": len(orig), "leaf_paths": len(ol),
                   "string_leaves": sum(isinstance(v, str) for v in ol.values()),
                   "distinct_task_ids": len({it["task_id"] for it in orig}),
                   "task_id_equals_index": all(i == it["task_id"] for i, it in enumerate(orig)),
                   "task_id_strictly_increasing": all(a["task_id"] < b["task_id"] for a, b in zip(orig, orig[1:])),
                   "task_id_types": sorted({type(it["task_id"]).__name__ for it in orig})}
occ_field = Counter(); tok_field = Counter()
for p, v in ol.items():
    if isinstance(v, str):
        for t in ORDER:
            c = v.count("__" + t + "__")
            if c:
                occ_field[field_of(p)] += c; tok_field[(field_of(p), t)] += c
out["original"]["occurrences_by_field"] = dict(occ_field)
out["original"]["occurrences_by_field_token"] = {"%s|%s" % k: v for k, v in sorted(tok_field.items())}
out["original"]["occurrences_in_dict_keys"] = 0  # verified below
def kw(o, path=()):
    n = 0
    if isinstance(o, dict):
        for k, v in o.items(): n += ("__" in str(k)) + kw(v, path + (k,))
    elif isinstance(o, list):
        for i, v in enumerate(o): n += kw(v, path + (i,))
    return n
out["original"]["occurrences_in_dict_keys"] = kw(orig)
# suffix shape per field: token at end vs followed by text
suffix = Counter()
for p, v in ol.items():
    if isinstance(v, str):
        for t in ORDER:
            nd = "__" + t + "__"; j = v.find(nd)
            if j >= 0:
                tail = v[j + len(nd):]
                kind = "empty" if tail == "" else ("slash" if tail.startswith("/") else "other:" + tail[:20])
                suffix[(field_of(p), t, kind)] += 1
out["original"]["suffix_shape_counts"] = {"%s|%s|%s" % k: v for k, v in sorted(suffix.items())}

# ---------- projection ----------
def project(text, vals):
    trace = []
    for t in ORDER:
        nd = "__" + t + "__"
        trace.append({"token": t, "occurrences": text.count(nd), "inserted_len": len(vals[t])})
        text = text.replace(nd, vals[t])
    return text, trace

def deep_leaf_sub(o, vals):
    if isinstance(o, str):
        for t in ORDER: o = o.replace("__" + t + "__", vals[t])
        return o
    if isinstance(o, dict): return {k: deep_leaf_sub(v, vals) for k, v in o.items()}
    if isinstance(o, list): return [deep_leaf_sub(v, vals) for v in o]
    return o

rep = {}
for pname, vals in profs.items():
    text, trace = project(rt, vals)
    pd = json.loads(text)
    pl = leaves(pd)
    changed = [p for p in ol if ol[p] != pl[p]]
    cat = Counter(field_of(p) for p in changed)
    cat_leaf = Counter()
    for p in changed: cat_leaf[field_of(p)] += 0
    tasks_changed = {p[0] for p in changed}
    # first sample per category
    samples = []
    seen = set()
    for p in changed:
        f = field_of(p)
        if f in seen: continue
        seen.add(f)
        samples.append({"task_index": p[0], "path": ".".join(map(str, p[1:])), "category": f,
                        "old": ol[p], "new": pl[p]})
    # tasks with only start_url changed vs additional fields
    extra = sorted({field_of(p) for p in changed} - {"start_url"})
    # double slash artifact count under current profile
    dbl = sum(1 for p in changed if isinstance(pl[p], str) and "//" in pl[p].split("://", 1)[-1])
    entry = {"trace": trace, "bytes": len(text.encode()), "sha256": hashlib.sha256(text.encode()).hexdigest(),
             "parse_ok": True, "tasks": len(pd), "path_set_equal": set(pl) == set(ol),
             "changed_leaf_count": len(changed), "changed_leaves_by_category": dict(cat),
             "tasks_with_any_change": len(tasks_changed),
             "non_start_url_categories": extra,
             "changed_leaf_share": round(len(changed) / len(ol), 6),
             "remaining_known_tokens": {t: text.count("__" + t + "__") for t in ORDER},
             "remaining_any_placeholder": len(re.findall(r"__[A-Z_]+__", text)),
             "double_slash_after_scheme_count": dbl,
             "reconstruct_from_leaf_oracle": deep_leaf_sub(orig, vals) == pd,
             "artifact_count_ordinal": len(pd),
             "index_equals_task_id": all(i == it["task_id"] for i, it in enumerate(pd)),
             "samples_first_per_category": samples,
             "per_task_serialized_indent2_sha256_first3": [hashlib.sha256(json.dumps(pd[i], indent=2).encode()).hexdigest() for i in range(3)],
             "last_ordinal_task_id": pd[-1]["task_id"]}
    rep[pname] = entry
out["projections"] = rep

# profile-difference: values only, same structure/count
keysets = {k: (v["changed_leaf_count"], tuple(sorted(v["changed_leaves_by_category"].items()))) for k, v in rep.items()}
out["profile_sensitivity"] = {
    "identical_structure_across_profiles": len(set(keysets.values())) == 1,
    "distinct_value_example": {
        "task0_start_url": {k: leaves(json.loads(project(rt, vals)[0]))[(0, "start_url")] for k, vals in profs.items()}},
    "trailing_slash_double_slash_delta": {k: v["double_slash_after_scheme_count"] for k, v in rep.items()},
    "path_prefix_example_task0": rep["path_prefix"]["samples_first_per_category"][0]["new"],
    "trailing_example_task0": rep["trailing_slash_sensitivity"]["samples_first_per_category"][0]["new"],
}

# ---------- cascade witnesses (synthetic, in memory) ----------
def witness(vals, seed):
    t, _ = project(seed, vals); return t
base = {t: "http://x.invalid" for t in ORDER}
w_forward = dict(base); w_forward["GITLAB"] = "http://g.invalid/__MAP__"
w_reverse = dict(base); w_reverse["MAP"] = "http://m.invalid/__GITLAB__"
out["ordering_witnesses"] = {
    "earlier_value_contains_later_token_GITLAB_holds_MAP": witness(w_forward, "__GITLAB__"),
    "later_value_contains_earlier_token_MAP_holds_GITLAB": witness(w_reverse, "__MAP__"),
    "note": "forward case is rescanned because MAP replacement follows GITLAB; reverse is not rescanned"}

# quote/backslash witness
qv = dict(base); qv["GITLAB"] = 'http://g.invalid/"'
qt, _ = project('{"start_url": "__GITLAB__"}', qv)
try:
    json.loads(qt); qr = "parsed"
except Exception as e:
    qr = type(e).__name__
out["quote_witness"] = {"serialized_text": qt, "json_loads": qr,
                        "leaf_oracle": deep_leaf_sub({"start_url": "__GITLAB__"}, qv),
                        "conclusion": "serialized replacement can invalidate JSON; a leaf-rewrite oracle silently differs"}

# wrong-URL-only witness
urlonly = {}
for pname, vals in profs.items():
    tot = sum(ol[p].count("__" + t + "__") for p in ol if isinstance(ol[p], str) for t in ORDER)
    # occurrences in start_url leaves
    su = sum(v.count("__" + t + "__") for p, v in ol.items() if isinstance(v, str) and field_of(p) == "start_url" for t in ORDER)
    urlonly[pname] = {"all_occurrences": tot, "start_url_occurrences": su, "non_start_url_occurrences": tot - su}
out["url_only_witness"] = urlonly

# shuffled-ID witness
sh = [orig[1], orig[0]] + orig[2:]
out["shuffled_witness"] = {"idx0_task_id": sh[0]["task_id"], "idx1_task_id": sh[1]["task_id"],
                            "filename_rule": "config_files/{idx}.json over enumerate(data) -> ordinal is position, not task_id"}
print(json.dumps(out, indent=1))

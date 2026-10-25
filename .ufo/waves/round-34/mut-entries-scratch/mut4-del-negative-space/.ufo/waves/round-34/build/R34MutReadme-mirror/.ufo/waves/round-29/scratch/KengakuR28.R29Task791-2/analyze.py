"""Independent case-791 projection derivation. Stdlib only. Reads pinned bytes once.
Does not import or execute scripts/generate_test_data.py or browser_env.env_config."""
import ast
import hashlib
import json
import re
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
FIX = LANE / "plans/fixtures"
P_GEN = FIX / "r29/generate_test_data.py"
P_MAN = FIX / "r29/manifest.json"
P_PROF = FIX / "r29/profiles.json"
P_RAW = FIX / "r28/webarena/config_files/test.raw.json"

EXPECT = {
    "manifest": "f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87",
    "generator": "45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd",
    "profiles": "90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018",
    "raw": "7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652",
}
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]

out = {}
raw_bytes = {}
for key, path in (("manifest", P_MAN), ("generator", P_GEN), ("profiles", P_PROF), ("raw", P_RAW)):
    b = path.read_bytes()
    raw_bytes[key] = b
    out.setdefault("hashes", {})[key] = {
        "path": str(path), "bytes": len(b),
        "sha256": hashlib.sha256(b).hexdigest(),
        "pin_ok": hashlib.sha256(b).hexdigest() == EXPECT[key],
    }
assert all(v["pin_ok"] for v in out["hashes"].values()), "pin mismatch"

man = json.loads(raw_bytes["manifest"])
prof_doc = json.loads(raw_bytes["profiles"])

# --- source structure (AST only; never exec/import) ---
gen_src = raw_bytes["generator"].decode("utf-8")
tree = ast.parse(gen_src)
src_repl = []
reads = []
loads_at = None
enum_at = None
fname_fmt = []
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "replace":
        if (len(node.args) == 2 and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str) and node.args[0].value.startswith("__")):
            target = node.func.value
            src_repl.append({
                "placeholder": node.args[0].value,
                "var": target.id if isinstance(target, ast.Name) else ast.dump(target),
                "lineno": node.lineno,
                "order_index": len(src_repl),
            })
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "open":
        mode = node.args[1].value if len(node.args) > 1 else "r"
        reads.append({"file": getattr(node.args[0], "value", ast.dump(node.args[0])), "mode": mode, "lineno": node.lineno})
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "loads":
        loads_at = node.lineno
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "enumerate":
        enum_at = node.lineno
    if isinstance(node, ast.JoinedStr):
        fname_fmt.append(("JoinedStr", node.lineno, ast.unparse(node)))
out["source_contract"] = {
    "replacements": src_repl,
    "order_matches_expectation": [r["placeholder"][2:-2] for r in src_repl] == ORDER,
    "json_loads_lineno": loads_at,
    "enumerate_lineno": enum_at,
    "open_calls": reads,
    "filename_expressions": fname_fmt,
    "imports": sorted({(n.module or "") if isinstance(n, ast.ImportFrom) else a.name
                       for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))
                       for a in (n.names if isinstance(n, ast.Import) else [None])}),
}

# --- profiles ---
profiles = {}
for pname, pobj in prof_doc.items():
    vals = pobj["values"]
    assert set(vals) == set(ORDER), (pname, set(vals))
    profiles[pname] = vals

# --- raw text facts ---
raw_text = raw_bytes["raw"].decode("utf-8")
out["raw_text"] = {
    "bytes": len(raw_bytes["raw"]),
    "utf8_codepoints": len(raw_text),
    "non_ascii_bytes": sum(1 for b in raw_bytes["raw"] if b > 127),
    "crlf": raw_text.count("\r\n"),
    "trailing_newline": raw_text.endswith("\n"),
    "bom": raw_bytes["raw"].startswith(b"\xef\xbb\xbf"),
}
orig = json.loads(raw_text)

# occurrences with codepoint offsets and line numbers
occ = []
for tok in ORDER:
    needle = "__" + tok + "__"
    start = 0
    while True:
        i = raw_text.find(needle, start)
        if i < 0:
            break
        occ.append({"token": tok, "needle": needle, "cp_offset": i,
                    "line": raw_text.count("\n", 0, i) + 1})
        start = i + len(needle)
out["raw_occurrences"] = {
    "per_token": {t: sum(1 for o in occ if o["token"] == t) for t in ORDER},
    "total": len(occ),
    "first_offsets_by_token": {t: [o["cp_offset"] for o in occ if o["token"] == t][:3] for t in ORDER},
    "last_offsets_by_token": {t: [o["cp_offset"] for o in occ if o["token"] == t][-3:] for t in ORDER},
    "offset_unit": "Unicode codepoint index into utf-8-decoded serialized text; here equal to byte index because non_ascii_bytes==0",
}

# --- leaf census on ORIGINAL parsed object ---
def walk(obj, path=()):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, path + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, path + (i,))
    else:
        yield path, obj

def leaves(obj):
    return {p: v for p, v in walk(obj)}

orig_leaves = leaves(orig)
def keycount(leaves_map, tok):
    n = 0
    for p, v in leaves_map.items():
        if isinstance(v, str):
            n += v.count("__" + tok + "__")
    return n

out["leaf_census_original"] = {
    "task_count": len(orig),
    "leaf_paths": len(orig_leaves),
    "string_leaves": sum(1 for v in orig_leaves.values() if isinstance(v, str)),
    "token_occurrences_in_string_leaves": {t: keycount(orig_leaves, t) for t in ORDER},
    "token_occurrences_in_dict_keys": sum(1 for p, v in walk(orig) if False),
}
# dict-key token check
key_hits = []
def keywalk(obj, path=()):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if "__" in str(k):
                key_hits.append({"path": path + (k,), "key": k})
            keywalk(v, path + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            keywalk(v, path + (i,))
keywalk(orig)
out["leaf_census_original"]["token_occurrences_in_dict_keys"] = len(key_hits)

# per-field token counts
field_counts = {}
for t in ORDER:
    c = {}
    for p, v in orig_leaves.items():
        if isinstance(v, str):
            k = v.count("__" + t + "__")
            if k:
                field = ".".join(str(x) for x in p)
                c[field] = c.get(field, 0) + k
    field_counts[t] = c
out["leaf_census_original"]["per_leaf_field_counts"] = field_counts

# distinct distinct original values with suffix after token
distinct = {}
for p, v in orig_leaves.items():
    if isinstance(v, str):
        ctx = tuple(t for t in ORDER if "__" + t + "__" in v)
        if ctx:
            field = p[0] if p else "?"
            if p[:2] == ("eval", "program_html"):
                field = "eval.program_html[].url"
            elif p[:2] == ("eval", "reference_url"):
                field = "eval.reference_url"
            elif p[0] == "start_url":
                field = "start_url"
            distinct.setdefault((field, ctx, v), 0)
            distinct[(field, ctx, v)] += 1
out["distinct_changed_original_values"] = [
    {"field": k[0], "tokens": list(k[1]), "value": k[2], "leaf_count": n}
    for k, n in sorted(distinct.items(), key=lambda kv: (kv[0][0], kv[0][2]))
]

# --- projection per profile ---
def apply_globals(text, vals):
    trace = []
    for tok in ORDER:
        needle = "__" + tok + "__"
        before = text.count(needle)
        text = text.replace(needle, vals[tok])
        trace.append({"token": tok, "occurrences_replaced": before,
                      "value_len": len(vals[tok])})
    return text, trace

proj_report = {}
for pname, vals in profiles.items():
    text, trace = apply_globals(raw_text, vals)
    entry = {
        "replacement_trace": trace,
        "projected_text_bytes": len(text.encode("utf-8")),
        "projected_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "cascade_present": any(vals[t].find("__" + t2 + "__") >= 0
                               for t in ORDER for t2 in ORDER
                               if ORDER.index(t2) > ORDER.index(t)),
    }
    try:
        pdata = json.loads(text)
        perr = None
    except Exception as e:
        pdata, perr = None, repr(e)
    entry["json_parse_ok"] = pdata is not None
    entry["json_parse_error"] = perr
    if pdata is not None:
        entry["parsed_task_count"] = len(pdata)
        pleaves = leaves(pdata)
        entry["leaf_path_count_equal"] = set(pleaves) == set(orig_leaves)
        changed = []
        for p in orig_leaves:
            if orig_leaves.get(p) != pleaves.get(p):
                changed.append(p)
        entry["changed_leaf_count"] = len(changed)
        cats = {}
        for p in changed:
            if p[0] == "start_url":
                c = "start_url (navigation URL consumed)"
            elif p[:2] == ("eval", "reference_url"):
                c = "eval.reference_url (gold locator predicate)"
            elif p[:2] == ("eval", "program_html"):
                c = "eval.program_html.url (programmatic locator)"
            elif p[:2] == ("eval", "reference_answer_raw_annotation"):
                c = "eval.reference_answer_raw_annotation (annotation text)"
            else:
                c = ".".join(str(x) for x in p)
            cats[c] = cats.get(c, 0) + 1
        entry["changed_leaf_by_category"] = cats
        entry["tasks_with_change"] = len({p[0] for p in changed})
        entry["remaining_known_token_counts"] = {t: text.count("__" + t + "__") for t in ORDER}
        entry["remaining_placeholder_regex_count"] = len(re.findall(r"__[A-Z_]+__", text))
        # ordinal vs task_id
        tids = [it.get("task_id") for it in pdata]
        entry["index_equals_task_id"] = all(i == t for i, t in enumerate(tids))
        entry["task_id_types"] = sorted({type(t).__name__ for t in tids})
        entry["task_id_distinct"] = len(set(tids))
        entry["task_id_min_max"] = [min(tids), max(tids)]
        # reconstruct check: applying diffs to orig reproduces projected
        entry["meta_equal"] = all(
            {k: v for k, v in it.items() if k != "id"} ==
            {k: v for k, v in pit.items() if k != "id"}
            for it, pit in zip(orig, pdata)
        )
        # sample values
        samples = []
        for p in changed[:6]:
            samples.append({"path": list(p), "old": orig_leaves[p], "new": pleaves[p],
                            "levels_up_in_proj": text.count("\n", 0, 0)})
        entry["sample_changes"] = samples
        # per-task_id sample
        byid = []
        for tid in (0, 145, 300, 700):
            it = pdata[tid]
            d = []
            for p, v in walk(it):
                if isinstance(v, str) and v != orig_leaves.get((tid,) + p):
                    d.append({"path": list(p), "new": v})
            byid.append({"index": tid, "task_id": it.get("task_id"), "changed": d})
        entry["per_task_samples"] = byid
        # per-task serialized digest for first 3 tasks (mirrors upstream json.dump indent=2)
        entry["per_task_serialized_sha256_first3"] = [
            hashlib.sha256(json.dumps(pdata[i], indent=2).encode()).hexdigest() for i in range(3)
        ]
    proj_report[pname] = entry

out["projections"] = proj_report

# --- leaf-only oracle (independently implemented) vs serialized projection ---
def leaf_oracle(obj, vals):
    def sub(v):
        if isinstance(v, str):
            for t in ORDER:
                v = v.replace("__" + t + "__", vals[t])
            return v
        if isinstance(v, dict):
            return {k: sub(x) for k, x in v.items()}
        if isinstance(v, list):
            return [sub(x) for x in v]
        return v
    return sub(obj)

oracle_eq = {}
for pname, vals in profiles.items():
    lo = leaf_oracle(orig, vals)
    text, _ = apply_globals(raw_text, vals)
    serialized = json.loads(text)
    oracle_eq[pname] = {"equal": lo == serialized, "digest": hashlib.sha256(json.dumps(lo, sort_keys=True).encode()).hexdigest()}
out["leaf_oracle_equivalence_benign_profiles"] = oracle_eq

# --- cascade hand witness (in-memory, not fixture data) ---
casc_vals = {t: "http://x.invalid/" for t in ORDER}
casc_vals["MAP"] = "http://map.invalid/__WIKIPEDIA__"
casc_text, _ = apply_globals("__MAP__", casc_vals)
out["cascade_witness"] = {"input": "__MAP__", "map_value": casc_vals["MAP"],
                          "output_after_ordered_replacements": casc_text,
                          "later_token_consumed": casc_text == "http://map.invalid/http://wikipedia.invalid:10105"}

# --- quote/backslash hand witness: serialized replacement breaks JSON, leaf oracle does not ---
qvals = {t: "http://x.invalid/" for t in ORDER}
qvals["GITLAB"] = 'http://gitlab.invalid/"'
qtext, _ = apply_globals('{"start_url": "__GITLAB__"}', qvals)
try:
    json.loads(qtext); qparse = "ok"
except Exception as e:
    qparse = type(e).__name__
out["quote_witness"] = {"projected_text": qtext, "json_loads_result": qparse,
                        "leaf_oracle_result": leaf_oracle({"start_url": "__GITLAB__"}, qvals)}

# --- shuffled-ID witness (upstream enumerate index) ---
shuffled = [orig[1], orig[0]] + orig[2:]
out["shuffled_witness"] = {
    "filename_index_0_task_id": shuffled[0]["task_id"],
    "filename_index_1_task_id": shuffled[1]["task_id"],
    "upstream_filename_expression": "config_files/{idx}.json over enumerate(data)",
}

# --- wrong URL-only witness: replace only start_url leaves ---
urlonly = {}
for pname, vals in profiles.items():
    cnt = 0
    for p, v in orig_leaves.items():
        if isinstance(v, str):
            cnt += sum(v.count("__" + t + "__") for t in ORDER)
    replaced = 0
    for p, v in orig_leaves.items():
        if p and p[0] == "start_url" and isinstance(v, str):
            replaced += sum(v.count("__" + t + "__") for t in ORDER)
    urlonly[pname] = {"all_string_leaf_occurrences": cnt,
                      "in_start_url_only": replaced,
                      "left_behind": cnt - replaced}
out["url_only_witness"] = urlonly

print(json.dumps(out, indent=1))

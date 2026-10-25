#!/usr/bin/env python3
"""Independent __GITLAB__ census/oracle. Reads only prereg TEXT, generator bytes,
pinned fixtures and the instrument's stdout JSON. Never reads/imports
plans/config_projection.py source."""
import json, hashlib, re, sys
from collections import Counter, defaultdict

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW_P = LANE + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
GEN_P = LANE + "/plans/fixtures/r29/generate_test_data.py"
MAN_P = LANE + "/plans/fixtures/r29/manifest.json"
PRO_P = LANE + "/plans/fixtures/r29/profiles.json"
OUT_P = LANE + "/.ufo/waves/round-29/scratch/falsify/FTokenGitlab/out.json"

raw_bytes = open(RAW_P, "rb").read()
raw = raw_bytes.decode("utf-8")
gen_bytes = open(GEN_P, "rb").read()
man = json.load(open(MAN_P))
prof = json.load(open(PRO_P))
out = json.load(open(OUT_P))

R = {}
def put(k, v): R[k] = v

put("inputs", {
    "raw_sha256": hashlib.sha256(raw_bytes).hexdigest(),
    "gen_sha256": hashlib.sha256(gen_bytes).hexdigest(),
    "manifest_sha256": hashlib.sha256(open(MAN_P, "rb").read()).hexdigest(),
    "profiles_sha256": hashlib.sha256(open(PRO_P, "rb").read()).hexdigest(),
    "raw_is_ascii": raw_bytes == raw.encode("ascii"),
    "raw_has_cr": b"\r" in raw_bytes,
    "raw_chars": len(raw),
    "raw_bytes": len(raw_bytes),
})

order = man["replacement_order"]
toks = ["__" + t + "__" for t in order]
TOK = dict(zip(order, toks))

# --- source replacement contract (from generator bytes text, inert) ---
src = gen_bytes.decode("utf-8")
put("source_contract", {
    "replace_lines": [l.strip() for l in src.splitlines() if ".replace(" in l],
    "replace_order_from_bytes": re.findall(r'raw\s*=\s*raw\.replace\("(__[A-Z_]+__)"', src),
})

# --- A. raw text census ---
raw_nonoverlap = {t: raw.count(t) for t in toks}
raw_overlap = {t: len(re.findall("(?=" + re.escape(t) + ")", raw)) for t in toks}
raw_offsets = {t: [m.start() for m in re.finditer("(?=" + re.escape(t) + ")", raw)] for t in toks}
put("raw_text_census", {
    "nonoverlap": raw_nonoverlap,
    "overlap": raw_overlap,
    "overlap_differs": {t: raw_overlap[t] - raw_nonoverlap[t] for t in toks if raw_overlap[t] != raw_nonoverlap[t]},
    "sum_nonoverlap_all_tokens": sum(raw_nonoverlap.values()),
    "occurrences_outside_json_string_literals": {
        t: re.sub(r'"(?:[^"\\]|\\.)*"', '""', raw).count(t) for t in toks},
})

# self-overlap adjacency: occurrences whose start distance < token length
self_overlap_adj = {}
for t in toks:
    offs = raw_offsets[t]
    d = [b - a for a, b in zip(offs, offs[1:]) if b - a < len(t)]
    if d:
        self_overlap_adj[t] = {"count": len(d), "distances": sorted(set(d))}
put("self_overlap_adjacency", self_overlap_adj)

# --- B. pairwise substring logic ---
sub = {}
for a in toks:
    for b in toks:
        if a != b:
            sub[a + "|" + b] = a in b
put("token_substring_matrix", {
    "pairs_true": [k for k, v in sub.items() if v],
    "shopping_vs_shopping_admin": {
        "__SHOPPING__ in __SHOPPING_ADMIN__": "__SHOPPING__" in "__SHOPPING_ADMIN__",
        "__SHOPPING_ADMIN__ in __SHOPPING__": "__SHOPPING_ADMIN__" in "__SHOPPING__",
    },
    "bare_stem_hits": {t: raw.count(t) for t in order},
    "other_markers": {m: raw.count(m) for m in ("__last_url__", "__page__")},
    "profile_values_contain_any_token": {
        pname: {k: [t for t in toks if t in v] for k, v in pdata["values"].items()}
        for pname, pdata in prof.items()
    },
})
# occurrences sitting inside another token's occurrence
inside = {}
for a in toks:
    hits = 0
    for b in toks:
        if a == b: continue
        for off in raw_offsets[b]:
            if a in raw[off:off + len(b)]:
                hits += 1
    inside[a] = hits
put("token_occurrences_inside_other_token_occurrences", inside)

# --- C. tasks / decoded leaves census (independent parse) ---
data = json.loads(raw)
dec = json.JSONDecoder()
assert raw.lstrip().startswith("[")
pos = raw.index("[") + 1
spans = []
n = len(raw)
while True:
    while pos < n and raw[pos] in " \t\r\n,":
        pos += 1
    if pos >= n or raw[pos] == "]":
        break
    obj, end = dec.raw_decode(raw, pos)
    spans.append((pos, end))
    pos = end
assert len(spans) == len(data), (len(spans), len(data))

def walk(o, ptr):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, ptr + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, ptr + "/" + str(i))
    elif isinstance(o, str):
        yield ptr, o

leaf_occ = {t: Counter() for t in toks}      # pointer -> occurrences
leaf_tokens = defaultdict(set)               # pointer -> token set
task_occ = {t: Counter() for t in toks}
all_leaves = 0
keys_with_token = []
string_leaf_list = []
for idx, item in enumerate(data):
    for ptr, val in walk(item, "/" + str(idx)):
        all_leaves += 1
        string_leaf_list.append((idx, ptr, val))
        for t in toks:
            c = val.count(t)
            if c:
                leaf_occ[t][ptr] = c
                leaf_tokens[ptr].add(t)
                task_occ[t][idx] += c
    # keys scan
    def keys(o):
        if isinstance(o, dict):
            for k, v in o.items():
                yield k
                yield from keys(v)
        elif isinstance(o, list):
            for v in o:
                yield from keys(v)
    for k in keys(item):
        for t in toks:
            if t in k:
                keys_with_token.append((idx, k, t))

leaf_value_by_ptr = dict((p, v) for _, p, v in string_leaf_list)
leaf_stats = {}
for t in toks:
    occ = leaf_occ[t]
    dist = Counter(occ.values())
    leaf_stats[t] = {
        "decoded_occurrences": sum(occ.values()),
        "leaves_with_token": len(occ),
        "tasks_with_token": len(task_occ[t]),
        "leaf_occurrence_distribution": dict(sorted(dist.items())),
        "leaves_with_multiple_occurrences": sum(1 for c in occ.values() if c > 1),
        "max_per_leaf": max(occ.values()) if occ else 0,
        "max_per_task": max(task_occ[t].values()) if task_occ[t] else 0,
    }
put("decoded_leaf_census", {
    "string_leaf_count": all_leaves,
    "per_token": leaf_stats,
    "sum_decoded_occurrences": sum(s["decoded_occurrences"] for s in leaf_stats.values()),
    "raw_vs_decoded_delta": {t: raw_nonoverlap[t] - leaf_stats[t]["decoded_occurrences"] for t in toks},
    "keys_containing_any_token": keys_with_token,
    "leaves_with_tokens_from_multiple_types": {
        "count": sum(1 for s in leaf_tokens.values() if len(s) > 1),
        "detail": [{"ptr": p, "tokens": sorted(s)} for p, s in leaf_tokens.items() if len(s) > 1],
    },
    "tasks_with_any_token": len({i for i, p, v in string_leaf_list if any(t in v for t in toks)}),
    "total_leaves_with_any_token": len(leaf_tokens),
    "total_leaves_with_multiple_occurrences_any_token": sum(
        1 for p, s in leaf_tokens.items() if sum(leaf_occ[t][p] for t in s) > 1),
})

# --- C2. raw per-task-span attribution (independent of JSON leaf parse) ---
span_occ = {t: Counter() for t in toks}
for i, (s, e) in enumerate(spans):
    seg = raw[s:e]
    for t in toks:
        c = seg.count(t)
        if c:
            span_occ[t][i] = c
put("raw_span_attribution", {
    "span_counts_equal_decoded": {t: dict(span_occ[t]) == dict(task_occ[t]) for t in toks},
    "tasks_with_token_spans": {t: len(span_occ[t]) for t in toks},
})

# --- C3. global offset uniqueness across token types ---
all_off = [(o, t) for t in toks for o in raw_offsets[t]]
put("offset_uniqueness", {
    "total": len(all_off),
    "duplicate_offsets_across_tokens": len(all_off) - len({o for o, _ in all_off}),
})

# --- C4. GITLAB context / task shape ---
g_tok = TOK["GITLAB"]
ctx = Counter()
for o in raw_offsets[g_tok]:
    prev = raw[o - 1] if o > 0 else "^"
    nxt = raw[o + len(g_tok)] if o + len(g_tok) < len(raw) else "$"
    ctx[(prev, nxt)] += 1
git_tasks = set(task_occ[g_tok])
git_start_tasks = {i for i, item in enumerate(data)
                   if isinstance(item.get("start_url"), str) and g_tok in item["start_url"]}
put("gitlab_context", {
    "adjacent_char_pairs": {"%s|%s" % k: v for k, v in sorted(ctx.items(), key=lambda kv: -kv[1])},
    "tasks_with_gitlab": len(git_tasks),
    "tasks_with_gitlab_in_start_url": len(git_start_tasks),
    "tasks_with_gitlab_outside_start_url": len(git_tasks - git_start_tasks),
    "outside_start_url_tasks": sorted(git_tasks - git_start_tasks),
})

# GITLAB occurrence distribution by top-level task field and must_include detail
field_counts = Counter()
must_inc = []
for ptr, c in leaf_occ[g_tok].items():
    parts = ptr.split("/")
    field_counts[parts[2] if len(parts) > 2 else "?"] += c
    if "must_include" in parts:
        must_inc.append({"task_index": int(parts[1]), "json_pointer": ptr,
                         "original": leaf_value_by_ptr[ptr]})
put("gitlab_field_distribution", dict(sorted(field_counts.items())))
put("gitlab_must_include_detail", must_inc)

# task-set overlaps between GITLAB and the other tokens
overlaps = {}
for t in toks:
    if t == g_tok: continue
    a, b = git_tasks, set(task_occ[t])
    overlaps[t] = {"gitlab_tasks": len(a), "token_tasks": len(b),
                   "intersection": len(a & b), "gitlab_only": len(a - b),
                   "token_only": len(b - a)}
put("gitlab_task_set_overlaps", overlaps)
all_task_sets = [set(v) for v in task_occ.values() if v]
put("task_set_union", {
    "sum_tasks_with_token": sum(len(s) for s in all_task_sets),
    "union_distinct_tasks": len(set().union(*all_task_sets)),
    "task_count": len(data),
})

# --- C5. provenance path_template label independent recomputation ---
def tmpl_of(ptr):
    parts = ptr.split("/")[1:]
    if len(parts) >= 2 and parts[1] == "start_url":
        return "start_url"
    if len(parts) >= 3 and parts[1] == "eval" and parts[2] == "reference_url":
        return "eval.reference_url"
    if "program_html" in parts and parts[-1] == "url":
        return "eval.program_html[].url"
    if "must_include" in parts:
        return "eval.program_html[].required_contents.must_include[]"
    if "reference_answer_raw_annotation" in parts:
        return "eval.reference_answer_raw_annotation"
    return "OTHER:" + ptr

tmpl_bad = []
for r in out["occurrence_provenance"]:
    want = tmpl_of(r["json_pointer"])
    if want != r["path_template"]:
        tmpl_bad.append({"ptr": r["json_pointer"], "instrument": r["path_template"], "derived": want})
put("provenance_path_template_recompute", {
    "total_records": len(out["occurrence_provenance"]),
    "mismatch_total": len(tmpl_bad),
    "mismatches": tmpl_bad[:10],
})

# --- D. provenance validation ---
prov = out["occurrence_provenance"]
prov_by_token = defaultdict(list)
for r in prov:
    prov_by_token[r["token"]].append(r)
prov_res = {}
for t in toks:
    recs = prov_by_token.get(t, [])
    offs = [r["original_input_codepoint_offset"] for r in recs]
    indep = raw_offsets[t]
    bad_slice = [o for o in offs if raw[o:o + len(t)] != t]
    # map offset -> task span
    def span_of(off):
        for i, (s, e) in enumerate(spans):
            if s <= off < e:
                return i
        return None
    bad_task = [r for r in recs if span_of(r["original_input_codepoint_offset"]) != r["task_index"]]
    bad_pointer_task = [r for r in recs if r["json_pointer"].split("/")[1] != str(r["task_index"])]
    # per-pointer count equality against independent leaf census
    pc = Counter(r["json_pointer"] for r in recs)
    ptr_mismatch = [
        {"ptr": p, "prov": pc.get(p, 0), "indep": leaf_occ[t].get(p, 0)}
        for p in sorted(set(pc) | set(leaf_occ[t]))
        if pc.get(p, 0) != leaf_occ[t].get(p, 0)
    ]
    # pointer must resolve to a leaf that contains token
    bad_ptr = [r["json_pointer"] for r in recs
               if not (r["json_pointer"] in leaf_value_by_ptr
                       and t in leaf_value_by_ptr[r["json_pointer"]])]
    prov_res[t] = {
        "records": len(recs),
        "independent_offsets": len(indep),
        "offset_set_equal": sorted(offs) == sorted(indep),
        "missing_offsets": sorted(set(indep) - set(offs)),
        "extra_offsets": sorted(set(offs) - set(indep)),
        "duplicate_offsets": len(offs) - len(set(offs)),
        "bad_slice": bad_slice,
        "bad_task_index": len(bad_task),
        "pointer_task_index_mismatches": len(bad_pointer_task),
        "pointer_count_mismatches": ptr_mismatch[:20],
        "pointer_count_mismatch_total": len(ptr_mismatch),
        "bad_pointer": bad_ptr[:10],
        "bad_pointer_total": len(bad_ptr),
        "path_template_counts": dict(sorted(Counter(r["path_template"] for r in recs).items())),
        "string_role_counts": dict(sorted(Counter(r["string_role"] for r in recs).items())),
    }
put("provenance_validation", prov_res)
put("provenance_total", len(prov))

# --- E. index/task_id mapping ---
mapres = {"tasks_without_task_id": 0, "task_id_ne_index": [], "output_index_ne_position": [],
          "filename_template_ok": True, "task_id_types": Counter()}
for i, item in enumerate(data):
    if "task_id" not in item:
        mapres["tasks_without_task_id"] += 1
        continue
    mapres["task_id_types"][type(item["task_id"]).__name__] += 1
    if item["task_id"] != i:
        mapres["task_id_ne_index"].append({"position": i, "task_id": item["task_id"]})
for pname, pdata in out["profiles"].items():
    for i, tr in enumerate(pdata["tasks"]):
        if tr["output_index"] != i or tr["output_filename"] != "config_files/%d.json" % i:
            mapres["filename_template_ok"] = False
            mapres["output_index_ne_position"].append({"profile": pname, "position": i,
                                                       "record": tr["output_index"],
                                                       "filename": tr["output_filename"]})
mapres["task_id_types"] = dict(mapres["task_id_types"])
put("index_mapping", mapres)

# --- F. per-profile independent projection ---
def project(text, values):
    applied = {}
    for t in order:
        tk = TOK[t]
        n = text.count(tk)
        applied[t] = n
        text = text.replace(tk, values[t])
    return text, applied

prof_res = {}
for pname, pdata in prof.items():
    values = pdata["values"]
    text, applied = project(raw, values)
    proj_data = json.loads(text)
    p_leaf = {}
    p_leaves = []
    for idx, item in enumerate(proj_data):
        for ptr, val in walk(item, "/" + str(idx)):
            p_leaf[ptr] = val
            p_leaves.append((idx, ptr, val))
    changed = {}
    changed_by_token = {t: 0 for t in toks}
    changed_tasks_by_token = {t: set() for t in toks}
    changed_category = Counter()
    changed_ptr_multi = 0
    leaf_orig = dict((p, v) for _, p, v in string_leaf_list)
    for idx, ptr, oval in string_leaf_list:
        nv = p_leaf.get(ptr)
        if nv != oval:
            changed[ptr] = (idx, oval, nv)
            tset = {t for t in toks if t in oval}
            for t in tset:
                changed_by_token[t] += 1
                changed_tasks_by_token[t].add(idx)
            if sum(oval.count(t) for t in toks) > 1:
                changed_ptr_multi += 1
            parts = ptr.split("/")
            if "must_include" in parts:
                tmpl = "eval.program_html[].required_contents.must_include[]"
            elif "reference_answer_raw_annotation" in parts:
                tmpl = "eval.reference_answer_raw_annotation"
            elif ptr.endswith("/start_url"):
                tmpl = "start_url"
            elif ptr.endswith("/reference_url"):
                tmpl = "eval.reference_url"
            elif "program_html" in parts and ptr.endswith("/url"):
                tmpl = "eval.program_html[].url"
            else:
                tmpl = "OTHER:" + ptr
            changed_category[tmpl] += 1
    prof_res[pname] = {
        "applied_replacements": applied,
        "projected_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "parsed_task_count": len(proj_data),
        "string_leaf_count": len(p_leaves),
        "changed_leaf_count": len(changed),
        "changed_task_count": len({v[0] for v in changed.values()}),
        "changed_leaves_by_token": changed_by_token,
        "changed_tasks_by_token": {t: len(s) for t, s in changed_tasks_by_token.items()},
        "changed_leaves_with_multiple_token_occurrences": changed_ptr_multi,
        "changed_leaves_by_path": dict(sorted(changed_category.items())),
        "remaining_known_tokens_text": {t: text.count(t) for t in toks},
        "remaining_known_tokens_decoded": {
            t: sum(v.count(t) for _, _, v in p_leaves) for t in toks},
        "token_then_slash_original": {t: len(re.findall(re.escape(t) + "/", raw)) for t in toks},
        "value_slash_then_raw_slash_junctions": {
            t: (len(re.findall(re.escape(values[t[2:-2]]) + "/", text))
                if values[t[2:-2]].endswith("/") else 0) for t in toks},
        "single_slash_junctions_projected": {
            t: len(re.findall(re.escape(values[t[2:-2]]) + "/", text)) for t in toks},
    }
    # projected task deep-equality + would-be file sha
    deep_bad = []
    sha_bad = []
    sha_alt_bad = 0
    inst_tasks = out["profiles"][pname]["tasks"]
    for i, tr in enumerate(inst_tasks):
        if tr["projected_task"] != proj_data[i]:
            deep_bad.append(i)
        want = hashlib.sha256(json.dumps(proj_data[i], indent=2).encode("utf-8")).hexdigest()
        if tr["would_be_file_sha256"] != want:
            sha_bad.append({"i": i, "want": want, "got": tr["would_be_file_sha256"]})
        if hashlib.sha256(json.dumps(proj_data[i], indent=2, sort_keys=True).encode()).hexdigest() != tr["would_be_file_sha256"]:
            sha_alt_bad += 1
    prof_res[pname]["projected_task_deep_mismatches"] = deep_bad
    prof_res[pname]["would_be_file_sha256_mismatches"] = sha_bad[:10]
    prof_res[pname]["would_be_file_sha256_mismatch_total"] = len(sha_bad)
    prof_res[pname]["would_be_file_sha256_also_not_sorted_keys"] = sha_alt_bad
    # instrument changed_leaves cross-check for every task
    cl_mismatch = []
    # build per-task independent changed list once
    by_task = defaultdict(list)
    for ptr, (idx, oval, nv) in changed.items():
        by_task[idx].append({"json_pointer": ptr, "original": oval, "projected": nv,
                             "tokens": sorted(t for t in toks if t in oval)})
    for i, tr in enumerate(inst_tasks):
        inst = sorted((c["json_pointer"], c["original"], c["projected"], tuple(sorted(c["tokens"])))
                      for c in tr["changed_leaves"])
        ind = sorted((c["json_pointer"], c["original"], c["projected"], tuple(c["tokens"]))
                     for c in by_task.get(i, []))
        if inst != ind:
            cl_mismatch.append({"task_index": i, "inst_only": [x for x in inst if x not in ind][:3],
                                "indep_only": [x for x in ind if x not in inst][:3]})
    prof_res[pname]["changed_leaves_per_task_mismatches"] = cl_mismatch[:10]
    prof_res[pname]["changed_leaves_per_task_mismatch_total"] = len(cl_mismatch)

put("profiles_independent", prof_res)

# --- G. compare + print ---
inst = {
    "original_occurrences_by_token": out["population"]["original_occurrences_by_token"],
    "tasks_with_token": out["population"]["tasks_with_token"],
    "occurrence_roles": out["population"]["occurrence_roles"],
    "tokens_followed_by_slash": out["population"]["tokens_followed_by_slash"],
    "profiles": {p: {**{k: v for k, v in pd.items()
                     if k in ("parsed_task_count", "string_leaf_count",
                              "changed_leaf_count", "changed_task_count", "changed_leaves_by_token",
                              "changed_tasks_by_token", "changed_leaves_with_multiple_occurrences",
                              "changed_leaves_by_category", "changed_leaves_by_path_template",
                              "projected_text_sha256", "remaining_known_tokens_text",
                              "remaining_known_tokens_decoded")},
                    "applied_replacements": {s["token"]: s["applied_replacements"] for s in pd["steps"]}}
                 for p, pd in out["profiles"].items()},
}
cmp = []
def chk(name, a, b):
    if a != b: cmp.append({"metric": name, "instrument": a, "independent": b})

chk("population.original_occurrences_by_token", inst["original_occurrences_by_token"], raw_nonoverlap)
chk("population.tasks_with_token", inst["tasks_with_token"],
    {t: leaf_stats[t]["tasks_with_token"] for t in toks})
chk("population.occurrence_roles.value", inst["occurrence_roles"]["value"], sum(raw_nonoverlap.values()))
chk("population.tokens_followed_by_slash", inst["tokens_followed_by_slash"],
    sum(len(re.findall(re.escape(t) + "/", raw)) for t in toks))
for pname, ind in prof_res.items():
    pd = inst["profiles"][pname]
    ind = dict(ind)
    ind["applied_replacements"] = {TOK[k]: v for k, v in ind["applied_replacements"].items()}
    for key in ("applied_replacements", "parsed_task_count", "string_leaf_count",
                "changed_leaf_count", "changed_task_count", "changed_leaves_by_token",
                "changed_tasks_by_token", "projected_text_sha256",
                "remaining_known_tokens_text", "remaining_known_tokens_decoded"):
        chk("profiles.%s.%s" % (pname, key), pd[key], ind[key])
    chk("profiles.%s.changed_leaves_by_category" % pname, pd["changed_leaves_by_category"],
        {"non_url_field": ind["changed_leaves_by_path"].get("eval.program_html[].required_contents.must_include[]", 0)
         + ind["changed_leaves_by_path"].get("eval.reference_answer_raw_annotation", 0),
         "url_field": ind["changed_leaf_count"] - (
             ind["changed_leaves_by_path"].get("eval.program_html[].required_contents.must_include[]", 0)
             + ind["changed_leaves_by_path"].get("eval.reference_answer_raw_annotation", 0))})
    chk("profiles.%s.changed_leaves_by_path_template" % pname,
        pd["changed_leaves_by_path_template"], ind["changed_leaves_by_path"])
    chk("profiles.%s.changed_leaves_with_multiple_occurrences" % pname,
        pd["changed_leaves_with_multiple_occurrences"],
        ind["changed_leaves_with_multiple_token_occurrences"])
    chk("profiles.%s.stimulus_observations.value_slash_then_raw_slash_junctions" % pname,
        out["profiles"][pname]["stimulus_observations"]["value_slash_then_raw_slash_junctions"],
        sum(ind["value_slash_then_raw_slash_junctions"].values()))
# source-contract facts straight from generator bytes
glines = src.splitlines()
src_facts = {
    "env_config_star_import_line": next(i for i, l in enumerate(glines, 1)
                                        if "from browser_env.env_config import *" in l),
    "parse_line": next(i for i, l in enumerate(glines, 1) if "json.loads(raw)" in l),
    "enumerate_loop_line": next(i for i, l in enumerate(glines, 1) if "enumerate(data)" in l),
    "per_task_filename_template": "config_files/{idx}.json" if 'f"config_files/{idx}.json"' in src else None,
    "replace_steps": [],
}
for i, l in enumerate(glines, 1):
    m = re.search(r'raw\s*=\s*raw\.replace\("(__[A-Z_]+__)",\s*([A-Z_]+)\)', l)
    if m:
        src_facts["replace_steps"].append({"line": i, "token": m.group(1), "name": m.group(2)})
chk("source_contract.env_config_star_import_line", out["source_contract"]["env_config_star_import_line"],
    src_facts["env_config_star_import_line"])
chk("source_contract.parse_line", out["source_contract"]["parse_line"], src_facts["parse_line"])
chk("source_contract.enumerate_loop_line", out["source_contract"]["enumerate_loop_line"],
    src_facts["enumerate_loop_line"])
chk("source_contract.per_task_filename_template", out["source_contract"]["per_task_filename_template"],
    src_facts["per_task_filename_template"])
chk("source_contract.replace_steps", out["source_contract"]["replace_steps"], src_facts["replace_steps"])
put("source_contract_independent", src_facts)

put("instrument_vs_independent", cmp)

# GITLAB focus blocks
g = TOK["GITLAB"]
put("gitlab_focus", {
    "raw_text_nonoverlap": raw_nonoverlap[g],
    "raw_text_overlap": raw_overlap[g],
    "decoded": leaf_stats[g],
    "provenance": prov_res[g],
    "provenance_task_set_equals_decoded_tasks": sorted({r["task_index"] for r in prov_by_token[g]}) == sorted(task_occ[g]),
    "profile_changed_leaves": {p: prof_res[p]["changed_leaves_by_token"][g] for p in prof_res},
    "profile_changed_tasks": {p: prof_res[p]["changed_tasks_by_token"][g] for p in prof_res},
    "profile_applied": {p: prof_res[p]["applied_replacements"]["GITLAB"] for p in prof_res},
    "gitlab_token_then_slash": {p: prof_res[p]["token_then_slash_original"][g] for p in prof_res},
    "gitlab_double_slash_junction": {p: prof_res[p]["value_slash_then_raw_slash_junctions"][g] for p in prof_res},
    "gitlab_single_slash_junction": {p: prof_res[p]["single_slash_junctions_projected"][g] for p in prof_res},
    "gitlab_leaf_counts_by_path": {p: {k: v for k, v in prof_res[p]["changed_leaves_by_path"].items()} for p in prof_res},
})

print(json.dumps(R, indent=1, sort_keys=True, default=str))

#!/usr/bin/env python3
"""Independent __WIKIPEDIA__ census + full token-census cross-check.

Derived ONLY from: prereg text semantics (six sequential global str.replace on
serialized raw text, then json parse, enumerate index), the pinned generator
bytes, the pinned raw 812-task file, the pinned profiles.json, and the
instrument's --json/--summary OUTPUT.  No production source is imported/read.
"""
import json, hashlib, sys, os

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = f"{ROOT}/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF = f"{ROOT}/plans/fixtures/r29/profiles.json"
GEN = f"{ROOT}/plans/fixtures/r29/generate_test_data.py"
INST = f"{ROOT}/.ufo/waves/round-29/scratch/falsify/FTokenWikipedia/json.out.json"

TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__", "__WIKIPEDIA__", "__MAP__"]
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOK = "__WIKIPEDIA__"

mism = []  # (location, expected_by_me, instrument)
def cmp(loc, mine, inst):
    if mine != inst:
        mism.append((loc, mine, inst))

b = open(RAW, "rb").read()
raw = b.decode("utf-8")
print("raw sha256", hashlib.sha256(b).hexdigest(), "bytes", len(b), "cp", len(raw),
      "ascii", all(c < 128 for c in b))

# ---- 1. literal raw counts -------------------------------------------------
raw_counts = {t: raw.count(t) for t in TOKENS}
print("raw literal counts:", json.dumps(raw_counts))
print("WIKIPEDIA in raw bytes:", b.count(TOK.encode()), "in decoded str:", raw.count(TOK))

# token-followed-by-slash census
fbs = 0
for t in TOKENS:
    st = 0
    o = raw.find(t)
    while o != -1:
        if raw[o + len(t):o + len(t) + 1] == "/":
            st += 1
        o = raw.find(t, o + 1)
    print(f"  {t} followed-by-slash: {st}")
    fbs += st
print("tokens_followed_by_slash total:", fbs)

# every __X__ marker
import re
mk = {}
for m in re.finditer(r"__[A-Za-z0-9_]+?__", raw):
    mk[m.group(0)] = mk.get(m.group(0), 0) + 1
print("all markers:", json.dumps(mk, sort_keys=True))

# ---- 2. parse + task slices ------------------------------------------------
data = json.loads(raw)
assert isinstance(data, list) and len(data) == 812
dec = json.JSONDecoder()
slices = []
pos = raw.index("[") + 1
while True:
    while raw[pos] in " \n\r\t,":
        pos += 1
    if raw[pos] == "]":
        break
    obj, end = dec.raw_decode(raw, pos)
    slices.append((pos, end, obj))
    pos = end
print("task slices:", len(slices), "contiguous-sum-check:", sum(e - s for s, e, _ in slices))
for i, (s, e, o) in enumerate(slices):
    if o != data[i]:
        print("SLICE PARSE MISMATCH at", i); break

def walk(o, path=(), out=None, keys=None):
    """Emit (pointer_string, value, path_tuple). Pointer is RFC6901-UNESCAPED
    (instrument style) so slash-bearing keys remain ambiguous there."""
    if out is None:
        out, keys = [], []
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(k, str):
                for t in TOKENS:
                    if t in k:
                        keys.append((("/" + "/".join(map(str, path + (k,)))), t, k.count(t)))
            walk(v, path + (k,), out, keys)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + (i,), out, keys)
    elif isinstance(o, str):
        out.append(("/" + "/".join(map(str, path)), o, path))
    return out, keys

def resolve(root, path):
    node = root
    for p in path:
        node = node[p]
    return node

def leaf_token_counts(s):
    return {t: s.count(t) for t in TOKENS if t in s}

# decoded leaf census (whole doc)
leaves, keyhits = walk(data)
print("decoded string leaves:", len(leaves), "dict-key token hits:", len(keyhits))
leaf_by_ptr = {p: v for p, v, _ in leaves}
dec_counts = {t: sum(v.count(t) for _, v, _ in leaves) for t in TOKENS}
print("decoded leaf occurrence counts:", json.dumps(dec_counts))
print("decoded leaves carrying WIKIPEDIA:", sum(1 for _, v, _ in leaves if TOK in v))

# per task decoded token counts / presence
task_pres = {t: 0 for t in TOKENS}
task_occ = {t: 0 for t in TOKENS}
task_token_sets = []
for i, (s, e, o) in enumerate(slices):
    lv, _ = walk(o)
    counts = {t: sum(x.count(t) for _, x, _ in lv) for t in TOKENS}
    for t in TOKENS:
        task_occ[t] += counts[t]
        if counts[t]:
            task_pres[t] += 1
    task_token_sets.append({t: counts[t] for t in TOKENS if counts[t]})
print("tasks carrying token (decoded):", json.dumps(task_pres))
print("per-task occurrence sum:", json.dumps(task_occ))
print("WIKIPEDIA tasks:", task_pres[TOK], "leaf hits:", dec_counts[TOK])

# raw-slice per-task occurrence counts must equal decoded per-task counts
rawslice_task_counts = []
for i, (s, e, o) in enumerate(slices):
    sl = raw[s:e]
    rawslice_task_counts.append({t: sl.count(t) for t in TOKENS})
norm = [{k: v for k, v in d.items() if v} for d in rawslice_task_counts]
diff = [(i, a, b2) for i, (a, b2) in enumerate(zip(task_token_sets, norm)) if a != b2]
print("decoded-vs-rawslice per-task token-count diffs:", len(diff), diff[:3])

# ---- 3. occurrence provenance check ---------------------------------------
inst = json.load(open(INST))
prov = inst["occurrence_provenance"]
print("instrument occurrence_provenance entries:", len(prov))
my_occ = []
for i, (s, e, o) in enumerate(slices):
    lv, _ = walk(o)
    sl = raw[s:e]
    for t in TOKENS:
        st = 0
        while True:
            k = sl.find(t, st)
            if k == -1:
                break
            my_occ.append((s + k, t, i))
            st = k + 1
my_occ.sort()
print("my raw occurrence tuples:", len(my_occ))
# instrument offsets sorted?
io = [(p["original_input_codepoint_offset"], p["token"], p["task_index"]) for p in prov]
print("instrument offsets sorted:", io == sorted(io), "unique offsets:", len({x[0] for x in io}))
cmp("occurrence tuple multiset", sorted(my_occ), sorted(io))
if sorted(my_occ) != sorted(io):
    a, bb = sorted(my_occ), sorted(io)
    print("first 5 mine-not-inst:", [x for x in a if x not in set(bb)][:5])
    print("first 5 inst-not-mine:", [x for x in bb if x not in set(a)][:5])
# prove offsets are raw-text coordinates
bad = [(p["original_input_codepoint_offset"], p["token"]) for p in prov
       if raw[p["original_input_codepoint_offset"]:p["original_input_codepoint_offset"] + len(p["token"])] != p["token"]]
print("provenance offsets whose raw text != token:", len(bad), bad[:3])
# json_pointer correctness: leaf at pointer contains token and occurrence rank matches
ptr_bad = []
from collections import Counter
per_leaf_rank = Counter()
for p in sorted(prov, key=lambda x: (x["task_index"], x["json_pointer"], x["original_input_codepoint_offset"])):
    ti, ptr = p["task_index"], p["json_pointer"]
    try:
        node = leaf_by_ptr[ptr]
    except Exception:
        ptr_bad.append(("unresolvable", ti, ptr)); continue
    if not isinstance(node, str) or p["token"] not in node:
        ptr_bad.append(("leaf-lacks-token", ti, ptr, p["token"], type(node).__name__))
    hit = sum(1 for x in prov if x["task_index"] == ti and x["json_pointer"] == ptr and x["token"] == p["token"])
    if node.count(p["token"]) != hit and isinstance(node, str):
        ptr_bad.append(("count-vs-provenance", ti, ptr, p["token"], node.count(p["token"]), hit))
print("json_pointer problems:", len(ptr_bad), ptr_bad[:5])
# path_template + string_role sanity
print("roles:", Counter(p["string_role"] for p in prov))

# ---- 4. cross-check instrument population --------------------------------
pop = inst["population"]
cmp("population.original_occurrences_by_token", raw_counts, pop["original_occurrences_by_token"])
cmp("population.tasks_with_token", task_pres, pop["tasks_with_token"])
cmp("population.tasks_with_any_token", 812, pop["tasks_with_any_token"])
cmp("population.input_task_count", 812, pop["input_task_count"])
cmp("population.other_double_underscore_markers",
    {k: v for k, v in mk.items() if k not in TOKENS}, pop["other_double_underscore_markers"])
cmp("population.tokens_followed_by_slash", fbs, pop["tokens_followed_by_slash"])
cmp("population.occurrence_roles", {"value": len(my_occ)}, pop["occurrence_roles"])

# ---- 5. sites metadata attack --------------------------------------------
site_sets = {}
for i, (s, e, o) in enumerate(slices):
    site_sets[i] = o.get("sites")
wiki_sites = [i for i, ss in site_sets.items() if isinstance(ss, list) and "wikipedia" in ss]
print("\ntasks with 'wikipedia' in sites:", len(wiki_sites), wiki_sites)
wiki_tok = [i for i in range(812) if task_token_sets[i].get(TOK)]
print("tasks with __WIKIPEDIA__ token:", wiki_tok)
print("intersection:", sorted(set(wiki_sites) & set(wiki_tok)))
print("wikipedia-site tasks that carry any token:", sum(1 for i in wiki_sites if task_token_sets[i]))
for i in wiki_sites:
    urls = []
    for p, sv, _pp in walk(slices[i][2])[0]:
        if sv in TOKENS or any(t in sv for t in TOKENS):
            urls.append((p, sv))
    print(f"  task {i} sites={site_sets[i]} token-counts={task_token_sets[i]} token-leaves={[(p,v) for p,v in urls]}")
# site census vs token census (shows whether counting is site-derived)
from collections import Counter
site_census = Counter()
for ss in site_sets.values():
    for sname in (ss if isinstance(ss, list) else []):
        site_census[sname] += 1
print("site-name task census:", dict(site_census))
print("token task census:    ", task_pres)

# ---- 6. per-profile independent projection -------------------------------
profiles = json.load(open(PROF))
print("\nprofiles:", list(profiles.keys()))
URLISH = lambda s: s.startswith(("http://", "https://")) or "://" in s
def path_template_path(path):
    parts = list(path)[1:]
    out = ""
    for p in parts:
        if isinstance(p, int):
            out += "[]"
        else:
            out += ("." if out else "") + str(p)
    return out

def classify(path, val):
    pt = path_template_path(path)
    if pt in ("start_url", "eval.reference_url") or pt.endswith(".url") or pt.endswith("must_include[]"):
        if "must_include" in pt:
            return "non_url_field"
        return "url_field"
    if URLISH(val) and (val.startswith("http://__") or val.startswith("https://__")):
        return "url_field"
    return "non_url_field"

def project(values):
    text = raw
    applied = {}
    step_counts = []
    for name in ORDER:
        t = f"__{name}__"
        n = text.count(t)
        step_counts.append((name, t, n))
        applied[name] = n
        text = text.replace(t, values[name])
    return text, applied, step_counts

def census_projection(text):
    d = json.loads(text)
    changed = []
    for ptr, sv, path in walk(d)[0]:
        node = resolve(data, path)
        if node != sv:
            changed.append({"task_index": int(path[0]),
                            "json_pointer": ptr,
                            "path_template": path_template_path(path),
                            "original": node, "projected": sv,
                            "tokens": sorted(leaf_token_counts(node).keys()),
                            "category": classify(path, sv)})
    return d, changed

results = {}
for pname, pobj in profiles.items():
    values = pobj["values"]
    for k in ORDER:
        if k not in values:
            print("PROFILE MISSING KEY", pname, k)
    text, applied, step_counts = project(values)
    d, changed = census_projection(text)
    sha = hashlib.sha256(text.encode()).hexdigest()
    # aggregates
    by_tok_leaf = {t: 0 for t in TOKENS}
    by_tok_task = {t: set() for t in TOKENS}
    for c in changed:
        for t in c["tokens"]:
            by_tok_leaf[t] += 1
            by_tok_task[t].add(c["task_index"])
    cats = Counter(c["category"] for c in changed)
    tmpl = Counter(c["path_template"] for c in changed)
    multi = sum(1 for c in changed if sum(leaf_token_counts(c["original"]).values()) > 1)
    rem_text = {t: text.count(t) for t in TOKENS}
    rem_dec = {t: sum(v.count(t) for _, v, _ in walk(d)[0]) for t in TOKENS}
    # per-task objects
    per_task = []
    for ti, item in enumerate(d):
        blob = json.dumps(item, indent=2)
        per_task.append({"index": ti, "task_id": item.get("task_id"),
                         "index_equals_task_id": item.get("task_id") == ti,
                         "filename": f"config_files/{ti}.json",
                         "sha": hashlib.sha256(blob.encode()).hexdigest()})
    results[pname] = dict(text=text, applied=applied, steps=step_counts, d=d, changed=changed,
                          sha=sha, by_tok_leaf=by_tok_leaf,
                          by_tok_task={t: len(v) for t, v in by_tok_task.items()},
                          cats=dict(cats), tmpl=dict(tmpl), multi=multi,
                          rem_text=rem_text, rem_dec=rem_dec, per_task=per_task)
    print(f"\n=== {pname} ===")
    print(" applied:", json.dumps(applied))
    print(" steps:", step_counts)
    print(" WIKIPEDIA applied:", applied["WIKIPEDIA"], "changed leaves w/ WIKI token:",
          sum(1 for c in changed if TOK in c["original"]),
          "projected text contains WIKI token:", text.count(TOK),
          "projected contains 'wikipedia.invalid':", text.count("wikipedia.invalid"))
    print(" parsed tasks:", len(d), "sha256:", sha)
    print(" changed leaves:", len(changed), "changed tasks:", len({c['task_index'] for c in changed}),
          "multi-occ leaves:", multi)
    print(" by token leaves:", json.dumps(by_tok_leaf))
    print(" by token tasks :", json.dumps(results[pname]["by_tok_task"]))
    print(" categories:", json.dumps(dict(cats)))
    print(" templates:", json.dumps(dict(tmpl)))
    print(" remaining text:", json.dumps(rem_text), "decoded:", json.dumps(rem_dec))
    # cross-check vs instrument profile output
    ip = inst["profiles"][pname]
    cmp(f"profiles.{pname}.steps", [{"applied_replacements": n, "name": nm, "token": t} for nm, t, n in step_counts],
        ip["steps"])
    cmp(f"profiles.{pname}.changed_leaf_count", len(changed), ip["changed_leaf_count"])
    cmp(f"profiles.{pname}.changed_task_count", len({c['task_index'] for c in changed}), ip["changed_task_count"])
    cmp(f"profiles.{pname}.changed_leaves_with_multiple_occurrences", multi, ip["changed_leaves_with_multiple_occurrences"])
    cmp(f"profiles.{pname}.changed_leaves_by_token", by_tok_leaf, ip["changed_leaves_by_token"])
    cmp(f"profiles.{pname}.changed_tasks_by_token", results[pname]["by_tok_task"], ip["changed_tasks_by_token"])
    cmp(f"profiles.{pname}.changed_leaves_by_category", dict(cats), ip["changed_leaves_by_category"])
    cmp(f"profiles.{pname}.changed_leaves_by_path_template", dict(tmpl), ip["changed_leaves_by_path_template"])
    cmp(f"profiles.{pname}.remaining_known_tokens_text", rem_text, ip["remaining_known_tokens_text"])
    cmp(f"profiles.{pname}.remaining_known_tokens_decoded", rem_dec, ip["remaining_known_tokens_decoded"])
    cmp(f"profiles.{pname}.projected_text_sha256", sha, ip["projected_text_sha256"])
    cmp(f"profiles.{pname}.string_leaf_count", len(walk(d)[0]), ip["string_leaf_count"])
    cmp(f"profiles.{pname}.parsed_task_count", len(d), ip["parsed_task_count"])
    cmp(f"profiles.{pname}.values", values, ip["values"])
    cat_dis = [(c["path_template"], c["category"]) for c in changed]
    inst_cat = {}
    for it in ip["tasks"]:
        for c in it["changed_leaves"]:
            inst_cat.setdefault(c["path_template"], set()).add(c["category"])
    cat_label_diff = sorted({(c["path_template"], c["category"], tuple(sorted(inst_cat.get(c["path_template"], ())))) for c in changed
                             if c["category"] not in inst_cat.get(c["path_template"], set())})
    print(" category label disagreements (mine template,path->):", len(cat_label_diff), cat_label_diff[:3])
    # per-task compare
    pt_bad = []
    for ti, ip_task in enumerate(ip["tasks"]):
        mine = per_task[ti]
        if (ip_task["output_index"] != mine["index"]
                or ip_task["output_filename"] != mine["filename"]
                or ip_task["task_id"] != mine["task_id"]
                or ip_task["would_be_file_sha256"] != mine["sha"]
                or ip_task["index_equals_task_id"] != mine["index_equals_task_id"]
                or ip_task["projected_task"] != d[ti]):
            pt_bad.append(ti)
        if mine["task_id"] != mine["index"]:
            pass
    print(" per-task mismatches vs instrument:", len(pt_bad), pt_bad[:5])
    if pt_bad:
        mism.append((f"profiles.{pname}.tasks[first]", pt_bad[:5], "instrument differs"))
    # per-task changed_leaves compare
    cl_bad = []
    for ti, ip_task in enumerate(ip["tasks"]):
        mine_cl = [{k: c[k] for k in ("json_pointer", "original", "path_template", "projected")}
                   for c in changed if c["task_index"] == ti]
        inst_cl = [{k: c[k] for k in ("json_pointer", "original", "path_template", "projected")}
                   for c in ip_task["changed_leaves"]]
        mine_tok = {c["json_pointer"]: c["tokens"] for c in changed if c["task_index"] == ti}
        inst_tok = {c["json_pointer"]: sorted(c["tokens"]) for c in ip_task["changed_leaves"]}
        if mine_cl != inst_cl or mine_tok != inst_tok:
            cl_bad.append(ti)
    print(" per-task changed_leaves mismatches:", len(cl_bad), cl_bad[:5])
    if cl_bad:
        mism.append((f"profiles.{pname}.tasks[*].changed_leaves", cl_bad[:5], "instrument differs"))
    # wikipedia-site tasks: instrument tokens must never include WIKIPEDIA
    wiki_bad = []
    for ti in wiki_sites:
        it = ip["tasks"][ti]
        blob = json.dumps(it)
        if TOK in blob or "wikipedia.invalid" in blob:
            wiki_bad.append(ti)
        for c in it["changed_leaves"]:
            if TOK in json.dumps(c):
                wiki_bad.append(("leaf", ti, c["json_pointer"]))
    print(" wikipedia-site tasks whose instrument record mentions WIKI token/value:", len(wiki_bad), wiki_bad[:5])
    if wiki_bad:
        mism.append((f"profiles.{pname}.wiki-site-tasks", wiki_bad[:5], "instrument leaks token"))

# ---- 7. instrument index mapping ----------------------------------------
im = inst["index_mapping"]
ids = [o.get("task_id") for _, _, o in slices]
cmp("index_mapping.index_equals_task_id", sum(1 for i, t in enumerate(ids) if i == t), im["index_equals_task_id"])
cmp("index_mapping.violations", [(i, t) for i, t in enumerate(ids) if i != t], im["violations"])
print("\nindex==task_id count:", sum(1 for i, t in enumerate(ids) if i == t), "of", len(ids))

# ---- 8. mismatches ------------------------------------------------------
print("\n================= MISMATCHES =================")
if not mism:
    print("NONE")
for loc, mine, instv in mism:
    print("LOC:", loc)
    print("  mine:", json.dumps(mine)[:800])
    print("  inst:", json.dumps(instv)[:800])

# ---- 9. summary-string cross-check --------------------------------------
inst_cli_summary = f"{ROOT}/.ufo/waves/round-29/scratch/falsify/FTokenWikipedia/summary.txt"
print("\n--- summary file token lines ---")
for line in open(inst_cli_summary):
    if "WIKIPEDIA" in line or "TOKEN" in line or "applied_replacements" in line:
        print(line.rstrip())

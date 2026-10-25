"""Independent re-derivation of C1 required metrics from prereg text + pinned bytes.

Does NOT read or import plans/config_projection.py. Compares against its --json output file.
"""
import hashlib
import json
import sys
from collections import Counter

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = f"{ROOT}/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF = f"{ROOT}/plans/fixtures/r29/profiles.json"
OUT = sys.argv[1]

ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOK = {n: f"__{n}__" for n in ORDER}
URL_KEYS = {"start_url", "url", "reference_url"}

raw_bytes = open(RAW, "rb").read()
raw = raw_bytes.decode("utf-8")
profiles = json.load(open(PROF))
out = json.load(open(OUT))
mism = []


def chk(label, mine, theirs):
    if mine != theirs:
        mism.append((label, mine if len(repr(mine)) < 300 else repr(mine)[:300],
                     theirs if len(repr(theirs)) < 300 else repr(theirs)[:300]))


def esc(k):
    return str(k).replace("~", "~0").replace("/", "~1")


def leaves(o, ptr=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, f"{ptr}/{esc(k)}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, f"{ptr}/{i}")
    else:
        yield ptr, o


def keys(o):
    if isinstance(o, dict):
        for k, v in o.items():
            yield k
            yield from keys(v)
    elif isinstance(o, list):
        for v in o:
            yield from keys(v)


orig = json.loads(raw)
chk("raw_text_sha256", hashlib.sha256(raw_bytes).hexdigest(), out["raw_text_sha256"])
pop = out["population"]
chk("input_task_count", len(orig), pop["input_task_count"])
chk("distinct_task_ids", len({t["task_id"] for t in orig}), pop["distinct_task_ids"])
chk("profile_count", len(profiles), pop["profile_count"])
chk("task_profile_projections", len(orig) * len(profiles), pop["task_profile_projections"])
occ = {TOK[n]: raw.count(TOK[n]) for n in ORDER}
chk("original_occurrences_by_token", occ, pop["original_occurrences_by_token"])
twt = {TOK[n]: sum(1 for t in orig if TOK[n] in json.dumps(t)) for n in ORDER}
chk("tasks_with_token", twt, pop["tasks_with_token"])
chk("tasks_with_any_token", sum(1 for t in orig if any(TOK[n] in json.dumps(t) for n in ORDER)),
    pop["tasks_with_any_token"])
key_tokens = sum(1 for k in keys(orig) for n in ORDER if TOK[n] in k)
print("tokens inside JSON object keys:", key_tokens)
idx_eq = sum(1 for i, t in enumerate(orig) if t["task_id"] == i)
chk("index_equals_task_id", idx_eq, out["index_mapping"]["index_equals_task_id"])

# occurrence provenance: all codepoint offsets of every token in raw text
mine_offsets = set()
for n in ORDER:
    t = TOK[n]
    i = raw.find(t)
    while i >= 0:
        mine_offsets.add((i, t))
        i = raw.find(t, i + 1)
prov = out["occurrence_provenance"]
theirs_offsets = {(p["original_input_codepoint_offset"], p["token"]) for p in prov}
chk("occurrence_provenance offsets set", sorted(mine_offsets), sorted(theirs_offsets))
chk("occurrence_provenance count", len(mine_offsets), len(prov))
bad_ptr = 0
olookup = {}
for ti, t in enumerate(orig):
    for p, v in leaves(t, f"/{ti}"):
        olookup[p] = v
for p in prov:
    v = olookup.get(p["json_pointer"])
    if not (isinstance(v, str) and p["token"] in v):
        bad_ptr += 1
    if p["task_index"] != int(p["json_pointer"].split("/")[1]):
        bad_ptr += 1
print("provenance pointer mismatches:", bad_ptr)
# byte vs codepoint distinction observable?
print("raw is ascii:", raw_bytes.isascii(), "len bytes", len(raw_bytes), "len cp", len(raw))

str_leaf_count = sum(1 for t in orig for _, v in leaves(t) if isinstance(v, str))

for pname, pdef in profiles.items():
    vals = pdef["values"]
    text = raw
    steps = []
    for n in ORDER:
        c = text.count(TOK[n])
        text = text.replace(TOK[n], vals[n])
        steps.append({"applied_replacements": c, "name": n, "token": TOK[n]})
    P = out["profiles"][pname]
    chk(f"{pname}.steps", steps, P["steps"])
    chk(f"{pname}.projected_text_sha256", hashlib.sha256(text.encode("utf-8")).hexdigest(),
        P["projected_text_sha256"])
    proj = json.loads(text)
    chk(f"{pname}.parsed_task_count", len(proj), P["parsed_task_count"])
    chk(f"{pname}.string_leaf_count", str_leaf_count, P["string_leaf_count"])
    chk(f"{pname}.remaining_text", {TOK[n]: text.count(TOK[n]) for n in sorted(ORDER)} and
        {TOK[n]: text.count(TOK[n]) for n in ORDER}, {k: v for k, v in P["remaining_known_tokens_text"].items()})
    changed = []
    by_cat, by_tmpl, by_tok, tasks_by_tok = Counter(), Counter(), Counter(), {TOK[n]: set() for n in ORDER}
    multi = 0
    changed_tasks = set()
    per_task = []
    for i, (a, b) in enumerate(zip(orig, proj)):
        la = dict(leaves(a, f"/{i}"))
        lb = dict(leaves(b, f"/{i}"))
        assert la.keys() == lb.keys()
        cl = []
        for p, va in la.items():
            vb = lb[p]
            if va != vb:
                last = p.rsplit("/", 1)[1]
                # template: replace numeric segments with []
                segs = p.split("/")[2:]
                tmpl = ""
                for s in segs:
                    tmpl += "[]" if s.isdigit() else ("." if tmpl else "") + s
                toks = [TOK[n] for n in ORDER if TOK[n] in va]
                cat = "url_field" if last in URL_KEYS else "non_url_field"
                cl.append({"category": cat, "json_pointer": p, "original": va,
                           "path_template": tmpl, "projected": vb, "tokens": toks})
                by_cat[cat] += 1
                by_tmpl[tmpl] += 1
                for tk in toks:
                    by_tok[tk] += 1
                    tasks_by_tok[tk].add(i)
                if sum(va.count(TOK[n]) for n in ORDER) > 1:
                    multi += 1
                changed_tasks.add(i)
        per_task.append(cl)
    chk(f"{pname}.changed_leaf_count", sum(by_cat.values()), P["changed_leaf_count"])
    chk(f"{pname}.by_category", dict(by_cat), P["changed_leaves_by_category"])
    chk(f"{pname}.by_template", dict(by_tmpl), P["changed_leaves_by_path_template"])
    chk(f"{pname}.by_token", {TOK[n]: by_tok[TOK[n]] for n in ORDER}, P["changed_leaves_by_token"])
    chk(f"{pname}.tasks_by_token", {TOK[n]: len(tasks_by_tok[TOK[n]]) for n in ORDER}, P["changed_tasks_by_token"])
    chk(f"{pname}.changed_task_count", len(changed_tasks), P["changed_task_count"])
    chk(f"{pname}.multi", multi, P["changed_leaves_with_multiple_occurrences"])
    junc = sum(text_count for text_count in [raw.count(TOK[n] + "/") for n in ORDER]) if vals["GITLAB"].endswith("/") else 0
    chk(f"{pname}.junctions", junc, P["stimulus_observations"]["value_slash_then_raw_slash_junctions"])
    task_mism = 0
    for i, rec in enumerate(P["tasks"]):
        exp = {"task_id": orig[i]["task_id"], "output_index": i, "output_filename": f"config_files/{i}.json",
               "index_equals_task_id": orig[i]["task_id"] == i,
               "would_be_file_sha256": hashlib.sha256(json.dumps(proj[i], indent=2).encode()).hexdigest(),
               "projected_task": proj[i], "changed_leaves": per_task[i]}
        for k, v in exp.items():
            if rec.get(k) != v:
                task_mism += 1
                if task_mism <= 5:
                    mism.append((f"{pname}.tasks[{i}].{k}", repr(v)[:200], repr(rec.get(k))[:200]))
        # key order preserved?
        if list(rec["projected_task"]) != list(proj[i]):
            task_mism += 1
    print(pname, "per-task record mismatches:", task_mism, "of", len(P["tasks"]))
    # non-url changed leaves listing
    nu = [(c["json_pointer"], c["original"][:90]) for cl in per_task for c in cl if c["category"] == "non_url_field"]
    if pname == "distinct_origins":
        print("non_url changed examples:", nu[:4], "... total", len(nu))
        urlish = sum(1 for _, o in nu if o.startswith("__"))
        print("non_url changed leaves whose original value starts with a token (URL-shaped):", urlish)

print("MISMATCHES:", len(mism))
for m in mism:
    print(" ", m)

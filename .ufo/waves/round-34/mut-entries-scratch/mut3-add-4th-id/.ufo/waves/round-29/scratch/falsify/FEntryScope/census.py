"""Independent census for FEntryScope. Derived from generator lines 11-23 and pinned bytes only;
does not read or import plans/config_projection.py."""
import collections
import hashlib
import itertools
import json
import re
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/"
RAW_PATH = ROOT + "plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF_PATH = ROOT + "plans/fixtures/r29/profiles.json"
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOK = {n: f"__{n}__" for n in ORDER}

raw_b = open(RAW_PATH, "rb").read()
print("raw_sha256", hashlib.sha256(raw_b).hexdigest(), "bytes", len(raw_b),
      "ascii", all(b < 128 for b in raw_b), "has_CR", b"\r" in raw_b)
raw = raw_b.decode("utf-8")
profiles = json.load(open(PROF_PATH))


def generate(text, values, order=ORDER):
    for n in order:
        text = text.replace(TOK[n], values[n])
    return text


def leaves(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from leaves(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for v in obj:
            yield from leaves(v, path + "[]")
    elif isinstance(obj, str):
        yield path, obj


data = json.loads(raw)
print("tasks", len(data), "distinct_ids", len({t["task_id"] for t in data}))
print("index_eq_task_id", sum(i == t["task_id"] for i, t in enumerate(data)))

# occurrences / tasks per token (decoded per task + serialized text)
occ = {n: raw.count(TOK[n]) for n in ORDER}
print("occ_text", occ, "sum", sum(occ.values()))
tasks_by = {}
for n in ORDER:
    tasks_by[n] = sum(1 for t in data if TOK[n] in json.dumps(t))
print("tasks_by_token", tasks_by, "sum", sum(tasks_by.values()),
      "any", sum(1 for t in data if any(TOK[n] in json.dumps(t) for n in ORDER)))

# role of each occurrence: inside key string / value string / structural
str_re = re.compile(r'"(?:[^"\\]|\\.)*"')
roles = collections.Counter()
for m in str_re.finditer(raw):
    s = m.group(0)
    after = raw[m.end():m.end() + 50].lstrip()
    role = "key" if after.startswith(":") else "value"
    for n in ORDER:
        roles[(role, n)] += s.count(TOK[n])
outside = raw
for m in str_re.finditer(raw):
    pass
struct_text = str_re.sub('""', raw)
print("roles", dict(roles), "in_structural_text", sum(struct_text.count(TOK[n]) for n in ORDER))

# other __x__ markers (occurrences and tasks)
mk = collections.Counter(re.findall(r"__[A-Za-z0-9_]+?__", raw))
print("all___markers_occ", dict(mk))
for k in mk:
    if k not in TOK.values():
        print("  marker", k, "occ", mk[k], "tasks", sum(1 for t in data if k in json.dumps(t)))

# chars adjacent to tokens in raw
pre, post = collections.Counter(), collections.Counter()
for n in ORDER:
    for m in re.finditer(re.escape(TOK[n]), raw):
        pre[raw[m.start() - 1]] += 1
        post[raw[m.end()]] += 1
print("pre_chars", dict(pre), "post_chars", dict(post))

# wikipedia population context
wiki_sites = [t for t in data if "wikipedia" in t.get("sites", [])]
print("tasks_with_sites_wikipedia", len(wiki_sites),
      "their_start_url_tokens", collections.Counter(re.match(r"(__\w+?__)?", t["start_url"]).group(1) for t in wiki_sites))
print("raw_lower_wikipedia_mentions", raw.lower().count("wikipedia"),
      "wiki_in_string_values_not_sites",
      sum(1 for t in data for p, v in leaves(t) if "wikipedia" in v.lower() and not p.startswith("sites")))

# per-profile projection
results = {}
for pname, p in profiles.items():
    vals = p["values"]
    out = generate(raw, vals)
    proj = json.loads(out)
    changed = []
    for t0, t1 in zip(data, proj):
        l0, l1 = list(leaves(t0)), list(leaves(t1))
        assert [a for a, _ in l0] == [a for a, _ in l1]
        for (pa, v0), (_, v1) in zip(l0, l1):
            if v0 != v1:
                changed.append((t0["task_id"], pa, v0, v1))
    cats = collections.Counter(pa for _, pa, _, _ in changed)
    multi = sum(1 for _, _, v0, _ in changed if sum(v0.count(TOK[n]) for n in ORDER) > 1)
    junction = sum(out_count for out_count in [0])
    # '//' junctions: value ends with '/' and raw next char '/'
    junc = 0
    for n in ORDER:
        if vals[n].endswith("/"):
            junc += len(re.findall(re.escape(TOK[n]) + "/", raw))
    perms_identical = all(generate(raw, vals, list(o)) == out for o in itertools.permutations(ORDER))
    results[pname] = dict(
        parsed=len(proj), string_leaves=sum(1 for t in data for _ in leaves(t)),
        changed=len(changed), changed_tasks=len({c[0] for c in changed}), multi=multi,
        cats=dict(cats), remaining_text=sum(out.count(TOK[n]) for n in ORDER),
        slash_junctions=junc, all_720_orders_identical=perms_identical,
        sha=hashlib.sha256(out.encode()).hexdigest())
    print("PROFILE", pname, json.dumps(results[pname], sort_keys=True))
    if pname == "distinct_origins":
        nonurl = [c for c in changed if "must_include" in c[1] or "annotation" in c[1]]
        print("nonurl_changed", len(nonurl))
        for c in nonurl[:6]:
            print("  ", c[0], c[1], repr(c[2][:90]))
        eval_types = collections.Counter()
        for c in nonurl:
            t = data[c[0]]
            eval_types[tuple(t["eval"]["eval_types"])] += 1
        print("nonurl_changed_eval_types", dict(eval_types))
        ref_must = sum(1 for c in changed if c[1].startswith("eval.reference_answers"))
        print("changed_under_eval.reference_answers", ref_must)

keys = ["parsed", "string_leaves", "changed", "changed_tasks", "multi", "cats", "remaining_text",
        "slash_junctions"]
for k in keys:
    vals_k = {p: json.dumps(results[p][k], sort_keys=True) for p in results}
    print("per_profile_identical", k, len(set(vals_k.values())) == 1, vals_k if len(set(vals_k.values())) > 1 else "")

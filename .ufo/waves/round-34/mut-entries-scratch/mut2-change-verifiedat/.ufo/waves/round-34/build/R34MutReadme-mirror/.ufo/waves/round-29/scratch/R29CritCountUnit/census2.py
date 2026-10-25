"""Second read-only census: order permutations, URL-only witness power, sites vs tokens,
multi-occurrence leaves, escapes near tokens, offset frames. No upstream code imported."""
import hashlib, itertools, json, re
from collections import Counter

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/"
t = open(ROOT + "plans/fixtures/r28/webarena/config_files/test.raw.json", "rb").read().decode("utf-8")
profiles = json.loads(open(ROOT + "plans/fixtures/r29/profiles.json", "rb").read())
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
tok = {k: f"__{k}__" for k in ORDER}


def project(text, vals, order):
    for k in order:
        text = text.replace(tok[k], vals[k])
    return text


for pname, p in profiles.items():
    vals = p["values"]
    ref = hashlib.sha256(project(t, vals, ORDER).encode()).hexdigest()
    perms = list(itertools.permutations(ORDER))
    differ = sum(1 for o in perms if hashlib.sha256(project(t, vals, o).encode()).hexdigest() != ref)
    drop_wiki = hashlib.sha256(project(t, vals, [k for k in ORDER if k != "WIKIPEDIA"]).encode()).hexdigest() == ref
    print(pname, "permutations", len(perms), "differing_from_upstream_order", differ,
          "omit_WIKIPEDIA_step_identical", drop_wiki)

data = json.loads(t)
# URL-only witness: substitute only leaves whose key name contains 'url'
URLKEY = re.compile(r"url", re.I)


def walk(x, key, path, out):
    if isinstance(x, dict):
        for k, v in x.items():
            walk(v, k, path + "/" + k, out)
    elif isinstance(x, list):
        for v in x:
            walk(v, key, path + "/[]", out)
    elif isinstance(x, str):
        out.append((path, key, x))


leaves = []
per_task = []
for ti, d in enumerate(data):
    o = []
    walk(d, "", "", o)
    per_task.append(o)
    leaves += [(ti,) + l for l in o]
hit = [l for l in leaves if any(tok[k] in l[3] for k in ORDER)]
nonurlkey = [l for l in hit if not URLKEY.search(l[2])]
print("token_leaves", len(hit), "token_leaves_under_non_url_keyname", len(nonurlkey),
      "tasks_affected_by_url_keyname_only_witness", len({l[0] for l in nonurlkey}))
print("non_url_key_paths", Counter(l[1] for l in nonurlkey))
for l in nonurlkey[:6]:
    print("  sample", l[0], l[1], repr(l[3][:120]))
# leaf value is not a single URL (contains whitespace or does not start with token)
nonsingle = [l for l in hit if re.search(r"\s", l[3]) or not l[3].startswith("__")]
print("token_leaves_not_single_url_shaped", len(nonsingle), Counter(l[1] for l in nonsingle))
multi = [l for l in hit if sum(l[3].count(tok[k]) for k in ORDER) > 1]
print("multi_occurrence_leaves", len(multi), "extra_occurrences", sum(sum(l[3].count(tok[k]) for k in ORDER) - 1 for l in multi))
print("multi_paths", Counter(l[1] for l in multi))
print("  sample_multi", repr(multi[0][3][:160]) if multi else None)
# sites vs tokens (site names are values; profile keys are token names)
site_c = Counter()
site_vs_tok = Counter()
for ti, d in enumerate(data):
    sites = tuple(sorted(d.get("sites", [])))
    for s in sites:
        site_c[s] += 1
    toks = tuple(sorted(k for k in ORDER if tok[k] in json.dumps(d)))
    site_vs_tok[(sites, toks)] += 1
print("site_value_task_counts", dict(site_c))
mism = {k: v for k, v in site_vs_tok.items() if tuple(sorted(s.upper() for s in k[0])) != k[1]}
print("site_set_vs_token_set_mismatches", mism)
# wikipedia tasks: what tokens/urls
wiki = [d for d in data if "wikipedia" in d.get("sites", [])]
print("wikipedia_site_tasks", len(wiki), "their_start_url_prefix", Counter(d["start_url"].split("/")[0] for d in wiki))
print("raw_lowercase_wikipedia_mentions", t.lower().count("wikipedia"), "literal_WIKIPEDIA_upper", t.count("WIKIPEDIA"))
# escapes inside token-bearing leaves: serialized vs decoded offset frames
esc_leaves = 0
for ti, d in enumerate(data):
    pass
# scan serialized string literals containing a token and a backslash before the token
lit = re.compile(r'"((?:[^"\\]|\\.)*)"')
esc_before = 0
esc_any = 0
for m in lit.finditer(t):
    s = m.group(1)
    if any(tok[k] in s for k in ORDER):
        if "\\" in s:
            esc_any += 1
            first = min(s.find(tok[k]) for k in ORDER if tok[k] in s)
            if "\\" in s[:first]:
                esc_before += 1
print("token_literals_with_escape", esc_any, "with_escape_before_first_token", esc_before)
# token-bearing tasks: projected object difference count under profile vs leaf-count
print("tasks_total", len(data), "tasks_with_token_leaf", len({l[0] for l in hit}))
# per-token task count pooled vs distinct
ptt = {k: len({l[0] for l in hit if tok[k] in l[3]}) for k in ORDER}
print("per_token_task_counts", ptt, "pooled_sum", sum(ptt.values()), "distinct_tasks", len({l[0] for l in hit}))
# per-token leaf counts vs occurrence counts
plc = {k: sum(1 for l in hit if tok[k] in l[3]) for k in ORDER}
poc = {k: sum(l[3].count(tok[k]) for l in hit) for k in ORDER}
print("per_token_leaf_counts", plc, "per_token_occurrence_counts", poc)
# map: token MAP vs site value 'map' vs key named map
print("json_keys_named_map", sum(1 for _ in re.finditer(r'"map"\s*:', t)), "string_value_map", len(re.findall(r'"map"\s*[,\]]', t)))

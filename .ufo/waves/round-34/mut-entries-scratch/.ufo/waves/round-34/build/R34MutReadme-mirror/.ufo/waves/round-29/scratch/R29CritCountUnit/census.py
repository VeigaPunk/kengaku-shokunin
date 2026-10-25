"""Read-only census of the pinned r28 raw WebArena config for round-29 count-unit critique.
Reads bytes once; never imports or executes upstream code."""
import hashlib, json, re, sys
from collections import Counter, defaultdict

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/"
RAW = ROOT + "plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF = ROOT + "plans/fixtures/r29/profiles.json"
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]

b = open(RAW, "rb").read()
print("raw_bytes", len(b), "sha256", hashlib.sha256(b).hexdigest())
t = b.decode("utf-8")
print("raw_codepoints", len(t), "non_ascii_codepoints", sum(1 for c in t if ord(c) > 127))
print("backslash_u_escapes", len(re.findall(r"\\u[0-9a-fA-F]{4}", t)))
print("backslash_any", t.count("\\"))
profiles = json.loads(open(PROF, "rb").read())

tok = {k: f"__{k}__" for k in ORDER}
# 1. raw non-overlapping str.count on ORIGINAL text vs sequential applied counts
print("== original-text str.count per token ==")
orig = {k: t.count(v) for k, v in tok.items()}
print(orig, "sum", sum(orig.values()))
# overlapping-occurrence count (regex lookahead)
ovl = {k: len(re.findall("(?=" + re.escape(v) + ")", t)) for k, v in tok.items()}
print("overlapping_occurrences", ovl)
# substring containment between tokens
for a in ORDER:
    for c in ORDER:
        if a != c and tok[a] in tok[c]:
            print("TOKEN_SUBSTRING", tok[a], "in", tok[c])
# all __UPPER__ like markers
allmk = Counter(re.findall(r"__[A-Z][A-Z_]*?__", t))
print("all_upper_double_underscore_markers", dict(allmk))
lowmk = Counter(re.findall(r"__[a-z][a-z_]*__", t))
print("lower_markers", dict(lowmk))
# adjacency: token immediately followed/preceded by letters/underscore
adj = Counter()
for k, v in tok.items():
    for m in re.finditer(re.escape(v), t):
        pre = t[max(0, m.start() - 1):m.start()]
        post = t[m.end():m.end() + 1]
        adj[(k, "pre_" + ("alnum_" if re.match(r"[A-Za-z0-9_]", pre) else repr(pre)), "post_" + ("alnum_" if re.match(r"[A-Za-z0-9_]", post) else repr(post)))] += 1
print("adjacency", dict(adj))

for pname, p in profiles.items():
    vals = p["values"]
    cur = t
    applied = {}
    for k in ORDER:
        applied[k] = cur.count(tok[k])
        cur = cur.replace(tok[k], vals[k])
    remaining = {k: cur.count(tok[k]) for k in ORDER}
    cascade_tokens_in_values = {k: [x for x in ORDER if tok[x] in vals[k]] for k in ORDER}
    data = json.loads(cur)
    print("== profile", pname, "applied_sequential", applied, "sum", sum(applied.values()),
          "eq_orig", applied == orig, "remaining", remaining, "tasks", len(data),
          "proj_codepoints", len(cur), "proj_sha", hashlib.sha256(cur.encode()).hexdigest()[:16],
          "values_contain_tokens", {k: v for k, v in cascade_tokens_in_values.items() if v})

# 2. leaf census on decoded raw
data = json.loads(t)
print("tasks", len(data), "distinct_task_ids", len({d["task_id"] for d in data}),
      "index_eq_task_id", sum(1 for i, d in enumerate(data) if d.get("task_id") == i))
key_hits = Counter()
leaf_hits = Counter()  # leaf count containing any token
leaf_occ = Counter()
multi_tok_leaves = 0
multi_occ_leaves = 0
field_cat = Counter()
tasks_with = set()
tasks_per_tok = defaultdict(set)
nonurl_leaf = Counter()
decoded_occ = Counter()


def walk(x, path, ti):
    global multi_tok_leaves, multi_occ_leaves
    if isinstance(x, dict):
        for k, v in x.items():
            for kk, vv in tok.items():
                if vv in k:
                    key_hits[(kk, path + "/" + k)] += 1
            walk(v, path + "/" + k, ti)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            walk(v, path + "/[]", ti)
    elif isinstance(x, str):
        occ = {kk: x.count(vv) for kk, vv in tok.items() if vv in x}
        if occ:
            tasks_with.add(ti)
            for kk, n in occ.items():
                decoded_occ[kk] += n
                tasks_per_tok[kk].add(ti)
            leaf_hits[path] += 1
            if len(occ) > 1:
                multi_tok_leaves += 1
            if sum(occ.values()) > 1:
                multi_occ_leaves += 1
            if not re.match(r"^\s*https?://|^__[A-Z_]+__", x):
                nonurl_leaf[path] += 1


for ti, d in enumerate(data):
    walk(d, "", ti)
print("decoded_leaf_token_occurrences", dict(decoded_occ), "sum", sum(decoded_occ.values()))
print("changed_leaf_count_total", sum(leaf_hits.values()), "distinct_paths", len(leaf_hits))
print("leaf_paths", dict(leaf_hits))
print("tokens_in_object_keys", dict(key_hits))
print("leaves_with_multiple_distinct_tokens", multi_tok_leaves, "leaves_with_multiple_occurrences", multi_occ_leaves)
print("tasks_with_any_token", len(tasks_with), {k: len(v) for k, v in tasks_per_tok.items()})
print("leaves_not_starting_with_url_or_token", dict(nonurl_leaf))
# 3. escaped-in-serialization tokens: occurrences in decoded leaves minus serialized
print("decoded_minus_serialized", {k: decoded_occ[k] - orig[k] for k in ORDER})

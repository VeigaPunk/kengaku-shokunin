import hashlib, json, re, sys, collections
p = "plans/fixtures/r28/webarena/config_files/test.raw.json"
b = open(p, "rb").read()
print("sha256", hashlib.sha256(b).hexdigest(), "bytes", len(b))
t = b.decode("utf-8")
toks = ["GITLAB","REDDIT","SHOPPING","SHOPPING_ADMIN","WIKIPEDIA","MAP"]
print("raw_occ", {k: t.count(f"__{k}__") for k in toks})
print("all__X__ distinct", sorted(collections.Counter(re.findall(r"__[A-Z_]+__", t)).items()))
print("lower markers", sorted(collections.Counter(re.findall(r"__[a-z_]+__", t)).items()))
print("tok_followed_by_slash", {k: t.count(f"__{k}__/") for k in toks})
data = json.loads(t)
print("tasks", len(data), "idx==task_id", sum(1 for i, x in enumerate(data) if x.get("task_id") == i))
leafpaths = collections.Counter(); leafocc = collections.Counter(); tasks_nonurl = set()
def norm(path): return re.sub(r"\[\d+\]", "[]", path)
URLISH = re.compile(r"(^|\.)(start_url|reference_url|url|storage_state)$")
def walk(o, path, tid):
    if isinstance(o, dict):
        for k, v in o.items(): walk(v, f"{path}.{k}" if path else k, tid)
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, f"{path}[{i}]", tid)
    elif isinstance(o, str):
        n = sum(o.count(f"__{k}__") for k in toks if k != "SHOPPING") + (o.count("__SHOPPING__"))
        if n:
            np_ = norm(path); leafpaths[np_] += 1; leafocc[np_] += n
            if not URLISH.search(np_): tasks_nonurl.add(tid)
for x in data: walk(x, "", x.get("task_id"))
for k in sorted(leafpaths): print("leafpath", k, "leaves", leafpaths[k], "occ", leafocc[k])
print("tasks_with_token_in_non_url_named_leaf", len(tasks_nonurl))

# Own census; does not read/import plans/config_projection.py. Upstream generator is not executed.
import json, re, sys, collections
RAW = "plans/fixtures/r28/webarena/config_files/test.raw.json"
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
raw = open(RAW, encoding="utf-8").read()
prof = json.load(open("plans/fixtures/r29/profiles.json", encoding="utf-8"))
# Counterfactual synthetic profile mirroring README.md:86-91 shapes (scheme-less, /admin, long wiki path); *.invalid hosts.
prof["readme_shape_counterfactual"] = {"values": {
    "SHOPPING": "shopping.invalid:7770", "SHOPPING_ADMIN": "shopping-admin.invalid:7780/admin",
    "REDDIT": "reddit.invalid:9999", "GITLAB": "gitlab.invalid:8023", "MAP": "map.invalid:3000",
    "WIKIPEDIA": "wikipedia.invalid:8888/wikipedia_en_all_maxi_2022-05/A/User:The_other_Kiwix_guy/Landing"}}
def leaves(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items(): yield from leaves(v, p + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from leaves(v, p + "/" + str(i))
    elif isinstance(o, str): yield p, o
base = dict(leaves(json.loads(raw)))
for name, pr in prof.items():
    t = raw
    for k in ORDER: t = t.replace("__%s__" % k, pr["values"][k])
    data = json.loads(t)
    L = dict(leaves(data))
    changed = {p: v for p, v in L.items() if base[p] != v}
    c = collections.Counter()
    for p, v in changed.items():
        c["changed_leaves"] += 1
        if "://" in v: c["leaves_with_scheme"] += 1
        if re.search(r"(?<!:)//", v): c["leaves_nonscheme_double_slash"] += 1
        if "/admin/admin" in v: c["leaves_admin_admin"] += 1
        if "/../" in v: c["leaves_dotdot"] += 1
        if p.endswith("/start_url") and "://" not in v: c["start_url_without_scheme"] += 1
    sa = [p for p in changed if "__SHOPPING_ADMIN__" in base[p]]
    c["shopping_admin_leaves"] = len(sa)
    c["shopping_admin_leaves_containing_/admin"] = sum("/admin" in changed[p] for p in sa)
    c["tasks"] = len(data)
    print(name, dict(sorted(c.items())))
# raw facts
print("raw SHOPPING_ADMIN occurrences followed by '/admin':", len(re.findall(r"__SHOPPING_ADMIN__/admin\b", raw)))
print("raw SHOPPING_ADMIN occurrences followed by '/':", len(re.findall(r"__SHOPPING_ADMIN__/", raw)))
print("raw SHOPPING_ADMIN occurrences followed by '/../':", len(re.findall(r"__SHOPPING_ADMIN__/\.\./", raw)))
print("raw 'http' substrings:", raw.count("http"))

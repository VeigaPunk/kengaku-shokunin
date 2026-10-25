"""Read-only independent census for R29CritPriorArt. Reads pinned DATA only; never imports/executes upstream code."""
import hashlib
import itertools
import json
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = LANE + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF = LANE + "/plans/fixtures/r29/profiles.json"
RAW_SHA = "7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652"
PROF_SHA = "90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018"
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]

with open(RAW, "rb") as f:
    raw_b = f.read()
with open(PROF, "rb") as f:
    prof_b = f.read()
assert hashlib.sha256(raw_b).hexdigest() == RAW_SHA, "raw pin"
assert hashlib.sha256(prof_b).hexdigest() == PROF_SHA, "profiles pin"
raw = raw_b.decode("utf-8")
profiles = json.loads(prof_b.decode("utf-8"))
print("RAW bytes", len(raw_b), "codepoints", len(raw), "sha", RAW_SHA[:12])
print("PROFILES", list(profiles))

data = json.loads(raw)
print("TASKS", len(data), "distinct_ids", len({t["task_id"] for t in data}))
print("INDEX_EQ_TASKID", sum(1 for i, t in enumerate(data) if t["task_id"] == i), "of", len(data))

# 1. token occurrences in raw text, and any other __X__ style placeholders
toks = {k: "__%s__" % k for k in ORDER}
for k in ORDER:
    print("RAW_OCC", k, raw.count(toks[k]))
print("RAW_OCC_TOTAL", sum(raw.count(t) for t in toks.values()))
other = sorted(set(re.findall(r"__[A-Z][A-Z_]*__", raw)) - set(toks.values()))
print("OTHER_DUNDER_UPPER", other)
# overlap/adjacency hazards: a token immediately followed by an uppercase letter or underscore-joined token
adj = re.findall(r"__(?:GITLAB|REDDIT|SHOPPING_ADMIN|SHOPPING|WIKIPEDIA|MAP)__[A-Z_]", raw)
print("ADJACENT_TOKEN_TAIL", len(adj), adj[:5])
for a, b in itertools.permutations(toks.values(), 2):
    if a in b:
        print("SUBSTRING", a, "in", b)
for name, p in profiles.items():
    vals = p["values"]
    hits = [(k, t) for k, v in vals.items() for t in toks.values() if t in v or "__" in v]
    print("PROFILE_VALUE_HAS_TOKEN_OR_DUNDER", name, hits)
    json_special = [k for k, v in vals.items() if any(c in v for c in '"\\') or any(ord(c) < 0x20 for c in v)]
    print("PROFILE_VALUE_JSON_SPECIAL", name, json_special)


# 2. leaf census: which JSON paths carry tokens (keys too)
def walk(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            yield ("KEY", path + (k,), k)
            yield from walk(v, path + (k,))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + (i,))
    elif isinstance(o, str):
        yield ("STR", path, o)


def gen(path):
    return "/".join("[]" if isinstance(p, int) else p for p in path[1:])


key_hits = 0
field_occ = {}
field_tasks = {}
leaf_count = 0
for i, t in enumerate(data):
    for kind, path, s in walk(t, (i,)):
        n = sum(s.count(x) for x in toks.values())
        if not n:
            continue
        if kind == "KEY":
            key_hits += n
            continue
        leaf_count += 1
        g = gen(path)
        field_occ[g] = field_occ.get(g, 0) + n
        field_tasks.setdefault(g, set()).add(i)
print("TOKEN_IN_KEYS", key_hits)
print("CHANGED_LEAVES_PER_PROFILE", leaf_count)
print("DECODED_OCC_TOTAL", sum(field_occ.values()))
for g in sorted(field_occ, key=lambda g: -field_occ[g]):
    print("FIELD", g, "occ", field_occ[g], "tasks", len(field_tasks[g]))
print("TASKS_WITH_ANY_TOKEN", len(set().union(*field_tasks.values())))

# 3. URL-vs-non-URL: leaves where the string does not START with a token (token embedded in text/code)
embedded = {}
for i, t in enumerate(data):
    for kind, path, s in walk(t, (i,)):
        if kind != "STR" or not any(x in s for x in toks.values()):
            continue
        if not re.match(r"^__(GITLAB|REDDIT|SHOPPING_ADMIN|SHOPPING|WIKIPEDIA|MAP)__", s):
            embedded.setdefault(gen(path), []).append((i, s[:90]))
for g, v in embedded.items():
    print("EMBEDDED_NONPREFIX", g, len(v), "e.g.", v[0])


# 4. order invariance over all 720 permutations, per profile
def project(text, vals, order):
    for k in order:
        text = text.replace(toks[k], vals[k])
    return text


for name, p in profiles.items():
    vals = p["values"]
    ref = project(raw, vals, ORDER)
    ref_sha = hashlib.sha256(ref.encode("utf-8")).hexdigest()
    distinct = {ref_sha}
    for perm in itertools.permutations(ORDER):
        distinct.add(hashlib.sha256(project(raw, vals, perm).encode("utf-8")).hexdigest())
    parsed = json.loads(ref)
    rem = sum(ref.count(x) for x in toks.values())
    # raw-text vs decoded-leaf agreement
    def leafsub(o):
        if isinstance(o, dict):
            return {k: leafsub(v) for k, v in o.items()}
        if isinstance(o, list):
            return [leafsub(v) for v in o]
        if isinstance(o, str):
            return project(o, vals, ORDER)
        return o
    print("PROFILE", name, "proj_sha", ref_sha[:12], "perm_distinct_digests", len(distinct), "of 720",
          "parsed", len(parsed), "remaining_tokens", rem,
          "leaf_oracle_equal", leafsub(data) == parsed, "double_slash_after_origin",
          len(re.findall(r"\.invalid:\d+(?:/prefix)?//", ref)))

# 5. structural invariance across profiles: changed-path sets per task identical?
def changed_paths(vals):
    out = []
    for i, t in enumerate(data):
        s = set()
        for kind, path, v in walk(t, (i,)):
            if kind == "STR" and project(v, vals, ORDER) != v:
                s.add(path)
        out.append(frozenset(s))
    return out


cps = [changed_paths(p["values"]) for p in profiles.values()]
print("CHANGED_PATHSETS_IDENTICAL_ACROSS_PROFILES", all(cps[0][i] == cps[1][i] == cps[2][i] for i in range(len(data))))

# 6. URL-only substitution witness: substitute only in leaves whose key name contains 'url'
def url_only(vals):
    def rec(o, key):
        if isinstance(o, dict):
            return {k: rec(v, k) for k, v in o.items()}
        if isinstance(o, list):
            return [rec(v, key) for v in o]
        if isinstance(o, str) and key is not None and "url" in str(key).lower():
            return project(o, vals, ORDER)
        return o
    return rec(data, None)


for name, p in profiles.items():
    faithful = json.loads(project(raw, p["values"], ORDER))
    uo = url_only(p["values"])
    diff_tasks = sum(1 for a, b in zip(faithful, uo) if a != b)
    print("URL_ONLY_WITNESS", name, "tasks_differing_from_faithful", diff_tasks)
sys.exit(0)

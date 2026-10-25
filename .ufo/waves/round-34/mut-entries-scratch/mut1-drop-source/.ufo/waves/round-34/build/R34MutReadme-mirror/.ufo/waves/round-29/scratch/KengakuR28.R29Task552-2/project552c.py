"""Third pass: edge cases, adjacency, shuffled-ID witness, URL-split categories."""
import hashlib
import json
from collections import Counter, defaultdict
from functools import reduce
from urllib.parse import urlsplit

RAW = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROFILES = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/profiles.json"
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOK = {k: "__%s__" % k for k in ORDER}
raw = open(RAW, "rb").read().decode("utf-8")
profiles = json.loads(open(PROFILES, "rb").read())
orig = json.loads(raw)


def project(values, text=raw):
    return reduce(lambda s, k: s.replace(TOK[k], values[k]), ORDER, text)


def walk(a, b, path=()):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in a:
            yield from walk(a[k], b[k], path + (k,))
    elif isinstance(a, list) and isinstance(b, list):
        for i, (x, y) in enumerate(zip(a, b)):
            yield from walk(x, y, path + (i,))
    elif a != b:
        yield path, a, b


# 1. marker pairwise substring
print("PAIRWISE_SUBSTRING", {(a, b): TOK[a] in TOK[b] for a in ORDER for b in ORDER if a != b and TOK[a] in TOK[b]})
print("PROFILE_VALUES_CONTAIN_MARKER", {p: any("__" in v for v in profiles[p]["values"].values()) for p in profiles})

# 2. adjacency census in raw text
prev_c = defaultdict(Counter)
next_c = defaultdict(Counter)
for k in ORDER:
    i = raw.find(TOK[k])
    while i >= 0:
        prev_c[k][raw[i - 1] if i else "<BOF>"] += 1
        j = i + len(TOK[k])
        next_c[k][raw[j] if j < len(raw) else "<EOF>"] += 1
        i = raw.find(TOK[k], j)
print("PREV_CHAR", {k: dict(v) for k, v in prev_c.items()})
print("NEXT_CHAR", {k: dict(v) for k, v in next_c.items()})

# 3. leaves per token and distinct tasks per token
leaf_per_tok = Counter()
task_per_tok = defaultdict(set)
for ti, d in enumerate(orig):
    def leaves(n, path=()):
        if isinstance(n, dict):
            for k, v in n.items():
                yield from leaves(v, path + (k,))
        elif isinstance(n, list):
            for i, v in enumerate(n):
                yield from leaves(v, path + (i,))
        elif isinstance(n, str):
            yield path, n
    for path, s in leaves(d):
        for k in ORDER:
            if TOK[k] in s:
                leaf_per_tok[k] += 1
                task_per_tok[k].add(ti)
print("LEAVES_PER_TOKEN", dict(leaf_per_tok))
print("TASKS_PER_TOKEN", {k: len(v) for k, v in task_per_tok.items()})
print("TASKID552_TOKEN_PRESENT", {k: any(TOK[k] in s for _p, s in
      [(None, json.dumps(orig[552]))] ) for k in ORDER})

# 4. edge case retrieval: annotation, multi-token start_url, program_html URL, reference_url, must_include
def find(pathpred):
    for ti, d in enumerate(orig):
        for path, old, new in walk(d, json.loads(project(profiles["distinct_origins"]["values"]))[ti]):
            yield ti, path, old, new

print("\nANNOTATION_CASES")
for ti, path, old, new in find(None):
    if path and path[-1] == "reference_answer_raw_annotation":
        print(" task", orig[ti]["task_id"], "path", path)
        print("  old", json.dumps(old, ensure_ascii=True))
        print("  new", json.dumps(new, ensure_ascii=True))

print("\nMULTI_START_URL")
for ti, path, old, new in find(None):
    if len(path) == 2 and path[1] == "start_url" and sum(old.count(TOK[k]) for k in ORDER) > 1:
        print(" task", orig[ti]["task_id"], "counts", {k: old.count(TOK[k]) for k in ORDER if TOK[k] in old})
        print("  old", json.dumps(old, ensure_ascii=True))
        print("  new", json.dumps(new, ensure_ascii=True))

print("\nMULTI_REFERENCE_URL")
n = 0
for ti, path, old, new in find(None):
    if len(path) == 3 and path[1] == "eval" and path[2] == "reference_url" and sum(old.count(TOK[k]) for k in ORDER) > 1:
        n += 1
        print(" task", orig[ti]["task_id"], "counts", {k: old.count(TOK[k]) for k in ORDER if TOK[k] in old})
        print("  old", json.dumps(old, ensure_ascii=True)[:200])
        print("  new", json.dumps(new, ensure_ascii=True)[:200])
print(" multi_reference_url_count", n)

print("\nBARE_START_URL_SAMPLES_PER_TOKEN")
seen = set()
for ti, path, old, new in find(None):
    if len(path) == 2 and path[1] == "start_url" and old in [TOK[k] for k in ORDER]:
        for k in ORDER:
            if old == TOK[k] and k not in seen:
                seen.add(k)
                print(" token", k, "task", orig[ti]["task_id"], "old", old, "new", new)

print("\nPROGRAM_HTML_URL_SAMPLES")
shown = set()
for ti, path, old, new in find(None):
    if "program_html" in path and path[-1] == "url":
        for k in ORDER:
            if TOK[k] in old and k not in shown:
                shown.add(k)
                print(" token", k, "task", orig[ti]["task_id"], "old", json.dumps(old)[:160], "->", new[:160])

print("\nMUST_INCLUDE_SAMPLES")
shown = set()
for ti, path, old, new in find(None):
    if path and path[-1] == "must_include":
        for k in ORDER:
            if TOK[k] in old and k not in shown:
                shown.add(k)
                print(" token", k, "task", orig[ti]["task_id"], "old", json.dumps(old)[:160], "->", new[:160])

# 5. URL split categories per profile for changed leaves
print("\nURLSPLIT_SUMMARY")
for pname in profiles:
    proj = json.loads(project(profiles[pname]["values"]))
    cats = Counter()
    dbl = 0
    for ti, (path, old, new) in enumerate(walk(orig, proj)):
        pass
    diffs = list(walk(orig, proj))
    # walk yields across whole doc; path carries list index; need task local paths; redo per task
    dbl = 0
    schemes = Counter()
    for ti, d in enumerate(orig):
        for path, old, new in walk(d, proj[ti]):
            if isinstance(new, str):
                sp = urlsplit(new)
                schemes[sp.scheme] += 1
                rest = new[len(sp.scheme) + 3:] if new.startswith(sp.scheme + "://") else ""
                if "//" in rest:
                    dbl += 1
    print(" ", pname, "schemes", dict(schemes), "leaves_with_post_scheme_double_slash", dbl)

# 6. shuffled-ID hand witness, literal source-contract walk
hand = '[{"task_id": 7, "start_url": "__GITLAB__/x"}, {"task_id": 2, "start_url": "__MAP__"}]'
print("\nHAND_RAW", hand)
for pname in profiles:
    txt = project(profiles[pname]["values"], hand)
    parsed = json.loads(txt)
    print(" ", pname, "text", txt)
    for idx, item in enumerate(parsed):
        print("   output", idx, "-> task_id", item["task_id"], "start_url", item["start_url"])

# 7. reversed frozen list witness (still independent, not upstream execution)
rev = list(reversed(orig))
print("\nREVERSED_FROZEN_WITNESS first3", [(i, rev[i]["task_id"]) for i in range(3)],
      "last1", (len(rev) - 1, rev[-1]["task_id"]))
print(" index_equals_task_id_after_reverse", all(i == d["task_id"] for i, d in enumerate(rev)))

# 8. hash of per-profile projected parse canonical? record text sha already; also empty projection guard
for pname in profiles:
    txt = project(profiles[pname]["values"])
    print("TEXT_SHA", pname, hashlib.sha256(txt.encode()).hexdigest(), len(txt))

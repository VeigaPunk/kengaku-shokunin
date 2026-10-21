"""Independent projection case for raw task_id 552 + 3 frozen neutral profiles.

Reads pinned bytes once, performs the six global serialized-text replacements in
source order, parses, enumerates by position, and walks original/projected JSON in
parallel. No upstream import/execution; no production projection module exists or is read.
"""
import hashlib
import json
import sys
from collections import Counter, defaultdict

RAW = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROFILES = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/profiles.json"
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOK = {k: "__%s__" % k for k in ORDER}

raw_bytes = open(RAW, "rb").read()
raw = raw_bytes.decode("utf-8")
prof_bytes = open(PROFILES, "rb").read()
profiles = json.loads(prof_bytes)
orig = json.loads(raw)

print("RAW bytes=%d codepoints=%d ascii=%s sha256=%s" % (
    len(raw_bytes), len(raw), raw.isascii(), hashlib.sha256(raw_bytes).hexdigest()))
print("PROFILES bytes=%d sha256=%s keys=%s" % (
    len(prof_bytes), hashlib.sha256(prof_bytes).hexdigest(), list(profiles)))


def walk(a, b, path=()):
    """Yield (path, old, new) for leaves whose serialized value differs."""
    if type(a) is not type(b):
        yield path, a, b
        return
    if isinstance(a, dict):
        if list(a) != list(b):
            yield path, list(a), list(b)
        for k in a:
            if k in b:
                yield from walk(a[k], b[k], path + (k,))
        return
    if isinstance(a, list):
        for i, (x, y) in enumerate(zip(a, b)):
            yield from walk(x, y, path + (i,))
        if len(a) != len(b):
            yield path, len(a), len(b)
        return
    if a != b:
        yield path, a, b


def leaf_strings(node, path=()):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from leaf_strings(v, path + (k,))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from leaf_strings(v, path + (i,))
    elif isinstance(node, str):
        yield path, node


def is_urlish(value):
    return isinstance(value, str) and (value.startswith("http://") or value.startswith("https://"))


# occurrence census by leaf and by next-character context
leaf_occ = Counter()
ctx_next = defaultdict(Counter)
for path, s in leaf_strings(orig):
    for name, tok in TOK.items():
        n = s.count(tok)
        if n:
            leaf_occ[(name, path[0] if path else "<root>")] += n
            # collect characters immediately after each occurrence
            i = s.find(tok)
            while i >= 0:
                j = i + len(tok)
                ctx_next[name][s[j] if j < len(s) else "<EOL>"] += 1
                i = s.find(tok, j)
print("TOKEN_OCCURRENCES_TOTAL", {k: sum(v for (n, _f), v in leaf_occ.items() if n == k) for k in ORDER})
print("BY_FIELD", dict(sorted(((f"{n}@{f}", v) for (n, f), v in leaf_occ.items()), key=lambda x: (x[0].split('@')[1], x[0]))))
print("NEXT_CHAR", {k: dict(v) for k, v in ctx_next.items()})

results = {}
for pname in profiles:
    vals = profiles[pname]["values"]
    text = raw
    repl = {}
    for name in ORDER:
        tok = TOK[name]
        c = text.count(tok)
        repl[name] = c
        text = text.replace(tok, vals[name])
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    proj = json.loads(text)
    diffs = list(walk(orig, proj))
    by_field = Counter(p[0] if p else "<root>" for p, _o, _n in diffs)
    by_path = Counter(p for p, _o, _n in diffs)
    print("\nPROFILE", pname, "purpose=", profiles[pname]["purpose"])
    print(" replacement_counts", repl)
    print(" projected_chars", len(text), "sha256", sha)
    print(" parsed_tasks", len(proj), "changed_leaves", len(diffs))
    print(" changed_by_toplevel_field", dict(sorted(by_field.items())))
    print(" changed_distinct_paths", len(by_path))
    # verify diff leaf count equals leaves containing >=1 token
    expect = sum(1 for _p, s in leaf_strings(orig) if any(t in s for t in TOK.values()))
    print(" leaves_containing_token", expect, "match", expect == len(diffs))
    # value samples per token from diffs
    samples = {}
    for name, tok in TOK.items():
        for p, o, n in diffs:
            if isinstance(o, str) and tok in o:
                samples.setdefault(name, (p, o, n))
    for name in ORDER:
        if name in samples:
            p, o, n = samples[name]
            print("  SAMPLE", name, "path", ".".join(map(str, p)))
            print("    old:", json.dumps(o, ensure_ascii=True)[:220])
            print("    new:", json.dumps(n, ensure_ascii=True)[:220])
        else:
            print("  SAMPLE", name, "NONE (zero occurrences)")
    # path-shape distribution at depth<=2
    shapes = Counter(".".join(str(x) if not isinstance(x, int) else "[]" for x in p[:2]) for p, _o, _n in diffs)
    print(" changed_path_shapes", dict(sorted(shapes.items())))
    # urlish vs non-urlish changed leaves
    url_leaves = sum(1 for _p, o, n in diffs if is_urlish(o))
    print(" changed_leaves_that_were_urlish", url_leaves, "non_urlish", len(diffs) - url_leaves)
    results[pname] = dict(repl=repl, sha=sha, tasks=len(proj), diffs=len(diffs),
                          by_field=dict(by_field), samples=samples)

# index vs task_id
ids = [d["task_id"] for d in orig]
print("\nINDEX_VS_TASK_ID all_equal=%s n=%d" % (all(i == v for i, v in enumerate(ids)), len(ids)))

# task 552 in detail
t = orig[552]
print("\nTASK552 task_id", t["task_id"], "sites", t["sites"], "start_url", json.dumps(t["start_url"]))
print("TASK552 eval", json.dumps(t["eval"], ensure_ascii=True)[:900])
print("TASK552 storage_state", json.dumps(t["storage_state"], ensure_ascii=True)[:400])
print("TASK552 intent", json.dumps(t["intent"], ensure_ascii=True)[:300])
print("TASK552 intent_template", json.dumps(t["intent_template"], ensure_ascii=True)[:300])
print("TASK552 instantiation_dict", json.dumps(t["instantiation_dict"], ensure_ascii=True)[:400])

# per-token occurrences inside task 552 object
for name, tok in TOK.items():
    cnt = 0
    for _p, s in leaf_strings(t):
        cnt += s.count(tok)
    print("TASK552 token", name, cnt)

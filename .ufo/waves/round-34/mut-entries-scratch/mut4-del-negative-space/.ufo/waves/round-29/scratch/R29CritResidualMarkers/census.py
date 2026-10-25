"""Read-only residual-marker census over the pinned raw WebArena config (data only)."""
import hashlib, json, re, sys, collections

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/"
RAW = ROOT + "plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF = ROOT + "plans/fixtures/r29/profiles.json"
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]

b = open(RAW, "rb").read()
print("raw_sha256", hashlib.sha256(b).hexdigest(), "bytes", len(b))
text = b.decode("utf-8")
print("codepoints", len(text), "non_ascii_codepoints", sum(1 for c in text if ord(c) > 127))
print("backslash_u_escapes_raw", len(re.findall(r"\\u[0-9a-fA-F]{4}", text)))

# 1. every maximal dunder-delimited identifier in RAW TEXT
pat = re.compile(r"__([A-Za-z0-9]+(?:_[A-Za-z0-9]+)*)__")
c = collections.Counter(m.group(0) for m in pat.finditer(text))
print("\n[raw-text dunder identifiers]")
for k, v in sorted(c.items()):
    print(f"  {k!r}: {v}")

# any '__' run not explained by the identifier regex
spans = set()
for m in pat.finditer(text):
    spans.update(range(m.start(), m.end()))
loose = [i for i in range(len(text) - 1) if text[i:i+2] == "__" and i not in spans]
print("unexplained '__' positions:", len(loose))
for i in loose[:20]:
    print("   ", repr(text[max(0, i-40):i+40]))

# case-insensitive variants of the six tokens not exactly matching
for t in ORDER:
    exact = text.count(f"__{t}__")
    ci = len(re.findall(re.escape(f"__{t}__"), text, re.I))
    bare = len(re.findall(r"(?<![A-Za-z_])" + t + r"(?![A-Za-z_])", text))
    print(f"token {t}: exact={exact} case_insensitive={ci} bare_word_uppercase={bare}")

# overlap: does any token occur inside another token's literal?
for a in ORDER:
    for z in ORDER:
        if a != z and f"__{a}__" in f"__{z}__":
            print("OVERLAP", a, "in", z)

# 2. decoded-leaf census: where do markers live (path categories)
data = json.loads(text)
print("\ntasks", len(data), "distinct_ids", len({d['task_id'] for d in data}))

def walk(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(k, str) and "__" in k:
                yield path + ("<KEY>",), k
            yield from walk(v, path + (k,))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + ("[]",))
    elif isinstance(o, str):
        yield path, o

by_marker_path = collections.defaultdict(collections.Counter)
tasks_by_marker = collections.defaultdict(set)
cooccur = collections.Counter()
examples = {}
for d in data:
    for path, s in walk(d, ()):
        ms = [m.group(0) for m in pat.finditer(s)]
        for mk in ms:
            p = ".".join(path)
            by_marker_path[mk][p] += 1
            tasks_by_marker[mk].add(d["task_id"])
            examples.setdefault((mk, p), (d["task_id"], s))
        envs = {m for m in ms if m.strip("_") in ORDER}
        runs = {m for m in ms if m.strip("_") not in ORDER}
        if envs and runs:
            cooccur[(tuple(sorted(envs)), tuple(sorted(runs)), ".".join(path))] += 1
print("\n[decoded-leaf marker occurrences by path]")
for mk in sorted(by_marker_path):
    print(f" {mk}: leaf-occ={sum(by_marker_path[mk].values())} tasks={len(tasks_by_marker[mk])}")
    for p, n in by_marker_path[mk].most_common():
        tid, s = examples[(mk, p)]
        print(f"    {p}: {n}  e.g. task {tid}: {s[:110]!r}")
print("\n[same-leaf co-occurrence env-token x non-env-marker]")
for k, v in cooccur.most_common():
    print("  ", k, v)

# 3. projection under each frozen profile: residual markers after six replacements
prof = json.load(open(PROF))
print("\n[post-projection residual dunder identifiers per profile]")
for name, p in prof.items():
    t = text
    for tok in ORDER:
        t = t.replace(f"__{tok}__", p["values"][tok])
    rc = collections.Counter(m.group(0) for m in pat.finditer(t))
    newly = {k: v for k, v in rc.items() if c.get(k) != v}
    ok = True
    try:
        json.loads(t)
    except Exception as e:
        ok = repr(e)
    print(f" {name}: parse={ok} residual={dict(sorted(rc.items()))} changed_vs_raw={newly}")

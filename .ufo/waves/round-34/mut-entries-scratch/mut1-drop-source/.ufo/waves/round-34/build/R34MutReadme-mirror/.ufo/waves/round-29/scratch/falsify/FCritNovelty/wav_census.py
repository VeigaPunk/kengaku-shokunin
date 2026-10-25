"""Read-only census of public prior-art files fetched into ./fetch. Data only; no code executed."""
import json, re, collections
TOK = re.compile(r"__(GITLAB|REDDIT|SHOPPING_ADMIN|SHOPPING|WIKIPEDIA|MAP|HOMEPAGE)__")
def walk(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items(): yield from walk(v, f"{p}.{k}")
    elif isinstance(o, list):
        for v in o: yield from walk(v, f"{p}[]")
    elif isinstance(o, str):
        yield p, o
for name in ("fetch/wav_verified.json", "fetch/wav_test.raw.json"):
    d = json.load(open(name, encoding="utf-8"))
    occ = collections.Counter(); leaves = collections.Counter(); nonurl = collections.Counter()
    for t in d:
        for p, s in walk(t):
            n = len(TOK.findall(s))
            if n:
                occ[p] += n; leaves[p] += 1
                if not re.search(r"url", p, re.I): nonurl[p] += 1
    print(name, "tasks", len(d), "idx==task_id", sum(1 for i, t in enumerate(d) if t.get("task_id") == i))
    print("  token occurrences", sum(occ.values()), "token-bearing leaves", sum(leaves.values()))
    for p, c in sorted(leaves.items(), key=lambda x: -x[1]): print("   leaf-path", p, c)
    print("  leaves on paths without 'url' in path:", sum(nonurl.values()), dict(nonurl))

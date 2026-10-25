"""Third read-only census: offset-frame divergence, multi-occurrence leaf shapes, quote word counts."""
import json, re
from collections import Counter

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/"
t = open(ROOT + "plans/fixtures/r28/webarena/config_files/test.raw.json", "rb").read().decode("utf-8")
profiles = json.loads(open(ROOT + "plans/fixtures/r29/profiles.json", "rb").read())
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
tok = {k: f"__{k}__" for k in ORDER}

vals = profiles["distinct_origins"]["values"]
orig_offsets = {k: [m.start() for m in re.finditer(re.escape(tok[k]), t)] for k in ORDER}
cur = t
diverge = {}
for k in ORDER:
    inter = [m.start() for m in re.finditer(re.escape(tok[k]), cur)]
    diverge[k] = (len(inter), sum(1 for a, b in zip(orig_offsets[k], inter) if a != b))
    cur = cur.replace(tok[k], vals[k])
print("distinct_origins: (occurrences, original_vs_intermediate_codepoint_offset_mismatches)", diverge)

data = json.loads(t)
def walk(x, path, out):
    if isinstance(x, dict):
        for k, v in x.items():
            walk(v, path + "/" + k, out)
    elif isinstance(x, list):
        for v in x:
            walk(v, path + "/[]", out)
    elif isinstance(x, str):
        out.append((path, x))
seps = Counter()
for ti, d in enumerate(data):
    o = []
    walk(d, "", o)
    for p, s in o:
        n = sum(s.count(tok[k]) for k in ORDER)
        if n > 1:
            rest = s
            for k in ORDER:
                rest = rest.replace(tok[k], "\x00")
            sep = re.findall(r"[^\x00]*?(\s*(?:\|[A-Z]+\||,|\s)\s*)\x00", rest)
            seps[(p, tuple(sorted(set(x.strip() for x in sep))))] += 1
            print("multi", ti, p, n, repr(re.sub(r"/[^ ,|]*", "/…", s)[:110]))
print("multi_separators", dict(seps))

plan = open(ROOT + "plans/round-29-claims.md", encoding="utf-8").read()
quotes = [
    "exact order and later-token cascade",
    "distinguish replacement occurrence counts, changed-leaf counts and task counts; do not pool units.",
    "F3 global replacement changes at least one non-URL-valued field, p=.7;",
    "raw occurrence provenance uses clearly named Unicode-codepoint offsets, NOT claimed byte offsets;",
    "The new projection must have a failing wrong URL-only or wrong-order witness before its control counts.",
    "unread metadata remains metadata, not a consumed scorer predicate.",
]
flat = re.sub(r"\s+", " ", plan)
for q in quotes:
    line = next((i + 1 for i, l in enumerate(plan.splitlines()) if q.split()[0] in l and q[:20].split()[-1] in l), None)
    print("QUOTE present=%s words=%d" % (q in flat, len(q.split())), repr(q))
for i, l in enumerate(plan.splitlines(), 1):
    for needle in ["later-token cascade", "do not pool units", "F3 global", "Unicode-codepoint", "wrong URL-only", "unread metadata"]:
        if needle in l:
            print("LINE", i, needle)

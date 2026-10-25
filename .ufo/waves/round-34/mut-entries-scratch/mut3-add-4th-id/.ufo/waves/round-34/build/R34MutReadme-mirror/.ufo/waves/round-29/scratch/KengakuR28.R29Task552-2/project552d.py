"""Fourth pass: corrected samples, start_url shape split, re-serialization facts."""
import json
from collections import Counter
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


proj0 = json.loads(project(profiles["distinct_origins"]["values"]))
diffs = []
for ti, d in enumerate(orig):
    for path, old, new in walk(d, proj0[ti]):
        diffs.append((ti, path, old, new))
print("TOTAL_DIFFS", len(diffs))

# start_url shape split
su = [(ti, old, new) for ti, path, old, new in diffs if path == ("start_url",)]
print("START_URL_LEAVES", len(su))
bare = Counter()
suffixed = Counter()
for ti, old, new in su:
    for k in ORDER:
        c = old.count(TOK[k])
        if not c:
            continue
        if old == TOK[k]:
            bare[k] += 1
        else:
            suffixed[k] += 1
print("START_URL_BARE", dict(bare), "total", sum(bare.values()))
print("START_URL_SUFFIXED", dict(suffixed), "total", sum(suffixed.values()))
print("START_URL_MULTI", [(orig[ti]["task_id"], old) for ti, old, new in su
                           if sum(old.count(TOK[k]) for k in ORDER) > 1])
print("START_URL_NO_TOKEN", sum(1 for _ti, old, _n in su if not any(TOK[k] in old for k in ORDER)))
print("START_URL_OLD_SAMPLE", json.dumps(su[0][1]), "NEW", su[0][2])
print("START_URL_OLD_SAMPLE_LAST", json.dumps(su[-1][1]), "NEW", su[-1][2])

# reference_url samples/counts
ru = [(ti, path, old, new) for ti, path, old, new in diffs if path == ("eval", "reference_url")]
print("\nREFERENCE_URL_LEAVES", len(ru))
print("REFERENCE_URL_EMPTY_OLD", sum(1 for _ti, _p, old, _n in ru if old == ""))
print("REFERENCE_URL_BY_TOKEN", {k: sum(1 for _ti, _p, old, _n in ru if TOK[k] in old) for k in ORDER})
for k in ORDER:
    for ti, path, old, new in ru:
        if TOK[k] in old:
            print("  sample", k, "task", orig[ti]["task_id"], "old", json.dumps(old)[:170])
            print("     new", json.dumps(new)[:170])
            break

# program_html url counts
pu = [(ti, path, old, new) for ti, path, old, new in diffs if path[:2] == ("eval", "program_html") and path[-1] == "url"]
print("\nPROGRAM_HTML_URL_LEAVES", len(pu), "by_token",
      {k: sum(1 for _ti, _p, old, _n in pu if TOK[k] in old) for k in ORDER})

# must_include
mi = [(ti, path, old, new) for ti, path, old, new in diffs if path[:2] == ("eval", "program_html") and len(path) > 3 and path[3] == "required_contents"]
print("\nMUST_INCLUDE_LEAVES", len(mi), "by_token",
      {k: sum(1 for _ti, _p, old, _n in mi if TOK[k] in old) for k in ORDER})
for k in ORDER:
    for ti, path, old, new in mi:
        if TOK[k] in old:
            print("  sample", k, "task", orig[ti]["task_id"], "path", path)
            print("     old", json.dumps(old)[:170])
            print("     new", json.dumps(new)[:170])
            break

# annotation
an = [(ti, path, old, new) for ti, path, old, new in diffs if path == ("eval", "reference_answer_raw_annotation")]
print("\nANNOTATION_LEAVES", len(an), [(orig[ti]["task_id"], path) for ti, path, _o, _n in an])

# eval leaf task set
eval_tasks = {ti for ti, path, _o, _n in diffs if path and path[0] == "eval"}
print("EVAL_TASK_COUNT", len(eval_tasks))

# double-slash origins in raw placeholders
print("\nRAW_TOKEN_FOLLOWED_BY_DOUBLE_SLASH", {k: raw.count(TOK[k] + "//") for k in ORDER})
print("RAW_UNICODE_ESCAPES", raw.count("\\u"), "RAW_ASCII", raw.isascii())

# reserialization: json.dump(item, indent=2) length sample
item = proj0[0]
text2 = json.dumps(item, indent=2)
print("PER_TASK_DUMP_CHARS task0", len(text2), "starts", repr(text2[:80]))
print("PER_TASK_DUMP_HAS_UNICODE_ESCAPE", "\\u" in text2)
print("PER_TASK_KEYS_ORDER_SAMPLE", list(item)[:6])

# schemes/hosts per profile for task552
print("\nT552_URLSPLIT")
for pname in profiles:
    tp = json.loads(project(profiles[pname]["values"]))[552]
    for field, val in [("start_url", tp["start_url"]),
                       ("program_html[0].url", tp["eval"]["program_html"][0]["url"]),
                       ("must_include[0]", tp["eval"]["program_html"][0]["required_contents"]["must_include"][0])]:
        sp = urlsplit(val)
        print(" ", pname, field, "scheme", sp.scheme, "netloc", sp.netloc, "path", sp.path[:60], "query", sp.query)

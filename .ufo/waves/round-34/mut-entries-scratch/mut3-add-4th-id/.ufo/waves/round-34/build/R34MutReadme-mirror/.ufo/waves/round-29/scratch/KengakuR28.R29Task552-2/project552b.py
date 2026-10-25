"""Second pass: exact changed-path templates, provenance offsets, task-552 detail."""
import hashlib
import json
from collections import Counter, defaultdict

RAW = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROFILES = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/profiles.json"
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOK = {k: "__%s__" % k for k in ORDER}

raw_bytes = open(RAW, "rb").read()
raw = raw_bytes.decode("utf-8")
profiles = json.loads(open(PROFILES, "rb").read())
orig = json.loads(raw)


def walk(a, b, path=()):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in a:
            yield from walk(a[k], b[k], path + (k,))
    elif isinstance(a, list) and isinstance(b, list):
        for i, (x, y) in enumerate(zip(a, b)):
            yield from walk(x, y, path + (i,))
    elif a != b:
        yield path, a, b


def tmpl(path):
    out = []
    for p in path:
        out.append("[]" if isinstance(p, int) else p)
    return ".".join(out)


def leaf_strings(node, path=()):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from leaf_strings(v, path + (k,))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from leaf_strings(v, path + (i,))
    elif isinstance(node, str):
        yield path, node


# keys holding tokens (expect none)
key_hits = Counter()
for d in orig:
    def scan_keys(n, path=()):
        if isinstance(n, dict):
            for k, v in n.items():
                if any(t in k for t in TOK.values()):
                    key_hits[k] += 1
                scan_keys(v, path + (k,))
        elif isinstance(n, list):
            for i, v in enumerate(n):
                scan_keys(v, path + (i,))
    scan_keys(d)
print("TOKENS_IN_KEYS", dict(key_hits))

# first occurrence codepoint offsets per token
print("FIRST_CODEPOINT_OFFSET", {k: raw.find(TOK[k]) for k in ORDER})
print("LAST_CODEPOINT_OFFSET", {k: raw.rfind(TOK[k]) for k in ORDER})
print("RAW_ASCII", raw.isascii(), "CODEPOINTS", len(raw), "BYTES", len(raw_bytes))

# occurrence census by collapsed path template and token
occ_tmpl = Counter()
occ_field = Counter()
leaves_per_tmpl = Counter()
for path, s in leaf_strings(orig):
    hits = sum(s.count(t) for t in TOK.values())
    if not hits:
        continue
    t = tmpl(path)
    leaves_per_tmpl[t] += 1
    for k in ORDER:
        c = s.count(TOK[k])
        if c:
            occ_tmpl[(k, t)] += c
            occ_field[(k, path[0] if path and isinstance(path[0], str) else "<root>")] += c
print("LEAVES_PER_TEMPLATE", dict(sorted(leaves_per_tmpl.items())))
print("OCC_BY_TEMPLATE")
for (k, t), c in sorted(occ_tmpl.items(), key=lambda x: (x[0][1], ORDER.index(x[0][0]))):
    print("  ", k, t, c)
print("OCC_BY_TOPFIELD", dict(sorted(((f"{k}@{f}", c) for (k, f), c in occ_field.items()))))

# multi-token leaves
multi = []
for path, s in leaf_strings(orig):
    present = [k for k in ORDER if TOK[k] in s]
    if len(present) > 1 or any(s.count(t) > 1 for t in TOK.values()):
        multi.append((tmpl(path), len(present), {k: s.count(TOK[k]) for k in present if s.count(TOK[k])}))
print("MULTI_OCCURRENCE_LEAVES", len(multi))
for m in multi[:10]:
    print("  ", m)
print("MULTI_SHAPES", dict(Counter(m[0] for m in multi)))

# task-552 detail per profile
t = orig[552]
print("\nT552 starts", t["task_id"], "sites", t["sites"], "start_url", json.dumps(t["start_url"]))
for pname, pdata in profiles.items():
    proj = json.loads(__import__("functools").reduce(
        lambda s, k: s.replace(TOK[k], pdata["values"][k]), ORDER, raw))
    tp = proj[552]
    print("\nT552 PROFILE", pname)
    print("  output_ordinal", 552, "task_id", tp["task_id"], "equal", tp["task_id"] == 552)
    print("  start_url", json.dumps(tp["start_url"]))
    print("  eval.program_html[0].url", json.dumps(tp["eval"]["program_html"][0]["url"]))
    for mi, val in enumerate(tp["eval"]["program_html"][0]["required_contents"]["must_include"]):
        print("  must_include[%d]" % mi, json.dumps(val))
    print("  storage_state", json.dumps(tp["storage_state"]))
    print("  intent", json.dumps(tp["intent"]))
    print("  instantiation_dict", json.dumps(tp["instantiation_dict"]))
    print("  require_login", tp["require_login"], "require_reset", tp["require_reset"],
          "geolocation", tp["geolocation"], "reference_url", json.dumps(tp["eval"]["reference_url"]),
          "reference_answers", json.dumps(tp["eval"]["reference_answers"]))

# structural invariance across profiles: path template sets and counts
base = None
for pname, pdata in profiles.items():
    proj = json.loads(__import__("functools").reduce(
        lambda s, k: s.replace(TOK[k], pdata["values"][k]), ORDER, raw))
    diffs = list(walk(orig, proj))
    sig = Counter(tmpl(p) for p, _o, _n in diffs)
    print("\nINVARIANCE", pname, "leaves", len(diffs), "sig", dict(sorted(sig.items())))
    if base is None:
        base = sig
    else:
        print("  same_path_signature", sig == base)

# tasks with eval changed vs start_url changed
for pname, pdata in profiles.items():
    proj = json.loads(__import__("functools").reduce(
        lambda s, k: s.replace(TOK[k], pdata["values"][k]), ORDER, raw))
    diffs = list(walk(orig, proj))
    start_tasks = {p[0] for p, _o, _n in diffs if len(p) == 2 and p[1] == "start_url"}
    eval_tasks = {p[0] for p, _o, _n in diffs if len(p) >= 2 and p[1] == "eval"}
    print("\nTASK_COVERAGE", pname, "start_url_tasks", len(start_tasks), "eval_tasks", len(eval_tasks),
          "overlap", len(start_tasks & eval_tasks), "union", len(start_tasks | eval_tasks))

# remaining known placeholders after projection
for pname, pdata in profiles.items():
    proj_txt = __import__("functools").reduce(
        lambda s, k: s.replace(TOK[k], pdata["values"][k]), ORDER, raw)
    print("REMAINING", pname, {k: proj_txt.count(TOK[k]) for k in ORDER},
          "any_marker", sum(proj_txt.count(t) for t in TOK.values()))

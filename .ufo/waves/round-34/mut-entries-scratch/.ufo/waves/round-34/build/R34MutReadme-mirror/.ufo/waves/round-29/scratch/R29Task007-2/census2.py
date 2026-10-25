"""Second independent pass: exact category/unit table and item-7 artifact bytes."""
import hashlib
import json
import collections

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = ROOT + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF = ROOT + "/plans/fixtures/r29/profiles.json"
raw = open(RAW, "rb").read().decode("utf-8")
data = json.loads(raw)
prof = json.loads(open(PROF, "rb").read().decode("utf-8"))
TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__",
          "__WIKIPEDIA__", "__MAP__"]
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


class S:
    def __init__(s, t):
        s.s = t
        s.n = len(t)

    def ws(s, i):
        while i < s.n and s.s[i] in " \t\r\n":
            i += 1
        return i

    def parse(s, i, path, out):
        i = s.ws(i)
        c = s.s[i]
        if c == '"':
            st = i
            val, i = json.decoder.scanstring(s.s, i + 1)
            out.append((path, st, i, val))
            return i
        if c == "{":
            i = s.ws(i + 1)
            if s.s[i] == "}":
                return i + 1
            while True:
                i = s.ws(i)
                k, i = json.decoder.scanstring(s.s, i + 1)
                i = s.ws(i)
                i = s.parse(i + 1, path + (k,), out)
                i = s.ws(i)
                if s.s[i] == ",":
                    i += 1
                    continue
                return i + 1
        if c == "[":
            i = s.ws(i + 1)
            k = 0
            if s.s[i] == "]":
                return i + 1
            while True:
                i = s.parse(i, path + (k,), out)
                k += 1
                i = s.ws(i)
                if s.s[i] == ",":
                    i += 1
                    continue
                return i + 1
        for lit, ln in (("true", 4), ("false", 5), ("null", 4)):
            if s.s.startswith(lit, i):
                return i + ln
        j = i
        while j < s.n and s.s[j] in "-+0123456789.eE":
            j += 1
        return j


leaves = []
end = S(raw).parse(0, (), leaves)
assert end == len(raw) - 1 and raw[end] == "\n"


def norm(p):
    o = ""
    for x in p:
        o += "[#]" if isinstance(x, int) else (("." if o else "") + x)
    return o


print("RAW sha256", sha(raw), "bytes", len(raw.encode()), "codepoints", len(raw))
print("RAW_IS_UTF8_ASCII", all(ord(c) < 128 for c in raw))
print("TOP_LIST", len(data), "string_leaves", len(leaves))

# ---- category table ----
cat_occ = collections.Counter()
cat_leaves = collections.Counter()
multi = []
items_by_cat = collections.defaultdict(set)
for p, st, en, v in leaves:
    hits = [(t, v.count(t)) for t in TOKENS if t in v]
    if not hits:
        continue
    c = norm(p)
    n = sum(k for _, k in hits)
    cat_occ[c] += n
    cat_leaves[c] += 1
    items_by_cat[c].add(p[0])
    if n > 1:
        multi.append((p[0], c, n, v, [h for h in hits]))
print("CATEGORY_TABLE")
for c in sorted(cat_occ):
    print("  %-52s occ=%3d leaves=%3d items=%3d" %
          (c, cat_occ[c], cat_leaves[c], len(items_by_cat[c])))
print("  TOTAL occ=%d leaves=%d" % (sum(cat_occ.values()), sum(cat_leaves.values())))
print("MULTI_OCC_LEAVES", len(multi))
for m in multi:
    print("  item=%d cat=%s n=%d tokens=%s val=%r" %
          (m[0], m[1], m[2], m[4], m[3][:80]))

# ---- projection per profile ----
projs = {}
for name in prof:
    t = raw
    rem = {}
    for tok in ORDER:
        rem["__%s__" % tok] = t.count("__%s__" % tok)
        t = t.replace("__%s__" % tok, prof[name]["values"][tok])
    pd = json.loads(t)
    projs[name] = (t, pd, rem)
    print("PROFILE", name, "replacement_counts", rem, "parsed", len(pd),
          "test_json_digest", sha(t),
          "remaining_tokens",
          {tok: t.count(tok) for tok in TOKENS},
          "wikipedia_string_present", "wikipedia.invalid" in t)

# item 7 description
item7 = data[7]
leaf7 = [(norm(p), v) for p, st, en, v in leaves if p[0] == 7]
print("ITEM7 leaf_count", len(leaf7))
print("ITEM7 diff-paths vs raw are only token leaves:")
t7_off = None
for p, st, en, v in leaves:
    if p[0] == 7 and "__MAP__" in v:
        t7_off = raw.index("__MAP__", st)
        print("ITEM7_LEAF", norm(p), "value_span", (st, en),
              "value_len", en - st, "token_offset_codepoints", t7_off,
              "token_offset_bytes", len(raw[:t7_off].encode("utf-8")))
print("ITEM7_KEYS", list(item7))

# changed-leaf set equality across profiles + distribution
def walk(a, b, path=(), out=None):
    if out is None:
        out = []
    if type(a) is not type(b):
        out.append((path, a, b))
        return out
    if isinstance(a, dict):
        for k in a:
            walk(a[k], b[k], path + (k,), out)
    elif isinstance(a, list):
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, path + (i,), out)
    else:
        if a != b:
            out.append((path, a, b))
    return out


sets = {}
for name in prof:
    t, pd, rem = projs[name]
    ds = []
    dist = collections.Counter()
    for i in range(812):
        d = walk(data[i], pd[i])
        dist[len(d)] += 1
        ds += [(i,) + p for p, a, b in d]
    sets[name] = set(ds)
    print("PROFILE", name, "changed_leaves", len(ds),
          "items_with_diff", 812 - dist[0],
          "leaves_per_item_hist", dict(sorted(dist.items())))
    assert len(ds) == len(sets[name])
print("CHANGED_PATH_SETS_IDENTICAL_ACROSS_PROFILES",
      sets["distinct_origins"] == sets["path_prefix"] == sets["trailing_slash_sensitivity"])

# per-profile item-7 old->new + artifact bytes + projected-slice equality
for name in prof:
    t, pd, rem = projs[name]
    it = pd[7]
    d = walk(item7, it)
    per = json.dumps(it, indent=2)
    # projected test.json item slice: locate via raw_decode on projected text
    dec = json.JSONDecoder()
    pos = t.index("[") + 1
    idx = 0
    while True:
        while t[pos] in ", \t\r\n":
            pos += 1
        if t[pos] == "]":
            break
        obj, e = dec.raw_decode(t, pos)
        if idx == 7:
            frag = t[pos:e]
            break
        idx += 1
        pos = e
    plines = per.split("\n")
    nested = "\n".join([plines[0]] + ["  " + ln for ln in plines[1:]])
    # projected codepoint offset of the substituted item-7 value
    pleaves = []
    S(t).parse(0, (), pleaves)
    _, pst, pen, pval = [x for x in pleaves if x[0][0] == 7 and x[0][1] == "start_url"][0]
    delta = 0
    for tok in ORDER:
        token = "__%s__" % tok
        val = prof[name]["values"][tok]
        pos = raw.find(token)
        while pos != -1 and pos < 6238:
            delta += len(val) - len(token)
            pos = raw.find(token, pos + len(token))
    print("ITEM7_PROJ", name,
          "diff", [(norm(p), a, b) for p, a, b in d],
          "per_task_bytes", len(per.encode()), "per_task_sha", sha(per),
          "test_slice_reindent_equals_per_task", frag == nested,
          "test_slice_len", len(frag),
          "projected_value_span", (pst, pen),
          "projected_value_cp_offset", pst + 1,
          "predicted_offset", 6238 + delta,
          "earlier_delta", delta,
          "eval_equal", it["eval"] == item7["eval"])

# ordinal/id witness
print("ORDINAL_FROZEN", [(i, it["task_id"]) for i, it in enumerate(data[:9])])
w = [{"task_id": 9}, {"task_id": 3}]
print("ORDINAL_SHUFFLED_WITNESS",
      [(i, it["task_id"], "config_files/%d.json" % i) for i, it in enumerate(w)])

# ---- independent decoded-leaf oracle vs serialized-text replacement ----
def rewrite(o, vals):
    if isinstance(o, dict):
        return {k: rewrite(v, vals) for k, v in o.items()}
    if isinstance(o, list):
        return [rewrite(v, vals) for v in o]
    if isinstance(o, str):
        for tok in ORDER:
            o = o.replace("__%s__" % tok, vals[tok])
        return o
    return o


for name in prof:
    t, pd, rem = projs[name]
    leaf_pd = rewrite(data, prof[name]["values"])
    ds = [p for i in range(812) for p in walk(data[i], leaf_pd[i])]
    print("ORACLE", name, "text_equals_leaf_rewrite", pd == leaf_pd,
          "leaf_changed", len(ds),
          "remaining_tokens", {tok: json.dumps(leaf_pd).count(tok) for tok in TOKENS})

# ---- URL decomposition of the three item-7 substitutes ----
from urllib.parse import urlsplit
for name in prof:
    v = prof[name]["values"]["MAP"]
    u = urlsplit(v)
    print("PROFILE_VALUE", name, "value", v, "len", len(v),
          "scheme", u.scheme, "netloc", u.netloc, "port", u.port,
          "path", repr(u.path), "query", repr(u.query), "fragment", repr(u.fragment))

# ---- serialized-text boundary for values containing JSON-significant chars ----
for label, val in [("quote", 'http://map.invalid:10106/pa"th'),
                   ("backslash_t", "http://map.invalid:10106/pa\\th"),
                   ("trailing_backslash", "http://map.invalid:10106/pa\\")]:
    try:
        got = json.loads(raw.replace("__MAP__", val))[7]["start_url"]
        print("BOUNDARY", label, "PARSED", repr(got), "contains_tab", "\t" in got)
    except json.JSONDecodeError as e:
        print("BOUNDARY", label, "JSONDecodeError", e.msg, "pos", e.pos,
              "line", e.lineno, "col", e.colno)
print("PROFILE_CHARSET",
      sorted({c for p in prof.values() for v in p["values"].values() for c in v}))
print("PROFILE_FORBIDDEN_CHARS",
      sorted({c for p in prof.values() for v in p["values"].values() for c in v}
             & set('"\\ \t\n|<>{}')))

# ---- item-7 static field-role table (pending runtime) ----
READS = {
    "eval.eval_types": "evaluators.py:361",
    "eval.reference_answers": "evaluators.py:137",
    "eval.string_note": "evaluators.py:161 (fuzzy N/A only)",
    "eval.reference_url": "evaluators.py:213 (url_match only)",
    "eval.program_html": "evaluators.py:258 (program_html only)",
    "intent": "evaluators.py:151,168 (fuzzy only)",
}
for k, v in item7.items():
    read = READS.get(k)
    if k == "eval":
        read = "subfields at evaluators.py:137,161,213,258,361"
    elif read is None:
        read = "not in pinned harness"
    print("ITEM7_FIELD", k, "type", type(v).__name__,
          "tokens", sum(json.dumps(v).count(t) for t in TOKENS),
          "evaluator_read", read)
print("ITEM7_TOKEN_LEAVES", [(norm(p), v) for p, st, en, v in leaves
                             if p[0] == 7 and any(t in v for t in TOKENS)])


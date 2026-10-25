"""Independent census for raw task index/id 7 under the six sequential global
text replacements of scripts/generate_test_data.py.

Reads pinned bytes once; no upstream import/exec; no network; no writes outside stdout.
Offsets are Unicode codepoint indices into the decoded serialized raw text.
"""
import hashlib
import json
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = ROOT + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
GEN = ROOT + "/plans/fixtures/r29/generate_test_data.py"
PROF = ROOT + "/plans/fixtures/r29/profiles.json"
MAN = ROOT + "/plans/fixtures/r29/manifest.json"

TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__",
          "__WIKIPEDIA__", "__MAP__"]
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read_once(path):
    with open(path, "rb") as f:
        return f.read()


raw_b = read_once(RAW)
gen_b = read_once(GEN)
prof_b = read_once(PROF)
man_b = read_once(MAN)
print("PIN raw sha256", sha(raw_b), "bytes", len(raw_b))
print("PIN generator sha256", sha(gen_b), "bytes", len(gen_b))
print("PIN profiles sha256", sha(prof_b), "bytes", len(prof_b))
print("PIN manifest sha256", sha(man_b), "bytes", len(man_b))

raw = raw_b.decode("utf-8", errors="strict")
print("ENC ascii_only", all(ord(c) < 128 for c in raw),
      "bytes_eq_codepoints", len(raw.encode("utf-8")) == len(raw))

data = json.loads(raw)
assert isinstance(data, list) and len(data) == 812, len(data)
ids = [it["task_id"] for it in data]
print("TASKS", len(data), "distinct_ids", len(set(ids)))
print("INDEX_EQ_TASK_ID", all(i == v for i, v in enumerate(ids)),
      "mismatches", [(i, v) for i, v in enumerate(ids) if i != v][:10])


# ---------- positional scanner: string leaves with paths and spans ----------
class Scanner:
    def __init__(self, s):
        self.s = s
        self.n = len(s)

    def ws(self, i):
        s, n = self.s, self.n
        while i < n and s[i] in " \t\r\n":
            i += 1
        return i

    def parse(self, i, path, out):
        """Returns index after value. Appends (path, start, end, value) for strings."""
        s = self.s
        i = self.ws(i)
        c = s[i]
        if c == '"':
            start = i
            val, end = json.decoder.scanstring(s, i + 1)
            out.append((path, start, end, val))
            return end
        if c == "{":
            i = self.ws(i + 1)
            if s[i] == "}":
                return i + 1
            while True:
                i = self.ws(i)
                assert s[i] == '"', (i, s[i:i + 20])
                key, i = json.decoder.scanstring(s, i + 1)
                i = self.ws(i)
                assert s[i] == ":", (i, s[i:i + 20])
                i = self.parse(i + 1, path + (key,), out)
                i = self.ws(i)
                if s[i] == ",":
                    i += 1
                    continue
                assert s[i] == "}", (i, s[i:i + 20])
                return i + 1
        if c == "[":
            i = self.ws(i + 1)
            if s[i] == "]":
                return i + 1
            k = 0
            while True:
                i = self.parse(i, path + (k,), out)
                k += 1
                i = self.ws(i)
                if s[i] == ",":
                    i += 1
                    continue
                assert s[i] == "]", (i, s[i:i + 20])
                return i + 1
        if s.startswith("true", i):
            return i + 4
        if s.startswith("false", i):
            return i + 5
        if s.startswith("null", i):
            return i + 4
        j = i
        while j < self.n and s[j] in "-+0123456789.eE":
            j += 1
        assert j > i
        return j


sc = Scanner(raw)
leaves = []
end = sc.parse(0, (), leaves)
assert sc.ws(end) == len(raw), (end, len(raw))
print("SCANNER leaves", len(leaves))

# Validate scanner values/positions against stdlib parse.
for path, start, end_, val in leaves:
    obj = data
    for p in path:
        obj = obj[p]
    assert obj == val, (path, obj, val)
    assert raw[start] == '"' and raw[end_ - 1] == '"', (path, start, end_)
print("SCANNER_VALUE_AGREEMENT OK")


def fmt_path(path):
    out = ""
    for p in path:
        if isinstance(p, int):
            out += "[%d]" % p
        else:
            out += ("." if out else "") + p
    return out


# ---------- occurrence census on serialized raw text ----------
occ = []
for tok in TOKENS:
    idxs = []
    pos = raw.find(tok)
    while pos != -1:
        idxs.append(pos)
        pos = raw.find(tok, pos + len(tok))
    occ.append((tok, idxs))
    print("OCC", tok, len(idxs))

leaf_by_span = leaves


def locate(off):
    for path, start, end_, val in leaf_by_span:
        if start <= off and off + 4 <= end_:
            # narrow: full token within this leaf
            pass
        if start <= off < end_:
            return path, start, end_, val
    return None


tok_stats = {}
for tok, idxs in occ:
    paths = []
    for off in idxs:
        hit = locate(off)
        assert hit is not None, (tok, off)
        path, start, end_, val = hit
        assert val.find(tok) != -1
        assert raw[off:off + len(tok)] == tok
        assert off - start == val.rfind(tok) or val.count(tok) >= 1
        paths.append((path, off - start, val))
    tok_stats[tok] = paths
    items = {p[0][1] for p in paths}
    leaves_hit = {(p[0][:2]) for p in paths}
    print("TOK", tok, "occ", len(paths), "leaves", len({p[0] for p in paths}),
          "items", len(items))

# token substring relations
for a in TOKENS:
    for b in TOKENS:
        if a != b and a in b:
            print("SUBSTRING", a, "in", b)
print("TOKEN_SUBSTRING_PAIRS done")

# ---------- task 7 leaf census ----------
item7 = data[7]
print("ITEM7 task_id", item7["task_id"], "sites", item7["sites"],
      "start_url", item7["start_url"], "eval_types", item7["eval"]["eval_types"])
print("ITEM7_EVAL", json.dumps(item7["eval"], ensure_ascii=False))
tok_leaves7 = [(fmt_path(p), start, end_, val) for (p, start, end_, val) in leaves
               if p[0] == 7 and any(t in val for t in TOKENS)]
print("ITEM7_TOKEN_LEAVES", [(p, v) for p, _, _, v in tok_leaves7])
print("ITEM7_TOKEN_OCC",
      [(fmt_path(p), raw[start:end].count(tok), tok)
       for (p, start, end_, val) in leaves
       for tok in TOKENS
       if p[0] == 7 and tok in val])
# also raw-text offsets for each occurrence in item 7
item7_offsets = [(tok, off) for tok, idxs in occ for off in idxs
                 if locate(off)[0][0] == 7]
print("ITEM7_OCC_OFFSETS", item7_offsets)

# ---------- replacement execution ----------
prof = json.loads(prof_b.decode("utf-8"))
profile_names = list(prof.keys())
print("PROFILES", profile_names)
expected = {
    "distinct_origins": {"GITLAB": "http://gitlab.invalid:10101",
                          "REDDIT": "http://reddit.invalid:10102",
                          "SHOPPING": "http://shopping.invalid:10103",
                          "SHOPPING_ADMIN": "http://shopping-admin.invalid:10104",
                          "WIKIPEDIA": "http://wikipedia.invalid:10105",
                          "MAP": "http://map.invalid:10106"},
}
for name in profile_names:
    vals = prof[name]["values"]
    print("PROFILE", name, "keys", sorted(vals))
    assert sorted(vals) == sorted(ORDER), (name, sorted(vals))


def walk_diff(a, b, path=(), out=None):
    if out is None:
        out = []
    if type(a) is not type(b):
        out.append((fmt_path(path), a, b, "type"))
        return out
    if isinstance(a, dict):
        assert set(a) == set(b), (path, set(a) ^ set(b))
        for k in a:
            walk_diff(a[k], b[k], path + (k,), out)
    elif isinstance(a, list):
        assert len(a) == len(b), (path, len(a), len(b))
        for i, (x, y) in enumerate(zip(a, b)):
            walk_diff(x, y, path + (i,), out)
    else:
        if a != b:
            out.append((fmt_path(path), a, b, "value"))
    return out


projected = {}
for name in profile_names:
    text = raw
    counts = {}
    for tok in ORDER:
        counts[tok] = text.count("__%s__" % tok)
        text = text.replace("__%s__" % tok, prof[name]["values"][tok])
    art = text.encode("utf-8")
    pdata = json.loads(text)
    projected[name] = (text, art, pdata, counts)
    print("PROJ", name, "counts", counts, "parsed", len(pdata),
          "ids_distinct", len({x["task_id"] for x in pdata}),
          "digest", sha(art))

# Verify per-profile diff for item 7 against token-leaf census.
for name in profile_names:
    text, art, pdata, counts = projected[name]
    d7 = walk_diff(item7, pdata[7])
    print("ITEM7_DIFF", name, json.dumps(d7, ensure_ascii=False))
    # every diff path must be a token-containing leaf path in the original
    for path, old, new, kind in d7:
        assert path == "start_url", path
        assert old == "__MAP__", old
    # per-task artifact bytes as upstream json.dump(item, f, indent=2) (ensure_ascii default True)
    per = json.dumps(pdata[7], indent=2)
    print("PER_TASK", name, "filename", "config_files/7.json",
          "bytes", len(per.encode("utf-8")), "sha256", sha(per.encode("utf-8")),
          "new_start_url", pdata[7]["start_url"])
    print("PER_TASK_EVAL_UNCHANGED", name,
          pdata[7]["eval"] == item7["eval"])

# Same instrumented replacement but with WIKIPEDIA substitute absent check: values contain no tokens
for name in profile_names:
    for k in ORDER:
        v = prof[name]["values"][k]
        assert not any(tok in v for tok in TOKENS), (name, k, v)
print("VALUES_CONTAIN_NO_TOKENS OK")

# Whole-population changed-leaf counts vs occurrence counts.
for name in profile_names:
    text, art, pdata, counts = projected[name]
    tot_diff = 0
    items_changed = 0
    for i, (a, b) in enumerate(zip(data, pdata)):
        d = walk_diff(a, b)
        if d:
            items_changed += 1
            tot_diff += len(d)
    print("PROJ_DIFF", name, "changed_leaves", tot_diff,
          "items_changed", items_changed)

# ---------- ordinal vs id witness (our own data, no upstream import) ----------
witness = [{"task_id": 9}, {"task_id": 3}]
print("ORDINAL_WITNESS",
      [(idx, item["task_id"], "config_files/%d.json" % idx)
       for idx, item in enumerate(witness)])

# ---------- task 7 field-role classification (static from this item + frozen harness) ----------
print("ITEM7_KEYS", list(item7.keys()))
print("ITEM7_URL_FIELDS", {
    "start_url": item7["start_url"],
    "eval.reference_url": item7["eval"]["reference_url"],
    "eval.program_html": item7["eval"]["program_html"],
})
print("ITEM7_CONSUMED_BY_DECLARED_EVAL",
      {"eval_types": item7["eval"]["eval_types"],
       "reference_answers.exact_match": item7["eval"]["reference_answers"]["exact_match"]})
print("ITEM7_METADATA_KEYS",
      ["sites", "task_id", "require_login", "storage_state", "start_url",
       "geolocation", "intent_template", "instantiation_dict", "intent",
       "require_reset", "eval", "intent_template_id"])

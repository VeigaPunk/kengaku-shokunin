#!/usr/bin/env python3
"""Independent oracle case for pinned WebArena generated-config projection,
raw task_id 389. Reads pinned bytes once; parses the pinned generator source as
inert text (AST, no import/exec). Never writes config_files outputs."""
import ast
import hashlib
import json
import re
import sys
from bisect import bisect_right

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = ROOT + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
GEN = ROOT + "/plans/fixtures/r29/generate_test_data.py"
MAN = ROOT + "/plans/fixtures/r29/manifest.json"
PROF = ROOT + "/plans/fixtures/r29/profiles.json"
EXPECT = {
    MAN: "f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87",
    GEN: "45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd",
    RAW: "7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652",
    PROF: "90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018",
}
TOKENS = ["__GITLAB__", "__REDDIT__", "__SHOPPING__", "__SHOPPING_ADMIN__",
          "__WIKIPEDIA__", "__MAP__"]
VAR = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read_once(path):
    with open(path, "rb") as f:
        return f.read()


bytes_by_path = {}
sha_by_path = {}
for p in (MAN, GEN, RAW, PROF):
    b = read_once(p)
    bytes_by_path[p] = b
    sha_by_path[p] = sha(b)
    assert sha_by_path[p] == EXPECT[p], ("pin mismatch", p, sha_by_path[p])
man = json.loads(bytes_by_path[MAN])
profiles = json.loads(bytes_by_path[PROF])
src = bytes_by_path[GEN].decode("utf-8")
raw_bytes = bytes_by_path[RAW]
text = raw_bytes.decode("utf-8")
assert text.encode("utf-8") == raw_bytes

# ---- generator source contract from inert AST ----
tree_src = ast.parse(src)
facts = {}
replaces = []
for node in ast.walk(tree_src):
    if isinstance(node, ast.ImportFrom):
        facts.setdefault("imports", []).append(
            (node.module, [a.name for a in node.names], node.lineno))
    if isinstance(node, ast.Call):
        f = node.func
        if isinstance(f, ast.Attribute) and f.attr == "replace":
            args = node.args
            if (len(args) == 2 and isinstance(args[0], ast.Constant)
                    and isinstance(args[1], ast.Name)):
                replaces.append((args[0].value, args[1].id, node.lineno))
        if isinstance(f, ast.Attribute) and f.attr in ("read", "write", "loads", "dump", "open"):
            facts.setdefault("calls", []).append((f.attr, node.lineno))
        if isinstance(f, ast.Name) and f.id == "open":
            facts.setdefault("calls", []).append(("open", node.lineno))
        if isinstance(f, ast.Name) and f.id == "enumerate":
            facts.setdefault("calls", []).append(("enumerate", node.lineno))
        if isinstance(f, ast.Name) and f.id == "main":
            facts.setdefault("calls", []).append(("main", node.lineno))
src_tokens = [r[0] for r in replaces]
src_vars = [r[1] for r in replaces]
src_lines = [r[2] for r in replaces]
assert src_tokens == TOKENS, src_tokens
assert src_vars == VAR, src_vars
assert man["replacement_order"] == [t.strip("_") for t in TOKENS]
assert man["upstream_revision"] == "dce04686a56253aefba7b18a4fa0937cf1dc987b"
assert man["base_revision"] == "ed26bdf5d924755697cd6812129be2fa441c42a3"
for rel in ("plans/fixtures/r29/generate_test_data.py",
            "plans/fixtures/r28/webarena/config_files/test.raw.json",
            "plans/fixtures/r29/profiles.json"):
    assert man["files"][rel]["sha256"] == sha_by_path[ROOT + "/" + rel], rel
assert sorted(p for p in profiles) == ["distinct_origins", "path_prefix",
                                       "trailing_slash_sensitivity"]
assert sorted(man["files"]) == sorted(["plans/fixtures/r29/generate_test_data.py",
                                       "plans/fixtures/r28/webarena/config_files/test.raw.json",
                                       "plans/fixtures/r29/profiles.json"])

# ---- profile validation (synthetic fixtures) ----
for name, rec in profiles.items():
    assert set(rec["values"]) == set(VAR), name
    vals = rec["values"]
    for v in vals.values():
        assert isinstance(v, str) and "://" in v
        assert not any(t in v for t in TOKENS)
        assert not any(c in v for c in '"\\\n\r\t') and v.isascii(), (name, v)
    assert "not an observed deployment" in rec["purpose"]
assert len({tuple(profiles[p]["values"][v] for v in VAR)
            for p in profiles}) == 3
assert all(profiles["distinct_origins"]["values"][v] !=
           profiles["path_prefix"]["values"][v] for v in VAR)
assert all(not profiles["path_prefix"]["values"][v].endswith("/") for v in VAR)
assert all(profiles["trailing_slash_sensitivity"]["values"][v].endswith("/")
           for v in VAR)

# ---- raw artifact facts ----
raw_ascii = all(c < 128 for c in raw_bytes)
cr = raw_bytes.count(b"\r")
assert cr == 0
orig = json.loads(text)
assert isinstance(orig, list) and len(orig) == 812
ids = [it["task_id"] for it in orig]
assert ids == list(range(812)) and len(set(ids)) == 812
assert all(isinstance(it["task_id"], int) and not isinstance(it["task_id"], bool)
           for it in orig)

# ---- position-tracking JSON parser over the retained text ----
NUM = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?")


class PosParser:
    def __init__(self, s):
        self.s = s
        self.i = 0
        self.nodes = []      # (start, end, path, value, raw)
        self.key_nodes = []  # (start, end, key)

    def ws(self):
        while self.i < len(self.s) and self.s[self.i] in " \t\n\r":
            self.i += 1

    def string(self, path, is_key=False):
        start = self.i
        assert self.s[self.i] == '"'
        self.i += 1
        while True:
            c = self.s[self.i]
            if c == "\\":
                self.i += 2
                continue
            if c == '"':
                self.i += 1
                break
            self.i += 1
        raw = self.s[start:self.i]
        val = json.loads(raw)
        if is_key:
            self.key_nodes.append((start, self.i, val))
        else:
            self.nodes.append((start, self.i, path, val, raw))
        return val

    def value(self, path):
        self.ws()
        c = self.s[self.i]
        if c == '"':
            return self.string(path)
        if c == "{":
            self.i += 1
            obj = {}
            self.ws()
            if self.s[self.i] == "}":
                self.i += 1
                return obj
            while True:
                self.ws()
                k = self.string(None, is_key=True)
                self.ws()
                assert self.s[self.i] == ":"
                self.i += 1
                obj[k] = self.value(path + (k,))
                self.ws()
                if self.s[self.i] == ",":
                    self.i += 1
                    continue
                assert self.s[self.i] == "}"
                self.i += 1
                return obj
        if c == "[":
            self.i += 1
            arr = []
            self.ws()
            if self.s[self.i] == "]":
                self.i += 1
                return arr
            n = 0
            while True:
                arr.append(self.value(path + (n,)))
                n += 1
                self.ws()
                if self.s[self.i] == ",":
                    self.i += 1
                    continue
                assert self.s[self.i] == "]"
                self.i += 1
                return arr
        for lit, v in (("true", True), ("false", False), ("null", None)):
            if self.s.startswith(lit, self.i):
                self.i += len(lit)
                return v
        m = NUM.match(self.s, self.i)
        assert m, self.i
        self.i = m.end()
        return json.loads(m.group(0))


pp = PosParser(text)
parsed_tree = pp.value(())
pp.ws()
assert pp.i == len(text)
assert parsed_tree == orig, "position parser disagrees with json.loads"
assert not any(any(t in k for t in TOKENS) for _, _, k in pp.key_nodes)


def jp(path):
    out = "$"
    for p in path:
        if isinstance(p, int):
            out += "[%d]" % p
        elif re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", p):
            out += "." + p
        else:
            out += "[" + json.dumps(p) + "]"
    return out


def pat(path):
    out = "$"
    for p in path:
        if isinstance(p, int):
            out += "[]"
        elif re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", p):
            out += "." + p
        else:
            out += "[" + json.dumps(p) + "]"
    return out


def leaves(t, path=()):
    if isinstance(t, dict):
        for k, v in t.items():
            yield from leaves(v, path + (k,))
    elif isinstance(t, list):
        for i, v in enumerate(t):
            yield from leaves(v, path + (i,))
    else:
        yield path, t


def diff(a, b, path=()):
    if type(a) is not type(b):
        yield path, a, b
    elif isinstance(a, dict):
        assert list(a) == list(b), ("key order/shape", path)
        for k in a:
            yield from diff(a[k], b[k], path + (k,))
    elif isinstance(a, list):
        assert len(a) == len(b), ("length", path)
        for i, (x, y) in enumerate(zip(a, b)):
            yield from diff(x, y, path + (i,))
    else:
        if a != b:
            yield path, a, b


# ---- occurrence census from string nodes, codepoint offsets ----
occ = []  # (doc_offset, token, path, terminal)
for start, end, path, val, rawslice in pp.nodes:
    for tok in TOKENS:
        pos = rawslice.find(tok)
        while pos != -1:
            occ.append((start + pos, tok, path, path[-1] if path else None))
            pos = rawslice.find(tok, pos + len(tok))
occ.sort()
occ_by_token = {t: 0 for t in TOKENS}
for _, t, _, _ in occ:
    occ_by_token[t] += 1
for tok in TOKENS:
    assert occ_by_token[tok] == text.count(tok), (tok, occ_by_token[tok],
                                                  text.count(tok))

idx_task = {i: (it["task_id"], tuple(it["sites"])) for i, it in enumerate(orig)}
glob_fields = {}
for off, tok, path, term in occ:
    p = pat(path)
    glob_fields[(p, term, tok)] = glob_fields.get((p, term, tok), 0) + 1
pattern_totals = {}
terminal_totals = {}
pattern_tokens = {}
pattern_leafcounts = {}
pattern_taskcounts = {}
for (p, term, tok), n in glob_fields.items():
    pattern_totals[p] = pattern_totals.get(p, 0) + n
    terminal_totals[term] = terminal_totals.get(term, 0) + n
    key = (p, tok)
    pattern_tokens[key] = pattern_tokens.get(key, 0) + n

# leaf-level occurrence multiplicity and per-pattern leaf/task counts
leaf_occ = {}
leaf_tasks = {}
for off, tok, path, term in occ:
    leaf_occ[path] = leaf_occ.get(path, 0) + 1
    leaf_tasks.setdefault(pat(path), set()).add(path[0])
multi_occ_leaves = {jp(k): v for k, v in leaf_occ.items() if v > 1}
for path, n in leaf_occ.items():
    p = pat(path)
    pattern_leafcounts[p] = pattern_leafcounts.get(p, 0) + 1
pattern_taskcounts = {p: len(s) for p, s in leaf_tasks.items()}
tasks_with_occ = sorted({path[0] for _, _, path, _ in occ})

# ---- projection, exactly six serialized replacements in order ----
def project(s, vals):
    trace = []
    for tok, var in zip(TOKENS, VAR):
        before = s.count(tok)
        s = s.replace(tok, vals[var])
        assert s.count(tok) == 0  # values carry no token
        trace.append((tok, before))
    return s, trace


out = {}
per_profile = {}
item389_original = orig[389]
item389_leaf_count = len(list(leaves(item389_original)))
orig_item_dump = json.dumps(item389_original, indent=2).encode("utf-8")
print("item389 leaves", item389_leaf_count, "original dump sha", sha(orig_item_dump))
expected_leaf_mode = None
for name in sorted(profiles):
    vals = profiles[name]["values"]
    ptext, trace = project(text, vals)
    deltas = {t: len(vals[v]) - len(t) for t, v in zip(TOKENS, VAR)}
    expected_len = len(text) + sum(occ_by_token[t] * deltas[t] for t in TOKENS)
    assert len(ptext) == expected_len, (len(ptext), expected_len)
    print("length delta", len(ptext) - len(text), "per-occurrence deltas", deltas,
          "occurrences", occ_by_token)
    pobj = json.loads(ptext)
    assert pobj != orig
    assert len(pobj) == 812
    assert [it["task_id"] for it in pobj] == ids
    # exhaustive structural + leaf diff
    changes = list(diff(orig, pobj))
    # every changed leaf must have had a token in its original value
    for path, old, new in changes:
        assert isinstance(old, str) and any(t in old for t in TOKENS), path
        assert isinstance(new, str)
    # every string leaf containing a token must have changed
    orig_leaves = dict(leaves(orig))
    for path, val in orig_leaves.items():
        if isinstance(val, str) and any(t in val for t in TOKENS):
            assert path in {p for p, _, _ in changes}, path
    # decoded-leaf oracle: apply the same six replacements to leaf values
    def rewrite(t):
        if isinstance(t, dict):
            return {k: rewrite(v) for k, v in t.items()}
        if isinstance(t, list):
            return [rewrite(v) for v in t]
        if isinstance(t, str):
            v = t
            for tok, var in zip(TOKENS, VAR):
                v = v.replace(tok, vals[var])
            return v
        return t
    leaf_mode = rewrite(orig)
    leaf_equiv = leaf_mode == pobj
    # item 389
    i389 = [p for p, _, _ in changes if p[:1] == (389,)]
    item_changes = []
    for path in i389:
        old = orig
        new = pobj
        for p in path:
            old = old[p]
            new = new[p]
        item_changes.append((jp(path), old, new))
    item_changes.sort()
    # every token occurrence inside item 389 string nodes, codepoint offsets
    item_occ = []
    for start, end, path, val, rawslice in pp.nodes:
        if path[:1] != (389,):
            continue
        for tok in TOKENS:
            pos = rawslice.find(tok)
            while pos != -1:
                item_occ.append((start + pos, tok, jp(path), path[-1],
                                 rawslice[1:-1]))
                pos = rawslice.find(tok, pos + len(tok))
    item_occ.sort()
    rem = {t: ptext.count(t) for t in TOKENS}
    assert sum(rem.values()) == 0
    psha = sha(ptext.encode("utf-8"))
    item_dump = json.dumps(pobj[389], indent=2).encode("utf-8")
    canon = json.dumps(pobj[389], sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True).encode("utf-8")
    per_profile[name] = {
        "replacement_trace": trace,
        "projected_text_sha256": psha,
        "projected_text_codepoints": len(ptext),
        "parsed_tasks": len(pobj),
        "structure": "identical (key order and array lengths)",
        "changed_leaves_total": len(changes),
        "changed_tasks": len({p[0] for p, _, _ in changes}),
        "changed_leaf_patterns": sorted({pat(p) for p, _, _ in changes}),
        "remaining_known_placeholders": rem,
        "item389_changed": item_changes,
        "item389_occurrences": item_occ,
        "item389_projected_object": pobj[389],
        "item389_upstream_dump_indent2_sha256": sha(item_dump),
        "item389_canonical_sha256": sha(canon),
        "leaf_oracle_equivalent": leaf_equiv,
        "ordinal_index_of_task_id_389": [i for i, it in enumerate(pobj)
                                         if it["task_id"] == 389],
        "task_id_at_ordinal_389": pobj[389]["task_id"],
        "index_equals_task_id_all": all(it["task_id"] == i
                                        for i, it in enumerate(pobj)),
    }
    print("== profile", name)
    print("trace", trace)
    print("text sha", psha, "len", len(ptext))
    print("changed leaves", len(changes), "changed tasks",
          len({p[0] for p, _, _ in changes}), "leaf-oracle-equal", leaf_equiv)
    print("patterns", sorted({pat(p) for p, _, _ in changes}))
    for ppath, old, new in item_changes:
        print("389", ppath, "OLD", repr(old), "NEW", repr(new))
    for off, tok, jpath, term, frag in item_occ:
        print("389-occ", tok, "cp", off, "line", text.count("\n", 0, off) + 1,
              jpath, "frag", repr(frag))
    print("item389 dump sha", sha(item_dump))
    print("ordinal of task_id389", per_profile[name]["ordinal_index_of_task_id_389"],
          "task_id at ordinal389", per_profile[name]["task_id_at_ordinal_389"])
    # non-locator content leaves changed (exclude pure URL/locator patterns)
    loc_pat = {"$[].start_url", "$[].eval.program_html[].url",
               "$[].eval.reference_url"}
    nonloc = [(jp(p), old, new) for p, old, new in changes
              if pat(p) not in loc_pat]
    nonloc.sort()
    loc_changed = len(changes) - len(nonloc)
    print("locator changed leaves", loc_changed,
          "content changed leaves", len(nonloc))
    for ppath, old, new in nonloc[:4]:
        print("nonloc", ppath, "OLD", repr(old), "NEW", repr(new))
    for p, old, new in changes:
        if jp(p) == "$[66].eval.reference_answer_raw_annotation":
            print("raw-annotation $[66] OLD", repr(old), "NEW", repr(new))

print("== GLOBAL RAW OCCURRENCE CENSUS (codepoint offsets)")
print("occurrences_by_token", occ_by_token, "total", len(occ))
print("tasks_with_occurrence", len(tasks_with_occ), "of", len(orig))
for p in sorted(pattern_totals):
    print("pattern", p, "occurrences", pattern_totals[p],
          "leaves", pattern_leafcounts[p], "tasks", pattern_taskcounts[p],
          "by_token", {t: n for (pp, t), n in sorted(pattern_tokens.items())
                       if pp == p})
print("multi-occurrence leaves", len(multi_occ_leaves), multi_occ_leaves)
print("item389 node spans:")
for start, end, path, val, rawslice in pp.nodes:
    if path[:1] == (389,):
        print(" node", jp(path), "cp_start", start, "cp_end_exclusive", end,
              "raw", repr(rawslice))
for off in (353262, 353887):
    print("slice", off, repr(text[off:off + 10]))
tid_off = text.find('"task_id": 389', 353000)
print("task_id389 literal cp", tid_off, "line", text.count("\n", 0, tid_off) + 1)
print("item389 first node cp", min(s for s, e, p, v, r in pp.nodes
                                   if p[:1] == (389,)))
print("item389 occ lines", [(off, text.count("\n", 0, off) + 1)
                             for off, *_ in item_occ])
resid = sorted(set(re.findall(r"__[A-Z][A-Z_]*__", text)))
print("double-underscore tokens in raw",
      [(t, text.count(t)) for t in resid])
print("pairwise token substring",
      [(a, b) for a in TOKENS for b in TOKENS if a != b and a in b])
i389_last = max(e for s, e, p, v, r in pp.nodes if p[:1] == (389,))
i390_first = min(s for s, e, p, v, r in pp.nodes if p[:1] == (390,))
print("item389 raw line span",
      text.count("\n", 0, min(s for s, e, p, v, r in pp.nodes
                              if p[:1] == (389,))) + 1,
      "to", text.count("\n", 0, i389_last) + 1,
      "next item first node line", text.count("\n", 0, i390_first) + 1)

# cross-profile: same field set, different values
fieldsets = {}
for name, rec in per_profile.items():
    fieldsets[name] = [x[0] for x in rec["item389_changed"]]
assert len({tuple(v) for v in fieldsets.values()}) == 1
print("item389 changed-field set identical across profiles:", fieldsets)

# ---- ordinal vs task_id hand witness (synthetic, in-memory) ----
shuffled_ids = [10, 2, 389]
shuf_doc = [{"task_id": tid, "start_url": "__GITLAB__"} for tid in shuffled_ids]
shuf_text = json.dumps(shuf_doc)
sproj, _ = project(shuf_text, profiles["distinct_origins"]["values"])
sdata = json.loads(sproj)
witness = [(i, it["task_id"], "config_files/%d.json" % i)
           for i, it in enumerate(sdata)]
print("shuffled witness idx/task_id/file:", witness)

# ---- oracle domain boundary hand cases (synthetic, in-memory) ----
def must_fail(label, raw_doc, vals):
    try:
        json.loads(project(raw_doc, vals)[0])
    except json.JSONDecodeError as e:
        print("boundary FAILS-PARSE", label, type(e).__name__, str(e)[:80])
        return
    print("boundary UNEXPECTED-PARSE", label)


must_fail("quote-in-value", '{"start_url": "__GITLAB__"}',
          {"GITLAB": 'http://x/"/', "REDDIT": "", "SHOPPING": "",
           "SHOPPING_ADMIN": "", "WIKIPEDIA": "", "MAP": ""})
bs = {"GITLAB": "C:\\x", "REDDIT": "", "SHOPPING": "", "SHOPPING_ADMIN": "",
      "WIKIPEDIA": "", "MAP": ""}
must_fail("backslash-in-value", '{"start_url": "__GITLAB__"}', bs)
esc = {"GITLAB": "http:\\/\\/x", "REDDIT": "", "SHOPPING": "",
       "SHOPPING_ADMIN": "", "WIKIPEDIA": "", "MAP": ""}
esc_doc = '{"start_url": "__GITLAB__"}'
esc_p = json.loads(project(esc_doc, esc)[0])
print("boundary ESCAPE-DIVERGES inserted", repr(esc["GITLAB"]),
      "decoded", repr(esc_p["start_url"]))
content = {"GITLAB": "http://g.invalid", "REDDIT": "", "SHOPPING": "",
           "SHOPPING_ADMIN": "", "WIKIPEDIA": "", "MAP": ""}
c_doc = '{"intent": "go to __GITLAB__ now"}'
c_p = json.loads(project(c_doc, content)[0])
print("boundary CONTENT-FIELD changed", repr(c_doc), "->", repr(c_p["intent"]))
cascade = {"GITLAB": "http://__MAP__", "REDDIT": "", "SHOPPING": "",
           "SHOPPING_ADMIN": "", "WIKIPEDIA": "", "MAP": "http://map.invalid"}
casc_p = json.loads(project('{"start_url": "__GITLAB__"}', cascade)[0])
print("boundary LATER-CASCADE start_url", repr(casc_p["start_url"]))

# ---- machine summary ----
summary = {
    "pins": {p: sha_by_path[p] for p in sha_by_path},
    "raw_bytes": len(raw_bytes),
    "raw_codepoints": len(text),
    "raw_ascii": raw_ascii,
    "raw_cr": cr,
    "raw_tasks": len(orig),
    "raw_ids_are_range": ids == list(range(812)),
    "occurrences_by_token": occ_by_token,
    "occurrence_total": len(occ),
    "tasks_with_occurrence": len(tasks_with_occ),
    "pattern_totals": pattern_totals,
    "terminal_field_totals": {str(k): v for k, v in terminal_totals.items()},
    "pattern_detail": {p: {"occurrences": pattern_totals[p],
                           "leaves": pattern_leafcounts[p],
                           "tasks": pattern_taskcounts[p],
                           "by_token": {t: n for (pp, t), n in pattern_tokens.items()
                                        if pp == p}}
                       for p in pattern_totals},
    "multi_occurrence_leaves": multi_occ_leaves,
    "item389_original": item389_original,
    "profiles": {n: {k: v for k, v in r.items()
                     if k not in ("item389_projected_object", "item389_occurrences",
                                  "replacement_trace", "item389_changed")}
                 for n, r in per_profile.items()},
    "shuffled_witness": witness,
}
print("== SUMMARY_JSON")
print(json.dumps(summary, indent=1, sort_keys=True))

sys.exit(0)

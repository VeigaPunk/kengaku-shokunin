"""Independent projection oracle for r29 case task_id 424.

Reads pinned bytes ONCE, hashes those retained bytes, applies the six
upstream serialized-text replacements in upstream order, parses, and
reports changed leaves / provenance. Never imports or executes the
upstream generator and never imports production projection code.
"""
import hashlib, json, sys

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = LANE + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF = LANE + "/plans/fixtures/r29/profiles.json"
MAN = LANE + "/plans/fixtures/r29/manifest.json"
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]

def read_once(p):
    b = open(p, "rb").read()
    return b, hashlib.sha256(b).hexdigest(), b.decode("utf-8")

raw_b, raw_sha, raw_t = read_once(RAW)
prof_b, prof_sha, prof_t = read_once(PROF)
man_b, man_sha, man_t = read_once(MAN)
manifest = json.loads(man_t)
profiles = json.loads(prof_t)

print("MANIFEST sha", man_sha, "bytes", len(man_b))
print("RAW sha", raw_sha, "bytes", len(raw_b), "codepoints", len(raw_t),
      "ascii_only", all(ord(c) < 128 for c in raw_t))
print("PROFILES sha", prof_sha, "bytes", len(prof_b), "profiles", sorted(profiles))

# item spans in raw text via raw_decode over the array
dec = json.JSONDecoder()
spans, idx = [], raw_t.index("[") + 1
pos = idx
n = len(raw_t)
while True:
    while pos < n and raw_t[pos] in " \t\r\n,":
        pos += 1
    if pos >= n or raw_t[pos] == "]":
        break
    obj, end = dec.raw_decode(raw_t, pos)
    spans.append((pos, end, obj))
    pos = end
print("parsed_items", len(spans), "ids_distinct", len({o['task_id'] for _,_,o in spans}))
id_to_pos = {o["task_id"]: i for i,(_,_,o) in enumerate(spans)}
print("task_id_424_pos", id_to_pos.get(424), "index_eq_id_all",
      all(o["task_id"] == i for i,(_,_,o) in enumerate(spans)))

def leafwalk(a, b, path=""):
    out = []
    if type(a) is not type(b):
        return [(path, a, b)]
    if isinstance(a, dict):
        for k in a:
            p = f"{path}.{k}" if path else k
            if k not in b:
                out.append((p, a[k], "<absent>"))
            else:
                out += leafwalk(a[k], b[k], p)
        for k in b:
            if k not in a:
                p = f"{path}.{k}" if path else k
                out.append((p, "<absent>", b[k]))
    elif isinstance(a, list):
        if len(a) != len(b):
            return [(path, f"<len {len(a)}>", f"<len {len(b)}>")]
        for i,(x,y) in enumerate(zip(a,b)):
            out += leafwalk(x, y, f"{path}[{i}]")
    elif a != b:
        out.append((path, a, b))
    return out

def occ_in_span(tok, start, end):
    res, p = [], raw_t.find(tok, start, end)
    while p != -1:
        res.append(p)
        p = raw_t.find(tok, p + 1, end)
    return res

summary = {"order": ORDER, "raw": {"sha256": raw_sha, "bytes": len(raw_b),
           "codepoints": len(raw_t), "ascii_only": True}, "profiles": {}}
target_pos = id_to_pos[424]
s0, e0, raw_item = spans[target_pos]

for name in sorted(profiles):
    vals = profiles[name]["values"]
    assert [k for k in profiles[name]["values"]]  # structural
    missing = [t for t in ORDER if t not in vals]
    if missing:
        print("PROFILE", name, "MISSING", missing); continue
    text = raw_t
    per_token = {}
    for tok in ORDER:
        before = text.count("__%s__" % tok)
        text = text.replace("__%s__" % tok, vals[tok])
        per_token[tok] = before
    proj_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    remaining = {("__%s__" % t): text.count("__%s__" % t) for t in ORDER}
    try:
        data = json.loads(text)
        ok = True
    except Exception as exc:
        print("PROFILE", name, "PARSE_FAIL", type(exc).__name__, exc)
        summary["profiles"][name] = {"parse": "fail", "error": type(exc).__name__}
        continue
    item = data[target_pos]
    changed = leafwalk(raw_item, item)
    dump = json.dumps(item, indent=2)
    dump_b = dump.encode("utf-8")
    # does any profile value contain a later/other token (cascade risk)?
    cascade = {t: [u for u,v in vals.items() if ("__%s__" % t) in v] for t in ORDER}
    summary["profiles"][name] = {
        "parse": "ok", "parsed_tasks": len(data),
        "ids_equal_index": all(x["task_id"] == i for i,x in enumerate(data)),
        "projected_text_sha256": proj_sha,
        "projected_text_bytes": len(text.encode("utf-8")),
        "token_replacements": per_token,
        "remaining_tokens": remaining,
        "cascade_value_contains_token": {k:v for k,v in cascade.items() if v},
        "ordinal": target_pos,
        "task_id": item["task_id"],
        "ordinal_equals_task_id": target_pos == item["task_id"],
        "output_filename_upstream": "config_files/%d.json" % target_pos,
        "changed_leaves": [{"path": p, "old": o, "new": nw} for p,o,nw in changed],
        "changed_leaf_count": len(changed),
        "per_task_artifact_sha256": hashlib.sha256(dump_b).hexdigest(),
        "per_task_artifact_bytes": len(dump_b),
    }
    print("\n== PROFILE", name, "==")
    print("token_repl", per_token)
    print("remaining", remaining)
    print("parsed", len(data), "projected_sha", proj_sha)
    print("ordinal", target_pos, "task_id", item["task_id"], "file", "config_files/%d.json" % target_pos)
    print("changed_leaves", json.dumps(changed, ensure_ascii=False))
    print("artifact_sha", summary["profiles"][name]["per_task_artifact_sha256"], "bytes", len(dump_b))

# provenance: codepoint offsets of every token occurrence inside item-424 span
print("\n== ITEM 424 SOURCE SPAN (codepoint offsets in raw text) ==")
print("span", s0, e0, "length", e0 - s0)
for tok in ORDER:
    offs = occ_in_span("__%s__" % tok, s0, e0)
    for o in offs:
        ctx = raw_t[max(s0,o-40):o+len(tok)+2]
        print(tok, "cp_offset", o, "byte_offset", len(raw_t[:o].encode()),
              "ctx", repr(ctx[-60:]))

print("\n== RAW ITEM 424 ==")
print(json.dumps(raw_item, indent=1, ensure_ascii=False))
print("\nJW", json.dumps(summary, ensure_ascii=False))

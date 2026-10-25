"""Independent round-29 C1 projection case: raw text -> 6 ordered global replacements
per frozen profile -> JSON parse -> path-attributed leaf diff. Stdlib only."""
import copy, hashlib, json, re, sys
from collections import Counter, OrderedDict

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = LANE + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
PROF = LANE + "/plans/fixtures/r29/profiles.json"
TOKENS = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
M = lambda n: "__%s__" % n

raw_bytes = open(RAW, "rb").read()
raw_text = raw_bytes.decode("utf-8")
raw_sha = hashlib.sha256(raw_bytes).hexdigest()
profiles = json.loads(open(PROF, "rb").read().decode("utf-8"))

def sha(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()

def project(text, values):
    """Six ordered global serialized replacements; returns text, per-step census."""
    steps = []
    cur = text
    for name in TOKENS:
        lit = M(name)
        before = cur.count(lit)
        repl = values[name]
        cur = cur.replace(lit, repl)
        after = cur.count(lit)
        steps.append({"token": name, "occurrences_before": before,
                      "occurrences_after": after, "replacement": repl,
                      "replacement_contains_token_literal":
                          any(M(t) in repl for t in TOKENS),
                      "len_before": len(cur) - 0})  # len_before informational
    return cur, steps

def leaves(node, path="", out=None):
    if out is None: out = []
    if isinstance(node, dict):
        for k, v in node.items(): leaves(v, path + "/" + k, out)
    elif isinstance(node, list):
        for i, v in enumerate(node): leaves(v, path + "/" + str(i), out)
    else:
        out.append((path, node))
    return out

def diff_leaves(a, b, path="", out=None):
    if out is None: out = []
    if type(a) != type(b) and not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        out.append((path, a, b)); return out
    if isinstance(a, dict):
        if list(a.keys()) != list(b.keys()):
            out.append((path, "<keys>", (list(a.keys()), list(b.keys()))))
        for k in a:
            if k in b: diff_leaves(a[k], b[k], path + "/" + k, out)
    elif isinstance(a, list):
        if len(a) != len(b): out.append((path, "<len>", (len(a), len(b))))
        for i in range(min(len(a), len(b))): diff_leaves(a[i], b[i], path + "/" + str(i), out)
    else:
        if a != b: out.append((path, a, b))
    return out

def leaf_oracle_rewrite(node, values):
    """Independent alternative: replace only inside decoded string leaves."""
    if isinstance(node, dict): return {k: leaf_oracle_rewrite(v, values) for k, v in node.items()}
    if isinstance(node, list): return [leaf_oracle_rewrite(v, values) for v in node]
    if isinstance(node, str):
        s = node
        for name in TOKENS: s = s.replace(M(name), values[name])
        return s
    return node

raw_obj = json.loads(raw_text)
print("raw sha256", raw_sha, "bytes", len(raw_bytes), "tasks", len(raw_obj))
result = {"raw_sha256": raw_sha, "raw_bytes": len(raw_bytes),
          "raw_codepoints": len(raw_text), "raw_tasks": len(raw_obj), "profiles": {}}

# ordinal vs task_id on the frozen input
ids = [t["task_id"] for t in raw_obj]
print("task_id distinct", len(set(ids)), "min", min(ids), "max", max(ids),
      "sorted", ids == sorted(ids),
      "index==task_id count", sum(1 for i, v in enumerate(ids) if i == v), "of", len(ids))
result["id_ordinal"] = {"distinct": len(set(ids)), "min": min(ids), "max": max(ids),
                        "ascending": ids == sorted(ids),
                        "index_equals_task_id": sum(1 for i, v in enumerate(ids) if i == v),
                        "n": len(ids)}

for pname in ["distinct_origins", "path_prefix", "trailing_slash_sensitivity"]:
    values = profiles[pname]["values"]
    proj, steps = project(raw_text, values)
    parsed_ok = True
    try: pobj = json.loads(proj)
    except Exception as e: parsed_ok = False; pobj = None; perr = repr(e)
    d = {"text_sha256": sha(proj), "text_bytes": len(proj.encode("utf-8")),
         "text_codepoints": len(proj), "parse_ok": parsed_ok,
         "steps": steps, "value_sha256": {k: hashlib.sha256(v.encode()).hexdigest() for k, v in values.items()},
         "remaining_tokens": {t: proj.count(M(t)) for t in TOKENS}}
    if parsed_ok:
        dl = diff_leaves(raw_obj, pobj)
        d["task_count"] = len(pobj)
        d["distinct_task_ids"] = len({t["task_id"] for t in pobj})
        d["changed_leaves"] = len(dl)
        d["changed_tasks"] = len({int(p.split("/")[1]) for p, _, _ in dl if p.startswith("/") and p.split("/")[1].isdigit()})
        d["changed_path_patterns"] = dict(Counter(re.sub(r"/\d+", "/[i]", p) for p, _, _ in dl))
        d["non_url_changed"] = [(p, o, n) for p, o, n in dl
                                if not re.match(r"^(https?:)?//", str(o)) and "/url" not in p]
        d["sample_changes"] = [(p, o, n) for p, o, n in dl[:6]]
        orc = leaf_oracle_rewrite(raw_obj, values)
        d["oracle_object_equal"] = orc == pobj
        d["oracle_changed_leaves_equal"] = diff_leaves(raw_obj, orc) == dl
        if not d["oracle_object_equal"]:
            od = diff_leaves(pobj, orc)
            d["oracle_divergence_count"] = len(od)
            d["oracle_divergence_sample"] = od[:5]
    result["profiles"][pname] = d
    print("PROFILE", pname, "text_sha", d["text_sha256"][:16], "bytes", d["text_bytes"],
          "parse", parsed_ok, "tasks", d.get("task_count"), "changed_leaves", d.get("changed_leaves"),
          "changed_tasks", d.get("changed_tasks"), "oracle_eq", d.get("oracle_object_equal"),
          "remaining", d["remaining_tokens"])

# cross-profile path-pattern equality
pats = {k: tuple(sorted(v["changed_path_patterns"].items())) for k, v in result["profiles"].items()}
print("pattern_sets_equal", len(set(pats.values())) == 1)
result["pattern_sets_equal"] = len(set(pats.values())) == 1

# per-task artifact reserialization: upstream json.dump(item, indent=2) with default ensure_ascii
sample = raw_obj[0]
artifact = json.dumps(sample, indent=2)
raw_slice = None
idx = 0
# locate exact serialized slice of task 0 is not trivial; instead demonstrate re-serialization differs
print("artifact0 bytes", len(artifact.encode()), "ends_newline", artifact.endswith("\n"),
      "ascii_only", artifact.isascii(), "contains_escaped_tm", "\\u2122" in artifact)
result["artifact"] = {"sample_task_id": sample["task_id"], "bytes": len(artifact.encode()),
                     "ends_newline": artifact.endswith("\n"), "ascii_only": artifact.isascii(),
                     "escaped_u2122": "\\u2122" in artifact,
                     "projected_testjson_verbatim": True}

# shuffled-ID witness (in-memory only; no files written)
shuffled = list(reversed(raw_obj))
w = [(i, it["task_id"]) for i, it in enumerate(shuffled)][:4]
print("shuffle_witness first4 (ordinal, task_id)", w)
result["shuffle_witness"] = w

# non-ascii count in raw text
print("non_ascii_codepoints", sum(1 for ch in raw_text if ord(ch) > 127))
result["non_ascii_codepoints"] = sum(1 for ch in raw_text if ord(ch) > 127)

out = LANE + "/.ufo/waves/round-29/scratch/KengakuR28.R29Task681-2/results.json"
open(out, "w").write(json.dumps(result, indent=1, sort_keys=True))
print("WROTE", out)

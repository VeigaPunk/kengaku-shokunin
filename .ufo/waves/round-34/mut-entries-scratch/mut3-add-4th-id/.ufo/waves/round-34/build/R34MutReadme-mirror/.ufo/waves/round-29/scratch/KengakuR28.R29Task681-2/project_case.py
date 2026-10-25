"""Independent projection case for round-29 C1 (seat KengakuR28.R29Task681-2).

Reads pinned raw text ONCE, applies the six global serialized replacements in the
frozen order, parses the projected text, and derives a path-attributed diff.
Never imports/executes upstream generator or browser_env.env_config.
"""
import ast, hashlib, json, re, sys

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = LANE + "/plans/fixtures/r28/webarena/config_files/test.raw.json"
GEN = LANE + "/plans/fixtures/r29/generate_test_data.py"
PROF = LANE + "/plans/fixtures/r29/profiles.json"
MAN = LANE + "/plans/fixtures/r29/manifest.json"
TOKENS = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
MARK = lambda n: "__%s__" % n

raw_bytes = open(RAW, "rb").read()
raw_text = raw_bytes.decode("utf-8")
print("RAW bytes", len(raw_bytes), "codepoints", len(raw_text),
      "sha256", hashlib.sha256(raw_bytes).hexdigest())

def walk(node, path, out):
    if isinstance(node, dict):
        for k, v in node.items():
            walk(v, path + "/" + k, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, path + "/" + str(i), out)
    else:
        out.append((path, node))

# --- occurrence -> path attribution (raw) ---
data = json.loads(raw_text)
leaves = []
walk(data, "", leaves)
raw_string_leaves = [(p, v) for p, v in leaves if isinstance(v, str)]
occ_by_path = {}
for p, v in raw_string_leaves:
    for tok in TOKENS:
        c = v.count(MARK(tok))
        if c:
            occ_by_path[p] = occ_by_path.get(p, {})
            occ_by_path[p][tok] = c
leaf_total = {t: sum(d.get(t, 0) for d in occ_by_path.values()) for t in TOKENS}
text_total = {t: raw_text.count(MARK(t)) for t in TOKENS}
print("RAW text occurrence counts", text_total)
print("RAW decoded-leaf occurrence counts", leaf_total)
print("equal(text, leaves)", text_total == leaf_total)
print("tokens in keys", any(MARK(t) in k for _, v in [] for t in TOKENS))
key_hits = [k for item in data for k in item if any(MARK(t) in k for t in TOKENS)]
print("key hits top-level", key_hits[:5], "count", len(key_hits))

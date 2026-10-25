"""Independent cross-checks for the R29 __GITLAB__ token census.

Deliberately separate from census_gitlab.py: re-reads the pinned raw file, re-parses with
json.loads, and compares against the census artifact occurrences.json. No upstream import.
"""

import hashlib
import json
import re
import collections

RAW = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
OCC = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/KengakuR28.R29TokenGitlab-2/occurrences.json"
TOKEN = "__GITLAB__"
PIN = "7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652"
PROFILES = {
    "distinct_origins": "http://gitlab.invalid:10101",
    "path_prefix": "http://gitlab.invalid:10201/prefix",
    "trailing_slash_sensitivity": "http://gitlab.invalid:10301/",
}

raw_bytes = open(RAW, "rb").read()
assert hashlib.sha256(raw_bytes).hexdigest() == PIN
text = raw_bytes.decode("utf-8")
data = json.loads(text)
rows = json.load(open(OCC))

# (a) recursive leaf walk -> pointer occurrence counts
leaf_counts = collections.Counter()


def walk(o, ptr):
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, ptr + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, ptr + "/" + str(i))
    elif isinstance(o, str) and TOKEN in o:
        leaf_counts[ptr] = o.count(TOKEN)


walk(data, "")
scanner_counts = collections.Counter({r["pointer"]: 1 for r in rows})
print("A leaf_walk_occurrences", sum(leaf_counts.values()),
      "leaves", len(leaf_counts), "map_equal", leaf_counts == scanner_counts)
assert len(rows) == len({r["pointer"] for r in rows})  # one occurrence per leaf

# (b) text-level independent attribution: nearest preceding key + task_id ordinal
keyre = re.compile(r'"([A-Za-z_]+)"\s*:')
bad = 0
for r in rows:
    s, e = r["span"]
    assert text[s:e] == TOKEN
    nearest = [m for m in keyre.finditer(text, 0, s)][-1].group(1)
    task_ord = text.count('"task_id"', 0, s) - 1
    if nearest != r["field"].split(".")[-1] or task_ord != r["task_index"]:
        bad += 1
print("B attribution_rows", len(rows), "mismatches", bad)
assert bad == 0

# (c) token-only projection: parse, leaf diff, set equality, hashes
def typed_leaves(o, path=()):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from typed_leaves(v, path + (k,))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from typed_leaves(v, path + (i,))
    else:
        yield path, o


token_leaf_paths = set()
for p, v in typed_leaves(data):
    if isinstance(v, str) and TOKEN in v:
        token_leaf_paths.add(p)
base = dict(typed_leaves(data))
for name, val in PROFILES.items():
    delta = len(val) - len(TOKEN)
    projected_text = text.replace(TOKEN, val)
    projected = json.loads(projected_text)
    proj = dict(typed_leaves(projected))
    changed = {p for p in base if base[p] != proj.get(p)}
    print("C", name, "delta", delta, "codepoints", len(projected_text),
          "utf8", len(projected_text.encode()),
          "sha256", hashlib.sha256(projected_text.encode()).hexdigest(),
          "tasks", len(projected),
          "changed", len(changed), "changed_eq_token_leaves", changed == token_leaf_paths,
          "added", len(set(proj) - set(base)), "removed", len(set(base) - set(proj)),
          "ids_preserved", all(x["task_id"] == y["task_id"] for x, y in zip(data, projected)),
          "remaining_token", projected_text.count(TOKEN))
    assert changed == token_leaf_paths and len(projected) == 812
    assert projected_text.count(TOKEN) == 0

# (d) program_html entry index distribution
pidx = collections.Counter()
for r in rows:
    m = re.search(r"/program_html/([0-9]+)/", r["pointer"])
    if m:
        pidx[(r["field"], int(m.group(1)))] += 1
print("D program_html_url", {k: v for k, v in sorted(pidx.items()) if k[0] == "eval.program_html.url"})
print("D must_include", {k: v for k, v in sorted(pidx.items()) if k[0] != "eval.program_html.url"})

# (e) profile-independent occurrence projection arithmetic
print("E occurrences_per_profile", len(rows), "x_profiles", len(rows) * 3,
      "leaf_changes_x_profiles", len(rows) * 3,
      "affected_task_projections", len({r["task_index"] for r in rows}) * 3,
      "of", len(data) * 3)

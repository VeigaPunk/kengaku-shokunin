#!/usr/bin/env python3
"""Independent literal-token census for the pinned WebArena raw task file.

No production instrument source is read or imported.  Inputs are the pinned
bytes only: raw test.raw.json and profiles.json.
"""
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict

BASE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures"
RAW = BASE + "/r28/webarena/config_files/test.raw.json"
PROFILES = BASE + "/r29/profiles.json"
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOKENS = ["__" + n + "__" for n in ORDER]

raw_bytes = open(RAW, "rb").read()
text = raw_bytes.decode("utf-8")
print("raw_bytes", len(raw_bytes), "sha256", hashlib.sha256(raw_bytes).hexdigest())
print("decoded_chars", len(text), "ascii", text.isascii(),
      "carriage_returns", text.count("\r"))

# ---- overlap / substring logic -------------------------------------------------
print("\n== substring matrix ==")
for a in TOKENS:
    for b in TOKENS:
        if a != b and a in b:
            print("SUBSTRING", a, "in", b)
# occurrences of the bare prefixes to show family membership
for probe in ["__SHOPPING__", "__SHOPPING_ADMIN__", "__SHOPPING",
              "__SHOPPING_ADMIN", "__SHOPPING__ADMIN__"]:
    print("probe", probe, "count", text.count(probe))

# every env-ish marker form present
print("\n== all __X__ / __x__ marker forms ==")
forms = Counter(re.findall(r"__[A-Za-z0-9_]+?__", text))
for k, v in sorted(forms.items()):
    print("FORM", k, v)

# ---- global raw-text counts ----------------------------------------------------
print("\n== raw text literal counts ==")
occ = {t: text.count(t) for t in TOKENS}
print("ORIGINAL_OCCURRENCES_BY_TOKEN", json.dumps(occ))
print("sum", sum(occ.values()))

# ---- task-level attribution ----------------------------------------------------
parsed = json.loads(text)
print("\nparsed_top_level", type(parsed).__name__, len(parsed))

def leaf_strings(obj, path, out, keypath):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str) and any(t in k for t in TOKENS):
                out.append((path + "/" + k, "$KEY", k))
            leaf_strings(v, path + "." + str(k), out, keypath + (str(k),))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            leaf_strings(v, path + "[]", out, keypath + (i,))
    else:
        if isinstance(obj, str):
            out.append((path, "$VALUE", obj))

tasks_with = Counter()
tasks_occ = Counter()
per_task_leaves = defaultdict(dict)  # token -> {task_index: [leaf paths]}
leaf_index = []  # (task_idx, path, text)
for idx, item in enumerate(parsed):
    out = []
    leaf_strings(item, "$", out, ())
    dumped = json.dumps(item, ensure_ascii=False)
    for t in TOKENS:
        if t in dumped:
            tasks_with[t] += 1
        tasks_occ[t] += dumped.count(t)
    for path, kind, s in out:
        if kind != "$VALUE":
            continue
        leaf_index.append((idx, path, s))
        for t in TOKENS:
            if t in s:
                per_task_leaves[t].setdefault(idx, []).append((path, s.count(t)))
print("TASKS_WITH_TOKEN", json.dumps({t: tasks_with[t] for t in TOKENS}))
print("TASKS_OCCURRENCE_SUM", json.dumps({t: tasks_occ[t] for t in TOKENS}))

# text-span attribution (independent of json round-trip)
spans = []
for i in range(len(parsed)):
    spans.append(parsed[i].get("task_id"))
span_task = Counter()
pos = 0
for idx in range(len(text)):
    pass
# walk top-level JSON object spans with raw_decode
dec = json.JSONDecoder()
p = text.index("[")
# map each object start to index
starts = []
depth = 0
in_str = False
esc = False
obj_start = None
arr_start = p
for i in range(p + 1, len(text)):
    c = text[i]
    if in_str:
        if esc:
            esc = False
        elif c == "\\":
            esc = True
        elif c == '"':
            in_str = False
        continue
    if c == '"':
        in_str = True
    elif c == "{":
        if depth == 0:
            obj_start = i
        depth += 1
    elif c == "}":
        depth -= 1
        if depth == 0:
            starts.append((obj_start, i))
print("raw_object_spans", len(starts))

# ---- decoded leaf census -------------------------------------------------------
print("\n== decoded string leaves ==")
print("string_leaf_count", len(leaf_index))
leaf_with_token = {t: [(idx, path) for idx, path, s in leaf_index if t in s]
                   for t in TOKENS}
for t in TOKENS:
    print("LEAVES_WITH", t, len(leaf_with_token[t]),
          "tasks", len({i for i, _ in leaf_with_token[t]}),
          "occurrences_in_leaves", sum(s.count(t) for i, p, s in leaf_index if t in s))

# overlap: leaves carrying both SHOPPING and SHOPPING_ADMIN
both = [(i, p) for i, p, s in leaf_index if "__SHOPPING__" in s and "__SHOPPING_ADMIN__" in s]
print("leaves_with_BOTH_SHOPPING_and_SHOPPING_ADMIN", len(both))
# leaves with more than one occurrence of any token
multi = [(i, p, {t: s.count(t) for t in TOKENS if s.count(t) > 1})
         for i, p, s in leaf_index if any(s.count(t) > 1 for t in TOKENS)]
print("leaves_with_multi_occurrence", len(multi))
for row in multi:
    print("MULTI", row)

# ---- per-profile sequential replacement over full raw text --------------------
print("\n== per-profile applied replacements and decoded changes ==")
profiles = json.load(open(PROFILES))
for pname, pdata in profiles.items():
    vals = pdata["values"]
    step_counts = {}
    cur = text
    for n in ORDER:
        tok = "__" + n + "__"
        c = cur.count(tok)
        step_counts[n] = c
        cur = cur.replace(tok, vals[n])
    after = json.loads(cur)
    assert len(after) == len(parsed)
    changed_leaves = 0
    changed_leaves_by_token = Counter()
    changed_tasks = set()
    changed_tasks_by_token = defaultdict(set)
    changed_by_category = Counter()
    changed_by_template = Counter()
    changed_leaves_by_token_and_path = defaultdict(list)
    for (idx, path, before_s) in leaf_index:
        # locate the corresponding after leaf by re-walking both
        pass
    # structural walk in parallel
    ctr = {"changed": 0}
    def walk(a, b, path, idx, tmpl):
        if isinstance(a, dict) and isinstance(b, dict):
            assert a.keys() == b.keys()
            for k in a:
                walk(a[k], b[k], path + "." + str(k), idx, tmpl + "." + str(k))
        elif isinstance(a, list) and isinstance(b, list):
            assert len(a) == len(b)
            for i, (x, y) in enumerate(zip(a, b)):
                walk(x, y, path + "[]", idx, tmpl + "[]")
        else:
            if isinstance(a, str):
                assert isinstance(b, str), (path, type(a), type(b))
                if a != b:
                    ctr["changed"] += 1
                    changed_tasks.add(idx)
                    cat = "url_field" if tmpl.split(".")[-1] in (
                        "start_url", "reference_url", "url") else "non_url_field"
                    changed_by_category[cat] += 1
                    changed_by_template[tmpl] += 1
                    for t in TOKENS:
                        if t in a:
                            changed_leaves_by_token[t] += 1
                            changed_tasks_by_token[t].add(idx)
                            changed_leaves_by_token_and_path[t].append((idx, path, tmpl, a.count(t)))
            elif isinstance(a, (int, float, bool)) or a is None:
                assert a == b
            else:
                raise AssertionError(type(a))
    for idx, (a, b) in enumerate(zip(parsed, after)):
        walk(a, b, "$", idx, "$")
    print("\nPROFILE", pname)
    print("  applied_replacements", json.dumps(step_counts, sort_keys=True))
    changed_leaves = ctr["changed"]; print("  changed_leaf_count", changed_leaves, "changed_task_count", len(changed_tasks))
    print("  changed_leaves_by_token", json.dumps({t: changed_leaves_by_token[t] for t in TOKENS}))
    print("  changed_tasks_by_token", json.dumps({t: len(changed_tasks_by_token[t]) for t in TOKENS}))
    print("  sum_changed_leaves_by_token", sum(changed_leaves_by_token.values()))
    print("  changed_leaves_by_category", json.dumps(dict(sorted(changed_by_category.items()))))
    print("  changed_leaves_by_path_template", json.dumps(dict(sorted(changed_by_template.items()))))
    print("  changed_leaves_with_multiple_occurrences",
          sum(1 for i, p, s in leaf_index if any(s.count(t) > 1 for t in TOKENS)))
    print("  projected_text_sha256", hashlib.sha256(cur.encode("utf-8")).hexdigest())
    # remaining known tokens in text and in decoded leaves
    print("  remaining_known_tokens_text", json.dumps({t: cur.count(t) for t in TOKENS}))
    rem_dec = Counter()
    def walk_rem(x, tmpl):
        if isinstance(x, dict):
            for k, v in x.items():
                walk_rem(v, tmpl + "." + str(k))
        elif isinstance(x, list):
            for v in x:
                walk_rem(v, tmpl + "[]")
        elif isinstance(x, str):
            for t in TOKENS:
                rem_dec[t] += x.count(t)
    for it in after:
        walk_rem(it, "$")
    print("  remaining_known_tokens_decoded", json.dumps({t: rem_dec[t] for t in TOKENS}))
    print("  SHOPPING_ADMIN changed leaves by path_template",
          json.dumps(dict(sorted(Counter(tm for i, p, tm, c in
                                         changed_leaves_by_token_and_path["__SHOPPING_ADMIN__"]).items()))))
    print("  SHOPPING_ADMIN changed leaves multi-occ", 
          [(i, p, c) for i, p, tm, c in changed_leaves_by_token_and_path["__SHOPPING_ADMIN__"] if c > 1])
    print("  SHOPPING_ADMIN changed leaves", len(changed_leaves_by_token_and_path["__SHOPPING_ADMIN__"]))
    print("  SHOPPING_ADMIN changed tasks", len(changed_tasks_by_token["__SHOPPING_ADMIN__"]))

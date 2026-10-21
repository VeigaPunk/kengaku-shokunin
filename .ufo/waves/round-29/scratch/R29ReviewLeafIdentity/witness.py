#!/usr/bin/env python3
"""Per-task witness census (review seat R29ReviewLeafIdentity). Read-only."""
import hashlib
import json
import os
import re

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
RAW = os.path.join(ROOT, "plans/fixtures/r28/webarena/config_files/test.raw.json")
PROF = os.path.join(ROOT, "plans/fixtures/r29/profiles.json")
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
TOKENS = {"%s" % t: "__%s__" % t for t in ORDER}

raw_bytes = open(RAW, "rb").read()
raw_text = raw_bytes.decode("utf-8")
data = json.loads(raw_text)
prof = json.load(open(PROF))["distinct_origins"]["values"]

# task index from path
def task_of(path):
    m = re.match(r"\$\[(\d+)\]", path)
    return int(m.group(1)) if m else None

def project(text, values):
    counts = {}
    for t in ORDER:
        tok = TOKENS[t]
        counts[t] = text.count(tok)
        text = text.replace(tok, values[t])
    return text, counts

def leaves(obj, path="$", acc=None):
    if acc is None:
        acc = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            leaves(v, path + "." + k, acc)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            leaves(v, "%s[%d]" % (path, i), acc)
    else:
        acc.append((path, obj))
    return acc

raw_leaves = leaves(data)
raw_map = {p: v for p, v in raw_leaves}
proj_text, counts = project(raw_text, prof)
pdata = json.loads(proj_text)
proj_map = {p: v for p, v in leaves(pdata)}

changed = [(p, raw_map[p], proj_map[p]) for p in raw_map if raw_map[p] != proj_map.get(p)]
per_task = {}
for p, a, b in changed:
    t = task_of(p)
    per_task.setdefault(t, []).append((p, a, b))

hist = {}
for t, v in per_task.items():
    hist[len(v)] = hist.get(len(v), 0) + 1
print("tasks_with_changes:", len(per_task))
print("per_task_changed_leaf_count_histogram:", json.dumps(hist, sort_keys=True))
print("total_changed_leaves:", len(changed))
print("tasks_with_zero_changes:", 812 - len(per_task))
print("occurrences_total:", sum(counts.values()))
print("leaves_changed:", len(changed))
print("leaves_with_multiple_occurrences:", sum(1 for p, a, b in changed if sum(a.count(t) for t in TOKENS.values()) > 1))
print("max_changed_leaves_in_one_task:", max((len(v) for v in per_task.values()), default=0))
top = sorted(per_task.items(), key=lambda kv: -len(kv[1]))[:5]
print("tasks_with_most_changed_leaves:", [(t, len(v)) for t, v in top])

print()
print("=== per-path changed leaf counts ===")
pp = {}
for p, a, b in changed:
    n = re.sub(r"\[\d+\]", "[]", p)
    pp[n] = pp.get(n, 0) + 1
for k in sorted(pp):
    print(" ", k, pp[k])

print()
print("=== witnesses ===")
for t in [0, 1, 66, 431, 682, 487, 490, 259]:
    print("--- task", t, "task_id_field=", repr(data[t]["task_id"]), "type=", type(data[t]["task_id"]).__name__)
    for p, a, b in per_task.get(t, []):
        print("    ", p)
        print("       raw:", repr(a)[:220])
        print("       prj:", repr(b)[:220])

print()
print("=== tasks with zero changed leaves (sample) ===")
zero = [t for t in range(812) if t not in per_task]
print("count:", len(zero), "first10:", zero[:10])
if zero:
    t = zero[0]
    print("example task", t, "start_url=", repr(data[t].get("start_url")))
    print("  keys:", list(data[t].keys()))
    print("  eval keys:", list(data[t]["eval"].keys()) if isinstance(data[t].get("eval"), dict) else None)

print()
print("=== index vs task_id ===")
print("all int task_id:", all(isinstance(it["task_id"], int) for it in data))
print("idx==task_id for all:", all(idx == it["task_id"] for idx, it in enumerate(data)))
print("str(task_id)==str(idx) for all:", all(str(idx) == str(it["task_id"]) for idx, it in enumerate(data)))
print("filename stem would be:", "0.json", "task_id str:", repr(str(data[0]["task_id"])))
print("upstream filename for ordinal 0:", "config_files/0.json")

print()
print("=== eval consumption structure sample (task 0) ===")
print(json.dumps(data[0], indent=1)[:1500])

print()
print("=== leaves NOT under eval but containing tokens? ===")
print(sorted({re.sub(r"\[\d+\]", "[]", p) for p, a, b in changed if ".eval" not in p}))
print("=== non-URL-valued token leaves (no http/:// in raw value) ===")
nourl = [(p, a) for p, a, b in changed if "://" not in a]
print("count:", len(nourl))
for p, a in nourl[:10]:
    print("   ", p, repr(a)[:160])

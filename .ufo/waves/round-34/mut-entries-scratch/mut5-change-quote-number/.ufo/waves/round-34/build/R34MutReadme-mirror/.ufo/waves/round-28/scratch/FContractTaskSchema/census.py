"""Independent top-level task-shape census of the pinned raw JSON; imports no production/oracle code."""
import collections
import json
import sys
from pathlib import Path

RAW = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json")
dupes = []


def hook(pairs):
    seen = collections.Counter(k for k, _ in pairs)
    for key, n in seen.items():
        if n > 1:
            dupes.append((key, n))
    return dict(pairs)


def constant(value):
    raise ValueError("non-standard JSON constant " + value)


tasks = json.loads(RAW.read_text(), object_pairs_hook=hook, parse_constant=constant)
out = {"top_type": type(tasks).__name__, "count": len(tasks), "duplicate_keys": dupes}
shape = collections.Counter()
ids = []
for task in tasks:
    shape["object" if isinstance(task, dict) else type(task).__name__] += 1
    tid = task.get("task_id")
    shape["tid:" + type(tid).__name__] += 1
    ids.append(tid)
    sites = task.get("sites")
    shape["sites:" + ("ok" if isinstance(sites, list) and sites and all(isinstance(s, str) and s for s in sites) else repr(sites))] += 1
    intent = task.get("intent")
    shape["intent:" + ("ok" if isinstance(intent, str) and intent.strip() else repr(intent))] += 1
    for flag in ("require_login", "require_reset"):
        shape[flag + ":" + (type(task[flag]).__name__ + "=" + str(task[flag]) if flag in task else "MISSING")] += 1
    ev = task.get("eval")
    shape["eval:" + type(ev).__name__] += 1
    kinds = ev.get("eval_types") if isinstance(ev, dict) else None
    shape["kinds:" + ("ok" if isinstance(kinds, list) and kinds and all(isinstance(k, str) for k in kinds) else repr(kinds))] += 1
    for key in task:
        shape["key:" + key] += 1
    if isinstance(ev, dict):
        for key in ev:
            shape["evalkey:" + key] += 1
out["ids_exact_0_811"] = sorted(ids) == list(range(812))
out["shape"] = dict(sorted(shape.items()))
json.dump(out, sys.stdout, indent=1)
print()

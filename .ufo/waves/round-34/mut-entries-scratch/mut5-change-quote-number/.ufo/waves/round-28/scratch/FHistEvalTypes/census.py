#!/usr/bin/env python3
"""Independent evaluator-type-set census for round-28 FHistEvalTypes.

Pure stdlib re-derivation over the pinned raw JSON. Does NOT import
plans/benchmark_spec_audit.py or any other oracle. Counts:
  - eval_type_sets  : histogram keyed by SORTED eval_types label
  - eval_type_orders: histogram keyed by DECLARED ORDER eval_types label
  - atomic membership counts (tasks containing each atomic type)
  - combination vs single-type split
  - site/evaluator strata keyed by (sorted sites, sorted eval types)
  - validation anomalies: invalid/empty/dup/unknown eval_types
"""
import collections
import hashlib
import json
import sys

RAW = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json"
KNOWN = {"string_match", "url_match", "program_html"}

raw = open(RAW, "rb").read()
print("raw_sha256", hashlib.sha256(raw).hexdigest())
tasks = json.loads(raw)
print("task_count", len(tasks), "top_level_type", type(tasks).__name__)

set_hist = collections.Counter()
order_hist = collections.Counter()
atomic_membership = collections.Counter()
strata = collections.defaultdict(list)
anomalies = []
combination_ids = []
missing_eval = []

for pos, task in enumerate(tasks):
    tid = task.get("task_id") if isinstance(task, dict) else None
    ev = task.get("eval") if isinstance(task, dict) else None
    if not isinstance(ev, dict):
        missing_eval.append((pos, tid))
        kinds = []
    else:
        kinds = ev.get("eval_types")
    valid_list = isinstance(kinds, list) and bool(kinds) and all(isinstance(x, str) for x in kinds)
    if not valid_list:
        anomalies.append({"pos": pos, "task_id": tid, "issue": "eval_types_not_nonempty_str_list", "value": kinds})
        kinds_l = kinds if isinstance(kinds, list) else []
    else:
        kinds_l = list(kinds)
        if len(kinds_l) != len(set(kinds_l)):
            anomalies.append({"pos": pos, "task_id": tid, "issue": "duplicate_eval_type", "value": kinds_l})
        for k in kinds_l:
            if k not in KNOWN:
                anomalies.append({"pos": pos, "task_id": tid, "issue": "unknown_eval_type", "value": k})
    set_key = ",".join(sorted(kinds_l))
    order_key = ",".join(kinds_l)
    set_hist[set_key] += 1
    order_hist[order_key] += 1
    for k in set(kinds_l):
        atomic_membership[k] += 1
    if len(set(kinds_l)) > 1:
        combination_ids.append((tid, order_key))
    sites = task.get("sites") if isinstance(task, dict) else None
    if isinstance(sites, list) and sites and all(isinstance(s, str) and s for s in sites) and isinstance(tid, int) and valid_list:
        strata[(tuple(sorted(sites)), tuple(sorted(kinds_l)))].append(tid)

print("\n== eval_type_sets (sorted-set key) ==")
for k in sorted(set_hist):
    print(f"  {k!r}: {set_hist[k]}")
print("distinct_eval_type_sets", len(set_hist))
print("sum_sets", sum(set_hist.values()))

print("\n== eval_type_orders (declared-order key) ==")
for k in sorted(order_hist):
    print(f"  {k!r}: {order_hist[k]}")
print("distinct_eval_type_orders", len(order_hist))

print("\n== atomic membership (tasks whose set contains the type) ==")
for k in sorted(atomic_membership):
    print(f"  {k}: {atomic_membership[k]}")

print("\n== combination vs single ==")
single = sum(v for k, v in set_hist.items() if "," not in k and k)
multi = sum(v for k, v in set_hist.items() if "," in k)
empty = set_hist.get("", 0)
print(f"  single_type_tasks={single} combination_tasks={multi} empty_set_tasks={empty}")
print("  combination task ids:", json.dumps(combination_ids[:40]), "...total", len(combination_ids))

print("\n== strata ==")
print("distinct_(sorted_sites,sorted_evaltypes)_strata", len(strata))
for k in sorted(strata):
    print(f"  {k}: n={len(strata[k])} min_id={min(strata[k])}")

print("\n== anomalies ==")
print("missing_eval_field", missing_eval)
print("anomaly_count", len(anomalies))
for a in anomalies[:20]:
    print("  ", a)

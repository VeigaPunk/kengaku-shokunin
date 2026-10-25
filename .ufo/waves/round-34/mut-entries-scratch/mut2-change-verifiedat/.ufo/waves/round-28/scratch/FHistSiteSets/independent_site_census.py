#!/usr/bin/env python3
"""FHistSiteSets: independent numeric replay of site-set counts and
site/evaluator strata over pinned test.raw.json.

Stdlib only. Never imports plans/benchmark_spec_audit.py or any alternate
oracle. Reads the raw JSON directly. Derives:
  - task population size, distinct task_ids
  - site-set multiset (order-insensitive, sorted tuple key) per task
  - per-site occurrence counts (a task may list several sites)
  - (sorted site set, sorted eval_types set) strata with member task_ids
  - deterministic selection: lexicographic stratum ordering, min task_id
    per stratum, first 16 -> compare to persisted selected-task-ids.json
  - sites appearing inside the selected sample (shopping omission check)
"""
import collections
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
RAW = ROOT / "plans/fixtures/r28/webarena/config_files/test.raw.json"
SEL = ROOT / "plans/fixtures/r28/webarena/selected-task-ids.json"
MANIFEST = ROOT / "plans/fixtures/r28/webarena/manifest.json"

out = {}
out["raw_sha256"] = hashlib.sha256(RAW.read_bytes()).hexdigest()
out["manifest_sha256"] = hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
out["selection_sha256"] = hashlib.sha256(SEL.read_bytes()).hexdigest()

tasks = json.loads(RAW.read_text())
out["task_count"] = len(tasks)
ids = [t["task_id"] for t in tasks]
out["distinct_task_ids"] = len(set(ids))
out["duplicate_task_ids"] = sorted(k for k, v in collections.Counter(ids).items() if v > 1)
out["id_range_min"], out["id_range_max"] = min(ids), max(ids)
out["missing_ids_0_811"] = sorted(set(range(len(tasks))) - set(ids))

# --- site-set census ---
site_set_counter = collections.Counter()          # sorted site tuple -> count
site_occurrence = collections.Counter()           # individual site name -> count
eval_type_set_counter = collections.Counter()     # sorted eval-type tuple -> count
for t in tasks:
    sites = t["sites"]
    assert isinstance(sites, list) and sites, t["task_id"]
    site_set_counter[tuple(sorted(sites))] += 1
    for s in sites:
        site_occurrence[s] += 1
    eval_type_set_counter[tuple(sorted(t["eval"]["eval_types"]))] += 1

out["site_sets"] = {", ".join(k): v for k, v in sorted(site_set_counter.items())}
out["distinct_site_sets"] = len(site_set_counter)
out["site_occurrences"] = dict(sorted(site_occurrence.items()))
out["eval_type_sets"] = {", ".join(k): v for k, v in sorted(eval_type_set_counter.items())}
out["distinct_eval_type_sets"] = len(eval_type_set_counter)
out["site_set_total"] = sum(site_set_counter.values())
out["eval_type_set_total"] = sum(eval_type_set_counter.values())

# --- strata: (sorted sites, sorted eval_types) ---
strata = collections.defaultdict(list)
skipped = []
for t in tasks:
    sites = t.get("sites")
    kinds = t.get("eval", {}).get("eval_types")
    tid = t.get("task_id")
    if not (isinstance(sites, list) and sites and all(isinstance(x, str) and x for x in sites)):
        skipped.append((tid, "sites_invalid")); continue
    if not (isinstance(kinds, list) and kinds and all(isinstance(x, str) for x in kinds)):
        skipped.append((tid, "eval_types_invalid")); continue
    if type(tid) is not int:
        skipped.append((tid, "task_id_invalid")); continue
    strata[(tuple(sorted(sites)), tuple(sorted(kinds)))].append(tid)

out["strata_skipped_tasks"] = skipped
out["strata_population"] = sum(len(v) for v in strata.values())
ordered_keys = sorted(strata.keys())
out["site_eval_strata"] = len(ordered_keys)
out["strata"] = [
    {
        "sites": list(sites),
        "eval_types": list(kinds),
        "size": len(strata[key]),
        "min_task_id": min(strata[key]),
        "member_task_ids": sorted(strata[key]),
    }
    for key in ordered_keys
    for sites, kinds in [key]
]

# --- deterministic selection replay ---
selection = [min(strata[k]) for k in ordered_keys][:16]
out["selection_replay"] = selection
persisted = json.loads(SEL.read_text())
out["selection_persisted"] = persisted
out["selection_matches_persisted"] = selection == persisted

# sites inside selected sample
sel_tasks = [t for t in tasks if t["task_id"] in selection]
out["selected_sites"] = sorted({s for t in sel_tasks for s in t["sites"]})
out["selected_eval_types"] = sorted({k for t in sel_tasks for k in t["eval"]["eval_types"]})
out["shopping_in_selection"] = any("shopping" in t["sites"] for t in sel_tasks)
out["selected_detail"] = [
    {"task_id": t["task_id"], "sites": sorted(t["sites"]),
     "eval_types": sorted(t["eval"]["eval_types"])}
    for t in sorted(sel_tasks, key=lambda x: selection.index(x["task_id"]))
]

print(json.dumps(out, indent=1, sort_keys=True))

#!/usr/bin/env python3
import json

inst = json.load(open("/tmp/fr29d/inst.json"))
orc = json.load(open("/tmp/fr29d/oracle.json"))
mism = []
for name, rec in orc.items():
    r = inst["profiles"][name]
    for key in ("parsed_task_count", "string_leaf_count", "changed_leaf_count", "changed_task_count",
                "changed_leaves_with_multiple_occurrences", "projected_text_sha256",
                "changed_leaves_by_path_template", "changed_leaves_by_category", "changed_leaves_by_token",
                "remaining_known_tokens_text", "remaining_known_tokens_decoded"):
        if r.get(key) != rec[key]:
            mism.append((name, key, r.get(key), rec[key]))
    # per-task changed leaf pointers
    inst_ptrs = {str(t["output_index"]): sorted(l["json_pointer"] for l in t["changed_leaves"]) for t in r["tasks"]}
    if inst_ptrs != rec["per_task_changed_leaves"]:
        diff_keys = [k for k in set(inst_ptrs) | set(rec["per_task_changed_leaves"])
                     if inst_ptrs.get(k) != rec["per_task_changed_leaves"].get(k)]
        mism.append((name, "per_task_changed_leaves", "differs on %d task indices" % len(diff_keys), diff_keys[:5]))
    # projected task objects
    for t in r["tasks"]:
        if t["projected_task"] != json.loads(json.dumps(inst["profiles"][name]["tasks"][t["output_index"]]["projected_task"])):
            pass
print("MISMATCHES:", len(mism))
for m in mism:
    print(m)
# instrument's own view of carriers (only appears inside findings) and changed-leaf sum checks
for name, rec in inst["profiles"].items():
    print(name, "sum_by_token=", sum(rec["changed_leaves_by_token"].values()), "changed_leaf_count=", rec["changed_leaf_count"],
          "sum_by_cat=", sum(rec["changed_leaves_by_category"].values()))
print("instrument findings:", json.dumps(inst["findings"]))
print("oracle problems:", {n: o["problem_count"] for n, o in orc.items()})
print("oracle carriers/unexplained:", {n: (o["carriers"], o["unexplained"], o["changed_leaf_count"]) for n, o in orc.items()})

#!/usr/bin/env python3
"""FHistStringOps independent census — stdlib only, no benchmark_spec_audit import.

Derives task-count denominators for string-match operators and N/A conditional
branch counts directly from plans/fixtures/r28/webarena/config_files/test.raw.json.
No upstream webarena code, no audit module, no alternate oracle.
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
RAW = ROOT / "plans/fixtures/r28/webarena/config_files/test.raw.json"

payload = RAW.read_bytes()
print("sha256", hashlib.sha256(payload).hexdigest())
tasks = json.loads(payload)
print("task_count", len(tasks))

# --- independent counting logic ---
# For every task whose eval.eval_types contains "string_match", look at
# eval.reference_answers keys. A task is counted under each operator it declares
# (operators can coexist). Track N/A conditional branches: any reference_answers
# value equal to the literal "N/A", split by operator, plus full keysets.

op_task_ids = {"exact_match": set(), "must_include": set(), "fuzzy_match": set()}
other_ops = Counter()
keysets = Counter()
na_tasks = []           # task ids where some operator value == "N/A"
na_by_operator = Counter()
na_fuzzy_keysets = Counter()
na_fuzzy_with_siblings = []
string_tasks = 0
nonna_fuzzy = 0
fuzzy_shape = Counter()  # value type for fuzzy_match

for t in tasks:
    ev = t.get("eval", {})
    types = ev.get("eval_types", [])
    if "string_match" not in types:
        continue
    string_tasks += 1
    refs = ev.get("reference_answers", {})
    keys = tuple(sorted(refs))
    keysets[keys] += 1
    for op, val in refs.items():
        if op in op_task_ids:
            op_task_ids[op].add(t["task_id"])
        else:
            other_ops[op] += 1
        if val == "N/A":
            na_tasks.append(t["task_id"])
            na_by_operator[op] += 1
    fz = refs.get("fuzzy_match")
    if "fuzzy_match" in refs:
        fuzzy_shape[type(fz).__name__] += 1
        if fz == "N/A":
            na_fuzzy_keysets[keys] += 1
            if len(refs) > 1:
                na_fuzzy_with_siblings.append(t["task_id"])
        else:
            nonna_fuzzy += 1

print("string_match_tasks", string_tasks)
for op in ("exact_match", "must_include", "fuzzy_match"):
    print(f"tasks_with_{op}", len(op_task_ids[op]))
print("other_reference_answer_operators", dict(other_ops))
print("reference_answer_keysets", {"/".join(k): v for k, v in sorted(keysets.items())})
print("na_branch_tasks_total", len(na_tasks), "distinct", len(set(na_tasks)))
print("na_by_operator", dict(na_by_operator))
print("fuzzy_na_keysets", {"/".join(k): v for k, v in sorted(na_fuzzy_keysets.items())})
print("fuzzy_na_with_sibling_operators", sorted(na_fuzzy_with_siblings))
print("fuzzy_non_na", nonna_fuzzy)
print("fuzzy_value_types", dict(fuzzy_shape))
# tasks whose ONLY reference operator is fuzzy_match == "N/A"
only_na = [tid for keys, n in na_fuzzy_keysets.items() if keys == ("fuzzy_match",) for tid in []]
na_only_count = na_fuzzy_keysets.get(("fuzzy_match",), 0)
print("na_only_tasks_fuzzy_match_sole_key", na_only_count)
# co-occurrence matrix of the three operators
cooc = Counter()
for t in tasks:
    ev = t.get("eval", {})
    if "string_match" not in ev.get("eval_types", []):
        continue
    present = tuple(sorted(op for op in op_task_ids if op in ev.get("reference_answers", {})))
    cooc[present] += 1
print("operator_cooccurrence", {"/".join(k) or "none": v for k, v in sorted(cooc.items())})
json.dump({
    "task_count": len(tasks),
    "string_match_tasks": string_tasks,
    "exact_match_tasks": len(op_task_ids["exact_match"]),
    "must_include_tasks": len(op_task_ids["must_include"]),
    "fuzzy_match_tasks": len(op_task_ids["fuzzy_match"]),
    "na_branch_tasks": len(set(na_tasks)),
    "na_by_operator": dict(na_by_operator),
    "fuzzy_na_keysets": {"/".join(k): v for k, v in na_fuzzy_keysets.items()},
    "fuzzy_na_with_sibling_operators": sorted(na_fuzzy_with_siblings),
    "fuzzy_non_na": nonna_fuzzy,
    "keysets": {"/".join(k): v for k, v in keysets.items()},
    "cooccurrence": {"/".join(k): v for k, v in cooc.items()},
}, open(ROOT / ".ufo/waves/round-28/scratch/FHistStringOps/census.json", "w"), indent=1, sort_keys=True)
print("wrote census.json")

#!/usr/bin/env python3
"""Leaf attribution under the adopted cascade hand fixture (R29_ORDER_CASCADE_01)."""
import importlib.util
import json

spec = importlib.util.spec_from_file_location("cp", "/tmp/fr29d/cp.py")
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)

case = json.load(open("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/hand/cascade-order.case.json"))
raw = case["raw_serialized_text"]
values = case["values"]
print("values:", json.dumps(values, indent=1))
result, findings = cp.audit_text(raw, {"distinct_origins": {"purpose": "cascade hand case", "values": values}})
rec = result["profiles"]["distinct_origins"]
print("findings:", [f["id"] for f in findings])
print("applied_replacements:", json.dumps({s["name"]: s["applied_replacements"] for s in rec["steps"]}))
print("changed_leaf_count:", rec["changed_leaf_count"], "changed_leaves_by_token:", json.dumps(rec["changed_leaves_by_token"]))
print("remaining_text:", json.dumps(rec["remaining_known_tokens_text"]))
print("remaining_decoded:", json.dumps(rec["remaining_known_tokens_decoded"]))
for t in rec["tasks"]:
    for leaf in t["changed_leaves"]:
        print("  leaf %s tokens=%s" % (leaf["json_pointer"], leaf["tokens"]))
        print("     original : %r" % leaf["original"])
        print("     projected: %r" % leaf["projected"])
# which profile value actually produced the final leaf text?
final = rec["tasks"][0]["changed_leaves"][0]["projected"]
producers = [name for name, val in values.items() if val == final]
print("final leaf text produced by profile value(s):", producers)
print("token credited by the leaf census:",
      [tok for tok in rec["changed_leaves_by_token"] if rec["changed_leaves_by_token"][tok]])
print("hand fixture asserts only text equality:", list(case.keys()))

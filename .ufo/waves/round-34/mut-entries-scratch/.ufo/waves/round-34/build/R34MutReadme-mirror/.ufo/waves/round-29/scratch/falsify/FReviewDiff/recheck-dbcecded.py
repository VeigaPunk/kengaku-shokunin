#!/usr/bin/env python3
"""Re-check of F1, F3, F4, F7 against the repaired instrument (lane master dbcecded).

Runs against a /tmp byte-copy of plans/config_projection.py at dbcecded.
"""
import importlib.util
import json
import traceback

spec = importlib.util.spec_from_file_location("cp2", "/tmp/fr29d2/cp2.py")
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)

VALUES = {n: "http://%s.invalid:1" % n.lower().replace("_", "-") for n in cp.ORDER}
print("instrument sha under test: 135cc68283e76635df913a085e6c3fcf93b8e04e83af8e9b9aac5b14876aa142")


def run(raw, values=None, label=""):
    vals = dict(VALUES if values is None else values)
    print("=== %s ===" % label)
    print("  input: %r" % raw)
    try:
        result, findings = cp.audit_text(raw, {"distinct_origins": {"purpose": "probe", "values": vals}})
    except Exception as error:
        print("  RAISED %s: %s" % (type(error).__name__, error))
        traceback.print_exc(limit=4)
        print()
        return None
    rec = result["profiles"]["distinct_origins"]
    print("  findings: %s" % json.dumps([f["id"] for f in findings]))
    for f in findings:
        print("    detail: %s" % json.dumps(f, sort_keys=True))
    print("  changed_leaf_count: %s  changed_task_count: %s" % (rec["changed_leaf_count"], rec["changed_task_count"]))
    print("  changed_leaves_by_token: %s" % json.dumps(rec["changed_leaves_by_token"]))
    print("  remaining_text: %s" % json.dumps(rec["remaining_known_tokens_text"]))
    print("  remaining_decoded: %s" % json.dumps(rec["remaining_known_tokens_decoded"]))
    print("  duplicate_object_keys: %s" % result["population"].get("duplicate_object_keys"))
    for t in rec["tasks"]:
        for leaf in t["changed_leaves"]:
            print("    leaf %s tmpl=%r cat=%s tokens=%s" % (leaf["json_pointer"], leaf["path_template"], leaf["category"], leaf["tokens"]))
    print()
    return result


# ---- F1: template() on list-shaped tasks (previously IndexError at config_projection.py:208)
run('[["__GITLAB__"]]', label="F1a nested-list task (previously IndexError)")
run('[["__GITLAB__"], {"z": "__MAP__", "a": 1}]', label="F1b list task + object task")
run('[[["__REDDIT__"]]]', label="F1c doubly nested list task")

# ---- F3: carrier invariant split into leaf_change_unexplained vs token_leaf_unchanged
run('[{"intent": "\\u005f\\u005fGITLAB__"}]', label="F3a escaped-only token in a VALUE (old: leaf_change_unexplained)")
run('[{"intent": "__GITLAB__"}]', values=dict(VALUES, GITLAB="__GITLAB__"), label="F3b profile value == token (old: leaf_change_unexplained)")
run('[{"intent": "__GITLAB__ and __REDDIT__"}]', label="F3c two tokens in one leaf (unchanged leaf set)")

# ---- F4: duplicate JSON key
run('[{"a": "__GITLAB__", "a": "__REDDIT__"}]', label="F4a duplicate key (old: no finding)")
run('[{"a": 1, "a": 2}, {"b": 3, "b": 4}]', label="F4b two objects with duplicate keys")

# ---- F7: pointer() root
print("=== F7 pointer() ===")
print("  pointer(())   = %r" % cp.pointer(()))
print("  pointer((0,))  = %r" % cp.pointer((0,)))
print("  pointer((0,'a')) = %r" % cp.pointer((0, "a")))
print("  template((0,0)) = %r" % cp.template((0, 0)))
print("  template((0,))  = %r" % cp.template((0,)))
print("  template((0,'a',1)) = %r" % cp.template((0, "a", 1)))
print()

#!/usr/bin/env python3
"""Crafted-input probes against the round-29 projection instrument's diff()/leaf-counting path.

Probes run against a /tmp byte-copy of plans/config_projection.py (no production mutation).
Each case prints the exact instrument behaviour (or the exception) for a stated input.
"""
import importlib.util
import json
import sys
import traceback

spec = importlib.util.spec_from_file_location("cp", "/tmp/fr29d/cp.py")
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)

VALUES = {n: "http://%s.invalid:1" % n.lower().replace("_", "-") for n in cp.ORDER}


def run(raw, values=None, label=""):
    vals = dict(VALUES if values is None else values)
    prof = {"distinct_origins": {"purpose": "probe", "values": vals}}
    print("=== %s ===" % label)
    print("  input: %r" % raw)
    try:
        result, findings = cp.audit_text(raw, prof)
    except Exception as error:
        print("  RAISED %s: %s" % (type(error).__name__, error))
        traceback.print_exc(limit=4)
        print()
        return None
    rec = result["profiles"]["distinct_origins"]
    print("  findings: %s" % json.dumps([f["id"] for f in findings]))
    for f in findings:
        print("    detail: %s" % json.dumps(f, sort_keys=True))
    print("  population.occurrence_roles: %s" % json.dumps(result["population"]["occurrence_roles"]))
    print("  population.tasks_with_token: %s" % json.dumps(result["population"]["tasks_with_token"]))
    print("  population.tasks_with_any_token: %s" % result["population"]["tasks_with_any_token"])
    print("  changed_leaf_count: %s  changed_task_count: %s" % (rec["changed_leaf_count"], rec["changed_task_count"]))
    print("  changed_leaves_by_token: %s  (sum=%d)" % (json.dumps(rec["changed_leaves_by_token"]),
                                                      sum(rec["changed_leaves_by_token"].values())))
    print("  changed_leaves_by_path_template: %s" % json.dumps(rec["changed_leaves_by_path_template"]))
    print("  remaining_text: %s" % json.dumps(rec["remaining_known_tokens_text"]))
    print("  remaining_decoded: %s" % json.dumps(rec["remaining_known_tokens_decoded"]))
    for t in rec["tasks"]:
        for leaf in t["changed_leaves"]:
            print("    leaf %s tmpl=%s cat=%s tokens=%s" % (leaf["json_pointer"], leaf["path_template"], leaf["category"], leaf["tokens"]))
    print()
    return result


# P1 nested list task: list index as first path element after the task index
run('[["__GITLAB__"]]', label="P1 nested-list task (list element inside task)")

# P2 duplicate JSON keys: text census vs decoded census
run('[{"a": "__GITLAB__", "a": "__REDDIT__"}]', label="P2 duplicate JSON keys")

# P3 escaped token in an object KEY (decoded census includes keys)
run('[{"\\u005f\\u005fGITLAB__": 1}]', label="P3 escaped token in KEY")

# P4 literal token in an object KEY
run('[{"__GITLAB__": 1}]', label="P4 literal token in KEY")

# P5 one leaf carrying two different tokens
run('[{"intent": "__GITLAB__ and __REDDIT__"}]', label="P5 one leaf, two different tokens")

# P6 escaped-only token inside a leaf value
run('[{"intent": "\\u005f\\u005fGITLAB__"}]', label="P6 escaped-only token in VALUE")

# P7 root type change
run('{"task_id": 0}', label="P7 root is an object, not a list")

# P8 profile value equal to the token itself
run('[{"intent": "__GITLAB__"}]', values=dict(VALUES, GITLAB="__GITLAB__"), label="P8 profile value == token")

# P9 later-token cascade: a profile value that itself contains a later token
run('[{"intent": "__GITLAB__"}]', values=dict(VALUES, GITLAB="http://__REDDIT__.invalid"), label="P9 later-token cascade in a value")

# P10 two tasks, one changed
run('[{"task_id": 0, "a": "__MAP__"}, {"task_id": 1, "b": "x"}]', label="P10 two tasks")

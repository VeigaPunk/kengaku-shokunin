#!/usr/bin/env python3
"""Probe audit_text() internals + how main() classifies them."""
import importlib.util, json, sys, io, contextlib

SRC = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py"
spec = importlib.util.spec_from_file_location("cp", SRC)
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)

VALS = {n: "http://%s.invalid:1" % n.lower() for n in cp.ORDER}
PROF = {"distinct_origins": {"purpose": "probe", "values": VALS}}

def show(label, raw, vals=None, expect_pop=None):
    p = {"distinct_origins": {"purpose": "probe", "values": vals or VALS}}
    try:
        res, f = cp.audit_text(raw, p, expect_pop)
        ids = [x["id"] for x in f]
        print(json.dumps({"label": label, "ok": True, "findings": ids,
                          "detail": f if f else None}, sort_keys=True)[:600])
    except BaseException as e:
        print(json.dumps({"label": label, "ok": False, "raised": type(e).__name__,
                          "msg": str(e)[:120],
                          "tb": [l.strip() for l in (io.StringIO() if False else [])][:0]}, sort_keys=True))

# 1. NaN: json.loads accepts it, the hand-rolled string_spans parser asserts.
show("nan_literal", '[{"task_id": 0, "start_url": "__GITLAB__", "x": NaN}]')
# 2. Infinity
show("infinity_literal", '[{"task_id": 0, "x": Infinity}]')
# 3. degenerate profile value == token: projection is a no-op, leaf unchanged.
show("degenerate_value_equals_token", '[{"task_id": 0, "start_url": "__GITLAB__/p"}]',
     vals=dict(VALS, GITLAB="__GITLAB__"))
# 4. profile value that breaks JSON -> projection_json_invalid (exit 1 finding)
show("value_breaks_json", '[{"task_id": 0, "start_url": "__GITLAB__"}]',
     vals=dict(VALS, GITLAB='http://x"y'))
# 5. token as a key -> token_outside_string_value + projection_structure_changed
show("token_as_key", '[{"task_id": 0, "__MAP__": 1}]')
# 6. valid but non-list input
show("non_list_input", '{"a": 1}')

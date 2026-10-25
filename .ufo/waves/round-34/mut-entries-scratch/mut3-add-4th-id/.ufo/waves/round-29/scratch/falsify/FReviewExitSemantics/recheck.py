#!/usr/bin/env python3
"""Re-check driver against the repaired instrument (lane master dbcecded)."""
import importlib.util, json, sys, io, contextlib

SRC = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py"
spec = importlib.util.spec_from_file_location("cp", SRC)
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)

def run_main(argv, audit_impl):
    cp.audit = audit_impl
    sys.argv = ["config_projection.py"] + argv
    buf = io.StringIO()
    code = 0
    uncaught = None
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            code = cp.main(argv)
    except BaseException as e:
        code = 1
        uncaught = "%s: %s" % (type(e).__name__, e)
    out = buf.getvalue()
    ids = []
    try:
        ids = [f.get("id") for f in json.loads(out)["findings"]]
    except Exception:
        pass
    return {"exit": code, "finding_ids": ids, "stdout_bytes": len(out), "uncaught": uncaught}

def raiser(exc):
    def f(root):
        raise exc
    return f

print("A internal exceptions via audit():")
for name, exc in (("RuntimeError", RuntimeError("boom")),
                  ("AttributeError", AttributeError("'NoneType' object has no attribute 'get'")),
                  ("AssertionError", AssertionError("internal invariant violated")),
                  ("KeyError", KeyError("manifest", "files")),
                  ("ValueError", ValueError("Expecting value: line 1 column 1")),
                  ("OSError", OSError("boom")),
                  ("RecursionError", RecursionError("maximum recursion depth exceeded")),
                  ("MemoryError", MemoryError())):
    r = run_main(["--json"], raiser(exc))
    print("   %-18s exit=%s ids=%s stdout_bytes=%s uncaught=%s" % (name, r["exit"], r["finding_ids"], r["stdout_bytes"], r["uncaught"]))

print("B post-try code (summary_lines / json.dumps) still outside the try:")
def bad_summary(root):
    return {"population": {"input_task_count": 1}, "findings": [], "limitations": cp.LIMITS}, 0
print("   summary_lines KeyError ->", run_main(["--summary"], bad_summary))
def bad_json(root):
    return {"findings": [], "limitations": cp.LIMITS, "bad": {1, 2}}, 0
print("   json.dumps TypeError   ->", run_main(["--json"], bad_json))

print("C audit_text internals (F2 NaN / F6 degenerate / F9 population):")
VALS = {n: "http://%s.invalid:1" % n.lower() for n in cp.ORDER}
def t(label, raw, vals=None, expect=None):
    p = {"p": {"purpose": "probe", "values": vals or VALS}}
    try:
        res, f = cp.audit_text(raw, p, expect)
        print("   %-28s findings=%s" % (label, [x["id"] for x in f]))
        for x in f:
            print("        payload:", json.dumps(x, sort_keys=True)[:180])
    except BaseException as e:
        print("   %-28s raised=%s msg=%s" % (label, type(e).__name__, str(e)[:80]))
t("nan_literal", '[{"task_id": 0, "start_url": "__GITLAB__", "x": NaN}]')
t("infinity_literal", '[{"task_id": 0, "x": Infinity}]')
t("degenerate_value_equals_token", '[{"task_id": 0, "start_url": "__GITLAB__/p"}]', vals=dict(VALS, GITLAB="__GITLAB__"))
t("population_mismatch", '[{"task_id": 7}]', expect=812)

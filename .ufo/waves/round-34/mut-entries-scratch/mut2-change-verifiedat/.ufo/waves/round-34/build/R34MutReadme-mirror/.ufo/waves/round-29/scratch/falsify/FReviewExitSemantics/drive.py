#!/usr/bin/env python3
"""Probe main()'s exception -> exit-code mapping by patching the module's audit()."""
import importlib.util, json, sys, traceback, types

SRC = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py"
spec = importlib.util.spec_from_file_location("cp", SRC)
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)

class Boom(Exception):
    pass

CASES = [
    ("Unevaluable_input_missing", cp.Unevaluable("input_missing", path="X")),
    ("AssertionError_invariant", AssertionError("internal invariant violated")),
    ("KeyError_bug", KeyError("manifest", "files")),
    ("TypeError_bug", TypeError("bug: str vs int")),
    ("IndexError_bug", IndexError("list index out of range")),
    ("ValueError_json", ValueError("Expecting value: line 1 column 1")),
    ("OSError_permission", PermissionError(13, "Permission denied")),
    ("AttributeError_bug", AttributeError("'NoneType' object has no attribute 'get'")),
    ("RecursionError_bug", RecursionError("maximum recursion depth exceeded")),
    ("RuntimeError_bug", RuntimeError("boom")),
    ("NameError_bug", NameError("free variable 'x' referenced")),
    ("ZeroDivisionError_bug", ZeroDivisionError("division by zero")),
]

results = []
for label, exc in CASES:
    def fake_audit(root, _e=exc):
        raise _e
    cp.audit = fake_audit
    sys.argv = ["config_projection.py", "--json"]
    out, err = "", ""
    code = 0
    try:
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            code = cp.main()
        out = buf.getvalue()
    except BaseException as e:  # uncaught -> interpreter-style failure
        code = 1
        out = "UNCAUGHT %s: %s\n" % (type(e).__name__, e)
    ids = []
    try:
        ids = [f.get("id") for f in json.loads(out)["findings"]]
    except Exception:
        pass
    results.append({"label": label, "exit": code, "finding_ids": ids, "stdout_head": out[:160].replace("\n", " ")})

for r in results:
    print(json.dumps(r, sort_keys=True))

#!/usr/bin/env python3
"""Raise a chosen exception class from audit() and let it escape main() -> real CLI shape."""
import importlib.util, sys

SRC = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py"
spec = importlib.util.spec_from_file_location("cp", SRC)
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)

CLASSES = {
    "AttributeError": lambda: AttributeError("'NoneType' object has no attribute 'get'"),
    "RecursionError": lambda: RecursionError("maximum recursion depth exceeded"),
    "RuntimeError": lambda: RuntimeError("boom"),
    "NameError": lambda: NameError("free variable 'x' referenced"),
    "ZeroDivisionError": lambda: ZeroDivisionError("division by zero"),
    "MemoryError": lambda: MemoryError(),
    "StopIteration": lambda: StopIteration(),
}
name = sys.argv[1]
def fake_audit(root, _f=CLASSES[name]):
    raise _f()
cp.audit = fake_audit
sys.argv = ["config_projection.py", "--json"]
raise SystemExit(cp.main())

#!/usr/bin/env python3
"""Real-CLI shape of an uncaught exception class inside audit(): no try/except coverage."""
import importlib.util, sys

SRC = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py"
spec = importlib.util.spec_from_file_location("cp", SRC)
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)

def fake_audit(root):
    raise AttributeError("'NoneType' object has no attribute 'get'")

cp.audit = fake_audit
sys.argv = ["config_projection.py", "--json"]
raise SystemExit(cp.main())

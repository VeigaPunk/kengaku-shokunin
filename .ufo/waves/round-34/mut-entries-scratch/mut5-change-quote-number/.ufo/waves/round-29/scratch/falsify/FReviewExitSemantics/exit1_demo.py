#!/usr/bin/env python3
"""Contrast: intended exit-1 path (audit returns findings) vs input-level finding class."""
import importlib.util, json, sys

SRC = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py"
spec = importlib.util.spec_from_file_location("cp", SRC)
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)

# (1) input-level defect class -> task_population_invalid (exit 1 in audit_text)
res, f = cp.audit_text('[{"task_id": 7}]', {"distinct_origins": {"purpose": "p",
                       "values": {n: "http://%s.invalid" % n.lower() for n in cp.ORDER}}},
                       expected_population=812)
print("A input-level defect class:", json.dumps([x["id"] for x in f]))

# (2) intended exit-1 path through main(): audit returns a findings-bearing result
real_audit = cp.audit
def one_finding(root):
    r, code = real_audit(root)
    r["findings"] = [{"id": "projection_json_invalid", "profile": "demo"}]
    return r, 1
cp.audit = one_finding
sys.argv = ["config_projection.py"]
rc = cp.main()
print("B intended exit-1 exit code:", rc)

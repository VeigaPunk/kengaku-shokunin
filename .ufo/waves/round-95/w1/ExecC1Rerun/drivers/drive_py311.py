#!/usr/bin/env python3
"""ExecC1Rerun portability probe (a) — rerun the 15 replay cases under Python 3.11
inside the frozen probe's bwrap shape (tmpfs /, ro /usr, no network). Report-only:
never claims counter legs. Reuses the frozen probe module unmodified; only the
sandboxed interpreter differs (uv-managed CPython 3.11, ro-bound at its real path).
"""
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r95/ExecC1Rerun")
LANE = S / "lane"
spec = importlib.util.spec_from_file_location("r95probe", str(LANE / "plans" / "round95_vuln_probe.py"))
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

work = S / "w-py311"
work.mkdir(parents=True, exist_ok=True)
cap = LANE / probe.CAP
table = json.loads((LANE / probe.TABLE).read_bytes().decode())
upstream = (cap / "upstream-bottle" / "bottle.py").read_bytes()
vuln = probe.vulnerable(upstream)
harness = work / "harness.py"
harness.write_text(probe.HARNESS, encoding="utf-8")

host_py = Path("/home/vgpnk/.local/bin/python3.11").resolve()
bind_root = host_py.parents[1]   # the uv cpython install prefix (bin/ + lib/)
sandbox_py = str(host_py)        # identical absolute path inside the namespace
bwrap = "/usr/bin/bwrap"

print("PORTABILITY-A python3.11 host:", host_py)
print("PORTABILITY-A bind:", bind_root, "->", bind_root)
ver = subprocess.run(probe.sandbox(bwrap, [("--ro-bind", str(bind_root), str(bind_root))], "/tmp",
                                  [sandbox_py, "-I", "-V"]), capture_output=True, text=True, timeout=60)
print("PORTABILITY-A sandboxed interpreter:", (ver.stdout or ver.stderr).strip(), "rc=%d" % ver.returncode)
if ver.returncode != 0:
    print("PORTABILITY-A sandboxed interpreter unusable")
    sys.exit(2)

print("VULNERABLE_BOTTLE_SHA %s" % probe.sha(vuln))
print("CASE_TABLE_SHA %s" % probe.sha((LANE / probe.TABLE).read_bytes()))
print("OBSERVATIONS_BEGIN")
mismatches = 0
for case in table["cases"]:
    app, tests = probe.stage(bwrap, case, cap, upstream, vuln, work / "cases" / case["id"])
    binds = [("--bind", str(app), "/app"), ("--ro-bind", str(tests), "/tests"),
             ("--ro-bind", str(harness), "/harness.py"),
             ("--ro-bind", str(bind_root), str(bind_root))]
    cmd = probe.sandbox(bwrap, binds, "/app", [sandbox_py, "-I", "-B", "/harness.py"])
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=probe.CASE_TIMEOUT)
    observed = "NOPAYLOAD(rc=%d)" % proc.returncode
    for line in proc.stdout.splitlines():
        if line.startswith("PAYLOAD "):
            observed = line.split(" ", 1)[1]
            break
    ok = observed == case["predicted"]
    mismatches += 0 if ok else 1
    print("CASE %s predicted=%s observed=%s ok=%s" % (case["id"], case["predicted"], observed, ok))
print("OBSERVATIONS_END")
print("mismatches %d" % mismatches)
shutil.rmtree(work / "cases", ignore_errors=True)
sys.exit(0 if mismatches == 0 else 1)

#!/usr/bin/env python3
"""Debug: stage C01 exactly like the probe and run the harness under py3.11, dumping stderr."""
import importlib.util
import json
import subprocess
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r95/ExecC1Rerun")
LANE = S / "lane"
spec = importlib.util.spec_from_file_location("r95probe", str(LANE / "plans" / "round95_vuln_probe.py"))
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
work = S / "w-py311dbg"
work.mkdir(parents=True, exist_ok=True)
cap = LANE / probe.CAP
table = json.loads((LANE / probe.TABLE).read_bytes().decode())
upstream = (cap / "upstream-bottle" / "bottle.py").read_bytes()
vuln = probe.vulnerable(upstream)
harness = work / "harness.py"
harness.write_text(probe.HARNESS, encoding="utf-8")
host_py = Path("/home/vgpnk/.local/bin/python3.11").resolve()
bind_root = host_py.parents[1]
case = table["cases"][0]
app, tests = probe.stage("/usr/bin/bwrap", case, cap, upstream, vuln, work / "cases" / case["id"])
cmd = probe.sandbox("/usr/bin/bwrap", [("--ro-bind", str(bind_root), str(bind_root))], "/app",
                    [str(host_py), "-I", "-B", "/harness.py"])
proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
print("RC", proc.returncode)
print("STDOUT_BEGIN")
print(proc.stdout)
print("STDOUT_END")
print("STDERR_BEGIN")
print(proc.stderr)
print("STDERR_END")

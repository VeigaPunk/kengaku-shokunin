#!/usr/bin/env python3
"""SentinelProbe-5 round 2: granular write probes (file targets, /data ops, ns-root
writability, /proc/sys DAC denial). Names/errnos only; no sysctl mutation possible
(uid 1000 vs root-owned 0644 files -> EACCES at open)."""
from __future__ import annotations

import importlib.util
import os
import subprocess
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r96/SentinelProbe")
LANE = S / "lane"
OUT = S / "out"
CAP = LANE / "corpus/evidence/round96/graders/multi-source-data-merger"

spec = importlib.util.spec_from_file_location("probe96", LANE / "plans" / "round96_merger_probe.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

E = (S / "E").resolve()
G = (S / "G").resolve()
STORE = probe.interpreter_root(E)
box = probe.Box("/usr/bin/bwrap", sorted({str(E), str(G), STORE, probe.interpreter_root(G)}))

P_WRITE2 = """
import os
store = %(store)s
e = %(e)s
g = %(g)s
for t in [store + "/SENTINEL", e + "/bin/SENTINEL", g + "/bin/SENTINEL",
          "/usr/bin/SENTINEL", "/data/SENTINEL", "/tests/SENTINEL"]:
    try:
        with open(t, "w") as f:
            f.write("x")
        print("WRITE_OK", t)
    except OSError as err:
        print("WRITE_DENIED", t, "errno", err.errno, os.strerror(err.errno))
print("DATA_LIST", sorted(os.listdir("/data")))
for op, fn in [("DATA_MKDIR", lambda: os.mkdir("/data/mkdir_sentinel")),
               ("DATA_REMOVE", lambda: os.remove("/data/source_b/users.csv")),
               ("DATA_CHMOD", lambda: os.chmod("/data/source_b/users.csv", 0o600))]:
    try:
        fn()
        print(op, "SUCCEEDED")
    except OSError as err:
        print(op, "errno", err.errno, os.strerror(err.errno))
try:
    os.makedirs("/etc")
    with open("/etc/SENTINEL", "w") as f:
        f.write("x")
    print("NS_ROOT_ETC_WRITE SUCCEEDED (namespaced tmpfs, ephemeral)")
except OSError as err:
    print("NS_ROOT_ETC errno", err.errno, os.strerror(err.errno))
try:
    with open("/fast/scratch/hyaku/kengaku-r96/SentinelProbe/OUTSIDE.txt", "w") as f:
        f.write("x")
    print("FAST_UNBOUND_PATH_WRITE SUCCEEDED")
except OSError as err:
    print("FAST_UNBOUND_PATH errno", err.errno, os.strerror(err.errno))
try:
    with open("/proc/sys/user/max_user_namespaces", "a") as f:
        f.write("x")
    print("PROC_SYS_WRITE SUCCEEDED")
except OSError as err:
    print("PROC_SYS_WRITE errno", err.errno, os.strerror(err.errno))
try:
    os.symlink("/data", "/tmp/link_data")
    print("SYMLINK_NS SUCCEEDED")
except OSError as err:
    print("SYMLINK_NS errno", err.errno)
""" % {"store": repr(str(STORE)), "e": repr(str(E)), "g": repr(str(G))}

pl = S / "pl/write2.py"
pl.write_text(P_WRITE2, encoding="utf-8")

cmd = box.cmd([("--bind", str(S / "wk/appdemo"), "/app"),
               ("--ro-bind", str(CAP / "environment/data"), "/data"),
               ("--ro-bind", str(S / "wk/tests"), "/tests"),
               ("--ro-bind", str(pl), "/payload.py")],
              "/app", "%s/bin:/usr/bin" % G, [str(probe.venv_python(G)), "-I", "-B", "/payload.py"])
proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
(OUT / "r5b-writes-granular.txt").write_text(
    "RC %d\nSTDOUT\n%s\nSTDERR\n%s" % (proc.returncode, proc.stdout, proc.stderr), encoding="utf-8")
print("DRIVER2 rc", proc.returncode)
print(proc.stdout)

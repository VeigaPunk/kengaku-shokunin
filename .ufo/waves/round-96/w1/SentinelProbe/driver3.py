#!/usr/bin/env python3
"""SentinelProbe-5 round 3: errno stability for read-only denial on /data and /usr,
plus open-flag variants. Denial (any errno) is the security property; the tally
characterizes which errno a forged run would observe."""
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

P_TALLY = """
import os
tally = {}
for i in range(12):
    for base, tag in [("/data", "DATA"), ("/usr", "USR"), ("/tests", "TESTS")]:
        p = "%s/sentinel_%d" % (base, i)
        try:
            open(p, "w").write("x")
            tally[(tag, "SUCCEEDED")] = tally.get((tag, "SUCCEEDED"), 0) + 1
        except OSError as e:
            k = (tag, "errno", e.errno)
            tally[k] = tally.get(k, 0) + 1
for k in sorted(tally, key=str):
    print("ERRNO_TALLY", k, tally[k])
for flags, tag in [(os.O_CREAT | os.O_WRONLY, "OCREAT_WRONLY"),
                   (os.O_WRONLY, "OWRONLY_EXISTING"),
                   (os.O_RDONLY, "ORDONLY_EXISTING")]:
    try:
        fd = os.open("/data/source_b/users.csv", flags)
        os.close(fd)
        print("OPENFLAG", tag, "SUCCEEDED")
    except OSError as e:
        print("OPENFLAG", tag, "errno", e.errno)
"""

pl = S / "pl/tally.py"
pl.write_text(P_TALLY, encoding="utf-8")
(S / "wk/tests2").mkdir(exist_ok=True)

for py_tag, py in (("E311", probe.venv_python(E)), ("G313", probe.venv_python(G))):
    cmd = box.cmd([("--bind", str(S / "wk/appdemo"), "/app"),
                   ("--ro-bind", str(CAP / "environment/data"), "/data"),
                   ("--ro-bind", str(S / "wk/tests2"), "/tests"),
                   ("--ro-bind", str(pl), "/payload.py")],
                  "/app", "%s/bin:/usr/bin" % py, [str(py), "-I", "-B", "/payload.py"])
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    (OUT / ("r5c-errno-tally-%s.txt" % py_tag)).write_text(
        "PY %s RC %d\nSTDOUT\n%s\nSTDERR\n%s" % (py_tag, proc.returncode, proc.stdout, proc.stderr),
        encoding="utf-8")
    print("TALLY", py_tag, "rc", proc.returncode)
    print(proc.stdout)

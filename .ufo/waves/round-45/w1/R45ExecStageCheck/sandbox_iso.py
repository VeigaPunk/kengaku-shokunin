#!/usr/bin/env python3
"""R45ExecStageCheck: what can a recipe reach inside the probe's own bwrap sandbox?

Builds the sandbox exactly as plans/password_recovery_probe.py does (its sandbox_argv / ENV, imported from
the clone), installs a harness that only *reports* the view, and prints it. Writes nothing on the host: the
one deliberate hostile write targets /home/vgpnk/R45-CANARY-PROBE, which must never appear on the host.
"""
import importlib.util
import pathlib
import shutil
import subprocess
import sys
import tempfile

LANE = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("prp", LANE / "plans/password_recovery_probe.py")
prp = importlib.util.module_from_spec(spec)
sys.modules["prp"] = prp
spec.loader.exec_module(prp)
cap = LANE / prp.CAP

HARNESS = r'''
import os
print("ROOT_ENTRIES " + repr(sorted(os.listdir("/"))))
for p in ("/home", "/fast", "/fast/scratch", "/app", "/pub", "/tests", "/proc"):
    print("EXISTS %s %s" % (p, os.path.exists(p)))
mt = [l for l in open("/proc/self/mounts") if not l.startswith(("proc ", "devpts "))]
print("MOUNTS %d" % len(mt))
for l in mt:
    print("MOUNT " + l.strip())
res = []
for p in ("/home/vgpnk/R45-CANARY-PROBE", "/app/write-ok", "/tmp/write-ok"):
    try:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            f.write("canary\n")
        res.append((p, "WROTE"))
    except OSError as e:
        res.append((p, "FAILED:" + type(e).__name__))
for p, r in res:
    print("WRITE %s %s" % (p, r))
print("HOST_HOME_LISTING " + repr(sorted(os.listdir("/home"))))
print("HOST_VGPNK_LISTING " + repr(sorted(os.listdir("/home/vgpnk"))[:10]))
'''

root = pathlib.Path(tempfile.mkdtemp(prefix="iso-", dir=sys.argv[2]))
work = pathlib.Path(tempfile.mkdtemp(prefix="kprp-", dir=root))
try:
    (work / "app").mkdir()
    (work / "tests").mkdir()
    (work / "zeros.bin").write_bytes(b"\0" * 65536)
    shutil.copyfile(cap / "tests/test_outputs.py", work / "tests" / "test_outputs.py")
    (work / "seed.sh").write_text(cap.joinpath("environment/setup.sh").read_text())
    (work / "recipe.sh").write_text(":\n")
    (work / "harness.py").write_text(HARNESS)
    p = subprocess.run(prp.sandbox_argv(cap, work) + ["/usr/bin/python3", "/harness.py", "stage"],
                       env=prp.ENV, capture_output=True, text=True, timeout=300)
    print("SANDBOX rc=%d" % p.returncode)
    print(p.stdout)
    if p.stderr:
        print("STDERR " + p.stderr.strip())
finally:
    shutil.rmtree(root, ignore_errors=True)

#!/usr/bin/env python3
"""Teardown/leak test: a setsid double-forked grandchild inside the frozen sandbox must not survive
(1) a SIGKILL of bwrap (the subprocess.run(timeout=300) path), (2) a normal exit."""
import importlib.util, pathlib, shutil, subprocess, sys, tempfile, time

LANE, ROOT = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("probe", str(pathlib.Path(LANE) / "plans/constraints_probe.py"))
probe = importlib.util.module_from_spec(spec); sys.modules["probe"] = probe; spec.loader.exec_module(probe)
cap = pathlib.Path(LANE) / probe.CAP
ENV = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "HOME": "/tmp", "LANG": "C.UTF-8"}
HOSTILE = r'''
import os, subprocess, time
open("/tmp/k41canary", "w").write("#!/bin/sh\nsleep 600\n"); os.chmod("/tmp/k41canary", 0o755)
subprocess.Popen(["/usr/bin/setsid", "--fork", "/bin/sh", "/tmp/k41canary"], start_new_session=True)
time.sleep(8)
print("HARNESS_DONE")
'''
def work(tag):
    w = pathlib.Path(tempfile.mkdtemp(prefix=tag + "-", dir=ROOT)); a = w / "app"; a.mkdir()
    for n in probe.INPUTS: shutil.copyfile(cap / n, a / n)
    (w / "recipe.sh").write_text(":\n"); (w / "harness.py").write_text(HOSTILE); return w
def ps(marker):
    return subprocess.run(["bash", "-c", f"ps -eo pid,ppid,args | grep -F {marker} | grep -v grep || true"],
                          capture_output=True, text=True).stdout.strip() or "(none)"

w = work("leak")
pr = subprocess.Popen(probe.sandbox_argv(cap, w) + ["/usr/bin/python3", "/harness.py", "grade"], env=ENV,
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(3.0)
print("GRANDCHILD_ALIVE_WHILE_SANDBOX_RUNS:", ps("/tmp/k41canary"))
pr.kill(); pr.wait(timeout=10)          # same shape as subprocess.run(timeout=...) killing bwrap
time.sleep(1.0)
print("AFTER_SIGKILL_BWRAP:", ps("/tmp/k41canary"))
shutil.rmtree(w, ignore_errors=True)

w = work("exit")
p = subprocess.run(probe.sandbox_argv(cap, w) + ["/usr/bin/python3", "/harness.py", "grade"], env=ENV,
                   capture_output=True, text=True, timeout=60)
print("NORMAL_RC", p.returncode, p.stdout.strip())
print("AFTER_NORMAL_EXIT:", ps("/tmp/k41canary"))
print("ZOMBIES:", subprocess.run(["bash", "-c", "ps -eo stat,pid,args | awk '$1 ~ /^Z/' | head -5"],
                                 capture_output=True, text=True).stdout.strip() or "(none)")
shutil.rmtree(w, ignore_errors=True)

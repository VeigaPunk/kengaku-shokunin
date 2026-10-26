#!/usr/bin/env python3
"""Round 5b: stdin inheritance + --bind following a symlinked /app source (frozen sandbox_argv)."""
import importlib.util, os, pathlib, shutil, subprocess, sys, tempfile

LANE, ROOT = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("probe", str(pathlib.Path(LANE) / "plans/constraints_probe.py"))
probe = importlib.util.module_from_spec(spec); sys.modules["probe"] = probe; spec.loader.exec_module(probe)
cap = pathlib.Path(LANE) / probe.CAP
ENV = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "HOME": "/tmp", "LANG": "C.UTF-8"}
STDIN_PROBE = r'''
import sys
try: d = sys.stdin.read(64)
except Exception as e: d = type(e).__name__
print("STDIN_READ", repr(d))
open("/app/hostmark", "w").write("written from sandbox")
'''
def work(tag, symlink_app=False):
    w = pathlib.Path(tempfile.mkdtemp(prefix=tag + "-", dir=ROOT))
    if symlink_app:
        target = w / "target"; target.mkdir()
        for n in probe.INPUTS: shutil.copyfile(cap / n, target / n)
        os.symlink(target, w / "app")
    else:
        a = w / "app"; a.mkdir()
        for n in probe.INPUTS: shutil.copyfile(cap / n, a / n)
    (w / "recipe.sh").write_text(":\n"); (w / "harness.py").write_text(STDIN_PROBE); return w

w = work("stdin")
p = subprocess.run(probe.sandbox_argv(cap, w) + ["/usr/bin/python3", "/harness.py", "grade"], env=ENV,
                   input="SECRET-PARENT-STDIN\n", capture_output=True, text=True, timeout=60)
print("WITH_PIPE_STDIN rc=%d out=%s" % (p.returncode, p.stdout.strip()))
print("APP_HOSTMARK_EXISTS", (w / "app" / "hostmark").exists())
print("WORK_ENTRIES", sorted(x.name for x in w.iterdir()))
shutil.rmtree(w, ignore_errors=True)

w = work("sym", symlink_app=True)
print("SYMLINK_APP_SOURCE_IS_LINK", (w / "app").is_symlink())
p = subprocess.run(probe.sandbox_argv(cap, w) + ["/usr/bin/python3", "/harness.py", "grade"], env=ENV,
                   capture_output=True, text=True, timeout=60)
print("SYMLINK_BIND rc=%d stderr=%s" % (p.returncode, p.stderr.strip()[:200]))
print("TARGET_GOT_WRITE", (w / "target" / "hostmark").exists())
shutil.rmtree(w, ignore_errors=True)

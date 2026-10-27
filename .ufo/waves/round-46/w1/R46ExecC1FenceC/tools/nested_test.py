import importlib.util, os, pathlib, subprocess, sys
lane = pathlib.Path(sys.argv[1]).resolve()
root = pathlib.Path(sys.argv[2]).resolve()
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
k44 = load(lane / "plans/round44_c1_verify.py", "k44")
root.mkdir(parents=True, exist_ok=True)
for n in ("fx", "btmp", "empty"):
    (root / n).mkdir(exist_ok=True)
d = root / "fx" / "fixture"
d.mkdir(parents=True, exist_ok=True)
env = {"PATH": k44.PATH, "HOME": "/nonexistent", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
subprocess.run(["git", "init", "-q", "-b", "master", str(d)], env=env, check=True)
(d / "a.txt").write_text("x\n")
subprocess.run(["git", "-C", str(d), "add", "-A"], env=env, check=True)
subprocess.run(["git", "-C", str(d), "-c", "user.email=a@b", "-c", "user.name=a", "commit", "-qm", "x"], env=env, check=True)
logdir = root / "strace"; logdir.mkdir(exist_ok=True)
inner = ["/usr/bin/bwrap", "--ro-bind", str(d), str(d),
         "--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64",
         "--symlink", "usr/bin", "/bin", "--symlink", "usr/bin", "/sbin",
         "--dev", "/dev", "--proc", "/proc", "--unshare-pid", "--unshare-net", "--unshare-ipc", "--die-with-parent",
         "--chdir", str(d), "/usr/bin/git", "-C", str(d), "rev-parse", "--show-toplevel",
         ]
outer = k44.ro_sandbox(writable=(logdir,), hide=k44.hide_list((lane,), existing=True), empty=root / "empty") + inner
r = subprocess.run(outer, capture_output=True, text=True, cwd=str(d), env=env, timeout=60)
print("OUTER rc=", r.returncode, "stdout=", r.stdout.strip()[-300:], "stderr=", r.stderr.strip()[-600:])
# the same inner alone, on the host
r2 = subprocess.run(inner, capture_output=True, text=True, cwd=str(d), env=env, timeout=60)
print("HOST-NESTED rc=", r2.returncode, "stdout=", r2.stdout.strip()[-200:], "stderr=", r2.stderr.strip()[-400:])
# with a commondir escape outside the bound d: should fail
out = root / "outside-store"; out.mkdir(exist_ok=True)
d2 = root / "fx" / "esc"; d2.mkdir(exist_ok=True)
(d2 / ".git").mkdir(exist_ok=True)
(d2 / ".git" / "commondir").write_text(str(out) + "\n")
(d2 / ".git" / "HEAD").write_text("ref: refs/heads/master\n")
inner2 = list(inner); inner2[2] = str(d2); inner2[3] = str(d2)
i = inner2.index("--chdir"); inner2[i+1] = str(d2)
i = inner2.index("-C"); inner2[i+1] = str(d2)
r3 = subprocess.run(inner2, capture_output=True, text=True, cwd=str(d2), env=env, timeout=60)
print("ESCAPE rc=", r3.returncode, "stdout=", r3.stdout.strip()[-200:], "stderr=", r3.stderr.strip()[-300:])

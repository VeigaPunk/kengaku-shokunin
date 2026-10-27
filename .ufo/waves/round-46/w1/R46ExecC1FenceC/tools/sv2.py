import importlib.util, os, pathlib, re, subprocess, sys
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
LANE = pathlib.Path(sys.argv[1]).resolve(); ROOT = pathlib.Path(sys.argv[2]).resolve()
k44 = load(LANE / "plans/round44_c1_verify.py", "k44_sv2")
for n in ("fx", "btmp", "empty"): (ROOT / n).mkdir(parents=True, exist_ok=True)
d = ROOT / "fx" / "mod" / "f000"; d.mkdir(parents=True, exist_ok=True)
(d / "a").write_text("x\n")
QUOTED = re.compile(r'"([^"]*)"')
def lines_for(log, d, root):
    out = []
    for line in log.read_text(errors="replace").splitlines():
        for m in QUOTED.finditer(line):
            p = m.group(1)
            if not p.startswith("/"): continue
            s = os.path.normpath(p)
            if not (s == str(root) or s.startswith(str(root) + "/")): continue
            if s == str(d) or s.startswith(str(d) + "/"): continue
            if s.startswith(str(root / "empty")): continue
            out.append(line[:200]); break
    return out
CORE = ["--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64",
        "--symlink", "usr/bin", "/bin", "--dev", "/dev", "--proc", "/proc",
        "--unshare-pid", "--unshare-net", "--die-with-parent"]
def run(tag, bwrap_args, env):
    logdir = ROOT / "log" / tag; logdir.mkdir(parents=True, exist_ok=True); log = logdir / "log"
    cmd = k44.ro_sandbox(writable=(logdir,), hide=k44.hide_list((LANE,), existing=True), empty=ROOT / "empty") + \
        ["/usr/bin/strace", "-f", "-qq", "-yy", "-e", "trace=%file", "-o", str(log),
         "/usr/bin/bwrap"] + CORE + bwrap_args
    r = subprocess.run(cmd, cwd=str(d), capture_output=True, text=True, timeout=120, env=env)
    bad = lines_for(log, d, ROOT)
    print(f"VARIANT {tag} rc={r.returncode} err={r.stderr.strip()[:100]!r} offenders={len(bad)}")
    for x in bad[:10]: print("   ", x)
env = {"PATH": k44.PATH, "HOME": "/nonexistent", "LC_ALL": "C"}
run("D-usr-only", ["/usr/bin/true"], env)
run("E-bind-d-true", ["--ro-bind", str(d), "/fixture", "--chdir", "/fixture", "/usr/bin/true"], env)
run("F-bind-d-git", ["--ro-bind", str(d), "/fixture", "--chdir", "/fixture", "/usr/bin/git", "-C", "/fixture", "rev-parse", "--show-toplevel"], env)
run("G-bind-d-abs-src-git", ["--ro-bind", str(d), "/fixture", "--chdir", "/fixture", "/usr/bin/git", "status"], env)
# H: no namespace at all, just git on d (control: how many scratch paths does plain git touch?)
logdir = ROOT / "log" / "H-plain-git"; logdir.mkdir(parents=True, exist_ok=True); log = logdir / "log"
cmd = k44.ro_sandbox(writable=(logdir,), hide=k44.hide_list((LANE,), existing=True), empty=ROOT / "empty") + \
    ["/usr/bin/strace", "-f", "-qq", "-yy", "-e", "trace=%file", "-o", str(log), "/usr/bin/git", "-C", str(d), "rev-parse", "--show-toplevel"]
r = subprocess.run(cmd, cwd=str(d), capture_output=True, text=True, timeout=120, env=env)
bad = lines_for(log, d, ROOT)
print(f"VARIANT H-plain-git rc={r.returncode} err={r.stderr.strip()[:100]!r} offenders={len(bad)}")
for x in bad[:10]: print("   ", x)

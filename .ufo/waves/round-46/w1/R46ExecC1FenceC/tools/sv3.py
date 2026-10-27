import importlib.util, os, pathlib, re, subprocess, sys
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
LANE = pathlib.Path(sys.argv[1]).resolve(); ROOT = pathlib.Path(sys.argv[2]).resolve()
k44 = load(LANE / "plans/round44_c1_verify.py", "k44_sv3")
for n in ("fx", "btmp", "empty"): (ROOT / n).mkdir(parents=True, exist_ok=True)
d = ROOT / "fx" / "mod" / "f000"; d.mkdir(parents=True, exist_ok=True)
env = {"PATH": k44.PATH, "HOME": "/nonexistent", "LC_ALL": "C"}
subprocess.run(["git", "init", "-q", "-b", "master", str(d)], env=env, check=True)
(d / "a").write_text("x\n"); subprocess.run(["git", "-C", str(d), "add", "-A"], env=env, check=True)
subprocess.run(["git", "-C", str(d), "-c", "user.email=a@b", "-c", "user.name=a", "commit", "-qm", "x"], env=env, check=True)
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
            out.append(line[:180]); break
    return out
CORE = ["--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64",
        "--symlink", "usr/bin", "/bin", "--dev", "/dev", "--proc", "/proc",
        "--unshare-pid", "--unshare-net", "--die-with-parent"]
def run(tag, src, cwd):
    logdir = ROOT / "log" / tag; logdir.mkdir(parents=True, exist_ok=True); log = logdir / "log"
    cmd = k44.ro_sandbox(writable=(logdir,), hide=k44.hide_list((LANE,), existing=True), empty=ROOT / "empty") + \
        ["/usr/bin/strace", "-f", "-qq", "-yy", "-e", "trace=%file", "-o", str(log),
         "/usr/bin/bwrap", "--ro-bind", src, "/fixture"] + CORE + ["--chdir", "/fixture",
         "/usr/bin/git", "-C", "/fixture", "rev-parse", "--show-toplevel", "--absolute-git-dir", "--git-common-dir"]
    r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=120, env=env)
    bad = lines_for(log, d, ROOT)
    print(f"VARIANT {tag} rc={r.returncode} out={r.stdout.strip()[:120]!r} err={r.stderr.strip()[:80]!r} offenders={len(bad)}")
    for x in bad[:8]: print("   ", x)
run("I-src-dot-cwd-d", ".", d)
run("J-src-basename-cwd-parent", "f000", d.parent)

#!/usr/bin/env python3
"""Sentinel probe 4: tracer env + output-path, build-child containment, leg-i parsing bypasses,
and the remediation shapes."""
import json, os, pathlib, shutil, subprocess, sys, time

S = pathlib.Path(os.environ["S"]).resolve()
PLANS = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans"
sys.path.insert(0, PLANS)
import round43_c1_verify as C

ENV = dict(C.PIN_CHECK_ENV)
BASE = S / "p4"
if BASE.exists():
    shutil.rmtree(BASE)
BASE.mkdir(parents=True)
CE = {"GIT_AUTHOR_NAME": "f", "GIT_AUTHOR_EMAIL": "f@x.invalid", "GIT_COMMITTER_NAME": "f",
      "GIT_COMMITTER_EMAIL": "f@x.invalid", "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+00:00",
      "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+00:00"}

def sh(argv, env=None, timeout=20, cwd=None):
    try:
        r = subprocess.run(argv, capture_output=True, text=True, env=env or ENV, cwd=cwd, timeout=timeout)
        return [r.returncode, r.stdout.strip()[-400:], r.stderr.strip()[-400:]]
    except subprocess.TimeoutExpired:
        return ["TIMEOUT", "", ""]

def note(name, **kw):
    print(json.dumps({"vector": name, **kw}, sort_keys=True), flush=True)

# ---------------------------------------------------------------- A: tracer output path follows a symlink?
sand = BASE / "tracer"
for sub in ("work", "tmp", "rtmp", "run", "outside"):
    (sand / sub).mkdir(parents=True)
leak = sand / "outside" / "leak.txt"
leak.write_text("UNTOUCHED\n")
slot = sand / "slot.py"
slot.write_text(
    "import os, sys\n"
    "t = os.environ['TMPDIR']\n"
    "try:\n"
    "    os.symlink(" + repr(str(leak)) + ", os.path.join(t, 'k43-trace.txt'))\n"
    "except OSError as e:\n"
    "    sys.stderr.write('symlink: %r\\n' % e)\n"
    "print('K43_SPAN' in os.environ, os.environ.get('K43_SPAN'))\n"
    "raise SystemExit(0)\n")
tracer = sand / "tracer" / "k43-tracer.py"
tracer.parent.mkdir(parents=True, exist_ok=True)
tracer.write_text(C.TRACER)
src = open(slot, "rb")
tsrc = open(tracer, "rb")
try:
    cmd = C.ro_sandbox(writable=(sand / "work", sand / "tmp"),
                       ro_data=((src.fileno(), C.SLOT), (tsrc.fileno(), C.TRACER_SLOT)),
                       empty=sand / "run") + ["/usr/bin/python3", C.TRACER_SLOT, C.SLOT]
    env = {"PATH": C.PATH, "HOME": "/nonexistent", "TMPDIR": str(sand / "tmp"), "K43_SPAN": "7,8",
           "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=120,
                       pass_fds=(src.fileno(), tsrc.fileno()))
    note("tracer output path is followed; sandbox writable set is work+tmp",
         rc=r.returncode, stdout=r.stdout.strip()[-200:], stderr=r.stderr.strip()[-200:],
         outside_target=leak.read_text().strip(),
         trace_file_after=(sand / "tmp" / "k43-trace.txt").is_symlink())
finally:
    src.close(); tsrc.close()

# does K43_SPAN reach the traced tool at all? (same run above printed it; untraced control)
untr = subprocess.run(["env", "-i", "PATH=" + C.PATH, "TMPDIR=" + str(sand / "tmp"),
                       "/usr/bin/python3", str(slot)], capture_output=True, text=True)
note("untraced run env has no K43_SPAN", stdout=untr.stdout.strip()[-80:])

# ---------------------------------------------------------------- B: build-child containment
bd = BASE / "build"
(bd / "destA").mkdir(parents=True)
(bd / "destB").mkdir(parents=True)
(bd / "tmp").mkdir()
(bd / "run").mkdir()
script = bd / "child.sh"
script.write_text(
    "#!/bin/bash\n"
    f"cd {bd}/destA\n"
    f"setsid bash -c 'sleep 3; echo late > {bd}/destA/late.txt; echo late2 > {bd}/destB/sibling.txt' "
    ">/dev/null 2>&1 &\n"
    f"echo now > {bd}/destA/now.txt\n"
    f"echo sib > {bd}/destB/sibling-now.txt 2>&1 || echo EROFS-sibling\n"
    "exit 0\n")
script.chmod(0o755)
cmd = C.ro_sandbox(writable=(bd / "destA", bd / "tmp"), empty=bd / "run") + ["/bin/bash", str(script)]
r = subprocess.run(cmd, capture_output=True, text=True, env={"PATH": C.PATH, "HOME": "/nonexistent"},
                   timeout=120)
immediate = sorted(p.name for p in (bd / "destA").iterdir())
time.sleep(5)
after = sorted(p.name for p in (bd / "destA").iterdir())
note("build-child containment (destA rw, destB ro, surviving commanded child)",
     rc=r.returncode, stderr=r.stderr.strip()[-200:], stderr_from_child=None,
     destA_immediate=immediate, destA_after_5s=after,
     destB=sorted(p.name for p in (bd / "destB").iterdir()))

# ---------------------------------------------------------------- C: leg-i parsing bypasses + remediation shapes
repo = BASE / "ord" / "repo"
repo.mkdir(parents=True)
sh(["git", "-C", str(repo), "init", "-q", "-b", "master"])
(repo / "claims").mkdir(); (repo / "claims" / "x").write_text("hi\n")
(repo / "README").write_text("r\n")
sh(["git", "-C", str(repo), "add", "-A"])
subprocess.run(["git", "-C", str(repo), "commit", "-qm", "f"], env=dict(ENV, **CE), capture_output=True)
d = BASE / "ord"
for argv in (["--lane", "repo", "--claims", "claims", "--receipt", "README"],
             ["--lane", "repo", "--claim", "claims", "--receipt", "README"],
             ["--lane", "repo", "--claim=claims", "--receipt", "README"],
             ["--lane", "repo", "--c", "claims", "--receipt", "README"],
             ["--lane", "repo", "--claims", "README", "--receip", "claims"],
             ["--lane", "repo", "--receipt", "claims", "--claims", "README"],
             ["--lane=repo", "--claims=claims", "--receipt=README"]):
    note("leg i " + " ".join(argv), result=C.order_argv_breach(d, argv))

# ---------------------------------------------------------------- D: remediation shapes
note("fix: absolute git dir inside d",
     gitdir=sh(["git", "-C", str(BASE / "p3fix" if False else repo), "rev-parse", "--absolute-git-dir"]),
     inside=True)
cfg = repo / ".git" / "config"
SEC = BASE / "ord" / "outside.cfg"
SEC.write_text("[core]\n\tworktree = /tmp/elsewhere\n")
cfg.write_text(cfg.read_text() + f"[include]\n\tpath = {SEC}\n")
note("fix: git config --local --no-includes",
     plain=sh(["git", "-C", str(repo), "config", "--get", "core.worktree"]),
     no_includes=sh(["git", "-C", str(repo), "config", "--local", "--no-includes", "--get", "core.worktree"]))
alt = repo / ".git" / "objects" / "info" / "alternates"
alt.parent.mkdir(parents=True, exist_ok=True)
alt.write_text("/tmp/does-not-exist/objects\n")
note("fix: alternates file presence is checkable", exists=alt.exists())
print("PROBE4 DONE")

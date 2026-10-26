#!/usr/bin/env python3
"""Sentinel probe 2: ceiling asymmetry, gitdir leakage, write-outside-d snapshot, symlink isolation,
leg-i abbreviation bypass end-to-end through the frozen counter."""
import json, os, pathlib, shutil, subprocess, sys

S = pathlib.Path(os.environ["S"]).resolve()
PLANS = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans"
sys.path.insert(0, PLANS)
import round43_c1_verify as C

ENV = dict(C.PIN_CHECK_ENV)
BASE = S / "p2"
if BASE.exists():
    shutil.rmtree(BASE)
BASE.mkdir(parents=True)
CE = {"GIT_AUTHOR_NAME": "f", "GIT_AUTHOR_EMAIL": "f@x.invalid", "GIT_COMMITTER_NAME": "f",
      "GIT_COMMITTER_EMAIL": "f@x.invalid", "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+00:00",
      "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+00:00"}

def sh(argv, timeout=15, env=None):
    try:
        r = subprocess.run(argv, capture_output=True, text=True, env=env or ENV, timeout=timeout)
        return [r.returncode, r.stdout.strip(), r.stderr.strip()[:200]]
    except subprocess.TimeoutExpired:
        return ["TIMEOUT", "", ""]

def commit(p):
    sh(["git", "-C", str(p), "add", "-A"])
    subprocess.run(["git", "-C", str(p), "commit", "-qm", "f"], env=dict(ENV, **CE), capture_output=True)

def mkrep(p, files=None):
    p = pathlib.Path(p); p.mkdir(parents=True, exist_ok=True)
    sh(["git", "-C", str(p), "init", "-q", "-b", "master"])
    for name, text in (files or {"README": "hello\n"}).items():
        q = p / name; q.parent.mkdir(parents=True, exist_ok=True); q.write_text(text)
    commit(p)
    return p

def note(name, **kw):
    print(json.dumps({"vector": name, **kw}, sort_keys=True))

def snap(p):
    out = []
    for t, ds, fs in os.walk(p):
        ds.sort()
        for f in sorted(fs):
            q = os.path.join(t, f)
            st = os.lstat(q)
            out.append(f"{os.path.relpath(q, p)}\0{st.st_mode}\0{st.st_size}\0{st.st_mtime_ns}")
    return out

# ---- 1. ceiling asymmetry: repo ABOVE d, --lane is a plain dir inside d
upg = mkrep(BASE / "upg" / "reporoot")
lane = BASE / "upg" / "plain" / "sub"
lane.mkdir(parents=True)
note("leg-i read escapes d upward (no GIT_CEILING_DIRECTORIES in PIN_CHECK_ENV)",
     pin_has_ceiling="GIT_CEILING_DIRECTORIES" in ENV,
     cat_file_no_ceiling=sh(["git", "-C", str(lane), "cat-file", "-t", "HEAD:README"]),
     cat_file_with_ceiling=sh(["git", "-C", str(lane), "cat-file", "-t", "HEAD:README"],
                              env=dict(ENV, GIT_CEILING_DIRECTORIES=str(BASE))),
     order_argv_breach=C.order_argv_breach(BASE / "upg" / "plain",
                                           ["--lane", "sub", "--claims", "README"]))
# the tool's own env DOES pin the ceiling (Runner.env) -- quote the line for the report
src = pathlib.Path(PLANS, "round43_c1_verify.py").read_text().splitlines()
for i, line in enumerate(src, 1):
    if "GIT_CEILING_DIRECTORIES" in line:
        print(f"LINE {i}: {line.strip()}")

# ---- 2. write-outside-d snapshot: gitdir outside d, aggressive config, three parent-side calls
outg = mkrep(BASE / "woutside" / "gitdir-src", {"README": "outside\n"})
victim = BASE / "woutside" / "f001"
victim.mkdir(parents=True)
(victim / "README").write_text("victim\n")
(victim / ".git").write_text(f"gitdir: {outg/'.git'}\n")
cfg = outg / ".git" / "config"
cfg.write_text(cfg.read_text() +
               "[gc]\n\tauto = 1\n\tautoPackLimit = 1\n[core]\n\tcommitGraph = true\n\tuntrackedCache = true\n"
               "[maintenance]\n\tauto = true\n[extensions]\n\tworktreeConfig = true\n"
               f"[core]\n\tworktree = {victim}\n")
before = snap(outg)
r = [sh(["git", "-C", str(victim), "rev-parse", "--show-toplevel"]),
     sh(["git", "-C", str(victim), "config", "--get", "core.worktree"]),
     sh(["git", "-C", str(victim), "cat-file", "-t", "HEAD:README"])]
after = snap(outg)
note("parent-side calls: writes outside d", calls=r, outside_tree_changed=before != after,
     added=sorted(set(after) - set(before))[:5], removed=sorted(set(before) - set(after))[:5])

# ---- 3. reverse read: outside gitdir serving HEAD content into leg i
SEC = outg / ".git"
note("outside gitdir is the fixture's real object store",
     cat_file_p=sh(["git", "-C", str(victim), "cat-file", "-p", "HEAD:README"]),
     gitdir=sh(["git", "-C", str(victim), "rev-parse", "--absolute-git-dir"]),
     inside_d=str(victim),
     gitdir_inside_d=None)
gd = sh(["git", "-C", str(victim), "rev-parse", "--absolute-git-dir"])[1]
note("repo_breach does not look at the git dir",
     repo_breach=C.repo_breach(BASE / "woutside"),
     gitdir_outside_d=not pathlib.Path(gd).resolve().is_relative_to((BASE / "woutside").resolve()))

# ---- 4. extensions.* / safe.directory no-ops
for k, v, sect in (("objectFormat", "sha256", "extensions"),
                   ("repositoryFormatVersion", "1", "core"),
                   ("safe", "true", "safe"),
                   ("directory", str(BASE), "safe")):
    p = mkrep(BASE / "ext" / f"{sect}-{k}")
    g = p / ".git" / "config"
    g.write_text(g.read_text() + f"[{sect}]\n\t{k} = {v}\n")
    note(f"config {sect}.{k}={v}", rev_parse=sh(["git", "-C", str(p), "rev-parse", "--show-toplevel"]),
         cat_file=sh(["git", "-C", str(p), "cat-file", "-t", "HEAD:README"]))
# objectformat must be set at init time to matter; also try a real sha256 repo
p = BASE / "ext" / "real-sha256"
p.mkdir(parents=True)
sh(["git", "-C", str(p), "init", "-q", "-b", "master", "--object-format=sha256"])
(p / "README").write_text("s\n"); commit(p)
note("real sha256 repo", cat_file=sh(["git", "-C", str(p), "cat-file", "-t", "HEAD:README"]),
     repo_breach=C.repo_breach(BASE / "ext"))

# ---- 5. symlink leg isolated shapes
def sl_case(name, build):
    d = BASE / "sl" / name / "f001"
    d.mkdir(parents=True)
    build(d)
    note("symlink " + name, result=C.symlink_breach(BASE / "sl" / name))

OUT = BASE / "sl" / "target"
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "x").write_text("x\n")
sl_case("inside-only", lambda d: (d / "a").symlink_to("b"))
sl_case("outside-file", lambda d: (d / "a").symlink_to(OUT / "x"))
sl_case("dangling-outside", lambda d: (d / "a").symlink_to(OUT / "nope"))
sl_case("relative-escape", lambda d: (d / "a").symlink_to("../../target/x"))
sl_case("absolute-inside", lambda d: (d / "a").write_text("") or (d / "b").symlink_to(d / "a"))
sl_case("symlink-to-dotdot-then-back", lambda d: (d / "a").symlink_to("../f001"))

print("PROBE2 DONE")

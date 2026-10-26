#!/usr/bin/env python3
"""Round-43 sentinel probe: the NEW parent-side git calls in plans/round43_c1_verify.py.

Every fixture is built under THIS script's own scratch root; every "outside" target is a sibling
directory inside the same scratch root. No vector names a real host path except /home/vgpnk/.gitconfig
(read-only, existence probed only) and /etc/os-release in the include-read demonstration.
"""
import json, os, pathlib, shutil, subprocess, sys, stat

S = pathlib.Path(os.environ["S"]).resolve()
PLANS = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans"
sys.path.insert(0, PLANS)
import round43_c1_verify as C

ENV = dict(C.PIN_CHECK_ENV)
BASE = S / "p1"
if BASE.exists():
    shutil.rmtree(BASE)
BASE.mkdir(parents=True)

def sh(argv, timeout=15):
    try:
        r = subprocess.run(argv, capture_output=True, text=True, env=ENV, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return "TIMEOUT", "", ""

def mkrep(p, commit_text="hello\n"):
    p = pathlib.Path(p)
    p.mkdir(parents=True, exist_ok=True)
    sh(["git", "-C", str(p), "init", "-q", "-b", "master"])
    (p / "README").write_text(commit_text)
    sh(["git", "-C", str(p), "add", "-A"])
    e = dict(ENV, GIT_AUTHOR_NAME="f", GIT_AUTHOR_EMAIL="f@x.invalid", GIT_COMMITTER_NAME="f",
             GIT_COMMITTER_EMAIL="f@x.invalid", GIT_AUTHOR_DATE="2026-01-01T00:00:00+00:00",
             GIT_COMMITTER_DATE="2026-01-01T00:00:00+00:00")
    subprocess.run(["git", "-C", str(p), "commit", "-qm", "f"], env=e, capture_output=True)
    return p

def cfg(p, text):
    g = pathlib.Path(p) / ".git" / "config"
    g.write_text(g.read_text() + text)

RES = []

def note(name, **kw):
    RES.append({"vector": name, **kw})
    print(json.dumps(RES[-1], sort_keys=True))

# ---------------------------------------------------------------- A: exec vectors
MARK = BASE / "marker"
SCRIPT = BASE / "runner.sh"
SCRIPT.write_text(f"#!/bin/sh\necho RAN >> {MARK}\nexit 0\n")
SCRIPT.chmod(0o755)
EXEC_KEYS = [
    ("core.fsmonitor", str(SCRIPT)),
    ("core.hooksPath", str(BASE / "hooks")),
    ("core.sshCommand", str(SCRIPT)),
    ("core.alternateRefsCommand", str(SCRIPT)),
    ("core.pager", str(SCRIPT)),
    ("core.editor", str(SCRIPT)),
    ("core.gitproxy", str(SCRIPT)),
    ("diff.external", str(SCRIPT)),
    ("filter.x.clean", str(SCRIPT)),
    ("credential.helper", str(SCRIPT)),
    ("uploadpack.packObjectsHook", str(SCRIPT)),
    ("gpg.program", str(SCRIPT)),
    ("sequence.editor", str(SCRIPT)),
    ("alias.rp", f"!{SCRIPT}"),
    ("alias.config", f"!{SCRIPT}"),
    ("alias.cat-file", f"!{SCRIPT}"),
    ("log.showSignature", "true"),
]
for k, v in EXEC_KEYS:
    p = mkrep(BASE / "exec" / k.replace(".", "-"))
    cfg(p, f'\n[{k.rsplit(".",1)[0]}]\n\t{k.rsplit(".",1)[1]} = {v}\n')
    rc1, o1, _e1 = sh(["git", "-C", str(p), "rev-parse", "--show-toplevel"])
    rc2, o2, _e2 = sh(["git", "-C", str(p), "config", "--get", "core.worktree"])
    rc3, o3, _e3 = sh(["git", "-C", str(p), "cat-file", "-t", "HEAD:README"])
    note("exec:" + k, rev_parse=[rc1, o1.strip()], config_get=[rc2, o2.strip()],
         cat_file=[rc3, o3.strip()], marker=MARK.exists())

# ---------------------------------------------------------------- B: include.path read of a file outside d
OUT = BASE / "outside"
OUT.mkdir(exist_ok=True)
SECRET = OUT / "secret.cfg"
SECRET.write_text("[core]\n\tworktree = /fast/scratch/hyaku/kengaku-r43/R43SentinelCounter/p1/outside/wt\n")
p = mkrep(BASE / "incl" / "repo")
cfg(p, f'\n[include]\n\tpath = {SECRET}\n')
d = p.parent
breach = C.repo_breach(d)
note("include.path outside d", repo_breach=breach,
     show_toplevel=sh(["git", "-C", str(p), "rev-parse", "--show-toplevel"]),
     config_worktree=sh(["git", "-C", str(p), "config", "--get", "core.worktree"]))
# does an include of a HOST config file succeed (a read outside d that the breach message can echo)?
p2 = mkrep(BASE / "incl" / "hostcfg")
cfg(p2, "\n[include]\n\tpath = /home/vgpnk/.gitconfig\n")
note("include.path host .gitconfig", config_get=sh(["git", "-C", str(p2), "config", "--get", "core.worktree"]),
     rc=sh(["git", "-C", str(p2), "rev-parse", "--show-toplevel"])[0])

# ---------------------------------------------------------------- C: .git FILE pointing outside d, worktree = the fixture
OUT_GIT = mkrep(OUT / "gitdir-src")
gdir = OUT_GIT / ".git"
victim = BASE / "gitfile" / "f001"
victim.mkdir(parents=True)
(victim / "README").write_text("inside\n")
sh(["git", "-C", str(OUT_GIT), "config", "core.worktree", str(victim)])
(victim / ".git").write_text(f"gitdir: {gdir}\n")
note("gitfile->outside gitdir, core.worktree=victim",
     repo_breach=C.repo_breach(BASE / "gitfile"),
     symlink_breach=C.symlink_breach(BASE / "gitfile"),
     show_toplevel=sh(["git", "-C", str(victim), "rev-parse", "--show-toplevel"]),
     cat_file=sh(["git", "-C", str(victim), "cat-file", "-t", "HEAD:README"]))

# same, but the outside gitdir is the REAL lane clone's .git shape (a repo whose objects the tool cannot see)
note("gitfile->outside gitdir: config readable?",
     config=sh(["git", "-C", str(victim), "config", "--list"])[0])

# ---------------------------------------------------------------- D: repo deeper than the walk's depth cap
deep = BASE / "deep" / "a" / "b" / "c" / "r"
deep.mkdir(parents=True)
sh(["git", "-C", str(deep), "init", "-q", "-b", "master"])
(deep / "README").write_text("deep\n")
sh(["git", "-C", str(deep), "add", "-A"])
subprocess.run(["git", "-C", str(deep), "commit", "-qm", "f"], env=dict(
    ENV, GIT_AUTHOR_NAME="f", GIT_AUTHOR_EMAIL="f@x.invalid", GIT_COMMITTER_NAME="f",
    GIT_COMMITTER_EMAIL="f@x.invalid", GIT_AUTHOR_DATE="2026-01-01T00:00:00+00:00",
    GIT_COMMITTER_DATE="2026-01-01T00:00:00+00:00"), capture_output=True)
WT = OUT / "wt-deep"
sh(["git", "-C", str(deep), "config", "core.worktree", str(WT)])
note("repo at depth 4, core.worktree outside",
     repo_breach=C.repo_breach(BASE / "deep"),
     show_toplevel=sh(["git", "-C", str(deep), "rev-parse", "--show-toplevel"]),
     config_worktree=sh(["git", "-C", str(deep), "config", "--get", "core.worktree"]))
note("repo at depth 2 for control", repo_breach=C.repo_breach(BASE / "deep" / "a" / "b"))

# ---------------------------------------------------------------- E: include.path = FIFO (parent-side hang)
FIFO = OUT / "fifo.cfg"
os.mkfifo(FIFO)
p3 = mkrep(BASE / "fifo" / "repo")
cfg(p3, f"\n[include]\n\tpath = {FIFO}\n")
note("include.path FIFO", config_get=sh(["git", "-C", str(p3), "config", "--get", "core.worktree"], timeout=5),
     rev_parse=sh(["git", "-C", str(p3), "rev-parse", "--show-toplevel"], timeout=5))

# ---------------------------------------------------------------- F: alternates outside d
ALT = mkrep(OUT / "alt-src")
(ALT / "SECRETBLOB").write_text("from-alternate\n")
sh(["git", "-C", str(ALT), "add", "-A"])
subprocess.run(["git", "-C", str(ALT), "commit", "-qm", "f"], env=dict(
    ENV, GIT_AUTHOR_NAME="f", GIT_AUTHOR_EMAIL="f@x.invalid", GIT_COMMITTER_NAME="f",
    GIT_COMMITTER_EMAIL="f@x.invalid", GIT_AUTHOR_DATE="2026-01-01T00:00:00+00:00",
    GIT_COMMITTER_DATE="2026-01-01T00:00:00+00:00"), capture_output=True)
sha = subprocess.run(["git", "-C", str(ALT), "rev-parse", "HEAD:SECRETBLOB"],
                     capture_output=True, text=True, env=ENV).stdout.strip()
p4 = mkrep(BASE / "alt" / "repo")
(p4 / ".git" / "objects" / "info").mkdir(parents=True, exist_ok=True)
(p4 / ".git" / "objects" / "info" / "alternates").write_text(str(ALT / ".git" / "objects") + "\n")
note("alternates outside d",
     cat_file=[sh(["git", "-C", str(p4), "cat-file", "-p", sha]),
               sh(["git", "-C", str(p4), "cat-file", "-t", sha])],
     repo_breach=C.repo_breach(BASE / "alt"))

# ---------------------------------------------------------------- G: upward escape with no ceiling
OUTER = BASE / "outer"
mkrep(OUTER / "reporoot")
plain = OUTER / "plain" / "sub"
plain.mkdir(parents=True)
note("no GIT_CEILING_DIRECTORIES: plain dir inside d, repo above d",
     show_toplevel=sh(["git", "-C", str(plain), "rev-parse", "--show-toplevel"]),
     cat_file=sh(["git", "-C", str(plain), "cat-file", "-t", "HEAD:README"]),
     ceiling_env_has_key="GIT_CEILING_DIRECTORIES" in ENV,
     with_ceiling=subprocess.run(["git", "-C", str(plain), "cat-file", "-t", "HEAD:README"],
                                 capture_output=True, text=True,
                                 env=dict(ENV, GIT_CEILING_DIRECTORIES=str(BASE))).returncode)

# ---------------------------------------------------------------- H: symlink leg, TOCTOU shapes
sl = BASE / "sym" / "f001"
sl.mkdir(parents=True)
(sl / "inside").write_text("i\n")
(sl / "ok_link").symlink_to("inside")
(sl / "out_link").symlink_to(OUT / "wt-deep")
(sl / "dangling").symlink_to(OUT / "does-not-exist")
note("symlink_breach", result=C.symlink_breach(BASE / "sym"))
note("symlink to inside only", result=C.symlink_breach(BASE / "sym" / "f001"), note="out_link present too")

# a symlinked DIRECTORY whose nested symlink leaves d (walk does not descend symlinks)
sl2 = BASE / "sym2" / "f001"
sl2.mkdir(parents=True)
(sl2 / "real").mkdir()
(sl2 / "ln").symlink_to("real")
(sl2 / "real" / "escape").symlink_to(OUT / "wt-deep")
note("nested symlink under an in-d symlinked dir", result=C.symlink_breach(BASE / "sym2"))

# ---------------------------------------------------------------- I: order_argv_breach parsing vs argparse
p5 = mkrep(BASE / "ord" / "repo")
(p5 / "claims").mkdir()
(p5 / "claims" / "x.txt").write_text("hi\n")
sh(["git", "-C", str(p5), "add", "-A"])
subprocess.run(["git", "-C", str(p5), "commit", "-qm", "f"], env=dict(
    ENV, GIT_AUTHOR_NAME="f", GIT_AUTHOR_EMAIL="f@x.invalid", GIT_COMMITTER_NAME="f",
    GIT_COMMITTER_EMAIL="f@x.invalid", GIT_AUTHOR_DATE="2026-01-01T00:00:00+00:00",
    GIT_COMMITTER_DATE="2026-01-01T00:00:00+00:00"), capture_output=True)
d5 = BASE / "ord"
note("order_argv_breach exact --claims tree", result=C.order_argv_breach(d5, ["--lane", "repo", "--claims", "claims", "--receipt", "README"]))
note("order_argv_breach abbreviated --claim tree", result=C.order_argv_breach(d5, ["--lane", "repo", "--claim", "claims", "--receipt", "README"]))
note("order_argv_breach abbreviated --receip README", result=C.order_argv_breach(d5, ["--lane", "repo", "--claims", "README", "--receip", "claims"]))
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("--lane"); ap.add_argument("--claims"); ap.add_argument("--receipt")
try:
    ns = ap.parse_args(["--lane", "repo", "--claim", "claims", "--receip", "README"])
    argp = {"claims": ns.claims, "receipt": ns.receipt}
except SystemExit as e:
    argp = {"argparse_exit": e.code}
note("argparse accepts the abbreviations order_check.py would use", parsed=argp)
note("order_argv_breach with = form", result=C.order_argv_breach(d5, ["--lane=repo", "--claims=claims"]))
note("order_argv_breach gitlink check path", result=C.order_argv_breach(d5, ["--lane", "repo", "--claims", "nope", "--receipt", "README"]))

print("PROBE1 DONE", len(RES))

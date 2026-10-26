#!/usr/bin/env python3
"""Sentinel probe 3: corrected upward-discovery asymmetry, git-dir remediation probe, and two
escape-shaped order fixtures pushed through the FROZEN counter end to end."""
import json, os, pathlib, shutil, subprocess, sys

S = pathlib.Path(os.environ["S"]).resolve()
PLANS = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans"
sys.path.insert(0, PLANS)
import round43_c1_verify as C

ENV = dict(C.PIN_CHECK_ENV)
BASE = S / "p3"
if BASE.exists():
    shutil.rmtree(BASE)
BASE.mkdir(parents=True)
CE = {"GIT_AUTHOR_NAME": "f", "GIT_AUTHOR_EMAIL": "f@x.invalid", "GIT_COMMITTER_NAME": "f",
      "GIT_COMMITTER_EMAIL": "f@x.invalid", "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+00:00",
      "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+00:00"}

def sh(argv, env=None, timeout=20):
    try:
        r = subprocess.run(argv, capture_output=True, text=True, env=env or ENV, timeout=timeout)
        return [r.returncode, r.stdout.strip(), r.stderr.strip()[:300]]
    except subprocess.TimeoutExpired:
        return ["TIMEOUT", "", ""]

def commit(p):
    sh(["git", "-C", str(p), "add", "-A"])
    subprocess.run(["git", "-C", str(p), "commit", "-qm", "f"], env=dict(ENV, **CE), capture_output=True)

def note(name, **kw):
    print(json.dumps({"vector": name, **kw}, sort_keys=True))

# ---- 1. corrected: the repo is an ANCESTOR of the fixture dir, i.e. above d
root = BASE / "upgc"
(root / "plain" / "sub").mkdir(parents=True)
sh(["git", "-C", str(root), "init", "-q", "-b", "master"])
(root / "README").write_text("anchored\n")
commit(root)
d = root / "plain"
note("repo above d found by discovery (no ceiling)",
     d=str(d), repo_root=str(root),
     no_ceiling=sh(["git", "-C", str(d / "sub"), "rev-parse", "--show-toplevel"]),
     cat_file_no_ceiling=sh(["git", "-C", str(d / "sub"), "cat-file", "-t", "HEAD:README"]),
     with_ceiling=sh(["git", "-C", str(d / "sub"), "cat-file", "-t", "HEAD:README"],
                     env=dict(ENV, GIT_CEILING_DIRECTORIES=str(d))),
     repo_breach_d=C.repo_breach(d),
     leg_i=C.order_argv_breach(d, ["--lane", "sub", "--claims", "README", "--receipt", "README"]))

# ---- 2. remediation probe: absolute git dir escapes d while every leg stays silent
gdroot = BASE / "gd"
d1 = gdroot / "f001"
gdir = gdroot / "side" / "gitdir"
gdir.parent.mkdir(parents=True)
note("separate-git-dir init", rc=sh(["git", "init", "-q", "-b", "master",
                                     "--separate-git-dir", str(gdir), str(d1)])[0])
(d1 / "claims.md").write_text("x\n")
sh(["git", "-C", str(d1), "add", "-A"])
subprocess.run(["git", "-C", str(d1), "commit", "-qm", "f"], env=dict(ENV, **CE), capture_output=True)
absgd = sh(["git", "-C", str(d1), "rev-parse", "--absolute-git-dir"])
note("separate git dir outside d",
     dot_git=(d1 / ".git").read_text().strip(),
     absolute_git_dir=absgd,
     inside_d=pathlib.Path(absgd[1]).resolve().is_relative_to(d1.resolve()) if absgd[0] == 0 else None,
     repo_breach=C.repo_breach(gdroot),
     symlink_breach=C.symlink_breach(gdroot),
     show_toplevel=sh(["git", "-C", str(d1), "rev-parse", "--show-toplevel"]))

# ---- 3. the battery module (built by the frozen builder, then run by the frozen counter)
BAT = BASE / "bat"
BAT.mkdir()
(BAT / "m_escape.py").write_text('''
import pathlib

def _order_fixture(d, gdname, wtname, claims, receipt, expect):
    return None

def f_gitdir(ctx, d):
    """A worktree whose git dir lives beside it, not under it."""
    gd = pathlib.Path(d).parent / "side" / "gitdir"
    ctx.write(pathlib.Path(gd).parent / ".keep", "")
    ctx.sh("git", "init", "-q", "-b", "master", "--separate-git-dir", str(gd), str(d))
    ctx.write(pathlib.Path(d) / ".ufo/waves/round-42/claims/round-42-claims.md", "nothing ran\\n")
    ctx.git(d, "add", "-A")
    ctx.git(d, "commit", "-qm", "claims")
    ctx.write(pathlib.Path(d) / "corpus/evidence/round42/receipt.txt", "receipt\\n")
    ctx.git(d, "add", "-A")
    ctx.git(d, "commit", "-qm", "receipt")
    return ["--lane", ".", "--claims", ".ufo/waves/round-42/claims/round-42-claims.md",
            "--receipt", "corpus/evidence/round42/receipt.txt"]

def f_deep(ctx, d):
    """A repo four levels down whose work tree is outside d."""
    key = "co" + "re.worktree"
    r = pathlib.Path(d) / "x" / "y" / "z" / "r"
    ctx.init(r)
    ctx.write(r / "claims.md", "x\\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "f")
    ctx.sh("git", "-C", str(r), "config", key, str(pathlib.Path(d).parent / "wt"))
    return ["--lane", "x/y/z/r", "--claims", "claims.md", "--receipt", "claims.md"]

FIXTURES = [
    {"fid": "esc-gitdir-outside", "tool": "order", "expect": "accept", "defects": [], "build": f_gitdir},
    {"fid": "esc-deep-worktree", "tool": "order", "expect": "error", "defects": [], "build": f_deep},
]
''')
built = subprocess.run(["/usr/bin/python3", str(BASE.parent / "lane/plans/round43_c1_verify.py"),
                        "--build-module", str(BAT / "m_escape.py"), "--dest", str(BASE / "built")],
                       capture_output=True, text=True, env=dict(ENV, PYTHONDONTWRITEBYTECODE="1"))
line = [l for l in built.stdout.splitlines() if l.startswith("BUILT ")]
note("builder accepted the module", rc=built.returncode, stderr=built.stderr.strip()[-300:],
     fixtures=[fx["fid"] for fx in json.loads(line[0][6:])] if line else None)
for k, fx in enumerate(json.loads(line[0][6:]) if line else []):
    d = BASE / "built" / f"f{k:03d}"
    r = subprocess.run(["/usr/bin/python3", str(BASE.parent / "lane/plans/order_check.py"), *fx["argv"]],
                       capture_output=True, text=True, env=dict(ENV, **CE), cwd=str(d), timeout=60)
    r = [r.returncode, r.stdout.strip(), r.stderr.strip()]
    note("order_check on " + fx["fid"], rc=r[0], out=r[1].splitlines()[-3:] if r[1] else "", err=r[2])
print("PROBE3 DONE")

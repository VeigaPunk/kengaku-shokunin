#!/usr/bin/env python3
"""Is the `_probe` core.worktree git leg ever reachable in its rc==0 branch?

The collection pass (fact 5) refuses any `core.worktree` value that does not resolve to the repo, so for the
git leg to be entered with a value the fence's own parser admitted, the value must be one the parser maps
onto the repo directory; git then resolves it relative to the gitdir. This probe builds exactly those configs
and reports, for the landed fence's own GIT_ENV: whether the fence admits, and what the three `_probe` git
calls return (so an rc==0 reachability claim is measured, not assumed).

usage: python3 worktree_leg_probe.py <landed.py> <root>
"""
import importlib.util
import pathlib
import subprocess
import sys

FENCE, ROOT = sys.argv[1], pathlib.Path(sys.argv[2]).resolve()
ROOT.mkdir(parents=True, exist_ok=True)

spec = importlib.util.spec_from_file_location("fence_wtl", FENCE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

GENV = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "HOME": str(ROOT / "nohome"),
        "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}

VALUES = [".", "./", "sub/..", "", '"./."', "x/.."]


def build(name, value):
    d = ROOT / "cases" / name / "d"
    d.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", str(d)], env=GENV, check=True, capture_output=True)
    (d / "sub").mkdir(exist_ok=True)
    with (d / ".git" / "config").open("a") as fh:
        fh.write(f"[core]\n\tworktree = {value}\n")
    return d


print("VALUE            ADMIT/BREACH(reason)                        toplevel_rc  gitdir_rc  wt_rc  wt_out")
for i, v in enumerate(VALUES):
    d = build(f"c{i}", v)
    verdict = m.breach(d, ["--lane", str(d)], "anchor")
    env = dict(m.GIT_ENV, GIT_CEILING_DIRECTORIES=str(d.parent))
    def run(*args):
        r = subprocess.run(["git", "-C", str(d), *args], capture_output=True, text=True, env=env,
                           stdin=subprocess.DEVNULL, timeout=30)
        return r.returncode, r.stdout.strip()
    t = run("rev-parse", "--show-toplevel")
    g = run("rev-parse", "--absolute-git-dir")
    w = run("config", "--local", "--no-includes", "--get", "core.worktree")
    print(f"{v!r:<16} {(verdict or 'ADMIT')[:46]:<46} {t[0]:<12} {g[0]:<10} {w[0]:<6} {w[1]!r}")

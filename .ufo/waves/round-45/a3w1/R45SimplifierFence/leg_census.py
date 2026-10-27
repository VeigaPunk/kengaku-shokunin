#!/usr/bin/env python3
"""Leg census for the landed fixture_fence: measures which helpers and which checks actually execute.

Instruments the landed module text with counters (no behaviour change beyond list appends) and replays
the same tree x argv matrix as diff_driver.py, reporting:
  CALLS        per-function call counts (are all five helpers reached?)
  TYPES        every `val` type seen at fact 2, and whether `val is True or isinstance(val, str)` was
               false even once (i.e. whether the `not isinstance(val, str)` disjunct ever decides)
  TARGETS      cases where `targets` carried a duplicate (would the `set()` in `sorted(set(targets))` matter?)
  WORKTREELEG  outcome of the `git config --local --get core.worktree` probe in _probe: rc values and
               whether it ever produced a breach

usage: python3 leg_census.py <landed.py> <root>
"""
import importlib.util
import os
import pathlib
import subprocess
import sys

OLD, ROOT = sys.argv[1], pathlib.Path(sys.argv[2]).resolve()
ROOT.mkdir(parents=True, exist_ok=True)
GENV = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "HOME": str(ROOT / "nohome"), "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}

src = pathlib.Path(OLD).read_text()


def splice(old, new):
    global src
    assert src.count(old) == 1, f"anchor not unique: {old!r}"
    src = src.replace(old, new, 1)


# fact 2 value types
splice("    for opt, val in vals.items():\n        if val is True or not isinstance(val, str) or val.startswith(\"{\"):\n",
       "    for opt, val in vals.items():\n"
       "        _VALS.append(val)\n"
       "        if val is True or not isinstance(val, str) or val.startswith(\"{\"):\n")
# targets list before the set() dedupe
splice("    for repo, need_root in sorted(set(targets)):\n",
       "    _TARGETS.append(tuple(targets))\n"
       "    for repo, need_root in sorted(set(targets)):\n")
# core.worktree git leg rc
splice('    wt = _git(repo, ceiling, "config", "--local", "--no-includes", "--get", "core.worktree")\n',
       '    wt = _git(repo, ceiling, "config", "--local", "--no-includes", "--get", "core.worktree")\n'
       '    _WTLEG.append(wt[0] if wt else "hung")\n')
inst_src = ("_VALS = []\n_TARGETS = []\n_WTLEG = []\n" + src)
(ROOT / "census.py").write_text(inst_src)

spec = importlib.util.spec_from_file_location("fence_census", ROOT / "census.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

CALLS = {}

def prof(frame, event, arg):
    if event == "call" and frame.f_code.co_filename == str(ROOT / "census.py"):
        name = frame.f_code.co_name
        CALLS[name] = CALLS.get(name, 0) + 1
    return prof

mod.__dict__["_VALS"], mod.__dict__["_TARGETS"], mod.__dict__["_WTLEG"] = [], [], []


def git_init(d):
    r = subprocess.run(["git", "init", "-q", str(d)], env=GENV, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr


def mk(name):
    root = ROOT / "cases" / name
    d = root / "d"
    d.mkdir(parents=True, exist_ok=True)
    return root, d


def shapes():
    out = []

    def add(fn):
        out.append(fn)

    def e(_):
        return mk("empty")

    add(e)

    def repo(_):
        r, d = mk("repo")
        git_init(d)
        return r, d
    add(repo)

    def subt(_):
        r, d = mk("repo_sub")
        git_init(d / "sub")
        return r, d
    add(subt)

    def gitfile(_):
        r, d = mk("gitfile")
        (d / ".git").write_text("gitdir: /tmp/elsewhere\n")
        return r, d
    add(gitfile)

    def wto(_):
        r, d = mk("worktree_out")
        git_init(d)
        with (d / ".git" / "config").open("a") as fh:
            fh.write(f"[core]\n\tworktree = {r / 'elsewhere'}\n")
        return r, d
    add(wto)

    def wtdot(_):
        r, d = mk("worktree_dot")
        git_init(d)
        with (d / ".git" / "config").open("a") as fh:
            fh.write("[core]\n\tworktree = .\n")
        return r, d
    add(wtdot)

    def wtempty(_):
        r, d = mk("worktree_empty")
        git_init(d)
        with (d / ".git" / "config").open("a") as fh:
            fh.write("[core]\n\tworktree\n")
        return r, d
    add(wtempty)

    def above(_):
        r, d = mk("above")
        (r / ".git").mkdir(exist_ok=True)
        return r, d
    add(above)

    def twoabove(_):
        r, d = mk("twoabove")
        (r / ".git").mkdir(exist_ok=True)
        d2 = r / "mid" / "d"
        d2.mkdir(parents=True)
        return r, d2
    add(twoabove)

    def inc(_):
        r, d = mk("include")
        git_init(d)
        with (d / ".git" / "config").open("a") as fh:
            fh.write("[include]\n\tpath = /etc/passwd\n")
        return r, d
    add(inc)

    def bare(_):
        r, d = mk("bare")
        git_init(d)
        with (d / ".git" / "config").open("a") as fh:
            fh.write("[core]\n\tbare = true\n")
        return r, d
    add(bare)
    return out


ARGS = [
    ("order", lambda d: ["--lane", str(d), "--claims", "c.txt", "--receipt", "r.txt"]),
    ("anchor", lambda d: ["--lane", str(d)]),
    ("anchor", lambda d: ["--lane", "{L}", "--evidence-ref", "{R}"]),
    ("anchor", lambda d: ["--lane", "../x"]),
    ("anchor", lambda d: ["--verbose", "--lane", str(d)]),
    ("anchor", lambda d: []),
    ("order", lambda d: []),
    ("zzz", lambda d: ["--lane", str(d)]),
]

sys.setprofile(prof)
cases = 0
for sh in shapes():
    root, d = sh(None)
    for tool, mkargv in ARGS:
        cases += 1
        try:
            mod.breach(pathlib.Path(d), list(mkargv(d)), tool)
        except BaseException:                                    # noqa: BLE001 - census only
            pass
sys.setprofile(None)

vals = mod.__dict__["_VALS"]
nontrivial = [v for v in vals if not (v is True or isinstance(v, str))]
types = sorted({type(v).__name__ for v in vals})
tg = mod.__dict__["_TARGETS"]
dup = [t for t in tg if len(set(t)) != len(t)]
wt = mod.__dict__["_WTLEG"]
print(f"CASES {cases}")
print(f"CALLS " + " ".join(f"{k}={v}" for k, v in sorted(CALLS.items())))
print(f"TYPES fact2_values={len(vals)} types={types} values_neither_True_nor_str={len(nontrivial)}")
print(f"TARGETS cases={len(tg)} with_duplicates={len(dup)}")
print(f"WORKTREELEG calls={len(wt)} rc0={wt.count(0)} rc1={wt.count(1)} other={len(wt) - wt.count(0) - wt.count(1)}")

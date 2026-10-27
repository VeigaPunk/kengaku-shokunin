#!/usr/bin/env python3
"""Differential equivalence driver: landed plans/fixture_fence.py (OLD) vs the simplified candidate (NEW).

For every (tree shape x argv shape x tool x d-shape) case the two modules are loaded side by side and
breach() must return the same value (or raise the same exception type). Trees are built under $S only.
usage: python3 diff_driver.py <OLD> <NEW> <root>
"""
import importlib.util
import os
import pathlib
import subprocess
import sys

OLD, NEW, ROOT = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3]).resolve()
ROOT.mkdir(parents=True, exist_ok=True)
FAKEHOME = ROOT / "home"
FAKEHOME.mkdir(exist_ok=True)
GENV = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": str(FAKEHOME), "LANG": "C.UTF-8"}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


old = load(OLD, "fence_old")
new = load(NEW, "fence_new")


def git_init(d):
    r = subprocess.run(["git", "init", "-q", str(d)], env=GENV, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert subprocess.run(["git", "-C", str(d), "rev-parse", "--show-toplevel"], env=GENV,
                          capture_output=True, text=True).stdout.strip() == str(d)


def mk(name):
    root = ROOT / "cases" / name
    d = root / "d"
    d.mkdir(parents=True, exist_ok=True)
    return root, d


def t_empty(_):
    return mk("empty")


def t_repo(_):
    root, d = mk("repo")
    git_init(d)
    (d / "a.txt").write_text("x\n")
    return root, d


def t_repo_sub(_):
    root, d = mk("repo_sub")
    git_init(d / "sub")
    return root, d


def t_gitfile(_):
    root, d = mk("gitfile")
    (d / ".git").write_text("gitdir: /tmp/elsewhere\n")
    return root, d


def t_symlink_out(_):
    root, d = mk("symlink_out")
    (root / "outside.txt").write_text("x\n")
    os.symlink(root / "outside.txt", d / "link")
    return root, d


def t_symlink_in(_):
    root, d = mk("symlink_in")
    (d / "real.txt").write_text("x\n")
    os.symlink(d / "real.txt", d / "link")
    return root, d


def t_fifo(_):
    root, d = mk("fifo")
    os.mkfifo(d / "p")
    return root, d


def t_above(_):
    root, d = mk("above")
    (root / ".git").mkdir(exist_ok=True)
    return root, d


def t_include(_):
    root, d = mk("include")
    git_init(d)
    with (d / ".git" / "config").open("a") as fh:
        fh.write('[include]\n\tpath = /etc/passwd\n')
    return root, d


def t_commondir(_):
    root, d = mk("commondir")
    git_init(d)
    (d / ".git" / "commondir").write_text("../x\n")
    return root, d


def t_alternates(_):
    root, d = mk("alternates")
    git_init(d)
    (d / ".git" / "objects" / "info").mkdir(parents=True, exist_ok=True)
    (d / ".git" / "objects" / "info" / "alternates").write_text("/tmp/other/objects\n")
    return root, d


def t_worktreecfg(_):
    root, d = mk("worktreecfg")
    git_init(d)
    with (d / ".git" / "config").open("a") as fh:
        fh.write('[extensions]\n\tworktreeConfig = true\n')
    return root, d


def t_bare(_):
    root, d = mk("bare")
    git_init(d)
    with (d / ".git" / "config").open("a") as fh:
        fh.write('[core]\n\tbare = true\n')
    return root, d


def t_worktree_out(_):
    root, d = mk("worktree_out")
    git_init(d)
    with (d / ".git" / "config").open("a") as fh:
        fh.write(f'[core]\n\tworktree = {root / "elsewhere"}\n')
    return root, d


def t_manyrepos(_):
    root, d = mk("manyrepos")
    for i in range(65):
        (d / f"r{i}" / ".git").mkdir(parents=True, exist_ok=True)
    return root, d


def t_cfg_notregular(_):
    root, d = mk("cfg_dir")
    git_init(d)
    (d / ".git" / "config.d").mkdir(exist_ok=True)
    return root, d


TREES = [t_empty, t_repo, t_repo_sub, t_gitfile, t_symlink_out, t_symlink_in, t_fifo, t_above,
         t_include, t_commondir, t_alternates, t_worktreecfg, t_bare, t_worktree_out, t_manyrepos,
         t_cfg_notregular]

b = ROOT / "notadir"
b.write_text("x\n") if not b.exists() else None
ABSENT = ROOT / "absent"


def argv_cases(d):
    rel = os.path.relpath(d, d)
    return [
        ("order-full", ["--lane", str(d), "--claims", "c.txt", "--receipt", "r.txt"], "order"),
        ("order-five", ["--lane", str(d), "--claims", "c.txt", "--receipt"], "order"),
        ("order-seven", ["--lane", str(d), "--claims", "c.txt", "--receipt", "r.txt", "x"], "order"),
        ("order-wrongtok", ["--lane", str(d), "--claims", "c.txt", "--receipts", "r.txt"], "order"),
        ("order-empty", [], "order"),
        ("anchor-empty", [], "anchor"),
        ("anchor-lane-abs", ["--lane", str(d)], "anchor"),
        ("anchor-lane-rel", ["--lane", rel], "anchor"),
        ("anchor-lane-dotdot", ["--lane", "../outside"], "anchor"),
        ("anchor-lane-absout", ["--lane", "/etc"], "anchor"),
        ("anchor-lane-token", ["--lane", "{LANE}"], "anchor"),
        ("anchor-lane-noval", ["--lane"], "anchor"),
        ("anchor-unknown", ["--frobnicate"], "anchor"),
        ("anchor-verbose", ["--verbose"], "anchor"),
        ("anchor-verbose-lane", ["--verbose", "--lane", str(d)], "anchor"),
        ("anchor-evref-out", ["--lane", str(d), "--evidence-ref", "/etc/passwd"], "anchor"),
        ("anchor-evref-rel", ["--lane", str(d), "--evidence-ref", "ev/x.txt"], "anchor"),
        ("tool-other", ["--lane", str(d)], "zzz"),
        ("tool-empty", ["--lane", str(d)], ""),
    ]


def call(mod, d, argv, tool):
    try:
        return ("ret", mod.breach(pathlib.Path(d), list(argv), tool))
    except BaseException as e:                                    # noqa: BLE001 - compare failures too
        return ("exc", type(e).__name__, str(e))


rows, bad = 0, []
for fn in TREES:
    root, d = fn(None)
    for label, argv, tool in argv_cases(d):
        a, c = call(old, d, argv, tool), call(new, d, argv, tool)
        rows += 1
        if a != c:
            bad.append((fn.__name__, label, a, c))
for dshape, d in (("absent", ABSENT), ("notadir", b)):
    for label, argv, tool in argv_cases(d):
        a, c = call(old, d, argv, tool), call(new, d, argv, tool)
        rows += 1
        if a != c:
            bad.append((dshape, label, a, c))
print(f"DIFF cases={rows} mismatches={len(bad)}")
for r in bad[:10]:
    print("MISMATCH", r)
sys.exit(1 if bad else 0)

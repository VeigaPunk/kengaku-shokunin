#!/usr/bin/env python3
"""Differential + dead-path evidence for the fixture_fence simplification.

Part A (structural): the LANDED module is copied with two probe counters injected around fact 3 —
`_ITERS.append("entry")` just before `anc = d.parent` and `_ITERS.append("iter")` as the first line of
the `while True:` body. Running the whole tree x argv matrix then shows, for every case that reaches
fact 3, that the loop body ran exactly once (iterations == entries). If that holds everywhere, the loop
can only ever execute one iteration, so collapsing it to a single `if` cannot change a decision.

Part B (behavioural): landed and candidate are loaded side by side and must return identical results
(same reason string, or same exception type and message) for every case.

usage: python3 diff_driver.py <landed.py> <candidate.py> <root>
Writes only under <root>. Exit 0 = identical + loop single-iteration everywhere, 1 = divergence.
"""
import importlib.util
import os
import pathlib
import subprocess
import sys

OLD, NEW, ROOT = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3]).resolve()
ROOT.mkdir(parents=True, exist_ok=True)
GENV = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "HOME": str(ROOT / "nohome"), "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


old = load(OLD, "fence_old")
new = load(NEW, "fence_new")

# ---- Part A: instrumented copy of the landed module (fact-3 entry / iteration counters) ----
inst_src = pathlib.Path(OLD).read_text()
anchor = "    anc = d.parent\n    while True:\n"
assert inst_src.count(anchor) == 1, "instrumentation anchor not unique"
inst_src = inst_src.replace(
    anchor,
    '    _ITERS.append("entry")\n    anc = d.parent\n    while True:\n        _ITERS.append("iter")\n', 1)
inst_src = "_ITERS = []\n" + inst_src
(ROOT / "inst.py").write_text(inst_src)
inst = load(ROOT / "inst.py", "fence_inst")


def git_init(d):
    r = subprocess.run(["git", "init", "-q", str(d)], env=GENV, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr


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


def t_symlink_dir_out(_):
    root, d = mk("symlink_dir_out")
    (root / "outdir").mkdir(exist_ok=True)
    os.symlink(root / "outdir", d / "outdir")
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


def t_above2(_):
    root, d = mk("above2")
    (root / ".git").mkdir(exist_ok=True)
    d2 = root / "mid" / "d"
    d2.mkdir(parents=True)
    return root, d2


def t_twoabove(_):
    root, d = mk("twoabove")
    (root / ".git").mkdir(exist_ok=True)
    d2 = root / "mid" / "d"
    d2.mkdir(parents=True)
    return root, d2


def t_include(_):
    root, d = mk("include")
    git_init(d)
    with (d / ".git" / "config").open("a") as fh:
        fh.write("[include]\n\tpath = /etc/passwd\n")
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
        fh.write("[extensions]\n\tworktreeConfig = true\n")
    return root, d


def t_bare(_):
    root, d = mk("bare")
    git_init(d)
    with (d / ".git" / "config").open("a") as fh:
        fh.write("[core]\n\tbare = true\n")
    return root, d


def t_worktree_out(_):
    root, d = mk("worktree_out")
    git_init(d)
    with (d / ".git" / "config").open("a") as fh:
        fh.write(f'[core]\n\tworktree = {root / "elsewhere"}\n')
    return root, d


def t_worktree_empty(_):
    root, d = mk("worktree_empty")
    git_init(d)
    with (d / ".git" / "config").open("a") as fh:
        fh.write("[core]\n\tworktree\n")
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


def t_cfg_symlink(_):
    root, d = mk("cfg_symlink")
    git_init(d)
    (root / "cfg.out").write_text("[core]\n\tbare = true\n")
    (d / ".git" / "config.zz").symlink_to(root / "cfg.out")
    return root, d


TREES = [t_empty, t_repo, t_repo_sub, t_gitfile, t_symlink_out, t_symlink_dir_out, t_symlink_in, t_fifo,
         t_above, t_above2, t_twoabove, t_include, t_commondir, t_alternates, t_worktreecfg, t_bare,
         t_worktree_out, t_worktree_empty, t_manyrepos, t_cfg_notregular, t_cfg_symlink]


def argv_cases(d):
    return [
        ("order-full", ["--lane", str(d), "--claims", "c.txt", "--receipt", "r.txt"], "order"),
        ("order-five", ["--lane", str(d), "--claims", "c.txt", "--receipt"], "order"),
        ("order-seven", ["--lane", str(d), "--claims", "c.txt", "--receipt", "r.txt", "x"], "order"),
        ("order-wrongtok", ["--lane", str(d), "--claims", "c.txt", "--receipts", "r.txt"], "order"),
        ("order-empty", [], "order"),
        ("order-dotdot", ["--lane", "../out", "--claims", "c.txt", "--receipt", "r.txt"], "order"),
        ("anchor-empty", [], "anchor"),
        ("anchor-lane-abs", ["--lane", str(d)], "anchor"),
        ("anchor-lane-rel", ["--lane", "."], "anchor"),
        ("anchor-lane-dotdot", ["--lane", "../outside"], "anchor"),
        ("anchor-lane-absout", ["--lane", "/etc"], "anchor"),
        ("anchor-lane-token", ["--lane", "{LANE}"], "anchor"),
        ("anchor-lane-token-dotdot", ["--lane", "{LANE}/../../etc"], "anchor"),
        ("anchor-lane-noval", ["--lane"], "anchor"),
        ("anchor-unknown", ["--frobnicate"], "anchor"),
        ("anchor-verbose", ["--verbose"], "anchor"),
        ("anchor-verbose-lane", ["--verbose", "--lane", str(d)], "anchor"),
        ("anchor-evref-out", ["--lane", str(d), "--evidence-ref", "/etc/passwd"], "anchor"),
        ("anchor-evref-rel", ["--lane", str(d), "--evidence-ref", "ev/x.txt"], "anchor"),
        ("anchor-token-sub", ["--lane", "{L}", "--evidence-ref", "{R}"], "anchor"),
        ("tool-other", ["--lane", str(d)], "zzz"),
        ("tool-empty", ["--lane", str(d)], ""),
    ]


def call(mod, d, argv, tool):
    try:
        return ("ret", mod.breach(pathlib.Path(d), list(argv), tool))
    except BaseException as e:                                   # noqa: BLE001 - compare failures too
        return ("exc", type(e).__name__, str(e))


rows, bad = 0, []
reached = 0
violations = []
for fn in TREES:
    root, d = fn(None)
    for label, argv, tool in argv_cases(d):
        rows += 1
        a = call(old, d, argv, tool)
        b = call(new, d, argv, tool)
        if a != b:
            bad.append((fn.__name__, label, a, b))
        inst._ITERS.clear()
        ia = call(inst, d, argv, tool)
        if ia != a:
            bad.append((fn.__name__, label, "instrumented verdict differs", a, ia))
        entries = inst._ITERS.count("entry")
        iters = inst._ITERS.count("iter")
        if entries:
            reached += 1
            if iters != entries:
                violations.append((fn.__name__, label, entries, iters))

print(f"MATRIX cases={rows} divergent={len(bad)}")
for row in bad[:10]:
    print("DIVERGENCE", row)
print(f"FACT3 reached_cases={reached} iterations_per_entry=1 violations={len(violations)}")
for row in violations[:10]:
    print("ITER-VIOLATION", row)
sys.exit(0 if not bad and not violations else 1)

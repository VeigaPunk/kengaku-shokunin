"""Critic probe (scratch): a `.git` that carries ONLY the entries a linked worktree's metadata dir carries, plus
an escaping `commondir`. Tests whether the landed fence containment-checks commondir or only classifies shapes."""
import os, pathlib

def _store(ctx, d, name):
    s = ctx.init(pathlib.Path(d).parent / name)
    ctx.write(s / "x.txt", "x\n"); ctx.git(s, "add", "-A"); ctx.git(s, "commit", "-qm", "x")
    return s

def _wt(d, line):
    gd = pathlib.Path(d) / "lane" / ".git"
    gd.mkdir(parents=True)
    (gd / "HEAD").write_text("ref: refs/heads/master\n")
    (gd / "index").write_bytes(b"")
    (gd / "commondir").write_text(line + "\n")
    (gd / "gitdir").write_text("../..\n")
    (gd / "logs").mkdir(); (gd / "logs" / "HEAD").write_text("")
    return ["--lane", "lane"]

def build_abs(ctx, d):
    s = _store(ctx, d, "wt-store-abs")
    return _wt(d, str(s / ".git"))

def build_rel(ctx, d):
    s = _store(ctx, d, "wt-store-rel")
    gd = pathlib.Path(d) / "lane" / ".git"
    return _wt(d, os.path.relpath(str(s / ".git"), str(gd)))

def build_in(ctx, d):
    s = pathlib.Path(d) / "inner"
    ctx.init(s); ctx.write(s / "y.txt", "y\n"); ctx.git(s, "add", "-A"); ctx.git(s, "commit", "-qm", "y")
    gd = pathlib.Path(d) / "lane" / ".git"
    return _wt(d, os.path.relpath(str(s / ".git"), str(gd)))

FIXTURES = [
    {"fid": "x1b-wt-abs", "tool": "anchor", "expect": "error", "defects": [], "build": build_abs},
    {"fid": "x1b-wt-rel", "tool": "anchor", "expect": "error", "defects": [], "build": build_rel},
    {"fid": "x1b-wt-in", "tool": "anchor", "expect": None, "defects": [], "build": build_in},
]

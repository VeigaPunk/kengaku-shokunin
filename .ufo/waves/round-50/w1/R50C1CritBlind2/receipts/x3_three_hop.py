"""Critic probe (scratch): three hops — worktree-shaped `.git` -> in-d `commondir` -> that store's
`objects/info/alternates` naming a store outside d. Tests whether the landed fence recurses containment
through the commondir hop into the common store's object graph."""
import os, pathlib

def _repo(ctx, p, name):
    s = ctx.init(p); ctx.write(s / "x.txt", name + "\n"); ctx.git(s, "add", "-A"); ctx.git(s, "commit", "-qm", name)
    return s

def _wt(d, line):
    gd = pathlib.Path(d) / "lane" / ".git"; gd.mkdir(parents=True)
    (gd / "HEAD").write_text("ref: refs/heads/master\n"); (gd / "index").write_bytes(b"")
    (gd / "commondir").write_text(line + "\n"); (gd / "gitdir").write_text("../..\n")
    (gd / "logs").mkdir(); (gd / "logs" / "HEAD").write_text("")
    return ["--lane", "lane"]

def build_abs(ctx, d):
    out = _repo(ctx, pathlib.Path(d).parent / "h3-out-abs", "out")
    inner = _repo(ctx, pathlib.Path(d) / "inner", "inner")
    ctx.write(inner / ".git/objects/info/alternates", str(out / ".git/objects") + "\n")
    gd = pathlib.Path(d) / "lane" / ".git"
    return _wt(d, os.path.relpath(str(inner / ".git"), str(gd)))

def build_rel(ctx, d):
    out = _repo(ctx, pathlib.Path(d).parent / "h3-out-rel", "out")
    inner = _repo(ctx, pathlib.Path(d) / "inner", "inner")
    base = inner / ".git/objects"
    ctx.write(base / "info/alternates", os.path.relpath(str(out / ".git/objects"), str(base)) + "\n")
    gd = pathlib.Path(d) / "lane" / ".git"
    return _wt(d, os.path.relpath(str(inner / ".git"), str(gd)))

def build_in(ctx, d):
    inner = _repo(ctx, pathlib.Path(d) / "inner", "inner")
    _repo(ctx, pathlib.Path(d) / "borrow", "borrow")
    ctx.write(inner / ".git/objects/info/alternates",
              os.path.relpath(str(pathlib.Path(d) / "borrow/.git/objects"), str(inner / ".git/objects")) + "\n")
    gd = pathlib.Path(d) / "lane" / ".git"
    return _wt(d, os.path.relpath(str(inner / ".git"), str(gd)))

FIXTURES = [
    {"fid": "x3-h3-abs", "tool": "anchor", "expect": "error", "defects": [], "build": build_abs},
    {"fid": "x3-h3-rel", "tool": "anchor", "expect": "error", "defects": [], "build": build_rel},
    {"fid": "x3-h3-in", "tool": "anchor", "expect": None, "defects": [], "build": build_in},
]

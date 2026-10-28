"""Sealed50 hostile: an unknown entry under `.git/objects/info/` (an object-store redirect by another name).

Witnesses the object-info leg (`_obj_info`): a fence that falls through unknown entries admits the directory.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.write(r / ".git/objects/info/packsets", "../elsewhere/objects\n")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "s50-05-objinfo-unknown", "tool": "anchor", "expect": "error", "defects": [], "build": build}]

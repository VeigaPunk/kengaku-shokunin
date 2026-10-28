"""Sealed50 hostile: a "store" with no `objects` directory at all.

Witnesses the store-requirement leg (`_store`): a fence that stops requiring `objects` admits a directory that
cannot be a repository, and whose refs may then be resolved elsewhere.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    import shutil
    shutil.rmtree(r / ".git/objects")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "s50-09-store-no-objects", "tool": "anchor", "expect": "error", "defects": [], "build": build}]

"""Sealed50 hostile: a ref file whose content is not a 40-hex object name.

Witnesses the ref-value leg (`_ref_tree`): a fence that only checks the ref's name admits a ref whose content
is a path-shaped token.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.write(r / ".git/refs/heads/master", "../../outside/objects\n")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "s50-08-ref-value-junk", "tool": "anchor", "expect": "error", "defects": [], "build": build}]

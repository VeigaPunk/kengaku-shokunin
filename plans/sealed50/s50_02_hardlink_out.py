"""Sealed50 hostile: a regular file in the fixture hard-linked to a file it created outside `d`.

Witnesses the hard-link leg (`_tree`): a fence that ignores link counts admits a file whose inode is shared with
a path outside the fixture.
"""
import os


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    outside = d.parent / "outside-shared.txt"
    outside.write_text("shared\n")
    os.link(outside, d / "shared-link")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "s50-02-hardlink-outside", "tool": "anchor", "expect": "error", "defects": [], "build": build}]

"""Sealed50 hostile: a stray symlink OUTSIDE any store, pointing outside the fixture.

Witnesses the fixture-walk symlink leg (`_tree`): a fence that only classifies `.git` directories admits it.
"""
import os


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    os.symlink("/etc/hostname", d / "outside-link")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "s50-01-stray-symlink", "tool": "anchor", "expect": "error", "defects": [], "build": build}]

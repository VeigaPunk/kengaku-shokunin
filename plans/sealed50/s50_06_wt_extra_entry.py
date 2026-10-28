"""Sealed50 hostile: a linked worktree whose store carries an entry git never writes (`extra`).

Witnesses the worktree-store allowlist (`WT_TOP`): a fence that accepts any entry name in a worktree store
admits metadata git did not write.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.git(r, "branch", "feature")
    ctx.git(r, "worktree", "add", "--relative-paths", "-q", "../wt", "feature")
    ctx.write(d / "repo/.git/worktrees/wt/extra", "not git\n")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "s50-06-wt-extra-entry", "tool": "anchor", "expect": "error", "defects": [], "build": build}]

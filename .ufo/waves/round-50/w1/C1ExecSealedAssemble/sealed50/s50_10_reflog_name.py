"""Sealed50 hostile: a reflog under a ref name git does not write (`logs/refs/weird/x`).

Witnesses the reflog-name leg (`_logs`): a fence that accepts any reflog name admits log metadata for a ref
namespace it otherwise refuses.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.write(r / ".git/logs/refs/weird/x", "0" * 40 + " " + "0" * 40 + " fixture <f@x> 0 +0000\tcommit\n")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "s50-10-reflog-name", "tool": "anchor", "expect": "error", "defects": [], "build": build}]

"""Fixture shape: `.git/config` enables the second repository config file, and that file declares an
include whose target sits outside d. The store fence reads only the primary config file, so the include is
invisible to the fence while every other git call in the counter's own process parses it.
"""
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    d = pathlib.Path(d)
    side = d.parent / "outside.cfg"
    ctx.write(side, "[user]\n\temail = OUTSIDE-MARKER@invalid\n")
    r = ctx.init(d / "lane")
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    ctx.git(r, "config", "extensions.worktreeConfig", "true")
    ctx.write(r / ".git/config.worktree", f"[include]\n\tpath = {side}\n")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "wtcfg-include-outside", "tool": "order", "expect": "accept", "defects": [], "build": build}]

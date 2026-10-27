"""Hostile filesystem-shape module: object-info directory redirected outside the fixture."""
import os
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    d = pathlib.Path(d)
    lane = ctx.init(d / "lane")
    ctx.write(lane / CLAIMS, "nothing ran\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "claims")
    ctx.write(lane / RECEIPT, "receipt\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "receipt")
    info = lane / ".git" / "objects" / "info"
    outside = d.parent / "outside-info"
    os.rename(info, outside)
    os.symlink(outside, info)
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "sealed-info-redirect", "tool": "order", "expect": "accept", "defects": [], "build": build}]

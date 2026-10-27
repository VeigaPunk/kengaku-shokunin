"""Hostile filesystem-shape module: packed object store redirected outside the fixture."""
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
    ctx.git(lane, "repack", "-a", "-d")
    pack = lane / ".git" / "objects" / "pack"
    outside = d.parent / "outside-pack"
    os.rename(pack, outside)
    os.symlink(outside, pack)
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "sealed-pack-redirect", "tool": "order", "expect": "accept", "defects": [], "build": build}]

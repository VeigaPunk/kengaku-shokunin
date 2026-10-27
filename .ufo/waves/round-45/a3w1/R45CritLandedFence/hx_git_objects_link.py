"""Held-out hostile fixture: a real in-fixture .git whose objects store is symlinked outside d."""
import os
import pathlib
import shutil


def build(ctx, d):
    d = pathlib.Path(d)
    lane = ctx.init(d / "lane")
    ctx.write(lane / "claims.md", "claims\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "claims")
    ctx.write(lane / "receipt.txt", "receipt\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "receipt")
    objects = lane / ".git" / "objects"
    outside = pathlib.Path(d).parent / "outside-objects"
    shutil.move(str(objects), str(outside))
    os.symlink(str(outside), str(objects), target_is_directory=True)
    return ["--lane", "lane", "--claims", "claims.md", "--receipt", "receipt.txt"]


FIXTURES = [{"fid": "hx-git-objects-outside", "tool": "order", "expect": "accept", "defects": [], "build": build}]

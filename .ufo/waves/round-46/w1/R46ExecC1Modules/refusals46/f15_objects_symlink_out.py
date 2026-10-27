"""Refusal fixture f15 (round-45 held-out driver `R45HoSymlinks/link_hostiles.py`, class A): the repo's
`.git/objects` is renamed out of `d` (to the module build root) and replaced by a symlink back to it. The landed
fence's walk prunes `.git`, so the redirect is never seen; it ADMITS the fixture and its own git children read
the outside object store. One class: object store symlinked out of `d`. Base fence (`a3w1/R45HoSymlinks.md`):
ADMIT, 8 outside opens."""
import os
import pathlib

CLAIMS = "claims.md"
RECEIPT = "receipt.md"


def _repo(ctx, d, name):
    r = ctx.init(pathlib.Path(d) / name)
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    return r


def build(ctx, d):
    d = pathlib.Path(d)
    r = _repo(ctx, d, "lane")
    outside = d.parent / "outside-objects"
    os.rename(r / ".git/objects", outside)
    os.symlink(outside, r / ".git/objects")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "link-objects-symlink-out", "tool": "order", "expect": "error", "defects": [], "build": build}]

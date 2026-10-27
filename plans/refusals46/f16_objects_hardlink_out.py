"""Refusal fixture f16 (round-45 held-out driver `R45HoSymlinks/link_hostiles.py`, class B): every file of the
repo's object store is hardlinked into a directory at the module build root, so the fixture's store has a second
name outside `d`. No symlink and no path value leaves `d`, so the landed fence's walk finds nothing to refuse and
ADMITS; the escape is a store-identity one, not an open-path one (0 outside opens). One class: object store
hardlinked out of `d`. Base fence (`a3w1/R45HoSymlinks.md`): ADMIT, 0 outside opens."""
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
    outside = d.parent / "outside-hardlinks"
    outside.mkdir()
    for p in (r / ".git/objects").rglob("*"):
        if p.is_file():
            q = outside / p.relative_to(r / ".git/objects")
            q.parent.mkdir(parents=True, exist_ok=True)
            os.link(p, q)
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "link-objects-hardlink-out", "tool": "order", "expect": "accept", "defects": [],
             "build": build}]

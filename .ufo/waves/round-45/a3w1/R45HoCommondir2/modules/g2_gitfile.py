"""Held-out hostile module g2 (R45HoCommondir2, vector b): `d/lane/.git` is a FILE whose gitdir line is
RELATIVE and SPACE-PADDED (`gitdir:   ../../g2-out/.git`), redirecting the store outside d. Same class as
f1 (whose store was built by --separate-git-dir); here the redirect text is relative and whitespace-padded,
so any parser that trims and resolves could be fooled. The fence must refuse any `.git` file before git runs."""
import os
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def _store(ctx, d, name):
    store = pathlib.Path(d).parent / name
    ctx.init(store)
    ctx.write(store / CLAIMS, "nothing ran\n")
    ctx.git(store, "add", "-A")
    ctx.git(store, "commit", "-qm", "claims")
    ctx.write(store / RECEIPT, "receipt\n")
    ctx.git(store, "add", "-A")
    ctx.git(store, "commit", "-qm", "receipt")
    return store


def build(ctx, d):
    out = _store(ctx, d, "g2-out")
    lane = d / "lane"
    rel = os.path.relpath(str(out / ".git"), str(lane))
    ctx.write(lane / ".git", "gitdir:   " + rel + "\n")
    ctx.write(lane / CLAIMS, "nothing ran\n")
    ctx.write(lane / RECEIPT, "receipt\n")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "g2-gitfile-pad", "tool": "order", "expect": "accept", "defects": [], "build": build}]

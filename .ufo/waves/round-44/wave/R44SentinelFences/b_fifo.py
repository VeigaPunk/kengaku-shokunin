"""Fixture shape: the repo's primary config file includes a FIFO that sits outside d. The argv/`--lane` fence
runs first and follows includes, so it opens the outside FIFO and blocks; each blocked call costs the full
per-call timeout, and the per-fixture cost multiplies by the number of fixtures.
"""
import os
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def _one(ctx, d, name):
    d = pathlib.Path(d)
    fifo = d.parent / name
    os.mkfifo(fifo)
    r = ctx.init(d / "lane")
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    with open(r / ".git/config", "a") as fh:
        fh.write(f"[include]\n\tpath = {fifo}\n")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


def build_a(ctx, d):
    return _one(ctx, d, "pipe-a")


def build_b(ctx, d):
    return _one(ctx, d, "pipe-b")


FIXTURES = [
    {"fid": "fifo-a", "tool": "order", "expect": "accept", "defects": [], "build": build_a},
    {"fid": "fifo-b", "tool": "order", "expect": "accept", "defects": [], "build": build_b},
]

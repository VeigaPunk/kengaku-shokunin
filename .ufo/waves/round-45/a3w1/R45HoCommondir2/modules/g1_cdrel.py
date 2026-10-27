"""Held-out hostile module g1 (R45HoCommondir2, vector a — straight): the repo at `d/repo` is an ordinary
repo, but a hand-written `.git/commondir` holding a RELATIVE path, resolved by git against the gitdir itself,
sends the common store (config, refs, objects) OUTSIDE d via `..` — same class as f7, but the redirect is
relative (`../../<name>/.git`) instead of absolute. The fence refuses any `.git/commondir` it walks; this
module checks that refusal still fires (and with no outside open) when the redirect is relative."""
import os
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def _store(ctx, d, name):
    store = pathlib.Path(d).parent / name  # deliberate outside artefact, still inside the build root
    ctx.init(store)
    ctx.write(store / CLAIMS, "nothing ran\n")
    ctx.git(store, "add", "-A")
    ctx.git(store, "commit", "-qm", "claims")
    ctx.write(store / RECEIPT, "receipt\n")
    ctx.git(store, "add", "-A")
    ctx.git(store, "commit", "-qm", "receipt")
    return store


def _repo(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    return r


def build(ctx, d):
    out = _store(ctx, d, "g1-out")
    r = _repo(ctx, d)
    rel = os.path.relpath(str(out / ".git"), str(r / ".git"))
    ctx.write(r / ".git" / "commondir", rel + "\n")
    return ["--lane", "repo", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "g1-cd-rel", "tool": "order", "expect": "accept", "defects": [], "build": build}]

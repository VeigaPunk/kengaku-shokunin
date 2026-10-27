"""Refusal fixture f12 (round-45 held-out h2, `R45HoIncludeIf`): `[includeIf "<cond>"]` headers prefixed with a
bare `\\r` — parsed by git (onbranch:, gitdir: exact, `**`/glob, gitdir/i:, hasconfig:) but invisible to the
landed fence's `_INCLUDE_RE`, which anchors at `^[ \\t]*\\[`. Matching conditions fire the include and the
fence's git children open the outside file; non-matching ones are admitted while the fixture still carries an
executable include directive the fence advertises it refuses outright. One class: conditional include,
CR-prefixed. Base fence (`a3w1/R45HoIncludeIf/driver.out`): 9/9 ADMIT, 6 with outside opens, 3 without."""
import os
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def _one(ctx, d, fid, cond, anchor=False):
    r = ctx.init(d / "lane")
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    if cond.startswith("hasconfig:"):
        ctx.sh("git", "-C", str(r), "config", "remote.origin.url", "file:///nonexistent-side-store")
    side = pathlib.Path(d).parent / f"side-{fid}.cfg"
    ctx.write(side, f"[user]\n\temail = {fid}@invalid\n")
    cfg = r / ".git" / "config"
    cfg.write_bytes(cfg.read_bytes() + f"\r[includeIf \"{cond}\"]\n\tpath = {side}\n".encode())
    if anchor:
        return ["--lane", "lane"]
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


def build_onbranch(ctx, d):
    return _one(ctx, pathlib.Path(d), "h2-onbranch", "onbranch:master")


def build_onbranch_nomatch(ctx, d):
    return _one(ctx, pathlib.Path(d), "h2-onbranch-nomatch", "onbranch:notabranch")


def build_gitdir_exact(ctx, d):
    lane = pathlib.Path(d) / "lane"
    return _one(ctx, pathlib.Path(d), "h2-gitdir-exact", f"gitdir:{os.path.realpath(lane / '.git')}")


def build_gitdir_glob(ctx, d):
    return _one(ctx, pathlib.Path(d), "h2-gitdir-glob", "gitdir:**/lane/.git")


def build_gitdir_i(ctx, d):
    lane = pathlib.Path(d) / "lane"
    return _one(ctx, pathlib.Path(d), "h2-gitdir-i", f"gitdir/i:{os.path.realpath(lane / '.git').upper()}")


def build_gitdir_star(ctx, d):
    return _one(ctx, pathlib.Path(d), "h2-gitdir-star", "gitdir:**")


def build_gitdir_nomatch(ctx, d):
    return _one(ctx, pathlib.Path(d), "h2-gitdir-nomatch", "gitdir:**/zzz-nomatch/.git")


def build_hasconfig(ctx, d):
    return _one(ctx, pathlib.Path(d), "h2-hasconfig", "hasconfig:remote.*.url")


def build_onbranch_anchor(ctx, d):
    return _one(ctx, pathlib.Path(d), "h2-onbranch-anchor", "onbranch:master", anchor=True)


FIXTURES = [
    {"fid": "h2-inclif-onbranch", "tool": "order", "expect": "accept", "defects": [], "build": build_onbranch},
    {"fid": "h2-inclif-onbranch-nomatch", "tool": "order", "expect": "accept", "defects": [],
     "build": build_onbranch_nomatch},
    {"fid": "h2-inclif-gitdir-exact", "tool": "order", "expect": "accept", "defects": [],
     "build": build_gitdir_exact},
    {"fid": "h2-inclif-gitdir-glob", "tool": "order", "expect": "accept", "defects": [],
     "build": build_gitdir_glob},
    {"fid": "h2-inclif-gitdir-i", "tool": "order", "expect": "accept", "defects": [], "build": build_gitdir_i},
    {"fid": "h2-inclif-gitdir-star", "tool": "order", "expect": "accept", "defects": [], "build": build_gitdir_star},
    {"fid": "h2-inclif-gitdir-nomatch", "tool": "order", "expect": "accept", "defects": [],
     "build": build_gitdir_nomatch},
    {"fid": "h2-inclif-hasconfig", "tool": "order", "expect": "accept", "defects": [], "build": build_hasconfig},
    {"fid": "h2-inclif-onbranch-anchor", "tool": "anchor", "expect": "error", "defects": [],
     "build": build_onbranch_anchor},
]

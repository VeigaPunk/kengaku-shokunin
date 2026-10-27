"""Refusal fixture F8 (`R44SentinelFences` V2): the repo enables `extensions.worktreeConfig` and its second
config file `.git/config.worktree` carries an include that names a file OUTSIDE d. The round-44 fence reads
`--local --no-includes` (`.git/config` only), so the include is invisible to both config calls while every
other git call parses it; the round-45 fence refuses any `.git/config.worktree` file and any `[include*]`
section or `path =` key found by its own text scan of `.git/config*` before any git call is trusted."""
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def _one(ctx, d, name):
    d = pathlib.Path(d)
    side = d.parent / name
    r = ctx.init(d / "lane")
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    ctx.sh("git", "-C", str(r), "config", "extensions.worktreeConfig", "true")
    ctx.write(r / ".git/config.worktree", f"[include]\n\tpath = {side}\n")
    ctx.write(side, "[user]\n\temail = OUTSIDE-MARKER@invalid\n")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


def build_a(ctx, d):
    return _one(ctx, d, "outside-a.cfg")


def build_b(ctx, d):
    return _one(ctx, d, "outside-b.cfg")


FIXTURES = [
    {"fid": "f8-wtcfg-a", "tool": "order", "expect": "accept", "defects": [], "build": build_a},
    {"fid": "f8-wtcfg-b", "tool": "order", "expect": "accept", "defects": [], "build": build_b},
]

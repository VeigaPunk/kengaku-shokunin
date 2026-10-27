"""Refusal fixture F9 (`R44SentinelFences` V3b): a bare-shaped repository (`core.bare=true` in `.git/config`)
that git refuses to describe (`rev-parse --show-toplevel` exits non-zero). The round-44 fence guards every
check with `rc == 0`, so "git cannot answer" reads as "nothing to see" and the fixture is admitted while the
tool's own setup fails; the round-45 fence treats `rc != 0` from any of its git probes as unverifiable."""
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    d = pathlib.Path(d)
    r = ctx.init(d / "lane")
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    ctx.sh("git", "-C", str(r), "config", "core.bare", "true")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "f9-bare-repo", "tool": "order", "expect": "error", "defects": [], "build": build}]

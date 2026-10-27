"""Refusal fixture F10 (`R44LabratLaneInclude`): `.git/config` of the `--lane` repo carries an `[include]` whose
target is a REGULAR file beside d (not a FIFO, so nothing hangs). The round-44 counter refuses the fixture in
`repo_breach`, but `lane_breach` runs first and its `git rev-parse` children open and parse the outside file before
any refusal: refused, yet read. The round-45 rule counts every successful open of a path outside d by the fence's
process tree; a fence passes this module only if it refuses it without opening the include target."""
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    d = pathlib.Path(d)
    side = d.parent / "inc10.cfg"
    ctx.write(side, "[user]\n\temail = OUTSIDE-READ@invalid\n")
    r = ctx.init(d / "lane")
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    ctx.sh("git", "-C", str(r), "config", "--add", "include.path", str(side))
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "f10-lane-include-regular", "tool": "order", "expect": "accept", "defects": [], "build": build}]

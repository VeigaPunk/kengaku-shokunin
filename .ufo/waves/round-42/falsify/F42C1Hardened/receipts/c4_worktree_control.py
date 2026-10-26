"""F42C1Hardened control module (not a hostile module): isolates what makes `h4_worktree` accept.

Same decoy repo (a `gate: P10 ok` blob under the claims dir, which the order tool reports as a hit), same
argv, but no `core.worktree`: the tool then measures the decoy itself and must exit 1. That makes h4's
`observed_rc=0 ok` attributable to the redirect, not to the fixture's own history.
"""

M42 = ".ufo/waves/round-42/claims"
CLAIMS = "plans/round-42-claims.md"
PROBE = "corpus/evidence/round42/fibsqrt-probe.txt"
RECEIPT_BODY = "cases=16 observed_pass=7 observed_fail=9 mismatches=0\nregrade cases=16 differ=0\n"
HIT = "gate: P10 ok fresh probe output byte-equal\n"


def commit(ctx, repo, message):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", message)


def build(ctx, d):
    decoy = ctx.init(d / "lane")
    ctx.write(decoy / CLAIMS, "# round 42 - frozen claims\n")
    ctx.write(decoy / M42 / "note.txt", HIT)
    commit(ctx, decoy, "freeze with the gate line in the tree")
    ctx.write(decoy / PROBE, RECEIPT_BODY)
    commit(ctx, decoy, "record the run")
    return ["--lane", str(decoy), "--claims", CLAIMS, "--receipt", PROBE]


FIXTURES = [
    {"fid": "c4-decoy-no-redirect", "tool": "order", "expect": "reject", "defects": [], "build": build},
]

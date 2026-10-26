"""F42C1Hardened hostile module `h4_worktree` — repair R4 (R42CritC1Counter V1b).

Vector: `path_ok` validates only the argv tokens against `d`, but `order_check.main` adopts
`git rev-parse --show-toplevel` as its root (plans/order_check.py:152). A fixture repo whose `.git/config`
carries `core.worktree=<host repo outside d>` therefore makes the tool measure a history that lives outside
the fixture, while the counter still prints `wrong=0 tampered=0`. R42CritC1Counter measured the same route
(`REV-PARSE-TOP …/p5/host`, `ORDER-RC 0`) and turned it into an attributed kill.

Observable, on a fixture that declares `accept`:

  frozen counter  FIXTURE h4-worktree-redirect … observed_rc=0 … ok
                  (the decoy's own history holds a `gate: P10 ok` hit and would be rc 1: the accept can
                   only come from the host repo the redirect names — vector green)
  hardened copy   SETUP fixture 'h4-worktree-redirect' of battery/h4_worktree.py escapes its directory:
                  lane/rev-parse --show-toplevel=<dest>/host        (refused before any run: vector red)
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
    # the clean host history the redirect points at (outside d, inside the fixture root)
    host = ctx.init(d.parent / "host")
    ctx.write(host / CLAIMS, "# host lane - frozen claims\n\nNothing was executed here.\n")
    ctx.write(host / M42 / "note.txt", "P10 DEFECT receipt unreadable\n")
    commit(ctx, host, "host freeze")
    ctx.write(host / PROBE, RECEIPT_BODY)
    commit(ctx, host, "host recorded run")

    # the decoy the argv names: its own claims blob proves the probe ran (order rc 1 without the redirect)
    decoy = ctx.init(d / "lane")
    ctx.write(decoy / CLAIMS, "# round 42 - frozen claims\n")
    ctx.write(decoy / M42 / "note.txt", HIT)
    commit(ctx, decoy, "freeze with the gate line in the tree")
    ctx.write(decoy / PROBE, RECEIPT_BODY)
    commit(ctx, decoy, "record the run")
    ctx.sh("git", "-C", str(decoy), "config", "core.worktree", str(host))
    return ["--lane", str(decoy), "--claims", CLAIMS, "--receipt", PROBE]


FIXTURES = [
    {"fid": "h4-worktree-redirect", "tool": "order", "expect": "accept", "defects": [], "build": build},
]

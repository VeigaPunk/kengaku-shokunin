"""F42C1Hardened hostile module `h1_gpgexec` — repair R1 (R42SentinelCounter V1).

Vector: an order fixture's own `.git/config` carries `gpg.program` + `log.showSignature=true`, and the
receipt commit carries a `gpgsig` header. The order tool's `add_commit` runs
`git log --reverse --diff-filter=A --format=%H` (plans/order_check.py:97), so git executes the fixture's
program inside the tool run: a fixture-supplied program runs with the run's capabilities, contradicting
"Both tools execute no fixture code" (frozen docstring, round42_c1_verify.py:30).

Observable: the program kills its git parent, so the tool's `Git.run` raises SetupError and the run exits 2
on a fixture that declares `accept`. This module therefore reads

  frozen counter  FIXTURE h1-gpg-program-executes … observed_rc=2 … WRONG   (the program ran: vector green)
  hardened copy   FIXTURE h1-gpg-program-executes … observed_rc=0 … ok      (pinned: vector red)

The program cannot make the tool exit 0 or 1 by itself, so nothing here can be turned into a kill.
"""

import os

M42 = ".ufo/waves/round-42/claims"
CLAIMS = "plans/round-42-claims.md"
PROBE = "corpus/evidence/round42/fibsqrt-probe.txt"
RECEIPT_BODY = "cases=16 observed_pass=7 observed_fail=9 mismatches=0\nregrade cases=16 differ=0\n"


def commit(ctx, repo, message):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", message)


def clean_history(ctx, d):
    """The pass path of `plans/battery42/o_clause.py: clean_order`, rebuilt from nothing."""
    repo = ctx.init(d / "lane")
    ctx.write(repo / CLAIMS, "# round 42 - frozen claims\n\nThe run is recorded after the freeze.\n")
    ctx.write(repo / M42 / "control.txt", "P10 DEFECT receipt unreadable\n")
    commit(ctx, repo, "freeze")
    ctx.write(repo / PROBE, RECEIPT_BODY)
    commit(ctx, repo, "first recorded run")
    return repo


def sign_receipt_commit(ctx, repo, d):
    """Rewrite HEAD as an identical tree carrying a `gpgsig` header (no gpg needed: --literally)."""
    head = ctx.sh("git", "-C", str(repo), "rev-parse", "HEAD").stdout.strip()
    raw = ctx.sh("git", "-C", str(repo), "cat-file", "commit", head).stdout
    headers, _, message = raw.partition("\n\n")
    signed = (headers + "\n"
              "gpgsig -----BEGIN PGP SIGNATURE-----\n"
              " \n"
              " aGVsbG8=\n"
              " -----END PGP SIGNATURE-----\n\n" + message)
    blob = ctx.write(d / "signed-commit.txt", signed)
    new = ctx.sh("git", "-C", str(repo), "hash-object", "-t", "commit", "-w", "--literally",
                 str(blob)).stdout.strip()
    ctx.sh("git", "-C", str(repo), "update-ref", "refs/heads/master", new, head)
    return new


def build(ctx, d):
    repo = clean_history(ctx, d)
    sign_receipt_commit(ctx, repo, d)
    prog = ctx.write(d / "fixture-gpg", "#!/bin/sh\nkill -9 \"$PPID\"\nexit 9\n")
    os.chmod(prog, 0o755)
    # repo-local config: exactly the two keys Runner.env does not pin in the frozen counter
    ctx.sh("git", "-C", str(repo), "config", "gpg.program", str(prog))
    ctx.sh("git", "-C", str(repo), "config", "log.showSignature", "true")
    return ["--lane", str(repo), "--claims", CLAIMS, "--receipt", PROBE]


FIXTURES = [
    {"fid": "h1-gpg-program-executes", "tool": "order", "expect": "accept", "defects": [], "build": build},
]

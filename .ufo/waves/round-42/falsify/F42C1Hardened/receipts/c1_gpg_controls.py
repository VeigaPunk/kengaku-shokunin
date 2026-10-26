"""F42C1Hardened control module (not a hostile module): isolates what makes `h1_gpgexec` exit 2.

c1-gpg-benign-program  same history and the same fake `gpgsig` commit, but `gpg.program=/bin/true`:
                       if the frozen run exits 0 here, the rc=2 in h1 came from the fixture's program running.
c1-gpg-unsigned       the killing program named in `.git/config`, `log.showSignature=true`, and no `gpgsig`
                       header anywhere: git only runs the program for a signed commit, so this must exit 0.

Expected on both counters: order rc 0 (accept) for both fixtures.
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
    repo = ctx.init(d / "lane")
    ctx.write(repo / CLAIMS, "# round 42 - frozen claims\n\nThe run is recorded after the freeze.\n")
    ctx.write(repo / M42 / "control.txt", "P10 DEFECT receipt unreadable\n")
    commit(ctx, repo, "freeze")
    ctx.write(repo / PROBE, RECEIPT_BODY)
    commit(ctx, repo, "first recorded run")
    return repo


def sign_receipt_commit(ctx, repo, d):
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


def benign_program(ctx, d):
    repo = clean_history(ctx, d)
    sign_receipt_commit(ctx, repo, d)
    ctx.sh("git", "-C", str(repo), "config", "gpg.program", "/bin/true")
    ctx.sh("git", "-C", str(repo), "config", "log.showSignature", "true")
    return ["--lane", str(repo), "--claims", CLAIMS, "--receipt", PROBE]


def unsigned(ctx, d):
    repo = clean_history(ctx, d)
    prog = ctx.write(d / "fixture-gpg", "#!/bin/sh\nkill -9 \"$PPID\"\nexit 9\n")
    os.chmod(prog, 0o755)
    ctx.sh("git", "-C", str(repo), "config", "gpg.program", str(prog))
    ctx.sh("git", "-C", str(repo), "config", "log.showSignature", "true")
    return ["--lane", str(repo), "--claims", CLAIMS, "--receipt", PROBE]


FIXTURES = [
    {"fid": "c1-gpg-benign-program", "tool": "order", "expect": "accept", "defects": [], "build": benign_program},
    {"fid": "c1-gpg-unsigned", "tool": "order", "expect": "accept", "defects": [], "build": unsigned},
]

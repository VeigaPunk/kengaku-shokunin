"""Draft hostile f4b (R44MutC1Fences, targets PG1): a SECOND repo under d whose .git/config is a FIFO.

f4's include is refused by the `--no-includes` include check before any parent-side git call can
block on the FIFO, so the 30 s timeout on pin_git is never what refuses f4. Here the honest
`--lane` repo passes every check and the decoy repo `d/decoy` carries a FIFO config; the walk
reaches it in repo_breach, where `git config --get-regexp` blocks on the FIFO.
Expected: pristine refuses after ~30 s ("decoy/git hung"); PG1 (no timeout) mutant stalls until
the outer kill (hang)."""
import pathlib

CL = ".ufo/waves/round-42/claims/round-42-claims.md"
RC = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    r = ctx.init(d / "lane")
    ctx.write(pathlib.Path(d) / "lane" / CL, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(pathlib.Path(d) / "lane" / RC, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    other = ctx.init(d / "decoy")
    ctx.sh("rm", str(other / ".git" / "config"))
    ctx.sh("mkfifo", str(other / ".git" / "config"))
    return ["--lane", "lane", "--claims", CL, "--receipt", RC]


FIXTURES = [{"fid": "f4b-decoy-fifo-config", "tool": "order", "expect": "accept", "defects": [], "build": build}]

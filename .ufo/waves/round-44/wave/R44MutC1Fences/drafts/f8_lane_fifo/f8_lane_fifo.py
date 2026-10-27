"""Draft hostile f8 (R44MutC1Fences, targets LB2): the `--lane` repo's own .git/config is a FIFO.

lane_breach runs its git calls with its own inline subprocess (not pin_git), so f4's include and
f4b's decoy never exercise this timeout. A FIFO config blocks even `git rev-parse --show-toplevel`
(measured: blocked at 5 s in the design experiment), and lane_breach is the first guard in the
chain, so it is the leg that must time out.
Expected: pristine refuses after ~30 s ("--lane git hung"); LB2 (no timeout) mutant stalls until
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
    ctx.sh("rm", str(r / ".git" / "config"))
    ctx.sh("mkfifo", str(r / ".git" / "config"))
    return ["--lane", "lane", "--claims", CL, "--receipt", RC]


FIXTURES = [{"fid": "f8-lane-fifo-config", "tool": "order", "expect": "accept", "defects": [], "build": build}]

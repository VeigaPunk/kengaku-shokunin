"""Negative control (F2): a repo nine levels down whose work tree sits outside d. The walk has no depth cap,
so the store fence must still see it."""
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    d = pathlib.Path(d)
    r = d / "a/b/c/d/e/f/g/h/r"
    ctx.init(r)
    ctx.write(r / CLAIMS, "x\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "x")
    ctx.sh("git", "-C", str(r), "config", "co" + "re.worktree", str(d.parent / "outside-wt"))
    return ["--lane", "a/b/c/d/e/f/g/h/r", "--claims", CLAIMS, "--receipt", CLAIMS]


FIXTURES = [{"fid": "deep-nine", "tool": "order", "expect": "error", "defects": [], "build": build}]

"""Refusal fixture f18 (round-45 held-out `R45HoCommondir2/modules/g3_wtmeta.py`): `d/repo` is an ordinary repo
that carries a real linked-worktree pair whose CHECKOUT lives outside `d` (created with `git worktree add` at the
module build root). The metadata dir `repo/.git/worktrees/<id>/` points at that outside checkout; the landed
fence's walk never descends into `.git`, its fact-5 scan only knows top-level `.git/commondir`, `alternates` and
`.git/config*`, and both rev-parse legs answer inside `d`. One class: linked-worktree metadata pointing outside
`d`. Base fence (`a3w1/R45HoCommondir2.md`): ADMIT, 0 outside opens."""
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    wt = pathlib.Path(d).parent / "g3-wt"  # linked-worktree checkout outside d, inside the build root
    ctx.git(r, "worktree", "add", "--detach", str(wt), "HEAD")
    return ["--lane", "repo", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "g3-wtmeta-out", "tool": "order", "expect": "accept", "defects": [], "build": build}]

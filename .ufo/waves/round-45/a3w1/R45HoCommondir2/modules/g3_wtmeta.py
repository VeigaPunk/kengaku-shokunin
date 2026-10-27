"""Held-out hostile module g3 (R45HoCommondir2, vector c): `d/repo` is an ordinary repo that carries a real
linked-worktree pair whose CHECKOUT lives outside d (`git worktree add` with the worktree at the module build
root): the metadata dir `repo/.git/worktrees/<id>/` (gitdir, commondir, HEAD, index) points at that outside
checkout. The fence's walk never descends into a `.git` dir, its fact-5 scan only knows top-level
`.git/commondir`, `alternates` and `.git/config*`, and both rev-parse legs answer inside d — so the metadata
pointing outside is invisible unless git itself opens the outside checkout."""
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

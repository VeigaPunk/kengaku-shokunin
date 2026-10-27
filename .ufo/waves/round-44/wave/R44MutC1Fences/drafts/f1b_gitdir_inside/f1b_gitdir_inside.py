"""Draft hostile f1b (R44MutC1Fences, targets RB1): gitdir redirect whose git store stays INSIDE d.

`d/.git` is a plain FILE pointing at `d/gd`, so both `rev-parse --show-toplevel` and
`rev-parse --absolute-git-dir` resolve inside the fixture and neither lane_breach (F1's
absolute-git-dir half) nor any other guard fires. Only repo_breach's `.git` FILE check refuses it.
Expected: pristine refuses (".git is a file (gitdir redirect)"); RB1 mutant admits."""
import pathlib


def build(ctx, d):
    ctx.init(d)
    ctx.write(pathlib.Path(d) / ".ufo/waves/round-42/claims/round-42-claims.md", "nothing ran\n")
    ctx.git(d, "add", "-A")
    ctx.git(d, "commit", "-qm", "claims")
    ctx.write(pathlib.Path(d) / "corpus/evidence/round42/receipt.txt", "receipt\n")
    ctx.git(d, "add", "-A")
    ctx.git(d, "commit", "-qm", "receipt")
    ctx.sh("mv", str(pathlib.Path(d) / ".git"), str(pathlib.Path(d) / "gd"))
    ctx.write(pathlib.Path(d) / ".git", "gitdir: gd\n")
    return ["--lane", ".", "--claims", ".ufo/waves/round-42/claims/round-42-claims.md",
            "--receipt", "corpus/evidence/round42/receipt.txt"]


FIXTURES = [{"fid": "f1b-gitdir-inside", "tool": "order", "expect": "accept", "defects": [], "build": build}]

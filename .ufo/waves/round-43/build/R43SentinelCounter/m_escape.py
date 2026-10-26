
import pathlib

def _order_fixture(d, gdname, wtname, claims, receipt, expect):
    return None

def f_gitdir(ctx, d):
    """A worktree whose git dir lives beside it, not under it."""
    gd = pathlib.Path(d).parent / "side" / "gitdir"
    ctx.write(pathlib.Path(gd).parent / ".keep", "")
    ctx.sh("git", "init", "-q", "-b", "master", "--separate-git-dir", str(gd), str(d))
    ctx.write(pathlib.Path(d) / ".ufo/waves/round-42/claims/round-42-claims.md", "nothing ran\n")
    ctx.git(d, "add", "-A")
    ctx.git(d, "commit", "-qm", "claims")
    ctx.write(pathlib.Path(d) / "corpus/evidence/round42/receipt.txt", "receipt\n")
    ctx.git(d, "add", "-A")
    ctx.git(d, "commit", "-qm", "receipt")
    return ["--lane", ".", "--claims", ".ufo/waves/round-42/claims/round-42-claims.md",
            "--receipt", "corpus/evidence/round42/receipt.txt"]

def f_deep(ctx, d):
    """A repo four levels down whose work tree is outside d."""
    key = "co" + "re.worktree"
    r = pathlib.Path(d) / "x" / "y" / "z" / "r"
    ctx.init(r)
    ctx.write(r / "claims.md", "x\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "f")
    ctx.sh("git", "-C", str(r), "config", key, str(pathlib.Path(d).parent / "wt"))
    return ["--lane", "x/y/z/r", "--claims", "claims.md", "--receipt", "claims.md"]

FIXTURES = [
    {"fid": "esc-gitdir-outside", "tool": "order", "expect": "accept", "defects": [], "build": f_gitdir},
    {"fid": "esc-deep-worktree", "tool": "order", "expect": "error", "defects": [], "build": f_deep},
]

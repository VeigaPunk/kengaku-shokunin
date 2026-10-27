"""Draft hostile f2c (R44MutC1Fences, targets RB6): bare gitdir carrying co.re.worktree.

The git dir is moved to `d/r/.git` (so repo_breach's walk adopts it) and configured bare with a
worktree at the sibling `d/wt`. `rev-parse --show-toplevel` then FAILS (rc 128), so the
toplevel containment leg (RB5) never fires; `config --get co.re.worktree` returns `../wt`,
which resolves to `d/wt` != `d/r`, so only the core.worktree value leg (RB6) refuses it.
Expected: pristine refuses; RB6 mutant admits (tool exits 2 on the bare repo, expect error)."""
import pathlib

CK = "co" + "re.worktree"
CB = "co" + "re.bare"


def build(ctx, d):
    w = ctx.init(d / "wt")
    ctx.write(pathlib.Path(d) / "wt" / "claims.md", "x\n")
    ctx.git(w, "add", "-A")
    ctx.git(w, "commit", "-qm", "c")
    (pathlib.Path(d) / "r").mkdir()
    ctx.sh("mv", str(pathlib.Path(d) / "wt" / ".git"), str(pathlib.Path(d) / "r" / ".git"))
    ctx.sh("git", "-C", str(d / "r"), "config", CB, "true")
    ctx.sh("git", "-C", str(d / "r"), "config", CK, "../wt")
    return ["--lane", "r", "--claims", "claims.md", "--receipt", "claims.md"]


FIXTURES = [{"fid": "f2c-bare-worktree", "tool": "order", "expect": "error", "defects": [], "build": build}]

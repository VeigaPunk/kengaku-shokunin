"""Round-44 hostile module f2 (`R43SentinelCounter` F2): a repo four levels down whose work tree is outside d.
Round-43 counter: admitted (depth cap); round-44 counter: SETUP refusal (toplevel outside the fixture)."""
import pathlib


def build(ctx, d):
    key = "co" + "re.worktree"
    r = pathlib.Path(d) / "x" / "y" / "z" / "r"
    ctx.init(r)
    ctx.write(r / "claims.md", "x\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "f")
    ctx.sh("git", "-C", str(r), "config", key, str(pathlib.Path(d).parent / "wt"))
    return ["--lane", "x/y/z/r", "--claims", "claims.md", "--receipt", "claims.md"]


FIXTURES = [{"fid": "f2-deep-worktree", "tool": "order", "expect": "error", "defects": [], "build": build}]

"""CONTROL: the honest shape both hostile modules are derived from (annotated tag + pack-refs + commit-graph)."""
def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.git(r, "tag", "-a", "v1", "-m", "tag one")
    ctx.git(r, "pack-refs", "--all")
    ctx.git(r, "commit-graph", "write", "--reachable", "--no-progress")
    return ["--lane", "repo"]
FIXTURES = [{"fid": "p07-honest-control", "tool": "anchor", "expect": None, "defects": None, "build": build}]

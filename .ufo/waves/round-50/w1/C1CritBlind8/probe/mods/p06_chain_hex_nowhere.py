"""chain row is a 40-hex with no graph file anywhere."""
def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.git(r, "commit-graph", "write", "--reachable", "--no-progress")
    ctx.write(r / ".git/objects/info/commit-graphs/commit-graph-chain", "b" * 40 + "\n")
    return ["--lane", "repo"]
FIXTURES = [{"fid": "p06-chain-hex-nowhere", "tool": "anchor", "expect": "error", "defects": [], "build": build}]

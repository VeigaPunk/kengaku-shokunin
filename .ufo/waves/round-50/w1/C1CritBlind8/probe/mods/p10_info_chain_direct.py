"""letter-(ii) literal alternative: `commit-graph-chain` placed directly in objects/info/."""
def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.git(r, "commit-graph", "write", "--reachable", "--no-progress")
    ctx.write(r / ".git/objects/info/commit-graph-chain", "/etc/hostname\n")
    return ["--lane", "repo"]
FIXTURES = [{"fid": "p10-info-chain-direct", "tool": "anchor", "expect": "error", "defects": [], "build": build}]

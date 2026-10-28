"""chain row is a 40-hex whose graph file exists only in an in-fixture outside store."""
def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.git(r, "commit-graph", "write", "--reachable", "--no-progress")
    single = r / ".git/objects/info/commit-graph"
    if single.read_bytes()[:4] != b"CGPH":
        raise RuntimeError("fixture defect: no CGPH")
    h = "a" * 40
    ctx.write(d / "outside-store/commit-graphs" / f"graph-{h}.graph", single.read_bytes())
    ctx.write(r / ".git/objects/info/commit-graphs/commit-graph-chain", h + "\n")
    return ["--lane", "repo"]
FIXTURES = [{"fid": "p05-chain-hex-outside-only", "tool": "anchor", "expect": "error", "defects": [], "build": build}]

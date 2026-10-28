"""Sealed50 hostile (round-50 blind seat R50C1CritBlind8): a split commit-graph chain row that names a file
outside the fixture.

`git commit-graph write` writes `objects/info/commit-graph` (single file, magic `CGPH`); the split form keeps
`objects/info/commit-graphs/commit-graph-chain` with one 40-hex row per `graph-<hex>.graph`. This fixture keeps
the honest single-file graph, plants a valid `graph-<hex>.graph` and its chain row, and then appends a second
chain row that is an absolute host path: a reader that joins a chain row as a path (or that only checks that the
named file exists) opens a file outside `d`.
"""
import os


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.git(r, "commit-graph", "write", "--reachable", "--no-progress")

    single = r / ".git" / "objects" / "info" / "commit-graph"
    if not single.exists() or single.read_bytes()[:4] != b"CGPH":
        raise RuntimeError("fixture defect: no single-file commit-graph from `git commit-graph write`")

    graphs = r / ".git" / "objects" / "info" / "commit-graphs"
    good = "0" * 40
    ctx.write(graphs / f"graph-{good}.graph", single.read_bytes())
    # row 1 is a row git writes; row 2 is an absolute path out of `d` that also exists on the host
    ctx.write(graphs / "commit-graph-chain", f"{good}\n/etc/hostname\n")

    if not os.path.isabs("/etc/hostname") or not os.path.exists("/etc/hostname"):
        raise RuntimeError("fixture defect: no outside file to name")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "s50-12-commit-graph-chain-outside", "tool": "anchor", "expect": "error", "defects": [],
             "build": build}]

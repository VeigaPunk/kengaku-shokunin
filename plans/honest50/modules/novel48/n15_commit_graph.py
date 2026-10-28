"""Round-48 C1 NEW honest class `n15_commit_graph`: `.git/objects/info/commit-graph` from `git commit-graph write`.

New in round 48 (not one of the nine round-46 classes). `git commit-graph write --reachable` writes one binary
file under `.git/objects/info/`; `git gc` writes the same file when `gc.writeCommitGraph` is enabled, so it is
an ordinary store entry on current git. It is not an object-store redirect: `objects/info/` also holds
`alternates` when a store is redirected, and a fence must distinguish the two by name and content, not by
refusing the directory. Every byte is inside `d`.

Authored against the BASE fence description only (`plans/fixture_fence.py` @ `a543d920`), never against a
repaired fence. Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.write(r / "b.txt", "two\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "two")
    ctx.git(r, "commit-graph", "write", "--reachable")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "n15-commit-graph", "tool": "anchor", "expect": None, "defects": None, "build": build}]

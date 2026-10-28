"""Round-49 C1 NEW honest class `n17_replace_ref`: one `git replace` entry under `refs/replace`.

New in round 49 (not one of the nine round-46 classes nor the seven round-48 ones). `git replace <object>
<replacement>` writes a single ref whose name is the replaced object's 40-hex id and whose value is the
replacement's 40-hex id — `refs/replace/<40hex>`. That filename is a 40-hex object name, not a path escape, and
the ref is a documented git namespace every user can create; the repository shape stays that of `git init` plus
two commits. Every byte is inside `d` and no store path is redirected.

Authored against the BASE fence description only (`plans/fixture_fence.py` @ round-49 stage-1 freeze
`9d2900af`, sha256 `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e` as pinned by this
population's builder), never against a repaired fence. Round-44 builder contract: `build(ctx, d)` fills `d` and
returns the argv tail.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.write(r / "b.txt", "two\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "two")
    first = ctx.sh("git", "-C", str(r), "rev-parse", "HEAD~1").stdout.strip()
    ctx.git(r, "replace", first, "HEAD")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "n17-replace-ref", "tool": "anchor", "expect": None, "defects": None, "build": build}]

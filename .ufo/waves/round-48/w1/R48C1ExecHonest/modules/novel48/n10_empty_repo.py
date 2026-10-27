"""Round-48 C1 NEW honest class `n10_empty_repo`: a fresh `git init` with no commit yet.

New in round 48 (not one of the nine round-46 classes). The single most ordinary `git init` state: `.git/HEAD`
names the unborn branch `refs/heads/master`, `refs/heads` and `refs/tags` are empty directories, there is no
`index`, no `logs/` and no object. Nothing is redirected and every byte is inside `d`; a fence that refuses it
refuses the state a fixture starts in before its first commit.

Authored against the BASE fence description only (`plans/fixture_fence.py` @ `a543d920`), never against a
repaired fence. Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""


def build(ctx, d):
    ctx.init(d / "repo")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "n10-empty-repo", "tool": "anchor", "expect": None, "defects": None, "build": build}]

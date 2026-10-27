"""Round-48 C1 NEW honest class `n14_stash_entry`: one `git stash` push.

New in round 48 (not one of the nine round-46 classes). `git stash push` writes `refs/stash` (a 40-hex file),
`logs/refs/stash`, `ORIG_HEAD` and two stash commit objects; all of it is ordinary store content inside `d`,
written by a user command that never reads or writes outside the repository. The base fence allows only
`refs/heads` and `refs/tags`, so `refs/stash` is refused; that is over-refusal of a documented git ref
namespace, not a containment breach.

Authored against the BASE fence description only (`plans/fixture_fence.py` @ `a543d920`), never against a
repaired fence. Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.write(r / "a.txt", "one, still being worked on\n")
    ctx.git(r, "stash", "push", "-q", "-m", "work in progress")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "n14-stash-entry", "tool": "anchor", "expect": None, "defects": None, "build": build}]

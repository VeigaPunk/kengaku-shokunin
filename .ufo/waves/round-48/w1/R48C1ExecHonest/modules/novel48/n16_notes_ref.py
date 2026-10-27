"""Round-48 C1 NEW honest class `n16_notes_ref`: one `git notes add` note on HEAD.

New in round 48 (not one of the nine round-46 classes). `git notes add` writes a note blob plus
`refs/notes/commits` and `logs/refs/notes/commits`; it is a documented ref namespace written entirely inside
`d` and read by `git log --notes`. The base fence allows only `refs/heads` and `refs/tags`, so `refs/notes` is
refused; that is over-refusal of an ordinary ref namespace, not containment.

Authored against the BASE fence description only (`plans/fixture_fence.py` @ `a543d920`), never against a
repaired fence. Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.git(r, "notes", "add", "-m", "fixture note on the first commit")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "n16-notes-ref", "tool": "anchor", "expect": None, "defects": None, "build": build}]

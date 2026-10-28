"""Round-48 C1 honest class `n03_detached_head`: `git checkout <sha>` leaves a 40-hex `.git/HEAD`.

Rebuilt from `.ufo/waves/round-46/w2/R46W2C1HoHonest.md` (nine novel honest classes, refused 9/9 by the base
fence): "detached HEAD". A detached HEAD is an ordinary consequence of inspecting an older commit; `.git/HEAD`
carries one 40-hex sha and every other byte stays inside `d`.

Authored against the BASE fence description only (`plans/fixture_fence.py` @ `a543d920`), never against a
repaired fence. Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    first = ctx.git(r, "rev-parse", "HEAD").stdout.strip()
    ctx.write(r / "b.txt", "two\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "two")
    ctx.git(r, "checkout", "-q", first)
    return ["--lane", "repo"]


FIXTURES = [{"fid": "n03-detached-head", "tool": "anchor", "expect": None, "defects": None, "build": build}]

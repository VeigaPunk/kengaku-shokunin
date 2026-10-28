"""Round-48 C1 honest class `n07_reflog_gc`: an expired reflog plus a packed object store.

Rebuilt from `.ufo/waves/round-46/w2/R46W2C1HoHonest.md` (nine novel honest classes, refused 9/9 by the base
fence): "reflog gc". `git reflog expire --expire=now --all` empties `logs/`, `git gc --prune=now` packs the
loose objects into `objects/pack/` and rewrites `packed-refs`; every path it writes is inside `d`.

Authored against the BASE fence description only (`plans/fixture_fence.py` @ `a543d920`), never against a
repaired fence. Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.write(r / "a.txt", "two\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "two")
    ctx.git(r, "reflog", "expire", "--expire=now", "--all")
    ctx.git(r, "gc", "--quiet", "--prune=now")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "n07-reflog-gc", "tool": "anchor", "expect": None, "defects": None, "build": build}]

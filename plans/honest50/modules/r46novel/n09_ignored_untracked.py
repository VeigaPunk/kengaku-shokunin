"""Round-48 C1 honest class `n09_ignored_untracked`: `.gitignore` plus an ignored, untracked file on disk.

Rebuilt from `.ufo/waves/round-46/w2/R46W2C1HoHonest.md` (nine novel honest classes, refused 9/9 by the base
fence): "an ignored untracked file". The ignored file is present in the worktree and absent from the index and
the store; the repository still holds only plain-init entries, all inside `d`.

Authored against the BASE fence description only (`plans/fixture_fence.py` @ `a543d920`), never against a
repaired fence. Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / ".gitignore", "*.tmp\n")
    ctx.write(r / "tracked.txt", "tracked\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "tracked files only")
    ctx.write(r / "scratch.tmp", "ignored worktree junk\n")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "n09-ignored-untracked", "tool": "anchor", "expect": None, "defects": None, "build": build}]

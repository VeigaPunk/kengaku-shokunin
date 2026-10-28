"""Round-48 C1 honest class `n05_gitignore`: a committed `.gitignore` in the worktree.

Rebuilt from `.ufo/waves/round-46/w2/R46W2C1HoHonest.md` (nine novel honest classes, refused 9/9 by the base
fence): "`.gitignore`". The file is a tracked blob; it changes no store entry and names nothing outside `d`.

Authored against the BASE fence description only (`plans/fixture_fence.py` @ `a543d920`), never against a
repaired fence. Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / ".gitignore", "*.log\nbuild/\n")
    ctx.write(r / "keep.txt", "kept\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "ignore patterns")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "n05-gitignore", "tool": "anchor", "expect": None, "defects": None, "build": build}]

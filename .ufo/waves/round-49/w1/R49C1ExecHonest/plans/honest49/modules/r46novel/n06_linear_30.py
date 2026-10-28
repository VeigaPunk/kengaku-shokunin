"""Round-48 C1 honest class `n06_linear_30`: a 30-commit linear history.

Rebuilt from `.ufo/waves/round-46/w2/R46W2C1HoHonest.md` (nine novel honest classes, refused 9/9 by the base
fence): "a 30-commit linear history". Thirty commits write thirty loose objects and three reflogs; no store
entry differs in kind from a one-commit repository, and every byte is inside `d`.

Authored against the BASE fence description only (`plans/fixture_fence.py` @ `a543d920`), never against a
repaired fence. Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""

COMMITS = 30


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "log.txt", "commit 0\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "commit 0")
    for i in range(1, COMMITS):
        ctx.write(r / "log.txt", "commit 0\n" + "".join(f"commit {j}\n" for j in range(1, i + 1)))
        ctx.git(r, "add", "-A")
        ctx.git(r, "commit", "-q", "-m", f"commit {i}")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "n06-linear-30", "tool": "anchor", "expect": None, "defects": None, "build": build}]

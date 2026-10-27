"""Round-48 C1 honest class `n04_merge_commit`: two parents on `refs/heads/master`.

Rebuilt from `.ufo/waves/round-46/w2/R46W2C1HoHonest.md` (nine novel honest classes, refused 9/9 by the base
fence): "a merge commit". `git merge --no-ff` writes one commit object with two parents and two `logs/`
entries; the store is still plain-init shaped and every byte is inside `d`.

Authored against the BASE fence description only (`plans/fixture_fence.py` @ `a543d920`), never against a
repaired fence. Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "base.txt", "base\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "base")
    ctx.git(r, "checkout", "-q", "-b", "side")
    ctx.write(r / "side.txt", "side\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "side work")
    ctx.git(r, "checkout", "-q", "master")
    ctx.write(r / "main.txt", "main\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "main work")
    ctx.git(r, "merge", "-q", "--no-ff", "-m", "merge side", "side")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "n04-merge-commit", "tool": "anchor", "expect": None, "defects": None, "build": build}]

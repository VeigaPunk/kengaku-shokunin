"""Round-48 C1 honest class `n02_annotated_tag`: an annotated tag object and its `refs/tags` file.

Rebuilt from `.ufo/waves/round-46/w2/R46W2C1HoHonest.md` (nine novel honest classes, refused 9/9 by the base
fence): "annotated tags". `git tag -a` writes one tag object plus `refs/tags/<name>` holding a 40-hex sha,
exactly the shape plain `git init` + `git commit` + `git tag -a` leaves; nothing is redirected outside `d`.

Authored against the BASE fence description only (`plans/fixture_fence.py` @ `a543d920`), never against a
repaired fence. Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "notes.txt", "tagged release\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "tagged commit")
    ctx.git(r, "tag", "-a", "v1.0.0", "-m", "release 1.0.0")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "n02-annotated-tag", "tool": "anchor", "expect": None, "defects": None, "build": build}]

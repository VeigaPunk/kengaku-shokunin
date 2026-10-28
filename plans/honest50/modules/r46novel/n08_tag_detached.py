"""Round-48 C1 honest class `n08_annotated_tag_detached_head`: both states in one repository.

Rebuilt from `.ufo/waves/round-46/w2/R46W2C1HoHonest.md` (nine novel honest classes, refused 9/9 by the base
fence): "annotated-tag-plus-detached-HEAD". The two ordinary states compose: a 40-hex `.git/HEAD` beside a
tag object and its `refs/tags` entry, all inside `d`.

Authored against the BASE fence description only (`plans/fixture_fence.py` @ `a543d920`), never against a
repaired fence. Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.git(r, "tag", "-a", "v0.1.0", "-m", "pre-release")
    first = ctx.git(r, "rev-parse", "HEAD").stdout.strip()
    ctx.write(r / "a.txt", "two\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "two")
    ctx.git(r, "checkout", "-q", first)
    return ["--lane", "repo"]


FIXTURES = [{"fid": "n08-tag-detached", "tool": "anchor", "expect": None, "defects": None, "build": build}]

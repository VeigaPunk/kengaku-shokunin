"""Sealed50 hostile: an anchor argv whose `--lane` normalises outside the fixture.

Witnesses the argv containment leg (`_argv`): a fence that resolves argv values without a containment check
admits a decision that names a path outside `d`.
"""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.init(d.parent / "outside-lane")
    return ["--lane", "../outside-lane", "--evidence-ref", "repo/a.txt"]


FIXTURES = [{"fid": "s50-07-argv-escape", "tool": "anchor", "expect": "error", "defects": [], "build": build}]

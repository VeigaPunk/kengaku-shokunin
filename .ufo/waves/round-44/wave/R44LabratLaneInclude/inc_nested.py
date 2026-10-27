"""Probe fixture (labrat, round 44): include.path names a scratch file that itself includes the lane's git config
(a path in the read-only home that the tool sandbox hides). Tests whether the PARENT process reads it."""

OUTSIDE = "/fast/scratch/hyaku/kengaku-r44/R44LabratLaneInclude/outside/inc_nested.cfg"


def build(ctx, d):
    repo = ctx.init(d / "repo")
    ctx.git(repo, "config", "include.path", OUTSIDE)
    return ["--lane", "repo"]


FIXTURES = [
    {"fid": "probe-include-nested", "tool": "anchor", "expect": "reject", "defects": [], "build": build},
]

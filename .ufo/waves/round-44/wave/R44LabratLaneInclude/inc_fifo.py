"""Probe fixture (labrat, round 44): include.path names a FIFO outside d, so the parent-side git of lane_breach()
blocks on open() until the counter's 30 s timeout (F4) kills it."""

OUTSIDE = "/fast/scratch/hyaku/kengaku-r44/R44LabratLaneInclude/outside/fifo.cfg"


def build(ctx, d):
    repo = ctx.init(d / "repo")
    ctx.git(repo, "config", "include.path", OUTSIDE)
    return ["--lane", "repo"]


FIXTURES = [
    {"fid": "probe-include-fifo", "tool": "anchor", "expect": "reject", "defects": [], "build": build},
]

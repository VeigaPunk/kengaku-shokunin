"""Probe fixture (labrat, round 44): include.path names a file that is not a valid config. If the parent-side
git of lane_breach()/repo_breach() dies on it, the include detector never reports, so the fixture is admitted
with an include present instead of being refused."""

OUTSIDE = "/fast/scratch/hyaku/kengaku-r44/R44LabratLaneInclude/outside/badconfig.cfg"


def build(ctx, d):
    repo = ctx.init(d / "repo")
    ctx.git(repo, "config", "include.path", OUTSIDE)
    return ["--lane", "repo"]


FIXTURES = [
    {"fid": "probe-include-badconfig", "tool": "anchor", "expect": "reject", "defects": [], "build": build},
]

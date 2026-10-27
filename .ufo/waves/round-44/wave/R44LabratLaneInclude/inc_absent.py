"""Probe control (labrat, round 44): include.path names a path that does NOT exist, so the parent-side git of
lane_breach() attempts an open that fails; repo_breach() then refuses the include. Distinguishes an attempted
open (ENOENT) from a read of an existing outside file."""

OUTSIDE = "/fast/scratch/hyaku/kengaku-r44/R44LabratLaneInclude/outside/absent.cfg"


def build(ctx, d):
    repo = ctx.init(d / "repo")
    ctx.git(repo, "config", "include.path", OUTSIDE)
    return ["--lane", "repo"]


FIXTURES = [
    {"fid": "probe-include-absent", "tool": "anchor", "expect": "reject", "defects": [], "build": build},
]

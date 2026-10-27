"""Probe fixture (labrat, round 44): a repo inside d whose .git/config carries include.path pointing at a file
OUTSIDE the fixture directory. Nothing else is special: the fixture asks only for `--lane repo`.
The build child runs with the fixture dir writable, so the include line is written by git itself."""

OUTSIDE = "/fast/scratch/hyaku/kengaku-r44/R44LabratLaneInclude/outside/inc_benign.cfg"


def build(ctx, d):
    repo = ctx.init(d / "repo")
    ctx.git(repo, "config", "include.path", OUTSIDE)
    return ["--lane", "repo"]


FIXTURES = [
    {"fid": "probe-include-benign", "tool": "anchor", "expect": "reject", "defects": [], "build": build},
]

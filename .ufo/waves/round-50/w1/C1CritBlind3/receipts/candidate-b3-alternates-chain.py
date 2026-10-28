"""Scratch control (NOT a deliverable, NOT production): the same repair hazard as blind module `b1`, one level
deeper. `lane/.git/objects/info/alternates` names `../../../store/objects`, a directory INSIDE `d` that is not a
repository (no `.git` marker, so `_tree` never classifies it), and that directory's own
`info/alternates` names a store OUTSIDE `d`.

Why it matters: a repair that checks "every alternates entry resolves inside d" once per repository under `d`
admits this fixture (the first entry is inside d) while the object bytes are still read outside `d`. git follows
the borrow graph recursively (`strace` receipt in the seat report), so containment must be checked along the
whole graph, not per repository.
"""
import os
import pathlib
import shutil


def build(ctx, d):
    d = pathlib.Path(d)
    far = ctx.init(d.parent / "far-store")
    ctx.write(far / "far.txt", "only outside d\n")
    ctx.git(far, "add", "-A")
    ctx.git(far, "commit", "-qm", "far")
    farsha = ctx.sh("git", "-C", str(far), "rev-parse", "HEAD").stdout.strip()

    mid = ctx.init(d / "mid")
    ctx.write(mid / "m.txt", "middle\n")
    ctx.git(mid, "add", "-A")
    ctx.git(mid, "commit", "-qm", "middle")
    store = d / "store"
    shutil.move(str(mid / ".git"), str(store))
    shutil.rmtree(mid)

    lane = ctx.init(d / "lane")
    ctx.write(lane / "l.txt", "local\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "local")

    first = os.path.relpath(store / "objects", lane / ".git" / "objects")
    ctx.write(lane / ".git/objects/info/alternates", first + "\n")
    second = os.path.relpath(far / ".git" / "objects", store / "objects")
    ctx.write(store / "objects/info/alternates", second + "\n")
    ctx.sh("git", "-C", str(lane), "cat-file", "-t", farsha)
    return ["--lane", "lane"]


FIXTURES = [{"fid": "ctl-alternates-chain-outside", "tool": "anchor", "expect": "reject", "defects": [],
             "build": build}]

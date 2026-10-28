"""Scratch control (NOT a deliverable, NOT production): the honest counterpart that keeps a repair from
over-correcting blind module `b1`.

    main/    a plain-init repository inside `d`
    lane/    alternates -> `../../../main/.git/objects` (inside `d`) and `refs/replace/<lane commit>` ->
             <main commit>

Every byte is inside `d`; the replaced object lives in the sibling in-`d` store, not in `lane`'s own objects
directory. git writes this state (`git replace` accepts the target precisely because the in-`d` alternate
resolves it) and `git -C lane log` follows it. A repair that closes `b1` by demanding "the replace target must
exist in this repository's own loose objects or pack" refuses this fixture: that is over-refusal, and it is why
the containment rule belongs on the alternates graph, not on the replace target.
"""
import os
import pathlib


def build(ctx, d):
    d = pathlib.Path(d)
    main = ctx.init(d / "main")
    ctx.write(main / "m.txt", "in d\n")
    ctx.git(main, "add", "-A")
    ctx.git(main, "commit", "-qm", "main")
    target = ctx.sh("git", "-C", str(main), "rev-parse", "HEAD").stdout.strip()

    lane = ctx.init(d / "lane")
    ctx.write(lane / "a.txt", "one\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "one")
    ctx.write(lane / "b.txt", "two\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "two")
    orig = ctx.sh("git", "-C", str(lane), "rev-parse", "HEAD~1").stdout.strip()

    entry = os.path.relpath(main / ".git" / "objects", lane / ".git" / "objects")
    ctx.write(lane / ".git/objects/info/alternates", entry + "\n")
    ctx.git(lane, "replace", orig, target)
    return ["--lane", "lane"]


FIXTURES = [{"fid": "ctl-replace-target-in-d-alternate", "tool": "anchor", "expect": "admit", "defects": [],
             "build": build}]

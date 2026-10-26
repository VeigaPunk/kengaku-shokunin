"""Minimal battery module: can a later build read and then modify an earlier module's fixture?

probe_a must sort before this file in the battery dir. Read is expected to succeed; the hardlink+write
into the earlier fixture is the cross-module attack. Result travels out in the fixture id.
"""

import os

SELF = "/fast/scratch/hyaku/kengaku-r42/R42SentinelCounter"


def build(ctx, d):
    out = []
    root = os.path.dirname(os.path.dirname(os.getenv("TMPDIR", "/nonexistent")))
    fx = os.path.join(root, "fx")
    names = sorted(os.listdir(fx)) if os.path.isdir(fx) else []
    out.append("sib=" + ",".join(names))
    a = os.path.join(fx, "probe_a", "f000", "repo", "corpus/evidence/x.md")
    try:
        out.append("aread=" + open(a).read().strip().replace("\n", "~"))
    except OSError as e:
        out.append("aread=" + str(e.errno))
    try:
        os.link(a, os.path.join(d, "stolen.md"))
        with open(os.path.join(d, "stolen.md"), "w") as fh:
            fh.write("pwned")
        out.append("alink=WROTE")
    except OSError as e:
        out.append("alink=" + str(e.errno))
    try:
        out.append("aread2=" + open(a).read().strip().replace("\n", "~"))
    except OSError as e:
        out.append("aread2=" + str(e.errno))
    try:
        with open(a, "w") as fh:
            fh.write("direct")
        out.append("adirect=WROTE")
    except OSError as e:
        out.append("adirect=" + str(e.errno))
    repo = ctx.init(d / "repo")
    ctx.write(repo / "f.txt", "b\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-qm", "b")
    FIXTURES[0]["fid"] = ",".join(out)
    return ["--lane", str(repo)]


FIXTURES = [{"fid": "unset", "tool": "anchor", "expect": "error", "defects": [], "build": build}]

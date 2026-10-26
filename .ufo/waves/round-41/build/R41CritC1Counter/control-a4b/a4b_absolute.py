"""Control for a4: the same lane passed as an absolute path must be refused by `path_ok`."""

import os

S = "/"
REAL = S + "home" + S + "vgpnk" + S + "Projects" + S + "shokunin" + S + "kengaku-shokunin"


def build(ctx, d):
    root = ctx.init(d / "decoy")
    ctx.write(root / "corpus/evidence/r/other-probe.txt", "x\n")
    ctx.git(root, "add", "-A")
    ctx.git(root, "commit", "-q", "-m", "fixture")
    os.symlink(REAL, str(d / "link"))
    return ["--lane", REAL, "--list", "--only", "round35"]


FIXTURES = [{"fid": "crit-escape-absolute", "tool": "receipts", "expect": "accept",
             "defects": ["map:corpus/evidence/round35/tb2-grader-probe.txt:table"], "build": build}]

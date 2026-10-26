"""`path_ok` only examines tokens that start with `/`: a relative token leaves the fixture dir.

The fixture builds a decoy lane inside d that carries no `round35` receipt, then hands the tool `--lane link`
where `link` is a symlink to the host lane. The class the fixture declares can only come from the host lane, so
`wrong=0` on this fixture proves the tool read a tree outside d.
"""

import os

S = "/"
REAL = S + "home" + S + "vgpnk" + S + "Projects" + S + "shokunin" + S + "kengaku-shokunin"


def build(ctx, d):
    root = ctx.init(d / "decoy")
    ctx.write(root / "corpus/evidence/r/other-probe.txt", "x\n")
    ctx.git(root, "add", "-A")
    ctx.git(root, "commit", "-q", "-m", "fixture")
    os.symlink(REAL, str(d / "link"))
    return ["--lane", "link", "--list", "--only", "round35"]


FIXTURES = [{"fid": "crit-escape-link", "tool": "receipts", "expect": "accept",
             "defects": ["map:corpus/evidence/round35/tb2-grader-probe.txt:table"], "build": build}]

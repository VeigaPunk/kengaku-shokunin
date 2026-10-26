"""Control for a4: the same in-tree symlink named by an ABSOLUTE token is refused by `path_ok`."""
import os

S = "/"
REAL = S + "home" + S + "vgpnk" + S + "Projects" + S + "shokunin" + S + "kengaku-shokunin"


def build(ctx, d):
    root = ctx.init(d / "decoy")
    ctx.write(root / "corpus/evidence/r/other-probe.txt", "x\n")
    ctx.git(root, "add", "-A")
    ctx.git(root, "commit", "-q", "-m", "fixture")
    os.symlink(REAL, str(d / "link"))
    return ["--lane", str(d / "link"), "--list", "--only", "round35"]


FIXTURES = [{"fid": "crit-escape-abs-link", "tool": "receipts", "expect": "accept",
             "defects": ["map:corpus/evidence/round35/tb2-grader-probe.txt:table"], "build": build}]

"""`_refs` liveness probe 1 (scratch, NOT a deliverable): a second branch file with a body that is not a
40-hex sha. If a repair drops the `_refs` call (the R50C1ExecRepair finding: n17 passing "by absence"), nothing
checks ref bodies and this is ADMITted. A fence that admits it is not measuring refs at all."""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "one")
    ctx.write(r / ".git/refs/heads/junk-branch", "not-a-sha\n")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "p-junk-branch-body", "tool": "anchor", "expect": "reject", "defects": [], "build": build}]

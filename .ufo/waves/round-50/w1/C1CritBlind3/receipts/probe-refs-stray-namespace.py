"""`_refs` liveness probe 2 (scratch, NOT a deliverable): a `refs/` subdirectory git does not write for this
population (`refs/foo/bar`) holding a well-formed 40-hex ref. Only a real namespace rule refuses it."""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "one")
    head = ctx.sh("git", "-C", str(r), "rev-parse", "HEAD").stdout.strip()
    ctx.write(r / ".git/refs/foo/bar", head + "\n")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "p-stray-ref-namespace", "tool": "anchor", "expect": "reject", "defects": [], "build": build}]

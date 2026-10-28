"""`_refs` liveness probe 3 (scratch, NOT a deliverable): a correctly named `refs/replace/<40hex>` whose body is
not a 40-hex sha. The honest `n17` shape must be admitted; the same name with a junk body must not be. A repair
that admits `refs/replace` by NAME only (no body test) admits this."""


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "one")
    head = ctx.sh("git", "-C", str(r), "rev-parse", "HEAD").stdout.strip()
    ctx.write(r / ".git/refs/replace" / head, "not-a-sha\n")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "p-replace-body-junk", "tool": "anchor", "expect": "reject", "defects": [], "build": build}]

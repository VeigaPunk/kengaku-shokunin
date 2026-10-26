"""Draft control D6 (R42MutC1Counter): a {WORK}-token argv must not contain .. either.
The intact counter rejects this fixture in the build contract (SETUP, exit 2); a counter whose WORK branch
of path_ok returns True accepts it and runs the tool against a path outside the run work dir."""
def b(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "corpus/SOURCES.md", "no rows\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "fixture")
    return ["--lane", "{WORK}/../../out"]

FIXTURES = [{"fid": "d6-work-escape", "tool": "anchor", "expect": "accept", "defects": [], "build": b}]

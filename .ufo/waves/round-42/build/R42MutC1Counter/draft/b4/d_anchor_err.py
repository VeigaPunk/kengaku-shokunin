"""Draft control D4 (R42MutC1Counter): an error-direction hit requires the mutant to exit 0 or 1, never 2.
The fixture makes the anchor tool die in argparse (invalid --evidence-ref choice, exit 2). With the no-op
mutant ERR1 the intact counter must print SURVIVED; a counter that widens the error branch to accept rc=2
counts a fake attributed kill."""
def b(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "corpus/SOURCES.md", "no rows\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "fixture")
    return ["--lane", str(r), "--evidence-ref=bogus"]

FIXTURES = [{"fid": "d4-errorexit", "tool": "anchor", "expect": "error", "defects": [], "build": b}]

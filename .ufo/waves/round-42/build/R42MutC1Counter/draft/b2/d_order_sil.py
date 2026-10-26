"""Draft control D2 (R42MutC1Counter): an rc-silence hit must require expect=reject.
The repo's freeze commit already carries the receipt, so the reference exits 1, but the fixture wrongly
declares expect=accept. The intact counter does not count XO1; a counter that drops the expect check does."""
def b(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / ".ufo/waves/round-9/claims/round-9-claims.md", "# claims draft d2\n")
    ctx.write(r / ".ufo/waves/round-9/claims/receipt.txt", "receipt draft d2\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "claims and receipt together")
    return ["--lane", str(r), "--claims", ".ufo/waves/round-9/claims/round-9-claims.md",
            "--receipt", ".ufo/waves/round-9/claims/receipt.txt"]

FIXTURES = [{"fid": "d2-wrongaccept", "tool": "order", "expect": "accept", "defects": [], "build": b}]

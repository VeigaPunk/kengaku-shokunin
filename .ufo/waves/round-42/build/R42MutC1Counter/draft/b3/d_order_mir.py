"""Draft control D3 (R42MutC1Counter): an rc-mirror hit must require expect=accept.
A claims blob with a P10 PASS line is committed before the receipt: the reference exits 0 (PASS is not a
verdict it matches), the XO6 mutant exits 1, but the fixture wrongly declares expect=reject."""
def b(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / ".ufo/waves/round-9/claims/round-9-claims.md", "# claims draft d3\nP10 PASS whatever\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "claims")
    ctx.write(r / "receipt.txt", "receipt draft d3\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "receipt")
    return ["--lane", str(r), "--claims", ".ufo/waves/round-9/claims/round-9-claims.md",
            "--receipt", "receipt.txt"]

FIXTURES = [{"fid": "d3-wrongreject", "tool": "order", "expect": "reject", "defects": [], "build": b}]

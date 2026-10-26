"""Draft control D1 (R42MutC1Counter): pair-direction hits must require the fixture to declare that expect.
Two fixtures with the same repo shape (post-receipt P10-ok blob): one declares accept (a legal rc-mirror-style
kill for XO5 relabelled 0>1), one wrongly declares reject. The intact counter kills with hits=1; a counter that
drops the want==a check in the pair branch also counts the wrong fixture and prints hits=2."""
def mk(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / ".ufo/waves/round-9/claims/round-9-claims.md", "# claims draft d1\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "claims")
    ctx.write(r / "receipt.txt", "receipt draft d1\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "receipt")
    ctx.write(r / ".ufo/waves/round-9/claims/note.md", "P10 ok filler\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "note")
    return r

def bk(ctx, d):
    r = mk(ctx, d)
    return ["--lane", str(r), "--claims", ".ufo/waves/round-9/claims/round-9-claims.md",
            "--receipt", "receipt.txt"]

FIXTURES = [
    {"fid": "d1-kill", "tool": "order", "expect": "accept", "defects": [], "build": bk},
    {"fid": "d1-wrongreject", "tool": "order", "expect": "reject", "defects": [], "build": bk},
]

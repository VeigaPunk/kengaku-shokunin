"""Round-42 substitute XO1, argv spelled with an ABSOLUTE path inside d for the receipt. Leg i checks
'HEAD:<raw token>' (absolute -> not a valid rev spec -> refused silently by the git call itself); the
tool normalizes absolute paths back into the repo. Same potential fence gap as the './' spelling.
"""


def build_rdir_abs(ctx, d):
    repo = d / "repo"
    ctx.init(repo)
    ctx.write(repo / "plans/round-43-claims.md", "# claims\nclean\n")
    ctx.write(repo / "corpus/evidence/r43/claimsdir/placeholder.txt", "x")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "freeze")
    return ["--lane", str(repo), "--claims", "plans/round-43-claims.md",
            "--receipt", str(repo / "corpus/evidence/r43/claimsdir")]


FIXTURES = [
    {"fid": "o-receipt-dir-abs", "tool": "order", "expect": "reject", "defects": [],
     "build": build_rdir_abs},
]

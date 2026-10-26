"""Round-42 substitute XO1 re-tried against leg i: --receipt names a DIRECTORY that exists at HEAD
(as a tree). Leg i must refuse the fixture at build time.
"""


def build_rdir(ctx, d):
    repo = d / "repo"
    ctx.init(repo)
    ctx.write(repo / "plans/round-43-claims.md", "# claims\nclean\n")
    ctx.write(repo / "corpus/evidence/r43/claimsdir/placeholder.txt", "x")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "freeze")
    return ["--lane", str(repo), "--claims", "plans/round-43-claims.md",
            "--receipt", "corpus/evidence/r43/claimsdir"]


FIXTURES = [
    {"fid": "o-receipt-dir", "tool": "order", "expect": "reject", "defects": [],
     "build": build_rdir},
]

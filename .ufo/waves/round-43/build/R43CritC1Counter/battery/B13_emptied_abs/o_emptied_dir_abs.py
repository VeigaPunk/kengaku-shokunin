"""Round-42 substitute XO3 (emptied-directory) with an ABSOLUTE --receipt argv: same tree-at-HEAD
history as B11, but leg i sees 'HEAD:<absolute path>', which git treats as an invalid rev spec, so the
blob check is bypassed. Documents the leg-i fence gap for absolute spellings.
"""


def build_emptied_abs(ctx, d):
    repo = d / "repo"
    ctx.init(repo)
    claims = "plans/round-43-claims.md"
    ctx.write(repo / claims, "# claims\nclean\n")
    ctx.write(repo / "corpus/evidence/r43/claimsdir/placeholder.txt", "x")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "freeze")
    ctx.sh("git", "-C", str(repo), "rm", "-q", "-r", "corpus/evidence/r43/claimsdir")
    ctx.git(repo, "commit", "-q", "-m", "empty")
    ctx.write(repo / "corpus/evidence/r43/claimsdir/again.txt", "y")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "recreate")
    receipt = str(repo / "corpus/evidence/r43/claimsdir")
    return ["--lane", str(repo), "--claims", claims, "--receipt", receipt]


FIXTURES = [
    {"fid": "o-emptied-dir-abs", "tool": "order", "expect": "reject", "defects": [],
     "build": build_emptied_abs},
]

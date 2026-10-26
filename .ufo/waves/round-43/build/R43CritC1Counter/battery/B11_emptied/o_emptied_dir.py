"""Round-42 substitute XO3 (emptied-directory) re-tried against leg i: the receipt path is a directory
created in commit 1, emptied and removed in commit 2, and re-created (with a placeholder) after the
freeze so it exists at HEAD as a tree. Leg i must refuse both spellings (plain relative and absolute).
"""


def build_emptied(ctx, d, abs_argv):
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
    receipt = str(repo / "corpus/evidence/r43/claimsdir") if abs_argv else "corpus/evidence/r43/claimsdir"
    return ["--lane", str(repo), "--claims", claims, "--receipt", receipt]


def build_emptied_rel(ctx, d):
    return build_emptied(ctx, d, False)


def build_emptied_abs(ctx, d):
    return build_emptied(ctx, d, True)


FIXTURES = [
    {"fid": "o-emptied-dir", "tool": "order", "expect": "reject", "defects": [],
     "build": build_emptied_rel},
    {"fid": "o-emptied-dir-abs", "tool": "order", "expect": "reject", "defects": [],
     "build": build_emptied_abs},
]

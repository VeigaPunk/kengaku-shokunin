import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    d = pathlib.Path(d)
    outside = d.parent / "worktree-config"
    ctx.write(outside, "[user]\n\temail = WORKTREE-OUTSIDE@invalid\n")
    repo = ctx.init(d / "lane")
    ctx.write(repo / CLAIMS, "nothing ran\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-qm", "claims")
    ctx.write(repo / RECEIPT, "receipt\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-qm", "receipt")
    (repo / ".git/config").write_text("[extensions]\n\tworktreeConfig = true\n")
    (repo / ".git/config.worktree").write_text("[include]\n\tpath = " + str(outside) + "\n")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "sealed-worktree-config-include", "tool": "order", "expect": "accept", "defects": [], "build": build}]

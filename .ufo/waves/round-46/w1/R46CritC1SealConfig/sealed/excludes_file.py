import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    d = pathlib.Path(d)
    outside = d.parent / "exclude-rules"
    ctx.write(outside, "*.secret\n")
    repo = ctx.init(d / "lane")
    ctx.write(repo / CLAIMS, "nothing ran\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-qm", "claims")
    ctx.write(repo / RECEIPT, "receipt\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-qm", "receipt")
    with (repo / ".git/config").open("a") as f:
        f.write("[core]\n\texcludesFile = " + str(outside) + "\n")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "sealed-core-excludes-file", "tool": "order", "expect": "accept", "defects": [], "build": build}]

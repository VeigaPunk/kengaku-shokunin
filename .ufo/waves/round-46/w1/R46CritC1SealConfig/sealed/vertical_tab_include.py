import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    d = pathlib.Path(d)
    outside = d.parent / "vt-include.cfg"
    ctx.write(outside, "[user]\n\temail = VT-INCLUDE-OUTSIDE@invalid\n")
    repo = ctx.init(d / "lane")
    ctx.write(repo / CLAIMS, "nothing ran\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-qm", "claims")
    ctx.write(repo / RECEIPT, "receipt\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-qm", "receipt")
    (repo / ".git/config").write_bytes(("\x0b[include]\n\tpath = " + str(outside) + "\n").encode())
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "sealed-vt-include", "tool": "order", "expect": "accept", "defects": [], "build": build}]

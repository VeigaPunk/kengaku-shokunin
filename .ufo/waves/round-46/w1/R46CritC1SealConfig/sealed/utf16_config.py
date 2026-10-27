import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    d = pathlib.Path(d)
    outside = d.parent / "utf16-include.cfg"
    ctx.write(outside, "[user]\n\temail = UTF16-OUTSIDE@invalid\n")
    repo = ctx.init(d / "lane")
    ctx.write(repo / CLAIMS, "nothing ran\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-qm", "claims")
    ctx.write(repo / RECEIPT, "receipt\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-qm", "receipt")
    raw = ("[include]\n\tpath = " + str(outside) + "\n").encode("utf-16")
    (repo / ".git/config").write_bytes(raw)
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "sealed-utf16-config-include", "tool": "order", "expect": "accept", "defects": [], "build": build}]

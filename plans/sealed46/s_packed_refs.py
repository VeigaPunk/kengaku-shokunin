import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    d = pathlib.Path(d)
    r = ctx.init(d / "lane")
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    ctx.git(r, "pack-refs", "--all", "--prune")
    outside = d.parent / "store-packed-refs"
    outside.mkdir()
    ctx.write(outside / "packed-refs", (r / ".git" / "packed-refs").read_bytes())
    (r / ".git" / "packed-refs").unlink()
    (r / ".git" / "packed-refs").symlink_to(outside / "packed-refs")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "seal-packed-refs-link", "tool": "order", "expect": "accept", "defects": [], "build": build}]

import pathlib
import shutil

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
    outside = d.parent / "store-refs"
    outside.mkdir()
    shutil.move(str(r / ".git" / "refs"), outside / "refs")
    (r / ".git" / "refs").symlink_to(outside / "refs", target_is_directory=True)
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "seal-refs-link", "tool": "order", "expect": "accept", "defects": [], "build": build}]

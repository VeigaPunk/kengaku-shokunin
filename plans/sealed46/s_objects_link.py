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
    outside = d.parent / "store-objects"
    outside.mkdir()
    shutil.move(str(r / ".git" / "objects"), outside / "objects")
    (r / ".git" / "objects").symlink_to(outside / "objects", target_is_directory=True)
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "seal-objects-link", "tool": "order", "expect": "accept", "defects": [], "build": build}]

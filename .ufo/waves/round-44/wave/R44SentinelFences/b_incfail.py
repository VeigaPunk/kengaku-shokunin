"""Fixture shape: the repo's primary config file includes a file outside d that is not valid config. Every
git call then aborts (rc != 0), and every store-fence check is guarded by `rc == 0`, so the fixture is
admitted while the outside file has already been opened and parsed.
"""
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    d = pathlib.Path(d)
    side = d.parent / "broken.cfg"
    r = ctx.init(d / "lane")
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    with open(r / ".git/config", "a") as fh:
        fh.write(f"[include]\n\tpath = {side}\n")
    ctx.write(side, "[this line is not config\n")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "broken-include-admitted", "tool": "order", "expect": "error", "defects": [], "build": build}]

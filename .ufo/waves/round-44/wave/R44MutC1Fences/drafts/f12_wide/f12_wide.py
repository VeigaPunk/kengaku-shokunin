"""Draft hostile f12 (R44MutC1Fences, targets RB2): a fixture tree exceeding the F2 entry bound.

F2 replaced the round-43 depth cap with a visited-entry bound of 200000 that refuses a
pathological tree instead of skipping it. No hostile module builds more than a handful of
entries, so the bound itself is unexercised. This module builds 200050 empty directories under
`d/bulk` beside an honest lane repo.
Expected: pristine refuses ("fixture tree exceeds 200000 entries"); RB2 (bound disabled) mutant
walks the whole tree, finds no breach and admits."""
import pathlib

CL = ".ufo/waves/round-42/claims/round-42-claims.md"
RC = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    r = ctx.init(d / "lane")
    ctx.write(pathlib.Path(d) / "lane" / CL, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(pathlib.Path(d) / "lane" / RC, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    ctx.sh("/usr/bin/python3", "-c",
           "import os, sys\n"
           "for i in range(200050):\n"
           "    os.makedirs(os.path.join(sys.argv[1], 'd%05d' % i), exist_ok=True)",
           str(pathlib.Path(d) / "bulk"))
    return ["--lane", "lane", "--claims", CL, "--receipt", RC]


FIXTURES = [{"fid": "f12-wide-tree", "tool": "order", "expect": "accept", "defects": [], "build": build}]

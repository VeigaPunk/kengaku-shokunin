"""Draft hostile f3b (R44MutC1Fences, targets OA1): contract-shaped argv, `--claims` names a TREE at HEAD.

f3 covers the same scenario behind an argparse abbreviation, which argv_shape_breach (F3) refuses
first, so leg i (order_argv_breach's HEAD-blob check) is never exercised by the six hostile modules.
Here the argv is exactly `--lane V --claims V --receipt V` and the claims path is a directory at
HEAD, so only the blob check refuses it.
Expected: pristine refuses ("is a tree at HEAD, not a blob"); OA1 mutant admits."""
import pathlib

CL = ".ufo/waves/round-42/claims/round-42-claims.md"
RC = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    r = ctx.init(d / "lane")
    ctx.write(pathlib.Path(d) / "lane" / (CL + "/x.md"), "# a directory standing in for the claims file\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(pathlib.Path(d) / "lane" / RC, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    return ["--lane", str(r), "--claims", CL, "--receipt", RC]


FIXTURES = [{"fid": "f3b-tree-exact", "tool": "order", "expect": "error", "defects": [], "build": build}]

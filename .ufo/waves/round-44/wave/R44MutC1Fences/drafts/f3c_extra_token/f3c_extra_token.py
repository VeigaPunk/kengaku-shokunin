"""Draft hostile f3c (R44MutC1Fences, targets AS1): order argv with an EXTRA trailing token.

The argv is the contract triple followed by a dangling `--verbose`, so the values of all three
options still pair up (lane_breach, repo_breach and the HEAD-blob leg all pass) and only the
length/shape half of argv_shape_breach refuses it. f3 (abbreviation) is caught by the shape leg
too, so it cannot separate AS1 from the KeyError accident in order_argv_breach.
Expected: pristine refuses (argv is not the contract shape); AS1 mutant admits."""
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
    return ["--lane", str(r), "--claims", CL, "--receipt", RC, "--verbose"]


FIXTURES = [{"fid": "f3c-extra-token", "tool": "order", "expect": "error", "defects": [], "build": build}]

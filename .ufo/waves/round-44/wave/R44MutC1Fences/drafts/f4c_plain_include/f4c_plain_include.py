"""Draft hostile f4c (R44MutC1Fences, targets RB4): config include naming a PLAIN readable file outside d.

f4's include target is a FIFO, so disabling the include leg (RB4) does not admit f4: lane_breach's
`rev-parse` follows the include, blocks on the FIFO and is refused by its own 30 s timeout. A plain
include target does not block, so with the include leg disabled every guard passes even though the
fixture's config parsed a file outside d.
Expected: pristine refuses ("lane/.git/config carries an include"); RB4 mutant admits."""
import pathlib

CL = ".ufo/waves/round-42/claims/round-42-claims.md"
RC = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    ctx.write(pathlib.Path(d).parent / "extra.cfg", "[co]\n\tfacts = true\n")
    r = ctx.init(d / "lane")
    ctx.write(pathlib.Path(d) / "lane" / CL, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(pathlib.Path(d) / "lane" / RC, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    ctx.sh("git", "-C", str(r), "config", "--add", "include.path", str(pathlib.Path(d).parent / "extra.cfg"))
    return ["--lane", "lane", "--claims", CL, "--receipt", RC]


FIXTURES = [{"fid": "f4c-plain-include", "tool": "order", "expect": "accept", "defects": [], "build": build}]

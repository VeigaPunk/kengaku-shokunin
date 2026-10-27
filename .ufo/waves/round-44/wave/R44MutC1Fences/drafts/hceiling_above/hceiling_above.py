"""Draft fixture hceiling (R44MutC1Fences, targets PG2): HONEST-direction catcher for the ceiling.

pin_git pins GIT_CEILING_DIRECTORIES at the fixture's parent so discovery from a fixture repo can
never adopt a repo above it. A repo above d is only reachable when the .git found under d is
INVALID, so this module places an empty `d/broken/.git` directory beside an honest `d/lane` repo,
plus a VALID repo exactly at d's parent (as hostile f6 does).
Expected: pristine ADMITS (the ceiling stops discovery at d's parent; the tool accepts the honest
lane). PG2 (ceiling dropped) mutant REFUSES: discovery from the broken .git climbs into the
parent repo and repo_breach reports a toplevel outside the fixture — an honest fixture refused."""
import pathlib

CL = ".ufo/waves/round-42/claims/round-42-claims.md"
RC = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    ctx.init(pathlib.Path(d).parent)
    r = ctx.init(d / "lane")
    ctx.write(pathlib.Path(d) / "lane" / CL, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(pathlib.Path(d) / "lane" / RC, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    (pathlib.Path(d) / "broken" / ".git").mkdir(parents=True)
    return ["--lane", "lane", "--claims", CL, "--receipt", RC]


FIXTURES = [{"fid": "hceiling-broken-gitdir", "tool": "order", "expect": "accept", "defects": [], "build": build}]

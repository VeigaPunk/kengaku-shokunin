"""Refusal fixture f20 (round-45 held-out `R45HoConfigKeys/configkeys.py`): `.git/config` sets
`core.attributesFile` to a regular file beside `d`. The landed fence's fact 5 judges include sections,
`extensions.worktreeConfig`, `core.bare` and `core.worktree` only, so the fixture is ADMITTED; git honours the
outside attributes file (`git check-attr` returns the outside marker, `a3w1/R45HoConfigKeys.md`). One class:
config key that redirects a read outside `d`. Base fence: ADMIT, 0 outside opens during the decision itself."""
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    d = pathlib.Path(d)
    outside = d.parent / "outside-attributes"
    ctx.write(outside, "* hostile=outside\n")
    repo = ctx.init(d / "lane")
    ctx.write(repo / CLAIMS, "nothing ran\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-qm", "claims")
    ctx.write(repo / RECEIPT, "receipt\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-qm", "receipt")
    ctx.write(repo / ".git/config", "[core]\n\tattributesFile = " + str(outside) + "\n")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "config-core-attributes-file-outside", "tool": "order", "expect": "accept", "defects": [],
             "build": build}]

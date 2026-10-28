"""Round-48 C1 NEW honest class `n11_multibranch`: three local branches, one of them nested.

New in round 48 (not one of the nine round-46 classes). Three committed branches — `master`, `feature`, and
the slash-named `release/v1` — leave three 40-hex files under `refs/heads` (one two levels deep) and three
matching reflogs. `git branch` and `git checkout` write nothing outside `.git`, so the fixture is honest; the
nested ref name is the shape `git branch release/v1` produces and must not be read as a path escape.

This fixture also carries the `order` argv shape (`--lane V --claims V --receipt V`), so the honest population
exercises both tool argv shapes: the claims file is committed before the receipt and no `claims/` blob carries
a gate `P10` or `CASE ... observed=` line.

Authored against the BASE fence description only (`plans/fixture_fence.py` @ `a543d920`), never against a
repaired fence. Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""

CLAIMS = "plans/round-48-claims.md"
RECEIPT = "corpus/evidence/round48/fixture-order-receipt.txt"
CLEAN = "no gate line and no case line was ever committed here\n"


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / CLAIMS, "# fixture claims\n\nWritten before the receipt.\n")
    ctx.write(r / ".ufo/waves/round-48/claims/control.txt", CLEAN)
    ctx.write(r / "README.md", "# three branches\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "freeze the fixture claims")
    ctx.git(r, "branch", "feature")
    ctx.git(r, "branch", "release/v1")
    ctx.git(r, "checkout", "-q", "feature")
    ctx.write(r / "feature.txt", "feature work\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "feature work")
    ctx.git(r, "checkout", "-q", "master")
    ctx.write(r / RECEIPT, "cases=3 observed_pass=3 observed_fail=0 mismatches=0\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "record the receipt after the freeze")
    return ["--lane", "repo", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "n11-multibranch", "tool": "order", "expect": None, "defects": None, "build": build}]

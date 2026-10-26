"""Pre-freeze direction witnesses (round 40, L1): O04, O12, O13, O14 of plans/order_check.py. Not battery40.

Each builds a two-commit repository: commit 1 freezes the claims file and one file under the round's claims/
directory, commit 2 adds the receipt."""

CLAIMS = "plans/round-50-claims.md"
CLAIMS_DIR = ".ufo/waves/round-50/claims"
RECEIPT = "corpus/evidence/round50/probe.txt"


def repo(ctx, d, control_text, claims=CLAIMS, gitlink=False):
    r = ctx.init(d / "repo")
    (r / "plans").mkdir()
    (r / claims).write_text("# frozen claims\n")
    (r / CLAIMS_DIR).mkdir(parents=True)
    (r / CLAIMS_DIR / "control.txt").write_text(control_text)
    ctx.git(r, "add", "-A")
    if gitlink:
        ctx.git(r, "update-index", "--add", "--cacheinfo",
                f"160000,{'1' * 40},{CLAIMS_DIR}/vendored")
    ctx.git(r, "commit", "-q", "-m", "freeze")
    (r / "corpus/evidence/round50").mkdir(parents=True)
    (r / RECEIPT).write_text("CASE a predicted=pass observed=pass\ncases=1 observed_pass=1\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "receipt")
    return ["--lane", str(r), "--claims", claims, "--receipt", RECEIPT]


FIXTURES = [
    {"fid": "w-o04-p10-ok-excuse", "tool": "order", "expect": "reject",
     "defects": ["hit:gate-p10"],
     "build": lambda ctx, d: repo(ctx, d, "P10 ok receipt unreadable\n")},
    {"fid": "w-o12-gitlink", "tool": "order", "expect": "accept", "defects": [],
     "build": lambda ctx, d: repo(ctx, d, "P10 DEFECT receipt unreadable\n", gitlink=True)},
    {"fid": "w-o13-quoted-case", "tool": "order", "expect": "accept", "defects": [],
     "build": lambda ctx, d: repo(ctx, d, "note: CASE a predicted=pass observed=pass\n")},
    {"fid": "w-o14-claims-name-suffixed", "tool": "order", "expect": "error", "defects": [],
     "build": lambda ctx, d: repo(ctx, d, "P10 DEFECT receipt unreadable\n", claims="plans/round-50-claims.md.bak")},
]

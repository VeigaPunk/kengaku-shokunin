"""R42CritC1Counter attack battery (order side).

Five one-repo fixtures written for this seat. Two are deliberately weak substitutes the counter
cannot tell apart from a demonstration (XO1, XO3): the argv receipt path is a DIRECTORY that the freeze
commit merely contains, so the clause fires with no receipt artefact in the history at all. The
other three are ordinary demonstrations.
"""

CLAIMS = "plans/round-42-claims.md"
CDIR = ".ufo/waves/round-42/claims"
BENIGN = "frozen notes, no gate line in this file\n"


def oc(ctx, r, msg):
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", msg)


def oargs(r, receipt):
    return ["--lane", str(r), "--claims", CLAIMS, "--receipt", receipt]


def f_xo1(ctx, d):
    """SUBSTITUTE: receipt is the claims directory; one commit carries claims and that directory."""
    r = ctx.init(d / "repo")
    ctx.write(r / CLAIMS, "# frozen claims for the fixture\n")
    ctx.write(r / CDIR / "note.txt", BENIGN)
    oc(ctx, r, "freeze")
    return oargs(r, CDIR)


def f_xo3(ctx, d):
    """SUBSTITUTE: receipt path is a directory created and then emptied before the claims commit."""
    r = ctx.init(d / "repo")
    ctx.write(r / "README.md", "fixture\n")
    ctx.write(r / CDIR / "note.txt", BENIGN)
    oc(ctx, r, "directory first")
    ctx.git(r, "rm", "-r", "-q", "--", CDIR)
    oc(ctx, r, "directory dropped")
    ctx.write(r / CLAIMS, "# frozen claims for the fixture\n")
    oc(ctx, r, "freeze")
    ctx.write(r / CDIR / "note.txt", BENIGN)
    oc(ctx, r, "directory present again at the tip")
    return oargs(r, CDIR)


def f_xo5(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / CLAIMS, "# frozen claims for the fixture\n")
    ctx.write(r / CDIR / "before.txt", BENIGN)
    oc(ctx, r, "freeze")
    ctx.write(r / "corpus/evidence/probe.txt", "probe receipt body\n")
    oc(ctx, r, "receipt")
    ctx.write(r / CDIR / "after.txt", "gate: P10 ok fresh probe output byte-equal\n")
    oc(ctx, r, "after the receipt")
    return oargs(r, "corpus/evidence/probe.txt")


def f_xo6(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / CLAIMS, "# frozen claims for the fixture\n")
    ctx.write(r / CDIR / "note.txt", "P10 PASS receipt unreadable\n")
    oc(ctx, r, "freeze")
    ctx.write(r / "corpus/evidence/probe.txt", "probe receipt body\n")
    oc(ctx, r, "receipt")
    return oargs(r, "corpus/evidence/probe.txt")


def f_xo7(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / CLAIMS, "# frozen claims for the fixture\n")
    ctx.write(r / CDIR / "note.txt", "CASE c1 observed=timeout\n")
    oc(ctx, r, "freeze")
    ctx.write(r / "corpus/evidence/probe.txt", "probe receipt body\n")
    oc(ctx, r, "receipt")
    return oargs(r, "corpus/evidence/probe.txt")


FIXTURES = [
    {"fid": "b-xo1-receipt-is-directory", "tool": "order", "expect": "reject", "defects": [],
     "build": f_xo1},
    {"fid": "b-xo3-emptied-directory", "tool": "order", "expect": "reject", "defects": [],
     "build": f_xo3},
    {"fid": "b-xo5-later-claims-blob", "tool": "order", "expect": "accept", "defects": [],
     "build": f_xo5},
    {"fid": "b-xo6-p10-pass", "tool": "order", "expect": "accept", "defects": [], "build": f_xo6},
    {"fid": "b-xo7-observed-timeout", "tool": "order", "expect": "reject", "defects": [],
     "build": f_xo7},
]

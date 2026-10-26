"""Round-42 pre-freeze direction module (L1 KengakuR42) for the five order near-variants of round42_c1_verify.py.

Shapes from the round-40 wave-2 report `.ufo/waves/round-40/falsify/F40XMutLedgerOrder.md` (wit-xo1, wit-xo3b,
wit-xo5, wit-xo6, wit-xo7), rebuilt from nothing under the round-42 battery contract. Committed as freeze
evidence; the battery42 modules may not import, copy or read it.
"""

CLAIMS = "plans/round-42-claims.md"
CDIR = ".ufo/waves/round-42/claims"
RECEIPT = "corpus/evidence/round42/probe.txt"


def c(ctx, r, msg):
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", msg)


def args(r):
    return ["--lane", str(r), "--claims", CLAIMS, "--receipt", RECEIPT]


def xo1(ctx, d):
    # one commit carries the claims file and the receipt
    r = ctx.init(d / "repo")
    ctx.write(r / CLAIMS, "# round 42 frozen claims\n")
    ctx.write(r / CDIR / "control.txt", "P10 DEFECT receipt unreadable\n")
    ctx.write(r / RECEIPT, "probe receipt\n")
    c(ctx, r, "freeze with receipt")
    return args(r)


def xo3(ctx, d):
    # receipt added, removed, claims frozen, receipt re-added: the first commit adding the receipt is an
    # ancestor of the freeze, while the freeze tree itself does not carry the receipt
    r = ctx.init(d / "repo")
    ctx.write(r / "README.md", "fixture\n")
    ctx.write(r / RECEIPT, "early receipt\n")
    c(ctx, r, "receipt first")
    ctx.git(r, "rm", "-q", RECEIPT)
    ctx.git(r, "commit", "-q", "-m", "receipt removed")
    ctx.write(r / CLAIMS, "# round 42 frozen claims\n")
    ctx.write(r / CDIR / "control.txt", "P10 DEFECT receipt unreadable\n")
    c(ctx, r, "freeze")
    ctx.write(r / RECEIPT, "probe receipt\n")
    c(ctx, r, "receipt again")
    return args(r)


def xo5(ctx, d):
    # honest freeze and receipt, then a claims/ blob showing an executed gate committed AFTER the receipt
    r = ctx.init(d / "repo")
    ctx.write(r / CLAIMS, "# round 42 frozen claims\n")
    ctx.write(r / CDIR / "control.txt", "P10 DEFECT receipt unreadable\n")
    c(ctx, r, "freeze")
    ctx.write(r / RECEIPT, "probe receipt\n")
    c(ctx, r, "receipt")
    ctx.write(r / CDIR / "post-receipt.txt", "gate: P10 ok fresh probe output byte-equal\n")
    c(ctx, r, "post-receipt rerun")
    return args(r)


def gate_repo(ctx, d, text):
    r = ctx.init(d / "repo")
    ctx.write(r / CLAIMS, "# round 42 frozen claims\n")
    ctx.write(r / CDIR / "control.txt", text)
    c(ctx, r, "freeze")
    ctx.write(r / RECEIPT, "probe receipt\n")
    c(ctx, r, "receipt")
    return args(r)


FIXTURES = [
    {"fid": "w-xo1-freeze-has-receipt", "tool": "order", "expect": "reject", "defects": [], "build": xo1},
    {"fid": "w-xo3-receipt-first-removed", "tool": "order", "expect": "reject", "defects": [], "build": xo3},
    {"fid": "w-xo5-post-receipt-blob", "tool": "order", "expect": "accept", "defects": [], "build": xo5},
    {"fid": "w-xo6-p10-pass-line", "tool": "order", "expect": "accept", "defects": [],
     "build": lambda ctx, d: gate_repo(ctx, d, "P10 PASS receipt unreadable\n")},
    {"fid": "w-xo7-case-timeout", "tool": "order", "expect": "reject", "defects": [],
     "build": lambda ctx, d: gate_repo(ctx, d, "CASE c1 observed=timeout\n")},
]

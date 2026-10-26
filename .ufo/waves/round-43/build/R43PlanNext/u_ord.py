"""Scratch battery for the R43PlanNext pricing run: argument-error behaviours of the order gate."""

CLAIMS = "plans/round-7-claims.md"
ODD = "plans/odd-claims.md"
RCPT = "corpus/evidence/round7/x-probe.txt"


def repo(ctx, d):
    r = ctx.init(d / "lane")
    ctx.write(r / CLAIMS, "# claims\n")
    ctx.write(r / ODD, "# odd name\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "freeze")
    ctx.write(r / RCPT, "CASE c1 observed=PASS\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "receipt")
    return r


def u14_missing_claims_flag(ctx, d):
    return ["--lane", str(repo(ctx, d)), "--receipt", RCPT]


def u14c_odd_claims_name(ctx, d):
    return ["--lane", str(repo(ctx, d)), "--claims", ODD, "--receipt", RCPT]


FIXTURES = [
    {"fid": "u14-no-claims-flag", "tool": "order", "expect": "error", "defects": [], "build": u14_missing_claims_flag},
    {"fid": "u14c-odd-claims-name", "tool": "order", "expect": "error", "defects": [], "build": u14c_odd_claims_name},
]

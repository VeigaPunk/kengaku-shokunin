"""Scratch battery (R44PlanNext): round_close.py fixtures built from nothing. Not lane material."""

ORDER_STUB = "import sys\nprint('ORDER-STUB receipt seen')\nsys.exit(0)\n"
CENSUS_PASS = "#!/bin/sh\necho 'CENSUS-STUB pass'\nexit 0\n"
CENSUS_FAIL = "#!/bin/sh\necho 'CENSUS-STUB fail'\nexit 2\n"
CLAIMS = "# Round 39 claims\n\n**Probe (frozen):** `plans/git_leak_probe.py`.\n"
CLAIMS_EVID = "# Round 39 claims\n\nEvidence: `corpus/evidence/round39/x-probe.txt`\n"
RECEIPT = "CASE c01 observed=PASS predicted=PASS\n"


def stub(ctx, d, rel, text):
    tmp = d / "stub.tmp"
    ctx.write(tmp, text)
    dst = d / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    ctx.sh("install", "-m", "755", str(tmp), str(dst))
    ctx.sh("rm", "-f", str(tmp))
    return dst


def lane(ctx, d, claims=CLAIMS, receipt="corpus/evidence/round39/git-leak-probe.txt", order=True, census=None):
    r = ctx.init(d / "lane")
    ctx.write(r / "plans/round-39-claims.md", claims)
    if order:
        ctx.write(r / "plans/order_check.py", ORDER_STUB)
    ctx.write(r / "corpus/SOURCES.md", "# sources\n")
    if receipt:
        ctx.write(r / receipt, RECEIPT)
    if census is not None:
        stub(ctx, r, "scripts/sources-census.sh", census)
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "freeze")
    return r


C_IN = "lane/scripts/sources-census.sh"


def b_ok(ctx, d):
    lane(ctx, d, census=CENSUS_PASS)
    return ["--lane", "lane", "--round", "39", "--census", C_IN]


def b_deleted(ctx, d):
    r = lane(ctx, d, census=CENSUS_PASS)
    ctx.sh("rm", str(r / "corpus/evidence/round39/git-leak-probe.txt"))
    return ["--lane", "lane", "--round", "39", "--census", C_IN]


def b_evid(ctx, d):
    lane(ctx, d, claims=CLAIMS_EVID, receipt="corpus/evidence/round39/x-probe.txt", census=CENSUS_PASS)
    return ["--lane", "lane", "--round", "39", "--census", C_IN]


def b_lane_first(ctx, d):
    lane(ctx, d, census=CENSUS_FAIL)
    stub(ctx, d, "scripts/sources-census.sh", CENSUS_PASS)
    return ["--lane", "lane", "--round", "39"]


def b_parent(ctx, d):
    lane(ctx, d)
    stub(ctx, d, "scripts/sources-census.sh", CENSUS_PASS)
    return ["--lane", "lane", "--round", "39"]


def b_noclaims(ctx, d):
    lane(ctx, d, census=CENSUS_PASS)
    return ["--lane", "lane", "--round", "40", "--census", C_IN]


def b_noorder(ctx, d):
    lane(ctx, d, order=False, census=CENSUS_PASS)
    return ["--lane", "lane", "--round", "39", "--census", C_IN]


def b_st_nocensus(ctx, d):
    lane(ctx, d)
    return ["--lane", "lane", "--census", "absent.sh", "--selftest"]


def b_st_noorder(ctx, d):
    lane(ctx, d, order=False, census=CENSUS_PASS)
    return ["--lane", "lane", "--census", C_IN, "--selftest"]


def b_census_absent(ctx, d):
    lane(ctx, d)
    return ["--lane", "lane", "--round", "39", "--census", "absent.sh"]


def b_st_runs(ctx, d):
    lane(ctx, d, census=CENSUS_PASS)
    return ["--lane", "lane", "--census", C_IN, "--selftest", "--work", "{WORK:sw}"]


def flat(ctx, d, claims=CLAIMS, sources=True, census=CENSUS_PASS, claims_name="plans/round-39-claims.md"):
    """A lane-shaped tree directly in d (no repo)."""
    ctx.write(d / claims_name, claims)
    ctx.write(d / "plans/order_check.py", ORDER_STUB)
    if sources:
        ctx.write(d / "corpus/SOURCES.md", "# sources\n")
    ctx.write(d / "corpus/evidence/round39/git-leak-probe.txt", RECEIPT)
    stub(ctx, d, "scripts/sources-census.sh", census)


def b_cwd_lane(ctx, d):
    flat(ctx, d)
    return ["--lane", ".", "--round", "39", "--census", "scripts/sources-census.sh"]


def b_nested(ctx, d):
    r = ctx.init(d / "lane")
    flat(ctx, r / "sub")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "freeze")
    return ["--lane", "lane/sub", "--round", "39", "--census", "lane/sub/scripts/sources-census.sh"]


def b_nosources(ctx, d):
    lane(ctx, d, census=CENSUS_PASS)
    ctx.sh("rm", str(d / "lane/corpus/SOURCES.md"))
    return ["--lane", "lane", "--round", "39", "--census", C_IN]


def b_noneround(ctx, d):
    r = ctx.init(d / "lane")
    ctx.write(r / "plans/round-None-claims.md", "# claims\n\nReceipt: `corpus/evidence/round39/git-leak-probe.txt`\n")
    ctx.write(r / "plans/order_check.py", ORDER_STUB)
    ctx.write(r / "corpus/SOURCES.md", "# sources\n")
    ctx.write(r / "corpus/evidence/round39/git-leak-probe.txt", RECEIPT)
    stub(ctx, r, "scripts/sources-census.sh", CENSUS_PASS)
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "freeze")
    return ["--lane", "lane", "--census", C_IN]


FIXTURES = [
    {"fid": "rc-gate-ok", "tool": "round_close", "expect": "accept", "defects": [], "build": b_ok},
    {"fid": "rc-receipt-deleted", "tool": "round_close", "expect": "accept", "defects": [], "build": b_deleted},
    {"fid": "rc-evidence-path-only", "tool": "round_close", "expect": "accept", "defects": [], "build": b_evid},
    {"fid": "rc-census-lane-first", "tool": "round_close", "expect": "error", "defects": [], "build": b_lane_first},
    {"fid": "rc-census-in-parent", "tool": "round_close", "expect": "accept", "defects": [], "build": b_parent},
    {"fid": "rc-no-claims", "tool": "round_close", "expect": "error", "defects": [], "build": b_noclaims},
    {"fid": "rc-no-order-tool", "tool": "round_close", "expect": "error", "defects": [], "build": b_noorder},
    {"fid": "rc-selftest-no-census", "tool": "round_close", "expect": "error", "defects": [], "build": b_st_nocensus},
    {"fid": "rc-selftest-no-order", "tool": "round_close", "expect": "error", "defects": [], "build": b_st_noorder},
    {"fid": "rc-census-absent", "tool": "round_close", "expect": "error", "defects": [], "build": b_census_absent},
    {"fid": "rc-selftest-runs", "tool": "round_close", "expect": "reject", "defects": [], "build": b_st_runs},
    {"fid": "rc-lane-is-cwd-nonrepo", "tool": "round_close", "expect": "error", "defects": [], "build": b_cwd_lane},
    {"fid": "rc-lane-nested-in-repo", "tool": "round_close", "expect": "error", "defects": [], "build": b_nested},
    {"fid": "rc-no-registry", "tool": "round_close", "expect": "error", "defects": [], "build": b_nosources},
    {"fid": "rc-claims-named-none", "tool": "round_close", "expect": "error", "defects": [], "build": b_noneround},
]

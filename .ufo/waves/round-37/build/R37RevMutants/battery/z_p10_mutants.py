"""R37RevMutants review battery: P10 (--rerun) fixtures for M41-M43.

The stub probe replaces plans/tb2_grader_probe.py (so P1 also defects); P10 runs it through
`uv run --no-project --with biopython==1.85 python3` on this host (Bio absent, uv cached).
"""


def _argv(d):
    return ["package", "--root", str(d), "--require-clean-tree", "--rerun"]


def _m41(ctx, d):
    ctx.genuine_package(d)
    ctx.git_add(d)
    (d / ctx.spec["receipt"]).unlink()
    return _argv(d)


def _m42(ctx, d):
    ctx.genuine_package(d)
    ctx.git_add(d)
    (d / "plans/tb2_grader_probe.py").write_text("import sys\nsys.exit(3)\n")
    return _argv(d)


def _m43(ctx, d):
    ctx.genuine_package(d)
    ctx.git_add(d)
    receipt = (d / ctx.spec["receipt"]).read_text()
    (d / "plans/tb2_grader_probe.py").write_text(
        "import sys\nsys.stdout.write(" + repr(receipt + "X") + ")\n")
    return _argv(d)


FIXTURES = [
    {"fid": "rev-m41-rerun-receipt-gone", "expect": "reject", "defects": ["P2", "P10"], "build": _m41},
    {"fid": "rev-m42-rerun-probe-exit3", "expect": "reject", "defects": ["P1", "P10"], "build": _m42},
    {"fid": "rev-m43-rerun-probe-offby", "expect": "reject", "defects": ["P1", "P10"], "build": _m43},
]

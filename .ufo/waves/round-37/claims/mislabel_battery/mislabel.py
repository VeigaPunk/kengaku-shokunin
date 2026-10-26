"""Skip-control battery: declares the genuine package a reject (a label nobody checked). Must make wrong>0."""


def _genuine(ctx, d):
    ctx.genuine_package(d)
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


FIXTURES = [{"fid": "mislabel-genuine-as-reject", "expect": "reject", "defects": ["P1"], "build": _genuine}]

"""Critic attack (rule check): the counter never enforces the claim's "SINGLE-DEFECT fixtures" rule.

plans/round-37-claims.md (C1) and the counter docstring say the battery is built of single-defect
fixtures.  The counter only compares the declared DEFECT set with the observed one; a fixture carrying two
independent defects is accepted with `ok` as long as it declares both.  This module is one such fixture:
one-word quotes (P3) *and* no README (P8).  A `FIXTURE crit-multi-defect ... ok` line is the evidence.
"""


def _build(ctx, d):
    ctx.genuine_package(d)
    entry = d / ctx.spec["entry"]
    entry.write_text(ctx.r36.mut_one_word(entry.read_text()))
    (d / ctx.spec["readme"]).unlink()
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


FIXTURES = [
    {"fid": "crit-multi-defect", "expect": "reject", "defects": ["P3", "P8"], "build": _build},
]

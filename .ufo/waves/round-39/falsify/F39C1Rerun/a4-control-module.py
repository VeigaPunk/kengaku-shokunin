"""F39C1Rerun control A4 (reconstructed evidence): a battery39 build child rewrites two pinned lane files after
the PINS line.  Placed in <clone>/plans/battery39/f39c1_a4pinwrite.py and removed afterwards; both pinned files
were restored from a pristine copy and re-hashed (`ea638822…`, `7064cf1a…`).

See ../F39C1Rerun.md §6.1 for the observed lines.
"""

import pathlib

MARK = b"\n# f39c1rerun a4 pinwrite witness\n"
TARGETS = ("plans/pkg_gate.py", "plans/round37_c1_attribution.py")


def build(ctx, d):
    ctx.genuine_package(d)
    ctx.git_add(d)
    lane = pathlib.Path(ctx.lane)
    for rel in TARGETS:
        p = lane / rel
        p.write_bytes(p.read_bytes() + MARK)
    return ["package", "--root", str(d), "--require-clean-tree"]


FIXTURES = [{"fid": "f39c1-a4-pinwrite", "expect": "accept", "defects": [], "build": build}]

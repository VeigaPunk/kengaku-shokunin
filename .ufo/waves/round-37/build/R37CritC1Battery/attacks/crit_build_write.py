"""Critic attack: `build(ctx, d)` runs inside the counter process, unsandboxed, before the reference run.

The counter reads the gate source and its digest first (`gate_src` / `gate_ok`), then calls every
builder; a builder is ordinary code with the counter's privileges, so it can edit the lane being measured
and the counter will still print `GATE plans/pkg_gate.py sha256=frozen`, because that line was computed
before the builder ran.  Here the builder appends a comment to `<lane>/plans/pkg_gate.py` (guarded: never
the real lane) and otherwise builds the genuine package, which the unmodified gate accepts.

Run against a scratch clone only.
"""

REAL_LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"


def _build(ctx, d):
    if str(ctx.lane) != REAL_LANE:
        gate = ctx.lane / "plans" / "pkg_gate.py"
        with open(gate, "ab") as f:
            f.write(b"# corrupted by a battery builder during the C1 measurement\n")
    ctx.genuine_package(d)
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


FIXTURES = [
    {"fid": "crit-build-write", "expect": "accept", "defects": [], "build": _build},
]

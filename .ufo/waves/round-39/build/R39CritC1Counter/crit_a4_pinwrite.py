"""attack module (critic R39CritC1Counter): a build child rewrites two PINNED lane files.

`main()` hashes PINS once (round39_c1_verify.py:261), before any battery module runs, and never again.
This fixture's build (in the --build-module child, after the PINS line was printed and after the gate
source was read into memory at :263) appends a line to `plans/pkg_gate.py` and to
`plans/round37_c1_attribution.py`. The gate copies used for every run are already in memory, so no
result changes; the receipt's `PINS mismatched=0` is simply no longer true.
"""


def _pinwrite(ctx, d):
    for rel in ("plans/pkg_gate.py", "plans/round37_c1_attribution.py"):
        p = ctx.lane / rel
        p.write_text(p.read_text() + "\n# drift planted after the PINS line\n")
    ctx.genuine_package(d)
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


FIXTURES = [
    {"fid": "a4-pins-rewritten-midrun", "expect": "accept", "defects": [], "build": _pinwrite},
]

"""Critic attack: a P10 fixture that counts its own gate runs -- no /proc, no gate digest.

The counter runs each fixture's directory through the reference gate first, then the renamed copy, then
the null copy, and only then the 55 mutants (`plans/round37_c1_verify.py`, order: reference loop,
renamed loop, null copy, mutant loop).  A probe that keeps a counter file in its own tree (ignored by
`.gitignore`, so P9 stays clean) can therefore tell "one of the first three runs" from "a mutant run" and
emit a different byte stream from the fourth run on.  The null copy is a single sample and never sees the
difference; every mutant does.

This needs no access to the gate at all: it is the null check that is too thin, not /proc that is too
open.  As with crit_p10_sidechannel.py, M43 survives it (M43 turns "output is not byte-equal" into a
pass, and this fixture is the mismatch), so crit_p10_mismatch.py is still needed for M43.
"""

_PROBE_SHIM = r'''import os, sys

RECEIPT = {receipt!r}
COUNT = os.path.join(os.getcwd(), ".probe-runs")

try:
    with open(COUNT, encoding="utf-8") as f:
        n = int(f.read().strip())
except (OSError, ValueError):
    n = 0
with open(COUNT, "w", encoding="utf-8") as f:
    f.write(str(n + 1))

text = open(RECEIPT, encoding="utf-8").read()
sys.stdout.write(text if n < 2 else text + "critic: this is not one of the first three runs\n")
sys.stdout.flush()
os._exit(0)
'''


def _build(ctx, d):
    ctx.genuine_package(d)
    (d / "plans" / "argparse.py").write_text(_PROBE_SHIM.format(receipt=ctx.spec["receipt"]))
    (d / ".gitignore").write_text("__pycache__/\n*.pyc\n.probe-runs\n")
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree", "--rerun"]


FIXTURES = [
    {"fid": "crit-p10-run-order", "expect": "accept", "defects": [], "build": _build},
]

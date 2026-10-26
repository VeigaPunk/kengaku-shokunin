"""Critic battery module (round 37, seat R37CritC1Battery), second half of the P10 attack.

One mutant is immune to the side-channel in crit_p10_sidechannel.py: M43 silences
`return False, "fresh probe output is not byte-equal to the receipt"`, i.e. it makes P10 *pass* exactly
when the probe's stdout differs from the receipt.  The accept fixture triggers the mismatch only under a
mutant, so M43 cancels it and survives.

This fixture is the converse and is honest: it makes a fresh run of the probe disagree with the pinned
receipt under the *unmodified* gate as well, so the reference is `reject` with the single clause P10 --
the class M43 advertises.  The probe is again an unpinned `plans/argparse.py` shim (the pinned
`plans/tb2_grader_probe.py` bytes are untouched, so P1 stays green), so the declaration is single-defect.

Together with the accept fixture this reaches `killed=55` while 54 of the 55 kills come from a fixture
that exercises no advertised branch at all.
"""

_PROBE_SHIM = r'''import os, sys

RECEIPT = {receipt!r}

text = open(RECEIPT, encoding="utf-8").read()
sys.stdout.write(text + "critic: probe output deliberately differs from the receipt\n")
sys.stdout.flush()
os._exit(0)
'''


def _build(ctx, d):
    ctx.genuine_package(d)
    (d / "plans" / "argparse.py").write_text(_PROBE_SHIM.format(receipt=ctx.spec["receipt"]))
    (d / ".gitignore").write_text("__pycache__/\n*.pyc\n")
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree", "--rerun"]


FIXTURES = [
    {"fid": "crit-p10-mismatch", "expect": "reject", "defects": ["P10"], "build": _build},
]

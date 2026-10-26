"""Critic attack (negative control): a fixture that keys on its own directory name.

The counter's renamed run copies every built fixture to `<work>/renamed/xNNNNNq` and requires the
reference result to be unchanged.  This fixture is name-sensitive by construction -- the shim writes the
pinned receipt only while the fixture's basename starts with `f` -- so the counter must report
`RENAMED crit-p10-namekey DISAGREES` and `renamed_disagree=1`.  It is here to show what the renamed check
does catch: a fixture whose behaviour depends on its own path.

It does not catch the attack that matters, because crit_p10_sidechannel.py keys on the *gate's bytes*:
the renamed copy of that fixture carries the same shim and behaves identically.
"""

_PROBE_SHIM = r'''import os, sys

RECEIPT = {receipt!r}

text = open(RECEIPT, encoding="utf-8").read()
if os.path.basename(os.getcwd()).startswith("f"):
    sys.stdout.write(text)
else:
    sys.stdout.write(text + "critic: renamed run seen\\n")
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
    {"fid": "crit-p10-namekey", "expect": "accept", "defects": [], "build": _build},
]

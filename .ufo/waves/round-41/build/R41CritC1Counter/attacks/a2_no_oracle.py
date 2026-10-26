"""Counterfactual control for a1: the same two lanes, with a stub that does NOT look at the bound variant.

If a1's kills are attributable to the mutants' own bytes, these fixtures kill them too. If they are
attributable to the stub's read of the variant slot, these survive and a1's kills are fabrications.
"""

BLOB = "RECEIPT-BODY r41\n"
EV = "corpus/evidence/r/foo-probe.txt"

STUB = '''"""Stub probe.

  python3 plans/foo_probe.py --lane .
"""
import sys

sys.stdout.write(__OUT__)
sys.exit(0)
'''


def stub(out):
    return STUB.replace("__OUT__", repr(out))


def lane(ctx, d, text):
    root = ctx.init(d / "lane")
    ctx.write(root / EV, BLOB)
    ctx.write(root / "plans/foo_probe.py", text)
    ctx.git(root, "add", "-A")
    ctx.git(root, "commit", "-q", "-m", "fixture")
    return root


def argv(root):
    return ["--lane", str(root), "--work", "{WORK}"]


def b_bytes(ctx, d):
    return argv(lane(ctx, d, stub(BLOB)))


def b_exit(ctx, d):
    return argv(lane(ctx, d, stub("AMENDED\n")))


FIXTURES = [
    {"fid": "plain-bytes", "tool": "receipts", "expect": "accept",
     "defects": [f"equal:{EV}", "control:differ"], "build": b_bytes},
    {"fid": "plain-exit", "tool": "receipts", "expect": "reject",
     "defects": [f"differ:{EV}"], "build": b_exit},
]

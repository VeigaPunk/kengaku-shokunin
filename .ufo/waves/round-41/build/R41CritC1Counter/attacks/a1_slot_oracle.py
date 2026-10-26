"""Attack module (critic R41CritC1Counter): the probe stub reads the variant the counter bound for this run.

The stub locates the counter's scratch root by walking up from its own working directory until it finds the
`slots/` and `variants/` directories, reads `slots/receipts.py` (the variant bound for THIS run) and
`variants/ref-receipts.py` (the unmutated copy), and branches on whether the two differ. No token of the
counter's side-channel list is used anywhere: the module source is clean by construction, so `sidechannel=0`
is literally true and still carries no information.
"""

BLOB = "RECEIPT-BODY r41\n"
EV = "corpus/evidence/r/foo-probe.txt"

STUB = '''"""Stub probe.

  python3 plans/foo_probe.py --lane .
"""
import pathlib
import sys

BLOB = __BLOB__
WRONG = "AMENDED\\n"

here = pathlib.Path.cwd()
top = None
while True:
    if (here / "slots").is_dir() and (here / "variants").is_dir():
        top = here
        break
    if here == here.parent:
        break
    here = here.parent

altered = False
if top is not None:
    slot = (top / "slots" / "receipts.py").read_bytes()
    base = (top / "variants" / "ref-receipts.py").read_bytes()
    altered = slot != base

sys.stdout.write(__PICK__)
sys.exit(0)
'''


def stub(pick):
    return STUB.replace("__BLOB__", repr(BLOB)).replace("__PICK__", pick)


def lane(ctx, d, text):
    root = ctx.init(d / "lane")
    ctx.write(root / EV, BLOB)
    ctx.write(root / "plans/foo_probe.py", text)
    ctx.git(root, "add", "-A")
    ctx.git(root, "commit", "-q", "-m", "fixture")
    return root


def argv(root):
    return ["--lane", str(root), "--work", "{WORK}"]


# Reference prints the receipt exactly (equal + a good control, exit 0); a mutated variant gets WRONG bytes.
def b_bytes(ctx, d):
    return argv(lane(ctx, d, stub("WRONG if altered else BLOB")))


# Reference differs (exit 1); a mutated variant gets the exact bytes (equal + control, exit 0).
def b_exit(ctx, d):
    return argv(lane(ctx, d, stub("BLOB if altered else WRONG")))


FIXTURES = [
    {"fid": "crit-oracle-bytes", "tool": "receipts", "expect": "accept",
     "defects": [f"equal:{EV}", "control:differ"], "build": b_bytes},
    {"fid": "crit-oracle-exit", "tool": "receipts", "expect": "reject",
     "defects": [f"differ:{EV}"], "build": b_exit},
]

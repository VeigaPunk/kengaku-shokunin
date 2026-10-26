"""Can a tool run write into the fixture tree, including the name the fingerprint skips?

The stub finds the counter's scratch root (the directory holding `slots/` and `variants/`), walks to the one
fixture dir `root/fx/<module>/f000`, and tries both an exempt name (`state.lock`, skipped by `fingerprint`)
and a hashed one (`state.log`). It reports through the tool's verdict: any successful write makes the probe
print the committed bytes (equal, exit 0); both denied makes it print other bytes (differ, exit 1).
"""

BLOB = "RECEIPT-BODY r41\n"
EV = "corpus/evidence/r/foo-probe.txt"

STUB = '''"""Stub probe.

  python3 plans/foo_probe.py --lane .
"""
import pathlib
import sys

here = pathlib.Path.cwd()
top = None
while True:
    if (here / "slots").is_dir() and (here / "variants").is_dir():
        top = here
        break
    if here == here.parent:
        break
    here = here.parent

wrote = False
if top is not None:
    fx = sorted((top / "fx").iterdir())[0] / "f000"
    for name in ("state.lock", "state.log"):
        try:
            with open(fx / name, "w") as fh:
                fh.write("x")
            wrote = True
        except OSError:
            pass

sys.stdout.write(__BLOB__ if wrote else "AMENDED\\n")
sys.exit(0)
'''


def build(ctx, d):
    root = ctx.init(d / "lane")
    ctx.write(root / EV, BLOB)
    ctx.write(root / "plans/foo_probe.py", STUB.replace("__BLOB__", repr(BLOB)))
    ctx.git(root, "add", "-A")
    ctx.git(root, "commit", "-q", "-m", "fixture")
    return ["--lane", str(root), "--work", "{WORK}"]


FIXTURES = [{"fid": "crit-write-d", "tool": "receipts", "expect": "reject",
             "defects": [f"differ:{EV}"], "build": build}]

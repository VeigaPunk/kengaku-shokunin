"""Is the tool run's PATH the counter's fixed constant, and is `uv` absent?

The probe stub answers `equal` only when the PATH it inherited is exactly the fixed system PATH and `uv` is not
resolvable, so an `ok` fixture is direct evidence that no shared PATH directory can shadow `git`/`python3`.
"""

BLOB = "RECEIPT-BODY r41\n"
EV = "corpus/evidence/r/foo-probe.txt"
FIXED = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

STUB = '''"""Stub probe.

  python3 plans/foo_probe.py --lane .
"""
import os
import shutil
import sys

ok = os.getenv("PATH") == __FIXED__ and shutil.which("uv") is None
sys.stdout.write(__BLOB__ if ok else "AMENDED\\n")
sys.exit(0)
'''


def build(ctx, d):
    root = ctx.init(d / "lane")
    ctx.write(root / EV, BLOB)
    ctx.write(root / "plans/foo_probe.py",
              STUB.replace("__FIXED__", repr(FIXED)).replace("__BLOB__", repr(BLOB)))
    ctx.git(root, "add", "-A")
    ctx.git(root, "commit", "-q", "-m", "fixture")
    return ["--lane", str(root), "--work", "{WORK}"]


FIXTURES = [{"fid": "crit-env-path", "tool": "receipts", "expect": "accept",
             "defects": [f"equal:{EV}", "control:differ"], "build": build}]

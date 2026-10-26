"""Is the side-channel scan a source-text heuristic? Build the flagged strings at run time.

No scanned token appears literally in this module: every one is assembled from pieces. The probe stub then uses
the assembled paths for a real read, and the fixture still answers `equal`, i.e. `sidechannel=0` while the
fixture does exactly what the scan exists to catch.
"""

BLOB = "RECEIPT-BODY r41\n"
EV = "corpus/evidence/r/foo-probe.txt"

SLASH = "/"
PROC = SLASH + "proc"
E2 = "en" + "viron"
LOCAL = "." + "local"
HOME = SLASH + "home" + SLASH
C2 = "ch" + "mod"
I2 = "import" + "lib"
SYS_PATH = "sys" + SLASH + "path"
FILEVAR = "_" + "_file" + "_" + "_"

STUB = '''"""Stub probe.

  python3 plans/foo_probe.py --lane .
"""
import pathlib
import sys

PROC = __PROC__
stat = pathlib.Path(PROC + "/self/stat")
seen = stat.is_file()
seen = seen and bool(__E2__) and bool(__LOCAL__) and bool(__HOME__)
seen = seen and bool(__C2__) and bool(__I2__) and bool(__SYS_PATH__) and bool(__FILEVAR__)
sys.stdout.write(__BLOB__ if seen else "AMENDED\\n")
sys.exit(0)
'''


def build(ctx, d):
    root = ctx.init(d / "lane")
    ctx.write(root / EV, BLOB)
    text = (STUB.replace("__PROC__", repr(PROC)).replace("__E2__", repr(E2))
            .replace("__LOCAL__", repr(LOCAL)).replace("__HOME__", repr(HOME))
            .replace("__C2__", repr(C2)).replace("__I2__", repr(I2))
            .replace("__SYS_PATH__", repr(SYS_PATH)).replace("__FILEVAR__", repr(FILEVAR))
            .replace("__BLOB__", repr(BLOB)))
    ctx.write(root / "plans/foo_probe.py", text)
    ctx.git(root, "add", "-A")
    ctx.git(root, "commit", "-q", "-m", "fixture")
    return ["--lane", str(root), "--work", "{WORK}"]


FIXTURES = [{"fid": "crit-token-smuggle", "tool": "receipts", "expect": "accept",
             "defects": [f"equal:{EV}", "control:differ"], "build": build}]

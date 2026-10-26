"""Freeze control (L1 KengakuR41): a module that tries the round-40 host-write vectors. Never a battery module.
Targets are marker files under the user's home, NOT a PATH directory, so a sandbox failure is harmless."""
import pathlib

LANE_TOOL = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/tip_receipts.py"
BUILD_MARK = "/home/vgpnk/k41-hostile-build-marker"
RUN_MARK = "/home/vgpnk/k41-hostile-run-marker"
STUB = '''"""Stub probe.

  python3 plans/foo_probe.py --lane .
"""
import sys
try:
    open("%s", "w").write("x")
    r = "write=allowed"
except OSError:
    r = "write=denied"
sys.stdout.write(r + "\\n")
''' % RUN_MARK


def outcome(fn):
    try:
        fn()
        return "allowed"
    except OSError as e:
        return type(e).__name__


def build(ctx, d):
    w = outcome(lambda: pathlib.Path(BUILD_MARK).write_text("x"))
    r = outcome(lambda: pathlib.Path(LANE_TOOL).read_bytes())
    root = ctx.init(d / "lane")
    ctx.write(root / "corpus/evidence/r/foo-probe.txt", "write=denied\n")
    ctx.write(root / "plans/foo_probe.py", STUB)
    ctx.git(root, "add", "-A")
    ctx.git(root, "commit", "-q", "-m", "fixture")
    FIXTURES[0]["fid"] = f"h-host-writes.build_write={w}.lane_read={r}"  # reported on the FIXTURE line
    return ["--lane", str(root), "--work", "{WORK}"]


FIXTURES = [{"fid": "h-host-writes", "tool": "receipts", "expect": "accept",
             "defects": ["equal:corpus/evidence/r/foo-probe.txt", "control:differ"], "build": build}]

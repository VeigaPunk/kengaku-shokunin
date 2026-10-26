"""Containment probe: what can a build child write, and can it read the hidden lane?

The build child runs inside the counter's ro_sandbox with only its fixture dir and tmp writable. This module
measures four things and aborts the module with the readings in the traceback, which the counter prints as
`SETUP module ... failed to build (rc=...): <stderr tail>`.
"""

import os


def build(ctx, d):
    report = []
    # 1. a PATH directory: writable? (no write attempted, per host guard)
    for p in ("/home/vgpnk/.local/bin", "/usr/local/bin", "/usr/bin"):
        try:
            report.append(f"writable:{p}={os.access(p, os.W_OK)}")
        except OSError as e:
            report.append(f"writable:{p}=ERR {e.__class__.__name__}")
    # 2. a write outside the fixture dir and outside tmp (scratch, root, sibling fixture tree)
    scratch = "/fast/scratch/hyaku/kengaku-r41/R41CritC1Counter/gate-escape.txt"
    for tag, outside in (("dest", str(d.parent / "escape.txt")), ("scratch", scratch),
                         ("root", str(d.parent.parent / "escape-root.txt"))):
        try:
            with open(outside, "w") as fh:
                fh.write("x")
            report.append(f"write:{tag}=ALLOWED")
            os.unlink(outside)
        except OSError as e:
            report.append(f"write:{tag}=DENIED {e.__class__.__name__}")
    outside = ""
    # 3. the lane the counter passed with --lane is hidden by a tmpfs overlay
    lane_tool = "/fast/scratch/hyaku/kengaku-r41/R41CritC1Counter/lane/plans/tip_receipts.py"
    try:
        size = len(open(lane_tool, "rb").read())
        report.append(f"read:lane-tool=ALLOWED bytes={size}")
    except OSError as e:
        report.append(f"read:lane-tool=DENIED {e.__class__.__name__}")
    # 4. the host copy of the same file (outside the --lane path) is on the read-only root
    try:
        size = len(open("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/tip_receipts.py", "rb").read())
        report.append(f"read:host-tool=ALLOWED bytes={size}")
    except OSError as e:
        report.append(f"read:host-tool=DENIED {e.__class__.__name__}")
    raise RuntimeError("build probe " + " | ".join(report))


FIXTURES = [{"fid": "crit-build-probe", "tool": "receipts", "expect": "error", "defects": [], "build": build}]

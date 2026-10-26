"""Hostile battery module (repair c): the tool run reads the host's `/run`.

The DEPLOYED counter sandbox is `--ro-bind / /` with no `/run` overlay, so a probe run by
`plans/tip_receipts.py` sees the host's runtime tree — systemd state, the session/system bus sockets that
AF_UNIX reaches without any network namespace, machine-id-adjacent state. The repaired counter mounts a
private `--tmpfs /run`, so the run sees an empty directory.

The receipt holds the "visible" output, so the fixture is green on the deployed counter and WRONG on the
repaired one. Nothing is written; the probe only lists the directory.
"""

EV = "corpus/evidence/r/run-probe.txt"

PROBE = '''"""Fixture probe: does this run see the host's /run?

  python3 plans/run_probe.py --lane .
"""
import os
import sys

try:
    seen = sorted(os.listdir("/run"))
except OSError:
    seen = []
sys.stdout.write("RUN " + ("visible" if seen else "empty") + "\\n")
'''


def lane(ctx, d, files):
    root = ctx.init(d / "lane")
    base = {
        "README.md": "# hostile fixture lane\n",
        "SKILL.md": "# fixture skill\n",
        "corpus/README.md": "# fixture lane receipts\n",
        "corpus/knowledge/fixture.md": "# fixture knowledge note\n",
    }
    base.update(files)
    for rel in sorted(base):
        ctx.write(root / rel, base[rel])
    ctx.git(root, "add", "-A")
    ctx.git(root, "commit", "-q", "-m", "fixture lane")
    return root


def b_run_visible(ctx, d):
    root = lane(ctx, d, {EV: "RUN visible\n", "plans/run_probe.py": PROBE})
    return ["--lane", str(root), "--work", "{WORK}"]


FIXTURES = [
    {"fid": "h_run-host-run-visible", "tool": "receipts", "expect": "accept",
     "defects": [f"equal:{EV}", "control:differ"], "build": b_run_visible},
]

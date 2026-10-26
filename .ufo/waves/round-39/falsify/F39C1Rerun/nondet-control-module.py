"""F39C1Rerun control N (reconstructed evidence): a battery39 module that flips its own fixture's --spec once
the mutant phase opens.  Placed in <clone>/plans/battery39/aa_flipwitness.py and removed afterwards; the clone
was restored to the landing tip before the final clean run.

See ../F39C1Rerun.md §6.2 for the observed lines (`AUDIT nondeterministic_kills=1 first=M02:f39c1-flip-spec-
after-ref`, `AUDIT C1 dirty`, and the frozen counter's `MUTANT M02 ... killed by=f39c1-flip-spec-after-ref`,
`PREDICATE C1 pass`).
"""

import json
import pathlib
import subprocess
import sys

MARK = b"\n# f39c1rerun nondet witness byte\n"
MARKER = pathlib.Path("/fast/scratch/hyaku/kengaku-r39/F39C1Rerun/nondet-flip-marker.txt")

DAEMON = """
import datetime, json, pathlib, time
root = pathlib.Path({root!r})
spec = pathlib.Path({spec!r})
marker = pathlib.Path({marker!r})
for _ in range(3000):
    if (root / "gates" / "M01.py").exists():
        break
    time.sleep(0.02)
s = json.loads(spec.read_text())
first = list(s["frozen_instruments"])[:1]
s["frozen_instruments"] = {{k: s["frozen_instruments"][k] for k in first}}
spec.write_text(json.dumps(s))
marker.write_text(datetime.datetime.now().isoformat() + " flipped pins=" + str(first) + "\\n")
"""


def build(ctx, d):
    ctx.genuine_package(d)
    rels = list(ctx.spec["frozen_instruments"])
    if len(rels) < 2:
        raise RuntimeError(f"spec carries {len(rels)} pins, need a second one")
    f = d / pathlib.PurePosixPath(rels[1])
    f.write_bytes(f.read_bytes() + MARK)
    spec_copy = d / "ci-spec.json"
    spec_copy.write_text((pathlib.Path(ctx.lane) / "plans/pkg-spec-r35.json").read_text())
    ctx.git_add(d)
    root = d.parents[2]  # <work>/k39-*/fx/battery39-<stem>/f000 -> root
    subprocess.Popen([sys.executable, "-c",
                      DAEMON.format(root=str(root), spec=str(spec_copy), marker=str(MARKER))],
                     start_new_session=True,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return ["package", "--root", str(d), "--spec", str(spec_copy), "--require-clean-tree"]


FIXTURES = [{"fid": "f39c1-flip-spec-after-ref", "expect": "reject", "defects": ["P1"], "build": build}]

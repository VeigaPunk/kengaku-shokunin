"""Hostile battery module (repair e): one fixture file defeats the whole measurement.

The deployed counter's fingerprint reads every fixture file with a single `fh.read()` (and `sha256()` with
`read_bytes()`), so a build that leaves one large file in its fixture directory makes the whole counter
allocate that file: under a modest address-space cap it dies with a MemoryError and no verdict is produced at
all, and on an uncapped host the cost is the file size per fingerprint pass. The repaired counter streams the
digest in 1 MiB chunks, so memory stays bounded and the run completes.

The file is sparse (no disk cost); the fixture itself is an ordinary `--list` tree.
"""

EV = "corpus/evidence/r/big-probe.txt"
BIG = "big-fixture.bin"
SIZE = 5 << 29  # 5 GiB of sparse zeros

STUB = '''"""Fixture probe: prints its recorded text.

  python3 plans/big_probe.py --lane .
"""
import sys

sys.stdout.write("BIG\\n")
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


def b_big(ctx, d):
    import os
    path = d / BIG
    with open(path, "wb") as fh:
        fh.truncate(SIZE)
    root = lane(ctx, d, {EV: "BIG\n", "plans/big_probe.py": STUB})
    return ["--lane", str(root), "--list"]


FIXTURES = [
    {"fid": "h_big-sparse-fixture-file", "tool": "receipts", "expect": "accept",
     "defects": [f"map:{EV}:derived"], "build": b_big},
]

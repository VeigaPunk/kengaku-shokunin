"""Attack probe: a symlink under d resolving OUTSIDE d (to the module's sibling fixture dir).
Leg h must refuse this at build time.
"""
import hashlib
import os


def sha(b):
    return hashlib.sha256(b).hexdigest()


ROW = ("| S999 | corpus/evidence/round43/cap.bin | capture | A | fixture | {d} "
       "| probe | mined | 2026-10-26 | 180d | - |\n")


def build_out(ctx, d):
    repo = d / "repo"
    ctx.init(repo)
    ctx.write(repo / "corpus/evidence/round43/cap.bin", b"CAPBYTES")
    ctx.write(repo / "corpus/real-sources.md", ROW.format(d=sha(b"CAPBYTES")))
    os.symlink(str(d.parent), repo / "corpus/SOURCES.md")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "sources")
    return ["--lane", str(repo)]


FIXTURES = [
    {"fid": "a-out-symlink", "tool": "anchor", "expect": "accept", "defects": [],
     "build": build_out},
]

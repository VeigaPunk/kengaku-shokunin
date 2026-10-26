"""Attack probe: a symlink INSIDE the fixture dir resolving to a file also inside d (leg h only
refuses symlinks that resolve outside d). Uses a green anchor lane whose SOURCES.md is the symlink.
"""
import hashlib
import os


def sha(b):
    return hashlib.sha256(b).hexdigest()


ROW = ("| S999 | corpus/evidence/round43/cap.bin | capture | A | fixture | {d} "
       "| probe | mined | 2026-10-26 | 180d | - |\n")


def build_in(ctx, d):
    repo = d / "repo"
    ctx.init(repo)
    ctx.write(repo / "corpus/evidence/round43/cap.bin", b"CAPBYTES")
    ctx.write(repo / "corpus/real-sources.md", ROW.format(d=sha(b"CAPBYTES")))
    os.symlink("real-sources.md", repo / "corpus/SOURCES.md")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "sources")
    return ["--lane", str(repo)]


FIXTURES = [
    {"fid": "a-in-symlink", "tool": "anchor", "expect": "accept", "defects": [],
     "build": build_in},
]

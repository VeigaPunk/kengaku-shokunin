"""Cross-fixture sharing WITHOUT a symlink: a hard link from fixture 1's tree to fixture 0's file
(same inode). Leg h only checks symlinks; the fingerprint reads both paths independently. Probe:
fixture 0 builds a green anchor lane; fixture 1 hard-links the evidence blob from fixture 0's repo
into its own repo and is likewise green. Nothing measurable is gained versus copying, but the counter
accepts it — documenting the boundary of leg h.
"""
import hashlib
import os


def sha(b):
    return hashlib.sha256(b).hexdigest()


ROW = ("| S999 | corpus/evidence/round43/cap.bin | capture | A | fixture | {d} "
       "| probe | mined | 2026-10-26 | 180d | - |\n")


def build_zero(ctx, d):
    repo = d / "repo"
    ctx.init(repo)
    ctx.write(repo / "corpus/evidence/round43/cap.bin", b"CAPBYTES")
    ctx.write(repo / "corpus/SOURCES.md", ROW.format(d=sha(b"CAPBYTES")))
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "sources")
    return ["--lane", str(repo)]


def build_one(ctx, d):
    zero = d.parent / "f000/repo/corpus/evidence/round43/cap.bin"
    repo = d / "repo"
    ctx.init(repo)
    ctx.write(repo / "corpus/SOURCES.md", ROW.format(d=sha(b"CAPBYTES")))
    ev = repo / "corpus/evidence/round43"
    ev.mkdir(parents=True, exist_ok=True)
    os.link(zero, ev / "cap.bin")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "sources")
    return ["--lane", str(repo)]


FIXTURES = [
    {"fid": "a-hardlink-host", "tool": "anchor", "expect": "accept", "defects": [],
     "build": build_zero},
    {"fid": "a-hardlink-shared", "tool": "anchor", "expect": "accept", "defects": [],
     "build": build_one},
]

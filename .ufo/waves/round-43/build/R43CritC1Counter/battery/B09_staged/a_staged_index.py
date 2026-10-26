"""Staged-manifest substitute (round-42 X13 shape) ported to the round-43 anchor: evidence committed,
SHA256SUMS staged-only and asserting a digest that equals the row's anchor token, run under
--evidence-ref index. Documented how HEAD mode would differ; none of the nine frozen mutants is
index-mode-dependent, so this shape cannot kill any of them.
"""
import hashlib


def sha(b):
    return hashlib.sha256(b).hexdigest()


ROW = ("| S999 | corpus/evidence/round43/cap.bin | capture | A | fixture | {d} "
       "| probe | mined | 2026-10-26 | 180d | - |\n")


def build_staged(ctx, d):
    repo = d / "repo"
    ctx.init(repo)
    ctx.write(repo / "corpus/evidence/round43/cap.bin", b"CAPBYTES")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "ev")
    fake = sha(b"STAGED-BYTES")
    ctx.write(repo / "corpus/evidence/round43/SHA256SUMS", f"{fake} *cap.bin\n")
    ctx.write(repo / "corpus/SOURCES.md", ROW.format(d=fake))
    ctx.git(repo, "add", "-A")  # staged, not committed
    return ["--lane", str(repo), "--evidence-ref", "index"]


FIXTURES = [
    {"fid": "a-staged-manifest", "tool": "anchor", "expect": "accept", "defects": [],
     "build": build_staged},
]

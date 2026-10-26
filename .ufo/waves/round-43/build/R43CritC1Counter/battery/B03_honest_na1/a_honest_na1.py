"""Positive control: an honest NA1 (row-malformed, silence) kill — a 12-cell row. Shows the dev-mode
harness reproduces attributed kills, so the attack probes below run against a working counter.
"""
import hashlib


def sha(b):
    return hashlib.sha256(b).hexdigest()


MALFORMED = ("| S999 | corpus/evidence/round43/cap.bin | capture | A | fixture | {d} "
             "| probe | mined | 2026-10-26 | 180d | - | extra |\n")


def build_na1(ctx, d):
    repo = d / "repo"
    ctx.init(repo)
    ctx.write(repo / "corpus/evidence/round43/cap.bin", b"CAPBYTES")
    ctx.write(repo / "corpus/SOURCES.md", MALFORMED.format(d=sha(b"CAPBYTES")))
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "sources")
    return ["--lane", str(repo)]


FIXTURES = [
    {"fid": "a-na1-long-row", "tool": "anchor", "expect": "reject",
     "defects": ["row-malformed"], "build": build_na1},
]

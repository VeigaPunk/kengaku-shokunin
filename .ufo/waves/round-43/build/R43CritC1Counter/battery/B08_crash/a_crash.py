"""Crash-direction probe (anchor): a repo with no corpus/SOURCES.md makes the anchor tool exit 2
(Usage). Declared expect=error. No frozen mutant's direction can be exhibited through this shape
because every direction requires mutant rc in {0,1}.
"""


def build_crash(ctx, d):
    repo = d / "repo"
    ctx.init(repo)
    ctx.write(repo / "corpus/evidence/round43/cap.bin", b"CAPBYTES")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "ev")
    return ["--lane", str(repo)]


FIXTURES = [
    {"fid": "a-crash", "tool": "anchor", "expect": "error", "defects": [],
     "build": build_crash},
]

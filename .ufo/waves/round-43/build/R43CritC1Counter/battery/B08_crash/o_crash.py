"""Crash-direction probe (order): a repo where the receipt is never committed makes order_check exit 2
(setup). Declared expect=error; no frozen order mutant exhibits through this shape.
"""


def build_crash(ctx, d):
    repo = d / "repo"
    ctx.init(repo)
    ctx.write(repo / "plans/round-43-claims.md", "# claims\nclean\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "freeze")
    return ["--lane", str(repo), "--claims", "plans/round-43-claims.md",
            "--receipt", "corpus/evidence/r43/probe.txt"]


FIXTURES = [
    {"fid": "o-crash", "tool": "order", "expect": "error", "defects": [],
     "build": build_crash},
]

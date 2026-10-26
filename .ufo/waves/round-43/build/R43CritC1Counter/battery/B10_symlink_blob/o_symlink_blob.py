"""Symlink-blob shaping: a symlink committed under .ufo/waves/round-NN/claims/ is a blob whose content
is its target string — which can carry a gate P10 sentence (the file name is the sentence). Leg i
passes (it IS a blob at HEAD); scan_claims reads the blob content and trips the token heuristic.
Fixture 1 (late claims-dir commit) kills NO5 (rc-silence); fixture 2 (excuse-with-path) kills NO7
(rc-mirror).
"""
import os

CLAIMS = ".ufo/waves/round-43/claims/round-43-claims.md"
RECEIPT = "corpus/evidence/r43/probe.txt"


def build_no5(ctx, d):
    repo = d / "repo"
    ctx.init(repo)
    ctx.write(repo / CLAIMS, "# claims\nclean\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "freeze")
    cd = repo / ".ufo/waves/round-43/claims"
    os.symlink("gate: P10 ok fresh probe output byte-equal", cd / "late.md")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "late")
    ctx.write(repo / RECEIPT, "receipt\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "receipt")
    return ["--lane", str(repo), "--claims", CLAIMS, "--receipt", RECEIPT]


def build_no7(ctx, d):
    repo = d / "repo"
    ctx.init(repo)
    ctx.write(repo / CLAIMS, "# claims\nclean\n")
    cd = repo / ".ufo/waves/round-43/claims"
    os.symlink("gate: P10 DEFECT receipt unreadable: x", cd / "excuse.md")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "freeze")
    ctx.write(repo / RECEIPT, "receipt\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "receipt")
    return ["--lane", str(repo), "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [
    {"fid": "o-symlink-blob-late", "tool": "order", "expect": "reject", "defects": [],
     "build": build_no5},
    {"fid": "o-symlink-blob-excuse", "tool": "order", "expect": "accept", "defects": [],
     "build": build_no7},
]

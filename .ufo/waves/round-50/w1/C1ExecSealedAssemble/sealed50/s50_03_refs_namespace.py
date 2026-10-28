"""Sealed50 hostile: a ref directory git never writes (`refs/weird/thing`) holding a valid 40-hex ref.

Witnesses the ref-namespace leg (`_refs`): a fence that accepts any `refs/<name>` directory admits it.
"""
import subprocess


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    sha = subprocess.run(["git", "-C", str(r), "rev-parse", "HEAD"], env=ctx.ENV,
                         capture_output=True, text=True).stdout.strip()
    ctx.write(r / ".git/refs/weird/thing", sha + "\n")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "s50-03-unknown-ref-namespace", "tool": "anchor", "expect": "error", "defects": [], "build": build}]

"""Negative control (F3): an unmodified `--claim` abbreviation names a directory at HEAD. The argv fence must
refuse the shape before any git call."""
import pathlib


def build(ctx, d):
    r = ctx.init(d / "lane")
    ctx.write(r / "plans/round-7-claims.md/x.md", "directory standing in for a claims file\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "freeze")
    ctx.write(r / "corpus/evidence/round7/x-probe.txt", "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    return ["--lane", str(r), "--claim", "plans/round-7-claims.md", "--receipt", "corpus/evidence/round7/x-probe.txt"]


FIXTURES = [{"fid": "abbrev-claim", "tool": "order", "expect": "error", "defects": [], "build": build}]

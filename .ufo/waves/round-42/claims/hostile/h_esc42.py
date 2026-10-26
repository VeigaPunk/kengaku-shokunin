"""Hostile module (repair d): a relative argv token that resolves outside the fixture dir must break the contract."""


def b(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "corpus/SOURCES.md", "no rows\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "fixture")
    return ["--lane", "../../../../.."]


FIXTURES = [{"fid": "h-esc42-relative-escape", "tool": "anchor", "expect": "accept", "defects": [], "build": b}]

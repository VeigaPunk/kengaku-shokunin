import pathlib


def build_placeholder(ctx, d):
    lane = ctx.init(d / "lane")
    ctx.write(lane / "note.txt", "local\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "local")
    return ["--lane", "{WORK}/../../outside", "--claims", "claims.md", "--receipt", "receipt.txt"]


def build_nul(ctx, d):
    lane = ctx.init(d / "lane")
    ctx.write(lane / "note.txt", "local\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "local")
    return ["--lane", "lane\u0000/../../outside", "--claims", "claims.md", "--receipt", "receipt.txt"]


def build_extra(ctx, d):
    lane = ctx.init(d / "lane")
    ctx.write(lane / "note.txt", "local\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "local")
    return ["--lane", "lane", "--claims", "claims.md", "--receipt", "receipt.txt", "surplus"]


FIXTURES = [
    {"fid": "argv-placeholder-lane-escape", "tool": "order", "expect": "error", "defects": [], "build": build_placeholder},
    {"fid": "argv-nul-lane", "tool": "order", "expect": "error", "defects": [], "build": build_nul},
    {"fid": "argv-extra-token", "tool": "order", "expect": "error", "defects": [], "build": build_extra},
]

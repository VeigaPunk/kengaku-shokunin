import pathlib


def build_accept(ctx, d):
    (pathlib.Path(d) / "lane-file").write_text("not a repository\n")
    return ["--lane", "lane-file", "--claims", "claims.md", "--receipt", "receipt.txt"]


def build_reject(ctx, d):
    (pathlib.Path(d) / "lane-file").write_text("still not a repository\n")
    return ["--lane", "lane-file", "--claims", "claims.md", "--receipt", "receipt.txt"]


FIXTURES = [
    {"fid": "phantom-order-accept", "tool": "order", "expect": "accept", "defects": [], "build": build_accept},
    {"fid": "phantom-order-reject", "tool": "order", "expect": "reject", "defects": [], "build": build_reject},
]

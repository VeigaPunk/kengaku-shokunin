def build_accept(ctx, d):
    return ["--lane", "missing\nlane", "--evidence-ref", "head"]


def build_reject(ctx, d):
    return ["--lane", "another\nmissing", "--evidence-ref", "index"]


FIXTURES = [
    {"fid": "newline-anchor-accept", "tool": "anchor", "expect": "accept", "defects": [], "build": build_accept},
    {"fid": "newline-anchor-reject", "tool": "anchor", "expect": "reject", "defects": [], "build": build_reject},
]

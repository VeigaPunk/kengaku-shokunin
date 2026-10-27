import pathlib


def build_accept(ctx, d):
    return ["--lane", "missing-lane", "--evidence-ref", "head"]


def build_reject(ctx, d):
    return ["--lane", "missing-lane", "--evidence-ref", "index"]


FIXTURES = [
    {"fid": "phantom-anchor-accept", "tool": "anchor", "expect": "accept", "defects": [], "build": build_accept},
    {"fid": "phantom-anchor-reject", "tool": "anchor", "expect": "reject", "defects": [], "build": build_reject},
]

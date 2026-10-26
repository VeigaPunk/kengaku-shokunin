"""D1 (R41MutC1Counter): an argv traversal token `{WORK}/../esc` must be refused by path_ok.

Drafted extra control for counter mutant KM06 (path_ok traversal check -> True).
Expected pristine counter: SETUP refusal, exit 2.
"""


def build(ctx, d):
    root = ctx.init(d / "lane")
    ctx.write(root / "README.md", "d1\n")
    return ["--lane", str(root), "--work", "{WORK}/../esc"]


FIXTURES = [{"fid": "d1-work-traversal", "tool": "receipts", "expect": "error", "defects": [],
             "build": build}]

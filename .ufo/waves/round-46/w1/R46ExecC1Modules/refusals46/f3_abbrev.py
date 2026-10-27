"""Round-44 hostile module f3 (`R43SentinelCounter` F3): `--claim` (argparse abbreviation) names a TREE at HEAD.
Round-43 counter: leg i silent, admitted; round-44 counter: SETUP refusal (argv not the contract shape)."""


def build(ctx, d):
    r = ctx.init(d / "lane")
    ctx.write(r / "plans/round-7-claims.md/x.md", "# a directory standing in for the claims file\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "freeze")
    ctx.write(r / "corpus/evidence/round7/x-probe.txt", "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "receipt")
    return ["--lane", str(r), "--claim", "plans/round-7-claims.md", "--receip", "corpus/evidence/round7/x-probe.txt"]


FIXTURES = [{"fid": "f3-abbrev-tree-claims", "tool": "order", "expect": "error", "defects": [], "build": build}]

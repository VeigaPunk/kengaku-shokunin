"""Round-44 hostile module f5 (`R43SentinelCounter` F5): the fixture's object store borrows from a store outside d
(`objects/info/alternates`). Round-43 counter: admitted; round-44 counter: SETUP refusal (alternates present)."""
import pathlib


def build(ctx, d):
    other = ctx.init(pathlib.Path(d).parent / "store")
    ctx.write(other / "x.txt", "borrowed\n")
    ctx.git(other, "add", "-A")
    ctx.git(other, "commit", "-qm", "store")
    r = ctx.init(d / "lane")
    ctx.write(r / ".git/objects/info/alternates", str(other / ".git/objects") + "\n")
    ctx.write(r / "claims.md", "x\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "f")
    return ["--lane", str(r), "--claims", "claims.md", "--receipt", "claims.md"]


FIXTURES = [{"fid": "f5-alternates-outside", "tool": "order", "expect": "error", "defects": [], "build": build}]

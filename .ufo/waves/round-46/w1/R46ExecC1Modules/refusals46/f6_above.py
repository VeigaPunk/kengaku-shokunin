"""Round-44 hostile module f6 (`R43SentinelCounter` F6/F2): `--lane` names a plain directory inside d, and the repo
git discovers from it sits ABOVE d. Round-43 counter: admitted (no repo under d to inspect); round-44 counter: SETUP
refusal (the `--lane` toplevel is outside the fixture)."""
import pathlib


def build(ctx, d):
    up = ctx.init(pathlib.Path(d).parent)
    ctx.write(pathlib.Path(d) / "sub" / "claims.md", "x\n")
    ctx.git(up, "add", "-A")
    ctx.git(up, "commit", "-qm", "above")
    return ["--lane", str(pathlib.Path(d) / "sub"), "--claims", "claims.md", "--receipt", "claims.md"]


FIXTURES = [{"fid": "f6-repo-above-d", "tool": "order", "expect": "error", "defects": [], "build": build}]

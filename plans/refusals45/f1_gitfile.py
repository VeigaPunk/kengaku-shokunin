"""Round-44 hostile module f1 (`R43SentinelCounter` F1): the fixture's git dir lives beside d, `d/.git` is a FILE.
Round-43 counter: admitted (`wrong=0`); round-44 counter: SETUP refusal (`.git is a file`)."""
import pathlib


def build(ctx, d):
    gd = pathlib.Path(d).parent / "side" / "gitdir"
    ctx.write(gd.parent / ".keep", "")
    ctx.sh("git", "init", "-q", "-b", "master", "--separate-git-dir", str(gd), str(d))
    ctx.write(pathlib.Path(d) / ".ufo/waves/round-42/claims/round-42-claims.md", "nothing ran\n")
    ctx.git(d, "add", "-A")
    ctx.git(d, "commit", "-qm", "claims")
    ctx.write(pathlib.Path(d) / "corpus/evidence/round42/receipt.txt", "receipt\n")
    ctx.git(d, "add", "-A")
    ctx.git(d, "commit", "-qm", "receipt")
    return ["--lane", ".", "--claims", ".ufo/waves/round-42/claims/round-42-claims.md",
            "--receipt", "corpus/evidence/round42/receipt.txt"]


FIXTURES = [{"fid": "f1-gitdir-outside", "tool": "order", "expect": "accept", "defects": [], "build": build}]

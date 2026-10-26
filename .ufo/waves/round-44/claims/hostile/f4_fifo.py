"""Round-44 hostile module f4 (`R43SentinelCounter` F4/F5): `.git/config` includes a FIFO outside d.
Round-43 counter: the parent-side `git config` blocks (run under `timeout 60`, exit 124); round-44 counter: SETUP
refusal (`carries an include`) with no hang."""
import os
import pathlib


def build(ctx, d):
    r = ctx.init(d / "lane")
    ctx.write(r / "claims.md", "x\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "f")
    fifo = pathlib.Path(d).parent / "fifo.cfg"
    os.mkfifo(fifo)
    ctx.sh("git", "-C", str(r), "config", "--add", "include.path", str(fifo))
    return ["--lane", str(r), "--claims", "claims.md", "--receipt", "claims.md"]


FIXTURES = [{"fid": "f4-fifo-include", "tool": "order", "expect": "error", "defects": [], "build": build}]

import os, pathlib

def f_fifo(ctx, d):
    ctx.init(d)
    ctx.write(pathlib.Path(d) / "claims.md", "x\n")
    ctx.git(d, "add", "-A")
    ctx.git(d, "commit", "-qm", "f")
    fifo = pathlib.Path(d).parent / "fifo.cfg"
    os.mkfifo(fifo)
    ctx.sh("git", "-C", str(d), "config", "--add", "include.path", str(fifo))
    return ["--lane", ".", "--claims", "claims.md", "--receipt", "claims.md"]

FIXTURES = [{"fid": "fifo-include", "tool": "order", "expect": "error", "defects": [], "build": f_fifo}]

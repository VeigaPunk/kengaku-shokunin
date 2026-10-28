"""packed-refs whose `^` peel row precedes every ref row (order violation)."""
def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.git(r, "tag", "-a", "v1", "-m", "tag one")
    ctx.git(r, "pack-refs", "--all")
    pk = r / ".git/packed-refs"
    rows = [x for x in pk.read_bytes().split(b"\n")]
    peel = [x for x in rows if x.startswith(b"^")]
    rest = [x for x in rows if not x.startswith(b"^")]
    ctx.write(pk, b"\n".join(peel + rest))
    return ["--lane", "repo"]
FIXTURES = [{"fid": "p08-peel-before-ref", "tool": "anchor", "expect": "error", "defects": [], "build": build}]

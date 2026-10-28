"""peel row carries 41 hex digits (a reader that truncates or slices the row resolves a foreign oid)."""
def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.git(r, "tag", "-a", "v1", "-m", "tag one")
    ctx.git(r, "pack-refs", "--all")
    pk = r / ".git/packed-refs"
    rows = pk.read_bytes().split(b"\n")
    ctx.write(pk, b"\n".join(b"^" + b"1" * 41 if x.startswith(b"^") else x for x in rows))
    return ["--lane", "repo"]
FIXTURES = [{"fid": "p09-peel-41hex", "tool": "anchor", "expect": "error", "defects": [], "build": build}]

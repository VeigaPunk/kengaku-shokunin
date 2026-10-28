"""peel line names an object present in NO store (pure dangling reference)."""
def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.git(r, "tag", "-a", "v1", "-m", "tag one")
    ctx.git(r, "pack-refs", "--all")
    pk = r / ".git" / "packed-refs"
    rows = pk.read_bytes().split(b"\n")
    ctx.write(pk, b"\n".join(b"^" + b"1" * 40 if row.startswith(b"^") else row for row in rows))
    if ctx.git(r, "cat-file", "-e", "1" * 40, check=False).returncode == 0:
        raise RuntimeError("fixture defect")
    return ["--lane", "repo"]
FIXTURES = [{"fid": "p02-peel-dangling", "tool": "anchor", "expect": "error", "defects": [], "build": build}]

"""SUBSTITUTE CANDIDATE for round-50 item (i) (seat R50C1CritBlind8) — NOT the item's letter shape.

The letter shape ("a peeled line naming an object only present in an outside store") is admitted by the fence at
`57adce4a` and cannot be refused without a resolvability leg the fence does not have (measured: the honest row
`n07-reflog-gc` keeps zero loose objects, so a loose-object existence check would over-refuse the frozen
population). This module is the minimum hostile shape the packed-refs leg *does* refuse: a peel row that is not
git's 40-hex oid, so a reader that slices the row (or trusts a 40-char prefix) resolves an oid git never wrote.
"""
def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.git(r, "tag", "-a", "v1", "-m", "tag one")
    ctx.git(r, "pack-refs", "--all")
    pk = r / ".git" / "packed-refs"
    rows = pk.read_bytes().split(b"\n")
    ctx.write(pk, b"\n".join(b"^" + b"1" * 41 if row.startswith(b"^") else row for row in rows))
    return ["--lane", "repo"]


FIXTURES = [{"fid": "s50-13-packed-peel-shape", "tool": "anchor", "expect": "error", "defects": [],
             "build": build}]

"""Sealed50 hostile (round-50 blind seat R50C1CritBlind8): the peeled line of a packed tag names an object whose
only bytes live outside the repository's store.

git writes `^<sha>` under an annotated tag's packed line (`git pack-refs`); this fixture packs the refs honestly
and then repoints the peel at a commit that exists only in a second object store under the fixture. Witnesses the
packed-refs leg (`_packed`): the peel is checked for 40-hex shape and nothing else, so a store whose ref graph is
resolved from bytes that are not its own is admitted.
"""
import shutil


def build(ctx, d):
    r = ctx.init(d / "repo")
    ctx.write(r / "a.txt", "one\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "one")
    ctx.git(r, "tag", "-a", "v1", "-m", "tag one")
    ctx.git(r, "pack-refs", "--all")

    # a second store: a real commit, its object file copied out, the repository that made it removed
    ext = ctx.init(d / "ext")
    ctx.write(ext / "b.txt", "two\n")
    ctx.git(ext, "add", "-A")
    ctx.git(ext, "commit", "-q", "-m", "two")
    foreign = ctx.git(ext, "rev-parse", "HEAD").stdout.strip()
    src = ext / ".git" / "objects" / foreign[:2] / foreign[2:]
    ctx.write(d / "outside-store" / "objects" / foreign[:2] / foreign[2:], src.read_bytes())
    shutil.rmtree(ext)

    pk = r / ".git" / "packed-refs"
    rows = pk.read_bytes().split(b"\n")
    ctx.write(pk, b"\n".join(b"^" + foreign.encode() if row.startswith(b"^") else row for row in rows))

    if ctx.git(r, "cat-file", "-e", foreign, check=False).returncode == 0:
        raise RuntimeError("fixture defect: the peeled target resolves inside the repository store")
    return ["--lane", "repo"]


FIXTURES = [{"fid": "s50-11-packed-peel-outside-store", "tool": "anchor", "expect": "error", "defects": [],
             "build": build}]

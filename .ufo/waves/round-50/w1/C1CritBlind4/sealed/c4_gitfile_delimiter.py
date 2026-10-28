"""Round-50 C1 blind hostile module (seat `R50C1CritBlind4`, class B4-a): a work tree whose `.git` is a FILE
and whose `gitdir:` line carries a DELIMITER — a NUL or a second newline-separated `gitdir:` declaration — that
makes the pointer name more than one store.

Written blind: authored in wave 1 before the repaired `plans/fixture_fence.py` exists, from git's documented
gitfile format plus the honest class `n21-separate-gitdir` only. The repaired fence must REFUSE every fixture
here (the counter's SEALED leg requires `BREACH` for each); nothing above is a claim about how the repair is
spelled.

Measured git 2.56.0 behaviour of the two payloads (receipts in the seat report, `git_delimiter.out`):

  `gitdir: ../../side/store2\\0../store\\n`  — git truncates the value at the first NUL (C-string), so it
      resolves the store OUTSIDE the fixture dir (`<gen>/side/store2`, `rev-parse --absolute-git-dir` = that
      path, `log -1` = `OUTSIDE-STORE-COMMIT`), while the same bytes, read to the end, name the in-`d` store
      `../store` (`INSIDE-STORE-COMMIT`). The pointer is not one store.

  `gitdir: ../store\\ngitdir: ../../side/store2\\n` — git refuses the gitfile outright
      (`fatal: gitfile does not point to a valid repository`, rc 128): it stats the whole buffer, newline
      included. A line-oriented reader takes line 1, `../store`, which is a complete plain-init store inside
      `d` — so a fence that resolves the first `gitdir:` line and classifies that store admits a fixture whose
      git dir git itself will not use, and whose second declaration names a store outside `d`.

Why these are hostile and not over-refusal bait: in both payloads the store that git uses (or refuses to pick)
is NOT the store the bytes declare, and one of the two candidate stores lies outside the fixture dir. The
fence's predicate is "admit only a fixture whose git store is provably the shape a plain init writes inside
`d`" — a pointer with two readings is not provable, so the only sound verdict is refusal. The delta from the
honest class `n21` is exactly the delimiter: `n21` writes `gitdir: ../store\\n` and must stay ADMITTED.

Round-44 builder contract: `build(ctx, d)` fills `d`, returns the argv tail. Deterministic: the gitfile payload
is a fixed byte literal, the in-`d` store is a plain init (its masked `index` the only volatile entry), and the
outside store carries fixed dates through the pinned `Ctx.ENV`.
"""
import pathlib
import shutil


def _outside_store(ctx, d):
    """A BARE store outside the fixture dir, holding one commit whose subject names it."""
    side = d.parent / "side" / "store2"
    ctx.sh("git", "init", "-q", "--bare", "-b", "master", str(side))
    seed = d.parent / "seed"
    ctx.sh("git", "init", "-q", "-b", "master", str(seed))
    ctx.write(seed / "x.txt", "outside\n")
    ctx.git(seed, "add", "-A")
    ctx.git(seed, "commit", "-q", "-m", "OUTSIDE-STORE-COMMIT")
    ctx.git(seed, "push", "-q", str(side), "master:refs/heads/master")
    shutil.rmtree(seed)
    return side


def _gitfile_repo(ctx, d):
    """`d/wt` with a relative `gitdir: ../store` file over a plain-init store at `d/store` (the n21 shape)."""
    wt, store = d / "wt", d / "store"
    ctx.sh("git", "init", "-q", "-b", "master", "--separate-git-dir", str(store), str(wt))
    ctx.write(wt / ".git", "gitdir: ../store\n")
    ctx.write(wt / "a.txt", "one\n")
    ctx.git(wt, "add", "-A")
    ctx.git(wt, "commit", "-q", "-m", "one")
    ctx.write(wt / "b.txt", "two\n")
    ctx.git(wt, "add", "-A")
    ctx.git(wt, "commit", "-q", "-m", "two")
    return wt


def build_nul(ctx, d):
    d = pathlib.Path(d)
    _outside_store(ctx, d)
    wt = _gitfile_repo(ctx, d)
    ctx.write(wt / ".git", b"gitdir: ../../side/store2\x00../store\n")
    return ["--lane", "wt"]


def build_newline(ctx, d):
    d = pathlib.Path(d)
    _outside_store(ctx, d)
    wt = _gitfile_repo(ctx, d)
    ctx.write(wt / ".git", b"gitdir: ../store\ngitdir: ../../side/store2\n")
    return ["--lane", "wt"]


FIXTURES = [
    {"fid": "b4a-gitfile-nul-two-stores", "tool": "anchor", "expect": "accept", "defects": [],
     "build": build_nul},
    {"fid": "b4a-gitfile-newline-two-pointers", "tool": "anchor", "expect": "accept", "defects": [],
     "build": build_newline},
]

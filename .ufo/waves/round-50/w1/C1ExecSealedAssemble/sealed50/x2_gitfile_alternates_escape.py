"""Blind hostile module X2 (round-50 wave 1, seat R50C1CritBlind2): TWO-HOP escape — the store is reached by a
`.git` FILE that stays inside `d` (the honest `n21_separate_gitdir` shape), and that store's
`objects/info/alternates` names an object store outside `d` (the hostile `f5_alternates` shape).

Hop 1 (legitimate, must be admitted): `d/wt/.git` is a file, `gitdir: ../store`, and `d/store` is the plain store
`git init --separate-git-dir` writes. This is byte-for-byte the honest class n21, whose admission R50-C1 requires.

Hop 2 (hostile, must be refused): `d/store/objects/info/alternates` names an object directory that lives BESIDE
`d`. Git reads it (gitrepository-layout(5): "objects/info/alternates — … to get information about objects
available in other object directories"), so an admitting fence hands the tool an object store outside `d`.

Why this is the two-hop blind case and not f5 with extra steps: `f5_alternates` (r44 refusal, single hop) writes
the alternates line into the `.git` DIRECTORY of the fixture's own repository, so a fence that classifies one
store at `<repo>/.git` and resolves that one alternates line catches it. Here the store that owns the alternates
line is not named `.git` at all — it is `d/store`, reachable only by resolving the fixture-level gitfile. A repair
that implements the two honest classes INDEPENDENTLY — "resolve `.git` files whose target is inside `d`"
(n21) and "admit alternates lines that resolve inside `d`, relative to the `.git/objects` of each store"
(n22) — is correct only if it feeds hop 1's RESOLVED store into hop 2's containment test. A repair that applies
the alternates check only to directories literally named `.git`, or that resolves the alternates line against
`d` instead of against the store's own `objects/` directory, admits X2 while admitting both honest classes.

Two fixtures, the two forms git accepts for an alternates line (both resolved relative to the OWNING store's
`objects/` directory):

  x2-alt-abs   absolute target   `<build>/alt-store-abs/.git/objects`
  x2-alt-rel   relative target   `../../../alt-store-rel/.git/objects` (escapes `d` through `..`)

The relative form is the interesting one: it contains no absolute path, so a fence that refuses absolute targets
and accepts `..`-relative lines (as the honest n22 fixture, `../../../main/.git/objects`, demands) admits it.

Distinctness from the frozen batteries (checked in this seat's report): no frozen module combines a gitfile hop
with an alternates hop. `f1_gitfile` has a gitfile and no alternates; `f5_alternates` has alternates and no
gitfile; `f15_objects_symlink_out`/`f16_objects_hardlink_out` move the objects directory itself; `s_objects_link`
(r46 sealed) symlinks `objects` out of a `.git` dir. None of them hides the alternates line behind a gitfile.

Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail. `ctx`'s root is the module build
dir (the parent of `d`), which is why the escaped object store can be created beside `d` — that is the escape.
"""
import os
import pathlib


def _outside_objects(ctx, d, name):
    """The borrowed object store: a full repository BESIDE `d`, so the borrow crosses the fence's boundary."""
    store = pathlib.Path(d).parent / name
    s = ctx.init(store)
    ctx.write(s / "borrowed.txt", "borrowed\n")
    ctx.git(s, "add", "-A")
    ctx.git(s, "commit", "-qm", "borrowed")
    return s / ".git" / "objects"


def _gitfile_repo(ctx, d):
    """Hop 1: the honest n21 shape — a work tree whose `.git` file names a store inside `d`."""
    wt = pathlib.Path(d) / "wt"
    store = pathlib.Path(d) / "store"
    ctx.sh("git", "init", "-q", "-b", "master", "--separate-git-dir", str(store), str(wt))
    ctx.write(wt / ".git", "gitdir: ../store\n")
    ctx.write(wt / "a.txt", "one\n")
    ctx.git(wt, "add", "-A")
    ctx.git(wt, "commit", "-q", "-m", "one")
    ctx.write(wt / "b.txt", "two\n")
    ctx.git(wt, "add", "-A")
    ctx.git(wt, "commit", "-q", "-m", "two")
    return store


def _with_alternates(ctx, d, line):
    store = _gitfile_repo(ctx, d)
    ctx.write(store / "objects" / "info" / "alternates", line + "\n")
    return ["--lane", "wt"]


def build_abs(ctx, d):
    objects = _outside_objects(ctx, d, "alt-store-abs")
    return _with_alternates(ctx, d, str(objects))


def build_rel(ctx, d):
    objects = _outside_objects(ctx, d, "alt-store-rel")
    base = pathlib.Path(d) / "store" / "objects"
    return _with_alternates(ctx, d, os.path.relpath(str(objects), str(base)))


FIXTURES = [
    {"fid": "x2-alt-abs", "tool": "anchor", "expect": "error", "defects": [], "build": build_abs},
    {"fid": "x2-alt-rel", "tool": "anchor", "expect": "error", "defects": [], "build": build_rel},
]

"""R50-C1 blind hostile module B7-a (seat `R50C1CritBlind7`, wave `round-50/w1`): the store a `.git` FILE names
is ITSELF A SYMLINK whose target is a full plain store INSIDE `d`.

Shape, inside the fixture dir `d` (one repository, everything else ordinary):

  d/wt/.git          a FILE, one line: `gitdir: ../store`
  d/store            a SYMLINK -> `realstore` (relative, same level, target inside `d`)
  d/realstore/       the store `git init --separate-git-dir` writes: HEAD, config (no absolute path), refs/,
                     logs/, objects/, info/exclude, index
  d/wt/a.txt, b.txt  two commits of ordinary worktree content

The gitfile text is exactly the honest `n21_separate_gitdir` form the round-50 repair must ADMIT, and the store
it resolves to is byte-for-byte a plain-init store. The single difference from `n21` is that the store the
gitfile names is reached through a symlink. Two containment answers exist for this fixture and they disagree:

  * lexically, `d/wt/../store` is inside `d` (no `..` escape, no absolute component, no separator a text check
    can object to);
  * after resolution, `d/realstore` is also inside `d`.

So every repair that widened the fence to `.git` files by `resolve()`-then-`is_relative_to(d)` — the natural
way to admit `n21`/`n20` — admits this fixture, and the advertised policy ("the tree has no symlink anywhere",
fence docstring structure item 3) says it must be REFUSED. Refusal by "any `.git` file is a gitdir redirect" is
also a refusal; the point of the fixture is that the *containment* argument cannot carry it.

Material, not cosmetic: git follows the symlink (`git -C wt rev-parse --absolute-git-dir` answers through it and
`git -C wt rev-parse HEAD` succeeds), so the fixture is a live repository rather than a broken one, and a tool
run behind an admitting fence stats and opens `d/realstore/*` through a path the fixture never classifies.

Distinct from the landed sealed set: `s50_01_stray_symlink` is a symlink outside any store pointing OUTSIDE `d`
(s50-01 admits nothing about gitfile stores), `s50_gitfile_symlink_chain` is a gitfile whose symlink chain ends
OUTSIDE `d`, `s6_gitfile_rel_objects_link` keeps the gitfile target a real directory and makes the store's
`objects` a symlink out. Here the gitfile target itself is the symlink and both its text and its resolution stay
inside `d`; nothing inside the store is a symlink.

Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""
import pathlib
import shutil

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    d = pathlib.Path(d)
    wt = d / "wt"
    store = d / "store"
    real = d / "realstore"
    ctx.sh("git", "init", "-q", "-b", "master", "--separate-git-dir", str(store), str(wt))
    shutil.move(str(store), str(real))
    store.symlink_to("realstore", target_is_directory=True)
    ctx.write(wt / ".git", "gitdir: ../store\n")      # git writes an absolute line; the relative form is n21's
    ctx.write(wt / "a.txt", "one\n")
    ctx.git(wt, "add", "-A")
    ctx.git(wt, "commit", "-q", "-m", "one")
    ctx.write(wt / RECEIPT, "receipt\n")
    ctx.git(wt, "add", "-A")
    ctx.git(wt, "commit", "-q", "-m", "receipt")
    return ["--lane", "wt", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "b7a-gitfile-store-symlink-inside-d", "tool": "order", "expect": "reject", "defects": [],
             "build": build}]

"""Round-50 blind hostile module 6b — a `.git` FILE naming `../`, whose store's `objects` is a symlink out.

The round-50 honest classes force the fence to stop refusing `.git` files outright: `n21`
(`init --separate-git-dir` with the store inside `d`) and `n20` (linked worktree) are git states the
instrument must ADMIT. The `.git`-file branch is therefore the widening this repair introduces, and
these two fixtures are the widening's two escape layers:

  seal6-gitfile-up-outside       the repository IS `d`, and `d/.git` is the FILE `gitdir: ../s6-store-up`
                                 — the `../` form, one level up, naming a store OUTSIDE `d`; that
                                 store's `objects` is a symlink to a third location outside `d`.
                                 Both indirections present, as specified.
  seal6-gitfile-up-inside-link   `.git` = `gitdir: ../store` where `d/sub/store` is INSIDE `d` — the
                                 honest `n21` shape — but that store's `objects` is a symlink to a
                                 directory outside `d`. The gitfile check passes; only classifying
                                 the *resolved* store catches it.
  seal6-gitfile-submodule-store-link
                                 `.git` = `gitdir: ../main/.git/modules/sub` — a path inside `d` that
                                 the tree walk never visits, because it is under a `.git` directory.
                                 That path is a symlink to a full, honest-looking store outside `d`.
                                 This is the fixture that tests the fence's own proof argument: the
                                 walk's "no symlinks anywhere" rule is what makes a gitfile widening
                                 safe, and the walk does not descend into `.git`.

The second fixture is the object-store layer; the third is the sharpest: a repair that proves the
gitfile target is inside `d` and then trusts it (skipping the store classification, or classifying
the redirect instead of the store) passes every honest class, the whole `refusals46` battery and
`sealed46`, and admits it.

Both repositories stay live: `git -C <repo> rev-parse HEAD` succeeds through the escape, so a refusal
cannot be excused as "the repo was broken".
"""
import os
import pathlib
import shutil

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"


def _repo_with_history(ctx, repo):
    ctx.write(repo / CLAIMS, "nothing ran\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-qm", "claims")
    ctx.write(repo / "corpus/evidence/receipt.txt", "receipt\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-qm", "receipt")
    return repo


def build_gitfile_up_outside(ctx, d):
    d = pathlib.Path(d)
    repo = _repo_with_history(ctx, ctx.init(d))           # the repository is d itself
    store = d.parent / "s6-store-up"                      # <gen>/s6-store-up — outside d
    os.rename(repo / ".git", store)
    (repo / ".git").write_text("gitdir: ../s6-store-up\n")
    out = d.parent / "s6-out-objects"
    out.mkdir()
    shutil.move(str(store / "objects"), str(out / "objects"))
    (store / "objects").symlink_to(out / "objects", target_is_directory=True)
    return ["--lane", ".", "--claims", CLAIMS, "--receipt", "corpus/evidence/receipt.txt"]


def build_gitfile_up_inside_objects_link(ctx, d):
    d = pathlib.Path(d)
    sub = d / "sub"
    sub.mkdir()
    repo = _repo_with_history(ctx, ctx.init(sub / "repo"))
    store = sub / "store"                                 # inside d: the honest n21 shape
    os.rename(repo / ".git", store)
    (repo / ".git").write_text("gitdir: ../store\n")
    out = d.parent / "s6-out-objects-2"
    out.mkdir()
    shutil.move(str(store / "objects"), str(out / "objects"))
    (store / "objects").symlink_to(out / "objects", target_is_directory=True)
    return ["--lane", "sub/repo", "--claims", CLAIMS, "--receipt", "corpus/evidence/receipt.txt"]


def build_gitfile_submodule_store_link(ctx, d):
    d = pathlib.Path(d)
    main = _repo_with_history(ctx, ctx.init(d / "main"))
    real = d.parent / "s6-real-sub-store"                 # full store, outside d
    shutil.copytree(str(main / ".git"), str(real))
    mods = main / ".git" / "modules"
    mods.mkdir()
    (mods / "sub").symlink_to(real, target_is_directory=True)
    second = d / "second"                                 # a worktree whose only store is the link
    second.mkdir()
    (second / ".git").write_text("gitdir: ../main/.git/modules/sub\n")
    return ["--lane", "main", "--claims", CLAIMS, "--receipt", "corpus/evidence/receipt.txt"]


FIXTURES = [
    {"fid": "seal6-gitfile-up-outside", "tool": "order", "expect": "reject", "defects": [],
     "build": build_gitfile_up_outside},
    {"fid": "seal6-gitfile-up-inside-link", "tool": "order", "expect": "reject", "defects": [],
     "build": build_gitfile_up_inside_objects_link},
    {"fid": "seal6-gitfile-submodule-store-link", "tool": "order", "expect": "reject", "defects": [],
     "build": build_gitfile_submodule_store_link},
]

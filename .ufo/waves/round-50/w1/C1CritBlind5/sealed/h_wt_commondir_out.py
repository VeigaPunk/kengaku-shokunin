"""Sealed blind hostile module B — round-50 wave-1 seat `R50C1CritBlind5` (critic, R50-C1).

Attack class: **a linked worktree whose gitdir is inside `d` and whose `commondir` leaves `d`.**

    wt/.git            "gitdir: ../wtadmin"                 a FILE, target INSIDE d
    wtadmin/gitdir     "../wt/.git"                         back-pointer, INSIDE d
    wtadmin/commondir  "../../wt-common/.git"               resolves OUTSIDE d

Built with real git, then relocated the way a moved store leaves a worktree: `git init` + commit + `git branch
feature` in `d.parent/wt-common`, `git worktree add --relative-paths -q d/wt feature`, then the per-worktree
admin directory (`wt-common/.git/worktrees/wt`) is moved into `d` and its two relative pointers are rewritten.
Git accepts and honours the result: `git -C wt rev-parse --show-toplevel` answers `d/wt` (inside) and
`rev-parse --absolute-git-dir` answers `d/wtadmin` (inside), while `rev-parse --git-common-dir` answers
`d.parent/wt-common/.git` (outside) and `git -C wt log`/`cat-file` read refs and objects from there (seat
receipt; moving the outside store away makes those reads fail).

Why this is the blind hostile counterpart of the repair. The repair must widen the allowlist twice for the
honest classes: a `.git` FILE whose target is inside `d` (`n21_separate_gitdir`) and the per-worktree metadata of
`n20_linked_worktree` (which carries `gitdir` and `commondir`). The tempting widenings — "admit a gitfile whose
target resolves inside `d`", "admit a worktree store whose `commondir` is a relative path", "admit `commondir`
== `../..`" — each admit this module, because its gitfile target is inside `d` and its `commondir` is a plain
relative path. Only a repair that resolves `commondir` against the *gitdir* (not against `d`, and not by shape)
and requires the resolved common store inside `d` refuses it. Both rev-parse legs a fence would consult for the
boundary answer "inside", so this class is invisible to a rev-parse-based gate and visible only to a
store-content walk.

Measured on the base fence `05d5fe03…`: BREACH, reason `wt/.git is a file (gitdir redirect), not a directory` —
the same blanket rule that over-refuses honest `n20`/`n21`, so that refusal says nothing about the repair.

Determinism: every pointer is relative (git `--relative-paths` wrote the originals; the relocation rewrites them
relative to their own directories), so no build-scratch absolute path enters the tree. Round-44 builder
contract: `build(ctx, d)` fills `d` and returns the argv tail. `expect` is this seat's statement of the required
verdict (`breach`); the round-50 counter reads only `fid`/`tool`/`build`.
"""
import shutil


def build(ctx, d):
    out = ctx.init(d.parent / "wt-common")
    ctx.write(out / "seed.txt", "seed\n")
    ctx.git(out, "add", "-A")
    ctx.git(out, "commit", "-qm", "seed")
    ctx.git(out, "branch", "feature")
    ctx.sh("git", "-C", str(out), "worktree", "add", "--relative-paths", "-q", str(d / "wt"), "feature")
    adm = d / "wtadmin"
    shutil.move(str(out / ".git" / "worktrees" / "wt"), str(adm))
    ctx.write(d / "wt" / ".git", "gitdir: ../wtadmin\n")
    ctx.write(adm / "gitdir", "../wt/.git\n")
    ctx.write(adm / "commondir", "../../wt-common/.git\n")
    return ["--lane", "wt"]


FIXTURES = [{"fid": "bl5-wt-commondir-out", "tool": "anchor", "expect": "breach", "defects": [], "build": build}]

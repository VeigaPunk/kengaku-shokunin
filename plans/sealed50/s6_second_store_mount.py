"""Round-50 blind hostile module 6a — the SECOND repository's store, and the mount boundary.

Item: two repositories where the second one's store crosses a mount boundary.

The literal shape (a store whose `st_dev` differs from `d`'s while the store is lexically inside `d`)
cannot be expressed as a *fixture state* on this host. Measured, receipts in
`C1CritBlind6/receipts/device-probe.txt`:

  * a hardlink can never emulate a mount boundary: the kernel refuses the link, by construction —
    `os.link(/tmp/x -> /fast/.../x)` and `os.link(/dev/shm/x -> ...)` both return EXDEV
    (`/fast` st_dev 66309, `/tmp` 66308, `/dev/shm` 33).
  * the only way to put a mount point under `d` is a bind mount; in the counter's own process
    `mount()` returns EPERM (no CAP_SYS_ADMIN in the initial user namespace).
  * a private user+mount namespace does make it work — `unshare(CLONE_NEWUSER|CLONE_NEWNS)` rc=0,
    then `mount(/dev/shm -> d/x)` rc=0 and `st_dev(d/x)` becomes 33 — but that is *process* state,
    not fixture state: it reconfigures the counter's namespace for every later fixture, it is
    invisible to `tree_identity`, and it makes the same fixture build differently on a host with
    `kernel.unprivileged_userns_clone=0`. A module that does it is attacking the harness, not the
    fence. It is therefore a counter-level shape (see the seat report), not a module-level one.

What *is* buildable, and what this module builds, is the same hazard in the form a fence can see
without any capability: **a second repository inside `d` whose store is not provably inside `d`.**
Both fixtures keep repository A (`lane`, named by `--lane`) honest, so a fence that validates only
the lane's store, or only the first repository it meets, admits them.

  seal6-second-store-outside  repo B's `.git` is a git-written gitfile naming a store OUTSIDE `d`
                              (absolute path, no `..`, no symlink): the mount boundary's lexical
                              analogue.
  seal6-second-store-twin     repo B's store is inside `d`, but one loose object in it has a second
                              name outside `d` (`nlink=2`): store bytes reachable from outside `d`,
                              which is what a cross-device store buys an attacker, and the only
                              emulation the kernel allows here.

Both must be refused. Refusal reason matters: fixture 1 has to die on "store not inside `d`", not
on the bare "`.git` is a file"; fixture 2 has to die on the second link, not on anything else.
"""
import os
import pathlib
import shutil

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"


def _honest_lane(ctx, d):
    lane = ctx.init(d / "lane")
    ctx.write(lane / CLAIMS, "nothing ran\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "claims")
    return lane


def build_second_store_outside(ctx, d):
    d = pathlib.Path(d)
    _honest_lane(ctx, d)
    outside = d.parent / "s6-store-second"
    outside.mkdir()
    other = d / "other"
    # `git init --separate-git-dir` is git's own way to write a store elsewhere and a `.git` FILE
    # in the worktree: the state is honest in form, hostile only in where the store lives.
    ctx.sh("git", "init", "-q", "-b", "master", "--separate-git-dir", str(outside), str(other))
    ctx.write(other / CLAIMS, "nothing ran\n")
    ctx.git(other, "add", "-A")
    ctx.git(other, "commit", "-qm", "claims")
    gitfile = (other / ".git").read_text().strip()
    if not gitfile.startswith("gitdir:") or ".." in gitfile:
        raise RuntimeError(f"unexpected gitfile form: {gitfile!r}")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", CLAIMS]


def build_second_store_twin(ctx, d):
    d = pathlib.Path(d)
    _honest_lane(ctx, d)
    other = ctx.init(d / "other")
    ctx.write(other / CLAIMS, "nothing ran\n")
    ctx.git(other, "add", "-A")
    ctx.git(other, "commit", "-qm", "claims")
    objs = other / ".git" / "objects"
    loose = sorted(p for p in objs.rglob("*")
                   if p.is_file() and len(p.name) == 38 and len(p.parent.name) == 2)
    if not loose:
        raise RuntimeError("no loose object to twin")
    twin_dir = d.parent / "s6-twin"
    twin_dir.mkdir()
    os.link(loose[0], twin_dir / loose[0].name)          # same device: the only hardlink allowed
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", CLAIMS]


FIXTURES = [
    {"fid": "seal6-second-store-outside", "tool": "order", "expect": "reject", "defects": [],
     "build": build_second_store_outside},
    {"fid": "seal6-second-store-twin", "tool": "order", "expect": "reject", "defects": [],
     "build": build_second_store_twin},
]

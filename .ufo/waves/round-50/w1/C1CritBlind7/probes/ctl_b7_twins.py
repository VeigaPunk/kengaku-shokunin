"""Seat R50C1CritBlind7 PAIRED CONTROLS for the two blind hostile modules (NOT part of the sealed set).

Each control is the twin of one hostile fixture with the symlink replaced by a real directory holding the same
bytes; the gitfile text is otherwise identical, the store is otherwise identical, and the argv is identical.
The hostile twin must be REFUSED and the control must be ADMITTED: that pair is what proves the refusal of the
hostile fixture rests on the symlink and not on a broken repository, an escaped pointer or a malformed store.

  ctl-b7a-real-store     `d/wt/.git` = `gitdir: ../store`, `d/store` a REAL directory  (the honest n21 shape)
  ctl-b7b-real-parent    `d/lane/.git` = `gitdir: ../alias/gitstore`, `d/alias` a REAL directory

Both are expected to be ADMITTED by the tip fence; if either is refused, the corresponding hostile module is not
evidence about the symlink leg (the fence refuses the shape for another reason) and the seat says so.
"""
import pathlib
import shutil

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build_real_store(ctx, d):
    d = pathlib.Path(d)
    wt = d / "wt"
    store = d / "store"
    ctx.sh("git", "init", "-q", "-b", "master", "--separate-git-dir", str(store), str(wt))
    ctx.write(wt / ".git", "gitdir: ../store\n")
    ctx.write(wt / "a.txt", "one\n")
    ctx.git(wt, "add", "-A")
    ctx.git(wt, "commit", "-q", "-m", "one")
    ctx.write(wt / RECEIPT, "receipt\n")
    ctx.git(wt, "add", "-A")
    ctx.git(wt, "commit", "-q", "-m", "receipt")
    return ["--lane", "wt", "--claims", CLAIMS, "--receipt", RECEIPT]


def build_real_parent(ctx, d):
    d = pathlib.Path(d)
    lane = d / "lane"
    store = d / "rho" / "hold" / "gitstore"
    store.parent.mkdir(parents=True, exist_ok=True)
    ctx.sh("git", "init", "-q", "-b", "master", "--separate-git-dir", str(store), str(lane))
    ctx.write(lane / ".git", "gitdir: ../rho/hold/gitstore\n")
    ctx.write(lane / "work.txt", "one\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-q", "-m", "one")
    ctx.write(lane / RECEIPT, "receipt\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-q", "-m", "receipt")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [
    {"fid": "ctl-b7a-real-store", "tool": "order", "expect": "accept", "defects": [],
     "build": build_real_store},
    {"fid": "ctl-b7b-real-parent", "tool": "order", "expect": "accept", "defects": [],
     "build": build_real_parent},
]

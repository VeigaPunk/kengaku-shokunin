#!/usr/bin/env python3
"""SCRATCH PROBE (not a lane artifact): the *plausible* repair, with the one omission I am hunting.

Identical to repair_careful.py except that the gitfile target is resolved lexically and then trusted:
no `lstat` of the target, no realpath containment. That is the omission the fence's own proof
argument invites — "the walk refuses symlinks anywhere in d" is offered as the reason a store cannot
point outside, and the walk does not descend into `.git`, so a target under another repository's
`.git` (a submodule store, a linked-worktree metadata dir) is never walked.

Everything else is the base fence.
"""
import importlib.util
import os
import pathlib
import re
import stat

BASE = pathlib.Path(__file__).with_name("fixture_fence_base.py")
_spec = importlib.util.spec_from_file_location("ff_base2", BASE)
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)

GITFILE = re.compile(r"\Agitdir:[ \t]*(\S+)[ \t]*\n?\Z")


def _gitfile_target(p, d):
    body = base._read(p, 4096)
    if body is None:
        return None, f"{base._rel(p, d)} is unreadable"
    text = body.decode("ascii", "replace")
    m = GITFILE.match(text)
    if m is None:
        return None, f"{base._rel(p, d)} is not a plain gitdir line"
    raw = m.group(1) if m.group(1).startswith("/") else os.path.join(str(p.parent), m.group(1))
    tgt = pathlib.Path(base._norm(raw))
    if not base._inside(tgt, d) or base._norm(tgt) == base._norm(d):
        return None, f"{base._rel(p, d)} names a store outside the fixture"
    return tgt, None


def _tree(d):
    repos, stores, seen = [], [], 0
    for top, dirs, files in os.walk(str(d), followlinks=False):
        seen += len(dirs) + len(files)
        if seen > base.ENTRY_CAP:
            return None, f"fixture tree exceeds {base.ENTRY_CAP} entries"
        t = pathlib.Path(top)
        keep = []
        for name in dirs:
            p = t / name
            try:
                mode = os.lstat(p).st_mode
            except OSError:
                return None, f"{base._rel(p, d)} cannot be lstat'ed"
            if stat.S_ISLNK(mode):
                return None, f"{base._rel(p, d)} is a symlink"
            if not stat.S_ISDIR(mode):
                return None, f"{base._rel(p, d)} is not a directory"
            if name == ".git":
                repos.append(t)
                continue
            keep.append(name)
        dirs[:] = sorted(keep)
        for name in files:
            p = t / name
            try:
                mode = os.lstat(p).st_mode
            except OSError:
                return None, f"{base._rel(p, d)} cannot be lstat'ed"
            if stat.S_ISLNK(mode):
                return None, f"{base._rel(p, d)} is a symlink"
            if name == ".git":
                tgt, why = _gitfile_target(p, d)
                if why:
                    return None, why
                stores.append(tgt)         # the store: classified by the base `_store`
                repos.append(t)            # the worktree counts as a repository for --lane
                continue
            if not stat.S_ISREG(mode):
                return None, f"{base._rel(p, d)} is a special file"
            if os.lstat(p).st_nlink > 1:
                return None, f"{base._rel(p, d)} has more than one hard link"
    if len(repos) + len(stores) > base.REPO_CAP:
        return None, f"fixture holds more than {base.REPO_CAP} repos"
    return (repos, stores), None


def breach(d, argv, tool):
    """The base decision, with `_tree`'s store list classified by the unchanged `_store`."""
    try:
        dpath = pathlib.Path(d)
        st = os.lstat(dpath)
    except (OSError, ValueError, TypeError):
        return "fixture dir cannot be lstat'ed"
    if stat.S_ISLNK(st.st_mode):
        return "fixture dir is a symlink"
    if not stat.S_ISDIR(st.st_mode):
        return "fixture dir is not a directory"
    d = pathlib.Path(base._norm(dpath))
    vals, why = base._argv(d, tool, argv)
    if why:
        return why
    found, why = _tree(d)
    if why:
        return why
    repos, stores = found
    for repo in repos:
        if not (repo / ".git").is_dir():
            continue                       # a gitfile worktree: its store is in `stores`
        why = base._store(repo / ".git", f"{base._rel(repo / '.git', d)}")
        if why:
            return why
    for store in stores:
        why = base._store(store, f"{base._rel(store, d)}")
        if why:
            return why
    lane_tok = vals.get("--lane")
    if not isinstance(lane_tok, str):
        return "argv names no lane to prove"
    lane = pathlib.Path(base._norm(lane_tok if lane_tok.startswith("/") else os.path.join(str(d), lane_tok)))
    try:
        lst = os.lstat(lane)
    except OSError:
        return f"--lane {lane_tok!r} does not exist inside the fixture"
    if stat.S_ISLNK(lst.st_mode):
        return f"--lane {lane_tok!r} is a symlink"
    if not stat.S_ISDIR(lst.st_mode):
        return f"--lane {lane_tok!r} is not a directory"
    if base._norm(lane) not in {base._norm(r) for r in repos}:
        return f"--lane {lane_tok!r} is not a repository inside the fixture"
    return None

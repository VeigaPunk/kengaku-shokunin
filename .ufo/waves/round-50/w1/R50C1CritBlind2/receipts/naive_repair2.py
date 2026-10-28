#!/usr/bin/env python3
"""Scratch-only candidate fence `naive_repair2` (seat R50C1CritBlind2, NOT a deliverable, never landed).

A repair that does the two containment checks the FROZEN sets force, and the relative shortcut they do not:

  gitfile  (`<repo>/.git` is a file)   lifted only when the line is relative AND its resolved target is inside `d`
  worktrees (`.git/worktrees` entry)   lifted only when every `.git/worktrees/*/gitdir` back-pointer resolves
                                       inside `d`  (this is what frozen f18_wtmeta_out demands)
  commondir                            lifted when the line is RELATIVE  (frozen f7 is absolute; f19 is refused
                                       earlier as "lane is not a repository")  <-- the shortcut
  alternates                           lifted when every line is RELATIVE    (frozen f5 is absolute)  <-- the shortcut

Measured consequence: this fence admits the three honest indirection classes R50-C1 requires, keeps REFUSALS
20/20 and SEALED46 12/12 clean, and still admits the blind X1/X2 relative fixtures — nothing in the frozen 32
modules forces a containment test on a relative `commondir` or a relative `alternates` line.
"""
import importlib.util
import os
import pathlib


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


BASE = _load(os.environ.get("NAIVE_BASE", "plans/fixture_fence.py"), "naive2_base")


def _lines(p):
    try:
        return [ln for ln in pathlib.Path(p).read_text(errors="replace").splitlines() if ln.strip()]
    except OSError:
        return None


def _rel_line(line):
    return bool(line) and not line.startswith("/")


def _gitfile_line(p):
    body = _lines(p) or []
    if not body or not body[0].startswith("gitdir:"):
        return None
    return body[0][len("gitdir:"):].strip()


def _inside(p, d):
    p, d = os.path.normpath(str(p)), os.path.normpath(str(d))
    return p == d or p.startswith(d + os.sep)


def _gitfiles(d):
    return [(p, _gitfile_line(p)) for p in pathlib.Path(d).rglob(".git") if p.is_file()]


def _commondirs(d):
    return [(p, (_lines(p) or [None])[0]) for p in pathlib.Path(d).rglob("commondir") if p.is_file()]


def _alternates(d):
    out = []
    for p in pathlib.Path(d).rglob("objects/info/alternates"):
        if p.is_file():
            out.extend((p, ln) for ln in (_lines(p) or []))
    return out


def _gitfile_ok(d):
    for p, line in _gitfiles(d):
        if line is None or not _rel_line(line):
            return False
        if not _inside(p.parent / line, d):
            return False
    return True


def _wtmeta_ok(d):
    """Every `.git/worktrees/*/gitdir` back-pointer must resolve inside `d` (f18's rule)."""
    for p in pathlib.Path(d).rglob(".git/worktrees/*/gitdir"):
        body = _lines(p) or []
        if not body or not _rel_line(body[0]) or not _inside(p.parent / body[0], d):
            return False
    for p in pathlib.Path(d).rglob(".git/worktrees/*/commondir"):
        body = _lines(p) or []
        if not body or not _rel_line(body[0]) or not _inside(p.parent / body[0], d):
            return False
    return True


def breach(d, argv, tool):
    why = BASE.breach(d, argv, tool)
    if why is None:
        return None
    if "is a file (gitdir redirect)" in why:
        return None if _gitfile_ok(d) else why
    if why.endswith("is not a plain-init entry"):
        entry = why.split("/")[-1].split(" ")[0]
        if entry == "worktrees":
            return None if _wtmeta_ok(d) else why
        if entry == "commondir":
            lines = [ln for _p, ln in _commondirs(d)]
            return None if lines and all(_rel_line(ln) for ln in lines) else why
        return why
    if "objects/info/alternates present" in why:
        lines = [ln for _p, ln in _alternates(d)]
        return None if lines and all(_rel_line(ln) for ln in lines) else why
    return why

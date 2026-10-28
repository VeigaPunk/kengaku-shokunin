"""Scratch candidate repairs for seat R50C1CritBlind1 (NOT lane code, NOT another seat's repair).

Two containment policies over one otherwise-identical pointer repair:

  `naive_breach`   the pathlib idiom a hasty repair writes — `pathlib.Path(target).is_relative_to(d)`. `PurePath`
                   never collapses `..` and never resolves symlinks, so a pointer that leaves `d` through either
                   mechanism passes the test.
  `breach`         `os.path.realpath(target)` then a prefix test: containment after the kernel's own resolution.

Both admit the honest in-`d` indirection classes (`n20` worktree gitfile + `commondir`, `n21` separate gitdir,
`n22` in-`d` alternates); only the containment policy differs. Contract matches the fence under test:
`breach(d, argv, tool) -> reason | None`, cwd `d`, no git child.
"""
import os
import pathlib
import stat

STORE_ENTRIES = {"HEAD", "config", "objects", "refs"}


def _inside(p, d):
    p, d = os.path.normpath(str(p)), os.path.normpath(str(d))
    return p == d or p.startswith(d + os.sep)


def _walk(d):
    """(repos, gitfiles, reason): repos are dirs holding a real `.git` dir; gitfiles are `.git` files."""
    repos, gitfiles = [], []
    for top, dirs, files in os.walk(str(d), followlinks=False):
        t = pathlib.Path(top)
        keep = []
        for name in dirs:
            p = t / name
            try:
                mode = os.lstat(p).st_mode
            except OSError:
                return None, None, f"{p} cannot be lstat'ed"
            if stat.S_ISLNK(mode):
                continue                     # naive: a symlink is simply not descended
            if not stat.S_ISDIR(mode):
                return None, None, f"{p} is not a directory"
            if name == ".git":
                repos.append(t)
                continue
            keep.append(name)
        dirs[:] = sorted(keep)
        for name in files:
            p = t / name
            if name == ".git":
                gitfiles.append(p)
                continue
            try:
                mode = os.lstat(p).st_mode
            except OSError:
                return None, None, f"{p} cannot be lstat'ed"
            if not stat.S_ISREG(mode):
                return None, None, f"{p} is a special file"
    return repos, gitfiles, None


def _store_ok(target):
    if not pathlib.Path(target).is_dir():
        return False
    try:
        return STORE_ENTRIES <= {q.name for q in pathlib.Path(target).iterdir()}
    except OSError:
        return False


def _meta_target(meta):
    """A linked worktree's metadata dir names the main store in `commondir` (relative to itself)."""
    cd = pathlib.Path(meta) / "commondir"
    if not (pathlib.Path(meta) / "gitdir").is_file() or not cd.is_file():
        return None
    try:
        raw = cd.read_text().strip()
    except OSError:
        return None
    if not raw:
        return None
    return raw if raw.startswith("/") else os.path.join(str(meta), raw)


def _contained(p, d, real):
    if real:
        return _inside(os.path.realpath(str(p)), d)
    return pathlib.Path(p).is_relative_to(d)      # pathlib idiom: no `..` collapse, no symlink following


def check(d, real):
    """None admits; a string refuses. `real=False` is the naive pathlib containment."""
    d = pathlib.Path(d)
    repos, gitfiles, why = _walk(d)
    if why:
        return why
    stores = [r / ".git" for r in repos]
    for gf in gitfiles:
        try:
            line = gf.read_text().strip()
        except OSError:
            return f"{gf} unreadable"
        if not line.startswith("gitdir:"):
            return f"{gf} is not a gitdir line"
        raw = line[len("gitdir:"):].strip()
        if not raw:
            return f"{gf} names no store"
        t = raw if raw.startswith("/") else os.path.join(str(gf.parent), raw)
        if not _contained(t, d, real):
            return f"{gf} names {t}, outside d"
        if _store_ok(t):
            stores.append(pathlib.Path(t))
            continue
        cd = _meta_target(t)
        if cd is None:
            return f"{gf} names neither a store nor worktree metadata: {t}"
        if not _contained(cd, d, real):
            return f"{gf} names a worktree whose commondir {cd} is outside d"
        if not _store_ok(cd):
            return f"{gf} names a worktree whose commondir is not a store"
        stores.append(pathlib.Path(cd))
    for s in stores:
        alt = s / "objects" / "info" / "alternates"
        if not alt.is_file():
            continue
        for line in alt.read_text().splitlines():
            e = line.strip()
            if not e:
                continue
            q = e if e.startswith("/") else os.path.join(str(s / "objects"), e)
            if not _contained(q, d, real):
                return f"alternates entry {e!r} resolves outside d"
            if not pathlib.Path(q).is_dir():
                return f"alternates entry {e!r} is not a directory"
    return None


def breach(d, argv, tool):
    """Correct containment: realpath, then prefix."""
    if not isinstance(argv, list):
        return "argv is not a list"
    return check(d, True)


def naive_breach(d, argv, tool):
    """Naive containment: `pathlib.Path(...).is_relative_to(d)`."""
    if not isinstance(argv, list):
        return "argv is not a list"
    return check(d, False)

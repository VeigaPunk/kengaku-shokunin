"""Round-45 fixture fence (witness): refuse a battery fixture whose git store, discovered repo or argv leaves `d`.

`breach(d, argv, tool)` answers `None` (admit) or a non-empty reason (refuse). `d` is the fixture directory as an
absolute resolved path, `argv` the module's argv, `tool` `anchor` or `order`.

Legs, static first (no subprocess, so no outside file is ever parsed before the verdict):

  a  argv  the tool's options must be written exactly as the contract writes them: an order argv is exactly
           `--lane V --claims V --receipt V`; an anchor argv is `--lane V` plus `--evidence-ref V` / `--verbose`.
           Every value that names a path must resolve inside `d` (no `..`, no absolute path outside).
  b  walk  no symlink under `d` may resolve outside it.
  c  git   a `.git` FILE (`gitdir:` redirect) must name a directory inside `d`; a `.git` DIRECTORY must not
           carry `commondir`, `config.worktree` or `objects/info/alternates`, and no `.git/config*` file may
           carry an `[include]`/`[includeIf]` section or `extensions.worktreeConfig`.
  d  above no `.git` may sit above `d` up to the module build root (`d.parent`): a repo whose work tree is
           above the fixture decides the tool's discovery from inside it.

Then the git legs (bounded: `GIT_CEILING_DIRECTORIES=d.parent`, no stdin, a timeout, no optional locks):
  e  store every repository discovered under `d` must answer `rev-parse --absolute-git-dir` and
           `rev-parse --show-toplevel` with a zero exit status and a path inside `d` (the toplevel exactly the
           repository directory), so `core.worktree`, `core.bare` and an undescribable store are refused;
  f  lane  the `--lane` repository, when it lies inside a repository found under `d`, must answer
           `rev-parse --show-toplevel` the same way. A `--lane` that is no repository at all (and no repository
           above `d`, leg d) stays the tool's own setup error and is admitted.

A git probe that hangs or exits non-zero is a breach, never "nothing to see".
"""
from __future__ import annotations

import os
import pathlib
import re
import subprocess

GIT_TIMEOUT = 30
GIT_ENV = {
    "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "HOME": "/nonexistent",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_TERMINAL_PROMPT": "0",
    "GIT_OPTIONAL_LOCKS": "0",
}
ORDER_SHAPE = ("--lane", "--claims", "--receipt")
ANCHOR_OPTS = {"--lane": True, "--evidence-ref": True, "--verbose": False}
MAX_ENTRIES = 200000
GITFILE_RE = re.compile(r"^\s*gitdir:\s*(.+?)\s*$")


def _inside(p, d):
    return p == d or p.is_relative_to(d)


def _git(cwd, *args, ceiling):
    """One bounded git call: no stdin, a timeout, discovery capped at `ceiling`. None when it could not answer."""
    env = dict(GIT_ENV, GIT_CEILING_DIRECTORIES=str(ceiling))
    try:
        r = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, env=env,
                           stdin=subprocess.DEVNULL, timeout=GIT_TIMEOUT)
    except (subprocess.TimeoutExpired, OSError):
        return None
    return r.returncode, r.stdout.strip()


def _argv_value_ok(tok, d):
    """A path a module hands the tool must stay inside the fixture (a bare word resolves under `d`)."""
    base = pathlib.Path(tok) if tok.startswith("/") else d / tok
    try:
        return _inside(base.resolve(), d)
    except (OSError, RuntimeError):
        return False


def argv_breach(d, argv, tool):
    if tool not in ("anchor", "order"):
        return f"unknown tool {tool!r}"
    if tool == "order":
        if len(argv) != 6 or tuple(argv[0::2]) != ORDER_SHAPE:
            return f"order argv is not the contract shape {list(ORDER_SHAPE)}: {argv}"
        values = argv[1::2]
    else:
        if not argv or argv[0] != "--lane":
            return f"anchor argv does not open with --lane: {argv}"
        values, k = [], 0
        while k < len(argv):
            tok = argv[k]
            if tok not in ANCHOR_OPTS:
                return f"anchor argv token {tok!r} is not an exact option"
            if ANCHOR_OPTS[tok]:
                if k + 1 >= len(argv):
                    return f"anchor option {tok} has no value"
                values.append(argv[k + 1])
                k += 2
            else:
                k += 1
    for v in values:
        if not _argv_value_ok(v, d):
            return f"argv path {v!r} leaves the fixture"
    return None


def _config_breach(gd, d, top):
    """`.git/config*` text legs: an include (any target), or a second config file, is refused unread."""
    for p in sorted(gd.iterdir()):
        if p.name == "config.worktree":
            return f"{top}/.git/config.worktree present (extensions.worktreeConfig include)"
        if not p.name.startswith("config") or not p.is_file():
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace").lower()
        except OSError:
            return f"{p} is unreadable"
        if "[include" in text:
            return f"{top}/.git/{p.name} carries an include section"
        if "worktreeconfig" in text:
            return f"{top}/.git/{p.name} enables extensions.worktreeConfig"
    return None


def static_breach(d):
    """Legs b, c: the tree walk, the `.git` store, the config text. Returns (reason, repos, gitfiles)."""
    repos, links = [], []
    seen = 0
    for top, dirs, files in os.walk(d):
        seen += len(dirs) + len(files)
        if seen > MAX_ENTRIES:
            return "fixture tree exceeds the entry bound", [], []
        here = pathlib.Path(top)
        for name in sorted(dirs) + sorted(files):
            p = here / name
            if p.is_symlink():
                try:
                    target = p.resolve()
                except OSError:
                    return f"symlink {p.name} cannot be resolved", [], []
                if not _inside(target, d):
                    return f"symlink {p.relative_to(d)} -> {os.readlink(p)} leaves the fixture", [], []
        if ".git" in files:
            p = here / ".git"
            try:
                m = GITFILE_RE.match(p.read_text(encoding="utf-8", errors="replace"))
            except OSError:
                return f"{p.relative_to(d)} is unresolvable", [], []
            if not m:
                return f"{p.relative_to(d)} is a file without a gitdir line", [], []
            tgt = pathlib.Path(m.group(1))
            tgt = (tgt if tgt.is_absolute() else here / tgt)
            try:
                tgt = tgt.resolve()
            except OSError:
                return f"{p.relative_to(d)} gitdir cannot be resolved", [], []
            if not _inside(tgt, d):
                return f"{p.relative_to(d)} gitdir {tgt} leaves the fixture", [], []
            repos.append(here)
        if ".git" in dirs:
            gd = here / ".git"
            if gd.is_symlink():
                return f"{here.relative_to(d)}/.git is a symlink", [], []
            if (gd / "commondir").exists():
                return f"{here.relative_to(d)}/.git/commondir present (store beside the fixture)", [], []
            if (gd / "objects" / "info" / "alternates").exists():
                return f"{here.relative_to(d)}/.git/objects/info/alternates present", [], []
            why = _config_breach(gd, d, here.relative_to(d))
            if why:
                return why, [], []
            repos.append(here)
        dirs[:] = [x for x in dirs if x != ".git"]
    return None, sorted(set(repos)), []


def above_breach(d):
    """Leg d: the module build root (d.parent) is the last ancestor a fixture may see a store from."""
    p = d.parent
    if p != d:
        for name in (".git",):
            cand = p / name
            if cand.is_symlink() or cand.exists():
                return f"a repository sits above the fixture at {p} ({name})"
    return None


def git_breach(d, repos, argv):
    """Legs e, f: bounded probes; a non-zero status or a path outside `d` refuses."""
    ceiling = d.parent
    for repo in repos:
        repo = repo.resolve()
        got = _git(repo, "rev-parse", "--absolute-git-dir", ceiling=ceiling)
        if got is None:
            return f"{repo.name}: git rev-parse --absolute-git-dir did not answer"
        rc, out = got
        if rc != 0:
            return f"{repo.name}: git rev-parse --absolute-git-dir failed rc={rc}"
        try:
            p = pathlib.Path(out).resolve()
        except OSError:
            return f"{repo.name}: git dir {out} cannot be resolved"
        if not _inside(p, d):
            return f"{repo.name}: git dir {p} leaves the fixture"
        got = _git(repo, "rev-parse", "--show-toplevel", ceiling=ceiling)
        if got is None:
            return f"{repo.name}: git rev-parse --show-toplevel did not answer (undescribable store)"
        rc, out = got
        if rc != 0:
            return f"{repo.name}: git rev-parse --show-toplevel failed rc={rc} (undescribable store)"
        try:
            p = pathlib.Path(out).resolve()
        except OSError:
            return f"{repo.name}: toplevel {out} cannot be resolved"
        if p != repo or not _inside(p, d):
            return f"{repo.name}: toplevel {p} is not the fixture repository"
    lane = None
    try:
        vals = dict(zip(argv[0::2], argv[1::2]))
    except (TypeError, ValueError):
        vals = {}
    if "--lane" in vals:
        lane = pathlib.Path(vals["--lane"])
        lane = (lane if lane.is_absolute() else d / lane)
        try:
            lane = lane.resolve()
        except OSError:
            return None
        if lane.is_dir() and any(_inside(lane, r) for r in repos):
            got = _git(lane, "rev-parse", "--show-toplevel", ceiling=ceiling)
            if got is None:
                return f"--lane {lane.name}: git rev-parse --show-toplevel did not answer"
            rc, out = got
            if rc != 0:
                return f"--lane {lane.name}: git rev-parse --show-toplevel failed rc={rc}"
            try:
                p = pathlib.Path(out).resolve()
            except OSError:
                return f"--lane {lane.name}: toplevel {out} cannot be resolved"
            if not _inside(p, d):
                return f"--lane {lane.name}: toplevel {p} leaves the fixture"
    return None


def breach(d, argv, tool):
    try:
        d = pathlib.Path(d).resolve()
        argv = [str(a) for a in (argv or [])]
        if not d.is_dir():
            return f"fixture directory {d} does not exist"
        why = argv_breach(d, argv, tool)
        if why:
            return why
        why, repos, _files = static_breach(d)
        if why:
            return why
        why = above_breach(d)
        if why:
            return why
        return git_breach(d, repos, argv)
    except (OSError, ValueError, RuntimeError) as exc:
        return f"fence could not decide: {exc}"

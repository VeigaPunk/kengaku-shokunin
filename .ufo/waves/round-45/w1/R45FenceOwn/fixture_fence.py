#!/usr/bin/env python3
"""Round-45 fixture fence: the advertised fence, implemented once.

Contract (`plans/round45_c1_verify.py` is the frozen rule)::

    breach(d: pathlib.Path, argv: list[str], tool: str) -> str | None

`d` is the fixture directory (absolute, resolved), `argv` the module's argv (tokens relative to `d` or
absolute inside it), `tool` is `anchor` or `order`. A non-empty one-line string refuses the fixture, `None`
admits it. The fence runs with cwd `d`, inside a read-only sandbox, under `strace -f -y`; the counter counts
every successful (or never-returned) open of a path under the build scratch that is not under `d`.

Leg order, and why it is that order:

  1. `_argv_shape` — pure syntax, no filesystem. First, because every later leg consumes the argv: an
     abbreviated order argv (`--claim`, `--receip`) must be refused by the shape leg, never turned into a
     `KeyError` in a leg that reads `--claims` (round 44's `order_argv_breach` crashed that way, which the
     builder reports as a build error rather than a refusal).
  2. `_walk` — one pass over `d`, no depth cap, no descent into `.git`. A `.git` FILE is a `gitdir:`
     redirect and is refused; a symlink that resolves outside `d` is refused (r44 leg h); a tree over
     200000 entries is refused rather than silently skipped.
  3. `_store_fs` — per repo found under `d`, by text and by `stat` only: `.git/commondir` (f7), a
     `.git/config.worktree` file or a `.git/config*` carrying `[include]`/`[includeIf]`/`include.path`/
     `extensions.worktreeConfig` (f4, f8, f10), `.git/objects/info/alternates` (f5). These are the legs that
     must decide BEFORE any git child runs: git parses the repo config (and honours `commondir`) on every
     invocation, so a git-first order opens a FIFO include, a sibling store or a regular include target
     outside `d` — that is exactly what made round 44's fence READ f4/f10 while refusing them.
  4. `_ancestor_breach` — a `.git` above `d`, among the ancestors up to this build's module root (the
     fixture directory's parent, and the counter's `fx/` level above it, both created by the counter, never
     by a module): f6's repo sits at `d.parent`. `stat` only, so nothing above `d` is opened.
  5. git legs, second tier, every call bounded (`GIT_CEILING_DIRECTORIES` at `d.parent`, a 10 s per-call
     timeout inside a 45 s overall budget — so the counter's own 120 s fence verdict is unreachable by a
     hung probe — at most 64 stores per fixture, no stdin, `PATH` without any per-user bin, config pins that
     neutralise fsmonitor/hooks/gpg/pager):
     `rev-parse --absolute-git-dir`, `rev-parse --show-toplevel`, `config --local --no-includes --get
     core.worktree` per repo, and for an order argv `cat-file -t HEAD:<claims|receipt>`. A non-zero rc from
     a store or lane probe is unverifiable and therefore a breach, never "clean" (f9's bare repo: `rev-parse
     --show-toplevel` exits non-zero, and a fence that guards on `rc == 0` admits it).

No leg raises: each returns a one-line reason or `None`, and `breach` has a last-resort guard so a malformed
fixture (say a `.git/config` full of continuation lines) becomes a refusal instead of a crash.
"""
from __future__ import annotations

import os
import pathlib
import stat
import subprocess
import time

TOOLS = frozenset(("anchor", "order"))
ORDER_SHAPE = ("--lane", "--claims", "--receipt")
ANCHOR_VALUE = frozenset(("--lane", "--evidence-ref"))
ANCHOR_FLAG = frozenset(("--verbose",))
MAX_ENTRIES = 200000
MAX_REPOS = 64
MAX_CONFIG_BYTES = 1 << 20
GIT_TIMEOUT = 10
GIT_BUDGET = 45
PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
GIT_ENV = {
    "PATH": PATH, "HOME": "/nonexistent", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
    "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_COUNT": "4",
    "GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_VALUE_0": "false",
    "GIT_CONFIG_KEY_1": "core.hooksPath", "GIT_CONFIG_VALUE_1": "/dev/null",
    "GIT_CONFIG_KEY_2": "gpg.program", "GIT_CONFIG_VALUE_2": "/bin/true",
    "GIT_CONFIG_KEY_3": "log.showSignature", "GIT_CONFIG_VALUE_3": "false",
}


# --- 1. argv syntax -------------------------------------------------------------------------------------

def _argv_shape(tool, argv):
    """The argv must be the tool's contract shape, spelled with exact option names."""
    if tool not in TOOLS:
        return f"tool {tool!r} is neither anchor nor order"
    if not isinstance(argv, list) or not all(type(t) is str for t in argv):
        return "argv is not a list of strings"
    if tool == "order":
        if len(argv) != 6 or tuple(argv[0::2]) != ORDER_SHAPE:
            return f"order argv is not the contract shape {list(ORDER_SHAPE)}: {argv}"
        for k in (1, 3, 5):
            if not argv[k]:
                return f"order argv carries an empty {argv[k - 1]} value"
        return None
    k, lane = 0, False
    while k < len(argv):
        tok = argv[k]
        if tok in ANCHOR_VALUE:
            if k + 1 >= len(argv):
                return f"anchor argv option {tok} has no value: {argv}"
            if not argv[k + 1]:
                return f"anchor argv carries an empty {tok} value"
            lane = lane or tok == "--lane"
            k += 2
        elif tok in ANCHOR_FLAG:
            k += 1
        else:
            return f"anchor argv token {tok!r} is not an exact option"
    if not lane:
        return f"anchor argv carries no --lane: {argv}"
    return None


def _value(argv, opt):
    """The value of `opt` in an already-shape-checked argv."""
    try:
        return argv[argv.index(opt) + 1]
    except (ValueError, IndexError):
        return None


def _values(argv):
    return {argv[k]: argv[k + 1] for k in range(0, len(argv) - 1, 2)}


# --- 2/3/4. filesystem legs (stat and text only) --------------------------------------------------------

def _within(p, d):
    try:
        return pathlib.Path(p).is_relative_to(d)
    except (OSError, ValueError):
        return False


def _rel(p, d):
    r = os.path.relpath(p, d)
    return "" if r == "." else r + "/"


def _walk(d):
    """One pass over `d`: (repos, None) or (None, reason). Never opens a path outside `d`."""
    repos, entries = [], 0
    for top, dirnames, filenames in os.walk(d, followlinks=False):
        for name in list(dirnames) + list(filenames):
            entries += 1
            if entries > MAX_ENTRIES:
                return None, f"fixture tree exceeds {MAX_ENTRIES} entries"
            p = os.path.join(top, name)
            if os.path.islink(p):
                try:
                    target = os.path.realpath(p)
                except OSError:
                    target = ""
                if not _within(target, d):
                    try:
                        shown = os.readlink(p)
                    except OSError:
                        shown = "?"
                    return None, f"symlink {os.path.relpath(p, d)} -> {shown} leaves the fixture"
        if ".git" in filenames:
            return None, f"{_rel(top, d)}.git is a file (gitdir redirect), not a directory"
        if ".git" in dirnames:
            repos.append(pathlib.Path(top))
            dirnames.remove(".git")
    return repos, None


def _config_files(gd):
    """Every `.git/config*` of a store, and of each linked worktree, by name: (list, None) or (None, reason)."""
    out = []
    try:
        with os.scandir(gd) as it:
            entries = list(it)
    except OSError as e:
        return None, f"{gd.name} store cannot be listed ({e.strerror})"
    for e in entries:
        if e.name.startswith("config"):
            out.append(pathlib.Path(e.path))
        elif e.name == "worktrees" and e.is_dir(follow_symlinks=False):
            try:
                with os.scandir(e.path) as it2:
                    subs = [x for x in it2 if x.is_dir(follow_symlinks=False)]
            except OSError:
                continue
            for sub in subs:
                try:
                    with os.scandir(sub.path) as it3:
                        out.extend(pathlib.Path(x.path) for x in it3 if x.name.startswith("config"))
                except OSError:
                    continue
    return out, None


def _config_breach(cfg, rel):
    """One config file: refuse an include surface, a worktree-config surface, or anything unreadable."""
    if cfg.name == "config.worktree":
        return f"{rel}{cfg.name} present (worktree-config include surface)"
    try:
        st = cfg.lstat()
    except OSError as e:
        return f"{rel}{cfg.name} cannot be examined ({e.strerror})"
    if not stat.S_ISREG(st.st_mode):
        return f"{rel}{cfg.name} is not a regular file"
    if st.st_size > MAX_CONFIG_BYTES:
        return f"{rel}{cfg.name} exceeds {MAX_CONFIG_BYTES} bytes"
    try:
        text = cfg.read_text(errors="replace")
    except OSError as e:
        return f"{rel}{cfg.name} cannot be read ({e.strerror})"
    section = ""
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line[0] in "#;":
            continue
        if line.startswith("["):
            end = line.find("]")
            section = line[1:end].strip().lower() if end > 0 else ""
            if section.startswith("include"):
                return f"{rel}{cfg.name} carries a [{section.split()[0]}] section"
            continue
        key = line.split("=", 1)[0].strip().lower()
        if key.startswith("include.") or key.startswith("includeif."):
            return f"{rel}{cfg.name} carries a {key} key"
        if key == "extensions.worktreeconfig" or (section == "extensions" and key == "worktreeconfig"):
            return f"{rel}{cfg.name} enables extensions.worktreeConfig"
    return None


def _store_fs(repo, d):
    """One repository under `d`: store redirects, borrows and include surfaces, without running git."""
    rel = _rel(repo, d)
    gd = repo / ".git"
    if gd.is_symlink():
        return f"{rel}.git is a symlink"
    if os.path.lexists(gd / "commondir"):
        return f"{rel}.git/commondir present (store redirected outside the fixture)"
    if os.path.lexists(gd / "objects" / "info" / "alternates"):
        return f"{rel}.git/objects/info/alternates present (objects borrowed)"
    configs, reason = _config_files(gd)
    if reason:
        return f"{rel}{reason}"
    for cfg in configs:
        reason = _config_breach(cfg, rel)
        if reason:
            return reason
    return None


def _ancestor_breach(d):
    """A `.git` above `d`: the fixture parent (module build root) and the counter's `fx/` level above it."""
    cur = d.parent
    for _ in range(2):
        if cur == cur.parent:
            break
        try:
            present = os.path.lexists(cur / ".git")
        except OSError:
            present = False
        if present:
            return f"a git store sits above the fixture at {cur / '.git'}"
        cur = cur.parent
    return None


# --- 5. bounded git legs --------------------------------------------------------------------------------

def _pin_git(repo, args, ceiling, deadline):
    """(rc, stdout) or None on a timeout/OS error/budget exhaustion: ceiling, timeout, no stdin, pinned config."""
    if time.monotonic() > deadline:
        return None
    env = dict(GIT_ENV)
    env["GIT_CEILING_DIRECTORIES"] = str(ceiling)
    try:
        r = subprocess.run(["git", "--no-pager", "-C", str(repo), *args], capture_output=True, text=True,
                           env=env, stdin=subprocess.DEVNULL,
                           timeout=max(1.0, min(GIT_TIMEOUT, deadline - time.monotonic())))
    except (subprocess.TimeoutExpired, OSError):
        return None
    return r.returncode, r.stdout.strip()


def _store_git(repo, d, ceiling, deadline):
    """A store that git cannot describe, or that describes something outside `d`, is a breach."""
    rel = _rel(repo, d)
    got = _pin_git(repo, ("rev-parse", "--absolute-git-dir"), ceiling, deadline)
    if got is None:
        return f"{rel}git store probe hung"
    if got[0] != 0:
        return f"{rel}git cannot name the store (rc={got[0]})"
    if not _within(got[1], d):
        return f"{rel}git dir {got[1]} is outside the fixture"
    got = _pin_git(repo, ("rev-parse", "--show-toplevel"), ceiling, deadline)
    if got is None:
        return f"{rel}git work tree probe hung"
    if got[0] != 0:
        return f"{rel}git cannot describe the work tree (rc={got[0]})"
    try:
        top_ok = pathlib.Path(got[1]).resolve() == repo.resolve()
    except OSError:
        top_ok = False
    if not top_ok:
        return f"{rel}work tree {got[1]} is not the repository directory"
    got = _pin_git(repo, ("config", "--local", "--no-includes", "--get", "core.worktree"), ceiling, deadline)
    if got is None:
        return f"{rel}git config probe hung"
    if got[0] == 0 and got[1]:
        wt = pathlib.Path(got[1])
        if not wt.is_absolute():
            wt = repo / wt
        try:
            wt_ok = wt.resolve() == repo.resolve()
        except OSError:
            wt_ok = False
        if not wt_ok:
            return f"{rel}core.worktree={got[1]} leaves the repository"
    return None


def _lane_repo(d, lane_val):
    """The repository `--lane` adopts: (repo, None) or (None, reason). Never ascends above `d`."""
    lane = pathlib.Path(lane_val)
    lane = lane if lane.is_absolute() else d / lane_val
    try:
        lane = lane.resolve()
    except OSError:
        return None, f"--lane {lane_val} cannot be resolved"
    if not _within(lane, d):
        return None, f"--lane {lane_val} leaves the fixture"
    if not lane.is_dir():
        return None, f"--lane {lane_val} is not a directory inside the fixture"
    cur = lane
    while True:
        if os.path.lexists(cur / ".git"):
            return cur, None
        if cur == d:
            return None, f"--lane {lane_val} names no repository inside the fixture"
        cur = cur.parent


def _order_git(repo, vals, ceiling, deadline):
    """An order argv names blobs at HEAD: a directory or missing object is not a blob (a missing path is the
    tool's own setup error, so a non-zero rc here is left to the tool)."""
    for opt in ("--claims", "--receipt"):
        val = vals[opt]
        if ".." in pathlib.PurePosixPath(val).parts:
            return f"{opt} {val} leaves the repository"
        got = _pin_git(repo, ("cat-file", "-t", f"HEAD:{val}"), ceiling, deadline)
        if got is None:
            return f"{opt} git probe hung"
        if got[0] == 0 and got[1] != "blob":
            return f"{opt} {val} is a {got[1]} at HEAD, not a blob"
    return None


# --- entry point ----------------------------------------------------------------------------------------

def breach(d, argv, tool):
    """A one-line refusal reason, or None to admit the fixture."""
    try:
        d = pathlib.Path(d).resolve()
    except (OSError, RuntimeError):
        return "fixture directory cannot be resolved"
    try:
        reason = _argv_shape(tool, argv)
        if reason:
            return reason
        if not d.is_dir():
            return "fixture directory is not a directory"
        repos, reason = _walk(d)
        if reason:
            return reason
        for repo in repos:
            reason = _store_fs(repo, d)
            if reason:
                return reason
        reason = _ancestor_breach(d)
        if reason:
            return reason
        if len(repos) > MAX_REPOS:
            return f"fixture holds {len(repos)} git stores, over the {MAX_REPOS} bound"
        ceiling = d.parent
        deadline = time.monotonic() + GIT_BUDGET
        for repo in repos:
            reason = _store_git(repo, d, ceiling, deadline)
            if reason:
                return reason
        lane_val = _value(argv, "--lane")
        if lane_val is None:
            return "argv carries no --lane value"
        lane_repo, reason = _lane_repo(d, lane_val)
        if reason:
            return reason
        if tool == "order":
            reason = _order_git(lane_repo, _values(argv), ceiling, deadline)
            if reason:
                return reason
        return None
    except Exception as e:  # a leg must never turn a refusal into a crash
        return f"fence internal error: {type(e).__name__}: {e}"

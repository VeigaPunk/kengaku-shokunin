"""Round-45 fixture fence (variant B): refuse a fixture whose git store, discovered repo or argv leaves
its directory. Pure-filesystem legs run first — nothing outside `d` is ever opened while deciding — then
bounded git legs run under GIT_CEILING_DIRECTORIES=d.parent; a probe that fails, times out or answers
outside `d` is a breach, never a "clean".

breach(d, argv, tool) -> str | None   (round45_c1_verify.py harness: cwd=d, strace -f -y, read-only sandbox)
"""
import os
import pathlib
import re
import subprocess

_TIMEOUT = 15
_ENV = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "HOME": "/nonexistent",
        "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_COUNT": "4", "GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_VALUE_0": "false",
        "GIT_CONFIG_KEY_1": "core.hooksPath", "GIT_CONFIG_VALUE_1": "/dev/null",
        "GIT_CONFIG_KEY_2": "gpg.program", "GIT_CONFIG_VALUE_2": "/bin/true",
        "GIT_CONFIG_KEY_3": "log.showSignature", "GIT_CONFIG_VALUE_3": "false"}
_ANCHOR_OPTS = {"--lane": 1, "--evidence-ref": 1, "--verbose": 0}
_INCLUDE_RE = re.compile(r"(?im)^\s*(\[include|include(if)?\.path\s*=|worktreeconfig\s*=)")

def _git(repo, *args, ceiling):
    """One bounded git call: ceiling discovery, 15 s timeout, no stdin. (rc, out) or (None, "hung")."""
    try:
        r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                           stdin=subprocess.DEVNULL, timeout=_TIMEOUT,
                           env={**_ENV, "GIT_CEILING_DIRECTORIES": str(ceiling)})
    except subprocess.TimeoutExpired:
        return None, "hung"
    return r.returncode, r.stdout.strip()


def _inside(tok, d):
    """Every argv token must resolve inside d (absolute inside it or relative to it)."""
    try:
        return os.path.realpath(tok if tok.startswith("/") else d / tok).startswith(str(d) + os.sep) \
            or os.path.realpath(tok if tok.startswith("/") else d / tok) == str(d)
    except OSError:
        return False


def _store_bad(gd, d):
    """Static per-.git checks, all lstat/read under d: no symlink, commondir, config.worktree, include
    surface, alternates, and every config* a plain regular file before any git call is trusted."""
    if os.path.islink(gd):
        return f"{os.path.relpath(gd, d)} is a symlink"
    for name, bad in (("commondir", ".git/commondir present"),
                      ("config.worktree", ".git/config.worktree present"),
                      ("objects/info/alternates", ".git/objects/info/alternates present")):
        if os.path.lexists(gd / name):
            return f"{os.path.relpath(gd.parent, d)}/{bad}"
    for cfg in sorted(gd.glob("config*")):
        if os.path.islink(cfg) or not cfg.is_file():
            return f"{os.path.relpath(cfg, d)} is not a regular file"
        try:
            if cfg.stat().st_size > 1 << 20:
                return f"{os.path.relpath(cfg, d)} exceeds 1 MiB"
            if _INCLUDE_RE.search(cfg.read_text(errors="replace")):
                return f"{os.path.relpath(cfg, d)} carries an include or worktreeConfig"
        except OSError as e:
            return f"{os.path.relpath(cfg, d)} unreadable ({e.strerror or e})"
    return None


def _static(d):
    """Walk the whole fixture tree: no escaping symlink, no .git file/symlink/redirect, no repo at the
    module build root, per-.git store checks before any git call. Returns (reason|None, [repo dirs])."""
    repos, n = [], 0
    for top, dirs, files in os.walk(d):
        n += len(dirs) + len(files)
        if n > 200000:
            return "fixture tree exceeds 200000 entries", repos
        in_store = ".git" in os.path.relpath(top, d).split(os.sep)
        for name in dirs + files:
            p = os.path.join(top, name)
            if os.path.islink(p):
                if name == ".git":
                    return f"{os.path.relpath(p, d)} is a symlink", repos
                try:
                    if not os.path.realpath(p).startswith(str(d) + os.sep):
                        return f"symlink {os.path.relpath(p, d)} escapes the fixture", repos
                except OSError:
                    return f"symlink {os.path.relpath(p, d)} unresolvable", repos
            elif name == ".git":
                if not os.path.isdir(p):
                    return f"{os.path.relpath(p, d)} is not a directory (gitdir redirect)", repos
                if not in_store:
                    repos.append(pathlib.Path(top))
        dirs.sort()
    if os.path.lexists(d.parent / ".git"):
        return ".git at the module build root (repo above the fixture)", repos
    for repo in repos:
        bad = _store_bad(repo.resolve() / ".git", d)
        if bad:
            return bad, repos
    return None, repos


def _repo_legs(d, repo):
    """Bounded git legs for one repo: the store must sit inside d, the worktree must be the repo, a probe
    that cannot answer is unverifiable."""
    for args, what, ok in ((("rev-parse", "--show-toplevel"), "--show-toplevel", lambda p: p == repo),
                           (("rev-parse", "--absolute-git-dir"), "--absolute-git-dir",
                            lambda p: p.is_relative_to(d))):
        rc, out = _git(repo, *args, ceiling=d.parent)
        if rc is None:
            return f"{repo.name}/git hung on rev-parse {what}"
        if rc != 0:
            return f"{repo.name}/rev-parse {what} unanswerable (rc={rc})"
        if not ok(pathlib.Path(out).resolve()):
            return f"{repo.name}/rev-parse {what}={out} leaves the fixture"
    rc, out = _git(repo, "config", "--local", "--no-includes", "--get", "core.worktree", ceiling=d.parent)
    if rc is None:
        return f"{repo.name}/git hung on core.worktree"
    if rc == 0 and out:
        p = pathlib.Path(out)
        if (p if p.is_absolute() else repo / p).resolve() != repo:
            return f"{repo.name}/core.worktree={out}"
    return None


def breach(d, argv, tool):
    d = pathlib.Path(d).resolve()
    if tool == "order":
        if len(argv) != 6 or tuple(argv[0::2]) != ("--lane", "--claims", "--receipt"):
            return f"order argv is not the contract shape: {argv}"
        vals = dict(zip(argv[0::2], argv[1::2]))
    elif tool == "anchor":
        vals, k = {}, 0
        while k < len(argv):
            t = argv[k]
            if t not in _ANCHOR_OPTS:
                return f"anchor argv token {t!r} is not an exact option"
            if _ANCHOR_OPTS[t]:
                if k + 1 >= len(argv):
                    return f"anchor argv ends at option {t!r}"
                vals[t] = argv[k + 1]
            k += 2 if _ANCHOR_OPTS[t] else 1
    else:
        return f"unknown tool {tool!r}"
    for t in argv:
        if not _inside(t, d):
            return f"argv token {t!r} resolves outside the fixture"
    bad, repos = _static(d)
    if bad:
        return bad
    if "--lane" in vals:
        lp = pathlib.Path(vals["--lane"])
        lp = lp.resolve() if lp.is_absolute() else (d / lp).resolve()
        for args, what in ((("rev-parse", "--show-toplevel"), "--show-toplevel"),
                           (("rev-parse", "--absolute-git-dir"), "--absolute-git-dir")):
            rc, out = _git(lp, *args, ceiling=d.parent)
            if rc is None:
                return f"--lane git hung on {what}"
            if rc != 0:
                return f"--lane rev-parse {what} unanswerable (rc={rc})"
            if not pathlib.Path(out).resolve().is_relative_to(d):
                return f"--lane rev-parse {what}={out} is outside the fixture"
        if tool == "order":
            for opt in ("--claims", "--receipt"):
                rc, out = _git(lp, "cat-file", "-t", f"HEAD:{vals[opt]}", ceiling=d.parent)
                if rc is None:
                    return f"{opt} git hung"
                if rc != 0 or out != "blob":
                    return f"{opt} {vals[opt]} is not a blob at HEAD"
    for repo in repos:
        bad = _repo_legs(d, repo.resolve())
        if bad:
            return bad
    return None

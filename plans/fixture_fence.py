"""Fixture fence (round-45 C1): admit only a fixture whose git store, discovered repos and argv stay inside `d`.

Contract (frozen, `plans/round45_c1_verify.py` docstring):

    breach(d: pathlib.Path, argv: list[str], tool: str) -> str | None

`d` is the fixture directory (absolute, resolved), `argv` the module's argv tail, `tool` `anchor` or `order`.
A non-empty string refuses (the reason, one line); None admits. Runs with cwd `d`, read-only, under
`strace -f -y`, so the fence's whole process tree must never open a path under the build scratch outside `d`.

Structure (variant A): COLLECT FIRST, git LAST. One sweep gathers every filesystem fact the decision can need
(argv shape, argv path values, `.git` above `d`, the full tree walk, every collected repo's store markers and
the text of every `.git/config*`) and judges all of it before a single git child exists. Only after the tree is
proven self-contained does the fence trust git to answer, and then only through `_git`, which pins a fixed
system PATH, an empty HOME, `GIT_CONFIG_NOSYSTEM`/`GIT_CONFIG_GLOBAL=/dev/null`, the executable-key pins, a
`GIT_CEILING_DIRECTORIES` at the module build root (`d.parent`), a 30 s timeout and no stdin. Any rc != 0 from a
store or lane probe means git could not verify the fixture and is a breach, never "clean".
"""
import os
import pathlib
import re
import stat
import subprocess

GIT_TIMEOUT = 30
ENTRY_CAP = 200000          # walked entries before the tree itself is refused as pathological
REPO_CAP = 64               # collected repos before the fixture is refused as pathological
CONFIG_CAP = 1 << 20        # a `.git/config*` file larger than this is refused unread

ORDER_SHAPE = ("--lane", "--claims", "--receipt")
ANCHOR_OPTS = {"--lane": True, "--evidence-ref": True, "--verbose": False}

_PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
GIT_ENV = {
    "PATH": _PATH,
    "HOME": "/nonexistent",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_COUNT": "4",
    "GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_VALUE_0": "false",
    "GIT_CONFIG_KEY_1": "core.hooksPath", "GIT_CONFIG_VALUE_1": "/dev/null",
    "GIT_CONFIG_KEY_2": "gpg.program", "GIT_CONFIG_VALUE_2": "/bin/true",
    "GIT_CONFIG_KEY_3": "log.showSignature", "GIT_CONFIG_VALUE_3": "false",
}
_INCLUDE_RE = re.compile(r"^[ \t]*\[[ \t]*include", re.IGNORECASE | re.MULTILINE)
_SECTION_RE = re.compile(r"\[\s*([A-Za-z0-9_.-]+)")


def _inside(p, d):
    """Resolved path inside (or equal to) the fixture dir?"""
    try:
        p = pathlib.Path(p).resolve()
    except OSError:
        return False
    return p == d or p.is_relative_to(d)


def _git(repo, ceiling, *args):
    """One bounded parent-side git call: fixed env, no stdin, 30 s, discovery capped at `ceiling`.
    Returns (rc, stdout) or None on timeout."""
    env = dict(GIT_ENV, GIT_CEILING_DIRECTORIES=str(ceiling))
    try:
        r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, env=env,
                           stdin=subprocess.DEVNULL, timeout=GIT_TIMEOUT)
    except subprocess.TimeoutExpired:
        return None
    except OSError:
        return (-1, "")
    return r.returncode, r.stdout.strip()


# ---------- collection pass (pure filesystem, no git child may exist yet) ----------


def _collect(d, tool, argv):
    """Gather every filesystem fact about the fixture and judge it. Returns (breach, repos, lane):
    breach is a reason string or None; repos the list of directories holding a `.git` dir inside d;
    lane the resolved `--lane` directory or None."""
    # fact 1: argv must be the tool's contract shape, so no abbreviation or `--opt=value` can smuggle a
    # second option past the legs below.
    vals = {}
    if tool == "order":
        if len(argv) != 6 or tuple(argv[0::2]) != ORDER_SHAPE:
            return f"order argv is not the contract shape {list(ORDER_SHAPE)}", None, None
        vals = dict(zip(argv[0::2], argv[1::2]))
    elif tool == "anchor":
        k = 0
        while k < len(argv):
            t = argv[k]
            if t not in ANCHOR_OPTS:
                return f"anchor argv token {t!r} is not an exact option", None, None
            if ANCHOR_OPTS[t]:
                vals[t] = argv[k + 1] if k + 1 < len(argv) else ""
                k += 2
            else:
                vals[t] = True
                k += 1
    else:
        return f"unknown tool {tool!r}", None, None

    # fact 2: every argv value that is a path must resolve inside d (a `{...}` placeholder is the
    # counter's own per-run token and is resolved by the harness, not here).
    for opt, val in vals.items():
        if val is True or not isinstance(val, str) or val.startswith("{"):
            continue
        cand = pathlib.Path(val) if val.startswith("/") else d / val
        if not _inside(cand, d):
            return f"{opt} value {val!r} resolves outside the fixture", None, None

    # fact 3: no `.git` may sit ABOVE d up to the module build root (the fixture dir's parent): a repo
    # there is what git discovery would adopt from a `--lane` that is a plain directory inside d.
    anc = d.parent
    while True:
        if os.path.lexists(anc / ".git"):
            return f".git exists at {anc} above the fixture", None, None
        if anc == d.parent or anc.parent == anc:
            break
        anc = anc.parent

    # fact 4: one walk of the whole fixture tree — `.git` files, `.git` symlink dirs, escaping symlinks,
    # and non-regular special files — collecting every directory that holds a real `.git` directory.
    repos, seen = [], 0
    for top, dirs, files in os.walk(d):
        seen += len(dirs) + len(files)
        if seen > ENTRY_CAP:
            return f"fixture tree exceeds {ENTRY_CAP} entries", None, None
        top = pathlib.Path(top)
        for name in dirs:
            p = top / name
            if name == ".git":
                if p.is_symlink():
                    return f"{p.relative_to(d)}/.git is a symlink", None, None
                repos.append(p.parent.resolve())
                continue
            if p.is_symlink() and not _inside(p, d):
                return f"symlink {p.relative_to(d)} -> {os.readlink(p)} leaves the fixture", None, None
        for name in files:
            p = top / name
            if name == ".git":
                return f"{p.relative_to(d)}/.git is a file (gitdir redirect), not a directory", None, None
            if p.is_symlink():
                if not _inside(p, d):
                    return f"symlink {p.relative_to(d)} -> {os.readlink(p)} leaves the fixture", None, None
            else:
                try:
                    mode = p.lstat().st_mode
                except OSError:
                    return f"{p.relative_to(d)} cannot be stat'ed", None, None
                if stat.S_ISFIFO(mode) or stat.S_ISSOCK(mode) or stat.S_ISBLK(mode) or stat.S_ISCHR(mode):
                    return f"{p.relative_to(d)} is a special file", None, None
        dirs[:] = sorted(x for x in dirs if x != ".git")
    if len(repos) > REPO_CAP:
        return f"fixture holds more than {REPO_CAP} repos", None, None

    # fact 5: every collected repo's store must be ordinary and self-contained — commondir redirect,
    # alternates, a second config file, and any include surface in ANY `.git/config*` — judged from the
    # file bytes before git is ever asked, so a hostile include can never be opened by a git child.
    for repo in repos:
        gd = repo / ".git"
        rel = repo.relative_to(d)
        if os.path.lexists(gd / "commondir"):
            return f"{rel}/.git/commondir present (store redirect)", None, None
        if os.path.lexists(gd / "objects" / "info" / "alternates"):
            return f"{rel}/.git/objects/info/alternates present", None, None
        for cfg in sorted(gd.glob("config*")):
            if not cfg.is_file() or cfg.is_symlink():
                return f"{rel}/.git/{cfg.name} is not a regular file", None, None
            try:
                with open(cfg, "rb") as fh:
                    raw = fh.read(CONFIG_CAP + 1)
            except OSError:
                return f"{rel}/.git/{cfg.name} unreadable", None, None
            if len(raw) > CONFIG_CAP:
                return f"{rel}/.git/{cfg.name} exceeds {CONFIG_CAP} bytes", None, None
            text = raw.decode("utf-8", "replace")
            if _INCLUDE_RE.search(text):
                return f"{rel}/.git/{cfg.name} carries an include", None, None
            sect = ""
            for line in text.splitlines():
                s = line.strip()
                if not s or s[0] in "#;":
                    continue
                if s.startswith("["):
                    m = _SECTION_RE.match(s)
                    sect = m.group(1).lower() if m else ""
                    continue
                key, _, val = s.partition("=")
                key = key.strip().lower()
                val = val.strip().strip('"').strip("'")
                if sect == "extensions" and key == "worktreeconfig":
                    return f"{rel}/.git/{cfg.name} enables extensions.worktreeConfig", None, None
                if sect == "core" and key == "bare" and (val == "" or val.lower() == "true"):
                    return f"{rel}/.git/{cfg.name} sets core.bare", None, None
                if sect == "core" and key == "worktree" and val:
                    wt = pathlib.Path(val)
                    wt = wt if wt.is_absolute() else repo / wt
                    if not _inside(wt, d) or wt.resolve() != repo:
                        return f"{rel}/.git/{cfg.name} sets core.worktree={val}", None, None

    lane = vals.get("--lane")
    lane = (pathlib.Path(lane) if str(lane).startswith("/") else d / lane) if isinstance(lane, str) else None
    return None, repos, lane


# ---------- git legs (only reached when the tree is proven self-contained) ----------


def _probe(repo, ceiling, need_root, d):
    """rev-parse the repo: toplevel and git dir must resolve inside d; for a collected repo (need_root)
    the toplevel must BE the repo dir itself. rc != 0 means git could not verify it -> breach."""
    top = _git(repo, ceiling, "rev-parse", "--show-toplevel")
    if top is None:
        return "git hung answering rev-parse --show-toplevel"
    if top[0] != 0:
        return f"git cannot describe the worktree at {repo} (rc={top[0]})"
    p = pathlib.Path(top[1]).resolve()
    if need_root:
        if p != repo:
            return f"rev-parse --show-toplevel={top[1]} is not the repo directory"
    elif not _inside(p, d):
        return f"rev-parse --show-toplevel={top[1]} is outside the fixture"
    gd = _git(repo, ceiling, "rev-parse", "--absolute-git-dir")
    if gd is None:
        return "git hung answering rev-parse --absolute-git-dir"
    if gd[0] != 0:
        return f"git cannot resolve the git dir at {repo} (rc={gd[0]})"
    if not _inside(pathlib.Path(gd[1]), d):
        return f"rev-parse --absolute-git-dir={gd[1]} is outside the fixture"
    wt = _git(repo, ceiling, "config", "--local", "--no-includes", "--get", "core.worktree")
    if wt is None:
        return "git hung answering config core.worktree"
    if wt[0] == 0:
        p = pathlib.Path(wt[1])
        p = p if p.is_absolute() else repo / p
        if p.resolve() != repo:
            return f"core.worktree={wt[1]} leaves the repo directory"
    elif wt[0] != 1:
        return f"git config core.worktree failed (rc={wt[0]})"
    return None


def breach(d, argv, tool):
    """Refuse (reason string) or admit (None). Collection pass first; not one git child before the tree
    is proven self-contained."""
    try:
        d = pathlib.Path(d).resolve()
    except OSError:
        return "fixture dir does not resolve"
    if not d.is_dir():
        return "fixture dir is not a directory"
    why, repos, lane = _collect(d, tool, argv)
    if why:
        return why
    ceiling = d.parent  # the module build root: no module writes, no repo and no opens above d
    targets = [(r, True) for r in repos]
    if lane is not None:
        if not _inside(lane, d):
            return "--lane resolves outside the fixture"
        lane = lane.resolve()
        if lane.is_dir() and all(lane != r for r in repos):
            targets.append((lane, False))
    for repo, need_root in sorted(set(targets)):
        why = _probe(repo, ceiling, need_root, d)
        if why:
            return f"{repo.relative_to(d) if _inside(repo, d) else repo}: {why}"
    if tool == "order" and lane is not None and lane.is_dir():
        vals = dict(zip(argv[0::2], argv[1::2]))
        for opt in ("--claims", "--receipt"):
            got = _git(lane, ceiling, "cat-file", "-t", f"HEAD:{vals[opt]}")
            if got is None:
                return f"{opt} git hung"
            if got[0] == 0 and got[1] != "blob":
                return f"{opt} {vals[opt]} is a {got[1]} at HEAD, not a blob"
    return None

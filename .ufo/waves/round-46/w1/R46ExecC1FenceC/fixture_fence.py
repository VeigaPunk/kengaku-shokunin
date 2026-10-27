"""Fixture fence (round-46 C1, variant C: isolated git): admit only a fixture proven self-contained.

Contract (frozen, `plans/round45_c1_verify.py` docstring):

    breach(d: pathlib.Path, argv: list[str], tool: str) -> str | None

`d` is the fixture directory (absolute, resolved), `argv` the module's argv tail, `tool` `anchor` or `order`.
A non-empty one-line string refuses; None admits. Runs with cwd `d`, read-only, under `strace -f -y`, and
must decide without opening, stat-ing or readlink-ing any path outside `d` under the build scratch.

Design. Refuse what cannot be proven safe, instead of naming attack classes:

1. STATIC PASS, no child process, no access outside `d`. Argv must be the tool's exact contract shape (no
   abbreviation, no `--opt=value`, no extra token, no NUL, no `{...}` placeholder) and every path value must
   resolve LEXICALLY inside `d`. One walk of the whole tree, `.git` directories included (never pruned),
   refuses: a `.git` file or symlink, a second `.git` nested inside a git dir, `worktrees/` or `modules/`
   metadata under a git dir, any `commondir`/`gitdir`/`alternates` file, any `.git/config*` file whose text
   carries an `include`/`includeIf` section or a path-bearing key (core.worktree outside the repo,
   core.attributesFile, core.excludesFile, core.hooksPath, core.fsmonitor, core.bare true,
   extensions.worktreeConfig), any symlink whose target chain leaves `d`, any special file, and any store
   file with an extra hard link. Config text is normalised (UTF-8 BOM stripped, CR and CRLF treated as line
   breaks) before it is scanned, so a `\\r[include]` or a BOM cannot hide a section.

2. GIT PASS, only for a fixture the static pass proved self-contained, and only INSIDE a mount namespace
   that contains `d` bound at a constant alias (`/fixture`), the read-only system tree and nothing else. A
   reference to any path outside `d` therefore cannot resolve at all: git fails, and `rc != 0` from any probe
   is a refusal, never "clean". The legs ask for the worktree top level, the absolute git dir and the COMMON
   dir (a store redirect hidden anywhere below `d` shows up here), plus `core.worktree`; for `order` the
   claims and receipt must not be a tree at HEAD. The namespace is built from a RELATIVE bind source (`"."`,
   the child's cwd is `d`): an absolute source makes bubblewrap canonicalise `d`'s parent components, three
   readlinks on paths outside `d` that a round-46 counter counts like opens. Measured with `trace=%file`:
   with the relative source and the alias, the whole fence process tree touches no path under the scratch
   root other than `d` itself.

No path outside `d` is read, stat'ed or readlink'ed while deciding: the only outside opens are the fixed
system executables (`/usr/bin/bwrap`, `/usr/bin/git`) and the system tree inside the inner namespace.

Limit named in the report (not hidden here): the git pass needs nested unprivileged namespaces to work inside
the counter's own sandbox. Measured working on this host (bwrap 0.13.1, kernel 7.2.11); if a future sandbox
forbids them, every repo probe fails and the fence refuses every fixture with a repo rather than admitting it.
"""
import os
import pathlib
import re
import stat
import subprocess

BWRAP = "/usr/bin/bwrap"
GIT = "/usr/bin/git"
GIT_TIMEOUT = 20
ENTRY_CAP = 200000          # walked entries before the tree itself is refused as pathological
REPO_CAP = 64               # collected repos before the fixture is refused as pathological
CONFIG_CAP = 1 << 20        # a `.git/config*` file larger than this is refused unread
LINK_CAP = 32               # symlink hops followed before a chain is refused

ORDER_SHAPE = ("--lane", "--claims", "--receipt")
ANCHOR_OPTS = {"--lane": True, "--evidence-ref": True, "--verbose": False}
DENY_SECTIONS = ("include",)                        # `[include]` and `[includeIf ...]`
DENY_CORE_KEYS = {"attributesfile", "excludesfile", "hookspath", "fsmonitor", "worktree"}
BARE_TRUE = {"", "true", "1", "yes", "on"}

SYSTEM_PATH = "/usr/bin:/bin"
GIT_ENV = {
    "PATH": SYSTEM_PATH,
    "HOME": "/nonexistent",
    "LANG": "C",
    "LC_ALL": "C",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_COUNT": "4",
    "GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_VALUE_0": "false",
    "GIT_CONFIG_KEY_1": "core.hooksPath", "GIT_CONFIG_VALUE_1": "/dev/null",
    "GIT_CONFIG_KEY_2": "gpg.program", "GIT_CONFIG_VALUE_2": "/bin/true",
    "GIT_CONFIG_KEY_3": "log.showSignature", "GIT_CONFIG_VALUE_3": "false",
    "GIT_TERMINAL_PROMPT": "0",
}
_SECTION_RE = re.compile(r"\[\s*([A-Za-z0-9_.-]+)")
_COMMENT_RE = re.compile(r"(?:^|\s)[#;]")


def _norm(p):
    """Lexical normalisation only: never stat or resolve a component outside d."""
    return os.path.normpath(p)


def _inside(p, d):
    """True when the lexically normalised absolute path is d or below it."""
    p = _norm(p)
    return p == d or p.startswith(d + os.sep)


def _value_path(v, d):
    p = v if v.startswith("/") else os.path.join(d, v)
    return _norm(p)


def _target(p):
    """The lexical target of the symlink at p, or None when it cannot be read."""
    try:
        t = os.readlink(p)
    except OSError:
        return None
    return _norm(t if os.path.isabs(t) else os.path.join(os.path.dirname(p), t))


def _link_leaves(p, d):
    """Follow the symlink at p by readlink only, all inside d, and report whether it leaves d.
    Returns (leaves, why). A cycle or a hop cap is a refusal, not an admission."""
    cur = p
    for _ in range(LINK_CAP):
        tgt = _target(cur)
        if tgt is None:
            return True, "cannot be read as a symlink"
        if not _inside(tgt, d):
            return True, f"-> {os.readlink(cur)} leaves the fixture"
        if not os.path.islink(tgt):
            return False, ""
        cur = tgt
    return True, "symlink chain is longer than the hop cap"


def _config_breach(raw, rel, repo_of, d):
    """Judge one config file's bytes. Any include, any path-bearing key, any worktree redirect: refusal."""
    if len(raw) > CONFIG_CAP:
        return f"{rel} exceeds {CONFIG_CAP} bytes"
    text = raw.decode("utf-8", "surrogateescape")
    if text.startswith("\ufeff"):
        text = text[1:]
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    sect = ""
    for line in text.splitlines():
        s = line.strip()
        if not s or s[0] in "#;":
            continue
        if s.startswith("["):
            m = _SECTION_RE.match(s)
            sect = m.group(1).lower() if m else ""
            if sect.startswith(DENY_SECTIONS):
                return f"{rel} carries a [{sect}] section"
            continue
        m = _COMMENT_RE.search(s)
        if m:
            s = s[:m.start()]
        key, _, val = s.partition("=")
        key = key.strip().lower()
        val = val.strip().strip('"').strip("'")
        if not key:
            continue
        if sect == "extensions" and key == "worktreeconfig":
            return f"{rel} enables extensions.worktreeConfig"
        if sect == "core" and key == "bare" and val.lower() in BARE_TRUE:
            return f"{rel} sets core.bare"
        if sect == "core" and key == "worktree":
            wt = _value_path(val, repo_of) if val.startswith("/") else _norm(os.path.join(repo_of, val))
            if wt != repo_of:
                return f"{rel} sets core.worktree={val}"
            continue
        if sect == "core" and key in DENY_CORE_KEYS:
            return f"{rel} sets core.{key}"
        if key == "path":
            return f"{rel} carries a path= key"
    return None


def _collect(d, tool, argv):
    """Static pass: argv shape and containment, then one walk of the whole tree. Returns (breach, repos, lane)."""
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
                if k + 1 >= len(argv):
                    return f"anchor option {t} has no value", None, None
                vals[t] = argv[k + 1]
                k += 2
            else:
                vals[t] = True
                k += 1
    else:
        return f"unknown tool {tool!r}", None, None

    for opt, val in vals.items():
        if val is True:
            continue
        if not isinstance(val, str) or not val:
            return f"{opt} value is empty", None, None
        if "{" in val or "}" in val:
            return f"{opt} value {val!r} is a placeholder, not a path", None, None
        if not _inside(_value_path(val, d), d):
            return f"{opt} value {val!r} resolves outside the fixture", None, None

    repos, seen = [], 0
    for top, dirs, files in os.walk(d, topdown=True, followlinks=False):
        seen += len(dirs) + len(files)
        if seen > ENTRY_CAP:
            return f"fixture tree exceeds {ENTRY_CAP} entries", None, None
        top = _norm(top)
        rel_top = os.path.relpath(top, d)
        parts_top = () if rel_top == "." else pathlib.PurePath(rel_top).parts
        in_git = ".git" in parts_top
        repo_of = None
        if in_git:
            idx = len(parts_top) - 1 - list(reversed(parts_top)).index(".git")
            repo_of = _norm(os.path.join(d, *parts_top[:idx])) if idx else d
        # a git dir and a bare store carry the same markers; a store outside a `.git` (bare) is judged too, so
        # no config file in the fixture escapes the scan by not sitting under a `.git` directory.
        store = (not in_git) and ("HEAD" in files) and ("objects" in dirs) and ("config" in files)
        if store:
            repo_of = top
        for name in list(dirs):
            p = os.path.join(top, name)
            rp = os.path.relpath(p, d)
            if os.path.islink(p):
                if name == ".git":
                    return f"{rp} is a symlink, not a git dir", None, None
                leaves, why = _link_leaves(p, d)
                if leaves:
                    return f"symlink {rp} {why}", None, None
                dirs.remove(name)
                continue
            if name == ".git":
                if in_git:
                    return f"{rp} is a .git nested inside a git dir", None, None
                try:
                    mode = os.lstat(p).st_mode
                except OSError:
                    return f"{rp} cannot be stat'ed", None, None
                if not stat.S_ISDIR(mode):
                    return f"{rp} is not a directory", None, None
                repos.append(top)
                continue
            if (in_git or store) and name in ("worktrees", "modules"):
                return f"{rp} is linked-worktree/submodule metadata", None, None
        for name in list(files):
            p = os.path.join(top, name)
            rp = os.path.relpath(p, d)
            if os.path.islink(p):
                leaves, why = _link_leaves(p, d)
                if leaves:
                    return f"symlink {rp} {why}", None, None
                continue
            try:
                st = os.lstat(p)
            except OSError:
                return f"{rp} cannot be stat'ed", None, None
            mode = st.st_mode
            if stat.S_ISFIFO(mode) or stat.S_ISSOCK(mode) or stat.S_ISBLK(mode) or stat.S_ISCHR(mode):
                return f"{rp} is a special file", None, None
            if not stat.S_ISREG(mode):
                return f"{rp} is not a regular file or directory", None, None
            if name == ".git":
                return f"{rp} is a file (gitdir redirect), not a directory", None, None
            if in_git or store:
                if name in ("commondir", "gitdir"):
                    return f"{rp} is a store/worktree redirect", None, None
                if name in ("alternates", "http-alternates"):
                    return f"{rp} is an alternates file", None, None
                if st.st_nlink > 1:
                    return f"{rp} has extra hard links", None, None
                if name.startswith("config"):
                    try:
                        with open(p, "rb") as fh:
                            raw = fh.read(CONFIG_CAP + 1)
                    except OSError:
                        return f"{rp} is unreadable", None, None
                    why = _config_breach(raw, rp, repo_of, d)
                    if why:
                        return why, None, None
        dirs.sort()
    if len(repos) > REPO_CAP:
        return f"fixture holds more than {REPO_CAP} repos", None, None
    lane = vals.get("--lane")
    lane = _value_path(lane, d) if isinstance(lane, str) else None
    return None, repos, lane


# ---------- isolated git pass (namespace contains d and the system tree only) ----------


ROOT_ALIAS = "/fixture"


def _sandbox():
    """Inner mount namespace: the fixture bound from the child's cwd (`.` == d) at ROOT_ALIAS, the read-only
    system tree, nothing else. Binding a RELATIVE source keeps bubblewrap from canonicalising d's parent
    components, so not one scratch path outside d is touched while the namespace is built (measured: zero
    path-taking syscalls on any path under the scratch root other than d; an absolute source leaks three
    readlinks on d's ancestors)."""
    return [BWRAP, "--ro-bind", ".", ROOT_ALIAS, "--ro-bind", "/usr", "/usr",
            "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64",
            "--symlink", "usr/bin", "/bin", "--symlink", "usr/bin", "/sbin",
            "--dev", "/dev", "--proc", "/proc",
            "--unshare-pid", "--unshare-net", "--unshare-ipc",
            "--die-with-parent", "--new-session", "--chdir", ROOT_ALIAS]


def _alias(repo, d):
    """The repo's path inside the inner namespace."""
    rel = os.path.relpath(repo, d)
    return ROOT_ALIAS if rel == "." else ROOT_ALIAS + "/" + rel


def _unmask(p, d):
    """Translate an inner-namespace path back to the fixture path, or None when it is not under the alias."""
    if p == ROOT_ALIAS:
        return d
    if p.startswith(ROOT_ALIAS + "/"):
        return d + p[len(ROOT_ALIAS):]
    return None


def _git(repo_alias, d, *args):
    """One git call inside the inner namespace. (rc, stdout) or (None, "") on a timeout."""
    try:
        r = subprocess.run(_sandbox() + [GIT, "-C", repo_alias, *args], capture_output=True, text=True,
                           env=GIT_ENV, stdin=subprocess.DEVNULL, timeout=GIT_TIMEOUT, cwd=d)
    except subprocess.TimeoutExpired:
        return None, ""
    except OSError:
        return -1, ""
    return r.returncode, r.stdout


def _probe(repo, d, need_root):
    """Worktree top, absolute git dir and COMMON dir must all answer inside d; any failure is a refusal.
    A reference to any path outside d cannot resolve in the namespace, so it surfaces as rc != 0."""
    rel = os.path.relpath(repo, d)
    rc, out = _git(_alias(repo, d), d, "rev-parse", "--show-toplevel", "--absolute-git-dir",
                   "--git-common-dir")
    if rc is None:
        return f"{rel}: git hung answering rev-parse"
    if rc != 0:
        return f"{rel}: git cannot describe the fixture (rc={rc})"
    lines = out.splitlines()
    if len(lines) != 3:
        return f"{rel}: rev-parse answered {len(lines)} fields, not 3"
    top, gdir, common = (_norm(x) for x in lines)
    host_top = _unmask(top, d)
    if host_top is None:
        return f"{rel}: worktree top level {top} is not the bound fixture"
    if need_root:
        if host_top != repo:
            return f"{rel}: worktree top level is {os.path.relpath(host_top, d)}, not the repo directory"
    host_gdir = _unmask(gdir, d)
    if host_gdir is None:
        return f"{rel}: git dir {gdir} is not inside the bound fixture"
    common = common if common.startswith("/") else _norm(os.path.join(_alias(repo, d), common))
    if _unmask(common, d) is None:
        return f"{rel}: git common dir {common} is not inside the bound fixture"
    rc, out = _git(_alias(repo, d), d, "config", "--local", "--no-includes", "--get", "core.worktree")
    if rc is None:
        return f"{rel}: git hung answering core.worktree"
    if rc == 0:
        val = out.strip()
        if val.startswith("/"):
            wt = _unmask(_norm(val), d)
            if wt is None or wt != repo:
                return f"{rel}: core.worktree={val} leaves the repo directory"
        elif _norm(os.path.join(repo, val)) != repo:
            return f"{rel}: core.worktree={val} leaves the repo directory"
    elif rc != 1:
        return f"{rel}: git config core.worktree failed (rc={rc})"
    return None


def _one_line(s, cap=200):
    """A reason is one printable line: fixture names may carry control bytes or surrogates."""
    s = str(s).encode("utf-8", "replace").decode("utf-8", "replace")
    s = "".join(ch if 32 <= ord(ch) < 127 else " " for ch in s)
    return " ".join(s.split())[:cap] or "refused"


def breach(d, argv, tool):
    """Refuse (one-line reason) or admit (None). Static proof first; git only inside an isolated namespace."""
    why = _decide(d, argv, tool)
    return None if why is None else _one_line(why)


def _decide(d, argv, tool):
    try:
        if not isinstance(argv, list) or not all(isinstance(t, str) for t in argv):
            return "argv is not a list of strings"
        for t in argv:
            if "\x00" in t:
                return "argv token carries a NUL byte"
        d = _norm(os.path.abspath(str(d)))
        if not os.path.isdir(d):
            return "fixture dir is not a directory"
        why, repos, lane = _collect(d, tool, argv)
        if why:
            return why
        targets = {r: True for r in repos}
        if lane is not None and os.path.isdir(lane):
            targets.setdefault(lane, False)
        for repo in sorted(targets):
            why = _probe(repo, d, targets[repo])
            if why:
                return why
        if tool == "order" and lane is not None and os.path.isdir(lane):
            vals = dict(zip(argv[0::2], argv[1::2]))
            for opt in ("--claims", "--receipt"):
                rc, out = _git(_alias(lane, d), d, "cat-file", "-t", f"HEAD:{vals[opt]}")
                if rc is None:
                    return f"{opt} git hung"
                if rc == 0 and out.strip() != "blob":
                    return f"{opt} {vals[opt]} is a {out.strip()} at HEAD, not a blob"
        return None
    except Exception as e:  # noqa: BLE001 — an answer is never "admit" because a check raised
        return f"fence could not decide: {type(e).__name__}"

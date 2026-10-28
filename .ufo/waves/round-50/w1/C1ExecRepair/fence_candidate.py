"""Fixture fence (round-46 C1, variant A: allowlist): admit only a fixture whose git store is provably the
shape a plain `git init` + commits writes inside `d`, and whose argv names nothing else.

Contract (frozen, `plans/round45_c1_verify.py` docstring):

    breach(d: pathlib.Path, argv: list[str], tool: str) -> str | None

`d` is the fixture directory (absolute, resolved), `argv` the module's argv tail, `tool` `anchor` or `order`.
A non-empty string refuses (the reason, one line); None admits. Runs with cwd `d`, read-only, under
`strace -f -y`.

Round 45's fence named attack classes (commondir, alternates, `[include]` text) and was passed by nine held-out
modules that spelled the same escapes differently: a bare `\\r` or a UTF-8 BOM before the section header, a
relative `commondir` below a pruned `.git`, `.git/objects` as a symlink, `core.attributesFile`, nested
worktree metadata. Variant A inverts the burden: nothing is admitted until every byte the decision depends on
has been classified against a small allowlist, and anything unclassified is refused.

Structure:
  1. `d` itself must be a real directory (lstat, never followed).
  2. argv must be the tool's exact option shape; every value must be a path that stays inside `d` lexically
     (no `..`, no absolute escape, no NUL, no `{...}` placeholder we cannot resolve).
  3. one walk of `d` proves the tree has no symlink and no special file anywhere, and collects every directory
     holding a real `.git` directory, plus every directory whose `.git` is a *file*: that file must hold one
     `gitdir: <path>` line that resolves inside `d` (round 50 admits n20/n21 instead of refusing the file).
  4. each collected store is classified entry by entry against a plain-init allowlist: `HEAD`, `ORIG_HEAD`,
     `FETCH_HEAD` (admitted by name, content never read), `COMMIT_EDITMSG`, `config`, `description`, `hooks/`
     (`*.sample` only), `index`, `info/exclude` only, `logs/`, `objects/` (2-hex/38-hex loose objects, pack
     files only, and `info/alternates` only when every line resolves inside `d`), `refs/heads|tags|replace`
     (40-hex refs), `packed-refs`, `worktrees/` (per-worktree metadata, whose `gitdir` and `commondir` must
     resolve inside `d`). `config` is parsed line by line against a `[core]` key allowlist plus the one
     `[extensions]` key a relative-path linked worktree needs (`relativeWorktrees`, which git writes only with
     `core.repositoryformatversion = 1`); any CR, any non-ASCII byte, any other section or key, or any line
     the parser does not fully understand is refused. This is what closes the CR/BOM/includeIf/attributesFile
     family.
  5. a `.git` file is not a redirect until its target is proved: the target must be a directory inside `d`, and
     either a store (classified as in 4) or a per-worktree metadata dir whose `commondir` resolves inside `d`.
     An out-of-`d` or dangling target, and a `commondir` outside `d`, are refused.
  6. `--lane` must be one of the collected repositories.
  7. no git child is started at all: measured, every git subcommand resolves the fixture path component-wise
     and stats `d`'s ancestors (paths under the build scratch outside `d`), which the advertisement and the
     round-46 counter's B3/B5 legs forbid. The store classification is the proof instead.

Every path the decision names is lexically inside `d`, and no syscall the decision makes names anything else
(the measured residue is only the interpreter importing the harness and this module, before `breach` runs).
`.git/index`, `COMMIT_EDITMSG`, `description`, `logs/*` and pack files are admitted by name and size without
content validation: the tool run behind this fence reads none of them for a path (named limit).
"""
import os
import pathlib
import re
import stat

ENTRY_CAP = 200000          # walked entries before the tree itself is refused as pathological
REPO_CAP = 64               # collected repos before the fixture is refused as pathological
CONFIG_CAP = 1 << 20        # a `.git/config` larger than this is refused unread
INDEX_CAP = 1 << 24         # a `.git/index` larger than this is refused
TEXT_CAP = 1 << 16          # cap for HEAD / ORIG_HEAD / COMMIT_EDITMSG / logs
ALTERNATES_DEPTH = 4        # hops of `objects/info/alternates` followed before the chain is refused

ORDER_SHAPE = ("--lane", "--claims", "--receipt")
ANCHOR_OPTS = {"--lane": True, "--evidence-ref": True, "--verbose": False}

HEX40 = re.compile(rb"\A[0-9a-f]{40}(?:\n)?\Z")
HEAD_REF = re.compile(rb"\Aref: refs/heads/[A-Za-z0-9_][A-Za-z0-9._/-]*\n\Z")
SECTION_LINE = re.compile(rb"\A\[([A-Za-z][A-Za-z0-9.-]*)\]\Z")
KEY_LINE = re.compile(rb"\A([A-Za-z][A-Za-z0-9-]*)(?:[ \t]*=[ \t]*([A-Za-z0-9._-]*))?\Z")
OBJ_DIR = re.compile(r"\A[0-9a-f]{2}\Z", re.ASCII)
OBJ_FILE = re.compile(r"\A[0-9a-f]{38}\Z", re.ASCII)
PACK_FILE = re.compile(r"\A[A-Za-z0-9_][A-Za-z0-9._-]*\.(?:pack|idx|rev|keep|bitmap|mtimes)\Z", re.ASCII)
SAFE_NAME = re.compile(r"\A[A-Za-z0-9_][A-Za-z0-9._-]*\Z", re.ASCII)
REF_PATH = re.compile(r"\A[A-Za-z0-9_][A-Za-z0-9._/-]*\Z", re.ASCII)
REPLACE_NAME = re.compile(r"\A[0-9a-f]{40}\Z", re.ASCII)

GIT_TOP = {"HEAD", "ORIG_HEAD", "FETCH_HEAD", "COMMIT_EDITMSG", "config", "description", "hooks", "index",
           "info", "logs", "objects", "refs", "packed-refs", "worktrees"}
GIT_DIRS = {"hooks", "info", "logs", "objects", "refs", "worktrees"}
WORKTREE_TOP = {"HEAD", "ORIG_HEAD", "commondir", "gitdir", "index", "logs", "refs"}
WORKTREE_DIRS = {"logs", "refs"}
GIT_REF_NAMESPACES = {"heads", "tags", "replace"}
GITDIR = b"gitdir: "          # git's own prefix, the single space included (`starts_with(buf, "gitdir: ")`)
CFG_SECTIONS = {"core", "extensions"}
CFG_KEYS = {
    ("core", "repositoryformatversion"): "version",
    ("core", "filemode"): "bool",
    ("core", "bare"): "false",
    ("core", "logallrefupdates"): "bool",
    ("core", "ignorecase"): "bool",
    ("core", "precomposeunicode"): "bool",
    ("core", "symlinks"): "bool",
    ("extensions", "relativeworktrees"): "bool",
}
BOOL = {"true", "yes", "on", "1", "false", "no", "off", "0"}
FALSEY = {"false", "no", "off", "0"}


# ---------- small path helpers (lexical only: no resolve, no follow) ----------


def _norm(p):
    return os.path.normpath(str(p))


def _inside(p, d):
    p, d = _norm(p), _norm(d)
    return p == d or p.startswith(d + os.sep)


def _rel(p, d):
    try:
        return os.path.relpath(str(p), str(d))
    except ValueError:
        return str(p)


def _entries(p):
    """[(name, mode, size, nlink)] of one directory, lstat-style. None when it cannot be read."""
    out = []
    try:
        with os.scandir(str(p)) as it:
            for e in it:
                st = e.stat(follow_symlinks=False)
                out.append((e.name, st.st_mode, st.st_size, st.st_nlink))
    except OSError:
        return None
    return sorted(out)


def _linked(mode, nlink):
    """A regular file with another name somewhere is not provably inside `d`: refuse it."""
    return stat.S_ISREG(mode) and nlink > 1


def _ref_name_ok(name):
    if not REF_PATH.match(name):
        return False
    parts = name.split("/")
    return all(p not in (".", "..") and p and not p.endswith(".lock") for p in parts)


def _read(p, cap):
    try:
        with open(p, "rb") as fh:
            return fh.read(cap + 1)
    except OSError:
        return None


def _one_line(p, label):
    """The single ASCII line of a pointer file (`.git`, a worktree's `gitdir`/`commondir`), or a reason."""
    raw = _read(p, TEXT_CAP)
    if raw is None:
        return None, f"{label} unreadable"
    if len(raw) > TEXT_CAP:
        return None, f"{label} exceeds {TEXT_CAP} bytes"
    if b"\x00" in raw:
        return None, f"{label} carries a NUL byte"
    if b"\r" in raw:
        return None, f"{label} carries a bare CR"
    if any(b >= 0x80 for b in raw):
        return None, f"{label} carries a non-ASCII byte"
    body = raw[:-1] if raw.endswith(b"\n") else raw
    if b"\n" in body:
        return None, f"{label} is not a single line"
    return body, None


def _pointer(p, label, base, d, prefixed):
    """(target, text, reason): a pointer file's path, resolved lexically against `base`, inside `d`.

    `prefixed` is true for git's `gitdir: <path>` shape (one space, then the path), false for `commondir` and a
    worktree's `gitdir` file, whose whole line is the path. Git does not trim these files: it reads one line and
    takes the remainder verbatim (measured, git 2.56.0: `gitdir: ../store   ` is rejected while
    `gitdir: ../store` without the newline is accepted), so nothing is trimmed here either. A bare CR is refused
    (stricter than git, which tolerates a CRLF terminator; no fixture in the population writes one).
    """
    body, why = _one_line(p, label)
    if why:
        return None, None, why
    if prefixed:
        if not body.startswith(GITDIR):
            return None, None, f"{label} is not a `gitdir: ` redirect"
        body = body[len(GITDIR):]
    text = body.decode("ascii")
    if not text:
        return None, None, f"{label} names an empty path"
    raw = text if text.startswith("/") else os.path.join(str(base), text)
    target = pathlib.Path(_norm(raw))
    if not _inside(target, d):
        return None, text, f"{label} names {text!r}, which resolves outside the fixture"
    return target, text, None


def _dir_ref(p, label, base, d, prefixed):
    """A pointer that must name an existing directory inside `d`, and not a symlink."""
    target, text, why = _pointer(p, label, base, d, prefixed)
    if why:
        return None, why
    try:
        st = os.lstat(target)
    except OSError:
        return None, f"{label} names {text!r}, which does not exist"
    if stat.S_ISLNK(st.st_mode):
        return None, f"{label} names {text!r}, which is a symlink"
    if not stat.S_ISDIR(st.st_mode):
        return None, f"{label} names {text!r}, which is not a directory"
    return target, None


def _file_ref(p, label, base, d, prefixed):
    """A pointer that must name an existing single-link regular file inside `d`, and not a symlink."""
    target, text, why = _pointer(p, label, base, d, prefixed)
    if why:
        return None, why
    try:
        st = os.lstat(target)
    except OSError:
        return None, f"{label} names {text!r}, which does not exist"
    if stat.S_ISLNK(st.st_mode):
        return None, f"{label} names {text!r}, which is a symlink"
    if not stat.S_ISREG(st.st_mode):
        return None, f"{label} names {text!r}, which is not a regular file"
    if st.st_nlink > 1:
        return None, f"{label} names {text!r}, which has more than one hard link"
    return target, None


# ---------- fact 1/2: argv ----------


def _argv(d, tool, argv):
    """Return (values, reason). Only the exact contract shape and inside-`d` path values pass."""
    if not isinstance(argv, (list, tuple)) or not all(isinstance(t, str) for t in argv):
        return None, "argv is not a list of strings"
    vals = {}
    if tool == "order":
        if len(argv) != 6 or tuple(argv[0::2]) != ORDER_SHAPE:
            return None, f"order argv is not the contract shape {list(ORDER_SHAPE)}"
        vals = dict(zip(argv[0::2], argv[1::2]))
    elif tool == "anchor":
        k = 0
        while k < len(argv):
            t = argv[k]
            if t not in ANCHOR_OPTS:
                return None, f"anchor argv token {t!r} is not an exact option"
            if ANCHOR_OPTS[t]:
                if k + 1 >= len(argv):
                    return None, f"anchor option {t} has no value"
                vals[t] = argv[k + 1]
                k += 2
            else:
                vals[t] = True
                k += 1
    else:
        return None, f"unknown tool {tool!r}"
    for opt, val in vals.items():
        if val is True:
            continue
        if "\x00" in val:
            return None, f"{opt} value carries a NUL byte"
        if "\r" in val or "\n" in val:
            return None, f"{opt} value carries a newline"
        if val.startswith("{"):
            return None, f"{opt} value {val!r} is a placeholder the fence cannot resolve"
        raw = val if val.startswith("/") else os.path.join(str(d), val)
        if not _inside(raw, d):
            return None, f"{opt} value {val!r} resolves outside the fixture"
    return vals, None


# ---------- fact 3: the whole tree ----------


def _tree(d):
    """Return (repos, gitfiles, reason): every directory holding a real `.git` dir, every directory whose
    `.git` is a file naming a store inside `d`, after refusing symlinks and special files anywhere."""
    repos, gitfiles, seen = [], [], 0
    for top, dirs, files in os.walk(str(d), followlinks=False):
        seen += len(dirs) + len(files)
        if seen > ENTRY_CAP:
            return None, None, f"fixture tree exceeds {ENTRY_CAP} entries"
        t = pathlib.Path(top)
        keep = []
        for name in dirs:
            p = t / name
            try:
                mode = os.lstat(p).st_mode
            except OSError:
                return None, None, f"{_rel(p, d)} cannot be lstat'ed"
            if stat.S_ISLNK(mode):
                return None, None, f"{_rel(p, d)} is a symlink"
            if not stat.S_ISDIR(mode):
                return None, None, f"{_rel(p, d)} is not a directory"
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
                return None, None, f"{_rel(p, d)} cannot be lstat'ed"
            if stat.S_ISLNK(mode):
                return None, None, f"{_rel(p, d)} is a symlink"
            if not stat.S_ISREG(mode):
                return None, None, f"{_rel(p, d)} is a special file"
            if os.lstat(p).st_nlink > 1:
                return None, None, f"{_rel(p, d)} has more than one hard link"
            if name == ".git":
                target, why = _dir_ref(p, _rel(p, d), t, d, True)
                if why:
                    return None, None, why
                gitfiles.append((t, target))
    if len(repos) > REPO_CAP:
        return None, None, f"fixture holds more than {REPO_CAP} repos"
    return repos, gitfiles, None


# ---------- fact 4: the store, classified against the plain-init allowlist ----------


def _config(p, label):
    """Parse `.git/config` strictly. Anything the parser does not fully classify is refused."""
    raw = _read(p, CONFIG_CAP)
    if raw is None:
        return f"{label}/config unreadable"
    if len(raw) > CONFIG_CAP:
        return f"{label}/config exceeds {CONFIG_CAP} bytes"
    if b"\x00" in raw:
        return f"{label}/config carries a NUL byte"
    if b"\r" in raw:
        return f"{label}/config carries a bare CR"
    if any(b >= 0x80 for b in raw):
        return f"{label}/config carries a non-ASCII byte"
    sect = ""
    version = "0"
    saw_ext = False
    for line in raw.split(b"\n"):
        s = line.lstrip(b" \t")
        if not s:
            continue
        if s[:1] in (b"#", b";"):
            continue
        if s.startswith(b"["):
            m = SECTION_LINE.match(s)
            if m is None:
                return f"{label}/config section header {s[:40]!r} is not plain"
            sect = m.group(1).decode("ascii").lower()
            if sect not in CFG_SECTIONS:
                return f"{label}/config section [{sect}] is not allowlisted"
            continue
        m = KEY_LINE.match(s)
        if m is None:
            return f"{label}/config line {s[:40]!r} is not a plain key=value"
        key = m.group(1).decode("ascii").lower()
        need = CFG_KEYS.get((sect, key))
        if need is None:
            return f"{label}/config key {sect}.{key} is not allowlisted"
        if sect == "extensions":
            saw_ext = True
        if m.group(2) is None:
            if need != "bool":
                return f"{label}/config key {sect}.{key} needs a value"
            continue
        val = m.group(2).decode("ascii").lower()
        if need == "version":
            if val not in ("0", "1"):
                return f"{label}/config {sect}.{key}={val!r} must be 0 or 1"
            if key == "repositoryformatversion":
                version = val
        elif need == "bool":
            if val not in BOOL:
                return f"{label}/config {sect}.{key}={val!r} is not a boolean"
        elif need == "false":
            if val not in FALSEY:
                return f"{label}/config {sect}.{key} must be false"
    if saw_ext and version != "1":
        return f"{label}/config [extensions] needs repositoryformatversion = 1"
    return None


def _refs(p, label):
    ents = _entries(p)
    if ents is None:
        return f"{label} unreadable"
    for name, mode, _s, _n in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{_rel(q, label)} is a symlink"
        if _linked(mode, _n):
            return f"{_rel(q, label)} has more than one hard link"
        if name not in GIT_REF_NAMESPACES:
            return f"{label}/{name} is not refs/heads, refs/tags or refs/replace"
        if not stat.S_ISDIR(mode):
            return f"{label}/{name} is not a directory"
        why = _ref_tree(q, label, name)
        if why:
            return why
    return None


def _ref_tree(p, label, ns=None):
    ents = _entries(p)
    if ents is None:
        return f"{_rel(p, label)} unreadable"
    for name, mode, _s, _n in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{_rel(q, label)} is a symlink"
        if _linked(mode, _n):
            return f"{_rel(q, label)} has more than one hard link"
        if stat.S_ISDIR(mode):
            if not _ref_name_ok(name):
                return f"{_rel(q, label)} has a name git does not write"
            if ns == "replace":
                return f"{_rel(q, label)} is a replace subdirectory git does not write"
            why = _ref_tree(q, label, ns)
            if why:
                return why
            continue
        if not stat.S_ISREG(mode):
            return f"{_rel(q, label)} is a special file"
        if not _ref_name_ok(name):
            return f"{_rel(q, label)} has a name git does not write"
        if ns == "replace" and REPLACE_NAME.match(name) is None:
            return f"{_rel(q, label)} is not a 40-hex replace ref"
        body = _read(q, 200)
        if body is None:
            return f"{_rel(q, label)} unreadable"
        if HEX40.match(body) is None:
            return f"{_rel(q, label)} is not a 40-hex ref"
    return None


def _alternates(objects, label, d, seen=None, depth=0):
    """`objects/info/alternates`: every line must name an object dir inside `d` — and so must every hop.

    A relative entry resolves against the object dir that holds the file, which is how git reads it; git then
    reads `<target>/info/alternates` as well (`link_alt_odb_entries` recurses), so a chain is followed here too.
    Without that, an entry that is inside `d` but names a store which borrows from outside `d` would be an
    escape. `seen` breaks cycles, `ALTERNATES_DEPTH` bounds the chain. Lines are taken verbatim: git trims
    nothing (measured), so a trailing space fails here exactly where it fails in git. Comment lines are refused
    (git writes none), and so is a file with no entry at all.
    """
    seen = set() if seen is None else seen
    p = objects / "info" / "alternates"
    try:
        st = os.lstat(p)
    except OSError:
        return None if depth else f"{label} unreadable"
    if stat.S_ISLNK(st.st_mode):
        return f"{label} is a symlink"
    if not stat.S_ISREG(st.st_mode):
        return f"{label} is not a regular file"
    if st.st_nlink > 1:
        return f"{label} has more than one hard link"
    raw = _read(p, TEXT_CAP)
    if raw is None:
        return f"{label} unreadable"
    if len(raw) > TEXT_CAP:
        return f"{label} exceeds {TEXT_CAP} bytes"
    if b"\x00" in raw:
        return f"{label} carries a NUL byte"
    if b"\r" in raw:
        return f"{label} carries a bare CR"
    if any(b >= 0x80 for b in raw):
        return f"{label} carries a non-ASCII byte"
    lines = [line for line in raw.split(b"\n") if line]
    if not lines:
        return f"{label} names no object directory"
    for line in lines:
        if line.startswith(b"#"):
            return f"{label} carries a comment line git does not write"
        text = line.decode("ascii")
        raw_target = text if text.startswith("/") else os.path.join(str(objects), text)
        target = pathlib.Path(_norm(raw_target))
        if not _inside(target, d):
            return f"{label} names {text!r}, which resolves outside the fixture"
        try:
            tst = os.lstat(target)
        except OSError:
            return f"{label} names {text!r}, which does not exist"
        if stat.S_ISLNK(tst.st_mode):
            return f"{label} names {text!r}, which is a symlink"
        if not stat.S_ISDIR(tst.st_mode):
            return f"{label} names {text!r}, which is not a directory"
        key = _norm(target)
        if key in seen:
            continue
        seen.add(key)
        if depth + 1 > ALTERNATES_DEPTH:
            return f"{label} chains deeper than {ALTERNATES_DEPTH} object stores"
        why = _alternates(target, f"{label} -> {text!r}", d, seen, depth + 1)
        if why:
            return why
    return None


def _objects(p, label, d):
    ents = _entries(p)
    if ents is None:
        return f"{label} unreadable"
    for name, mode, _s, _n in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{_rel(q, label)} is a symlink"
        if not stat.S_ISDIR(mode):
            return f"{label}/{name} is not a directory"
        if name == "info":
            inner = _entries(q)
            if inner is None:
                return f"{label}/info unreadable"
            for iname, imode, _is, _in in inner:
                if stat.S_ISLNK(imode):
                    return f"{label}/info/{iname} is a symlink"
                if not stat.S_ISREG(imode):
                    return f"{label}/info/{iname} is not a regular file"
                if _linked(imode, _in):
                    return f"{label}/info/{iname} has more than one hard link"
                if iname != "alternates":
                    return f"{label}/info/{iname} is not git's alternates file"
                why = _alternates(p, f"{label}/info/{iname}", d)
                if why:
                    return why
            continue
        if name == "pack":
            inner = _entries(q)
            if inner is None:
                return f"{label}/pack unreadable"
            for pname, pmode, _ps, _pn in inner:
                if stat.S_ISLNK(pmode):
                    return f"{label}/pack/{pname} is a symlink"
                if not stat.S_ISREG(pmode) or not PACK_FILE.match(pname):
                    return f"{label}/pack/{pname} is not a pack file"
                if _linked(pmode, _pn):
                    return f"{label}/pack/{pname} has more than one hard link"
            continue
        if not OBJ_DIR.match(name):
            return f"{label}/{name} is not a loose-object directory"
        inner = _entries(q)
        if inner is None:
            return f"{_rel(q, label)} unreadable"
        for oname, omode, _os_, _on in inner:
            qq = q / oname
            if stat.S_ISLNK(omode):
                return f"{_rel(qq, label)} is a symlink"
            if not stat.S_ISREG(omode) or not OBJ_FILE.match(oname):
                return f"{_rel(qq, label)} is not a loose object"
            if _linked(omode, _on):
                return f"{_rel(qq, label)} has more than one hard link"
    return None


def _log_name_ok(rel):
    """A reflog lives at `HEAD` or under `refs/heads|refs/tags` with git's own name shape."""
    if rel == "HEAD":
        return True
    m = re.fullmatch(r"refs/(?:heads|tags)/(.+)", rel, re.ASCII)
    if not m:
        return False
    return all(SAFE_NAME.match(part) for part in m.group(1).split("/"))


def _logs(p, label, prefix=""):
    ents = _entries(p)
    if ents is None:
        return f"{label} unreadable"
    for name, mode, size, n in ents:
        q = p / name
        rel = prefix + name
        if stat.S_ISLNK(mode):
            return f"{_rel(q, label)} is a symlink"
        if _linked(mode, n):
            return f"{_rel(q, label)} has more than one hard link"
        if stat.S_ISDIR(mode):
            if not (rel in ("refs", "refs/heads", "refs/tags") or _log_name_ok(rel)):
                return f"{_rel(q, label)} has a name git does not write"
            why = _logs(q, label, rel + "/")
            if why:
                return why
            continue
        if not stat.S_ISREG(mode):
            return f"{_rel(q, label)} is a special file"
        if not _log_name_ok(rel):
            return f"{_rel(q, label)} has a name git does not write"
        if size > TEXT_CAP:
            return f"{_rel(q, label)} exceeds {TEXT_CAP} bytes"
    return None


def _hooks(p, label):
    ents = _entries(p)
    if ents is None:
        return f"{label} unreadable"
    for name, mode, _s, _n in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{_rel(q, label)} is a symlink"
        if not stat.S_ISREG(mode) or not name.endswith(".sample"):
            return f"{_rel(q, label)} is not a hook sample"
        if _linked(mode, _n):
            return f"{_rel(q, label)} has more than one hard link"
    return None


def _packed(p, label):
    raw = _read(p, CONFIG_CAP)
    if raw is None:
        return f"{label} unreadable"
    if len(raw) > CONFIG_CAP:
        return f"{label} exceeds {CONFIG_CAP} bytes"
    for line in raw.split(b"\n"):
        if not line:
            continue
        if line.startswith(b"#"):
            if not line.startswith(b"# pack-refs with:"):
                return f"{label} carries an unknown header"
            continue
        if line.startswith(b"^"):
            if HEX40.match(line[1:] + b"\n") is None:
                return f"{label} carries a bad peeled line"
            continue
        sha, _, ref = line.partition(b" ")
        if HEX40.match(sha + b"\n") is None:
            return f"{label} carries a line that is not a packed ref"
        try:
            name = ref.decode("ascii")
        except UnicodeDecodeError:
            return f"{label} carries a non-ASCII ref name"
        if not _ref_name_ok(name):
            return f"{label} carries a ref name git does not write"
    return None


def _store(gd, label, d, seen=None):
    """Classify one `.git` directory, entry by entry, against what `git init` + commits writes.

    `seen` memoizes classified stores: a working tree's `.git` file, a worktree's `commondir` and a repo's
    own store all name the same directory, and each directory is classified once.
    """
    key = _norm(gd)
    seen = set() if seen is None else seen
    if key in seen:
        return None
    seen.add(key)
    ents = _entries(gd)
    if ents is None:
        return f"{label} unreadable"
    have = set()
    for name, mode, size, n in ents:
        q = gd / name
        if stat.S_ISLNK(mode):
            return f"{label}/{name} is a symlink"
        if name not in GIT_TOP:
            return f"{label}/{name} is not a plain-init entry"
        have.add(name)
        if name in GIT_DIRS:
            if not stat.S_ISDIR(mode):
                return f"{label}/{name} is not a directory"
            continue
        if not stat.S_ISREG(mode):
            return f"{label}/{name} is not a regular file"
        if _linked(mode, n):
            return f"{label}/{name} has more than one hard link"
        if name == "HEAD":
            body = _read(q, 200)
            if body is None or HEAD_REF.match(body) is None:
                return f"{label}/HEAD is not a plain branch HEAD"
        elif name == "ORIG_HEAD":
            body = _read(q, 200)
            if body is None or HEX40.match(body) is None:
                return f"{label}/ORIG_HEAD is not a 40-hex sha"
        elif name == "COMMIT_EDITMSG":
            if size > TEXT_CAP:
                return f"{label}/COMMIT_EDITMSG exceeds {TEXT_CAP} bytes"
        elif name == "config":
            why = _config(q, label)
            if why:
                return why
        elif name == "description":
            if size > 4096:
                return f"{label}/description exceeds 4096 bytes"
        elif name == "index":
            if size > INDEX_CAP:
                return f"{label}/index exceeds {INDEX_CAP} bytes"
        elif name == "packed-refs":
            why = _packed(q, label)
            if why:
                return why
    for req in ("HEAD", "config", "objects", "refs"):
        if req not in have:
            return f"{label} has no {req}"
    if "hooks" in have:
        why = _hooks(gd / "hooks", f"{label}/hooks")
        if why:
            return why
    if "info" in have:
        inner = _entries(gd / "info")
        if inner is None:
            return f"{label}/info unreadable"
        for name, mode, _s, _n in inner:
            if stat.S_ISLNK(mode) or not stat.S_ISREG(mode) or name != "exclude":
                return f"{label}/info/{name} is not git's exclude file"
            if _linked(mode, _n):
                return f"{label}/info/{name} has more than one hard link"
    if "logs" in have:
        why = _logs(gd / "logs", f"{label}/logs")
        if why:
            return why
    if "worktrees" in have:
        why = _worktrees(gd / "worktrees", f"{label}/worktrees", d, seen)
        if why:
            return why
    why = _objects(gd / "objects", f"{label}/objects", d)
    if why:
        return why
    why = _refs(gd / "refs", f"{label}/refs")
    if why:
        return why
    return None


def _worktrees(p, label, d, seen):
    """Classify `.git/worktrees`: one per-worktree metadata dir per linked worktree."""
    ents = _entries(p)
    if ents is None:
        return f"{label} unreadable"
    for name, mode, _s, _n in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{label}/{name} is a symlink"
        if not stat.S_ISDIR(mode):
            return f"{label}/{name} is not a directory"
        if not SAFE_NAME.match(name):
            return f"{label}/{name} has a name git does not write"
        why = _worktree(q, f"{label}/{name}", d, seen)
        if why:
            return why
    return None


def _worktree(p, label, d, seen):
    """Classify one per-worktree metadata dir: `.git/worktrees/<name>`, or the dir a `.git` file names.

    Git writes `gitdir` (a back-pointer to the worktree's `.git` file), `commondir` (the common store),
    `HEAD`, the per-worktree `index` stat cache, `ORIG_HEAD`, `logs/HEAD` and an empty `refs/`. Both pointers
    must resolve inside `d`, and the common store is then classified as a store.
    """
    ents = _entries(p)
    if ents is None:
        return f"{label} unreadable"
    have = set()
    for name, mode, size, n in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{label}/{name} is a symlink"
        if name not in WORKTREE_TOP:
            return f"{label}/{name} is not worktree metadata git writes"
        have.add(name)
        if name in WORKTREE_DIRS:
            if not stat.S_ISDIR(mode):
                return f"{label}/{name} is not a directory"
            continue
        if not stat.S_ISREG(mode):
            return f"{label}/{name} is not a regular file"
        if _linked(mode, n):
            return f"{label}/{name} has more than one hard link"
        if name == "HEAD":
            body = _read(q, 200)
            if body is None or HEAD_REF.match(body) is None:
                return f"{label}/HEAD is not a plain branch HEAD"
        elif name == "ORIG_HEAD":
            body = _read(q, 200)
            if body is None or HEX40.match(body) is None:
                return f"{label}/ORIG_HEAD is not a 40-hex sha"
        elif name == "index":
            if size > INDEX_CAP:
                return f"{label}/index exceeds {INDEX_CAP} bytes"
    for req in ("HEAD", "gitdir", "commondir"):
        if req not in have:
            return f"{label} has no {req}"
    _back, why = _file_ref(p / "gitdir", f"{label}/gitdir", p, d, False)
    if why:
        return why
    common, why = _dir_ref(p / "commondir", f"{label}/commondir", p, d, False)
    if why:
        return why
    if "logs" in have:
        why = _logs(p / "logs", f"{label}/logs")
        if why:
            return why
    if "refs" in have:
        why = _refs(p / "refs", f"{label}/refs")
        if why:
            return why
    return _store(common, f"{label}/commondir store", d, seen)


def _gitfile_store(target, label, d, seen):
    """A `.git` file names a store (n21) or, when it carries `commondir`, a per-worktree metadata dir (n20)."""
    ents = _entries(target)
    if ents is None:
        return f"{label} unreadable"
    if "commondir" in {name for name, _m, _s, _n in ents}:
        return _worktree(target, label, d, seen)
    return _store(target, label, d, seen)


# ---------- the decision ----------


def breach(d, argv, tool):
    """Refuse (one-line reason) or admit (None).

    No git child is ever started. Measured (receipt `paths-*.out`, `gitleg*.sh`): every git subcommand
    (`-C <repo>` and `cd <repo>` alike) resolves the worktree path component-wise and stats `d`'s ancestors
    with `newfstatat`, i.e. paths under the build scratch outside `d` — exactly what this fence advertises it
    never touches, and what the round-46 counter's B3/B5 legs count. The store classification below is the
    proof: a store that matches the plain-init allowlist cannot have its config, refs or objects anywhere but
    under `d`, so `rev-parse --show-toplevel`/`--git-common-dir` have nothing left to add.
    """
    try:
        dpath = pathlib.Path(d)
        st = os.lstat(dpath)
    except (OSError, ValueError, TypeError):
        return "fixture dir cannot be lstat'ed"
    if stat.S_ISLNK(st.st_mode):
        return "fixture dir is a symlink"
    if not stat.S_ISDIR(st.st_mode):
        return "fixture dir is not a directory"
    d = pathlib.Path(_norm(dpath))
    vals, why = _argv(d, tool, argv)
    if why:
        return why
    repos, gitfiles, why = _tree(d)
    if why:
        return why
    seen = set()
    for repo in repos:
        why = _store(repo / ".git", f"{_rel(repo / '.git', d)}", d, seen)
        if why:
            return why
    for repo, target in gitfiles:
        why = _gitfile_store(target, f"{_rel(target, d)} (via {_rel(repo / '.git', d)})", d, seen)
        if why:
            return why
    lane_tok = vals.get("--lane")
    if not isinstance(lane_tok, str):
        return "argv names no lane to prove"
    lane = pathlib.Path(_norm(lane_tok if lane_tok.startswith("/") else os.path.join(str(d), lane_tok)))
    try:
        lst = os.lstat(lane)
    except OSError:
        return f"--lane {lane_tok!r} does not exist inside the fixture"
    if stat.S_ISLNK(lst.st_mode):
        return f"--lane {lane_tok!r} is a symlink"
    if not stat.S_ISDIR(lst.st_mode):
        return f"--lane {lane_tok!r} is not a directory"
    if _norm(lane) not in {_norm(r) for r in repos} | {_norm(r) for r, _t in gitfiles}:
        return f"--lane {lane_tok!r} is not a repository inside the fixture"
    return None

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
worktree metadata. Variant B (round 50 C1 repair candidate) inverts the burden in two phases: first every pointer git itself
writes — a `.git` gitfile, `commondir`, `gitdir`, `objects/info/alternates` — is RESOLVED to a real path and
required to stay inside `d`, closing over the store graph; then every resolved store is classified against a
small allowlist of bytes git writes. A pointer that escapes `d` is refused where it is read, so the
classification never has to guess what a redirection means; and nothing is admitted until every byte the
decision depends on has been classified, so anything unclassified is refused.

Structure:
  1. `d` itself must be a real directory (lstat, never followed).
  2. argv must be the tool's exact option shape; every value must be a path that stays inside `d` lexically
     (no `..`, no absolute escape, no NUL, no `{...}` placeholder we cannot resolve).
  3. one walk of `d` proves the tree has no symlink and no special file anywhere, and collects every directory
     holding a real `.git` directory (a `.git` file is refused).
  4. each collected store is classified entry by entry against a plain-init allowlist: `HEAD`, `ORIG_HEAD`,
     `COMMIT_EDITMSG`, `config`, `description`, `hooks/` (`*.sample` only), `index`, `info/exclude` only
     (so no `alternates`), `logs/`, `objects/` (2-hex/38-hex loose objects, empty `info/`, pack files only),
     `refs/heads|tags` (40-hex refs), `packed-refs`. `config` is parsed line by line against a `[core]` key
     allowlist; any CR, any non-ASCII byte, any section or key not listed, or any line the parser does not
     fully understand is refused. This is what closes the CR/BOM/includeIf/attributesFile/worktree family.
  5. `--lane` must be one of the collected repositories.
  6. no git child is started at all: measured, every git subcommand resolves the fixture path component-wise
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

ORDER_SHAPE = ("--lane", "--claims", "--receipt")
ANCHOR_OPTS = {"--lane": True, "--evidence-ref": True, "--verbose": False}

HEX40 = re.compile(rb"\A[0-9a-f]{40}(?:\n)?\Z")
HEAD_REF = re.compile(rb"\Aref: refs/heads/[A-Za-z0-9_][A-Za-z0-9._/-]*\n\Z")
SECTION_LINE = re.compile(rb"\A\[([A-Za-z][A-Za-z0-9.-]*)(?: \"([A-Za-z0-9_][A-Za-z0-9._-]*)\")?\]\Z")
KEY_LINE = re.compile(rb"\A([A-Za-z][A-Za-z0-9-]*)(?:[ \t]*=[ \t]*([\x20-\x7e]*))?\Z")
GITFILE_LINE = re.compile(rb"\Agitdir: ([^\x00-\x1f]+)\n\Z")
SHA_NAME = re.compile(r"\A[0-9a-f]{40}\Z", re.ASCII)
FETCH_LINE = re.compile(rb"\A[0-9a-f]{40}\t[^\x00-\x08\x0b-\x1f\x7f]*\Z")
REFSPEC = re.compile(r"\A\+?refs/[A-Za-z0-9._*/-]+:refs/[A-Za-z0-9._*/-]+\Z", re.ASCII)
REMOTE_URL = re.compile(r"\A(?:https?|ssh|git)://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+\Z", re.ASCII)
OBJ_DIR = re.compile(r"\A[0-9a-f]{2}\Z", re.ASCII)
OBJ_FILE = re.compile(r"\A[0-9a-f]{38}\Z", re.ASCII)
PACK_FILE = re.compile(r"\A[A-Za-z0-9_][A-Za-z0-9._-]*\.(?:pack|idx|rev|keep|bitmap|mtimes)\Z", re.ASCII)
SAFE_NAME = re.compile(r"\A[A-Za-z0-9_][A-Za-z0-9._-]*\Z", re.ASCII)
REF_PATH = re.compile(r"\A[A-Za-z0-9_][A-Za-z0-9._/-]*\Z", re.ASCII)

GITFILE_CAP = 1 << 12       # a `.git` gitfile / `commondir` / `gitdir` / `alternates` larger than this is refused

GIT_TOP = {"HEAD", "ORIG_HEAD", "COMMIT_EDITMSG", "FETCH_HEAD", "config", "description", "hooks", "index",
           "info", "logs", "objects", "refs", "packed-refs", "shallow", "worktrees"}
GIT_DIRS = {"hooks", "info", "logs", "objects", "refs", "worktrees"}
WT_TOP = {"HEAD", "ORIG_HEAD", "commondir", "gitdir", "index", "logs", "refs"}   # `git worktree add` metadata
REFS_DIRS = {"heads": "plain", "tags": "plain", "notes": "plain", "remotes": "remotes", "replace": "sha"}
REFS_FILES = {"stash"}                     # `git stash` writes `refs/stash` directly under `refs/`
OBJ_INFO = {"alternates": "alternates", "commit-graph": "file", "packs": "file"}
INFO_FILES = {"exclude": "plain", "refs": "refs"}
CFG_SECTIONS = {"core", "branch", "extensions", "remote", "user"}
CFG_SUBSECTION = {"remote", "branch"}
CFG_KEYS = {
    ("core", "repositoryformatversion"): "version",
    ("core", "filemode"): "bool",
    ("core", "bare"): "false",
    ("core", "logallrefupdates"): "bool",
    ("core", "ignorecase"): "bool",
    ("core", "precomposeunicode"): "bool",
    ("core", "symlinks"): "bool",
    ("extensions", "relativeworktrees"): "bool",
    ("user", "name"): "text",
    ("user", "email"): "text",
    ("remote", "url"): "url",
    ("remote", "fetch"): "refspec",
    ("branch", "remote"): "text",
    ("branch", "merge"): "refname",
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


# ---------- pointer resolution (phase 1: every indirection becomes a real path inside `d`) ----------


def _isreg(p):
    try:
        return stat.S_ISREG(os.lstat(str(p)).st_mode)
    except OSError:
        return False


def _chain_ok(p, d):
    """Every component of `p` between `d` and `p` must exist and be a real directory (the last one included).
    Then the lexical path IS the real path: no symlink is ever followed, so the decision never names a path
    outside `d` even to lstat it. This is what lets the resolution pass stay inside the advertisement."""
    p, d = pathlib.Path(_norm(p)), pathlib.Path(_norm(d))
    rel = os.path.relpath(str(p), str(d))
    cur = d
    for part in rel.split(os.sep):
        if part in ("", "."):
            continue
        cur = cur / part
        try:
            m = os.lstat(cur).st_mode
        except OSError:
            return f"{_rel(cur, d)} does not exist"
        if stat.S_ISLNK(m):
            return f"{_rel(cur, d)} is a symlink"
    return None


def _resolve(base, raw, d):
    """Resolve one pointer value (`gitdir:` target, `commondir`, an `alternates` row) to a path inside `d`.

    The lexical path must stay inside `d` (a `..` that leaves and comes back is normalised first) and every
    component below `d` must be a real directory, so the resolved path is also the real path. An absolute
    pointer is accepted only when it already names a path inside `d` (git writes absolute gitfiles for
    `--separate-git-dir`; a fixture may rewrite them, the fence must still judge what is there)."""
    try:
        s = raw.decode("utf-8") if isinstance(raw, bytes) else str(raw)
    except UnicodeDecodeError:
        return None, "pointer is not UTF-8"
    if not s:
        return None, "pointer is empty"
    if "\x00" in s or "\r" in s or "\n" in s:
        return None, "pointer carries a control byte"
    p = s if os.path.isabs(s) else os.path.join(str(base), s)
    lex = pathlib.Path(_norm(p))
    if not _inside(lex, d):
        return None, f"pointer {s!r} leaves the fixture"
    why = _chain_ok(lex, d)
    if why:
        return None, f"pointer {s!r}: {why}"
    return lex, None


def _pointer(p, base, d):
    """Read one single-line pointer file and resolve it; anything else about the file is a refusal."""
    raw = _read(p, GITFILE_CAP)
    if raw is None:
        return None, f"{_rel(p, d)} unreadable"
    if len(raw) > GITFILE_CAP:
        return None, f"{_rel(p, d)} exceeds {GITFILE_CAP} bytes"
    if raw.endswith(b"\n"):
        raw = raw[:-1]
    return _resolve(base, raw, d)


def _gitfile_target(p, d):
    """`<worktree>/.git` is a file: it must be exactly one `gitdir: <path>` line naming a path inside `d`."""
    raw = _read(p, GITFILE_CAP)
    if raw is None:
        return None, f"{_rel(p, d)} unreadable"
    if len(raw) > GITFILE_CAP:
        return None, f"{_rel(p, d)} exceeds {GITFILE_CAP} bytes"
    m = GITFILE_LINE.match(raw)
    if m is None:
        return None, f"{_rel(p, d)} is not a single gitdir: line"
    return _resolve(p.parent, m.group(1), d)


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
    """Return (repos, gitfiles, reason): every directory holding a real `.git` dir, every directory whose `.git`
    is a gitfile (resolved later), after refusing symlinks and special files anywhere in the fixture. A `.git`
    file is only a pointer and must be exactly one `gitdir: <path>` line; a tree with no repository is not a
    refusal here (the `--lane` check refuses it)."""
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
                _target, why = _gitfile_target(p, d)
                if why:
                    return None, None, why
                gitfiles.append(t)
    if len(repos) + len(gitfiles) > REPO_CAP:
        return None, None, f"fixture holds more than {REPO_CAP} repos"
    return repos, gitfiles, None


# ---------- fact 4: the store, classified against the plain-init allowlist ----------


def _config_url(v, d, root):
    """A remote URL may name a network transport, or a path that stays inside `d`. A path that leaves `d` is
    refused: `git fetch` would read it. `root` is the worktree the relative path is resolved against."""
    if REMOTE_URL.match(v):
        return None
    if "://" in v:
        return f"url {v!r} is not a plain network URL"
    p = v if os.path.isabs(v) else os.path.join(str(root), v)
    lex = pathlib.Path(_norm(p))
    if not _inside(lex, d):
        return f"url {v!r} resolves outside the fixture"
    why = _chain_ok(lex, d)
    if why:
        return f"url {v!r}: {why}"
    return None


def _config(p, label, d, root):
    """Parse `.git/config` strictly against an allowlist of the keys git itself writes for a plain init plus the
    classes this population holds. Anything the parser does not fully classify is refused. `root` is the
    directory a relative `remote.*.url` is resolved against (the worktree git runs in)."""
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
    sect = sub = None
    version, ext = None, False
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
            sub = m.group(2).decode("ascii") if m.group(2) else None
            if sect not in CFG_SECTIONS:
                return f"{label}/config section [{sect}] is not allowlisted"
            if (sub is not None) != (sect in CFG_SUBSECTION):
                return f"{label}/config section [{sect}] has a subsection git does not write"
            if sub is not None and not SAFE_NAME.match(sub):
                return f"{label}/config subsection {sub!r} is not a plain name"
            continue
        if sect is None:
            return f"{label}/config key line {s[:40]!r} precedes any section"
        m = KEY_LINE.match(s)
        if m is None:
            return f"{label}/config line {s[:40]!r} is not a plain key=value"
        key = m.group(1).decode("ascii").lower()
        need = CFG_KEYS.get((sect, key))
        if need is None:
            return f"{label}/config key {sect}.{key} is not allowlisted"
        if m.group(2) is None:
            if need != "bool":
                return f"{label}/config key {sect}.{key} needs a value"
            continue
        v = m.group(2).decode("ascii")
        if need == "bool":
            if v.lower() not in BOOL:
                return f"{label}/config {sect}.{key}={v!r} is not a boolean"
        elif need == "false":
            if v.lower() not in FALSEY:
                return f"{label}/config {sect}.{key} must be false"
        elif need == "version":
            if v not in ("0", "1"):
                return f"{label}/config {sect}.{key} must be 0 or 1"
            version = v
        elif need == "text":
            if not 0 < len(v) <= 512:
                return f"{label}/config {sect}.{key} value is empty or over 512 bytes"
        elif need == "refname":
            if not v.startswith("refs/") or not _ref_name_ok(v):
                return f"{label}/config {sect}.{key}={v!r} is not a ref name git writes"
        elif need == "refspec":
            if REFSPEC.match(v) is None or ".." in v:
                return f"{label}/config {sect}.{key}={v!r} is not a plain refspec"
        elif need == "url":
            why = _config_url(v, d, root)
            if why:
                return f"{label}/config {sect}.{key}: {why}"
        if sect == "extensions":
            ext = True
    if ext and version != "1":
        return f"{label}/config extensions need repositoryformatversion 1"
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
        if stat.S_ISREG(mode):
            if name not in REFS_FILES:
                return f"{label}/{name} is not a ref name git writes"
            body = _read(q, 200)
            if body is None or HEX40.match(body) is None:
                return f"{_rel(q, label)} is not a 40-hex ref"
            continue
        if not stat.S_ISDIR(mode):
            return f"{label}/{name} is not a directory"
        kind = REFS_DIRS.get(name)
        if kind is None:
            return f"{label}/{name} is not a ref namespace git writes"
        why = _ref_tree(q, label, kind)
        if why:
            return why
    return None


def _ref_tree(p, label, kind):
    """Classify one ref namespace subtree. `plain`: git's usual name shape with 40-hex leaves. `sha`: names are
    object ids (`refs/replace`). `remotes`: one remote name, then a plain subtree."""
    ents = _entries(p)
    if ents is None:
        return f"{_rel(p, label)} unreadable"
    for name, mode, _s, _n in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{_rel(q, label)} is a symlink"
        if _linked(mode, _n):
            return f"{_rel(q, label)} has more than one hard link"
        if kind == "sha":
            if not stat.S_ISREG(mode) or SHA_NAME.match(name) is None:
                return f"{_rel(q, label)} is not a 40-hex replace ref"
            body = _read(q, 200)
            if body is None or HEX40.match(body) is None:
                return f"{_rel(q, label)} is not a 40-hex ref"
            continue
        if kind == "remotes":
            if not stat.S_ISDIR(mode) or SAFE_NAME.match(name) is None:
                return f"{_rel(q, label)} is not a remote name git writes"
            why = _ref_tree(q, label, "plain")
            if why:
                return why
            continue
        if stat.S_ISDIR(mode):
            if not _ref_name_ok(name):
                return f"{_rel(q, label)} has a name git does not write"
            why = _ref_tree(q, label, kind)
            if why:
                return why
            continue
        if not stat.S_ISREG(mode):
            return f"{_rel(q, label)} is a special file"
        if not _ref_name_ok(name):
            return f"{_rel(q, label)} has a name git does not write"
        body = _read(q, 200)
        if body is None:
            return f"{_rel(q, label)} unreadable"
        if HEX40.match(body) is None:
            return f"{_rel(q, label)} is not a 40-hex ref"
    return None


def _hex_lines(p, label, rx):
    """Every non-empty line must match `rx` after a newline is appended (HEX40-style anchored patterns)."""
    raw = _read(p, CONFIG_CAP)
    if raw is None:
        return f"{_rel(p, label)} unreadable"
    if len(raw) > CONFIG_CAP:
        return f"{_rel(p, label)} exceeds {CONFIG_CAP} bytes"
    for line in raw.split(b"\n"):
        if not line:
            continue
        if rx.match(line + b"\n") is None:
            return f"{_rel(p, label)} carries a line git does not write"
    return None


def _alternates(p, label, d, queue):
    """`objects/info/alternates`: each row names another object directory, resolved relative to the object
    database itself (`p` is `<store>/objects/info/alternates`). A row that leaves `d` is refused here; a row
    that stays is queued and classified with the same object-store rules."""
    raw = _read(p, GITFILE_CAP)
    if raw is None:
        return f"{_rel(p, label)} unreadable"
    if len(raw) > GITFILE_CAP:
        return f"{_rel(p, label)} exceeds {GITFILE_CAP} bytes"
    for line in raw.split(b"\n"):
        if not line:
            continue
        target, why = _resolve(p.parent.parent, line, d)
        if why:
            return f"{_rel(p, label)} row: {why}"
        try:
            m = os.lstat(target).st_mode
        except OSError:
            return f"{_rel(p, label)} names {_rel(target, d)} which does not exist"
        if stat.S_ISLNK(m) or not stat.S_ISDIR(m):
            return f"{_rel(p, label)} names {_rel(target, d)} which is not a directory"
        queue.append(target)
    return None


def _objects(p, label, d, queue):
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
            for iname, imode, isize, inl in inner:
                qq = q / iname
                if stat.S_ISLNK(imode):
                    return f"{_rel(qq, label)} is a symlink"
                if _linked(imode, inl):
                    return f"{_rel(qq, label)} has more than one hard link"
                if not stat.S_ISREG(imode):
                    return f"{_rel(qq, label)} is not a regular file"
                need = OBJ_INFO.get(iname)
                if need is None:
                    return f"{label}/info/{iname} is not an object-info file git writes"
                if need == "alternates":
                    why = _alternates(qq, label, d, queue)
                    if why:
                        return why
                elif isize > CONFIG_CAP:
                    return f"{_rel(qq, label)} exceeds {CONFIG_CAP} bytes"
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
    """A reflog lives at `HEAD` or under a ref namespace git writes, with git's own name shape."""
    if rel in ("HEAD", "refs/stash"):
        return True
    m = re.fullmatch(r"refs/(?:heads|tags|notes)/(.+)", rel, re.ASCII)
    if m:
        return all(SAFE_NAME.match(part) for part in m.group(1).split("/"))
    m = re.fullmatch(r"refs/remotes/([A-Za-z0-9_][A-Za-z0-9._-]*)/(.+)", rel, re.ASCII)
    if m:
        return all(SAFE_NAME.match(part) for part in m.group(2).split("/"))
    return re.fullmatch(r"refs/replace/[0-9a-f]{40}", rel, re.ASCII) is not None


def _log_dir_ok(rel):
    """An intermediate reflog directory: a namespace git writes, or a prefix of a valid reflog name."""
    if rel in ("refs", "refs/heads", "refs/tags", "refs/notes", "refs/remotes", "refs/replace"):
        return True
    m = re.fullmatch(r"refs/(?:heads|tags|notes)/(.+)", rel, re.ASCII)
    if m and all(SAFE_NAME.match(part) for part in m.group(1).split("/")):
        return True
    m = re.fullmatch(r"refs/remotes/([A-Za-z0-9_][A-Za-z0-9._-]*)(?:/(.+))?", rel, re.ASCII)
    return bool(m) and (m.group(2) is None or all(SAFE_NAME.match(p) for p in m.group(2).split("/")))


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
            if not _log_dir_ok(rel):
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


def _info_refs(p, label):
    """`.git/info/refs` is what `git update-server-info` writes: `<40-hex>\\t<refname>` rows."""
    raw = _read(p, CONFIG_CAP)
    if raw is None:
        return f"{label} unreadable"
    if len(raw) > CONFIG_CAP:
        return f"{label} exceeds {CONFIG_CAP} bytes"
    for line in raw.split(b"\n"):
        if not line:
            continue
        sha, sep, ref = line.partition(b"\t")
        if not sep or HEX40.match(sha + b"\n") is None:
            return f"{label} carries a line that is not an info/refs row"
        try:
            name = ref.decode("ascii")
        except UnicodeDecodeError:
            return f"{label} carries a non-ASCII ref name"
        if not _ref_name_ok(name):
            return f"{label} carries a ref name git does not write"
    return None


def _worktrees(p, label, d):
    """`<store>/worktrees/<name>` holds one metadata directory per linked worktree; each is classified on its
    own by `_wtmeta` (discovery has already resolved it as a store root)."""
    ents = _entries(p)
    if ents is None:
        return f"{label} unreadable"
    for name, mode, _s, _n in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{_rel(q, label)} is a symlink"
        if not stat.S_ISDIR(mode) or SAFE_NAME.match(name) is None:
            return f"{_rel(q, label)} is not a worktree metadata dir git writes"
    return None


def _wtrefs(p, label):
    """`worktrees/<name>/refs` holds only the worktree-local namespaces git writes (`refs/bisect`,
    `refs/worktree`), each a plain 40-hex ref tree. `git worktree add` also leaves the directory empty."""
    ents = _entries(p)
    if ents is None:
        return f"{label} unreadable"
    for name, mode, _s, n in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{_rel(q, label)} is a symlink"
        if _linked(mode, n):
            return f"{_rel(q, label)} has more than one hard link"
        if not stat.S_ISDIR(mode) or name not in ("bisect", "worktree"):
            return f"{_rel(q, label)} is not a worktree-local ref namespace git writes"
        why = _ref_tree(q, label, "plain")
        if why:
            return why
    return None


def _wtmeta(gd, label, d):
    """Classify one linked-worktree metadata directory (`git worktree add`): `commondir` and `gitdir` are
    pointers, resolved here and required to close back onto this directory and a store inside `d`."""
    ents = _entries(gd)
    if ents is None:
        return f"{label} unreadable"
    have = set()
    for name, mode, size, n in ents:
        q = gd / name
        if stat.S_ISLNK(mode):
            return f"{label}/{name} is a symlink"
        if name not in WT_TOP:
            return f"{label}/{name} is not a worktree metadata entry git writes"
        have.add(name)
        if name in ("logs", "refs"):
            if not stat.S_ISDIR(mode):
                return f"{label}/{name} is not a directory"
            continue
        if not stat.S_ISREG(mode):
            return f"{label}/{name} is not a regular file"
        if _linked(mode, n):
            return f"{label}/{name} has more than one hard link"
        if name == "HEAD":
            body = _read(q, 200)
            if body is None or not (HEAD_REF.match(body) or HEX40.match(body)):
                return f"{label}/HEAD is neither a branch HEAD nor a 40-hex sha"
        elif name == "ORIG_HEAD":
            body = _read(q, 200)
            if body is None or HEX40.match(body) is None:
                return f"{label}/ORIG_HEAD is not a 40-hex sha"
        elif name == "index":
            if size > INDEX_CAP:
                return f"{label}/index exceeds {INDEX_CAP} bytes"
        elif name == "commondir":
            target, why = _pointer(q, gd, d)
            if why:
                return f"{label}/commondir: {why}"
            try:
                m = os.lstat(target).st_mode
            except OSError:
                return f"{label}/commondir names {_rel(target, d)} which does not exist"
            if stat.S_ISLNK(m) or not stat.S_ISDIR(m):
                return f"{label}/commondir names {_rel(target, d)} which is not a directory"
        elif name == "gitdir":
            target, why = _pointer(q, gd, d)
            if why:
                return f"{label}/gitdir: {why}"
            if not _isreg(target):
                return f"{label}/gitdir names {_rel(target, d)} which is not a regular file"
            back, why = _gitfile_target(target, d)
            if why:
                return f"{label}/gitdir: {why}"
            if _norm(back) != _norm(gd):
                return f"{label}/gitdir does not point back at this metadata dir"
    for req in ("HEAD", "commondir", "gitdir"):
        if req not in have:
            return f"{label} has no {req}"
    if "logs" in have:
        why = _logs(gd / "logs", f"{label}/logs")
        if why:
            return why
    if "refs" in have:
        why = _wtrefs(gd / "refs", f"{label}/refs")
        if why:
            return why
    return None


def _store(gd, label, kind, d, wt, queue):
    """Classify one resolved store directory.

    `kind` `store`: what `git init` + commits writes, plus `FETCH_HEAD`/`shallow` and the `worktrees/` metadata
    git writes when a linked worktree exists. `kind` `wtmeta`: one per-worktree metadata dir (see `_wtmeta`)."""
    if kind == "wtmeta":
        return _wtmeta(gd, label, d)
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
            if body is None or not (HEAD_REF.match(body) or HEX40.match(body)):
                return f"{label}/HEAD is neither a branch HEAD nor a 40-hex sha"
        elif name == "ORIG_HEAD":
            body = _read(q, 200)
            if body is None or HEX40.match(body) is None:
                return f"{label}/ORIG_HEAD is not a 40-hex sha"
        elif name == "shallow":
            why = _hex_lines(q, label, HEX40)
            if why:
                return why
        elif name == "FETCH_HEAD":
            why = _hex_lines(q, label, FETCH_LINE)
            if why:
                return why
        elif name == "COMMIT_EDITMSG":
            if size > TEXT_CAP:
                return f"{label}/COMMIT_EDITMSG exceeds {TEXT_CAP} bytes"
        elif name == "config":
            why = _config(q, label, d, wt if wt is not None else gd.parent)
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
    if "worktrees" in have:
        why = _worktrees(gd / "worktrees", label, d)
        if why:
            return why
    if "hooks" in have:
        why = _hooks(gd / "hooks", f"{label}/hooks")
        if why:
            return why
    if "info" in have:
        inner = _entries(gd / "info")
        if inner is None:
            return f"{label}/info unreadable"
        for name, mode, _s, _n in inner:
            q = gd / "info" / name
            if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
                return f"{label}/info/{name} is not a git-written info file"
            if _linked(mode, _n):
                return f"{label}/info/{name} has more than one hard link"
            need = INFO_FILES.get(name)
            if need is None:
                return f"{label}/info/{name} is not a git-written info file"
            if need == "refs":
                why = _info_refs(q, f"{label}/info/{name}")
                if why:
                    return why
    if "logs" in have:
        why = _logs(gd / "logs", f"{label}/logs")
        if why:
            return why
    why = _objects(gd / "objects", f"{label}/objects", d, queue)
    if why:
        return why
    why = _refs(gd / "refs", f"{label}/refs")
    if why:
        return why
    return None


# ---------- the decision ----------


def _discover(d, repos, gitfiles):
    """Phase 1: resolve every pointer to a real path inside `d` and close over the store graph.

    Returns (stores, queue, reason). `stores` maps a resolved directory to (kind, worktree): `store` for what
    `git init` writes, `wtmeta` for one linked-worktree metadata dir. `queue` is the list of resolved alternate
    object directories still to classify. A pointer that leaves `d` is refused here, before its target is read.
    """
    stores, pend, queue = {}, [], []

    def want(path, kind, wt):
        rp = pathlib.Path(_norm(path))
        if rp not in stores:
            stores[rp] = (kind, wt)
            pend.append(rp)

    for repo in repos:
        want(repo / ".git", "store", repo)
    for worktree in gitfiles:
        target, why = _gitfile_target(worktree / ".git", d)
        if why:
            return None, None, why
        try:
            m = os.lstat(target).st_mode
        except OSError:
            return None, None, f"{_rel(worktree / '.git', d)} names {_rel(target, d)} which does not exist"
        if stat.S_ISLNK(m) or not stat.S_ISDIR(m):
            return None, None, f"{_rel(worktree / '.git', d)} names {_rel(target, d)} which is not a directory"
        want(target, "auto", worktree)
    while pend:
        root = pend.pop(0)
        kind, _wt = stores[root]
        ents = _entries(root)
        if ents is None:
            return None, None, f"{_rel(root, d)} unreadable"
        names = {e[0] for e in ents}
        if kind == "auto":
            kind = "wtmeta" if "commondir" in names or "gitdir" in names else "store"
            stores[root] = (kind, stores[root][1])
        if kind == "wtmeta":
            if "commondir" in names:
                target, why = _pointer(root / "commondir", root, d)
                if why:
                    return None, None, f"{_rel(root, d)}/commondir: {why}"
                try:
                    m = os.lstat(target).st_mode
                except OSError:
                    return None, None, f"{_rel(root, d)}/commondir names {_rel(target, d)} which does not exist"
                if stat.S_ISLNK(m) or not stat.S_ISDIR(m):
                    return None, None, f"{_rel(root, d)}/commondir names {_rel(target, d)} which is not a directory"
                want(target, "auto", None)
            continue
        # a plain store has no `commondir`/`gitdir` at its root: those are worktree metadata
        if "commondir" in names or "gitdir" in names:
            return None, None, f"{_rel(root, d)} carries worktree metadata at a store root"
        if "worktrees" in names:
            kids = _entries(root / "worktrees")
            if kids is None:
                return None, None, f"{_rel(root / 'worktrees', d)} unreadable"
            for name, mode, _s, _n in kids:
                q = root / "worktrees" / name
                if stat.S_ISLNK(mode):
                    return None, None, f"{_rel(q, d)} is a symlink"
                if not stat.S_ISDIR(mode) or SAFE_NAME.match(name) is None:
                    return None, None, f"{_rel(q, d)} is not a worktree metadata dir git writes"
                want(q, "wtmeta", None)
    return stores, queue, None


def breach(d, argv, tool):
    """Refuse (one-line reason) or admit (None).

    No git child is ever started. Measured (receipt `paths-*.out`, `gitleg*.sh`): every git subcommand
    (`-C <repo>` and `cd <repo>` alike) resolves the worktree path component-wise and stats `d`'s ancestors
    with `newfstatat`, i.e. paths under the build scratch outside `d` — exactly what this fence advertises it
    never touches, and what the round-46 counter's B3/B5 legs count.

    The decision is two passes over the same tree. Phase 1 (`_discover`) resolves every pointer git writes — a
    `.git` gitfile, `commondir`, `gitdir`, `objects/info/alternates` — to a real path and refuses it if that
    path leaves `d`, closing over the resulting store graph; phase 2 classifies every resolved directory entry
    by entry against a small allowlist of bytes git writes. Together they are the proof: a store that matches
    the allowlist cannot have its config, refs or objects anywhere but under `d`, and every indirection it does
    have has been followed to a path inside `d`, so `rev-parse --show-toplevel`/`--git-common-dir` have nothing
    left to add.
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
    stores, queue, why = _discover(d, repos, gitfiles)
    if why:
        return why
    for root in sorted(stores, key=str):
        kind, wt = stores[root]
        why = _store(root, _rel(root, d), kind, d, wt, queue)
        if why:
            return why
    seen = set()
    while queue:
        objs = queue.pop(0)
        if objs in seen:
            continue
        seen.add(objs)
        why = _objects(objs, _rel(objs, d), d, queue)
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
    if _norm(lane) not in {_norm(r) for r in [*repos, *gitfiles]}:
        return f"--lane {lane_tok!r} is not a repository inside the fixture"
    return None

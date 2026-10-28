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
SECTION_LINE = re.compile(rb"\A\[([A-Za-z][A-Za-z0-9.-]*)\]\Z")
KEY_LINE = re.compile(rb"\A([A-Za-z][A-Za-z0-9-]*)(?:[ \t]*=[ \t]*([A-Za-z0-9._-]*))?\Z")
OBJ_DIR = re.compile(r"\A[0-9a-f]{2}\Z", re.ASCII)
OBJ_FILE = re.compile(r"\A[0-9a-f]{38}\Z", re.ASCII)
PACK_FILE = re.compile(r"\A[A-Za-z0-9_][A-Za-z0-9._-]*\.(?:pack|idx|rev|keep|bitmap|mtimes)\Z", re.ASCII)
SAFE_NAME = re.compile(r"\A[A-Za-z0-9_][A-Za-z0-9._-]*\Z", re.ASCII)
REF_PATH = re.compile(r"\A[A-Za-z0-9_][A-Za-z0-9._/-]*\Z", re.ASCII)

GIT_TOP = {"HEAD", "ORIG_HEAD", "COMMIT_EDITMSG", "config", "description", "hooks", "index", "info",
           "logs", "objects", "refs", "packed-refs"}
GIT_DIRS = {"hooks", "info", "logs", "objects", "refs"}
CFG_SECTIONS = {"core"}
CFG_KEYS = {
    ("core", "repositoryformatversion"): "0",
    ("core", "filemode"): "bool",
    ("core", "bare"): "false",
    ("core", "logallrefupdates"): "bool",
    ("core", "ignorecase"): "bool",
    ("core", "precomposeunicode"): "bool",
    ("core", "symlinks"): "bool",
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
    """Return (repos, reason): every directory holding a real `.git` dir, after refusing symlinks and
    special files anywhere in the fixture."""
    repos, seen = [], 0
    for top, dirs, files in os.walk(str(d), followlinks=False):
        seen += len(dirs) + len(files)
        if seen > ENTRY_CAP:
            return None, f"fixture tree exceeds {ENTRY_CAP} entries"
        t = pathlib.Path(top)
        keep = []
        for name in dirs:
            p = t / name
            try:
                mode = os.lstat(p).st_mode
            except OSError:
                return None, f"{_rel(p, d)} cannot be lstat'ed"
            if stat.S_ISLNK(mode):
                return None, f"{_rel(p, d)} is a symlink"
            if not stat.S_ISDIR(mode):
                return None, f"{_rel(p, d)} is not a directory"
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
                return None, f"{_rel(p, d)} cannot be lstat'ed"
            if stat.S_ISLNK(mode):
                return None, f"{_rel(p, d)} is a symlink"
            if name == ".git":
                return None, f"{_rel(p, d)} is a file (gitdir redirect), not a directory"
            if not stat.S_ISREG(mode):
                return None, f"{_rel(p, d)} is a special file"
            if os.lstat(p).st_nlink > 1:
                return None, f"{_rel(p, d)} has more than one hard link"
    if len(repos) > REPO_CAP:
        return None, f"fixture holds more than {REPO_CAP} repos"
    return repos, None


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
        if m.group(2) is None:
            if need != "bool":
                return f"{label}/config key {sect}.{key} needs a value"
            continue
        val = m.group(2).decode("ascii").lower()
        if need == "bool":
            if val not in BOOL:
                return f"{label}/config {sect}.{key}={val!r} is not a boolean"
        elif need == "false":
            if val not in FALSEY:
                return f"{label}/config {sect}.{key} must be false"
        elif need == "0":
            if val not in ("0", ""):
                return f"{label}/config {sect}.{key} must be 0"
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
        if name not in ("heads", "tags"):
            return f"{label}/{name} is not refs/heads or refs/tags"
        if not stat.S_ISDIR(mode):
            return f"{label}/{name} is not a directory"
        why = _ref_tree(q, label)
        if why:
            return why
    return None


def _ref_tree(p, label):
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
            why = _ref_tree(q, label)
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


def _objects(p, label):
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
            if inner:
                return f"{label}/info/{inner[0][0]} present (object-store redirect)"
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


def _store(gd, label):
    """Classify one `.git` directory, entry by entry, against what `git init` + commits writes."""
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
    why = _objects(gd / "objects", f"{label}/objects")
    if why:
        return why
    why = _refs(gd / "refs", f"{label}/refs")
    if why:
        return why
    return None


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
    repos, why = _tree(d)
    if why:
        return why
    for repo in repos:
        why = _store(repo / ".git", f"{_rel(repo / '.git', d)}")
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
    if _norm(lane) not in {_norm(r) for r in repos}:
        return f"--lane {lane_tok!r} is not a repository inside the fixture"
    return None

"""Fixture fence (round-49 C1, variant B: kind classification): admit a fixture only when the KIND of every
store entry, ref, config key and argv value is classified, and every classified byte lies inside `d`.

Contract (frozen, `plans/round45_c1_verify.py` docstring):

    breach(d: pathlib.Path, argv: list[str], tool: str) -> str | None

`d` is the fixture directory (absolute, resolved), `argv` the module's argv tail, `tool` `anchor` or `order`.
A non-empty string refuses (the reason, one line); None admits. Runs with cwd `d`, read-only, under
`strace -f -y`.

Mechanism (variant B; distinct from the round-46 variant A allowlist):
  1. `d` itself must be a real directory (lstat, never followed).
  2. argv must be the tool's exact option shape; every value must be a path that stays inside `d` lexically
     (no `..`, no absolute escape, no NUL, no newline, no `{...}` placeholder we cannot resolve).
  3. one walk of `d` proves the tree has no symlink, no special file and no multiply-linked file anywhere, and
     collects every directory holding a real `.git` directory (a `.git` file is refused: gitdir redirect).
  4. each store's TOP-LEVEL entries are classified by kind: symref-head / sha-file / message / config / index
     / text / packed-refs / hooks / info / logs / objects / refs. A name whose kind is unclassified is refused.
  5. refs are classified by REF KIND, not by a namespace allowlist: a ref path is admitted iff every component
     is a valid refname component and its content is 40-hex (object ref) or a `ref: <refs/...>` symref naming a
     valid refname. `refs/heads`, `refs/tags`, `refs/remotes`, `refs/notes` and `refs/stash` are therefore all
     admitted as the same kind (branch/tag/remote-tracking/notes/stash differ in namespace, not in kind), while
     a redirecting name (`..`, absolute, `.lock`) is not a ref name at all.
  6. `HEAD` is classified by kind: symbolic (`ref: refs/...`) or detached (one 40-hex id); anything else refused.
  7. `.git/config` is classified by SECTION/KEY KIND: redirect sections (`include`, `includeIf`, `url`) are
     refused; `[extensions]` is pinned (objectFormat=sha1, refStorage=files, worktreeConfig/preciousObjects
     false); `core` shape keys are pinned (repositoryFormatVersion=0, bare=false); every PATH-kind key must name
     a relative path that stays inside `d` and is not a symlink; every COMMAND-kind key (exec value, `!` value,
     command-valued key name) is refused; every other key is an inert scalar admitted by SHAPE (printable ASCII,
     no backslash escape, no control byte, no non-ASCII, no NUL/CR), never by a per-key allowlist.
  8. `objects/info` is classified by kind: `alternates` refused (object-store redirect); `commit-graph` and
     `commit-graphs/` admitted as opaque graph data; any other name refused. Loose objects, `objects/pack` files
     and `packed-refs` are validated by name/shape at their own kind.
  9. `--lane` must be one of the collected repositories.

Every path the decision names is lexically inside `d`, and no git child is started: git's own store discovery
resolves the worktree path component-wise and stats `d`'s ancestors (outside `d`), which the advertisement and
the counter's B3/B5 legs forbid. The kind classification is the proof instead.

Named limits: `.git/index`, `COMMIT_EDITMSG`, `description`, `logs/*`, pack files, `commit-graph` and
`multi-pack-index` are admitted by name/size/shape, not by content validation; `objects/info` admits exactly the
graph kinds above (git's `info/refs`, if written by `git update-server-info`, is refused); a directory stat's
`st_nlink` channel is not measured (only the fixture parent is padded by the counter).
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
REF_CAP = 4096              # a single ref file larger than this is refused
GRAPH_CAP = 1 << 26         # an opaque graph file larger than this is refused

ORDER_SHAPE = ("--lane", "--claims", "--receipt")
ANCHOR_OPTS = {"--lane": True, "--evidence-ref": True, "--verbose": False}

HEX40 = re.compile(rb"\A[0-9a-f]{40}(?:\n)?\Z")
SYMREF = re.compile(rb"\Aref: ([^\r\n]+)(?:\n)?\Z")
OBJ_DIR = re.compile(r"\A[0-9a-f]{2}\Z", re.ASCII)
OBJ_FILE = re.compile(r"\A[0-9a-f]{38}\Z", re.ASCII)
PACK_FILE = re.compile(r"\A[A-Za-z0-9_][A-Za-z0-9._-]*\.(?:pack|idx|rev|keep|bitmap|mtimes)\Z", re.ASCII)
GRAPH_FILE = re.compile(r"\A(?:graph-[0-9a-f]{40,64}\.graph|commit-graph)\Z", re.ASCII)
REF_COMP = re.compile(r"\A[A-Za-z0-9_][A-Za-z0-9._-]*\Z", re.ASCII)
SECTION_LINE = re.compile(rb"\A\[([A-Za-z][A-Za-z0-9.-]*)(?:[ \t]+\"([^\"\\]*)\")?\]\Z")
KEY_LINE = re.compile(rb"\A([A-Za-z][A-Za-z0-9-]*)(?:[ \t]*=[ \t]*(.*?))?\Z")
TRUE = {"true", "yes", "on", "1"}
FALSEY = {"false", "no", "off", "0", ""}

# store entry kinds: name -> kind token; a top-level name outside this table is unclassified and refused
STORE_KINDS = {
    "HEAD": "head", "ORIG_HEAD": "sha", "COMMIT_EDITMSG": "message", "config": "config",
    "description": "text", "index": "index", "packed-refs": "packed",
    "hooks": "dir", "info": "dir", "logs": "dir", "objects": "dir", "refs": "dir",
}
REQUIRED = ("HEAD", "config", "objects", "refs")

# config sections whose whole kind is a redirect: refused as a section, never parsed as scalars
REDIRECT_SECTIONS = {"include", "includeif"}
# path-kind core keys: the value names a filesystem location the store reads
CORE_PATH_KEYS = {"worktree", "attributesfile", "excludesfile", "hookspath", "templatedir", "commondir",
                  "gitdir"}
# command-kind core keys: the value is executed or names an executable
CORE_COMMAND_KEYS = {"fsmonitor", "sshcommand", "pager", "editor", "alternaterefscommand", "askpass",
                     "gitproxy"}
# key names that name a command in any section
COMMAND_NAMES = {"command", "helper", "clean", "smudge", "process", "textconv", "editor", "pager", "proxy",
                 "askpass", "uploadpack", "receivepack", "sshcommand", "hookspath", "fsmonitor"}
# key-name suffixes that name a filesystem location in any section
PATH_SUFFIXES = ("file", "path", "dir", "directory", "location")
EXTENSION_KINDS = {"objectformat": {"sha1"}, "refstorage": {"files"},
                   "worktreeconfig": FALSEY, "preciousobjects": FALSEY}


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


def _read(p, cap):
    try:
        with open(p, "rb") as fh:
            return fh.read(cap + 1)
    except OSError:
        return None


# ---------- ref kinds ----------


def _refname_ok(name):
    """git refname kind: `refs/...`, every component plain, no `.`/`..`/`.lock`/`@{`."""
    if not isinstance(name, str) or not name.startswith("refs/") or "@{" in name or ".." in name:
        return False
    if name.endswith(".") or name.endswith("/") or "\\" in name:
        return False
    parts = name.split("/")
    if len(parts) < 2:
        return False
    for part in parts:
        if not REF_COMP.match(part) or part.endswith(".lock"):
            return False
    return True


def _ref_body_ok(body):
    """A ref file's kind: object ref (40-hex) or symbolic ref to a valid refname. Returns kind or None."""
    if body is None:
        return None
    if HEX40.match(body):
        return "object"
    m = SYMREF.match(body)
    if m:
        try:
            target = m.group(1).decode("ascii")
        except UnicodeDecodeError:
            return None
        if _refname_ok(target):
            return "symbolic"
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
    """Return (repos, reason): every directory holding a real `.git` dir, after refusing symlinks, special
    files and multiply-linked files anywhere in the fixture. `.git` directories are not descended into; their
    whole content is classified by `_store`."""
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
                st = os.lstat(p)
            except OSError:
                return None, f"{_rel(p, d)} cannot be lstat'ed"
            if stat.S_ISLNK(st.st_mode):
                return None, f"{_rel(p, d)} is a symlink"
            if name == ".git":
                return None, f"{_rel(p, d)} is a file (gitdir redirect), not a directory"
            if not stat.S_ISREG(st.st_mode):
                return None, f"{_rel(p, d)} is a special file"
            if st.st_nlink > 1:
                return None, f"{_rel(p, d)} has more than one hard link"
    if len(repos) > REPO_CAP:
        return None, f"fixture holds more than {REPO_CAP} repos"
    return repos, None


# ---------- fact 4: ref kind, by namespace-agnostic name+content classification ----------


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
        if not REF_COMP.match(name) or name.endswith(".lock"):
            return f"{_rel(q, label)} is not a refname component git writes"
        if stat.S_ISDIR(mode):
            why = _ref_tree(q, label)
            if why:
                return why
            continue
        if not stat.S_ISREG(mode):
            return f"{_rel(q, label)} is a special file"
        body = _read(q, REF_CAP)
        if body is None:
            return f"{_rel(q, label)} unreadable"
        if len(body) > REF_CAP:
            return f"{_rel(q, label)} exceeds {REF_CAP} bytes"
        if _ref_body_ok(body) is None:
            return f"{_rel(q, label)} is neither a 40-hex ref nor a symbolic ref"
    return None


def _one_ref(q, label, rel):
    """Classify one ref file inside the store's ref namespace: name kind and content kind."""
    body = _read(q, REF_CAP)
    if body is None:
        return f"{_rel(q, label)} unreadable"
    if len(body) > REF_CAP:
        return f"{_rel(q, label)} exceeds {REF_CAP} bytes"
    if _ref_body_ok(body) is None:
        return f"{_rel(q, label)} is neither a 40-hex ref nor a symbolic ref"
    return None


def _refs(p, label):
    ents = _entries(p)
    if ents is None:
        return f"{label} unreadable"
    if not ents:
        return None
    for name, mode, _s, _n in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{_rel(q, label)} is a symlink"
        if _linked(mode, _n):
            return f"{_rel(q, label)} has more than one hard link"
        if not REF_COMP.match(name) or name.endswith(".lock"):
            return f"{_rel(q, label)} is not a refname component"
        if stat.S_ISDIR(mode):
            why = _ref_tree(q, label)
            if why:
                return why
            continue
        if not stat.S_ISREG(mode):
            return f"{_rel(q, label)} is a special file"
        # a ref may sit directly under refs/ (git writes refs/stash, refs/bisect/* ...)
        why = _one_ref(q, label, name)
        if why:
            return why
    return None


# ---------- fact 5: objects, pack and object-info kinds ----------


def _packs_list(p, label, packdir):
    """`objects/info/packs` kind: the dumb-HTTP pack list, `P <pack name>` lines and blank/comment lines."""
    raw = _read(p, TEXT_CAP)
    if raw is None:
        return f"{label} unreadable"
    if len(raw) > TEXT_CAP:
        return f"{label} exceeds {TEXT_CAP} bytes"
    if any(b >= 0x80 for b in raw) or b"\x00" in raw:
        return f"{label} carries an unplain byte"
    for line in raw.split(b"\n"):
        if not line or line.startswith(b"#"):
            continue
        head, _, name = line.partition(b" ")
        if head != b"P":
            return f"{label} carries a line that is not a pack entry"
        try:
            txt = name.decode("ascii")
        except UnicodeDecodeError:
            return f"{label} carries a non-ASCII pack name"
        if not PACK_FILE.match(txt) or not txt.endswith(".pack"):
            return f"{label} carries a pack name git does not write"
        if not (packdir / txt).is_file():
            return f"{label} names a pack that is not in objects/pack"
    return None


def _objects_info(p, label, packdir):
    """objects/info by kind: alternates is a redirect; commit-graph(s) and the `packs` list are store data;
    any other name is refused."""
    ents = _entries(p)
    if ents is None:
        return f"{label} unreadable"
    for name, mode, size, n in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{_rel(q, label)} is a symlink"
        if _linked(mode, n):
            return f"{_rel(q, label)} has more than one hard link"
        if name == "alternates":
            return f"{label}/alternates present (object-store redirect)"
        if name == "packs":
            if not stat.S_ISREG(mode):
                return f"{_rel(q, label)} is not a pack list"
            why = _packs_list(q, f"{label}/packs", packdir)
            if why:
                return why
            continue
        if name == "commit-graphs":
            if not stat.S_ISDIR(mode):
                return f"{_rel(q, label)} is not a directory"
            inner = _entries(q)
            if inner is None:
                return f"{_rel(q, label)} unreadable"
            for iname, imode, isize, inlink in inner:
                if stat.S_ISLNK(imode) or not stat.S_ISREG(imode):
                    return f"{_rel(q / iname, label)} is not graph data"
                if _linked(imode, inlink):
                    return f"{_rel(q / iname, label)} has more than one hard link"
                if not (GRAPH_FILE.match(iname) or iname == "commit-graph-chain"):
                    return f"{_rel(q / iname, label)} is not graph data"
                if isize > GRAPH_CAP:
                    return f"{_rel(q / iname, label)} exceeds {GRAPH_CAP} bytes"
            continue
        if not stat.S_ISREG(mode) or not GRAPH_FILE.match(name):
            return f"{_rel(q, label)} is not an object-info kind the fence classifies"
        if size > GRAPH_CAP:
            return f"{_rel(q, label)} exceeds {GRAPH_CAP} bytes"
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
            why = _objects_info(q, f"{label}/info", p / "pack")
            if why:
                return why
            continue
        if name == "pack":
            inner = _entries(q)
            if inner is None:
                return f"{label}/pack unreadable"
            for pname, pmode, _ps, _pn in inner:
                qq = q / pname
                if stat.S_ISLNK(pmode):
                    return f"{_rel(qq, label)} is a symlink"
                if not stat.S_ISREG(pmode):
                    return f"{_rel(qq, label)} is not a pack file"
                if not (PACK_FILE.match(pname) or pname == "multi-pack-index"):
                    return f"{_rel(qq, label)} is not a pack file"
                if _linked(pmode, _pn):
                    return f"{_rel(qq, label)} has more than one hard link"
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


# ---------- fact 6: logs, hooks, info, packed-refs kinds ----------


def _log_name_ok(rel):
    """A reflog lives at `HEAD` or at any valid refname under `refs/` (namespace-agnostic)."""
    if rel == "HEAD":
        return True
    return _refname_ok(rel)


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
            if not _refname_ok(rel + "/x"):
                return f"{_rel(q, label)} is not a reflog namespace"
            why = _logs(q, label, rel + "/")
            if why:
                return why
            continue
        if not stat.S_ISREG(mode):
            return f"{_rel(q, label)} is a special file"
        if not _log_name_ok(rel):
            return f"{_rel(q, label)} is not a reflog name git writes"
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


def _info_refs(p, label):
    """`.git/info/refs` kind: a plain `<40-hex>\t<refname>` list (git writes it during gc on current git)."""
    raw = _read(p, TEXT_CAP)
    if raw is None:
        return f"{label} unreadable"
    if len(raw) > TEXT_CAP:
        return f"{label} exceeds {TEXT_CAP} bytes"
    if b"\x00" in raw or b"\r" in raw or any(b >= 0x80 for b in raw):
        return f"{label} carries an unplain byte"
    for line in raw.split(b"\n"):
        if not line:
            continue
        sha, tab, ref = line.partition(b"\t")
        if not tab or HEX40.match(sha + b"\n") is None:
            return f"{label} carries a line that is not an info ref"
        try:
            name = ref.decode("ascii")
        except UnicodeDecodeError:
            return f"{label} carries a non-ASCII ref name"
        if not _refname_ok(name):
            return f"{label} carries a ref name git does not write"
    return None


def _info(p, label):
    """`.git/info` by kind: `exclude` (text) and `refs` (info-refs list); any other name refused."""
    ents = _entries(p)
    if ents is None:
        return f"{label} unreadable"
    for name, mode, _s, _n in ents:
        q = p / name
        if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
            return f"{_rel(q, label)} is not an info kind the fence classifies"
        if _linked(mode, _n):
            return f"{_rel(q, label)} has more than one hard link"
        if name == "refs":
            why = _info_refs(q, f"{label}/refs")
            if why:
                return why
            continue
        if name != "exclude":
            return f"{_rel(q, label)} is not an info kind the fence classifies"
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
        if not _refname_ok(name):
            return f"{label} carries a ref name git does not write"
    return None


# ---------- fact 7: config, by section/key kind ----------


def _plain_value(val):
    """Scalar kind: printable ASCII, no backslash escape, no control byte, no non-ASCII, no NUL/CR."""
    if b"\\" in val:
        return False
    return all(0x20 <= b <= 0x7e for b in val)


def _config_path_ok(repo, val):
    """Path kind: relative, no `..`, no `~`, lexically inside `d`, and not a symlink when it exists."""
    if not val or val.startswith("/") or val.startswith("~") or "\x00" in val:
        return False
    if any(part in ("..", "") for part in val.split("/")):
        return False
    target = os.path.join(str(repo), val)
    try:
        st = os.lstat(target)
    except OSError:
        return True                      # names nothing the fence could read
    return not stat.S_ISLNK(st.st_mode)


def _config(repo, gd, label, d):
    """Classify `.git/config` line by line. Returns None (classified) or a reason."""
    raw = _read(gd / "config", CONFIG_CAP)
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
    sect, kind = "", None
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
            kind = _section_kind(sect, m.group(2))
            if kind == "redirect":
                return f"{label}/config section [{sect}] is a redirect kind"
            if kind is None:
                return f"{label}/config section [{sect}] is not a kind the fence classifies"
            continue
        m = KEY_LINE.match(s)
        if m is None:
            return f"{label}/config line {s[:40]!r} is not a plain key=value"
        key = m.group(1).decode("ascii").lower()
        val = m.group(2)
        if val is not None and val.startswith(b'"') and val.endswith(b'"') and len(val) >= 2:
            val = val[1:-1]
        if kind == "extensions":
            allowed = EXTENSION_KINDS.get(key)
            if allowed is None:
                return f"{label}/config extension {key} is not a known store-semantics kind"
            if val is None:
                return f"{label}/config extension {key} needs a value"
            if val.decode("ascii", "replace").lower() not in allowed:
                return f"{label}/config extension {key}={val[:40]!r} is not the plain value"
            continue
        keystr = val.decode("ascii", "replace") if val is not None else ""
        pathy = (kind == "core" and key in CORE_PATH_KEYS) or key.endswith(PATH_SUFFIXES)
        commandy = ((kind == "core" and key in CORE_COMMAND_KEYS) or key in COMMAND_NAMES
                    or keystr.startswith("!"))
        if kind == "core" and key == "repositoryformatversion":
            if val is None or keystr.strip() not in ("0", ""):
                return f"{label}/config core.repositoryformatversion must be 0"
            continue
        if kind == "core" and key == "bare":
            if val is None or keystr.strip().lower() not in FALSEY:
                return f"{label}/config core.bare must be false"
            continue
        if commandy:
            return f"{label}/config key {key} is a command kind"
        if pathy:
            if val is None:
                return f"{label}/config path key {key} has no value"
            if not _plain_value(val):
                return f"{label}/config path key {key} carries an unplain value"
            try:
                text = val.decode("ascii")
            except UnicodeDecodeError:
                return f"{label}/config path key {key} is not ASCII"
            if not _config_path_ok(repo, text):
                return f"{label}/config path key {key}={text[:60]!r} does not stay inside the fixture"
            continue
        if val is not None and not _plain_value(val):
            return f"{label}/config key {sect}.{key} carries an unplain value"
    return None


def _section_kind(sect, sub):
    """Section kind: redirect | extensions | core | scalar (subsections allowed for name-bearing sections)."""
    if sect in REDIRECT_SECTIONS:
        return "redirect"
    if sect == "extensions":
        return "extensions" if sub is None else None
    if sect == "core":
        return "core" if sub is None else None
    return "scalar"


# ---------- the store ----------


def _store(repo, d):
    gd = repo / ".git"
    label = _rel(gd, d)
    ents = _entries(gd)
    if ents is None:
        return f"{label} unreadable"
    have = set()
    for name, mode, size, n in ents:
        q = gd / name
        if stat.S_ISLNK(mode):
            return f"{label}/{name} is a symlink"
        kind = STORE_KINDS.get(name)
        if kind is None:
            return f"{label}/{name} has no store-entry kind the fence classifies"
        have.add(name)
        if kind == "dir":
            if not stat.S_ISDIR(mode):
                return f"{label}/{name} is not a directory"
            continue
        if not stat.S_ISREG(mode):
            return f"{label}/{name} is not a regular file"
        if _linked(mode, n):
            return f"{label}/{name} has more than one hard link"
        if kind == "head":
            body = _read(q, REF_CAP)
            if body is None:
                return f"{label}/HEAD unreadable"
            if body.startswith(b"ref: "):
                m = SYMREF.match(body)
                if not m:
                    return f"{label}/HEAD is not a plain symbolic HEAD"
                try:
                    target = m.group(1).decode("ascii")
                except UnicodeDecodeError:
                    return f"{label}/HEAD names a non-ASCII branch"
                if not _refname_ok(target):
                    return f"{label}/HEAD names a ref kind git does not write"
            elif not HEX40.match(body):
                return f"{label}/HEAD is neither symbolic nor a detached 40-hex id"
        elif kind == "sha":
            body = _read(q, REF_CAP)
            if body is None or HEX40.match(body) is None:
                return f"{label}/{name} is not a 40-hex sha"
        elif kind == "message":
            if size > TEXT_CAP:
                return f"{label}/{name} exceeds {TEXT_CAP} bytes"
        elif kind == "config":
            why = _config(repo, gd, label, d)
            if why:
                return why
        elif kind == "text":
            if size > 4096:
                return f"{label}/{name} exceeds 4096 bytes"
        elif kind == "index":
            if size > INDEX_CAP:
                return f"{label}/{name} exceeds {INDEX_CAP} bytes"
        elif kind == "packed":
            why = _packed(q, f"{label}/packed-refs")
            if why:
                return why
    for req in REQUIRED:
        if req not in have:
            return f"{label} has no {req}"
    for name, fn in (("hooks", _hooks), ("info", _info), ("logs", _logs)):
        if name in have:
            why = fn(gd / name, f"{label}/{name}")
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

    No git child is started; every fact the decision rests on is read from inside `d` and classified by kind.
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
        why = _store(repo, d)
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

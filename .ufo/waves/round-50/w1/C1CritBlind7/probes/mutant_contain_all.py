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
  3. one walk of `d` proves the tree has no symlink, no special file and no multi-link file anywhere, that no
     entry crosses a device boundary (mount point), and collects every directory holding a real `.git`
     directory (a `.git` file is refused).
  4. each collected store is classified entry by entry against a plain-init allowlist: `HEAD` (a
     `refs/heads` branch line or a detached 40-hex sha), `ORIG_HEAD`, `COMMIT_EDITMSG`, `config`, `description`,
     `hooks/` (`*.sample` only), `index`, `info/` (`exclude` and the `refs` file update-server-info writes only,
     so no `alternates`), `logs/`, `objects/` (2-hex/38-hex loose objects, pack files only, and an `info/`
     holding only `packs` / `commit-graph` / `commit-graphs/`), `refs/heads|tags` (40-hex refs),
     `packed-refs` (with peeled lines). `config` is parsed line by line against a `[core]` key allowlist; any
     CR, any non-ASCII byte, any section or key not listed, or any line the parser does not fully understand is
     refused. This is what closes the CR/BOM/includeIf/attributesFile/worktree family.
  5. `--lane` must be one of the collected repositories.
  6. no git child is started at all: measured, every git subcommand resolves the fixture path component-wise
     and stats `d`'s ancestors (paths under the build scratch outside `d`), which the advertisement and the
     round-46 counter's B3/B5 legs forbid. The store classification is the proof instead.

Every path the decision names is lexically inside `d`, and no syscall the decision makes names anything else
(the measured residue is only the interpreter importing the harness and this module, before `breach` runs).
`.git/index`, `COMMIT_EDITMSG`, `description`, `logs/*` and pack files are admitted by name and size without
content validation: the tool run behind this fence reads none of them for a path (named limit).

Round 48 repair (fixture-fence honest over-refusal, `w2/R46W2C1HoHonest.md`): the round-46 allowlist refused
ordinary `git init` repository states. This variant keeps the allowlist and extends it to the shapes git itself
writes for the nine novel honest classes, and to nothing else:

  - detached HEAD: `HEAD` may be a symbolic `refs/heads` line OR one 40-hex sha (git's own detached write);
  - packed refs / `gc`: `.git/info/refs` (update-server-info: `sha\tref`, optional `^{}` peel), and under
    `.git/objects/info/`: `packs` (`P <pack>.pack` lines), `commit-graph` (magic `CGPH`) and
    `commit-graphs/` (`graph-<hex>.graph` with magic, `commit-graph-chain` of 40-hex lines). `alternates`,
    `http-alternates`, `objects/info/*` redirects and `.git/info/*` names not listed here stay refused.
  - annotated tags, merge commits, `.gitignore`, long linear histories and ignored untracked files are worktree
    and object shapes the walk already classifies; they were only ever refused through the two rules above.
  - the round-48 honest population's further ordinary states: `.git/config` may carry `[user] name|email`,
    `[init] defaultBranch` (printable text) and the inert declaration sections `[remote "<name>"]`
    (`url`/`fetch`/`tagopt`) and `[branch "<name>"]` (`remote`/`merge`), plus `core.autocrlf`/`core.safecrlf`;
    `refs/notes/...`, `refs/stash`, and their reflogs are ordinary ref namespaces. No section or key that
    redirects a read is added: `[include]`, `[includeIf]`, `[url "<base>"]` (`insteadOf`), `core.attributesFile`,
    `core.excludesFile`, `core.hooksPath`, `core.fsmonitor`, `core.worktree`, `extensions.worktreeConfig`,
    `.git/commondir`, `.git/config.worktree`, `objects/info/alternates|http-alternates` stay refused, and so do
    `.git` gitdir files and `refs/remotes` (a clone is not a plain-init state).

Mount-point boundary (`w2/R46W2C1Intent.md`): every directory and file the decision visits, and every store
entry it classifies, must live on the same device as `d`; a store whose tree crosses a device boundary is
refused (`mount boundary`), because the fence cannot prove those bytes are the fixture's. Named limit: a bind
mount of the SAME filesystem below `d` is lexically indistinguishable from a plain directory without reading
outside `d` (e.g. `/proc/self/mountinfo`), which the advertisement forbids; for such a fixture the fence's
guarantee is the one it advertises — every path it names, stats or opens is inside `d`, and the store it
classifies has the plain-init shape.
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
_ROOT = None  # fixture root, set once per decision
GITFILE = re.compile(rb"\Agitdir:[ \t]*([^\r\n\x00]+?)[ \t]*\n?\Z")
HEAD_REF = re.compile(rb"\Aref: refs/heads/[A-Za-z0-9_][A-Za-z0-9._/-]*\n\Z")
HEAD_HEX = re.compile(rb"\A[0-9a-f]{40}\n\Z")
INFO_REFS = re.compile(rb"\A[0-9a-f]{40}\t([A-Za-z0-9_][A-Za-z0-9._/-]*)(\^\{\})?\n\Z")
PACKS_ROW = re.compile(rb"\AP ([A-Za-z0-9_][A-Za-z0-9._-]*\.pack)\n\Z")
GRAPH_NAME = re.compile(r"\Agraph-[0-9a-f]{8,64}\.graph\Z", re.ASCII)
CHAIN_ROW = re.compile(rb"\A[0-9a-f]{40}(?: [0-9]+)?\n\Z")
CG_MAGIC = b"CGPH"
SECTION_LINE = re.compile(rb"\A\[([A-Za-z][A-Za-z0-9.-]*)\]\Z")
SECTION_SUB = re.compile(rb'\A\[([A-Za-z][A-Za-z0-9.-]*) "([A-Za-z0-9_@:+-][A-Za-z0-9._/@:+-]{0,239})"\]\Z')
KEY_NAME = re.compile(rb"\A([A-Za-z][A-Za-z0-9-]*)\Z")
VALUE_TEXT = re.compile(rb"\A[\x20-\x5b\x5d-\x7e]{0,1024}\Z")
OBJ_DIR = re.compile(r"\A[0-9a-f]{2}\Z", re.ASCII)
OBJ_FILE = re.compile(r"\A[0-9a-f]{38}\Z", re.ASCII)
PACK_FILE = re.compile(r"\A[A-Za-z0-9_][A-Za-z0-9._-]*\.(?:pack|idx|rev|keep|bitmap|mtimes)\Z", re.ASCII)
SAFE_NAME = re.compile(r"\A[A-Za-z0-9_][A-Za-z0-9._-]*\Z", re.ASCII)
REF_PATH = re.compile(r"\A[A-Za-z0-9_][A-Za-z0-9._/-]*\Z", re.ASCII)

GIT_TOP = {"HEAD", "ORIG_HEAD", "COMMIT_EDITMSG", "config", "description", "hooks", "index", "info",
           "logs", "objects", "refs", "packed-refs", "FETCH_HEAD", "commondir", "gitdir", "worktrees",
           "shallow"}
GIT_DIRS = {"hooks", "info", "logs", "objects", "refs"}
REF_NAMESPACES = ("heads", "tags", "notes", "replace", "remotes")  # `replace` names an object (S176)
CFG_SECTIONS = {"core", "user", "init", "extensions"}
CFG_SUB_SECTIONS = {"remote", "branch"}         # inert declarations: URLs and refspecs, no reads
CFG_KEYS = {
    ("core", "repositoryformatversion"): "version",
    ("core", "filemode"): "bool",
    ("core", "bare"): "false",
    ("core", "logallrefupdates"): "bool",
    ("core", "ignorecase"): "bool",
    ("core", "precomposeunicode"): "bool",
    ("core", "symlinks"): "bool",
    ("core", "autocrlf"): "autocrlf",
    ("core", "safecrlf"): "safecrlf",
    ("extensions", "relativeworktrees"): "bool",
}
CFG_TEXT = {("user", "name"), ("user", "email"), ("init", "defaultbranch")}
CFG_SUB_KEYS = {("remote", "url"), ("remote", "fetch"), ("remote", "tagopt"),
                ("branch", "remote"), ("branch", "merge")}
BOOL = {"true", "yes", "on", "1", "false", "no", "off", "0"}
FALSEY = {"false", "no", "off", "0"}
AUTOCRLF = {"true", "false", "input"}
SAFECRLF = {"true", "false", "warn"}


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
    """[(name, mode, size, nlink, dev)] of one directory, lstat-style. None when it cannot be read."""
    out = []
    try:
        with os.scandir(str(p)) as it:
            for e in it:
                st = e.stat(follow_symlinks=False)
                out.append((e.name, st.st_mode, st.st_size, st.st_nlink, st.st_dev))
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


def _tree(d, ddev):
    """Return (repos, reason): every directory holding a real `.git` dir, after refusing symlinks, special
    files, multi-link files and device boundaries anywhere in the fixture."""
    repos, stores, seen = [], [], 0
    for top, dirs, files in os.walk(str(d), followlinks=False):
        seen += len(dirs) + len(files)
        if seen > ENTRY_CAP:
            return None, f"fixture tree exceeds {ENTRY_CAP} entries"
        t = pathlib.Path(top)
        keep = []
        for name in dirs:
            p = t / name
            try:
                st = os.lstat(p)
            except OSError:
                return None, f"{_rel(p, d)} cannot be lstat'ed"
            if stat.S_ISLNK(st.st_mode):
                if not _inside(os.path.realpath(str(p)), d):
                    return None, f"{_rel(p, d)} is a symlink"
                continue
            if not stat.S_ISDIR(st.st_mode):
                return None, f"{_rel(p, d)} is not a directory"
            if st.st_dev != ddev:
                return None, f"{_rel(p, d)} crosses a mount boundary (device {st.st_dev} != {ddev})"
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
                if not _inside(os.path.realpath(str(p)), d):
                    return None, f"{_rel(p, d)} is a symlink"
                continue
            if name == ".git":
                body = _read(p, 4096)
                if body is None:
                    return None, f"{_rel(p, d)} is a .git file that cannot be read"
                m = GITFILE.match(body)
                if m is None:
                    return None, f"{_rel(p, d)} is a .git file that is not a gitdir line"
                target = pathlib.Path(_norm(os.path.join(str(t), os.fsdecode(m.group(1)))))
                if not _inside(target, d):
                    return None, f"{_rel(target, d)} resolves outside the fixture"
                stores.append((t, target))
                continue
            if not stat.S_ISREG(st.st_mode):
                return None, f"{_rel(p, d)} is a special file"
            if st.st_nlink > 1:
                return None, f"{_rel(p, d)} has more than one hard link"
            if st.st_dev != ddev:
                return None, f"{_rel(p, d)} crosses a mount boundary (device {st.st_dev} != {ddev})"
    if len(repos) + len(stores) > REPO_CAP:
        return None, f"fixture holds more than {REPO_CAP} repos"
    return (repos, stores), None


# ---------- fact 4: the store, classified against the plain-init allowlist ----------


def _sub_name_ok(name):
    """A remote or branch subsection name git itself would write: no empty, dot or dot-dot component."""
    if name.startswith("-") or name.endswith(".lock"):
        return False
    return all(part and part not in (".", "..") for part in name.split("/"))


def _config_value(label, sect, sub, key, val, has):
    """Classify one config value against the key's kind. `has` is whether the line carried `=`."""
    where = f"{sect}.{sub}.{key}" if sub is not None else f"{sect}.{key}"
    if sub is not None:
        if (sect, key) not in CFG_SUB_KEYS:
            return f"{label}/config key [{sect} \"{sub}\"] {key} is not allowlisted"
        if not has or not val:
            return f"{label}/config key {where} needs a value"
        if VALUE_TEXT.match(val) is None:
            return f"{label}/config {where} carries a value the parser cannot classify"
        return None
    need = CFG_KEYS.get((sect, key))
    if need == "version" and val == "1":
        return None
    if need is None:
        if (sect, key) in CFG_TEXT:
            if not has:
                return f"{label}/config key {where} needs a value"
            if VALUE_TEXT.match(val) is None:
                return f"{label}/config {where} carries a value the parser cannot classify"
            return None
        return f"{label}/config key {where} is not allowlisted"
    if not has:
        if need != "bool":
            return f"{label}/config key {where} needs a value"
        return None
    low = val.decode("ascii").lower()
    if need == "bool":
        if low not in BOOL:
            return f"{label}/config {where}={low!r} is not a boolean"
    elif need == "false":
        if low not in FALSEY:
            return f"{label}/config {where} must be false"
    elif need == "0":
        if low not in ("0", ""):
            return f"{label}/config {where} must be 0"
    elif need == "autocrlf":
        if low not in AUTOCRLF:
            return f"{label}/config {where}={low!r} is not true|false|input"
    elif need == "safecrlf":
        if low not in SAFECRLF:
            return f"{label}/config {where}={low!r} is not true|false|warn"
    return None


def _config(p, label):
    """Parse `.git/config` strictly. Anything the parser does not fully classify is refused.

    Sections: `[core]`, `[user]`, `[init]` and the inert declaration sections `[remote "<name>"]` /
    `[branch "<name>"]`. A redirect section or key (`[include]`, `[includeIf]`, `[url "<base>"]`,
    `core.attributesFile`, `core.excludesFile`, `core.hooksPath`, `core.worktree`, `core.fsmonitor`) is not in
    the tables above and is refused; a value is printable ASCII with no backslash, quote, CR, NUL or non-ASCII.
    """
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
    sect, sub = "", None
    for line in raw.split(b"\n"):
        s = line.strip(b" \t")
        if not s:
            continue
        if s[:1] in (b"#", b";"):
            continue
        if s.startswith(b"["):
            m = SECTION_LINE.match(s)
            if m is not None:
                sect = m.group(1).decode("ascii").lower()
                sub = None
                if sect not in CFG_SECTIONS:
                    return f"{label}/config section [{sect}] is not allowlisted"
                continue
            m = SECTION_SUB.match(s)
            if m is not None:
                sect = m.group(1).decode("ascii").lower()
                sub = m.group(2).decode("ascii")
                if sect not in CFG_SUB_SECTIONS:
                    return f"{label}/config section [{sect} \"{sub}\"] is not allowlisted"
                if not _sub_name_ok(sub):
                    return f"{label}/config section [{sect} \"{sub}\"] has a name git does not write"
                continue
            return f"{label}/config section header {s[:40]!r} is not plain"
        key_raw, eq, val_raw = s.partition(b"=")
        key_raw = key_raw.strip(b" \t")
        m = KEY_NAME.match(key_raw)
        if m is None:
            return f"{label}/config line {s[:40]!r} is not a plain key=value"
        why = _config_value(label, sect, sub, m.group(1).decode("ascii").lower(),
                            val_raw.strip(b" \t") if eq else b"", bool(eq))
        if why:
            return why
    return None


def _refs(p, label, ddev):
    ents = _entries(p)
    if ents is None:
        return f"{label} unreadable"
    for name, mode, _s, n, dev in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{_rel(q, label)} is a symlink"
        if dev != ddev:
            return f"{_rel(q, label)} crosses a mount boundary"
        if _linked(mode, n):
            return f"{_rel(q, label)} has more than one hard link"
        if name == "stash":                       # `git stash push` writes the ref as a plain file
            if not stat.S_ISREG(mode):
                return f"{label}/stash is not a regular file"
            body = _read(q, 200)
            if body is None or HEX40.match(body) is None:
                return f"{label}/stash is not a 40-hex ref"
            continue
        if name not in REF_NAMESPACES:
            return f"{label}/{name} is not a ref namespace git writes"
        if not stat.S_ISDIR(mode):
            return f"{label}/{name} is not a directory"
        why = _ref_tree(q, label, ddev)
        if why:
            return why
    return None


def _ref_tree(p, label, ddev):
    ents = _entries(p)
    if ents is None:
        return f"{_rel(p, label)} unreadable"
    for name, mode, _s, _n, dev in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{_rel(q, label)} is a symlink"
        if dev != ddev:
            return f"{_rel(q, label)} crosses a mount boundary"
        if _linked(mode, _n):
            return f"{_rel(q, label)} has more than one hard link"
        if stat.S_ISDIR(mode):
            if not _ref_name_ok(name):
                return f"{_rel(q, label)} has a name git does not write"
            why = _ref_tree(q, label, ddev)
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


def _objects(p, label, ddev):
    ents = _entries(p)
    if ents is None:
        return f"{label} unreadable"
    for name, mode, _s, _n, dev in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{_rel(q, label)} is a symlink"
        if dev != ddev:
            return f"{_rel(q, label)} crosses a mount boundary"
        if not stat.S_ISDIR(mode):
            return f"{label}/{name} is not a directory"
        if name == "info":
            why = _obj_info(q, f"{label}/info", ddev)
            if why:
                return why
            continue
        if name == "pack":
            inner = _entries(q)
            if inner is None:
                return f"{label}/pack unreadable"
            for pname, pmode, _ps, _pn, pdev in inner:
                if stat.S_ISLNK(pmode):
                    return f"{label}/pack/{pname} is a symlink"
                if pdev != ddev:
                    return f"{label}/pack/{pname} crosses a mount boundary"
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
        for oname, omode, _os_, _on, odev in inner:
            qq = q / oname
            if stat.S_ISLNK(omode):
                return f"{_rel(qq, label)} is a symlink"
            if odev != ddev:
                return f"{_rel(qq, label)} crosses a mount boundary"
            if not stat.S_ISREG(omode) or not OBJ_FILE.match(oname):
                return f"{_rel(qq, label)} is not a loose object"
            if _linked(omode, _on):
                return f"{_rel(qq, label)} has more than one hard link"
    return None


def _graph_dir(p, label, ddev):
    """`.git/objects/info/commit-graphs/`: git's own split-commit-graph names, each a graph file."""
    ents = _entries(p)
    if ents is None:
        return f"{label} unreadable"
    for name, mode, size, n, dev in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{_rel(q, label)} is a symlink"
        if dev != ddev:
            return f"{_rel(q, label)} crosses a mount boundary"
        if not stat.S_ISREG(mode):
            return f"{_rel(q, label)} is not a plain file"
        if _linked(mode, n):
            return f"{_rel(q, label)} has more than one hard link"
        if name == "commit-graph-chain":
            if size > TEXT_CAP:
                return f"{_rel(q, label)} exceeds {TEXT_CAP} bytes"
            raw = _read(q, TEXT_CAP)
            if raw is None:
                return f"{_rel(q, label)} unreadable"
            for line in raw.split(b"\n"):
                if line and CHAIN_ROW.match(line + b"\n") is None:
                    return f"{_rel(q, label)} carries a row git does not write"
            continue
        if GRAPH_NAME.match(name) is None:
            return f"{_rel(q, label)} is not a graph file name"
        head = _read(q, 8)
        if head is None or len(head) < 8 or not head.startswith(CG_MAGIC):
            return f"{_rel(q, label)} is not a commit-graph file"
    return None



ALTERNATES_DEPTH = 4


def _alternates(path, objects, depth, seen):
    """Every alternates entry must resolve inside the fixture, and the borrow graph is walked (visited set, cap).

    Per-repository containment is not enough (round-50 blind seat b3): an in-`d` entry may name a plain directory
    whose own `info/alternates` leaves `d`. Entries are resolved against the OBJECTS directory, never against
    `objects/info`.
    """
    if depth > ALTERNATES_DEPTH:
        return f"{_rel(path, _ROOT)} alternates chain deeper than {ALTERNATES_DEPTH}"
    key = _norm(path)
    if key in seen:
        return None
    seen.add(key)
    try:
        size = os.lstat(path).st_size
    except OSError:
        return f"{_rel(path, _ROOT)} unreadable"
    if size > TEXT_CAP:
        return f"{_rel(path, _ROOT)} exceeds {TEXT_CAP} bytes"
    raw = _read(path, TEXT_CAP)
    if raw is None:
        return f"{_rel(path, _ROOT)} unreadable"
    for line in raw.split(b"\n"):
        if not line.strip():
            continue
        target = pathlib.Path(_norm(os.path.join(str(objects), os.fsdecode(line))))
        if not _inside(target, _ROOT):
            return f"{_rel(path, _ROOT)} names a store outside the fixture"
        try:
            tst = os.lstat(target)
        except OSError:
            return f"{_rel(target, _ROOT)} does not exist"
        if stat.S_ISLNK(tst.st_mode) or not stat.S_ISDIR(tst.st_mode):
            return f"{_rel(target, _ROOT)} is not an objects directory"
        nxt = target / "info" / "alternates"
        if nxt.exists():
            why = _alternates(nxt, target, depth + 1, seen)
            if why:
                return why
    return None


def _obj_info(p, label, ddev):
    """`.git/objects/info/`: only git's own `packs`, `commit-graph` and `commit-graphs/` shapes.

    Anything that can redirect the object store (`alternates`, `http-alternates`, ...) stays refused.
    """
    ents = _entries(p)
    if ents is None:
        return f"{label} unreadable"
    for name, mode, size, n, dev in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{_rel(q, label)} is a symlink"
        if dev != ddev:
            return f"{_rel(q, label)} crosses a mount boundary"
        if not stat.S_ISREG(mode) and not (name == "commit-graphs" and stat.S_ISDIR(mode)):
            return f"{_rel(q, label)} is not a plain file"
        if _linked(mode, n):
            return f"{_rel(q, label)} has more than one hard link"
        if name == "packs":
            if size > TEXT_CAP:
                return f"{_rel(q, label)} exceeds {TEXT_CAP} bytes"
            raw = _read(q, TEXT_CAP)
            if raw is None:
                return f"{_rel(q, label)} unreadable"
            for line in raw.split(b"\n"):
                if line and PACKS_ROW.match(line + b"\n") is None:
                    return f"{_rel(q, label)} carries a row git does not write"
            continue
        if name == "alternates":
            why = _alternates(q, p.parent, 0, set())
            if why:
                return why
            continue
        if name == "commit-graph":
            if size > CONFIG_CAP:
                return f"{_rel(q, label)} exceeds {CONFIG_CAP} bytes"
            head = _read(q, 8)
            if head is None or len(head) < 8 or not head.startswith(CG_MAGIC):
                return f"{_rel(q, label)} is not a commit-graph file"
            continue
        if name == "commit-graphs":
            why = _graph_dir(q, f"{label}/commit-graphs", ddev)
            if why:
                return why
            continue
        return f"{_rel(q, label)} is not a plain object-info entry (object-store redirect)"
    return None


def _log_name_ok(rel):
    """A reflog lives at `HEAD`, at `refs/stash`, or under git's ref namespaces with git's own name shape."""
    if rel in ("HEAD", "refs/stash"):
        return True
    m = re.fullmatch(r"refs/(?:heads|tags|notes|replace|remotes)/(.+)", rel, re.ASCII)
    if not m:
        return False
    return all(SAFE_NAME.match(part) for part in m.group(1).split("/"))


def _logs(p, label, ddev, prefix=""):
    ents = _entries(p)
    if ents is None:
        return f"{label} unreadable"
    for name, mode, size, n, dev in ents:
        q = p / name
        rel = prefix + name
        if stat.S_ISLNK(mode):
            return f"{_rel(q, label)} is a symlink"
        if dev != ddev:
            return f"{_rel(q, label)} crosses a mount boundary"
        if _linked(mode, n):
            return f"{_rel(q, label)} has more than one hard link"
        if stat.S_ISDIR(mode):
            if not (rel in ("refs", "refs/heads", "refs/tags", "refs/notes", "refs/replace", "refs/remotes")
                    or (_log_name_ok(rel) and rel != "refs/stash")):
                return f"{_rel(q, label)} has a name git does not write"
            why = _logs(q, label, ddev, rel + "/")
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


def _hooks(p, label, ddev):
    ents = _entries(p)
    if ents is None:
        return f"{label} unreadable"
    for name, mode, _s, _n, dev in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{_rel(q, label)} is a symlink"
        if dev != ddev:
            return f"{_rel(q, label)} crosses a mount boundary"
        if not stat.S_ISREG(mode) or not name.endswith(".sample"):
            return f"{_rel(q, label)} is not a hook sample"
        if _linked(mode, _n):
            return f"{_rel(q, label)} has more than one hard link"
    return None


def _info(p, label, ddev):
    """`.git/info/`: git's `exclude`, and the `refs` file `git gc`'s update-server-info writes.

    `info/attributes` and every other name stay refused: the allowlist is the point.
    """
    ents = _entries(p)
    if ents is None:
        return f"{label} unreadable"
    for name, mode, size, n, dev in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{_rel(q, label)} is a symlink"
        if dev != ddev:
            return f"{_rel(q, label)} crosses a mount boundary"
        if not stat.S_ISREG(mode):
            return f"{_rel(q, label)} is not a plain file"
        if _linked(mode, n):
            return f"{_rel(q, label)} has more than one hard link"
        if name == "exclude":
            continue
        if name == "refs":
            if size > TEXT_CAP:
                return f"{_rel(q, label)} exceeds {TEXT_CAP} bytes"
            raw = _read(q, TEXT_CAP)
            if raw is None:
                return f"{_rel(q, label)} unreadable"
            for line in raw.split(b"\n"):
                if line and INFO_REFS.match(line + b"\n") is None:
                    return f"{_rel(q, label)} carries a line git does not serve"
            continue
        return f"{_rel(q, label)} is not a plain `.git/info` entry"
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


def _store(gd, label, ddev):
    """Classify one `.git` directory, entry by entry, against what `git init` + commits writes."""
    ents = _entries(gd)
    if ents is None:
        return f"{label} unreadable"
    have = set()
    for name, mode, size, n, dev in ents:
        q = gd / name
        if stat.S_ISLNK(mode):
            return f"{label}/{name} is a symlink"
        if dev != ddev:
            return f"{label}/{name} crosses a mount boundary"
        if name not in GIT_TOP:
            return f"{label}/{name} is not a plain-init entry"
        have.add(name)
        if name in GIT_DIRS or name == "worktrees":
            if not stat.S_ISDIR(mode):
                return f"{label}/{name} is not a directory"
            if name == "worktrees":
                inner = _entries(q)
                if inner is None:
                    return f"{label}/worktrees unreadable"
                for wname, wmode, _ws, _wn, wdev in inner:
                    if stat.S_ISLNK(wmode) or wdev != ddev or not stat.S_ISDIR(wmode):
                        return f"{label}/worktrees/{wname} is not a plain directory"
                    why = _wt_store(q / wname, f"{label}/worktrees/{wname}", ddev)
                    if why:
                        return why
            continue
        if not stat.S_ISREG(mode):
            return f"{label}/{name} is not a regular file"
        if _linked(mode, n):
            return f"{label}/{name} has more than one hard link"
        if name == "HEAD":
            body = _read(q, 200)
            if body is None or (HEAD_REF.match(body) is None and HEAD_HEX.match(body) is None):
                return f"{label}/HEAD is not a branch line or a detached sha"
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
        elif name == "shallow":
            if size > TEXT_CAP:
                return f"{label}/shallow exceeds {TEXT_CAP} bytes"
        elif name == "FETCH_HEAD":
            if size > TEXT_CAP:
                return f"{label}/FETCH_HEAD exceeds {TEXT_CAP} bytes"
        elif name in ("commondir", "gitdir"):
            if size > TEXT_CAP:
                return f"{label}/{name} exceeds {TEXT_CAP} bytes"
            body = _read(q, TEXT_CAP)
            if body is None or not body.strip() or b"\x00" in body or b"\r" in body:
                return f"{label}/{name} is not a plain pointer line"
            if name == "gitdir":
                back = pathlib.Path(_norm(os.path.join(str(gd), os.fsdecode(body.strip()))))
                if _ROOT is None or not _inside(back, _ROOT):
                    return f"{label}/gitdir points outside the fixture"
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
        why = _hooks(gd / "hooks", f"{label}/hooks", ddev)
        if why:
            return why
    if "info" in have:
        why = _info(gd / "info", f"{label}/info", ddev)
        if why:
            return why
    if "logs" in have:
        why = _logs(gd / "logs", f"{label}/logs", ddev)
        if why:
            return why
    why = _objects(gd / "objects", f"{label}/objects", ddev)
    if why:
        return why
    why = _refs(gd / "refs", f"{label}/refs", ddev)
    if why:
        return why
    return None


WT_TOP = {"HEAD", "ORIG_HEAD", "index", "commondir", "gitdir", "logs", "refs"}


def _wt_store(gd, label, ddev):
    """A worktree store: HEAD, commondir, gitdir, index, logs; refs and objects come from the common dir."""
    ents = _entries(gd)
    if ents is None:
        return f"{label} unreadable"
    have = set()
    for name, mode, size, n, dev in ents:
        q = gd / name
        if stat.S_ISLNK(mode):
            return f"{label}/{name} is a symlink"
        if dev != ddev:
            return f"{label}/{name} crosses a mount boundary"
        if name not in WT_TOP:
            return f"{label}/{name} is not a worktree-store entry"
        have.add(name)
        if name in ("logs", "refs"):
            if not stat.S_ISDIR(mode):
                return f"{label}/{name} is not a directory"
            if name == "refs":
                why = _refs(q, f"{label}/refs", ddev)
                if why:
                    return why
            continue
        if not stat.S_ISREG(mode):
            return f"{label}/{name} is not a regular file"
        if _linked(mode, n):
            return f"{label}/{name} has more than one hard link"
        if name == "HEAD":
            body = _read(q, 200)
            if body is None or (HEAD_REF.match(body) is None and HEAD_HEX.match(body) is None):
                return f"{label}/HEAD is not a branch line or a detached sha"
        elif name == "ORIG_HEAD":
            body = _read(q, 200)
            if body is None or HEX40.match(body) is None:
                return f"{label}/ORIG_HEAD is not a 40-hex sha"
        elif name == "index":
            if size > INDEX_CAP:
                return f"{label}/index exceeds {INDEX_CAP} bytes"
        elif name in ("commondir", "gitdir"):
            if size > TEXT_CAP:
                return f"{label}/{name} exceeds {TEXT_CAP} bytes"
            body = _read(q, TEXT_CAP)
            if body is None or not body.strip() or b"\x00" in body or b"\r" in body:
                return f"{label}/{name} is not a plain pointer line"
            if name == "gitdir":
                back = pathlib.Path(_norm(os.path.join(str(gd), os.fsdecode(body.strip()))))
                if _ROOT is None or not _inside(back, _ROOT):
                    return f"{label}/gitdir points outside the fixture"
    if "HEAD" not in have or "commondir" not in have:
        return f"{label} has no HEAD or commondir"
    if "logs" in have:
        why = _logs(gd / "logs", f"{label}/logs", ddev)
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
    ddev = st.st_dev
    vals, why = _argv(d, tool, argv)
    if why:
        return why
    global _ROOT
    _ROOT = d
    built, why = _tree(d, ddev)
    if why:
        return why
    repos, stores = built

    def store_of(path):
        """One gitdir; a store whose `commondir` names another gitdir is classified with its common dir."""
        why = _wt_store(path, f"{_rel(path, d)}", ddev) if (path / "commondir").exists() \
            else _store(path, f"{_rel(path, d)}", ddev)
        if why:
            return why
        cd = path / "commondir"
        if cd.exists():
            body = _read(cd, TEXT_CAP)
            if body is None or not body.strip() or b"\x00" in body or b"\r" in body:
                return f"{_rel(cd, d)} is not a plain pointer line"
            common = pathlib.Path(_norm(os.path.join(str(path), os.fsdecode(body.strip()))))
            if not _inside(common, d):
                return f"{_rel(cd, d)} names a common dir outside the fixture"
            if _norm(common) != _norm(path):
                why = _store(common, f"{_rel(common, d)}", ddev)
                if why:
                    return why
        return None

    for repo in repos:
        why = store_of(repo / ".git")
        if why:
            return why
    for _repo, store in stores:
        why = store_of(store)
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
    if _norm(lane) not in ({_norm(r) for r in repos} | {_norm(r) for r, _s in stores}):
        return f"--lane {lane_tok!r} is not a repository inside the fixture"
    return None

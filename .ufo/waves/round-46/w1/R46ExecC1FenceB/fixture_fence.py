"""Fixture fence (round-46 C1, variant B): prove a fixture self-contained by reading its own store; never run git.

Contract (frozen, `plans/round46_c1_verify.py` docstring):

    breach(d: pathlib.Path, argv: list[str], tool: str) -> str | None

`d` is the fixture directory (absolute, resolved), `argv` the module's argv tail, `tool` `anchor` or `order`.
A non-empty string refuses (the reason, one line); None admits. The fence runs with cwd `d`, read-only, under
`strace -f -y`, and the counter counts every successful open of a path under the build scratch outside `d`.
This variant therefore spawns no child at all (no git, no subprocess, no shell): the whole decision is a walk of
`d` plus a strict parse of the store bytes it contains, so there is no process tree to open anything anywhere.

Design rule, learned from round 45 (`R45CriticPredicate` B1/B3/B4/B5/B6, `a3w1` held-out modules): a denylist of
named attack classes is unprovable, because the next class is never on it. This fence inverts the rule — it admits
only shapes it can fully parse and prove inert, and refuses everything else:

  * `d`'s tree: regular files and directories only, each file with exactly one hard link. Every symlink is
    refused unfollowed (a link is not proven inside `d`, and `objects` symlinked from the build root was a
    round-45 escape) and a multiply-linked inode is refused because its other name may sit outside `d` — so the
    fence never `stat`s, `readlink`s or opens a path outside `d`, and an inode shared with the outside is refused
    rather than read.
  * argv: the tool's exact option shape (no abbreviation, no `--opt=value`), every value a plain token that
    normalises inside `d` lexically (no filesystem access is needed to prove that), no NUL, no control character,
    no brace placeholder, no option-looking value.
  * `--lane`: must be a store root the fence itself validated. Git discovery stops at the first `.git` walking up,
    so a validated store root can never discover a repo above `d` — which is why this fence never has to look
    above `d` (f6 stays refused without an outside `stat`).
  * each `.git`: entries drawn from a closed inert set; `commondir`, `worktrees`, `modules`, `config.*`,
    `objects/info/alternates`, `refs/replace`, grafts and every other redirect shape are simply not in the set and
    are refused before anything inside them is read.
  * `.git/config`: strict grammar (no BOM, no CR, no NUL, no dotted section, no escape sequence, no inline
    comment) plus a closed key table of keys that cannot name a path or a program. An `[include]`/`[includeIf]`
    section, hidden behind a CR, a BOM, mixed case or a harmless-looking name, fails the key table without the
    fence ever reading the include target.
  * `HEAD`, `packed-refs` and loose refs: parsed here; every object id must exist in this store, as a loose object
    whose zlib header parses, or in a pack index the fence parses itself (v2).
  * `.git/index`: `DIRC` header, v2 only, every entry path proven repo-relative with no `..`, trailing tarball
    checksum, then extension blocks that exactly consume the file.
  * `order`'s `--claims`/`--receipt`: resolved through HEAD's commit and tree objects read from this store; a path
    that is a tree or a gitlink at HEAD is refused, an absent path is admitted (a receipt may not exist yet).

Every refusal is one line naming the shape that could not be proved inert. Known limits are named in the round-46
report: a pack payload is opaque bytes whose index is parsed but whose objects are not decoded (so a `--claims`
path that lives only inside a pack is refused, not resolved), and a repo above `d` is not detected — it is made
irrelevant by the lane rule instead.
"""
import hashlib
import os
import pathlib
import posixpath
import re
import stat
import zlib

ENTRY_CAP = 200000          # walked entries in d before the tree itself is refused as pathological
DEPTH_CAP = 64              # directory depth in d
REPO_CAP = 64               # collected stores before the fixture is refused as pathological
OBJ_CAP = 20000             # loose object files per store
TEXT_CAP = 1 << 20          # any text store file larger than this is refused unread
OBJ_FILE_CAP = 16 << 20     # a loose object file larger than this is refused unread
OBJ_PAYLOAD_CAP = 16 << 20  # inflated object larger than this is refused
IDX_CAP = 64 << 20          # a pack index larger than this is refused unread
REF_HOPS = 8                # symbolic refs followed in one chain
FILES_CAP = 20000           # store files read for one decision, so a pathological fixture is refused not hung
BYTES_CAP = 64 << 20        # bytes read for one decision, same reason

ORDER_SHAPE = ("--lane", "--claims", "--receipt")
ANCHOR_OPTS = {"--lane": True, "--evidence-ref": True, "--verbose": False}

# Closed table of config keys the fence can prove inert: they neither name a path the store would read nor a
# program it would run. A value tuple lists the only accepted values; None accepts any short plain string.
_INERT_KEYS = {
    ("core", "repositoryformatversion"): ("0",),
    ("core", "filemode"): ("true", "false"),
    ("core", "bare"): ("false",),
    ("core", "logallrefupdates"): ("true", "false"),
    ("core", "symlinks"): ("true", "false"),
    ("core", "ignorecase"): ("true", "false"),
    ("core", "precomposeunicode"): ("true", "false"),
    ("core", "quotepath"): ("true", "false"),
    ("user", "name"): None,
    ("user", "email"): None,
}
# Keys that are inert only inside a `[branch "<name>"]` subsection: a remote name and a ref name.
_BRANCH_KEYS = ("remote", "merge")

_STORE_DIRS = frozenset({"objects", "refs", "logs", "hooks", "info", "branches"})
_STORE_FILES = frozenset({"HEAD", "config", "description", "index", "packed-refs", "COMMIT_EDITMSG",
                          "ORIG_HEAD", "FETCH_HEAD", "MERGE_HEAD", "MERGE_MSG", "MERGE_MODE", "AUTO_MERGE"})
_OBJECT_INFO = frozenset({"packs", "commit-graph"})
_PACK_SUFFIX = frozenset({".pack", ".idx", ".rev", ".keep", ".bitmap", ".mtimes"})
_HOOK_SUFFIX = ".sample"

_HEX = re.compile(r"\A[0-9a-f]{40}(?:[0-9a-f]{24})?\Z")
_LOOSE_DIR = re.compile(r"\A[0-9a-f]{2}\Z")
_LOOSE_FILE = re.compile(r"\A[0-9a-f]{38}\Z")
_OBJECT_KINDS = ("commit", "tree", "blob", "tag")
_OBJ_HEADER = re.compile(rb"\A(blob|tree|commit|tag) ([0-9]{1,20})\Z")
_SECTION = re.compile(r"\A\[([A-Za-z][A-Za-z0-9-]*)(?:[ \t]+\"([^\"\\\x00-\x1f]{0,240})\")?\]\Z")
_CFG_KEY = re.compile(r"\A([A-Za-z][A-Za-z0-9-]*)[ \t]*(?:=[ \t]*(.*))?\Z")
_BAD_REF = re.compile(r"[\x00-\x20\x7f~^:?*\[\\]|\.\.|@\{")
_CTRL_RUN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


# One decision per process is the contract (`breach` is called once by the counter harness), so the read budget
# lives in one place and is reset at entry. Without it a fixture with 64 stores of 20000 loose objects would be
# refused only after minutes of inflating, which reads to the counter as a HUNG fence rather than a refusal.
_SPENT = {"files": 0, "bytes": 0}


def _spend(nbytes):
    """(reason, None): charge one file read to the decision's budget."""
    _SPENT["files"] += 1
    _SPENT["bytes"] += nbytes
    if _SPENT["files"] > FILES_CAP:
        return f"the fixture needs more than {FILES_CAP} file reads to judge"
    if _SPENT["bytes"] > BYTES_CAP:
        return f"the fixture needs more than {BYTES_CAP} bytes to judge"
    return None


def _rel(p, d):
    """Render a path for a reason string, relative to d when it lies inside it."""
    try:
        p = str(p)
        ds = str(d)
        return p[len(ds) + 1:] if p.startswith(ds + "/") else p
    except Exception:  # noqa: BLE001 - a reason string must never raise
        return "?"


def _show(path, name, d):
    return _rel(os.path.join(str(path), name), d)


def _lexical(d, value):
    """Join one argv value onto d and normalise it LEXICALLY (no stat, no readlink, no resolve).

    Returns the normalised absolute string when it stays inside d, else None. This is the whole containment
    proof for argv: a value that normalises inside d cannot name a path outside it, and a value that does not is
    refused without touching the filesystem.
    """
    ds = str(d)
    if value.startswith("/"):
        cand = posixpath.normpath(value)
    else:
        cand = posixpath.normpath(posixpath.join(ds, value))
    if cand == ds:
        return cand
    if ds == "/":
        return cand
    return cand if cand.startswith(ds + "/") else None


def _plain(token):
    """A token the fence is willing to treat as a value: no NUL, no control character, no brace placeholder,
    and not option-shaped (so a value can never be read as a second option by a later leg)."""
    if not isinstance(token, str) or not token or token[0] == "-":
        return False
    if "{" in token or "}" in token or _CTRL_RUN.search(token) or "\x00" in token:
        return False
    return True


def _listdir(path, d):
    """(entries, reason) with entries [(name, kind, path)], kind 'd'|'f'. Refuses every symlink and special file
    in place, so nothing in this module ever follows a link out of d."""
    try:
        with os.scandir(str(path)) as it:
            items = sorted(it, key=lambda e: e.name)
    except OSError:
        return None, f"{_rel(path, d)} cannot be listed"
    out = []
    for e in items:
        if e.is_symlink():
            return None, f"{_show(path, e.name, d)} is a symlink; the fence cannot prove it stays inside"
        try:
            mode = e.stat(follow_symlinks=False).st_mode
        except OSError:
            return None, f"{_show(path, e.name, d)} cannot be stat'ed"
        why = _spend(0)
        if why:
            return None, why
        if stat.S_ISDIR(mode):
            out.append((e.name, "d", e.path))
        elif stat.S_ISREG(mode):
            if e.stat(follow_symlinks=False).st_nlink != 1:
                return None, (f"{_show(path, e.name, d)} has {e.stat(follow_symlinks=False).st_nlink} hard links; "
                              "the fence cannot prove the inode has none outside")
            out.append((e.name, "f", e.path))
        else:
            return None, f"{_show(path, e.name, d)} is not a regular file or directory"
    return out, None


def _read(path, cap, d):
    """(bytes, reason): a regular non-symlink file of at most `cap` bytes, read whole."""
    try:
        st = os.lstat(str(path))
    except OSError:
        return None, f"{_rel(path, d)} cannot be stat'ed"
    if not stat.S_ISREG(st.st_mode):
        return None, f"{_rel(path, d)} is not a regular file"
    if st.st_size > cap:
        return None, f"{_rel(path, d)} exceeds {cap} bytes"
    try:
        with open(str(path), "rb") as fh:
            raw = fh.read(cap + 1)
    except OSError:
        return None, f"{_rel(path, d)} is unreadable"
    if len(raw) > cap:
        return None, f"{_rel(path, d)} exceeds {cap} bytes"
    why = _spend(len(raw))
    return (None, why) if why else (raw, None)


# ---------- argv ----------


def _argv(d, tool, argv):
    """(values, reason). The contract shape only: exact options, plain values, lexical containment in d."""
    if not isinstance(argv, list):
        return None, "argv is not a list"
    for tok in argv:
        if not isinstance(tok, str):
            return None, "argv carries a non-string token"
    vals = {}
    if tool == "order":
        if len(argv) != 6 or tuple(argv[0::2]) != ORDER_SHAPE:
            return None, f"order argv is not the contract shape {list(ORDER_SHAPE)}"
        pairs = list(zip(argv[0::2], argv[1::2]))
    elif tool == "anchor":
        pairs, k = [], 0
        while k < len(argv):
            tok = argv[k]
            if tok not in ANCHOR_OPTS:
                return None, f"anchor argv token {tok!r} is not an exact option"
            if ANCHOR_OPTS[tok]:
                if k + 1 >= len(argv):
                    return None, f"anchor option {tok} has no value"
                pairs.append((tok, argv[k + 1]))
                k += 2
            else:
                pairs.append((tok, True))
                k += 1
    else:
        return None, f"unknown tool {tool!r}"
    for opt, val in pairs:
        if val is True:
            continue
        if not _plain(val):
            return None, f"{opt} value {val!r} is not a plain token"
        if _lexical(d, val) is None:
            return None, f"{opt} value {val!r} resolves outside the fixture"
        vals[opt] = val
    return vals, None


# ---------- tree ----------


def _walk(d):
    """(repos, reason): every directory in d that holds a real `.git` directory. Nothing outside d is touched."""
    repos, seen = [], 0
    stack = [(d, 0)]
    while stack:
        top, depth = stack.pop()
        if depth > DEPTH_CAP:
            return None, f"fixture tree is deeper than {DEPTH_CAP} directories"
        entries, why = _listdir(top, d)
        if why:
            return None, why
        seen += len(entries)
        if seen > ENTRY_CAP:
            return None, f"fixture tree exceeds {ENTRY_CAP} entries"
        for name, kind, path in entries:
            if name == ".git":
                if kind != "d":
                    return None, f"{_show(top, name, d)} is a file (gitdir redirect), not a directory"
                repos.append(pathlib.Path(top))
                continue
            if kind == "d":
                stack.append((pathlib.Path(path), depth + 1))
    if len(repos) > REPO_CAP:
        return None, f"fixture holds more than {REPO_CAP} stores"
    return repos, None


# ---------- store primitives ----------


def _ref_component(name):
    return bool(name) and not name.startswith(".") and not name.endswith(".") \
        and not name.endswith(".lock") and not _BAD_REF.search(name) and len(name) <= 255


def _oid_len(text):
    """20 for a sha1 id, 32 for a sha256 id, else None."""
    if _HEX.match(text) is None:
        return None
    return 20 if len(text) == 40 else 32


def _loose(db, d, rel):
    """(present oids, reason): every loose object file, header and declared size parsed from its zlib stream."""
    present, count = set(), 0
    entries, why = _listdir(db, d)
    if why:
        return None, why
    for name, kind, path in entries:
        if name in ("info", "pack"):
            if kind != "d":
                return None, f"{rel}/objects/{name} is not a directory"
            continue
        if kind != "d" or _LOOSE_DIR.match(name) is None:
            return None, f"{rel}/objects/{name} is not a loose object directory"
        files, why = _listdir(path, d)
        if why:
            return None, why
        for fname, fkind, fpath in files:
            if fkind != "f" or _LOOSE_FILE.match(fname) is None:
                return None, f"{rel}/objects/{name}/{fname} is not a loose object file"
            count += 1
            if count > OBJ_CAP:
                return None, f"{rel}/objects holds more than {OBJ_CAP} loose objects"
            raw, why = _read(fpath, OBJ_FILE_CAP, d)
            if why:
                return None, why
            try:
                body = zlib.decompress(raw)
            except zlib.error:
                return None, f"{rel}/objects/{name}/{fname} is not a zlib object"
            if len(body) > OBJ_PAYLOAD_CAP:
                return None, f"{rel}/objects/{name}/{fname} inflates past {OBJ_PAYLOAD_CAP} bytes"
            header, sep, payload = body.partition(b"\x00")
            m = _OBJ_HEADER.match(header) if sep else None
            if m is None:
                return None, f"{rel}/objects/{name}/{fname} carries no `<kind> <size>` header"
            if int(m.group(2)) != len(payload):
                return None, f"{rel}/objects/{name}/{fname} declares {m.group(2).decode()} bytes, holds {len(payload)}"
            present.add(name + fname)
    return present, None


def _pack_idx(path, d):
    """(oids, reason): the object-id table of a v2 pack index, parsed here rather than trusted."""
    raw, why = _read(path, IDX_CAP, d)
    if why:
        return None, why
    if raw[:4] != b"\xfftOc":
        return None, f"{_rel(path, d)} is not a v2 pack index"
    if int.from_bytes(raw[4:8], "big") != 2:
        return None, f"{_rel(path, d)} is not a v2 pack index"
    if len(raw) < 8 + 1024:
        return None, f"{_rel(path, d)} is a truncated pack index"
    fan = [int.from_bytes(raw[8 + 4 * i:12 + 4 * i], "big") for i in range(256)]
    if fan != sorted(fan):
        return None, f"{_rel(path, d)} has a non-monotonic fanout table"
    count, off = fan[255], 8 + 1024
    if off + 20 * count > len(raw):
        return None, f"{_rel(path, d)} is a truncated pack index"
    oids, prev = set(), None
    for i in range(count):
        oid = raw[off + 20 * i:off + 20 * i + 20].hex()
        if prev is not None and oid <= prev:
            return None, f"{_rel(path, d)} has an unsorted object-id table"
        prev = oid
        oids.add(oid)
    return oids, None


def _pack(db, d, rel):
    """(present oids, reason): pack indexes parsed; every `.pack` must have its `.idx` and vice versa."""
    entries, why = _listdir(db, d)
    if why:
        return None, why
    names, idx, present = {}, [], set()
    for name, kind, path in entries:
        if kind != "f":
            return None, f"{rel}/objects/pack/{name} is not a file"
        stem, suffix = os.path.splitext(name)
        if suffix not in _PACK_SUFFIX or _oid_len(stem[5:] if stem.startswith("pack-") else stem) is None:
            return None, f"{rel}/objects/pack/{name} is not a pack member"
        names.setdefault(stem, set()).add(suffix)
        if suffix == ".idx":
            idx.append(path)
    for stem, suffixes in names.items():
        if ".idx" not in suffixes or ".pack" not in suffixes:
            return None, f"{rel}/objects/pack/{stem} lacks its pack/idx pair"
    for path in idx:
        oids, why = _pack_idx(path, d)
        if why:
            return None, why
        present |= oids
    return present, None


def _config(path, d, rel):
    """(reason, None): a `.git/config` whose every line parses under the strict grammar AND names a key this
    fence has proven inert. Anything else — include, includeIf, extensions, core.worktree, attributesFile,
    hooksPath, a CR or BOM that hides a section from a line-anchored reader, a dotted section, an escape — is
    refused before the target of such a key could be opened."""
    raw, why = _read(path, TEXT_CAP, d)
    if why:
        return why
    if raw.startswith(b"\xef\xbb\xbf"):
        return f"{rel}/config starts with a byte-order mark"
    if b"\x00" in raw:
        return f"{rel}/config carries a NUL byte"
    if b"\r" in raw:
        return f"{rel}/config carries a carriage return"
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return f"{rel}/config is not UTF-8"
    section, sub = None, None
    for lineno, line in enumerate(text.split("\n"), 1):
        stripped = line.strip()
        if not stripped or stripped[0] in "#;":
            continue
        if stripped.startswith("["):
            m = _SECTION.match(stripped)
            if m is None:
                return f"{rel}/config:{lineno} has a section header the fence cannot parse"
            section, sub = m.group(1).lower(), m.group(2)
            continue
        if section is None:
            return f"{rel}/config:{lineno} sets a key before any section"
        m = _CFG_KEY.match(stripped)
        if m is None:
            return f"{rel}/config:{lineno} is not `key = value`"
        key, value = m.group(1).lower(), (m.group(2) or "").strip()
        if value.startswith('"'):
            if len(value) < 2 or not value.endswith('"') or "\\" in value[1:-1]:
                return f"{rel}/config:{lineno} has a quoted value the fence will not decode"
            value = value[1:-1]
        elif '"' in value or "\\" in value or " #" in value or " ;" in value:
            return f"{rel}/config:{lineno} has a value the fence will not decode"
        if sub is not None and section != "branch":
            return f"{rel}/config carries a [{section} \"{sub}\"] subsection the fence does not admit"
        watched = section == "branch" and sub is not None and key in _BRANCH_KEYS
        allowed = _INERT_KEYS.get((section, key)) if sub is None else None
        if allowed is None and not watched:
            return f"{rel}/config sets [{section}]{' \"' + sub + '\"' if sub else ''} {key}, which cannot be proven inert"
        if allowed is not None and value not in allowed:
            return f"{rel}/config sets [{section}] {key} = {value!r}, outside the admitted values"
        if allowed is None and (len(value) > 200 or _CTRL_RUN.search(value)):
            return f"{rel}/config:{lineno} has an implausible value"
    return None


def _index(path, d, rel):
    """(reason, None): a `DIRC` index, version 2 only, every entry path repo-relative with no `..`, the trailer
    checksum over the file, and trailing extension blocks that exactly consume it."""
    raw, why = _read(path, IDX_CAP, d)
    if why:
        return why
    if len(raw) < 32 or raw[:4] != b"DIRC":
        return f"{rel}/index is not a DIRC file"
    version = int.from_bytes(raw[4:8], "big")
    if version != 2:
        return f"{rel}/index is version {version}, which the fence does not parse"
    if hashlib.sha1(raw[:-20]).digest() != raw[-20:]:
        return f"{rel}/index checksum does not match its bytes"
    count, off = int.from_bytes(raw[8:12], "big"), 12
    for _ in range(count):
        if off + 62 > len(raw):
            return f"{rel}/index is truncated in its entry table"
        flags = int.from_bytes(raw[off + 60:off + 62], "big")
        start = off + 62
        end = raw.find(b"\x00", start)
        if end < 0:
            return f"{rel}/index has an unterminated entry path"
        name = raw[start:end]
        if not name or b"\\" in name or name.startswith(b"/") or any(b < 0x20 or b == 0x7f for b in name):
            return f"{rel}/index has an entry path the fence will not accept"
        if any(part in (b"", b".", b"..") for part in name.split(b"/")):
            return f"{rel}/index entry {name[:40]!r} is not a plain repo-relative path"
        if (flags & 0xFFF) != 0xFFF and (flags & 0xFFF) != len(name):
            return f"{rel}/index entry name length disagrees with its flags"
        size = 62 + len(name) + 1
        off += (size + 7) // 8 * 8
    while off < len(raw) - 20:
        if off + 8 > len(raw) - 20:
            return f"{rel}/index has a truncated extension header"
        sig = raw[off:off + 4]
        if not all(0x41 <= b <= 0x5A for b in sig):
            return f"{rel}/index carries an extension signature {sig!r} the fence does not parse"
        length = int.from_bytes(raw[off + 4:off + 8], "big")
        off += 8 + length
    if off != len(raw) - 20:
        return f"{rel}/index extensions do not consume the file"
    return None


def _refs(root, d, rel, present, depth=0):
    """(reason, None): every ref under refs/ is inside heads/ or tags/, named like a ref, and named by an object
    this store holds (or by another such ref). Nothing else lives under refs/."""
    if depth > REF_HOPS:
        return f"{rel} refs nest deeper than {REF_HOPS}"
    entries, why = _listdir(root, d)
    if why:
        return why
    for name, kind, path in entries:
        if not _ref_component(name):
            return f"{_rel(path, d)} is not a valid ref name"
        if kind == "d":
            if depth == 0 and name not in ("heads", "tags"):
                return f"{rel} holds {name}/, outside the refs the fence admits"
            why = _refs(path, d, rel, present, depth + 1)
            if why:
                return why
            continue
        raw, why = _read(path, TEXT_CAP, d)
        if why:
            return why
        text = raw.decode("ascii", "replace").strip()
        if text.startswith("ref: "):
            target = text[5:].strip()
            if not target.startswith("refs/") or not all(_ref_component(c) for c in target.split("/")):
                return f"{_rel(path, d)} names an unparseable symbolic ref"
            continue
        if text not in present:
            return f"{_rel(path, d)} names {text[:12]!r}, an object this store does not hold"
    return None


def _packed_refs(path, d, rel, present):
    """(mapping, reason): `packed-refs` parsed here, every id an object of this store. The mapping lets HEAD
    resolve when its branch lives only in the packed file, so a packed branch cannot look unborn."""
    raw, why = _read(path, TEXT_CAP, d)
    if why:
        return None, why
    if b"\x00" in raw or b"\r" in raw:
        return None, f"{rel}/packed-refs carries a NUL or CR"
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError:
        return None, f"{rel}/packed-refs is not ASCII"
    refs = {}
    for lineno, line in enumerate(text.split("\n"), 1):
        if not line or line.startswith("#"):
            continue
        if line.startswith("^"):
            if line[1:].strip() not in present:
                return None, f"{rel}/packed-refs:{lineno} peels an object this store does not hold"
            continue
        oid, _, name = line.partition(" ")
        if _oid_len(oid) is None or not name.startswith("refs/") or not all(_ref_component(c) for c in name.split("/")):
            return None, f"{rel}/packed-refs:{lineno} is not `<oid> <ref>`"
        if oid not in present:
            return None, f"{rel}/packed-refs:{lineno} names an object this store does not hold"
        refs[name] = oid
    return refs, None


def _info_refs(path, d, rel, present):
    """(reason, None): `info/refs` (the dumb-protocol ref list) parses as `<oid>\t<ref>` naming objects held here."""
    raw, why = _read(path, TEXT_CAP, d)
    if why:
        return why
    if b"\x00" in raw or b"\r" in raw:
        return f"{rel}/info/refs carries a NUL or CR"
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError:
        return f"{rel}/info/refs is not ASCII"
    for lineno, line in enumerate(text.split("\n"), 1):
        if not line:
            continue
        oid, sep, name = line.partition("\t")
        if not sep or _oid_len(oid) is None or not name.startswith("refs/") \
                or not all(_ref_component(c) for c in name.split("/")):
            return f"{rel}/info/refs:{lineno} is not `<oid>\t<ref>`"
        if oid not in present:
            return f"{rel}/info/refs:{lineno} names an object this store does not hold"
    return None


def _logs(root, d, rel, depth=0):
    """(reason, None): reflogs are text: two object ids then a message. Nothing under logs/ is a path."""
    if depth > REF_HOPS:
        return f"{rel}/logs nests deeper than {REF_HOPS}"
    entries, why = _listdir(root, d)
    if why:
        return why
    for name, kind, path in entries:
        if not _ref_component(name):
            return f"{_rel(path, d)} is not a valid reflog name"
        if kind == "d":
            why = _logs(path, d, rel, depth + 1)
            if why:
                return why
            continue
        raw, why = _read(path, TEXT_CAP, d)
        if why:
            return why
        if b"\x00" in raw:
            return f"{_rel(path, d)} carries a NUL"
        for lineno, line in enumerate(raw.decode("utf-8", "replace").split("\n"), 1):
            if not line:
                continue
            old, sep1, rest = line.partition(" ")
            new, sep2, _ = rest.partition(" ")
            if not sep1 or not sep2 or _oid_len(old) is None or _oid_len(new) is None:
                return f"{_rel(path, d)}:{lineno} is not a reflog line"
    return None


def _hooks(path, d, rel):
    entries, why = _listdir(path, d)
    if why:
        return why
    for name, kind, _ in entries:
        if kind != "f" or not name.endswith(_HOOK_SUFFIX):
            return f"{rel}/hooks/{name} is not an inert sample hook"
    return None


def _info(path, d, rel, present):
    entries, why = _listdir(path, d)
    if why:
        return why
    for name, kind, full in entries:
        if kind != "f" or name not in ("exclude", "refs"):
            return f"{rel}/info/{name} is not a store file the fence can prove inert"
        if name == "refs":
            why = _info_refs(full, d, rel, present)
            if why:
                return why
        else:
            why = _textfile(full, d, rel)
            if why:
                return why
    return None


def _textfile(path, d, rel):
    raw, why = _read(path, TEXT_CAP, d)
    if why:
        return why
    return f"{rel}/{os.path.basename(str(path))} carries a NUL" if b"\x00" in raw else None


# ---------- store ----------


class _Store:
    """One validated store: the object ids it holds and the means to read a loose object body for the tree walk."""

    def __init__(self, gitdir, rel, d):
        self.gitdir, self.rel, self.d = gitdir, rel, d
        self.present = set()
        self.packed = set()
        self.packed_refs = {}
        self.head = None

    def body(self, oid):
        """(payload, kind, reason): one object decoded from a loose file in this store; a packed object is not
        decoded, so its reason says the fence cannot prove what it holds."""
        if oid in self.packed:
            return None, None, f"{self.rel} holds {oid[:12]} in a pack the fence does not decode"
        path = os.path.join(str(self.gitdir), "objects", oid[:2], oid[2:])
        raw, why = _read(path, OBJ_FILE_CAP, self.d)
        if why:
            return None, None, why
        try:
            body = zlib.decompress(raw)
        except zlib.error:
            return None, None, f"{self.rel} object {oid[:12]} does not inflate"
        header, sep, payload = body.partition(b"\x00")
        m = _OBJ_HEADER.match(header) if sep else None
        if m is None or int(m.group(2)) != len(payload):
            return None, None, f"{self.rel} object {oid[:12]} has an unparseable header"
        return payload, m.group(1).decode(), None

    def commit_tree(self, oid):
        """(tree oid, reason) for a commit object."""
        payload, kind, why = self.body(oid)
        if why:
            return None, why
        if kind != "commit":
            return None, f"{self.rel} HEAD is a {kind}, not a commit"
        first = payload.split(b"\n", 1)[0].decode("ascii", "replace")
        if not first.startswith("tree ") or _oid_len(first[5:].strip()) is None:
            return None, f"{self.rel} commit {oid[:12]} carries no tree line"
        return first[5:].strip(), None

    def tree_entry(self, tree_oid, name):
        """(mode, oid, reason) of one entry of a tree object, or (None, None, reason)."""
        payload, kind, why = self.body(tree_oid)
        if why:
            return None, None, why
        if kind != "tree":
            return None, None, f"{self.rel} object {tree_oid[:12]} is a {kind}, not a tree"
        off = 0
        while off < len(payload):
            sp = payload.find(b" ", off)
            nul = payload.find(b"\x00", sp)
            if sp < 0 or nul < 0:
                return None, None, f"{self.rel} tree {tree_oid[:12]} is malformed"
            mode = payload[off:sp].decode("ascii", "replace")
            entry = payload[sp + 1:nul]
            start = nul + 1
            width = 20                       # sha1 ids only: a sha256 store's refs cannot resolve here
            oid = payload[start:start + width]
            if len(oid) != width:
                return None, None, f"{self.rel} tree {tree_oid[:12]} is truncated"
            off = start + width
            if mode not in ("100644", "100755", "120000", "40000", "160000"):
                return None, None, f"{self.rel} tree {tree_oid[:12]} holds an entry mode the fence does not parse"
            if entry == name:
                return mode, oid.hex(), None
        return None, None, None


def _head_oid(store, d):
    """(oid, reason) for HEAD's commit, or (None, None) when the branch is unborn."""
    gd, rel = store.gitdir, store.rel
    raw, why = _read(os.path.join(str(gd), "HEAD"), TEXT_CAP, d)
    if why:
        return None, why
    text = raw.decode("ascii", "replace").strip()
    hops = 0
    while text.startswith("ref: "):
        hops += 1
        if hops > REF_HOPS:
            return None, f"{rel}/HEAD nests deeper than {REF_HOPS} symbolic refs"
        target = text[5:].strip()
        parts = target.split("/")
        if not target.startswith("refs/") or not all(_ref_component(c) for c in parts):
            return None, f"{rel}/HEAD names an unparseable symbolic ref"
        path = os.path.join(str(gd), *parts)
        if not os.path.lexists(path):
            packed = store.packed_refs.get(target)   # a packed branch is not an unborn one
            if packed is None:
                return None, None                   # unborn branch: nothing at HEAD to contradict
            text = packed
            break
        raw, why = _read(path, TEXT_CAP, d)
        if why:
            return None, why
        text = raw.decode("ascii", "replace").strip()
    if text.startswith("ref: "):
        return None, f"{rel}/HEAD does not settle on an object id"
    if text not in store.present:
        return None, f"{rel}/HEAD names {text[:12]!r}, an object this store does not hold"
    return text, None


def _store(repo, rel, d):
    """(store, reason): validate one `.git` directory as a store this fence parses itself."""
    gd = pathlib.Path(repo) / ".git"
    gds = str(gd)
    entries, why = _listdir(gd, d)
    if why:
        return None, why
    seen = {name: kind for name, kind, _p in entries}
    for name, kind, _ in entries:
        if kind == "d" and name in _STORE_DIRS or kind == "f" and name in _STORE_FILES:
            continue
        return None, f"{rel}/.git/{name} is a store entry the fence cannot prove inert"
    for need, kind, what in (("HEAD", "f", "file"), ("config", "f", "file"), ("objects", "d", "directory")):
        if seen.get(need) != kind:
            return None, f"{rel}/.git has no {need} {what}"
    why = _config(os.path.join(gds, "config"), d, rel)
    if why:
        return None, why
    store = _Store(gd, rel, d)
    loose, why = _loose(os.path.join(gds, "objects"), d, rel)
    if why:
        return None, why
    store.present = loose
    info = os.path.join(gds, "objects", "info")
    if os.path.lexists(info):
        listed, why = _listdir(info, d)
        if why:
            return None, why
        for name, kind, _ in listed:
            if kind != "f" or name not in _OBJECT_INFO:
                return None, f"{rel}/objects/info/{name} is not an inert object-store file"
    pack = os.path.join(gds, "objects", "pack")
    if os.path.lexists(pack):
        packed, why = _pack(pack, d, rel)
        if why:
            return None, why
        store.packed = packed
        store.present |= packed
    else:
        store.packed = set()
    refs = os.path.join(gds, "refs")
    if os.path.lexists(refs):
        why = _refs(refs, d, f"{rel}/.git/refs", store.present)
        if why:
            return None, why
    store.packed_refs = {}
    if "packed-refs" in seen:
        mapping, why = _packed_refs(os.path.join(gds, "packed-refs"), d, rel, store.present)
        if why:
            return None, why
        store.packed_refs = mapping
    logs = os.path.join(gds, "logs")
    if os.path.lexists(logs):
        why = _logs(logs, d, f"{rel}/.git/logs")
        if why:
            return None, why
    hooks = os.path.join(gds, "hooks")
    if os.path.lexists(hooks):
        why = _hooks(hooks, d, rel)
        if why:
            return None, why
    infod = os.path.join(gds, "info")
    if os.path.lexists(infod):
        why = _info(infod, d, rel, store.present)
        if why:
            return None, why
    branches = os.path.join(gds, "branches")
    if os.path.lexists(branches):
        listed, why = _listdir(branches, d)
        if why:
            return None, why
        if listed:
            return None, f"{rel}/.git/branches is not empty"
    if "index" in seen:
        why = _index(os.path.join(gds, "index"), d, rel)
        if why:
            return None, why
    for name in set(seen) & {"description", "COMMIT_EDITMSG", "ORIG_HEAD", "FETCH_HEAD", "MERGE_HEAD", "MERGE_MSG",
                        "MERGE_MODE", "AUTO_MERGE"}:
        why = _textfile(os.path.join(gds, name), d, rel)
        if why:
            return None, why
    oid, why = _head_oid(store, d)
    if why:
        return None, why
    store.head = oid
    return store, None


def _head_path(store, path, d):
    """(kind, reason) for `path`, repo-relative at HEAD: 'blob' | 'absent' | 'tree' | 'gitlink' | 'packed'."""
    if store.head is None:
        return "absent", None
    tree, why = store.commit_tree(store.head)
    if why:
        return None, why
    parts = [p for p in path.split("/") if p]
    for i, part in enumerate(parts):
        mode, oid, why = store.tree_entry(tree, part.encode())
        if why:
            return None, why
        if mode is None:
            return "absent", None
        last = i == len(parts) - 1
        if mode == "160000":
            return ("gitlink" if last else "tree"), None
        if last:
            return ("tree" if mode == "40000" else "blob"), None
        if mode != "40000":
            return "absent", None
        tree = oid
    return "tree", None


# ---------- entry point ----------


def breach(d, argv, tool):
    """Refuse (one-line reason) or admit (None). No child process, no git, and no path outside d is opened,
    stat'ed or readlink'ed: the decision is a walk of d plus a strict parse of the store it holds."""
    _SPENT["files"] = _SPENT["bytes"] = 0
    try:
        d = pathlib.Path(os.path.abspath(str(d)))
        if os.path.islink(str(d)):
            return "fixture dir is a symlink"
        if not os.path.isdir(str(d)):
            return "fixture dir is not a directory"
        vals, why = _argv(d, tool, argv)
        if why:
            return why
        repos, why = _walk(d)
        if why:
            return why
        stores = {}
        for repo in repos:
            rel = _rel(repo, d)
            store, why = _store(repo, rel, d)
            if why:
                return why
            stores[str(repo)] = store
        # The tool's repo root is `--lane`, and a tool that omits the option works in its cwd, which is `d`. Both
        # are held to the same rule: the directory must be a store root the fence validated. Git discovery stops
        # at the first `.git` walking up, so a validated root cannot discover a repo above `d` (f6's vector) —
        # which is why this fence never has to look above `d` to answer.
        lane = vals.get("--lane", ".")
        lane_abs = _lexical(d, lane)
        if lane_abs is None:
            return "--lane resolves outside the fixture"
        store = stores.get(lane_abs)
        if store is None:
            return f"--lane {lane!r} is not a store root the fence validated (discovery would leave the fixture)"
        # The tool reads these as repo paths at HEAD (`cat-file HEAD:<value>`), so a value the fence cannot read
        # that way is refused rather than waved through: absolute, empty or `..`-escaping values name no lane path
        # the fence could resolve, and a path that IS a tree or a gitlink at HEAD is not the blob the tool
        # advertises. An absent path is admitted: a receipt may not exist yet.
        if tool == "order":
            for opt in ("--claims", "--receipt"):
                value = vals.get(opt, "")
                inner = posixpath.normpath(value)
                if value.startswith("/") or inner in ("", ".", "..") or inner.startswith("../"):
                    return f"{opt} {value!r} is not a lane-relative path"
                kind, why = _head_path(store, inner, d)
                if why:
                    return f"{opt}: {why}"
                if kind in ("tree", "gitlink"):
                    return f"{opt} {value} is a {kind} at HEAD, not a blob"
        return None
    except Exception as exc:  # noqa: BLE001 - fail closed: an unhandled shape must never read as admission
        return f"fixture cannot be judged ({type(exc).__name__})"

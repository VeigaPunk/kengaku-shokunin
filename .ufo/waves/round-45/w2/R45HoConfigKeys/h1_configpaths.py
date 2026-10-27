"""Held-out hostile module h1_configpaths (R45HoConfigKeys, kengaku round-45 wave 2): config keys that name a
file outside the fixture without any include. The repo IS the fixture dir, so `../evil/<name>` — the module
build root, `pathlib.Path(d).parent` — lies outside `d`. The landed fence's `.git/config*` text scan checks only
`include`, `extensions.worktreeConfig`, `core.bare` and `core.worktree`; the keys below pass that scan unjudged,
and the fence's git legs (`rev-parse --show-toplevel`, `--absolute-git-dir`, `config --get core.worktree`,
`cat-file -t`) never consult them. Fixture h1-wt-rel is the control: relative `core.worktree` IS scanned and
must be refused; every other fixture is expected to be ADMITTED (the fence miss this module measures)."""
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"
FIRE = "#!/bin/sh\necho fired \"$0\" \"$*\" >> \"$(dirname \"$0\")/fired.log\" 2>/dev/null\nexit 0\n"


def _repo(ctx, d):
    r = ctx.init(d)
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    return r


def _evil(ctx, d, name, text, exe=False):
    """The deliberate outside artefact: under pathlib.Path(d).parent (the module build root), outside d."""
    p = pathlib.Path(d).parent / "evil" / name
    ctx.write(p, text)
    if exe:
        ctx.sh("chmod", "+x", str(p))
    return p


def _key(ctx, r, key, val):
    """Set the hostile key LAST, after every commit, so the build itself is undisturbed."""
    ctx.sh("git", "-C", str(r), "config", key, val)


def _order():
    return ["--lane", ".", "--claims", CLAIMS, "--receipt", RECEIPT]


def b_baseline(ctx, d):
    _repo(ctx, d)
    return _order()


def b_attrs(ctx, d):
    r = _repo(ctx, d)
    _evil(ctx, d, "attrs", "* -text\n")
    _key(ctx, r, "core.attributesFile", "../evil/attrs")
    return _order()


def b_mailmap(ctx, d):
    r = _repo(ctx, d)
    _evil(ctx, d, "mailmap", "Proper Name <proper@kengaku.invalid> <fixture@kengaku.invalid>\n")
    _key(ctx, r, "mailmap.file", "../evil/mailmap")
    return _order()


def b_mailmap_on(ctx, d):
    r = _repo(ctx, d)
    _evil(ctx, d, "mailmap", "Proper Name <proper@kengaku.invalid> <fixture@kengaku.invalid>\n")
    _key(ctx, r, "log.mailmap", "true")
    _key(ctx, r, "mailmap.file", "../evil/mailmap")
    return _order()


def b_fsmon(ctx, d):
    r = _repo(ctx, d)
    _evil(ctx, d, "fsmon", FIRE, exe=True)
    _key(ctx, r, "core.fsmonitor", "../evil/fsmon")
    return _order()


def b_hooks(ctx, d):
    r = _repo(ctx, d)
    _evil(ctx, d, "hooks/post-commit", FIRE, exe=True)
    _key(ctx, r, "core.hooksPath", "../evil/hooks")
    return _order()


def b_wt_rel(ctx, d):
    r = _repo(ctx, d)
    _key(ctx, r, "core.worktree", "../evil-wt")
    return _order()


FIXTURES = [
    {"fid": "h1-baseline", "tool": "order", "expect": "accept", "defects": [], "build": b_baseline},
    {"fid": "h1-attrs", "tool": "order", "expect": "accept", "defects": [], "build": b_attrs},
    {"fid": "h1-mailmap", "tool": "order", "expect": "accept", "defects": [], "build": b_mailmap},
    {"fid": "h1-mailmap-on", "tool": "order", "expect": "accept", "defects": [], "build": b_mailmap_on},
    {"fid": "h1-fsmon", "tool": "order", "expect": "accept", "defects": [], "build": b_fsmon},
    {"fid": "h1-hooks", "tool": "order", "expect": "accept", "defects": [], "build": b_hooks},
    {"fid": "h1-wt-rel", "tool": "order", "expect": "error", "defects": [], "build": b_wt_rel},
]

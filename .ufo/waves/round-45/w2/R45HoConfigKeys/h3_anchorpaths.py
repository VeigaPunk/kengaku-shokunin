"""Held-out hostile module h3_anchorpaths (R45HoConfigKeys, kengaku round-45 wave 2): the same path-naming
config keys under the ANCHOR tool's git surface (`ls-tree -r`, `ls-files --cached`, `cat-file --batch`), so the
honour measurement covers both landed tools. The fixture is a green anchor lane: one census-shaped row bound by
its explicit lane path to the committed receipt capture, so the tool runs its whole git surface and exits 0.
The repo IS the fixture dir; artefacts sit under `pathlib.Path(d).parent`. All fixtures are expected to be
ADMITTED by the landed fence (none of these keys is scanned or probed)."""
import hashlib
import pathlib

RECEIPT = "corpus/evidence/round42/receipt.txt"
BODY = "receipt\n"
DIGEST = hashlib.sha256(BODY.encode()).hexdigest()
HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|---|---|---|---|---|---|---|---|---|---|---|\n")
ROW = (f"| S901 | captured at {RECEIPT} | capture | A | fixture | sha256 {DIGEST} "
       "| held-out config-key probe | mined | 2026-10-26 | 180d | - |\n")
FIRE = "#!/bin/sh\necho fired \"$0\" \"$*\" >> \"$(dirname \"$0\")/fired.log\" 2>/dev/null\nexit 0\n"


def _arepo(ctx, d):
    r = ctx.init(d)
    ctx.write(r / RECEIPT, BODY)
    ctx.write(r / "corpus/SOURCES.md", HEADER + ROW)
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "sources")
    return r


def _evil(ctx, d, name, text, exe=False):
    p = pathlib.Path(d).parent / "evil" / name
    ctx.write(p, text)
    if exe:
        ctx.sh("chmod", "+x", str(p))
    return p


def _key(ctx, r, key, val):
    ctx.sh("git", "-C", str(r), "config", key, val)


def _anchor():
    return ["--lane", ".", "--evidence-ref", "index"]


def b_baseline(ctx, d):
    _arepo(ctx, d)
    return _anchor()


def b_attrs(ctx, d):
    r = _arepo(ctx, d)
    _evil(ctx, d, "attrs", "* -text\n")
    _key(ctx, r, "core.attributesFile", "../evil/attrs")
    return _anchor()


def b_mailmap_on(ctx, d):
    r = _arepo(ctx, d)
    _evil(ctx, d, "mailmap", "Proper Name <proper@kengaku.invalid> <fixture@kengaku.invalid>\n")
    _key(ctx, r, "log.mailmap", "true")
    _key(ctx, r, "mailmap.file", "../evil/mailmap")
    return _anchor()


def b_fsmon(ctx, d):
    r = _arepo(ctx, d)
    _evil(ctx, d, "fsmon", FIRE, exe=True)
    _key(ctx, r, "core.fsmonitor", "../evil/fsmon")
    return _anchor()


def b_hooks(ctx, d):
    r = _arepo(ctx, d)
    _evil(ctx, d, "hooks/post-commit", FIRE, exe=True)
    _key(ctx, r, "core.hooksPath", "../evil/hooks")
    return _anchor()


FIXTURES = [
    {"fid": "h3-baseline", "tool": "anchor", "expect": "accept", "defects": [], "build": b_baseline},
    {"fid": "h3-attrs", "tool": "anchor", "expect": "accept", "defects": [], "build": b_attrs},
    {"fid": "h3-mailmap-on", "tool": "anchor", "expect": "accept", "defects": [], "build": b_mailmap_on},
    {"fid": "h3-fsmon", "tool": "anchor", "expect": "accept", "defects": [], "build": b_fsmon},
    {"fid": "h3-hooks", "tool": "anchor", "expect": "accept", "defects": [], "build": b_hooks},
]

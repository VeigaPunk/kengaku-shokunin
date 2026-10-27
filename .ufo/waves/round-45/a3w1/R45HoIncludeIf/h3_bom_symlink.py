"""Held-out hostile module h3 (R45HoIncludeIf): two independent _INCLUDE_RE evasions.

f001/f003: UTF-8 BOM at byte 0 of `.git/config` — git skips the BOM at file start and parses
`[include]`/`[includeIf]` on line 1; the fence regex needs `[` (or whitespace) at line start and the
BOM's 3 bytes are neither, so no refusal leg runs and the include fires inside the fence's own git
children (probed: email applied, 1 outside open on rev-parse --show-toplevel).

f002: the include target itself is a SYMLINK *inside* `.git` pointing outside d. The fence's walk
removes `.git` from `dirs` (`dirs[:] = sorted(x for x in dirs if x != ".git")`), so `.git/inc.cfg`
is never inspected by the symlink leg, never matched by the `config*` glob, and git follows it to
the outside file.
"""
import os
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def _repo(ctx, d, fid):
    r = ctx.init(d / "lane")
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    side = pathlib.Path(d).parent / f"side-{fid}.cfg"
    ctx.write(side, f"[user]\n\temail = {fid}@invalid\n")
    return r, side


def build_bom_include(ctx, d):
    r, side = _repo(ctx, pathlib.Path(d), "h3-bom-inc")
    cfg = r / ".git" / "config"
    cfg.write_bytes(b"\xef\xbb\xbf[include]\n\tpath = " + str(side).encode() + b"\n" + cfg.read_bytes())
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


def build_cr_include_symlink(ctx, d):
    r, side = _repo(ctx, pathlib.Path(d), "h3-cr-symlink")
    os.symlink(str(side), r / ".git" / "inc.cfg")
    cfg = r / ".git" / "config"
    cfg.write_bytes(cfg.read_bytes() + b"\r[include]\n\tpath = inc.cfg\n")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


def build_bom_includeif(ctx, d):
    r, side = _repo(ctx, pathlib.Path(d), "h3-bom-inclif")
    cfg = r / ".git" / "config"
    head = b"\xef\xbb\xbf[includeIf \"onbranch:master\"]\n\tpath = " + str(side).encode() + b"\n"
    cfg.write_bytes(head + cfg.read_bytes())
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


def build_cr_include_anchor(ctx, d):
    r, side = _repo(ctx, pathlib.Path(d), "h3-cr-anchor")
    cfg = r / ".git" / "config"
    cfg.write_bytes(cfg.read_bytes() + f"\r[include]\n\tpath = {side}\n".encode())
    return ["--lane", "lane"]


FIXTURES = [
    {"fid": "h3-bom-include", "tool": "order", "expect": "accept", "defects": [], "build": build_bom_include},
    {"fid": "h3-cr-include-symlink", "tool": "order", "expect": "accept", "defects": [],
     "build": build_cr_include_symlink},
    {"fid": "h3-bom-includeif", "tool": "order", "expect": "accept", "defects": [], "build": build_bom_includeif},
    {"fid": "h3-cr-include-anchor", "tool": "anchor", "expect": "error", "defects": [],
     "build": build_cr_include_anchor},
]

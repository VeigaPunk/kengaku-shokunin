"""Held-out hostile module h1 (R45HoIncludeIf): `[include]` hidden from the round-45 fence's
_INCLUDE_RE (`^[ \\t]*\\[[ \\t]*include`) by a bare carriage return before the section header.
git 2.56 treats a leading `\\r` as whitespace and parses the include; the fence regex does not
match `\\r`, so no refusal leg ever runs and the fence's own rev-parse/config/cat-file children
open the included file outside d. Probed: `\\r[include]` applied `user.email` from a file at
d.parent and produced 1 outside open under `strace -y` on `rev-parse --show-toplevel`.
"""
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


def build_cr_lf(ctx, d):
    r, side = _repo(ctx, pathlib.Path(d), "h1-cr-lf")
    cfg = r / ".git" / "config"
    cfg.write_bytes(cfg.read_bytes() + f"\r[include]\n\tpath = {side}\n".encode())
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


def build_cr_crlf(ctx, d):
    r, side = _repo(ctx, pathlib.Path(d), "h1-cr-crlf")
    cfg = r / ".git" / "config"
    cfg.write_bytes(cfg.read_bytes() + f"\r[include]\r\n\tpath = {side}\r\n".encode())
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [
    {"fid": "h1-cr-include-lf", "tool": "order", "expect": "accept", "defects": [], "build": build_cr_lf},
    {"fid": "h1-cr-include-crlf", "tool": "order", "expect": "accept", "defects": [], "build": build_cr_crlf},
]

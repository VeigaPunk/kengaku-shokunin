"""Refusal fixture f13 (round-45 held-out h3, first of its two independent evasions, `R45HoIncludeIf`): a UTF-8
BOM at byte 0 of `.git/config` — git skips the BOM at file start and parses `[include]`/`[includeIf]` on line 1;
the landed fence's regex needs `[` or whitespace at line start and the BOM's three bytes are neither, so no
refusal leg runs and the include fires inside the fence's own git children. One class: BOM-prefixed config
section at file start. Base fence (`a3w1/R45HoIncludeIf/driver.out`): both ADMIT (7 and 5 outside opens)."""
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


def build_bom_includeif(ctx, d):
    r, side = _repo(ctx, pathlib.Path(d), "h3-bom-inclif")
    cfg = r / ".git" / "config"
    head = b"\xef\xbb\xbf[includeIf \"onbranch:master\"]\n\tpath = " + str(side).encode() + b"\n"
    cfg.write_bytes(head + cfg.read_bytes())
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [
    {"fid": "h3-bom-include", "tool": "order", "expect": "accept", "defects": [], "build": build_bom_include},
    {"fid": "h3-bom-includeif", "tool": "order", "expect": "accept", "defects": [], "build": build_bom_includeif},
]

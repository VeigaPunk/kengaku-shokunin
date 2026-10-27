"""Refusal fixture f11 (round-45 held-out h1, `R45HoIncludeIf`): a bare carriage return immediately before a
`[include]` header is whitespace to git's config parser but not to the landed fence's `_INCLUDE_RE`
(`^[ \\t]*\\[[ \\t]*include`), so no refusal leg runs and the fence's own git children open the include target
outside `d`. One class: CR-prefixed include directive, order leg (LF and CRLF forms) and anchor leg
(`h3-cr-include-anchor` from `R45HoIncludeIf/h3_bom_symlink.py`, same class, other tool).
Base fence (`a3w1/R45HoIncludeIf/driver.out`): all three fixtures ADMIT, 7/7/3 outside opens."""
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


def build_cr_include_anchor(ctx, d):
    r, side = _repo(ctx, pathlib.Path(d), "h3-cr-anchor")
    cfg = r / ".git" / "config"
    cfg.write_bytes(cfg.read_bytes() + f"\r[include]\n\tpath = {side}\n".encode())
    return ["--lane", "lane"]


FIXTURES = [
    {"fid": "h1-cr-include-lf", "tool": "order", "expect": "accept", "defects": [], "build": build_cr_lf},
    {"fid": "h1-cr-include-crlf", "tool": "order", "expect": "accept", "defects": [], "build": build_cr_crlf},
    {"fid": "h3-cr-include-anchor", "tool": "anchor", "expect": "error", "defects": [],
     "build": build_cr_include_anchor},
]

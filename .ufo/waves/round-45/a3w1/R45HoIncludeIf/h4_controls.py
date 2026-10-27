"""Control module h4 (R45HoIncludeIf): plain-text `[includeIf]` variants in every case/style my class
names — the fence's own advertised behaviour is to refuse these. If any is ADMITTED or produces an
outside open, the regex leg is broken worse than the \\r/BOM evasions show; if all are refused with
zero opens, they witness that the include leg works on the text it can see (calibration controls for
h1-h3: identical config except the evasion prefix).
"""
import os
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def _one(ctx, d, fid, header, anchor=False):
    r = ctx.init(d / "lane")
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    side = pathlib.Path(d).parent / f"side-{fid}.cfg"
    ctx.write(side, f"[user]\n\temail = {fid}@invalid\n")
    cfg = r / ".git" / "config"
    cfg.write_bytes(cfg.read_bytes() + f"{header}\n\tpath = {side}\n".encode())
    if anchor:
        return ["--lane", "lane"]
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


def build_onbranch(ctx, d):
    return _one(ctx, pathlib.Path(d), "h4-onbranch", '[includeIf "onbranch:master"]')


def build_mixedcase_gitdir(ctx, d):
    lane = pathlib.Path(d) / "lane"
    return _one(ctx, pathlib.Path(d), "h4-mixedcase",
                f'[InClUdEiF "gitdir:{os.path.realpath(lane / ".git")}"]')


def build_gitdir_anchor(ctx, d):
    return _one(ctx, pathlib.Path(d), "h4-gitdir-anchor", '[includeIf "gitdir:**/lane/.git"]',
                anchor=True)


FIXTURES = [
    {"fid": "h4-plain-inclif-onbranch", "tool": "order", "expect": "accept", "defects": [],
     "build": build_onbranch},
    {"fid": "h4-mixedcase-inclif-gitdir", "tool": "order", "expect": "accept", "defects": [],
     "build": build_mixedcase_gitdir},
    {"fid": "h4-plain-inclif-gitdir-anchor", "tool": "anchor", "expect": "error", "defects": [],
     "build": build_gitdir_anchor},
]

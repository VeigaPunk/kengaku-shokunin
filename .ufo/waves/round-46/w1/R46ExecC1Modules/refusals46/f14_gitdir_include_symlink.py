"""Refusal fixture f14 (round-45 held-out h3, second of its two independent evasions, `R45HoIncludeIf`): the
include TARGET is a symlink placed inside `.git` (`lane/.git/inc.cfg`) pointing outside `d`. The landed fence's
walk prunes every `.git` directory (`dirs[:] = sorted(x for x in dirs if x != ".git")`), so that symlink is never
inspected and never matches the `config*` glob; git follows it to the outside file. One class: include target
symlink hidden inside the pruned git dir. Base fence (`a3w1/R45HoIncludeIf/driver.out`): ADMIT, 7 outside opens."""
import os
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    d = pathlib.Path(d)
    r = ctx.init(d / "lane")
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    side = d.parent / "side-h3-cr-symlink.cfg"
    ctx.write(side, "[user]\n\temail = h3-cr-symlink@invalid\n")
    os.symlink(str(side), r / ".git" / "inc.cfg")
    cfg = r / ".git" / "config"
    cfg.write_bytes(cfg.read_bytes() + b"\r[include]\n\tpath = inc.cfg\n")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "h3-cr-include-symlink", "tool": "order", "expect": "accept", "defects": [], "build": build}]

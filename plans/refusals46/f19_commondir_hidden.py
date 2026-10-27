"""Refusal fixture f19 (round-45 held-out `R45HoCommondir2/modules/g4_cdrel_hidden.py`): the round-44 commondir
escape, but planted one level BELOW the `.git` directory the landed fence's walk prunes — at
`repo/.git/modules/escape/.git/commondir`, a RELATIVE path resolved against the gitdir. `--lane` names that hidden
store; both rev-parse legs answer inside `d`, so the fence ADMITS and its own git children open the outside
common store (config, refs, objects) while deciding. One class: relative `commondir` redirect hidden below a
pruned `.git`. Base fence (`a3w1/R45HoCommondir2.md`): ADMIT, 32 outside opens."""
import os
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def _store(ctx, d, name):
    store = pathlib.Path(d).parent / name
    ctx.init(store)
    ctx.write(store / CLAIMS, "nothing ran\n")
    ctx.git(store, "add", "-A")
    ctx.git(store, "commit", "-qm", "claims")
    ctx.write(store / RECEIPT, "receipt\n")
    ctx.git(store, "add", "-A")
    ctx.git(store, "commit", "-qm", "receipt")
    return store


def build(ctx, d):
    out = _store(ctx, d, "g4-out")
    r = ctx.init(d / "repo")
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    hidden = r / ".git" / "modules" / "escape"  # never walked: os.walk prunes `.git` dirs
    ctx.init(hidden)
    rel = os.path.relpath(str(out / ".git"), str(hidden / ".git"))
    ctx.write(hidden / ".git" / "commondir", rel + "\n")  # relative to the gitdir, escaping d via ..
    return ["--lane", "repo/.git/modules/escape", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "g4-cd-hidden", "tool": "order", "expect": "accept", "defects": [], "build": build}]

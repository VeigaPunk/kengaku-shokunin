"""Held-out hostile module g4 (R45HoCommondir2, vector a — walk-invisible delivery): the SAME relative
`.git/commondir` escape as g1, but planted at `repo/.git/modules/escape/.git/commondir`, one level BELOW the
`.git` directory the fence's walk prunes. The fixture then points `--lane` at that hidden store. Both fence
legs answer INSIDE d (`--show-toplevel` and `--absolute-git-dir` report the per-worktree gitdir), so if the
fence admits it, its git children will have opened the outside COMMON store (config, refs, objects) while
deciding — an admit WITH outside opens in one fixture."""
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

"""Extra hostile shapes I wrote to test that the repaired fence generalizes beyond the frozen held-out set."""
import os
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def _repo(ctx, d, name="lane"):
    r = ctx.init(pathlib.Path(d) / name)
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    return r


def _argv():
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


def bare_store(ctx, d):
    """Bare store at d/store with an include in its own config (not under any .git directory)."""
    d = pathlib.Path(d)
    store = d / "store"
    store.mkdir(parents=True)
    ctx.sh("git", "init", "-q", "--bare", str(store))
    side = pathlib.Path(d).parent / "bare-side.cfg"
    ctx.write(side, "[user]\n\temail = bare-outside@invalid\n")
    with open(store / "config", "a") as fh:
        fh.write("[include]\n\tpath = " + str(side) + "\n")
    r = _repo(ctx, d)
    return _argv()


def http_alternates(ctx, d):
    r = _repo(ctx, d)
    (r / ".git/objects/info").mkdir(parents=True, exist_ok=True)
    (r / ".git/objects/info/http-alternates").write_text("https://outside.invalid/objects/\n")
    return _argv()


def worktree_key_inside(ctx, d):
    """core.worktree set to the repo itself (legitimate shape): must be ADMITTED."""
    r = _repo(ctx, d)
    ctx.sh("git", "-C", str(r), "config", "core.worktree", ".")
    return _argv()


def nested_second_repo_inside(ctx, d):
    """Two real repos inside d, the second nested in the first one's worktree: must be ADMITTED."""
    r = _repo(ctx, d)
    ctx.write(r / "inner/x.txt", "x\n")
    inner = ctx.init(r / "inner")
    ctx.write(inner / "y.txt", "y\n")
    ctx.git(inner, "add", "-A")
    ctx.git(inner, "commit", "-qm", "inner")
    return _argv()


def worktree_key_outside(ctx, d):
    r = _repo(ctx, d)
    ctx.sh("git", "-C", str(r), "config", "core.worktree", str(pathlib.Path(d).parent / "wt"))
    return _argv()


def gitlink_file_dotgit_in_d(ctx, d):
    """d/lane/.git is a symlink to a git dir INSIDE d: refusal (no symlinked git dir is provable)."""
    r = _repo(ctx, d, "real")
    (pathlib.Path(d) / "lane").mkdir()
    os.symlink(r / ".git", pathlib.Path(d) / "lane" / ".git")
    return _argv()


def alternates_inside(ctx, d):
    """alternates pointing to a store INSIDE d: refusal (a borrowed store is not provable)."""
    other = ctx.init(pathlib.Path(d) / "other")
    ctx.write(other / "z.txt", "z\n")
    ctx.git(other, "add", "-A")
    ctx.git(other, "commit", "-qm", "z")
    r = _repo(ctx, d)
    (r / ".git/objects/info").mkdir(parents=True, exist_ok=True)
    (r / ".git/objects/info/alternates").write_text(str(other / ".git/objects") + "\n")
    return _argv()


def include_in_worktree_config_inside(ctx, d):
    """config.worktree carrying an include whose target is INSIDE d: refusal (any include)."""
    r = _repo(ctx, d)
    target = pathlib.Path(d) / "inside.cfg"
    ctx.write(target, "[user]\n\temail = inside@invalid\n")
    ctx.write(r / ".git/config.worktree", "[include]\n\tpath = " + str(target) + "\n")
    return _argv()


FIXTURES = [
    {"fid": "x-bare-store-include", "tool": "order", "expect": "error", "defects": [], "build": bare_store},
    {"fid": "x-http-alternates", "tool": "order", "expect": "error", "defects": [], "build": http_alternates},
    {"fid": "x-core-worktree-inside", "tool": "order", "expect": "accept", "defects": [], "build": worktree_key_inside},
    {"fid": "x-second-repo-inside", "tool": "order", "expect": "accept", "defects": [], "build": nested_second_repo_inside},
    {"fid": "x-core-worktree-outside", "tool": "order", "expect": "error", "defects": [], "build": worktree_key_outside},
    {"fid": "x-git-symlink-inside", "tool": "order", "expect": "error", "defects": [], "build": gitlink_file_dotgit_in_d},
    {"fid": "x-alternates-inside", "tool": "order", "expect": "error", "defects": [], "build": alternates_inside},
    {"fid": "x-wtcfg-include-inside", "tool": "order", "expect": "error", "defects": [], "build": include_in_worktree_config_inside},
]

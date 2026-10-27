"""Held-out hostile module R45HoCommondir2 h3 (wave 2): the lane repo's store carries `worktrees/<id>/`
linked-worktree metadata whose `commondir`/`gitdir` point OUTSIDE the fixture dir. The landed fence's walk
prunes `.git` from descent and its store scan checks only `commondir`, `objects/info/alternates` and
`config*` at the gitdir top, so `worktrees/<id>/commondir` is never inspected; the git legs probe only the
main worktree, which never reads `worktrees/`. Expected: the fence admits it."""
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def _lane(ctx, d):
    r = ctx.init(d / "lane")
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    return r


def _meta(ctx, d, r, store_name, commondir_text):
    store = pathlib.Path(d).parent / store_name
    ctx.init(store)
    wtd = r / ".git" / "worktrees" / "wt1"
    wtd.mkdir(parents=True)
    (wtd / "commondir").write_text(commondir_text + "\n")
    (wtd / "gitdir").write_text(str(pathlib.Path(d).parent / "outside-wt" / ".git") + "\n")
    (wtd / "HEAD").write_text("ref: refs/heads/master\n")


def build_abs(ctx, d):
    d = pathlib.Path(d)
    r = _lane(ctx, d)
    _meta(ctx, d, r, "wtstore-abs", str(d.parent / "wtstore-abs" / ".git"))
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


def build_rel(ctx, d):
    d = pathlib.Path(d)
    r = _lane(ctx, d)
    _meta(ctx, d, r, "wtstore-rel", "../../../../../wtstore-rel/.git")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [
    {"fid": "h3-wt-abs", "tool": "order", "expect": "accept", "defects": [], "build": build_abs},
    {"fid": "h3-wt-rel", "tool": "order", "expect": "accept", "defects": [], "build": build_rel},
]

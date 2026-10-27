"""Refusal fixture F7 (`R44SentinelFences` V1): the repo's `.git` is a real directory inside d, but a
hand-written `.git/commondir` sends refs, objects and config to a store built BESIDE d. `rev-parse
--show-toplevel` and `--absolute-git-dir` both answer inside d, so the round-44 store fence admits it; the
round-45 fence refuses any `.git/commondir` outright (no module-built repo needs one)."""
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def _store(ctx, d, name, claims_text):
    store = pathlib.Path(d).parent / name
    ctx.init(store)
    ctx.write(store / CLAIMS, claims_text)
    ctx.git(store, "add", "-A")
    ctx.git(store, "commit", "-qm", "claims")
    ctx.write(store / RECEIPT, "receipt\n")
    ctx.git(store, "add", "-A")
    ctx.git(store, "commit", "-qm", "receipt")
    return store


def _lane(d, store):
    lane = pathlib.Path(d) / "lane"
    gd = lane / ".git"
    gd.mkdir(parents=True)
    (gd / "commondir").write_text(str(store / ".git") + "\n")
    (gd / "HEAD").write_text("ref: refs/heads/master\n")
    return lane


def build_accept(ctx, d):
    store = _store(ctx, d, "storeA", "nothing ran\n")
    _lane(d, store)
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


def build_reject(ctx, d):
    store = _store(ctx, d, "storeB", "CASE x observed=1\n")
    _lane(d, store)
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


def build_anchor(ctx, d):
    store = pathlib.Path(d).parent / "storeC"
    ctx.init(store)
    ctx.write(store / "note.txt", "x\n")
    ctx.git(store, "add", "-A")
    ctx.git(store, "commit", "-qm", "x")
    lane = pathlib.Path(d) / "lane"
    gd = lane / ".git"
    gd.mkdir(parents=True)
    (gd / "commondir").write_text(str(store / ".git") + "\n")
    (gd / "HEAD").write_text("ref: refs/heads/master\n")
    return ["--lane", str(lane)]


FIXTURES = [
    {"fid": "f7-cd-accept", "tool": "order", "expect": "accept", "defects": [], "build": build_accept},
    {"fid": "f7-cd-reject", "tool": "order", "expect": "reject", "defects": [], "build": build_reject},
    {"fid": "f7-cd-anchor", "tool": "anchor", "expect": "error", "defects": [], "build": build_anchor},
]

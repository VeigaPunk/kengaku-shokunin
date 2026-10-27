"""Fixture shape: the repo's per-worktree gitdir is a DIRECTORY inside d, but a hand-written `commondir`
(and its HEAD) sends refs, objects and config to a storage dir built BESIDE d. `rev-parse --show-toplevel`
and `rev-parse --absolute-git-dir` both answer inside d, so the round-44 store fence has nothing to refuse,
while the measured history (both commits, the claims blob and the receipt blob) lives outside d.
"""
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
    ctx.write(store / "corpus/evidence/round42/x.txt", "capture\n")
    ctx.git(store, "add", "-A")
    ctx.git(store, "commit", "-qm", "capture")
    gd = pathlib.Path(d) / ".git"
    ctx.write(gd / "commondir", str(store / ".git") + "\n")
    ctx.write(gd / "HEAD", "ref: refs/heads/master\n")
    ctx.write(pathlib.Path(d) / "corpus/SOURCES.md", "# no rows\n")
    return ["--lane", "."]

FIXTURES = [
    {"fid": "cd-accept", "tool": "order", "expect": "accept", "defects": [], "build": build_accept},
    {"fid": "cd-reject", "tool": "order", "expect": "reject", "defects": [], "build": build_reject},
    {"fid": "cd-anchor", "tool": "anchor", "expect": "accept", "defects": [], "build": build_anchor},
]

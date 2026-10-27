"""Held-out hostile module R45HoCommondir2 h1 (wave 2): `.git/commondir` whose target is RELATIVE, resolved
against the gitdir that holds it, escaping the fixture dir via `..` (f7 used an absolute target). The landed
fence refuses any `.git/commondir` outright before any git child exists, so the expected verdict is a clean
refusal with no outside open; this probe measures whether the relative form changes that."""
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


def _lane(d, commondir_text):
    lane = pathlib.Path(d) / "lane"
    gd = lane / ".git"
    gd.mkdir(parents=True)
    (gd / "commondir").write_text(commondir_text + "\n")
    (gd / "HEAD").write_text("ref: refs/heads/master\n")
    return lane


def build_rel(ctx, d):
    _store(ctx, d, "cdstore")
    _lane(d, "../../../cdstore/.git")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


def build_abs(ctx, d):
    _store(ctx, d, "cdstore-abs")
    _lane(d, str(pathlib.Path(d).parent / "cdstore-abs" / ".git"))
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [
    {"fid": "h1-cdrel", "tool": "order", "expect": "accept", "defects": [], "build": build_rel},
    {"fid": "h1-cdabs-ctrl", "tool": "order", "expect": "accept", "defects": [], "build": build_abs},
]

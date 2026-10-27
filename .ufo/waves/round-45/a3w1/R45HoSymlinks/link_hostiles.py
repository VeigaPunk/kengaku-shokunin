"""Held-out link probes for the round-45 fixture fence."""
import os
import pathlib

CLAIMS = "claims.md"
RECEIPT = "receipt.md"


def _repo(ctx, d, name):
    r = ctx.init(pathlib.Path(d) / name)
    ctx.write(r / CLAIMS, "nothing ran\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "claims")
    ctx.write(r / RECEIPT, "receipt\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-qm", "receipt")
    return r


def build_objects_out(ctx, d):
    d = pathlib.Path(d)
    r = _repo(ctx, d, "lane")
    outside = d.parent / "outside-objects"
    os.rename(r / ".git/objects", outside)
    os.symlink(outside, r / ".git/objects")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


def build_git_symlink_inside(ctx, d):
    d = pathlib.Path(d)
    r = _repo(ctx, d, "real-lane")
    (d / "lane").mkdir()
    os.symlink(r / ".git", d / "lane/.git")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


def build_claims_symlink_out(ctx, d):
    d = pathlib.Path(d)
    r = _repo(ctx, d, "lane")
    outside = d.parent / "outside-claims"
    outside.write_text("outside marker\n")
    (r / CLAIMS).unlink()
    os.symlink(outside, r / CLAIMS)
    return ["--lane", "lane", "--claims", "lane/" + CLAIMS, "--receipt", "lane/" + RECEIPT]


def build_objects_hardlinked_out(ctx, d):
    d = pathlib.Path(d)
    r = _repo(ctx, d, "lane")
    outside = d.parent / "outside-hardlinks"
    outside.mkdir()
    for p in (r / ".git/objects").rglob("*"):
        if p.is_file():
            q = outside / p.relative_to(r / ".git/objects")
            q.parent.mkdir(parents=True, exist_ok=True)
            os.link(p, q)
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


def build_include_chain_inside(ctx, d):
    d = pathlib.Path(d)
    r = _repo(ctx, d, "lane")
    target = d / "inside-include.cfg"
    target.write_text("[user]\n email = inside@invalid\n")
    os.symlink(target, d / "inc2")
    os.symlink(d / "inc2", d / "inc1")
    ctx.sh("git", "-C", str(r), "config", "--add", "include.path", str(d / "inc1"))
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [
    {"fid": "link-objects-symlink-out", "tool": "order", "expect": "error", "defects": [], "build": build_objects_out},
    {"fid": "link-git-symlink-in", "tool": "order", "expect": "error", "defects": [], "build": build_git_symlink_inside},
    {"fid": "link-claims-symlink-out", "tool": "order", "expect": "error", "defects": [], "build": build_claims_symlink_out},
    {"fid": "link-objects-hardlink-out", "tool": "order", "expect": "accept", "defects": [], "build": build_objects_hardlinked_out},
    {"fid": "link-include-chain-in", "tool": "order", "expect": "error", "defects": [], "build": build_include_chain_inside},
]

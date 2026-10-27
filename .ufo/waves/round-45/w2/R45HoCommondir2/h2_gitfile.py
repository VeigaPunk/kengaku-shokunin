"""Held-out hostile module R45HoCommondir2 h2 (wave 2): the fixture's git store lives beside d and `d/.git`
is a FILE whose `gitdir:` line is RELATIVE (f1 used an absolute target). Probe-measured on this host
(gtest probe, 2026-10-26): this git parses `gitdir: <one space> <relative path>` and follows it, while
space/tab-padded or leading-space lines are rejected by git itself. Fixtures: the file left visible (the
fence's walk refuses any `.git` file outright); the same file hidden by making d execute-only (mode 111)
after building, so the fence's os.walk cannot list d while `git -C d` still traverses d and opens `d/.git`,
following the relative gitdir to a store OUTSIDE d (expected: refusal WITH outside opens = READ defect) and
to a store INSIDE d (expected: ADMIT, bypassing the fence's structural `.git`-file refusal)."""
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def _separate_outside(ctx, d, store_name, gitfile_text):
    d = pathlib.Path(d)
    gd = d.parent / store_name
    ctx.sh("git", "init", "-q", "-b", "master", "--separate-git-dir", str(gd), str(d))
    ctx.write(d / CLAIMS, "nothing ran\n")
    ctx.git(d, "add", "--", CLAIMS)
    ctx.git(d, "commit", "-qm", "claims")
    ctx.write(d / RECEIPT, "receipt\n")
    ctx.git(d, "add", "--", RECEIPT)
    ctx.git(d, "commit", "-qm", "receipt")
    ctx.write(d / ".git", gitfile_text)
    return d


def _separate_inside(ctx, d):
    d = pathlib.Path(d)
    seed = d / "seed"
    ctx.sh("git", "init", "-q", "-b", "master", "--separate-git-dir", str(d / "inner-store"), str(seed))
    ctx.write(d / "inner-store" / "config",
              "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n")
    ctx.sh("mv", str(seed / ".git"), str(d / ".git"))
    ctx.sh("rmdir", str(seed))
    ctx.write(d / ".git", "gitdir: inner-store\n")
    ctx.write(d / CLAIMS, "nothing ran\n")
    ctx.git(d, "add", "--", CLAIMS)
    ctx.git(d, "commit", "-qm", "claims")
    ctx.write(d / RECEIPT, "receipt\n")
    ctx.git(d, "add", "--", RECEIPT)
    ctx.git(d, "commit", "-qm", "receipt")
    return d


def build_visible(ctx, d):
    _separate_outside(ctx, d, "gfstore-a", "gitdir: ../gfstore-a\n")
    return ["--lane", ".", "--claims", CLAIMS, "--receipt", RECEIPT]


def build_padded(ctx, d):
    _separate_outside(ctx, d, "gfstore-p", "gitdir:   ../gfstore-p\n")
    return ["--lane", ".", "--claims", CLAIMS, "--receipt", RECEIPT]


def build_hidden_outside(ctx, d):
    d = _separate_outside(ctx, d, "gfstore-b", "gitdir: ../gfstore-b\n")
    ctx.sh("chmod", "111", str(d))
    return ["--lane", ".", "--claims", CLAIMS, "--receipt", RECEIPT]


def build_hidden_inside(ctx, d):
    d = _separate_inside(ctx, d)
    ctx.sh("chmod", "111", str(d))
    return ["--lane", ".", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [
    {"fid": "h2-gitfile-rel-visible", "tool": "order", "expect": "accept", "defects": [], "build": build_visible},
    {"fid": "h2-gitfile-pad-visible", "tool": "order", "expect": "accept", "defects": [], "build": build_padded},
    {"fid": "h2-gitfile-rel-hidden-outside", "tool": "order", "expect": "accept", "defects": [], "build": build_hidden_outside},
    {"fid": "h2-gitfile-rel-hidden-inside", "tool": "order", "expect": "accept", "defects": [], "build": build_hidden_inside},
]

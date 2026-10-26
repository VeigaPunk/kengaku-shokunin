"""Round-42 pre-freeze direction module (L1 KengakuR42) for the nine anchor near-variants of round42_c1_verify.py.

Ported from the round-40 wave-2 builders in `.ufo/waves/round-40/falsify/F40XMutAnchor/` (W1 W3 W6 W7 W9 W12
W13 W14 W15) to the round-42 battery contract: each fixture is a one-row git repository built from nothing in
the fixture dir. Committed as freeze evidence; the battery42 modules may not import, copy or read it.
"""
import hashlib

PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
HDR = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
       "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")


def dig(b):
    return hashlib.sha256(b).hexdigest()


def row(sid, source, anchor):
    return (f"| {sid} | {source} | code | A | fixture | sha256 {anchor} | fixture row | mined | "
            "2026-10-26 | 180d | corpus/knowledge/x.md |")


def cap(ctx, r, reldir, body, name="test_outputs.py", sums=True, toml=None):
    base = r / "corpus/evidence" / reldir
    ctx.write(base / name, body)
    if sums:
        ctx.write(base / "SHA256SUMS", f"{dig(body)}  {name}\n")
    if toml is not None:
        ctx.write(base / "task.toml", toml)
    return dig(body)


def commit(ctx, r):
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "fixture")


def w1(ctx, d):
    r = ctx.init(d / "repo")
    h = cap(ctx, r, "round41/anchor-captures", b"w1 capture body\n", name="capture.txt")
    ctx.write(r / "corpus/evidence/round41/anchor-captures/PROVENANCE.md",
              "| sid | file | note |\n|---|---|---|\n"
              "| S900 | `capture.txt` | captured beside this table; the table carries no pinned URL |\n")
    ctx.write(r / "corpus/SOURCES.md", HDR + row("S900", "task generator, captured beside PROVENANCE.md", h) + "\n")
    commit(ctx, r)
    return ["--lane", str(r)]


def w3(ctx, d):
    r = ctx.init(d / "repo")
    h = cap(ctx, r, "round41/w3cap", b"w3 capture body\n")
    url = f"https://raw.githubusercontent.com/o/r/{PIN}/plain-cap/tests/test_outputs.py"
    ctx.write(r / "corpus/evidence/round41/w3cap/PROVENANCE.md",
              "| url | file |\n|---|---|---|\n"
              f"| {url} | `test_outputs.py` | pinned upstream file, no row id in this table |\n")
    ctx.write(r / "corpus/SOURCES.md", HDR + row("S901", f"pinned at {url}", h) + "\n")
    commit(ctx, r)
    return ["--lane", str(r)]


def w6(ctx, d):
    r = ctx.init(d / "repo")
    cap(ctx, r, "round41/w6a", b"w6 capture A\n")
    db = cap(ctx, r, "round41/w6b", b"w6 capture B\n")
    ctx.write(r / "corpus/SOURCES.md",
              HDR + row("S902", "capture A at corpus/evidence/round41/w6a/test_outputs.py", db) + "\n")
    commit(ctx, r)
    return ["--lane", str(r)]


def w7(ctx, d):
    r = ctx.init(d / "repo")
    cap(ctx, r, "round41/w7", b"w7 capture\n")
    bogus = dig(b"w7 made-up token\n")
    ctx.write(r / "corpus/SOURCES.md",
              HDR + row("S903", "capture at corpus/evidence/round41/w7/test_outputs.py", bogus) + "\n")
    commit(ctx, r)
    return ["--lane", str(r)]


def w9(ctx, d):
    r = ctx.init(d / "repo")
    h = cap(ctx, r, "round41/w9", b"w9 capture\n")
    cells = row("S909", "capture at corpus/evidence/round41/w9/test_outputs.py", h).split("|")
    ctx.write(r / "corpus/SOURCES.md", HDR + "|".join(cells[:-2]) + "|\n")
    commit(ctx, r)
    return ["--lane", str(r)]


def w12(ctx, d):
    r = ctx.init(d / "repo")
    h = cap(ctx, r, "round41/w12", b"w12 capture\n", toml='name = "plain-slug"\n')
    url = f"https://raw.githubusercontent.com/o/r/{PIN}/plain-slug/tests/test_outputs.py"
    ctx.write(r / "corpus/SOURCES.md", HDR + row("S905", f"pinned at {url}", h) + "\n")
    commit(ctx, r)
    return ["--lane", str(r)]


def w13(ctx, d):
    r = ctx.init(d / "repo")
    base = r / "corpus/evidence/round41/w13"
    d1 = dig(b"w13 committed view\n")
    ctx.write(base / "test_outputs.py", b"w13 committed view\n")
    ctx.write(base / "SHA256SUMS", f"{d1}  test_outputs.py\n")
    ctx.write(r / "corpus/SOURCES.md",
              HDR + row("S906", "capture at corpus/evidence/round41/w13/test_outputs.py", d1) + "\n")
    commit(ctx, r)
    d2 = dig(b"w13 staged view\n")
    ctx.write(base / "test_outputs.py", b"w13 staged view\n")
    ctx.write(base / "SHA256SUMS", f"{d2}  test_outputs.py\n")
    ctx.git(r, "add", "-A")
    ctx.write(r / "corpus/SOURCES.md",
              HDR + row("S906", "capture at corpus/evidence/round41/w13/test_outputs.py", d2) + "\n")
    return ["--lane", str(r)]


def w14(ctx, d):
    r = ctx.init(d / "repo")
    h = cap(ctx, r, "round41/w14", b"w14 capture\n")
    upper = dig(b"w14 bogus uppercase\n").upper()
    ctx.write(r / "corpus/lessons/round-37.md",
              f"Erratum (round 37): S907 anchor sha256 {upper} is committed nowhere; the capture's digest is "
              f"sha256 {h} (corpus/evidence/round41/w14/SHA256SUMS).\n")
    ctx.write(r / "corpus/SOURCES.md",
              HDR + row("S907", "capture at corpus/evidence/round41/w14/test_outputs.py", h) + "\n")
    commit(ctx, r)
    return ["--lane", str(r)]


def w15(ctx, d):
    r = ctx.init(d / "repo")
    cap(ctx, r, "round41/w15a", b"w15 capture A\n")
    db = cap(ctx, r, "round41/w15b", b"w15 capture B (sibling row's capture)\n")
    w = dig(b"w15 made-up wrong token\n")
    ctx.write(r / "corpus/lessons/round-37.md",
              f"Erratum (round 37): S908 anchor sha256 {w} was wrong; the capture's digest is sha256 {db} "
              f"(corpus/evidence/round41/w15b/SHA256SUMS).\n")
    ctx.write(r / "corpus/SOURCES.md",
              HDR + row("S908", "capture A at corpus/evidence/round41/w15a/test_outputs.py", w) + "\n")
    commit(ctx, r)
    return ["--lane", str(r)]


FIXTURES = [
    {"fid": "w-x1-provrow-only", "tool": "anchor", "expect": "accept", "defects": [], "build": w1},
    {"fid": "w-x3-provurl-fallback", "tool": "anchor", "expect": "accept", "defects": [], "build": w3},
    {"fid": "w-x6-wrong-capture", "tool": "anchor", "expect": "reject", "defects": ["digest-wrong-capture"],
     "build": w6},
    {"fid": "w-x7-unknown", "tool": "anchor", "expect": "reject", "defects": ["digest-unknown"], "build": w7},
    {"fid": "w-x9-short-row", "tool": "anchor", "expect": "reject", "defects": ["row-malformed"], "build": w9},
    {"fid": "w-x12-slashless-slug", "tool": "anchor", "expect": "accept", "defects": [], "build": w12},
    {"fid": "w-x13-staged-index", "tool": "anchor", "expect": "reject", "defects": ["digest-unknown"], "build": w13},
    {"fid": "w-x14-erratum-upper", "tool": "anchor", "expect": "reject", "defects": ["erratum-digest-unresolved"],
     "build": w14},
    {"fid": "w-x15-erratum-sibling", "tool": "anchor", "expect": "reject",
     "defects": ["digest-unknown", "erratum-incomplete"], "build": w15},
]

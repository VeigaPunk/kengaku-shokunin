"""R42CritC1Counter attack battery (anchor side).

Nine one-repo fixtures written for this seat. Seven are ordinary demonstrations of the advertised
route; two are deliberately weak substitutes the counter cannot tell apart from a demonstration
(see the seat report for the two substitutions: X13 rides a staged locator table, not an
unpromoted capture). Every repo is built from nothing with ctx only.
"""
import hashlib

PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
HDR = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
       "|----|--------|------|------|-------|--------|---------|--------|--------|---------|----------|\n")


def dh(b):
    if isinstance(b, str):
        b = b.encode()
    return hashlib.sha256(b).hexdigest()


def row(sid, source, tok):
    return (f"| {sid} | {source} | code | A | fixture | sha256 {tok} | note | mined | "
            "2026-10-26 | 180d | corpus/knowledge/x.md |")


def cap(ctx, r, sub, body, name="file.txt", sums=True):
    ctx.write(r / "corpus/evidence" / sub / name, body)
    if sums:
        ctx.write(r / "corpus/evidence" / sub / "SHA256SUMS", f"{dh(body)}  {name}\n")
    return dh(body)


def cm(ctx, r):
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "fixture")


def f_x1(ctx, d):
    r = ctx.init(d / "repo")
    h = cap(ctx, r, "r1", b"alpha body\n")
    ctx.write(r / "corpus/evidence/r1/PROVENANCE.md",
              "| sid | file | note |\n|---|---|---|\n| S901 | `file.txt` | table line |\n")
    ctx.write(r / "corpus/SOURCES.md",
              HDR + row("S901", "recorded beside the table, no locator", h) + "\n")
    cm(ctx, r)
    return ["--lane", str(r)]


def f_x3(ctx, d):
    r = ctx.init(d / "repo")
    h = cap(ctx, r, "r3", b"beta body\n")
    url = "https://raw.githubusercontent.com/o/r/" + PIN + "/plainx/tests/file.txt"
    ctx.write(r / "corpus/evidence/r3/PROVENANCE.md",
              "| url | file |\n|---|---|\n| " + url + " | `file.txt` | upstream |\n")
    ctx.write(r / "corpus/SOURCES.md", HDR + row("S903", "pinned at " + url, h) + "\n")
    cm(ctx, r)
    return ["--lane", str(r)]


def f_x6(ctx, d):
    r = ctx.init(d / "repo")
    cap(ctx, r, "r6a", b"gamma A\n")
    hb = cap(ctx, r, "r6b", b"gamma B\n")
    ctx.write(r / "corpus/SOURCES.md",
              HDR + row("S906", "capture at corpus/evidence/r6a/file.txt", hb) + "\n")
    cm(ctx, r)
    return ["--lane", str(r)]


def f_x7(ctx, d):
    r = ctx.init(d / "repo")
    cap(ctx, r, "r7", b"delta body\n")
    bogus = dh(b"a value committed nowhere\n")
    ctx.write(r / "corpus/SOURCES.md",
              HDR + row("S907", "capture at corpus/evidence/r7/file.txt", bogus) + "\n")
    cm(ctx, r)
    return ["--lane", str(r)]


def f_x9(ctx, d):
    r = ctx.init(d / "repo")
    h = cap(ctx, r, "r9", b"epsilon body\n")
    cells = row("S909", "capture at corpus/evidence/r9/file.txt", h).split("|")
    ctx.write(r / "corpus/SOURCES.md", HDR + "|".join(cells[:-2]) + "|\n")
    cm(ctx, r)
    return ["--lane", str(r)]


def f_x12(ctx, d):
    r = ctx.init(d / "repo")
    h = cap(ctx, r, "r12", b"zeta body\n")
    ctx.write(r / "corpus/evidence/r12/task.toml", 'name = "plain"\n')
    url = "https://raw.githubusercontent.com/o/r/" + PIN + "/plain/tests/file.txt"
    ctx.write(r / "corpus/SOURCES.md", HDR + row("S912", "pinned at " + url, h) + "\n")
    cm(ctx, r)
    return ["--lane", str(r)]


def f_x13(ctx, d):
    """SUBSTITUTE: the index-only change is a manifest entry that contradicts the committed capture
    bytes. No capture is unpromoted: file.txt and its manifest are committed at HEAD, then the
    manifest alone is staged with a made-up digest equal to the row's token."""
    r = ctx.init(d / "repo")
    body = b"eta body\n"
    base = r / "corpus/evidence/r13"
    ctx.write(base / "file.txt", body)
    ctx.write(base / "SHA256SUMS", f"{dh(body)}  file.txt\n")
    made = dh(b"a value committed nowhere\n")
    ctx.write(r / "corpus/SOURCES.md",
              HDR + row("S913", "capture at corpus/evidence/r13/file.txt", made) + "\n")
    cm(ctx, r)
    ctx.write(base / "SHA256SUMS", f"{made}  file.txt\n")
    ctx.git(r, "add", "corpus/evidence/r13/SHA256SUMS")
    return ["--lane", str(r)]


def f_x14(ctx, d):
    r = ctx.init(d / "repo")
    h = cap(ctx, r, "r14", b"theta body\n")
    u = dh(b"a value committed nowhere upper\n").upper()
    ctx.write(r / "corpus/lessons/round-37.md",
              f"Erratum (round 37): S914 anchor sha256 {u} sits nowhere; the digest is sha256 {h}.\n")
    ctx.write(r / "corpus/SOURCES.md",
              HDR + row("S914", "capture at corpus/evidence/r14/file.txt", h) + "\n")
    cm(ctx, r)
    return ["--lane", str(r)]


def f_x15(ctx, d):
    r = ctx.init(d / "repo")
    cap(ctx, r, "r15a", b"iota A\n")
    hb = cap(ctx, r, "r15b", b"iota B sibling\n")
    w = dh(b"a value committed nowhere wrong\n")
    ctx.write(r / "corpus/lessons/round-37.md",
              f"Erratum (round 37): S915 anchor sha256 {w} was wrong; the digest is sha256 {hb}.\n")
    ctx.write(r / "corpus/SOURCES.md",
              HDR + row("S915", "capture at corpus/evidence/r15a/file.txt", w) + "\n")
    cm(ctx, r)
    return ["--lane", str(r)]


FIXTURES = [
    {"fid": "b-x1-provenance-only", "tool": "anchor", "expect": "accept", "defects": [], "build": f_x1},
    {"fid": "b-x3-provenance-url", "tool": "anchor", "expect": "accept", "defects": [], "build": f_x3},
    {"fid": "b-x6-sibling-digest", "tool": "anchor", "expect": "reject",
     "defects": ["digest-wrong-capture"], "build": f_x6},
    {"fid": "b-x7-made-up-digest", "tool": "anchor", "expect": "reject",
     "defects": ["digest-unknown"], "build": f_x7},
    {"fid": "b-x9-ten-cells", "tool": "anchor", "expect": "reject",
     "defects": ["row-malformed"], "build": f_x9},
    {"fid": "b-x12-slashless-name", "tool": "anchor", "expect": "accept", "defects": [], "build": f_x12},
    {"fid": "b-x13-staged-manifest", "tool": "anchor", "expect": "reject",
     "defects": ["digest-unknown"], "build": f_x13},
    {"fid": "b-x14-erratum-upper", "tool": "anchor", "expect": "reject",
     "defects": ["erratum-digest-unresolved"], "build": f_x14},
    {"fid": "b-x15-erratum-sibling", "tool": "anchor", "expect": "reject",
     "defects": ["digest-unknown", "erratum-incomplete"], "build": f_x15},
]

"""battery43 / a_row: over-long registry rows, the side of `row-malformed` that battery42 never built.

`anchor_digest_check.py:34-35` advertises "A row that matches the census regex but does not have 11 cells is a
`row-malformed` defect"; the check at `:477` is `len(r["cells"]) != NCELLS`. Every fixture here is a committed git
repo built from nothing: `corpus/SOURCES.md` on HEAD, captures under `corpus/evidence/`. The UNMODIFIED tool must
report exactly `row-malformed` (exit 1) on each; the `!=` -> `<` near-variant (NA1) lets over-long rows through, so
each fixture is a silent acceptance under the mutation.

Three shapes, none sharing its construction with the freeze probe module: a duplicate trailing cell closing a
four-row registry (12 cells), two duplicated mid-table fields in an eight-row registry (13 cells), and a row pasted
from a wider table with nine extra cells that already carries a *correct* anchor (20 cells, accepted outright).
"""

import hashlib

HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|---|---|---|---|---|---|---|---|---|---|---|\n")


def digest(body):
    return hashlib.sha256(body).hexdigest()


def row(cells):
    return "| " + " | ".join(cells) + " |\n"


def green(sid, rel, body, teaches):
    """One 11-cell registry row: explicit lane path for its capture, anchor equal to that capture's digest."""
    return row([sid, f"captured at {rel}", "capture", "A", "registry", f"sha256 {digest(body)}",
                teaches, "mined", "2026-10-26", "180d", "-"])


def commit(ctx, repo, note):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", note)


def a_row_na1_tail12(ctx, d):
    """A duplicate used-by cell at the END of a four-row registry (12 cells): reference refuses, NA1 accepts."""
    r = ctx.init(d / "repo")
    caps = [("corpus/evidence/a-row/reg/a.txt", b"first registry capture\n"),
            ("corpus/evidence/a-row/reg/b.txt", b"second registry capture\n"),
            ("corpus/evidence/a-row/reg/c.txt", b"third registry capture\n")]
    text = HEADER
    for n, (rel, body) in enumerate(caps, 1):
        ctx.write(r / rel, body)
        text += green(f"S43{n}", rel, body, f"registry member {n}")
    text += row(["S436", "captured at corpus/evidence/a-row/reg/a.txt", "capture", "A", "registry", "",
                 "row pasted with a duplicated used-by cell", "mined", "2026-10-26", "180d", "-", "-"])
    ctx.write(r / "corpus/SOURCES.md", text)
    commit(ctx, r, "registry whose last row carries one cell too many")
    return ["--lane", str(r)]


def a_row_na1_mid13(ctx, d):
    """Two duplicated mid-table fields in an eight-row registry (13 cells): the over-long row is not last."""
    r = ctx.init(d / "repo")
    text = HEADER
    for n in range(1, 5):
        rel, body = f"corpus/evidence/a-row/mid/m{n}.txt", f"mid-registry capture {n}\n".encode()
        ctx.write(r / rel, body)
        text += green(f"S44{n}", rel, body, f"mid registry member {n}")
    text += row(["S449", "captured at corpus/evidence/a-row/mid/m2.txt", "capture", "A", "A", "registry",
                 "", "row with a repeated tier and status", "mined", "mined", "2026-10-26", "180d", "-"])
    for n in range(5, 8):
        rel, body = f"corpus/evidence/a-row/mid/m{n}.txt", f"mid-registry capture {n}\n".encode()
        ctx.write(r / rel, body)
        text += green(f"S45{n}", rel, body, f"mid registry member {n}")
    ctx.write(r / "corpus/SOURCES.md", text)
    commit(ctx, r, "eight-row registry with one over-long row in the middle")
    return ["--lane", str(r)]


def a_row_na1_wide20(ctx, d):
    """A row pasted from a wider table (20 cells) whose anchor is CORRECT: refused while malformed, accepted after."""
    r = ctx.init(d / "repo")
    rel, body = "corpus/evidence/a-row/wide/w.txt", b"capture a wider table row anchors\n"
    ctx.write(r / rel, body)
    wide = ["S461", f"captured at {rel}", "capture", "A", "registry", f"sha256 {digest(body)}",
            "wide row with a correct anchor", "mined", "2026-10-26", "180d", "-"]
    wide += [f"extra-{n}" for n in range(1, 10)]
    ctx.write(r / "corpus/SOURCES.md", HEADER + row(wide))
    commit(ctx, r, "one row pasted from a twenty-column table")
    return ["--lane", str(r)]


FIXTURES = [
    {"fid": "a_row-na1-tail12", "tool": "anchor", "expect": "reject",
     "defects": ["row-malformed"], "build": a_row_na1_tail12},
    {"fid": "a_row-na1-mid13", "tool": "anchor", "expect": "reject",
     "defects": ["row-malformed"], "build": a_row_na1_mid13},
    {"fid": "a_row-na1-wide20", "tool": "anchor", "expect": "reject",
     "defects": ["row-malformed"], "build": a_row_na1_wide20},
]

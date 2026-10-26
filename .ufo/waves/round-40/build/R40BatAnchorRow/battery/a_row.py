"""battery40 a_row — row-shape fixtures for plans/anchor_digest_check.py (fid prefix `a_row-`).

Each fixture clones the lane HEAD into `<fixture>/lane`, rewrites the S111 row of
`corpus/SOURCES.md` in that clone's working tree (the tool parses rows from the working tree and
binds digests against committed evidence, so the edit needs no commit), and hands that clone to
the tool as `--lane`. One row-shape behaviour per fixture; `defects` is the exact class set the
unmodified tool prints on it.
"""
import re

ROW = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
TOKEN = re.compile(r"sha256[ \t]+`?([0-9a-f]{64})")
SOURCES = "corpus/SOURCES.md"


def _row_at(lines, sid):
    for i, line in enumerate(lines):
        m = ROW.match(line)
        if m and m.group(1) == sid:
            return i
    raise ValueError(f"row {sid} not found")


def _prepare(ctx, d):
    repo = ctx.clone(d / "lane")
    p = repo / SOURCES
    return repo, p, p.read_text().split("\n")


def _finish(repo, p, lines):
    p.write_text("\n".join(lines))
    return ["--lane", str(repo)]


def build_indent4_wrong(ctx, d):
    """A 4-space-indented copy of S111 carrying another row's real digest: not a row."""
    repo, p, lines = _prepare(ctx, d)
    i = _row_at(lines, "S111")
    j = _row_at(lines, "S108")
    other = TOKEN.search(lines[j]).group(1)
    line = lines[i]
    m = TOKEN.search(line)
    lines[i] = "    " + line[:m.start()] + "sha256 " + other + line[m.end():]
    return _finish(repo, p, lines)


def build_token_in_teaches(ctx, d):
    """S111's digest claim moved into the teaches cell: present, but outside the anchor cell."""
    repo, p, lines = _prepare(ctx, d)
    i = _row_at(lines, "S111")
    parts = lines[i].split("|")
    tok = re.search(r"sha256 [0-9a-f]{64}", parts[6]).group(0)
    parts[6] = parts[6].replace("; " + tok, "").replace(tok, "")
    parts[7] = parts[7].rstrip() + " " + tok + " "
    lines[i] = "|".join(parts)
    return _finish(repo, p, lines)


def build_cells12(ctx, d):
    """S111 with a twelfth cell appended: still census-shaped, no longer an 11-cell row."""
    repo, p, lines = _prepare(ctx, d)
    i = _row_at(lines, "S111")
    lines[i] = lines[i].rstrip().rstrip("|") + "| extra |"
    return _finish(repo, p, lines)


FIXTURES = [
    {"fid": "a_row-indent4-wrong", "tool": "anchor", "expect": "accept", "defects": [],
     "build": build_indent4_wrong},
    {"fid": "a_row-token-in-teaches", "tool": "anchor", "expect": "reject",
     "defects": ["token-outside-anchor"], "build": build_token_in_teaches},
    {"fid": "a_row-12-cells", "tool": "anchor", "expect": "reject",
     "defects": ["row-malformed"], "build": build_cells12},
]

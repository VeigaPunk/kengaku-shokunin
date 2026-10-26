"""Battery38 module p6m — boundary fixtures for the frozen P6 mutants N09 and N10.

Both fixtures start from the genuine round-35 package (``ctx.genuine_package``), inject exactly ONE defect into
one registry row of ``corpus/SOURCES.md``, stage the tree index-only (``ctx.git_add``) and run
``package --root DIR --require-clean-tree``. P6 (``gate.c_sources``) is the only clause that reads the registry,
so each fixture declares that single clause id.

  p6m-n09-teaches-one-below-min  a teaches cell with exactly ``min_teaches_words - 1`` words. The frozen gate
                                 rejects it (``len(cells[6].split()) < rules["min_teaches_words"]``); N09 lowers
                                 the threshold by one, so the same cell passes — the off-by-one is the only way
                                 the two runs differ (no other fixture in the battery sits at this boundary).
  p6m-n10-url-scheme-http        the row's pinned raw URL with its scheme swapped ``https://`` -> ``http://``.
                                 The frozen gate compares the URL text against ``raw_base + upstream``, so the
                                 scheme is load-bearing; N10 compares both sides with the scheme stripped, so the
                                 same cell passes.

Cells are edited by index (never by a whole-line substring), the teach-cell length and the single occurrence of
the pinned URL are asserted inside the builder, and the sheet is rewritten in place.
"""

import re

SOURCE_ROW = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
SOURCES = "corpus/SOURCES.md"
TEACHES_IDX = 6
URL_IDX = 1
# Distinct, in-cell words used to reach an exact teaches-word count; the ids keep the cell unique across rows.
TEACHES_WORDS = ("n09", "teaches", "boundary", "off", "by", "one", "floor", "probe", "cell", "counter",
                 "gate", "word")


def _mutate(d, sid, fn):
    """Rewrite the one registry row `sid` with fn(cells); exactly one such row must exist."""
    path = d / SOURCES
    out, hit = [], 0
    for line in path.read_text().splitlines():
        m = SOURCE_ROW.match(line)
        if m and m.group(1) == sid:
            indent = line[: len(line) - len(line.lstrip())]
            line = indent + "|" + "|".join(fn(line.strip().strip("|").split("|"))) + "|"
            hit += 1
        out.append(line)
    if hit != 1:
        raise RuntimeError(f"{SOURCES}: expected one {sid} row, edited {hit}")
    path.write_text("\n".join(out) + "\n")


def _cells(d, sid):
    for line in (d / SOURCES).read_text().splitlines():
        m = SOURCE_ROW.match(line)
        if m and m.group(1) == sid:
            return [c.strip() for c in line.strip().strip("|").split("|")]
    raise RuntimeError(f"{SOURCES}: no {sid} row")


def _target_row(ctx):
    """The first registry row of the frozen spec (S105 in the round-35 spec), never a re-invented id."""
    rows = sorted(ctx.spec["rows"])
    if not rows:
        raise RuntimeError("spec carries no registry row")
    return rows[0]


def _mut_n09(d, ctx):
    """A teaches cell with exactly min_teaches_words - 1 words (the frozen gate rejects, N09 accepts)."""
    n = ctx.spec["entry_rules"]["min_teaches_words"] - 1
    if not 1 <= n < len(TEACHES_WORDS):
        raise RuntimeError(f"min_teaches_words-1={n} is outside the fixture's word list")
    cell = " ".join(TEACHES_WORDS[:n])
    if len(cell.split()) != n:
        raise RuntimeError(f"teaches cell has {len(cell.split())} words, wanted {n}")
    sid = _target_row(ctx)
    others = {c[TEACHES_IDX].lower() for s, c in
              ((s, _cells(d, s)) for s in ctx.spec["rows"] if s != sid)}
    if cell.lower() in others:
        raise RuntimeError(f"teaches cell collides with another row: {cell!r}")

    def fn(cells):
        if cells[TEACHES_IDX].split() and len(cells[TEACHES_IDX].split()) < n:
            raise RuntimeError("genuine teaches cell is already under the frozen minimum")
        cells[TEACHES_IDX] = f" {cell} "
        return cells

    _mutate(d, sid, fn)


def _mut_n10(d, ctx):
    """The pinned raw URL with its scheme swapped https -> http (the frozen gate rejects, N10 accepts)."""
    sid = _target_row(ctx)
    pinned = ctx.spec["raw_base"] + ctx.spec["rows"][sid]["upstream"]
    scheme, _, rest = pinned.partition("://")
    if scheme != "https" or not rest:
        raise RuntimeError(f"pinned url is not an https path: {pinned!r}")
    swapped = "http://" + rest

    def fn(cells):
        if cells[URL_IDX].count(pinned) != 1:
            raise RuntimeError(f"{sid} source cell carries the pinned url "
                               f"{cells[URL_IDX].count(pinned)} times, wanted exactly one")
        cells[URL_IDX] = cells[URL_IDX].replace(pinned, swapped)
        return cells

    _mutate(d, sid, fn)


def _fixture(mutator):
    def build(ctx, d):
        ctx.genuine_package(d)
        mutator(d, ctx)
        ctx.git_add(d)
        return ["package", "--root", str(d), "--require-clean-tree"]

    return build


FIXTURES = [
    {"fid": "p6m-n09-teaches-one-below-min", "expect": "reject", "defects": ["P6"],
     "build": _fixture(_mut_n09)},
    {"fid": "p6m-n10-url-scheme-http", "expect": "reject", "defects": ["P6"],
     "build": _fixture(_mut_n10)},
]

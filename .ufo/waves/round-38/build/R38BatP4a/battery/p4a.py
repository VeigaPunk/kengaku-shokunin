"""battery38 module `p4a` — P4 fixtures that kill mutants N03 and N04 of plans/round38_c1_verify.py.

Both mutants weaken the gate's `c_quote_verbatim` loop while leaving `c_quote_shape` (P3) and
`c_captures` (P5) untouched; the round-37 P4 fixtures all deface the FIRST data row of the genuine
entry's `## Located quotes` table, so neither mutant is killed by them.

  * N03 (`for q in p.quotes:` -> `for q in p.quotes[:1]:`) checks only the first quote. Fixture
    `p4a-second-row-line-outside` retargets the SECOND data row to a line past the end of its capture
    (`test_outputs.py` has 73 lines). The unmodified gate prints P4 DEFECT (`line range outside the
    capture`); N03 never reaches row 2 and prints P4 ok. Row 1 stays verbatim, so the fixture cannot
    kill any first-row mutant. P3 keeps 22 distinct (capture, start) pairs because the new line is
    cited by no other row.

  * N04 (`q.text not in "\\n".join(lines[q.start - 1:q.end])` -> `... lines`) tests the whole capture
    instead of the cited range. Fixture `p4a-text-elsewhere` retargets the FIRST data row to a line of
    its capture that does not contain the quote text, while the text stays byte-verbatim at its
    original line 13. The unmodified gate prints P4 DEFECT (`quote not verbatim there`); N04 finds the
    text anywhere in the file and prints P4 ok. Because the defaced row is the first, N03 still sees
    it and this fixture cannot kill N03.

Declared `defects` are exactly the clause set the UNMODIFIED gate prints DEFECT on each fixture,
observed before writing them into FIXTURES. Every builder starts from the genuine round-35 package
(`ctx.genuine_package`), edits only the cited line of one existing quote row through
`ctx.r36.rewrite_quotes`, stages the tree index-only (`ctx.git_add`, which P9 needs) and returns
`package --root <fixture> --require-clean-tree`. No fixture keys on a name, marker or path: the
counter's renamed run copies each tree under another directory name.
"""

OUT_OF_RANGE_MARGIN = 1000


def _data_rows(text, ctx):
    pat = ctx.r36.QUOTE_ROW
    return [line for line in text.splitlines() if pat.match(line)]


def _capture_lines(ctx, d, name):
    return (d / ctx.spec["capture_dir"] / name).read_text().splitlines()


def _retarget(row, m, line):
    """Rewrite the row's cited line(s) to `line`, keeping the rest of the row byte-identical."""
    if m.group(4):
        row = row[:m.span(4)[0]] + str(line) + row[m.span(4)[1]:]
    return row[:m.span(3)[0]] + str(line) + row[m.span(3)[1]:]


def _build(ctx, d, fn):
    ctx.genuine_package(d)
    entry = d / ctx.spec["entry"]
    entry.write_text(ctx.r36.rewrite_quotes(entry.read_text(), fn))
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


def _second_row_outside(ctx, d):
    def fn(rows):
        rows = list(rows)
        if len(rows) < 2:
            raise RuntimeError("p4a fixture: the genuine table has no second data row")
        m = ctx.r36.QUOTE_ROW.match(rows[1])
        n = max(len(_capture_lines(ctx, d, m.group(2))), int(m.group(3))) + OUT_OF_RANGE_MARGIN
        rows[1] = _retarget(rows[1], m, n)
        return rows
    return _build(ctx, d, fn)


def _text_elsewhere(ctx, d):
    def fn(rows):
        rows = list(rows)
        m = ctx.r36.QUOTE_ROW.match(rows[0])
        quote, capture = m.group(1), m.group(2)
        lines = _capture_lines(ctx, d, capture)
        if quote not in "\n".join(lines):
            raise RuntimeError("p4a fixture: the first quote is not verbatim anywhere in its capture")
        cited = set()
        for row in rows:
            mm = ctx.r36.QUOTE_ROW.match(row)
            if mm and mm.group(2) == capture:
                cited.update(range(int(mm.group(3)), int(mm.group(4) or mm.group(3)) + 1))
        pick = next((n for n in range(1, len(lines) + 1)
                     if n not in cited and quote not in lines[n - 1]), None)
        if pick is None:
            raise RuntimeError("p4a fixture: no uncited line lacks the quote text")
        rows[0] = _retarget(rows[0], m, pick)
        return rows
    return _build(ctx, d, fn)


FIXTURES = [
    {"fid": "p4a-second-row-line-outside", "expect": "reject", "defects": ["P4"],
     "build": _second_row_outside},
    {"fid": "p4a-text-elsewhere", "expect": "reject", "defects": ["P4"],
     "build": _text_elsewhere},
]

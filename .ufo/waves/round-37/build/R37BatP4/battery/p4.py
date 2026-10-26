"""battery37 module `p4` — single-defect fixtures for the P4 clause (a quote must be verbatim on its
cited line), mutants M09-M12 of plans/round37_c1_verify.py.

Every builder starts from the genuine round-35 package (`ctx.genuine_package`), rewrites only the data rows
of the genuine entry's `## Located quotes` table through `ctx.r36.rewrite_quotes`, stages the tree (index
only) and returns `package --root <fixture> --require-clean-tree`. No fixture carries a name, marker or path
that the gate could key on: the counter's renamed run copies each tree under another directory name.

Declared `defects` are exactly the clauses the UNMODIFIED gate prints `DEFECT` on the fixture:

  * p4-no-quote-row (M09, `no parsed quote`): the table keeps its header and separator but loses every data
    row. P3 fires unavoidably alongside P4 — with zero parsed quotes the shape clause can never reach
    `min_quotes=8`, and there is no other way to reach `p.quotes == []` while the section still parses
    (dropping the section is the M04 branch). Declaration P3+P4; M09 removes P4 from the set, M04 the whole
    section, so the two mutants are still distinguished by separate fixtures.
  * p4-capture-unreadable (M10, `unreadable capture`): the first quote cites a capture file that does not
    exist. P5 fires too — the same name is not pinned in the capture manifest (`quote capture ... is not
    pinned in the manifest`), a different clause and a different branch. M10 erases only the P4 member.
  * p4-line-outside (M11, `line range outside the capture`): the first quote cites line 9999 of a capture
    that has 73 lines. The capture is pinned and the row is parseable, so P3 and P5 stay ok: P4 alone.
  * p4-one-char-off (M12, `quote not verbatim there`): the first quote's text has one alphanumeric
    character replaced (same length, same word count, same location). P4 alone.
"""

MISSING_CAPTURE = "no-such-capture-37.py"
OUT_OF_RANGE_LINE = 9999


def _first_row(rows, ctx):
    """Index of the first parsable data row and its QUOTE_ROW match (the genuine table always has one)."""
    for i, row in enumerate(rows):
        m = ctx.r36.QUOTE_ROW.match(row)
        if m:
            return i, m
    raise RuntimeError("p4 fixture: the genuine entry has no parsable quote row")


def _rebuild(row, span, replacement):
    return row[:span[0]] + replacement + row[span[1]:]


def _apply(ctx, d, fn):
    ctx.genuine_package(d)
    entry = d / ctx.spec["entry"]
    entry.write_text(ctx.r36.rewrite_quotes(entry.read_text(), fn))
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


def _no_quote_row(ctx, d):
    return _apply(ctx, d, lambda rows: [])


def _capture_unreadable(ctx, d):
    def fn(rows):
        rows = list(rows)
        i, m = _first_row(rows, ctx)
        rows[i] = _rebuild(rows[i], m.span(2), MISSING_CAPTURE)
        return rows
    return _apply(ctx, d, fn)


def _line_outside(ctx, d):
    def fn(rows):
        rows = list(rows)
        i, m = _first_row(rows, ctx)
        rows[i] = _rebuild(rows[i], m.span(3), str(OUT_OF_RANGE_LINE))
        return rows
    return _apply(ctx, d, fn)


def _one_char_off(ctx, d):
    def fn(rows):
        rows = list(rows)
        i, m = _first_row(rows, ctx)
        text = m.group(1)
        for j in range(len(text) - 1, -1, -1):
            ch = text[j]
            if ch.isalnum():
                rows[i] = _rebuild(rows[i], (m.start(1), m.end(1)),
                                   text[:j] + ("z" if ch != "z" else "q") + text[j + 1:])
                break
        else:
            raise RuntimeError("p4 fixture: the first quote has no alphanumeric character")
        return rows
    return _apply(ctx, d, fn)


FIXTURES = [
    {"fid": "p4-no-quote-row", "expect": "reject", "defects": ["P3", "P4"], "build": _no_quote_row},
    {"fid": "p4-capture-unreadable", "expect": "reject", "defects": ["P4", "P5"], "build": _capture_unreadable},
    {"fid": "p4-line-outside", "expect": "reject", "defects": ["P4"], "build": _line_outside},
    {"fid": "p4-one-char-off", "expect": "reject", "defects": ["P4"], "build": _one_char_off},
]

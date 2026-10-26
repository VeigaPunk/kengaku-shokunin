"""battery38 module `p4b` — two single-defect fixtures for the P4 clause (a quote must be verbatim, in the
same case, on the lines it cites, and its cited range must lie inside the capture).

Each builder starts from the genuine round-35 package (`ctx.genuine_package`), rewrites only the data rows of
the genuine entry's `## Located quotes` table through `ctx.r36.rewrite_quotes`, stages the tree (index only)
and returns `package --root <fixture> --require-clean-tree`. No fixture carries a name, marker or path the
gate could key on: the counter's renamed run copies each tree under another directory name.

Declared `defects` are exactly the clauses the UNMODIFIED gate prints `DEFECT` on the fixture:

  * p4b-case-only (N05, `quote not verbatim there`): one quote's text has a single ASCII letter's case flipped
    (`gblock_path` -> `Gblock_path`). The row still parses, the word count and the distinct text/location
    counts are unchanged, so P3 stays ok; the cite is inside the capture and the capture is pinned, so P4
    alone. A gate that lower-cases both sides finds the quote and prints P4 ok.
  * p4b-range-end-past-last (N06, `line range outside the capture`): one quote cites
    `instruction.md:<N>-<N+1>` where N is the capture's last line, and its text is that last line verbatim.
    `q.end > len(lines)` is true by exactly one; the text itself is present on line N, so a gate that lets the
    end run one past the last line finds the quote and prints P4 ok. P3 alone sees an in-range word count and
    an extra distinct location, so P4 is the only defect.
"""

CAPTURE = "instruction.md"


def _first_row(ctx, rows):
    """(index, QUOTE_ROW match) of the first parsable data row (the genuine table always has one)."""
    for i, row in enumerate(rows):
        m = ctx.r36.QUOTE_ROW.match(row)
        if m:
            return i, m
    raise RuntimeError("p4b fixture: the genuine entry has no parsable quote row")


def _apply(ctx, d, fn):
    ctx.genuine_package(d)
    entry = d / ctx.spec["entry"]
    entry.write_text(ctx.r36.rewrite_quotes(entry.read_text(), fn))
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


def _case_only(ctx, d):
    def fn(rows):
        rows = list(rows)
        i, m = _first_row(ctx, rows)
        text = m.group(1)
        for j, ch in enumerate(text):
            if ch.isascii() and ch.isalpha():
                flipped = text[:j] + (ch.lower() if ch.isupper() else ch.upper()) + text[j + 1:]
                rows[i] = rows[i][:m.start(1)] + flipped + rows[i][m.end(1):]
                return rows
        raise RuntimeError("p4b fixture: the first quote has no ASCII letter")
    return _apply(ctx, d, fn)


def _range_end_past_last(ctx, d):
    def fn(rows):
        rows = list(rows)
        i, _m = _first_row(ctx, rows)
        lines = (d / ctx.spec["capture_dir"] / CAPTURE).read_text().splitlines()
        n = len(lines)
        text = lines[-1].strip()
        if not 3 <= len(text.split()) <= 25 or "”" in text or "|" in text:
            raise RuntimeError(f"p4b fixture: last line of {CAPTURE} is not a quotable claim: {text!r}")
        claim = rows[i].split("|")[1].strip()
        rows[i] = f"| {claim} | “{text}” | `{CAPTURE}:{n}-{n + 1}` |"
        return rows
    return _apply(ctx, d, fn)


FIXTURES = [
    {"fid": "p4b-case-only", "expect": "reject", "defects": ["P4"], "build": _case_only},
    {"fid": "p4b-range-end-past-last", "expect": "reject", "defects": ["P4"], "build": _range_end_past_last},
]

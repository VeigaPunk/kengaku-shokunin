"""Round-37 battery module p23: single-defect fixtures for the P2 (receipt) and P3 (quote shape) branches
of `plans/pkg_gate.py`, one fixture per frozen mutant M02, M03, M04, M06, M07, M08.

Every fixture starts from the genuine round-35 package (`ctx.genuine_package`), changes exactly one thing,
stages it index-only, and runs `package --root d --require-clean-tree` (P10 is not asked to run: the probe
re-run is a different clause and would blur the single defect).

  p23-p2-receipt-deleted   M02  receipt file gone (staged deletion)      -> P2
  p23-p2-receipt-byte      M03  one receipt byte changed                 -> P2
  p23-p3-heading-renamed   M04  '## Located quotes' heading renamed      -> P3, P4
  p23-p3-seven-texts       M06  seven distinct quote texts on eight
                                distinct located lines                   -> P3
  p23-p3-seven-locations   M07  eight distinct quote texts on seven
                                distinct located lines                   -> P3
  p23-p3-two-word-quote    M08  one genuine quote cut to two words       -> P3

`p23-p3-heading-renamed` unavoidably prints a second clause: renaming the heading removes the quote
section, so `Package._parse_quotes` returns early and P4 sees `not p.quotes` ("no parsed quote"). There is
no way to silence the P3 "no section" branch while a quote is parsed, because parsing is keyed on that exact
heading; the declared set is therefore {P3, P4}.
"""


def _package_argv(d):
    return ["package", "--root", str(d), "--require-clean-tree"]


def _receipt_deleted(ctx, d):
    """M02: the pinned receipt is absent, its deletion staged so P9 stays clean."""
    ctx.genuine_package(d)
    (d / ctx.spec["receipt"]).unlink()
    ctx.git_add(d)
    return _package_argv(d)


def _receipt_byte(ctx, d):
    """M03: the receipt is readable but one byte differs from the spec pin."""
    ctx.genuine_package(d)
    receipt = d / ctx.spec["receipt"]
    data = bytearray(receipt.read_bytes())
    data[0] = ord("Y") if data[0] != ord("Y") else ord("Z")
    receipt.write_bytes(bytes(data))
    ctx.git_add(d)
    return _package_argv(d)


def _heading_renamed(ctx, d):
    """M04: the quote section heading is renamed, so no section is found."""
    ctx.genuine_package(d)
    entry = d / ctx.spec["entry"]
    text = entry.read_text()
    if text.count("## Located quotes") != 1:
        raise RuntimeError("genuine entry does not carry exactly one '## Located quotes' heading")
    entry.write_text(text.replace("## Located quotes", "## Quotes, located", 1))
    ctx.git_add(d)
    return _package_argv(d)


def _quote_rows(ctx, d, fn):
    entry = d / ctx.spec["entry"]
    entry.write_text(ctx.r36.rewrite_quotes(entry.read_text(), fn))


def _retarget(row, old, new):
    if old not in row:
        raise RuntimeError(f"row does not cite {old}: {row!r}")
    return row.replace(old, new)


def _seven_texts(ctx, d):
    """M06: 8 data rows carrying only 7 distinct texts, on 8 distinct located lines.

    The genuine `assert 15 <= gc <= 35, (` row cites test_outputs.py:71; the same text is verbatim on
    test_outputs.py:66, so a copy of that row re-cited at :66 keeps P4 green while `len(texts)` stays 7.
    """
    ctx.genuine_package(d)

    def fn(rows):
        gc71 = rows[14]
        if "test_outputs.py:71" not in gc71:
            raise RuntimeError(f"genuine row 14 is not the gc row at :71: {gc71!r}")
        return rows[:6] + [_retarget(gc71, "test_outputs.py:71", "test_outputs.py:66"), gc71]

    _quote_rows(ctx, d, fn)
    ctx.git_add(d)
    return _package_argv(d)


def _seven_locations(ctx, d):
    """M07: 8 data rows with 8 distinct texts but only 7 distinct (capture, line) locations.

    Two different texts are both verbatim on test_outputs.py:23 — the whole genuine line and its first
    five words — so the table keeps P4 green and `len(locs)` stays 7.
    """
    ctx.genuine_package(d)

    def fn(rows):
        line23 = rows[4]
        m = ctx.r36.QUOTE_ROW.match(line23)
        if not m or "test_outputs.py:23" not in line23:
            raise RuntimeError(f"genuine row 4 is not the :23 row: {line23!r}")
        prefix = " ".join(m.group(1).split()[:5])
        return rows[:7] + [line23.replace(f"“{m.group(1)}”", f"“{prefix}”")]

    _quote_rows(ctx, d, fn)
    ctx.git_add(d)
    return _package_argv(d)


def _two_word_quote(ctx, d):
    """M08: one genuine quote is cut to two words (below the spec's 3-word floor), still verbatim."""
    ctx.genuine_package(d)

    def fn(rows):
        row = rows[6]
        m = ctx.r36.QUOTE_ROW.match(row)
        if not m or "test_outputs.py:27" not in row:
            raise RuntimeError(f"genuine row 6 is not the :27 row: {row!r}")
        short = " ".join(m.group(1).split()[:2])
        return rows[:6] + [row.replace(f"“{m.group(1)}”", f"“{short}”")] + rows[7:]

    _quote_rows(ctx, d, fn)
    ctx.git_add(d)
    return _package_argv(d)


FIXTURES = [
    {"fid": "p23-p2-receipt-deleted", "expect": "reject", "defects": ["P2"], "build": _receipt_deleted},
    {"fid": "p23-p2-receipt-byte", "expect": "reject", "defects": ["P2"], "build": _receipt_byte},
    {"fid": "p23-p3-heading-renamed", "expect": "reject", "defects": ["P3", "P4"], "build": _heading_renamed},
    {"fid": "p23-p3-seven-texts", "expect": "reject", "defects": ["P3"], "build": _seven_texts},
    {"fid": "p23-p3-seven-locations", "expect": "reject", "defects": ["P3"], "build": _seven_locations},
    {"fid": "p23-p3-two-word-quote", "expect": "reject", "defects": ["P3"], "build": _two_word_quote},
]

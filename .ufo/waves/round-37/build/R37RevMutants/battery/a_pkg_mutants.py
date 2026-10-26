"""R37RevMutants review battery: single-edit package fixtures, one per gate branch (M02-M39).

Each fixture: genuine round-35 package + ONE edit; `defects` is the exact DEFECT set the
unmodified gate must print (verified by the counter's battery check).
"""
import hashlib
import pathlib
import re
import shutil

def _argv(d):
    return ["package", "--root", str(d), "--require-clean-tree"]


def _pkg(ctx, d, git=True):
    ctx.genuine_package(d)
    if git:
        ctx.git_add(d)


def _entry(ctx, d):
    return d / ctx.spec["entry"]


def _cap(ctx, d):
    return d / ctx.spec["capture_dir"]


def _edit_line(ctx, d, prefix, fn):
    """Rewrite the SOURCES row whose stripped text starts with prefix (e.g. '| S105')."""
    p = d / ctx.spec["sources"]
    out = []
    for l in p.read_text().splitlines():
        if l.strip().startswith(prefix):
            cells = l.strip().strip("|").split("|")
            line = fn(cells)
            l = "|" + "|".join(cells) + "|" if line is None else line
        out.append(l)
    p.write_text("\n".join(out) + "\n")


# ---- P2 receipt ---------------------------------------------------------------------

def _m02(ctx, d):
    _pkg(ctx, d)
    (d / ctx.spec["receipt"]).unlink()
    return _argv(d)


def _m03(ctx, d):
    _pkg(ctx, d)
    r = d / ctx.spec["receipt"]
    r.write_bytes(r.read_bytes() + b"x")
    return _argv(d)


# ---- P3 quote shape -----------------------------------------------------------------

def _m04(ctx, d):
    _pkg(ctx, d)
    e = _entry(ctx, d)
    e.write_text(e.read_text().replace("## Located quotes\n", "## Renamed quotes\n", 1))
    return _argv(d)


def _m06(ctx, d):
    _pkg(ctx, d)
    e = _entry(ctx, d)

    def fn(rows):
        t = ctx.r36.QUOTE_ROW.match(rows[0]).group(1)
        return [l.replace(f"“{ctx.r36.QUOTE_ROW.match(l).group(1)}”", f"“{t}”") for l in rows]

    e.write_text(ctx.r36.rewrite_quotes(e.read_text(), fn))
    return _argv(d)


def _m07(ctx, d):
    _pkg(ctx, d)
    e = _entry(ctx, d)

    def fn(rows):
        m0 = ctx.r36.QUOTE_ROW.match(rows[0])
        out = []
        for i, l in enumerate(rows):
            m = ctx.r36.QUOTE_ROW.match(l)
            claim = l.split("|")[1].strip()
            if i >= 7:
                out.append(f"| {claim} | “{m.group(1)}” | `{m0.group(2)}:{m0.group(3)}` |")
            else:
                out.append(l)
        return out

    e.write_text(ctx.r36.rewrite_quotes(e.read_text(), fn))
    return _argv(d)


def _m08(ctx, d):
    _pkg(ctx, d)
    e = _entry(ctx, d)

    def fn(rows):
        l = rows[0]
        m = ctx.r36.QUOTE_ROW.match(l)
        words = m.group(1).split()
        return [l.replace(f"“{m.group(1)}”", f"“{' '.join(words[:2])}”")] + rows[1:]

    e.write_text(ctx.r36.rewrite_quotes(e.read_text(), fn))
    return _argv(d)


def _m09(ctx, d):
    _pkg(ctx, d)
    e = _entry(ctx, d)
    e.write_text(ctx.r36.rewrite_quotes(e.read_text(), lambda rows: []))
    return _argv(d)


# ---- P4 verbatim --------------------------------------------------------------------

def _m11(ctx, d):
    _pkg(ctx, d)
    e = _entry(ctx, d)
    e.write_text(e.read_text().replace("`test_outputs.py:13`", "`test_outputs.py:9999`", 1))
    return _argv(d)


def _m12(ctx, d):
    _pkg(ctx, d)
    e = _entry(ctx, d)

    def fn(rows):
        l = rows[0]
        m = ctx.r36.QUOTE_ROW.match(l)
        return [l.replace(f"“{m.group(1)}”", "“wholly unrelated text about linker length”")] + rows[1:]

    e.write_text(ctx.r36.rewrite_quotes(e.read_text(), fn))
    return _argv(d)


# ---- P5 captures --------------------------------------------------------------------

def _m10(ctx, d):
    _pkg(ctx, d)
    (_cap(ctx, d) / "test_outputs.py").unlink()
    return _argv(d)


def _m13(ctx, d):
    _pkg(ctx, d)
    (_cap(ctx, d) / "SHA256SUMS").unlink()
    return _argv(d)


def _m14(ctx, d):
    _pkg(ctx, d)
    m = _cap(ctx, d) / "SHA256SUMS"
    m.write_text(m.read_text() + "zz garbage-line\n")
    return _argv(d)


def _m15(ctx, d):
    _pkg(ctx, d)
    p = _cap(ctx, d) / "test.sh"
    p.write_bytes(p.read_bytes() + b"\n")
    return _argv(d)


def _m16(ctx, d):
    _pkg(ctx, d)
    c = _cap(ctx, d)
    (c / "test.sh").unlink()
    m = c / "SHA256SUMS"
    m.write_text("".join(l + "\n" for l in m.read_text().splitlines() if l.split()[-1] != "test.sh"))
    e = _entry(ctx, d)  # drop the quote rows citing test.sh so M18 cannot mask M16
    e.write_text(ctx.r36.rewrite_quotes(e.read_text(),
                 lambda rows: [l for l in rows if "`test.sh:" not in l]))
    return _argv(d)


def _m17(ctx, d):
    _pkg(ctx, d)
    c = _cap(ctx, d)
    p = c / "test.sh"
    p.write_bytes(p.read_bytes() + b"\n")
    nd = hashlib.sha256(p.read_bytes()).hexdigest()
    m = c / "SHA256SUMS"
    m.write_text("".join((nd + "  test.sh\n") if l.split()[-1] == "test.sh" else l + "\n"
                         for l in m.read_text().splitlines()))
    return _argv(d)


def _m18(ctx, d):
    _pkg(ctx, d)
    e = _entry(ctx, d)
    e.write_text(e.read_text().replace("`test_outputs.py:13`", "`ghost.py:13`", 1))
    return _argv(d)


def _m19(ctx, d):
    _pkg(ctx, d, git=False)
    (_cap(ctx, d) / "zz-extra.txt").write_text("stray capture\n")
    ctx.git_add(d)
    return _argv(d)


# ---- P6 sources ---------------------------------------------------------------------

def _m20(ctx, d):
    _pkg(ctx, d)
    p = d / ctx.spec["sources"]
    p.write_text("".join(l + "\n" for l in p.read_text().splitlines() if not l.startswith("| S105 ")))
    return _argv(d)


def _m21(ctx, d):
    _pkg(ctx, d)
    _edit_line(ctx, d, "| S105", lambda cells: cells.append(" x ") or None)
    return _argv(d)


def _m22(ctx, d):
    _pkg(ctx, d)
    _edit_line(ctx, d, "| S105",
               lambda cells: cells.__setitem__(1, cells[1].replace("protein-assembly/tests/test_outputs.py",
                                                                   "protein-assembly/tests/renamed_outputs.py")))
    return _argv(d)


def _m23(ctx, d):
    _pkg(ctx, d)
    _edit_line(ctx, d, "| S105", lambda cells: cells.__setitem__(3, " B "))
    return _argv(d)


def _m24(ctx, d):
    _pkg(ctx, d)
    _edit_line(ctx, d, "| S105", lambda cells: cells.__setitem__(7, " draft "))
    return _argv(d)


def _m25(ctx, d):
    _pkg(ctx, d)
    _edit_line(ctx, d, "| S105",
               lambda cells: cells.__setitem__(10, cells[10].replace("tb2-protein-assembly-grader.md",
                                                                     "zz-elsewhere-entry.md")))
    return _argv(d)


def _m26(ctx, d):
    _pkg(ctx, d)
    _edit_line(ctx, d, "| S105", lambda cells: cells.__setitem__(6, " junk "))
    return _argv(d)


def _m27(ctx, d):
    _pkg(ctx, d)
    src = {}

    def fn(cells):
        src["teaches"] = cells[6]

    _edit_line(ctx, d, "| S105", fn)
    _edit_line(ctx, d, "| S106", lambda cells: cells.__setitem__(6, src["teaches"]))
    return _argv(d)


# ---- P7 provenance ------------------------------------------------------------------

def _m28(ctx, d):
    _pkg(ctx, d)
    _entry(ctx, d).unlink()
    return _argv(d)


def _m29(ctx, d):
    _pkg(ctx, d)
    e = _entry(ctx, d)
    e.write_text("".join(l + "\n" for l in e.read_text().splitlines() if not l.startswith("source: S105")))
    return _argv(d)


def _m30(ctx, d):
    _pkg(ctx, d)
    e = _entry(ctx, d)
    e.write_text(e.read_text().replace("verified-at: 2026-10-25", "verified-at: 2026-10-24", 1))
    return _argv(d)


def _m31(ctx, d):
    _pkg(ctx, d)
    e = _entry(ctx, d)
    e.write_text("".join(l + "\n" for l in e.read_text().splitlines() if not l.startswith("recheck:")))
    return _argv(d)


def _m32(ctx, d):
    _pkg(ctx, d)
    e = _entry(ctx, d)
    e.write_text(e.read_text().replace("## Negative space\n", "## Open space\n", 1))
    return _argv(d)


def _m33(ctx, d):
    _pkg(ctx, d)
    e = _entry(ctx, d)
    e.write_text(re.sub(r"(?i)falsifi", "xxxxxi", e.read_text()))
    return _argv(d)


# ---- P8 readme ----------------------------------------------------------------------

def _m34(ctx, d):
    _pkg(ctx, d)
    (d / ctx.spec["readme"]).unlink()
    return _argv(d)


def _m35(ctx, d):
    _pkg(ctx, d)
    r = d / ctx.spec["readme"]
    lines = r.read_text().splitlines()
    row = next(l for l in lines if l.startswith("| `knowledge/tb2-protein-assembly-grader.md`"))
    r.write_text("\n".join(lines) + "\n" + row + "\n")
    return _argv(d)


def _m36(ctx, d):
    _pkg(ctx, d)
    r = d / ctx.spec["readme"]
    r.write_text(r.read_text().replace("S105, S106, S107", "S105, S107", 1))
    return _argv(d)


def _m37(ctx, d):
    _pkg(ctx, d)
    r = d / ctx.spec["readme"]
    keep = [l for l in r.read_text().splitlines()
            if not (l.startswith("- ") and "tb2-protein-assembly-grader.md" in l
                    and "evidence/round35/tb2-grader-probe.txt" in l)]
    r.write_text("\n".join(keep) + "\n")
    return _argv(d)


def _m38(ctx, d):
    _pkg(ctx, d, git=False)
    (d / "corpus/knowledge/zz-rev-extra.md").write_text("# extra knowledge file\n")
    ctx.git_add(d)
    return _argv(d)


# ---- P9 clean tree ------------------------------------------------------------------

def _m39(ctx, d):
    ctx.r36.copy_package(ctx.lane, ctx.spec, d)  # no git init, no add: not a worktree
    return _argv(d)


FIXTURES = [
    {"fid": "rev-m02-receipt-gone", "expect": "reject", "defects": ["P2"], "build": _m02},
    {"fid": "rev-m03-receipt-byte", "expect": "reject", "defects": ["P2"], "build": _m03},
    {"fid": "rev-m04-quote-heading", "expect": "reject", "defects": ["P3", "P4"], "build": _m04},
    {"fid": "rev-m06-dup-texts", "expect": "reject", "defects": ["P3", "P4"], "build": _m06},
    {"fid": "rev-m07-dup-locs", "expect": "reject", "defects": ["P3", "P4"], "build": _m07},
    {"fid": "rev-m08-short-quote", "expect": "reject", "defects": ["P3"], "build": _m08},
    {"fid": "rev-m09-no-rows", "expect": "reject", "defects": ["P3", "P4"], "build": _m09},
    {"fid": "rev-m11-range-9999", "expect": "reject", "defects": ["P4"], "build": _m11},
    {"fid": "rev-m12-text-swap", "expect": "reject", "defects": ["P4"], "build": _m12},
    {"fid": "rev-m10-capture-gone", "expect": "reject", "defects": ["P4", "P5"], "build": _m10},
    {"fid": "rev-m13-manifest-gone", "expect": "reject", "defects": ["P5"], "build": _m13},
    {"fid": "rev-m14-garbage-line", "expect": "reject", "defects": ["P5"], "build": _m14},
    {"fid": "rev-m15-capture-byte", "expect": "reject", "defects": ["P5"], "build": _m15},
    {"fid": "rev-m16-row-cap-gone", "expect": "reject", "defects": ["P5"], "build": _m16},
    {"fid": "rev-m17-pin-vs-spec", "expect": "reject", "defects": ["P5"], "build": _m17},
    {"fid": "rev-m18-ghost-quote", "expect": "reject", "defects": ["P4", "P5"], "build": _m18},
    {"fid": "rev-m19-extra-capture", "expect": "reject", "defects": ["P5"], "build": _m19},
    {"fid": "rev-m20-row-missing", "expect": "reject", "defects": ["P6"], "build": _m20},
    {"fid": "rev-m21-12-cells", "expect": "reject", "defects": ["P6"], "build": _m21},
    {"fid": "rev-m22-url", "expect": "reject", "defects": ["P6"], "build": _m22},
    {"fid": "rev-m23-tier", "expect": "reject", "defects": ["P6"], "build": _m23},
    {"fid": "rev-m24-status", "expect": "reject", "defects": ["P6"], "build": _m24},
    {"fid": "rev-m25-usedby", "expect": "reject", "defects": ["P6"], "build": _m25},
    {"fid": "rev-m26-short-teaches", "expect": "reject", "defects": ["P6"], "build": _m26},
    {"fid": "rev-m27-dup-teaches", "expect": "reject", "defects": ["P6"], "build": _m27},
    {"fid": "rev-m28-entry-gone", "expect": "reject", "defects": ["P3", "P4", "P7", "P8"], "build": _m28},
    {"fid": "rev-m29-source-line", "expect": "reject", "defects": ["P7"], "build": _m29},
    {"fid": "rev-m30-verified-at", "expect": "reject", "defects": ["P7"], "build": _m30},
    {"fid": "rev-m31-recheck", "expect": "reject", "defects": ["P7"], "build": _m31},
    {"fid": "rev-m32-no-ns", "expect": "reject", "defects": ["P7"], "build": _m32},
    {"fid": "rev-m33-no-falsifier", "expect": "reject", "defects": ["P7"], "build": _m33},
    {"fid": "rev-m34-readme-gone", "expect": "reject", "defects": ["P8"], "build": _m34},
    {"fid": "rev-m35-dup-index", "expect": "reject", "defects": ["P8"], "build": _m35},
    {"fid": "rev-m36-index-sid", "expect": "reject", "defects": ["P8"], "build": _m36},
    {"fid": "rev-m37-no-bullet", "expect": "reject", "defects": ["P8"], "build": _m37},
    {"fid": "rev-m38-extra-knowledge", "expect": "reject", "defects": ["P8"], "build": _m38},
    {"fid": "rev-m39-no-git", "expect": "reject", "defects": ["P9"], "build": _m39},
]

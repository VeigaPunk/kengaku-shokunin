"""Skip-control battery (seat F38CritSkipControls), control B1: every fixture fires a clause OTHER than the
one its name aims at.

Each fixture's own name points at a mutant of a different clause, so the battery is the shape the seat was
asked to test: "fixtures each kill by a clause other than the advertised one". The counter loads every
module in plans/battery38 (this file replaces the landed twelve), so this is measured against the FROZEN
predicate, not a dev subset.

Fixtures (fired clause -> the mutant the name aims at):
  x-p1-aimed-at-N21   fires P1 (empty frozen_instruments pin set)        -> aimed at N21 (D5)
  x-p4-aimed-at-N10   fires P4 (last quote row past its capture)         -> aimed at N10 (P6)
  x-p6-aimed-at-N13   fires P6 (teaches cell under min words)            -> aimed at N13 (P10)
  x-p7-aimed-at-N19   fires P7 (recheck line deleted)                    -> aimed at N19 (D4)
  x-p8-aimed-at-N20   fires P8 (coverage bullet deleted from README)     -> aimed at N20 (D4)
"""
import json
import pathlib

QUOTE = None


def _own_spec_empty_pins(ctx, d):
    ctx.genuine_package(d)
    spec = json.loads(ctx.spec_path.read_text())
    spec["frozen_instruments"] = {}
    sp = d / "own-spec.json"
    sp.write_text(json.dumps(spec))
    ctx.git_add(d)
    return ["package", "--root", str(d), "--spec", str(sp), "--require-clean-tree"]


def _p4_last_row_outside(ctx, d):
    ctx.genuine_package(d)
    entry = d / ctx.spec["entry"]
    qr = ctx.r36.QUOTE_ROW

    def fn(rows):
        rows = list(rows)
        if len(rows) < 2:
            raise RuntimeError("fixture: no second data row")
        m = qr.match(rows[-1])
        cap = (d / ctx.spec["capture_dir"] / m.group(2)).read_text().splitlines()
        n = max(len(cap), int(m.group(3))) + 1000
        row = rows[-1]
        if m.group(4):
            row = row[:m.span(4)[0]] + str(n) + row[m.span(4)[1]:]
        row = row[:m.span(3)[0]] + str(n) + row[m.span(3)[1]:]
        rows[-1] = row
        return rows

    entry.write_text(ctx.r36.rewrite_quotes(entry.read_text(), fn))
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


def _p6_teaches_short(ctx, d):
    ctx.genuine_package(d)
    src = d / ctx.spec["sources"]
    sids = set(ctx.spec["rows"])
    lines = src.read_text().splitlines()
    out, hit = [], False
    for line in lines:
        cells = [c for c in line.strip().strip("|").split("|")]
        if not hit and len(cells) == 11 and cells[0].strip() in sids:
            cells[6] = " short "
            line = "|" + "|".join(cells) + "|"
            hit = True
        out.append(line)
    if not hit:
        raise RuntimeError("fixture: no registry row rewritten")
    src.write_text("\n".join(out) + "\n")
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


def _p7_no_recheck(ctx, d):
    ctx.genuine_package(d)
    entry = d / ctx.spec["entry"]
    text = entry.read_text()
    out = [l for l in text.splitlines() if not l.startswith("recheck:")]
    if len(out) == len(text.splitlines()):
        raise RuntimeError("fixture: no recheck line found")
    entry.write_text("\n".join(out) + "\n")
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


def _p8_no_bullet(ctx, d):
    ctx.genuine_package(d)
    readme = d / ctx.spec["readme"]
    name = pathlib.PurePosixPath(ctx.spec["entry"]).name
    text = readme.read_text()
    out = [l for l in text.splitlines()
           if not (l.startswith("- ") and name in l and ctx.spec["receipt"].split("/", 1)[1] in l)]
    if len(out) == len(text.splitlines()):
        raise RuntimeError("fixture: no coverage bullet found")
    readme.write_text("\n".join(out) + "\n")
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree"]


FIXTURES = [
    {"fid": "x-p1-aimed-at-N21", "expect": "reject", "defects": ["P1"], "build": _own_spec_empty_pins},
    {"fid": "x-p4-aimed-at-N10", "expect": "reject", "defects": ["P4"], "build": _p4_last_row_outside},
    {"fid": "x-p6-aimed-at-N13", "expect": "reject", "defects": ["P6"], "build": _p6_teaches_short},
    {"fid": "x-p7-aimed-at-N19", "expect": "reject", "defects": ["P7"], "build": _p7_no_recheck},
    {"fid": "x-p8-aimed-at-N20", "expect": "reject", "defects": ["P8"], "build": _p8_no_bullet},
]

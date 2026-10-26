"""Battery37 module p6 — single-defect fixtures for the frozen P6 mutants M20–M27.

Every fixture starts from the genuine round-35 package (``ctx.genuine_package``), injects exactly ONE defect
into the registry (``corpus/SOURCES.md``) rows S105–S107, stages the tree index-only and runs
``package --root DIR --require-clean-tree``. P6 (``c_sources``) is the only clause that reads the registry, so
each fixture declares that single clause id. Cells are edited by index (never by a whole-line substring), so a
coincidental match elsewhere in the row — the commit hash in cells[5], the upstream name in cells[1] — is
never touched.
"""

import re

SOURCE_ROW = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
SOURCES = "corpus/SOURCES.md"


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


def _set_cell(d, sid, idx, value):
    """Set cells[idx] of row sid to value, keeping that cell's padding."""

    def fn(cells):
        old = cells[idx]
        cells[idx] = old.replace(old.strip(), value) if old.strip() else value
        return cells

    _mutate(d, sid, fn)


def _mut20(d):
    """M20: a registry row present twice (one extra byte-identical copy of S105)."""
    path = d / SOURCES
    lines, hit = path.read_text().splitlines(), 0
    for i, line in enumerate(list(lines)):
        m = SOURCE_ROW.match(line)
        if m and m.group(1) == "S105":
            lines.insert(i + 1, line)
            hit += 1
            break
    if hit != 1:
        raise RuntimeError(f"{SOURCES}: S105 row absent")
    path.write_text("\n".join(lines) + "\n")


def _mut21(d):
    """M21: S106 has 12 cells (an extra trailing cell; every indexed cell keeps its value)."""
    _mutate(d, "S106", lambda cells: cells + [" extra-cell "])


def _mut22(d):
    """M22: S107's pinned raw URL points at another task's upstream path (a real URL, not the pinned one)."""
    _set_cell(d, "S107", 1,
              "Terminal-Bench 2.0 protein-assembly task instruction (instruction.md) — "
              "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/"
              "2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/instruction.md")


def _mut23(d):
    """M23: S106 declares tier B (the frozen row tier is A)."""
    _set_cell(d, "S106", 3, "B")


def _mut24(d):
    """M24: S105 declares status queued (the frozen row status is mined)."""
    _set_cell(d, "S105", 7, "queued")


def _mut25(d):
    """M25: S107's used-by names another knowledge file instead of the entry."""
    _set_cell(d, "S107", 10, "corpus/knowledge/tb2-regex-log-grader.md")


def _mut26(d):
    """M26: S105's teaches cell is 5 distinct words (the frozen minimum is 8); the three cells stay distinct."""
    _set_cell(d, "S105", 6, "alpha beta gamma delta epsilon")


def _mut27(d):
    """M27: S107's teaches cell becomes S106's, both >= 8 words, so two of the three cells are identical."""
    path = d / SOURCES
    teaches = {}
    for line in path.read_text().splitlines():
        m = SOURCE_ROW.match(line)
        if m and m.group(1) in ("S106", "S107"):
            teaches[m.group(1)] = line.strip().strip("|").split("|")[6].strip()
    if set(teaches) != {"S106", "S107"} or teaches["S106"] == teaches["S107"]:
        raise RuntimeError(f"{SOURCES}: cannot build the identical-teaches cell pair")
    if len(teaches["S106"].split()) < 8:
        raise RuntimeError(f"{SOURCES}: S106 teaches cell is under 8 words")

    def fn(cells):
        cells[6] = " " + teaches["S106"] + " "
        return cells

    _mutate(d, "S107", fn)


def _fixture(mutator):
    def build(ctx, d):
        ctx.genuine_package(d)
        mutator(d)
        ctx.git_add(d)
        return ["package", "--root", str(d), "--require-clean-tree"]

    return build


FIXTURES = [
    {"fid": "p6-m20-registry-row-duplicated", "expect": "reject", "defects": ["P6"], "build": _fixture(_mut20)},
    {"fid": "p6-m21-row-with-twelve-cells", "expect": "reject", "defects": ["P6"], "build": _fixture(_mut21)},
    {"fid": "p6-m22-url-off-the-pinned-raw-path", "expect": "reject", "defects": ["P6"], "build": _fixture(_mut22)},
    {"fid": "p6-m23-row-tier-b", "expect": "reject", "defects": ["P6"], "build": _fixture(_mut23)},
    {"fid": "p6-m24-row-status-queued", "expect": "reject", "defects": ["P6"], "build": _fixture(_mut24)},
    {"fid": "p6-m25-used-by-another-path", "expect": "reject", "defects": ["P6"], "build": _fixture(_mut25)},
    {"fid": "p6-m26-five-word-teaches-cell", "expect": "reject", "defects": ["P6"], "build": _fixture(_mut26)},
    {"fid": "p6-m27-two-identical-teaches-cells", "expect": "reject", "defects": ["P6"], "build": _fixture(_mut27)},
]

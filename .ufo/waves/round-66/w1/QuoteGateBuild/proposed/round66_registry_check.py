#!/usr/bin/env python3
"""Registry quote and meta checks for the kengaku SOURCES registry (round 66 frontier fix).

Two checks, each shown able to fail before it is trusted:

quote  Every line of a lesson's `## Gate` section of the form

           QUOTE S### | <capture path relative to the lane root> | <verbatim text>

       must occur literally (grep -F semantics, no regex) inside the named capture. The
       capture path must resolve inside `<root>/corpus/evidence/`; an absolute path or a
       path that resolves outside it is refused, not read. Any miss, malformed line,
       missing capture or refused path is a finding; the id and the miss are printed.

meta   The `teaches` cell of each selected registry row must not contain a frozen meta
       phrase ("word bar", "teaches is one benefit", "same source and capture", matched
       case-insensitively). The teaches cell is located by the table header when a header
       row is present, else at index 6 of the 11 real cells (0-based, leading empty cell
       dropped) -- the 7th column, i.e. the cell between `anchor` and `status`.

Fail-closed choices (documented, not accidental): a lesson with no `## Gate` section or a
Gate with no QUOTE lines is a finding, and a registry with no `S###` rows is a finding, so
an empty input cannot pass vacuously. A row that does not have exactly 11 cells is a
finding: the teaches index would be untrustworthy.

Root: `--root` if given, else `$KENGAKU_ROOT`, else the directory above this script
(so the counter works with no arguments once it lives in `plans/`). The quote check needs
a root that contains `corpus/evidence/`; otherwise it is SETUP, exit 2. `meta` reads only
the registry file it is given and needs no root.

Usage:
    python3 plans/round66_registry_check.py quote corpus/lessons/round-66.md
    python3 plans/round66_registry_check.py meta corpus/SOURCES.md [S236 S237 ...]
    python3 plans/round66_registry_check.py --selftest --work <scratch>

Exit: 0 all selected checks clean, 1 a named finding (red), 2 could-not-evaluate (SETUP).
Selftest fixtures are created under --work only and removed before exit.
"""

import argparse
import contextlib
import io
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

META_PHRASES = ("word bar", "teaches is one benefit", "same source and capture")
TEACHES_FALLBACK_INDEX = 6  # 0-based over the 11 real cells (leading empty cell dropped)
COLUMNS = 11
QUOTE_RE = re.compile(r"^\s*QUOTE\s+(S\d{3,})\s*\|\s*(.*)$")
GATE_RE = re.compile(r"^##\s+Gate\b")
HEADING_RE = re.compile(r"^#{1,2}\s+")
ID_RE = re.compile(r"^S\d{3,}$")


def setup(msg: str) -> int:
    print(f"SETUP {msg}")
    return 2


def lane_root(arg: Path | None) -> Path:
    if arg is not None:
        return Path(arg).resolve()
    env = os.environ.get("KENGAKU_ROOT")
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parents[1]


def root_problem(root: Path) -> str | None:
    if not (root / "corpus").is_dir():
        return f"root {root} has no corpus/ directory (pass --root)"
    if not (root / "corpus/evidence").is_dir():
        return f"root {root} has no corpus/evidence/ directory (pass --root)"
    return None


def gate_section(lines: list[str]) -> list[str] | None:
    start = None
    for i, line in enumerate(lines):
        if GATE_RE.match(line.strip()):
            start = i + 1
            break
    if start is None:
        return None
    section = []
    for line in lines[start:]:
        if HEADING_RE.match(line):
            break
        section.append(line)
    return section


def parse_quotes(section: list[str]) -> list[dict]:
    quotes = []
    for line in section:
        m = QUOTE_RE.match(line)
        if not m:
            continue
        sid, rest = m.group(1), m.group(2)
        if "|" not in rest:
            quotes.append({"id": sid, "capture": None, "needle": None, "error": "malformed"})
            continue
        capture, needle = rest.split("|", 1)
        quotes.append({"id": sid, "capture": capture.strip(), "needle": needle.strip(), "error": None})
    return quotes


def cmd_quote(lesson: Path, root: Path) -> int:
    if not lesson.is_file():
        return setup(f"lesson not found: {lesson}")
    section = gate_section(lesson.read_text(encoding="utf-8", errors="replace").splitlines())
    if section is None:
        print(f"CHECK defect: quote lesson={lesson} has no ## Gate section")
        print("CHECK quote fail")
        return 1
    quotes = parse_quotes(section)
    if not quotes:
        print(f"CHECK defect: quote lesson={lesson} ## Gate has no QUOTE lines (vacuous check refused)")
        print("CHECK quote fail")
        return 1
    evidence = (root / "corpus/evidence").resolve()
    misses = 0
    for q in quotes:
        sid = q["id"]
        if q["error"]:
            print(f"CHECK defect: quote {sid} malformed QUOTE line (want QUOTE {sid} | <capture> | <verbatim text>)")
            misses += 1
            continue
        capture, needle = q["capture"], q["needle"]
        if not needle:
            print(f"CHECK defect: quote {sid} empty verbatim text")
            misses += 1
            continue
        raw = Path(capture)
        resolved = (root / raw).resolve()
        if raw.is_absolute() or resolved == evidence or not resolved.is_relative_to(evidence):
            print(f"CHECK defect: quote {sid} refused capture outside corpus/evidence/: {capture}")
            misses += 1
            continue
        if not resolved.is_file():
            print(f"CHECK defect: quote {sid} miss capture={capture} (capture file missing)")
            misses += 1
            continue
        if needle.encode("utf-8") in resolved.read_bytes():
            print(f"QUOTE {sid} capture={capture} result=FOUND needle={needle!r}")
        else:
            print(f"CHECK defect: quote {sid} miss capture={capture} needle={needle!r}")
            misses += 1
    print(f"CHECK quote quotes={len(quotes)} misses={misses}")
    print("CHECK ok quote" if misses == 0 else "CHECK quote fail")
    return 0 if misses == 0 else 1


def parse_registry(path: Path) -> tuple[int | None, list[dict]]:
    header_index = None
    rows = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        lowered = [c.lower() for c in cells]
        if header_index is None and cells and lowered[0] == "id" and "teaches" in lowered:
            header_index = lowered.index("teaches")
            continue
        if cells and ID_RE.match(cells[0]):
            rows.append({"line": lineno, "id": cells[0], "cells": cells})
    return header_index, rows


def cmd_meta(registry: Path, ids: list[str]) -> int:
    if not registry.is_file():
        return setup(f"registry not found: {registry}")
    header_index, rows = parse_registry(registry)
    index = header_index if header_index is not None else TEACHES_FALLBACK_INDEX
    by_id = {}
    for row in rows:
        by_id.setdefault(row["id"], []).append(row)
    if ids:
        missing = [i for i in ids if i not in by_id]
        if missing:
            print(f"CHECK defect: meta ids not found in {registry}: {' '.join(missing)}")
            print("CHECK meta fail")
            return 1
        selected = [row for i in ids for row in by_id[i]]
    else:
        selected = rows
    if not selected:
        print(f"CHECK defect: meta registry={registry} has no S### rows (vacuous check refused)")
        print("CHECK meta fail")
        return 1
    findings = 0
    for row in selected:
        cells = row["cells"]
        if len(cells) != COLUMNS:
            print(f"CHECK defect: meta {row['id']} row has {len(cells)} cells, expected {COLUMNS} (line {row['line']})")
            findings += 1
            continue
        cell = cells[index]
        lowered = cell.lower()
        for phrase in META_PHRASES:
            if phrase in lowered:
                print(f"CHECK defect: meta {row['id']} phrase={phrase!r} in teaches cell (line {row['line']}): {cell!r}")
                findings += 1
    print(f"CHECK meta rows={len(selected)} findings={findings} teaches_column={index}")
    print("CHECK ok meta" if findings == 0 else "CHECK meta fail")
    return 0 if findings == 0 else 1


def quiet(fn, *args) -> int:
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args)


def cmd_selftest(work: Path) -> int:
    """A passing and a failing fixture for each check, plus the refusal and fail-closed edges."""
    fx = Path(tempfile.mkdtemp(dir=work, prefix="selftest-"))
    try:
        root = fx / "root"
        (root / "corpus/evidence").mkdir(parents=True)
        (root / "corpus/SOURCES.md").write_text("outside evidence\n", encoding="utf-8")
        (root / "corpus/evidence/cap.txt").write_text("alpha line\nbeta line\n", encoding="utf-8")

        def lesson(name: str, body: str) -> Path:
            p = fx / name
            p.write_text(body, encoding="utf-8")
            return p

        good_lesson = lesson(
            "good.md",
            "# fixture\n\n## Gate\n\n"
            "QUOTE S900 | corpus/evidence/cap.txt | alpha line\n"
            "QUOTE S901 | corpus/evidence/cap.txt | beta line\n\n"
            "## Mistakes\n\nQUOTE S902 | corpus/evidence/cap.txt | not in gate section\n",
        )
        miss_lesson = lesson(
            "miss.md",
            "## Gate\n\nQUOTE S903 | corpus/evidence/cap.txt | gamma line\n",
        )
        refuse_lesson = lesson(
            "refuse.md",
            "## Gate\n\nQUOTE S904 | corpus/SOURCES.md | outside evidence\n",
        )
        absolute_lesson = lesson(
            "absolute.md",
            f"## Gate\n\nQUOTE S905 | {root / 'corpus/evidence/cap.txt'} | alpha line\n",
        )
        nogate_lesson = lesson("nogate.md", "# fixture\n\n## Other\n\nno gate here\n")
        empty_gate_lesson = lesson("empty-gate.md", "## Gate\n\nplain prose only\n")

        header = (
            "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|\n"
        )

        def row(sid: str, teaches: str) -> str:
            return (
                f"| {sid} | synthetic source | code | A | synthetic scope | synthetic anchor | "
                f"{teaches} | mined | 2026-11-03 | 180d | corpus/lessons/round-66.md |\n"
            )

        clean_registry = fx / "clean.md"
        clean_registry.write_text(header + row("S910", "one grounded benefit of at most 25 words"), encoding="utf-8")
        meta_registry = fx / "meta.md"
        meta_registry.write_text(header + row("S911", "supersedes S1 - same source and capture"), encoding="utf-8")
        select_registry = fx / "select.md"
        select_registry.write_text(
            header + row("S912", "one grounded benefit") + row("S913", "teaches is one benefit within the word bar"),
            encoding="utf-8",
        )
        noheader_registry = fx / "noheader.md"
        noheader_registry.write_text(row("S914", "same source and capture, no header row here"), encoding="utf-8")
        shape_registry = fx / "shape.md"
        shape_registry.write_text(header + "| S915 | a | b | c | d | e | f | g | h | i |\n", encoding="utf-8")

        results = {
            "quote_pass": quiet(cmd_quote, good_lesson, root) == 0,
            "quote_miss": quiet(cmd_quote, miss_lesson, root) == 1,
            "quote_refuse_outside_evidence": quiet(cmd_quote, refuse_lesson, root) == 1,
            "quote_refuse_absolute": quiet(cmd_quote, absolute_lesson, root) == 1,
            "quote_no_gate": quiet(cmd_quote, nogate_lesson, root) == 1,
            "quote_empty_gate": quiet(cmd_quote, empty_gate_lesson, root) == 1,
            "meta_pass": quiet(cmd_meta, clean_registry, []) == 0,
            "meta_fail": quiet(cmd_meta, meta_registry, []) == 1,
            "meta_selection_clean": quiet(cmd_meta, select_registry, ["S912"]) == 0,
            "meta_selection_dirty": quiet(cmd_meta, select_registry, ["S913"]) == 1,
            "meta_no_header_fallback": quiet(cmd_meta, noheader_registry, []) == 1,
            "meta_bad_shape": quiet(cmd_meta, shape_registry, []) == 1,
            "meta_missing_id": quiet(cmd_meta, select_registry, ["S999"]) == 1,
        }
        print(f"SELFTEST {results}")
        return 0 if all(results.values()) else 1
    finally:
        shutil.rmtree(fx, ignore_errors=True)


def main() -> int:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", type=Path, help="lane root (default: $KENGAKU_ROOT or the script's parent)")
    ap = argparse.ArgumentParser(description="quote/meta checks over the kengaku registry and lesson Gates")
    sub = ap.add_subparsers(dest="command")
    p_quote = sub.add_parser("quote", parents=[common], help="check QUOTE lines against their captures")
    p_quote.add_argument("lesson", type=Path)
    p_meta = sub.add_parser("meta", parents=[common], help="check teaches cells for frozen meta phrases")
    p_meta.add_argument("registry", type=Path)
    p_meta.add_argument("ids", nargs="*", help="row ids (default: every row)")
    ap.add_argument("--root", type=Path, help="lane root (default: $KENGAKU_ROOT or the script's parent)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--work", type=Path, help="scratch dir for --selftest")
    a = ap.parse_args()

    if a.selftest:
        if not a.work:
            return setup("--work required for --selftest")
        a.work.mkdir(parents=True, exist_ok=True)
        return cmd_selftest(a.work)
    if a.command is None:
        ap.print_usage(sys.stderr)
        return setup("subcommand required: quote <lesson.md> or meta <SOURCES.md> [ids ...]")

    root = lane_root(a.root)
    if a.command == "quote":
        problem = root_problem(root)
        if problem:
            return setup(problem)
        return cmd_quote(a.lesson, root)
    return cmd_meta(a.registry, a.ids)


if __name__ == "__main__":
    sys.exit(main())

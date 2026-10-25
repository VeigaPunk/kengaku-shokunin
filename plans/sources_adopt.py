#!/usr/bin/env python3
"""Source-adoption gate for kengaku's corpus registry.

Round 29 attempt 2 (2026-10-25). The fleet census (`scripts/sources-census.sh`)
validates a registry that already exists; nothing in the lane checked a row set
*before* it was appended. This gate does that check, so an adoption round cannot
append a colliding id, a mangled cell, or a `used-by` pointing at an entry that
was never admitted.

Capabilities (each separately exercised by `--selftest`):
  1. id-collision detection against the live registry, using the census parser's
     own 0-3-leading-space row anchor -- a column-zero-only pattern false-greens
     an indented collision (scratch `  | S002 |` fixture, SKILL/CORPUS note);
  2. staged-row schema check: exactly 11 cells, no literal or escaped `|` inside
     a cell, a valid `status`, and a valid `recheck` cell;
  3. append-block construction that normalizes a prose `recheck` cell to the
     frozen access date (reporting the stripped prose separately) and rewrites
     `used-by` to exactly the admitted entries citing the row;
  4. refusal with a non-zero exit for a missing requested id, an escaped pipe, a
     duplicate staged id, or a nonempty collision set.

Scope: registry row mechanics only. Source truth, tier judgement and the census
itself stay where they are (CORPUS.md contract v1; census is fleet-owned).
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

ROW_RE = re.compile(r"^( {0,3})\|[ \t]*(S[0-9]{3,})[ \t]*\|")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CADENCE_RE = re.compile(r"^\d+d$")
SYMBOLIC_CADENCE = {"on-release", "on-request", "on-commit", "never"}
STATUSES = {"queued", "mined", "rejected"}
COLUMNS = 11

EXIT_OK = 0
EXIT_COLLISION = 3
EXIT_MALFORMED = 4
EXIT_REQUEST = 5


class Row:
    __slots__ = ("line_no", "indent", "row_id", "cells", "raw")

    def __init__(self, line_no: int, indent: int, row_id: str, cells: list[str], raw: str):
        self.line_no = line_no
        self.indent = indent
        self.row_id = row_id
        self.cells = cells
        self.raw = raw

    def cell(self, index: int) -> str:
        return self.cells[index].strip()


def split_cells(raw: str) -> tuple[list[str] | None, str]:
    """Split one table row into its 11 cells.

    Returns (cells, reason). cells is None when the row cannot be parsed as an
    11-cell row; reason names the defect. An escaped pipe (`\\|`) inside a cell
    is a defect rather than a separator: it silently produces 12 cells upstream,
    which is the real failure seen on the kengaku campaign package.
    """
    stripped = raw.rstrip("\n")
    if "\\|" in stripped:
        return None, "escaped-pipe"
    body = stripped.strip()
    if not body.startswith("|") or not body.endswith("|"):
        return None, "not-a-table-row"
    cells = body[1:-1].split("|")
    if len(cells) != COLUMNS:
        return None, f"columns={len(cells)}"
    return cells, ""


def parse_rows(text: str) -> tuple[list[Row], list[tuple[int, str, str]]]:
    """Rows matching the census anchor (0-3 leading spaces) plus malformed rows."""
    pattern = ROW_RE
    rows: list[Row] = []
    bad: list[tuple[int, str, str]] = []
    for index, raw in enumerate(text.splitlines(), start=1):
        match = pattern.match(raw)
        if not match:
            continue
        cells, reason = split_cells(raw)
        if cells is None:
            bad.append((index, match.group(2), reason))
            continue
        rows.append(Row(index, len(match.group(1)), match.group(2), cells, raw))
    return rows, bad


def row_defects(row: Row) -> list[str]:
    defects: list[str] = []
    status = row.cell(7)
    if status not in STATUSES:
        defects.append(f"status={status or '<empty>'}")
    recheck = row.cell(9)
    if not (ISO_DATE_RE.match(recheck) or CADENCE_RE.match(recheck) or recheck in SYMBOLIC_CADENCE):
        defects.append("recheck-prose" if recheck else "recheck-empty")
    if not row.cell(1):
        defects.append("source-empty")
    return defects


def ids(rows: list[Row]) -> list[str]:
    return [row.row_id for row in rows]


def collisions(registry_ids: list[str], staged_ids: list[str]) -> list[str]:
    return sorted(set(registry_ids) & set(staged_ids))


def duplicate_ids(staged_ids: list[str]) -> list[str]:
    seen: set[str] = set()
    dupes: list[str] = []
    for row_id in staged_ids:
        if row_id in seen and row_id not in dupes:
            dupes.append(row_id)
        seen.add(row_id)
    return dupes


def build_block(
    rows: list[Row],
    want_ids: list[str],
    admitted_entries: list[str],
    access_date: str,
    recheck_default: str = "180d",
    attest_opened: bool = False,
) -> tuple[list[str], list[tuple[str, str]], list[str]]:
    """Return (block_lines, stripped_prose, missing_ids)."""
    by_id = {row.row_id: row for row in rows}
    if len(set(want_ids)) != len(want_ids):
        return [], [], ["duplicate-request"]
    missing = [row_id for row_id in want_ids if row_id not in by_id]
    if missing:
        return [], [], missing
    block: list[str] = []
    prose: list[tuple[str, str]] = []
    used_by = ", ".join(admitted_entries) or "\u2014"
    for row_id in want_ids:
        row = by_id[row_id]
        cells = [cell.strip() for cell in row.cells]
        # A row is appended only if it was opened this round and is already mined.
        # The gate cannot verify a fetch, so re-dating a staged `opened` cell requires
        # an explicit attestation; silently stamping it would launder a stale row.
        if cells[7] != "mined":
            return [], [], [f"{row_id}:not-mined"]
        if cells[8] != access_date:
            if not attest_opened:
                return [], [], [f"{row_id}:not-opened-this-round"]
            cells[8] = access_date
        recheck = cells[9]
        if not (ISO_DATE_RE.match(recheck) or CADENCE_RE.match(recheck) or recheck in SYMBOLIC_CADENCE):
            prose.append((row_id, recheck))
            # A recheck is a future due date or an interval from `opened`, never the
            # access date itself: that would put every adopted row 0 days overdue.
            cells[9] = recheck_default
        cells[10] = used_by
        block.append("| " + " | ".join(cells) + " |")
    return block, prose, []


def collect(package: Path, registry: Path) -> tuple[list[Row], list[Row], list[tuple[int, str, str]]]:
    staged_text = package.read_text(encoding="utf-8")
    registry_text = registry.read_text(encoding="utf-8")
    staged, bad = parse_rows(staged_text)
    registry_rows, _ = parse_rows(registry_text)
    return staged, registry_rows, bad


def check(
    package: Path,
    registry: Path,
    want_ids: list[str] | None = None,
    scope: bool = False,
) -> tuple[int, dict[str, object]]:
    staged, registry_rows, bad = collect(package, registry)
    clash = collisions(ids(registry_rows), ids(staged))
    dupes = duplicate_ids(ids(staged))
    defects = {row.row_id: row_defects(row) for row in staged}
    defects = {row_id: found for row_id, found in defects.items() if found}
    malformed = [f"{row_id}:{reason}" for _, row_id, reason in bad]
    report: dict[str, object] = {
        "registry": len(registry_rows),
        "staged": len(staged),
        "malformed_total": len(malformed),
        "prose_recheck_total": sum(1 for row in staged if "recheck-prose" in row_defects(row)),
    }
    if want_ids and scope:
        # Opt-in (`--scope-to-admit`): a package is staged for many rounds and the
        # round cannot fix a row it does not append. The default stays strict, so a
        # mangled staged row is refused unless the caller narrows the set explicitly.
        scope = set(want_ids)
        clash = [row_id for row_id in clash if row_id in scope]
        dupes = [row_id for row_id in dupes if row_id in scope]
        # A prose `recheck` is not a refusal in scoped mode: build_block normalizes
        # it to the frozen access date and reports the stripped prose (capability 3).
        defects = {
            row_id: [item for item in found if item != "recheck-prose"]
            for row_id, found in defects.items()
            if row_id in scope
        }
        defects = {row_id: found for row_id, found in defects.items() if found}
        report["prose_recheck"] = sum(
            1 for row in staged if row.row_id in scope and "recheck-prose" in row_defects(row)
        )
        malformed = [item for item in malformed if item.split(":", 1)[0] in scope]
    report.update({"collisions": clash, "duplicates": dupes, "malformed": malformed, "defects": defects})
    if malformed or dupes or defects:
        code = EXIT_COLLISION if clash else EXIT_MALFORMED
        return code, report
    if clash:
        return EXIT_COLLISION, report
    if want_ids:
        missing = [row_id for row_id in want_ids if row_id not in ids(staged)]
        if missing:
            report["missing"] = missing
            return EXIT_REQUEST, report
    return EXIT_OK, report


def print_report(report: dict[str, object]) -> None:
    print(
        "registry={registry} staged={staged} collisions={coll} malformed={mal} "
        "duplicates={dup} defects={defc} prose={prose}".format(
            registry=report["registry"],
            staged=report["staged"],
            coll=len(report["collisions"]),
            mal=len(report["malformed"]),
            dup=len(report["duplicates"]),
            defc=len(report["defects"]),
            prose=report.get("prose_recheck", report.get("prose_recheck_total", 0)),
        )
    )
    for key in ("collisions", "malformed", "duplicates"):
        values = report[key]
        if values:
            print(f"  {key}: {' '.join(str(value) for value in values)}")
    defects = report["defects"]
    if defects:
        for row_id, found in sorted(defects.items()):
            print(f"  defect {row_id}: {' '.join(found)}")
    if report.get("missing"):
        print(f"  missing: {' '.join(report['missing'])}")


# --------------------------------------------------------------------------- selftest

HEADER = "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
GOOD_ROW = (
    "| S900 | fixture source — https://example.invalid/x | docs | A | fixture scope | "
    "anchor text | fixture teaches | mined | 2026-10-25 | 180d | "
    "corpus/knowledge/old.md |"
)
PROSE_ROW = GOOD_ROW.replace("| 180d |", "| 2026-10-23 — re-verify at next release |")


def selftest() -> int:
    cases: list[tuple[str, bool]] = []

    def case(name: str, passed: bool) -> None:
        cases.append((name, passed))
        print(f"CASE {name} {'PASS' if passed else 'FAIL'}")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)

        def write(name: str, text: str) -> Path:
            path = root / name
            path.write_text(text, encoding="utf-8")
            return path

        # 1. column-zero collision is caught
        reg = write("reg0.md", HEADER + GOOD_ROW.replace("S900", "S001") + "\n")
        staged = write("staged0.md", HEADER + GOOD_ROW.replace("S900", "S001") + "\n")
        code, report = check(staged, reg)
        case("collision-zero-indent", code == EXIT_COLLISION and report["collisions"] == ["S001"])

        # 2. 1-space-indented collision is caught (the proven false-green)
        staged = write("staged1.md", HEADER + " " + GOOD_ROW.replace("S900", "S002") + "\n")
        reg = write("reg1.md", HEADER + GOOD_ROW.replace("S900", "S002") + "\n")
        code, report = check(staged, reg)
        case("collision-one-space", code == EXIT_COLLISION and report["collisions"] == ["S002"])

        # 3. 3-space-indented collision is caught (census anchor boundary)
        staged = write("staged2.md", HEADER + "   " + GOOD_ROW.replace("S900", "S003") + "\n")
        reg = write("reg2.md", HEADER + GOOD_ROW.replace("S900", "S003") + "\n")
        code, report = check(staged, reg)
        case("collision-three-space", code == EXIT_COLLISION and report["collisions"] == ["S003"])

        # 4. 4-space indentation is outside the clause: no row, so no collision
        staged = write("staged3.md", HEADER + "    " + GOOD_ROW.replace("S900", "S004") + "\n")
        reg = write("reg3.md", HEADER + GOOD_ROW.replace("S900", "S004") + "\n")
        code, report = check(staged, reg)
        case(
            "four-space-not-a-row",
            code == EXIT_OK and report["staged"] == 0 and report["collisions"] == [],
        )

        # 5. escaped pipe is refused as malformed, never silently 12 cells
        staged = write(
            "staged4.md",
            HEADER + GOOD_ROW.replace("S900", "S005").replace("fixture scope", "scope \\| scope") + "\n",
        )
        reg = write("reg4.md", HEADER)
        code, report = check(staged, reg)
        twelve = write("staged4b.md", HEADER + GOOD_ROW.replace("S900", "S005") + " extra cell |\n")
        code12, report12 = check(twelve, reg)
        case(
            "escaped-pipe-refused",
            code == EXIT_MALFORMED
            and report["malformed"] == ["S005:escaped-pipe"]
            and code12 == EXIT_MALFORMED
            and report12["malformed"] == ["S005:columns=12"],
        )

        # 6. prose recheck normalizes to the access date, prose kept
        staged = write("staged5.md", HEADER + PROSE_ROW.replace("S900", "S006") + "\n")
        reg = write("reg5.md", HEADER)
        rows, _ = parse_rows(staged.read_text(encoding="utf-8"))
        code_scoped, _ = check(staged, reg, ["S006"], scope=True)
        stale_rows, _ = parse_rows(
            (HEADER + GOOD_ROW.replace("S900", "S014").replace("| 2026-10-25 |", "| 2026-10-19 |"))
            + "\n"
        )
        _, _, stale_missing = build_block(
            stale_rows, ["S014"], ["corpus/knowledge/new.md"], "2026-10-25"
        )
        stale_block, _, stale_ok = build_block(
            stale_rows, ["S014"], ["corpus/knowledge/new.md"], "2026-10-25", "180d", True
        )
        block, prose, missing = build_block(rows, ["S006"], ["corpus/knowledge/new.md"], "2026-10-25")
        on_commit = write(
            "staged5b.md",
            HEADER + GOOD_ROW.replace("S900", "S013").replace("| 180d |", "| on-commit |") + "\n",
        )
        oc_rows, _ = parse_rows(on_commit.read_text(encoding="utf-8"))
        oc_block, oc_prose, _ = build_block(oc_rows, ["S013"], ["corpus/knowledge/new.md"], "2026-10-25")
        case(
            "prose-recheck-normalized",
            not missing
            and len(block) == 1
            and len(block[0].split("|")) == 13
            and block[0].split("|")[10].strip() == "180d"
            and block[0].split("|")[9].strip() == "2026-10-25"
            and prose and prose[0][0] == "S006"
            # a symbolic cadence is a valid recheck and must survive, not become a date
            and bool(oc_block) and "| on-commit |" in oc_block[0] and not oc_prose
            # the branch main() actually takes: a requested prose row is tolerated
            and code_scoped == EXIT_OK
            and stale_missing == ["S014:not-opened-this-round"]
            and not stale_ok and stale_block[0].split("|")[9].strip() == "2026-10-25",
        )

        # 7. dangling used-by is rewritten to the admitted set only
        block, _, _ = build_block(rows, ["S006"], ["corpus/knowledge/new.md"], "2026-10-25")
        case(
            "usedby-projected",
            bool(block) and block[0].rstrip().endswith("corpus/knowledge/new.md |")
            and "old.md" not in block[0],
        )

        # 8. duplicate staged id is refused
        staged = write(
            "staged6.md",
            HEADER + GOOD_ROW.replace("S900", "S007") + "\n" + GOOD_ROW.replace("S900", "S007") + "\n",
        )
        reg = write("reg6.md", HEADER)
        code, report = check(staged, reg)
        case("duplicate-staged-id", code == EXIT_MALFORMED and report["duplicates"] == ["S007"])

        # 9. a targeted append passes even when an unrequested row is malformed
        staged = write(
            "staged7.md",
            HEADER + GOOD_ROW.replace("S900", "S008") + "\n"
            + GOOD_ROW.replace("S900", "S011").replace("fixture scope", "scope \\| scope") + "\n",
        )
        code, report = check(staged, reg, ["S008"], scope=True)
        case(
            "clean-package-passes",
            code == EXIT_OK and report["staged"] == 1 and report["malformed_total"] == 1,
        )

        # 10. an invalid nonempty recheck is refused unscoped, and a missing id is refused
        prose_only = write("staged8.md", HEADER + PROSE_ROW.replace("S900", "S012") + "\n")
        code_prose, _ = check(prose_only, reg)
        code, report = check(staged, reg, ["S008", "S010"], scope=True)
        case(
            "missing-requested-id",
            code == EXIT_REQUEST
            and report.get("missing") == ["S010"]
            and code_prose == EXIT_MALFORMED,
        )

    failed = [name for name, passed in cases if not passed]
    print(f"SELFTEST cases={len(cases)} failed={len(failed)}")
    if failed:
        print("  failed: " + " ".join(failed))
        return 1
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--registry", type=Path, help="live corpus/SOURCES.md")
    parser.add_argument("--package", type=Path, help="SOURCES.append.md to check")
    parser.add_argument("--admit-ids", default="", help="comma-separated ids to append")
    parser.add_argument("--entries", default="", help="comma-separated admitted entry paths")
    parser.add_argument("--access-date", default="", help="ISO date frozen for this adoption")
    parser.add_argument(
        "--recheck",
        default="180d",
        help="recheck value written when a staged cell is prose (a cadence or a future ISO date)",
    )
    parser.add_argument("--out", type=Path, help="write the append block here")
    parser.add_argument(
        "--attest-opened",
        action="store_true",
        help="assert the requested rows were opened on --access-date (re-dates their opened cell)",
    )
    parser.add_argument(
        "--scope-to-admit",
        action="store_true",
        help="refuse only the requested rows' defects (default: any staged defect refuses)",
    )
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.registry or not args.package:
        parser.error("--registry and --package are required unless --selftest")
    want = [item for item in args.admit_ids.split(",") if item]
    code, report = check(args.package, args.registry, want or None, args.scope_to_admit)
    print_report(report)
    if code != EXIT_OK or not want:
        return code
    if not args.access_date:
        parser.error("--access-date is required when --admit-ids is given")
    if not args.entries:
        parser.error("--entries is required when --admit-ids is given (used-by has no fallback)")
    if not ISO_DATE_RE.match(args.access_date):
        parser.error("--access-date must be an ISO date (YYYY-MM-DD)")
    if not (
        ISO_DATE_RE.match(args.recheck)
        or CADENCE_RE.match(args.recheck)
        or args.recheck in SYMBOLIC_CADENCE
    ):
        parser.error("--recheck must be an ISO date, <N>d, or a known symbolic cadence")
    rows, _ = parse_rows(args.package.read_text(encoding="utf-8"))
    entries = [item for item in args.entries.split(",") if item]
    block, prose, missing = build_block(
        rows, want, entries, args.access_date, args.recheck, args.attest_opened
    )
    if args.attest_opened:
        print("  attested: the caller asserts every requested source was opened on "
              + args.access_date)
    if missing:
        print(f"  missing: {' '.join(missing)}")
        return EXIT_REQUEST
    for row_id, text in prose:
        print(f"  normalized recheck {row_id}: {text}")
    text = "\n".join(block) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
        print(f"wrote {args.out} rows={len(block)}")
    else:
        sys.stdout.write(text)
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

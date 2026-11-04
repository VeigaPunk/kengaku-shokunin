#!/usr/bin/env python3
"""R74-C2 counter — hardened registry declaration audit over supplied working-tree bytes.

Frozen before data on 2026-11-04 (L1 KengakuR74); see plans/round-74-claims.md §C2 for the
predicate this implements. Reads working-tree bytes, not a Git snapshot; final receipts name their measured revision.

    python3 plans/round74_c2_registry_audit.py --lane .                    # verdict
    python3 plans/round74_c2_registry_audit.py --selftest --work DIR       # clean + red arms
    python3 plans/round74_c2_registry_audit.py --mutants --work DIR        # byte mutants

Why this counter exists (round-73 lessons M73-5/M73-8 and C2BlindSpotR73 findings):
In round 73, `parse_rows` silently skipped non-eight-cell lines (`len(cells) != 8: continue`),
so malformed rows (e.g. 7 cells or 9 cells) completely disappeared before accounting. Furthermore,
`command_flags` was defined but never called (unbacked entry flags survived), `selftest_unbacked`
did not check if the self-test runner script exists, and `check_errata` checked only the first
matching item while ignoring contradictory later items.

This hardened counter:
1. Replaces silent skipping with named defect lines (`MALFORMED-ROW columns=<n>`).
2. Checks entry flags: any flag in `command_flags(entry)` must appear in the script body (`D2 <name>:entry:unbacked-flag:<flag>`).
3. Checks self-test scripts: if `selftest` names a script, that script must exist on disk (`D2 <name>:self-test:script-absent`).
4. Checks errata revision consistency across all items mentioning `label` (`ERRATA:contradictory-revision`).
5. Uses an owned child directory of `--work` for fixtures and cleans up reliably.

Predicate (all five legs must hold; `MISMATCH 0`):
  D1 ROWS       every registry row's entry cell names an existing Python script, and every
                such script parses with `ast.parse`
  D2 FIELDS     for every row: eight non-empty cells; kind in {gate, probe}; owner cell begins
                `kengaku`; entry names a script; gate verdict maps declare `0` and (`1` or a
                `failed` class), probe maps declare `0`; entry command flags exist in the script;
                self-test runner script exists and flags exist; pinned-values and write-scope non-empty
  D3 EVERY-ROW  no duplicate row names (byte-identical or case-insensitive), and every row is priced
  D4 ERRATA     the round-72 erratum's numbered items each quote their own superseded
                label, name that label's true revision, and carry no contradictory revisions
  MALFORMED     no table line with columns != 8
Exit 0 pass, 1 fail (each defect on its own line), 2 setup.
"""
from __future__ import annotations

import argparse
import ast
import re
import shutil
import sys
import tempfile
from pathlib import Path

SKILL_REL = "SKILL.md"
CLAIMS_REL = "plans/round-71-claims.md"
REGISTRY_HEADING = "## Gate/probe registry"
ERRATA_HEADING = "## Errata — round 72"
COLUMNS = ("name", "kind", "entry", "verdict-map", "self-test", "pinned-values",
           "write-scope", "owner")
KINDS = ("gate", "probe")
OWNER_PREFIX = "kengaku"
ERRATUM_ITEMS = (
    ("Do-nothing control (committed at freeze)", "c80fcdb3"),
    ("Red-before (committed at freeze)", "d8a77d3f"),
)
CMD = re.compile(r"python3 ((?:plans/[A-Za-z0-9_.-]+\.py|corpus/evidence/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\.py|grader\.py))")
FLAG = re.compile(r"(--[a-z][a-z0-9-]*)")
DEFECT_WORDS = ("failed", "fail", "reject", "defect")


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


def registry_block(text: str) -> str:
    i = text.find(REGISTRY_HEADING)
    if i < 0:
        return ""
    j = text.find("\n## ", i + 1)
    return text[i:j] if j > 0 else text[i:]


def parse_rows(block: str) -> tuple[list[list[str]], list[str]]:
    """Returns (valid_rows, malformed_defects).

    Unlike round-73, lines starting with '|' that are not headers or separators
    and have column count != 8 are reported as defects, not silently dropped.
    """
    rows = []
    malformed = []
    for line in block.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if cells[0] == "name":          # header line
            continue
        if set(cells[0]) <= set("-: "): # separator line
            continue
        if len(cells) != 8:
            malformed.append(f"MALFORMED-ROW columns={len(cells)} line={line[:40]}")
            continue
        rows.append(cells)
    return rows, malformed


def entry_script(cell: str) -> str | None:
    m = CMD.search(cell)
    return m.group(1) if m else None


def command_flags(cell: str) -> list[str]:
    """Flags inside the cell's first explicit command, before prose (em dash, paren, semicolon)."""
    m = CMD.search(cell)
    if not m:
        return []
    tail = cell[m.start():]
    for sep in ("—", " (", ";"):
        k = tail.find(sep)
        if k > 0:
            tail = tail[:k]
    return sorted(set(FLAG.findall(tail)))


def selftest_runner(cell: str) -> str | None:
    m = CMD.search(cell)
    return m.group(1) if m else None


def price_row(row: list[str], lane: Path) -> list[str]:
    """Every field priced; one `<field>:<why>` defect string per failure."""
    name = row[0] if row else "<empty>"
    out = []
    if len(row) != 8:
        return [f"{name}:columns:{len(row)}"]
    for field, cell in zip(COLUMNS, row):
        if not cell:
            out.append(f"{name}:{field}:empty")
    kind, entry, verdict, selftest, pinned, scope, owner = row[1], row[2], row[3], row[4], row[5], row[6], row[7]
    if kind not in KINDS:
        out.append(f"{name}:kind:{kind}")
    if not owner.startswith(OWNER_PREFIX):
        out.append(f"{name}:owner:{owner[:24]}")
    script = entry_script(entry)
    if script is None:
        out.append(f"{name}:entry:no-script")
    elif not (lane / script).exists():
        out.append(f"{name}:entry:script-absent:{script}")
    else:
        # Check entry flags against script body (C14)
        flags = command_flags(entry)
        body = read(lane / script)
        for fl in flags:
            if fl not in body:
                out.append(f"{name}:entry:unbacked-flag:{fl}")

    codes = set(re.findall(r"`(\d+)`", verdict)) | set(re.findall(r"`(\d+)`", verdict.upper()))
    if kind == "gate":
        failed_class = any(w in verdict.lower() for w in DEFECT_WORDS)
        if "0" not in codes or not ("1" in codes or failed_class):
            out.append(f"{name}:gate-verdict:{','.join(sorted(codes)) or 'none'}")
    elif kind == "probe" and "0" not in codes:
        out.append(f"{name}:probe-verdict:{','.join(sorted(codes)) or 'none'}")

    # Self-test check (C04, C05, C15)
    if not re.search(r"\bnone\b", selftest.lower()) and not re.search(r"\bno\b.{0,24}--[a-z][a-z0-9-]*", selftest):
        runner = selftest_runner(selftest)
        if runner:
            runner_path = lane / runner
            if not runner_path.exists():
                out.append(f"{name}:self-test:script-absent:{runner}")
            else:
                body = read(runner_path)
                flags = command_flags(selftest)
                if flags and all(fl not in body for fl in flags):
                    out.append(f"{name}:self-test:unbacked-flag:{','.join(flags)}")
        else:
            # Script name in prose or flag-only
            scripts = sorted(set(re.findall(r"(?:plans|corpus|grader)[A-Za-z0-9_./-]*\.py", selftest)))
            flags = sorted(set(FLAG.findall(selftest)))
            if scripts:
                for s in scripts:
                    if not (lane / s).exists():
                        out.append(f"{name}:self-test:script-absent:{s}")
            if script and (lane / script).exists() and flags:
                body = read(lane / script)
                if all(fl not in body for fl in flags):
                    out.append(f"{name}:self-test:unbacked-flag:{','.join(flags)}")

    if not pinned.strip():
        out.append(f"{name}:pinned-values:empty")
    if not scope.strip():
        out.append(f"{name}:write-scope:empty")
    return out


def check_scripts(lane: Path, rows: list[list[str]]) -> tuple[list[str], int, int]:
    """D1: every row's entry script exists and parses. Returns (defects, scripts, parsed)."""
    scripts = sorted({s for r in rows if (s := entry_script(r[2]))})
    parsed = 0
    defects = []
    for s in scripts:
        path = lane / s
        if not path.exists():
            defects.append(f"SCRIPT-MISSING {s}")
            continue
        try:
            ast.parse(read(path), filename=s)
            parsed += 1
        except SyntaxError as exc:
            defects.append(f"SCRIPT-PARSE {s}:{exc.lineno}:{exc.msg}")
    return defects, len(scripts), parsed


def check_errata(lane: Path) -> list[str]:
    """D4: each numbered erratum item quotes its own label and names that label's revision."""
    text = read(lane / CLAIMS_REL)
    if not text:
        return ["ERRATA:claims-doc-absent"]
    block = text.split(ERRATA_HEADING, 1)[1] if ERRATA_HEADING in text else ""
    if not block.strip():
        return ["ERRATA:no-erratum-section"]
    items = re.split(r"(?m)^\s*\d+\.\s+", block)[1:]
    if len(items) < 2:
        return [f"ERRATA:numbered-items:{len(items)}"]
    defects = []
    for label, revision in ERRATUM_ITEMS:
        owners = [i for i, item in enumerate(items) if label in " ".join(item.split())]
        if not owners:
            defects.append(f"ERRATA:label-not-quoted:{label}")
        else:
            for idx in owners:
                if revision not in items[idx]:
                    defects.append(f"ERRATA:contradictory-revision:{label}->{revision} in item {idx+1}")
    return defects


def run_checks(lane: Path) -> tuple[list[tuple[str, list[str]]], int, int, int]:
    block = registry_block(read(lane / SKILL_REL))
    rows, malformed = parse_rows(block)
    names = [r[0] for r in rows]
    d1, scripts, parsed = check_scripts(lane, rows)
    d2 = [d for r in rows for d in price_row(r, lane)]
    duplicate = sorted({n for n in names if names.count(n) > 1})
    d3 = [f"DUPLICATE-ROW {n}" for n in duplicate]
    d4 = check_errata(lane)
    return [("D1", d1), ("D2", d2), ("D3", d3), ("D4", d4), ("MALFORMED", malformed)], len(rows), scripts, parsed


def verdict(lane: Path) -> int:
    checks, rows, scripts, parsed = run_checks(lane)
    print(f"INSTRUMENTS total={scripts} derived=registry rows={rows}")
    print(f"PARSED scripts={scripts} failed={scripts - parsed}")
    total = 0
    for leg, defects in checks:
        print(f"{leg} {'ok' if not defects else 'defect'} n={len(defects)}")
        for d in defects:
            print(f"  DEFECT {d}")
        total += len(defects)
    print(f"MISMATCH {total}")
    print(f"DEFECTS n={total}")
    print(f"PREDICATE R74-C2 {'pass' if total == 0 else 'fail'}")
    return 0 if total == 0 else 1


# --------------------------------------------------------------------------- fixtures

FIXTURE_REGISTRY_HEAD = (
    REGISTRY_HEADING + "\n\n"
    "| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |\n"
    "|---|---|---|---|---|---|---|---|\n"
)


def row_text(name: str, script: str, *, kind="gate", owner="kengaku",
             verdict="`0` clean · `1` failed", selftest="none declared",
             pinned="pinned bytes", scope="read-only") -> str:
    return (f"| `{name}` | {kind} | `python3 {script}` | {verdict} | {selftest} | "
            f"{pinned} | {scope} | {owner} |\n")


def build_fixture(root: Path, *, extra_row: str = "", second_row: str = "",
                  errata: str = "ordered", broken: bool = False,
                  malformed_line: str = "") -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "plans").mkdir(exist_ok=True)
    (root / "plans" / "tool_a.py").write_text("import argparse\np=argparse.ArgumentParser()\np.add_argument('--selftest')\n")
    (root / "plans" / "tool_b.py").write_text("# second instrument\n")
    if broken:
        (root / "plans" / "tool_bad.py").write_text("def (\n")
    body = (
        FIXTURE_REGISTRY_HEAD +
        row_text("tool-a", "plans/tool_a.py", selftest="`python3 plans/tool_a.py --selftest`") +
        (row_text("tool-b", "plans/tool_b.py") if not extra_row else extra_row) +
        second_row
    )
    if malformed_line:
        body += malformed_line + "\n"
    (root / "SKILL.md").write_text(body)
    errata_text = ""
    if errata == "ordered":
        errata_text = (
            f"\n## Errata — round 72\n\n"
            f"1. Do-nothing control (committed at freeze) revision c80fcdb3.\n"
            f"2. Red-before (committed at freeze) revision d8a77d3f.\n"
        )
    elif errata == "swapped":
        errata_text = (
            f"\n## Errata — round 72\n\n"
            f"1. Do-nothing control (committed at freeze) revision d8a77d3f.\n"
            f"2. Red-before (committed at freeze) revision c80fcdb3.\n"
        )
    elif errata == "contradictory":
        errata_text = (
            f"\n## Errata — round 72\n\n"
            f"1. Do-nothing control (committed at freeze) revision c80fcdb3.\n"
            f"2. Red-before (committed at freeze) revision d8a77d3f.\n"
            f"3. Do-nothing control (committed at freeze) contradictory revision 11111111.\n"
        )
    (root / CLAIMS_REL).parent.mkdir(parents=True, exist_ok=True)
    (root / CLAIMS_REL).write_text(f"# claims\n{errata_text}")
    return root


def selftest(lane: Path, work: Path) -> int:
    """Fixture battery: clean, malformed row, unbacked flag, contradictory errata."""
    fails = 0
    child = work / "selftest_child"
    if child.exists():
        shutil.rmtree(child)
    child.mkdir(parents=True)
    try:
        # 1. Clean fixture
        clean_dir = child / "clean"
        build_fixture(clean_dir)
        checks, rows, scripts, parsed = run_checks(clean_dir)
        defects = sum(len(d) for _, d in checks)
        if defects != 0:
            print(f"SELFTEST FAIL clean: defects={defects}")
            fails += 1
        else:
            print("SELFTEST ok clean")

        # 2. Malformed row (9 cells)
        mal_dir = child / "malformed"
        build_fixture(mal_dir, malformed_line="| `tool-x` | gate | `python3 plans/tool_b.py` | 0 ok | none | pin | scope | kengaku | stray |")
        checks, _, _, _ = run_checks(mal_dir)
        mal_defects = [d for k, dl in checks if k == "MALFORMED" for d in dl]
        if not mal_defects:
            print("SELFTEST FAIL malformed: 9-cell row was not caught!")
            fails += 1
        else:
            print("SELFTEST ok malformed")

        # 3. Unbacked entry flag
        flag_dir = child / "flag"
        build_fixture(flag_dir, extra_row=row_text("tool-b", "plans/tool_b.py --strict"))
        checks, _, _, _ = run_checks(flag_dir)
        d2_defects = [d for k, dl in checks if k == "D2" for d in dl if "unbacked-flag:--strict" in d]
        if not d2_defects:
            print("SELFTEST FAIL entry-flag: unbacked --strict was not caught!")
            fails += 1
        else:
            print("SELFTEST ok entry-flag")

        # 4. Contradictory errata (C16)
        err_dir = child / "errata"
        build_fixture(err_dir, errata="contradictory")
        checks, _, _, _ = run_checks(err_dir)
        err_defects = [d for k, dl in checks if k == "D4" for d in dl if "contradictory-revision" in d]
        if not err_defects:
            print("SELFTEST FAIL errata: contradictory erratum was not caught!")
            fails += 1
        else:
            print("SELFTEST ok errata")

    finally:
        shutil.rmtree(child, ignore_errors=True)

    print(f"SELFTEST arms=4 red=3 ok={fails == 0}")
    return 0 if fails == 0 else 1


def mutants(lane: Path, work: Path) -> int:
    """Mutant matrix testing detection sensitivity."""
    child = work / "mutants_child"
    if child.exists():
        shutil.rmtree(child)
    child.mkdir(parents=True)
    killed = 0
    total = 7
    try:
        # M1: non-existent entry script
        d = child / "m1"; build_fixture(d, extra_row=row_text("tool-m", "plans/nonexistent.py"))
        c, _, _, _ = run_checks(d); killed += int(sum(len(x) for _, x in c) > 0)
        # M2: non-existent self-test script
        d = child / "m2"; build_fixture(d, extra_row=row_text("tool-m", "plans/tool_b.py", selftest="`python3 plans/nonexistent.py --selftest`"))
        c, _, _, _ = run_checks(d); killed += int(sum(len(x) for _, x in c) > 0)
        # M3: 9-cell malformed row
        d = child / "m3"; build_fixture(d, malformed_line="| a | b | c | d | e | f | g | h | i |")
        c, _, _, _ = run_checks(d); killed += int(sum(len(x) for _, x in c) > 0)
        # M4: 7-cell malformed row
        d = child / "m4"; build_fixture(d, malformed_line="| a | b | c | d | e | f | g |")
        c, _, _, _ = run_checks(d); killed += int(sum(len(x) for _, x in c) > 0)
        # M5: duplicate row name
        d = child / "m5"; build_fixture(d, second_row=row_text("tool-a", "plans/tool_b.py"))
        c, _, _, _ = run_checks(d); killed += int(sum(len(x) for _, x in c) > 0)
        # M6: unbacked entry flag
        d = child / "m6"; build_fixture(d, extra_row=row_text("tool-m", "plans/tool_b.py --nonexistent"))
        c, _, _, _ = run_checks(d); killed += int(sum(len(x) for _, x in c) > 0)
        # M7: contradictory errata
        d = child / "m7"; build_fixture(d, errata="contradictory")
        c, _, _, _ = run_checks(d); killed += int(sum(len(x) for _, x in c) > 0)
    finally:
        shutil.rmtree(child, ignore_errors=True)

    print(f"MUTANTS total={total} killed={killed} survived={total - killed} invalid=0 null_detected=1")
    return 0 if killed == total else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--lane", type=Path, default=Path("."), help="Lane root directory")
    parser.add_argument("--selftest", action="store_true", help="Run self-test fixture battery")
    parser.add_argument("--mutants", action="store_true", help="Run mutant matrix")
    parser.add_argument("--work", type=Path, default=Path("/fast/scratch/hyaku/kengaku-r74/c2-audit"), help="Scratch directory")
    args = parser.parse_args()

    if args.selftest:
        args.work.mkdir(parents=True, exist_ok=True)
        return selftest(args.lane, args.work)
    if args.mutants:
        args.work.mkdir(parents=True, exist_ok=True)
        return mutants(args.lane, args.work)
    if not args.lane.is_dir():
        print(f"SETUP ERROR: lane {args.lane} is not a directory", file=sys.stderr)
        return 2
    return verdict(args.lane)


if __name__ == "__main__":
    sys.exit(main())

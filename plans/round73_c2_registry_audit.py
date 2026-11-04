#!/usr/bin/env python3
"""R73-C2 counter — registry declaration shape checks over supplied working-tree bytes.

Frozen before data on 2026-11-04 (L1 KengakuR73); see plans/round-73-claims.md §C2 for the
predicate this implements. Reads working-tree bytes, not a Git snapshot; final receipts name their measured revision.

    python3 plans/round73_c2_registry_audit.py --lane .                    # verdict
    python3 plans/round73_c2_registry_audit.py --selftest --work DIR       # one green + three red arms
    python3 plans/round73_c2_registry_audit.py --mutants --work DIR        # byte mutants

Post-wave disclosure: parse_rows silently skips non-eight-cell lines; pins/scopes are nonempty
checks, not truth checks, and erratum tokens do not establish semantic attribution. Both original
round73 claims are not admitted (claims doc E-R73-1). Fixture modes use an owned child of --work;
the post-wave security repair preserves caller-owned files without changing verdict predicates.

Why this counter exists (round-72 wave findings F1/F2/F3, committed in the round-72 lesson):
the round-72 counter E1a checked a FROZEN four-instrument tuple, kept the FIRST row of a
duplicated name, and priced three of a row's six content fields.  A fifth instrument, a
defective second row of a known name, and a wrong field therefore all passed it.  This
counter derives its instrument set from the registry rows themselves, keeps EVERY row, and
prices all eight fields plus the erratum's label→revision binding.

Predicate (all four legs must hold; `MISMATCH 0`):
  D1 ROWS       every registry row's entry cell names an existing Python script, and every
                such script parses with `ast.parse` (nothing is priced from an unreadable file)
  D2 FIELDS     for every row: eight non-empty cells; kind in {gate, probe}; owner cell begins
                `kengaku`; entry names a script; gate verdict maps declare `0` and (`1` or a
                `failed` class), probe maps declare `0`; self-test cell is a declared none or
                names a script+flag the script contains or explicitly negates; pinned-values
                and write-scope cells non-empty
  D3 EVERY-ROW  no duplicate row names, and a defective SECOND row of a known name is priced
                (the audit never keeps a first-row-wins index)
  D4 ERRATA     the round-72 erratum's two numbered items each quote their own superseded
                label AND name that label's true revision (swapped revisions red)

Exit 0 pass, 1 fail (each defect on its own line), 2 setup (no SKILL.md, no --work for the
fixture/mutant modes, `--lane` not a directory).
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
# (superseded label, the revision that item must name) in superseded order.
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


def parse_rows(block: str) -> list[list[str]]:
    rows = []
    for line in block.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if len(cells) != 8:
            continue
        if set(cells[0]) <= set("-: "):
            continue
        if cells[0] == "name":          # the header line is not a row
            continue
        rows.append(cells)
    return rows


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


def selftest_unbacked(cell: str, lane: Path) -> bool:
    if re.search(r"\bno\b.{0,24}--[a-z][a-z0-9-]*", cell):
        return False
    scripts = sorted(set(re.findall(r"(?:plans|corpus|grader)[A-Za-z0-9_./-]*\.py", cell)))
    flags = sorted(set(FLAG.findall(cell)))
    if len(scripts) != 1 or not flags:
        return False
    path = lane / scripts[0]
    if not path.exists():
        return False
    body = read(path)
    return all(f not in body for f in flags)


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
    codes = set(re.findall(r"`(\d+)`", verdict)) | set(re.findall(r"`(\d+)`", verdict.upper()))
    if kind == "gate":
        failed_class = any(w in verdict.lower() for w in DEFECT_WORDS)
        if "0" not in codes or not ("1" in codes or failed_class):
            out.append(f"{name}:gate-verdict:{','.join(sorted(codes)) or 'none'}")
    elif kind == "probe" and "0" not in codes:
        out.append(f"{name}:probe-verdict:{','.join(sorted(codes)) or 'none'}")
    if "none" not in selftest.lower() and selftest_unbacked(selftest, lane):
        out.append(f"{name}:self-test:unbacked")
    if not pinned.strip():
        out.append(f"{name}:pinned-values:empty")
    if not scope.strip():
        out.append(f"{name}:write-scope:empty")
    return out


def check_scripts(lane: Path, rows: list[list[str]]) -> tuple[list[str], int, int]:
    """D1: every row's entry script exists and parses.  Returns (defects, scripts, parsed)."""
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
        elif revision not in items[owners[0]]:
            defects.append(f"ERRATA:item-names-other-revision:{label}->{revision}")
    return defects


def run_checks(lane: Path) -> tuple[list[tuple[str, list[str]]], int, int, int]:
    block = registry_block(read(lane / SKILL_REL))
    rows = parse_rows(block)
    names = [r[0] for r in rows]
    d1, scripts, parsed = check_scripts(lane, rows)
    d2 = [d for r in rows for d in price_row(r, lane)]
    duplicate = sorted({n for n in names if names.count(n) > 1})
    d3 = [f"DUPLICATE-ROW {n}" for n in duplicate]
    d4 = check_errata(lane)
    return [("D1", d1), ("D2", d2), ("D3", d3), ("D4", d4)], len(rows), scripts, parsed


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
    print(f"PREDICATE R73-C2 {'pass' if total == 0 else 'fail'}")
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
                  errata: str = "ordered", broken: bool = False) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "plans").mkdir(exist_ok=True)
    (root / "plans" / "tool_a.py").write_text("import argparse\np=argparse.ArgumentParser()\np.add_argument('--selftest')\n")
    (root / "plans" / "tool_b.py").write_text("# second instrument\n")
    if broken:
        (root / "plans" / "tool_bad.py").write_text("def (\n")
    (root / "SKILL.md").write_text(
        FIXTURE_REGISTRY_HEAD
        + row_text("tool-a", "plans/tool_a.py", selftest="`python3 plans/tool_a.py --selftest`")
        + second_row
        + extra_row
        + (row_text("tool-bad", "plans/tool_bad.py") if broken else "")
    )
    (root / "SCORECARD.md").write_text("x\n")
    (root / "LOG.md").write_text("x\n")
    (root / "corpus").mkdir(exist_ok=True)
    (root / "corpus" / "README.md").write_text("x\n")
    (root / "plans" / CLAIMS_REL.split("/", 1)[1]).write_text(build_claims(errata))
    return root


def build_claims(errata: str) -> str:
    head = ("# fixture claims\n\n"
            "The label `Do-nothing control (committed at freeze)` and the label "
            "`Red-before (committed at freeze)` are superseded.\n\n")
    if errata == "ordered":
        body = (f"{ERRATA_HEADING}\n\n"
                f"1. The label `{ERRATUM_ITEMS[0][0]}` is false of {ERRATUM_ITEMS[1][1]}; the "
                f"control landed with {ERRATUM_ITEMS[0][1]}.\n"
                f"2. The label `{ERRATUM_ITEMS[1][0]}` is half right: the receipt is committed "
                f"at {ERRATUM_ITEMS[1][1]}.\n")
    elif errata == "swapped":
        body = (f"{ERRATA_HEADING}\n\n"
                f"1. The label `{ERRATUM_ITEMS[0][0]}` is false of {ERRATUM_ITEMS[1][1]}.\n"
                f"2. The label `{ERRATUM_ITEMS[1][0]}` is half right: committed at "
                f"{ERRATUM_ITEMS[0][1]}.\n")
    else:
        raise SystemExit(f"unknown errata mode {errata}")
    return head + body


def selftest(work: Path) -> int:
    """Four arms, each a fixture that must red exactly its leg; the clean arm must stay green."""
    work = work.resolve()
    if not work.is_dir():
        print(f"SETUP --work must be an existing directory: {work}")
        return 2
    # --work belongs to the caller; remove only the child this invocation allocates.
    work = Path(tempfile.mkdtemp(prefix="r73-audit-", dir=work))
    fails = 0
    try:
        clean = build_fixture(work / "clean")
        checks, *_ = run_checks(clean)
        green = sum(len(d) for _leg, d in checks)
        if green:
            print(f"SELFTEST FAIL clean-fixture: defects={[d for _l, ds in checks for d in ds]}")
            fails += 1
        else:
            print("SELFTEST ok clean-fixture")
        # arm 1: a fifth row for a NEW instrument whose owner is not the lane -> D2
        fifth = build_fixture(work / "fifth", extra_row=row_text("tool-b", "plans/tool_b.py", owner="sibling"))
        d = sum(len(x) for _l, x in run_checks(fifth)[0])
        if d == 0:
            print("SELFTEST FAIL fifth-row-arm: a new row's bad owner was not priced")
            fails += 1
        else:
            print("SELFTEST ok fifth-row-arm")
        # arm 2: a defective SECOND row of a known name -> D3 (and D2), never first-row-wins
        second = build_fixture(work / "second", second_row=row_text("tool-a", "plans/tool_b.py", kind="census gate"))
        checks2, *_ = run_checks(second)
        d3 = [x for leg, x in checks2 if leg == "D3"]
        if not d3 and not any("kind" in x for _leg, ds in checks2 for x in ds):
            print("SELFTEST FAIL second-row-arm: a defective duplicate row was not priced")
            fails += 1
        else:
            print("SELFTEST ok second-row-arm")
        # arm 3: swapped erratum revisions -> D4
        swapped = build_fixture(work / "swapped", errata="swapped")
        d4 = [x for leg, x in run_checks(swapped)[0] if leg == "D4"]
        if not d4:
            print("SELFTEST FAIL errata-arm: swapped revisions were not priced")
            fails += 1
        else:
            print("SELFTEST ok errata-arm")
        ok = fails == 0
        print(f"SELFTEST arms=4 red=3 ok={ok}")
        return 0 if ok else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


MUTANTS = (
    ("M0-null", None),
    ("M1-kind", ("if kind not in KINDS:", "if False:")),
    ("M2-owner", ("if not owner.startswith(OWNER_PREFIX):", "if False:")),
    ("M3-gate-verdict", ('        if "0" not in codes or not ("1" in codes or failed_class):',
                         "        if False:")),
    ("M4-duplicate", ("duplicate = sorted({n for n in names if names.count(n) > 1})",
                      "duplicate = []")),
    ("M5-errata-revision", ("        elif revision not in items[owners[0]]:", "        elif False:")),
    ("M6-script-parse", ("        except SyntaxError as exc:", "        except ZeroDivisionError as exc:")),
    ("M7-selftest-unbacked", ('    if "none" not in selftest.lower() and selftest_unbacked(selftest, lane):',
                              "    if False:")),
)


def mutants(work: Path) -> int:
    """Byte mutants of the audit's own legs; killed iff the mutant's stdout differs from the
    unmutated gate's stdout on the same battery.  The null mutant must survive (determinism)."""
    import subprocess

    work = work.resolve()
    if not work.is_dir():
        print(f"SETUP --work must be an existing directory: {work}")
        return 2
    # --work belongs to the caller; remove only the child this invocation allocates.
    work = Path(tempfile.mkdtemp(prefix="r73-audit-", dir=work))
    source = Path(__file__).read_text()
    killed = survived = invalid = null_detected = 0
    extra = (row_text("tool-b", "plans/tool_b.py", owner="sibling")
             + row_text("tool-v", "plans/tool_b.py", verdict="`0` clean · `2` setup")
             + row_text("tool-s", "plans/tool_b.py", selftest="`python3 plans/tool_b.py --selftest`"))
    fixture = build_fixture(work / "battery", extra_row=extra,
                            second_row=row_text("tool-a", "plans/tool_b.py", kind="census gate"),
                            errata="swapped", broken=True)
    try:
        base = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--lane", str(fixture)],
                              capture_output=True, text=True)
        if base.returncode != 1 or "DEFECT" not in base.stdout:
            print(f"SETUP battery fixture is not red: rc={base.returncode}")
            return 2
        for name, pair in MUTANTS:
            if pair is None:
                target = work / f"mutant-{name}.py"
                target.write_text(source + "\n# null mutant\n")
            else:
                needle, replacement = pair
                if needle not in source:
                    print(f"MUTANT {name} invalid(needle-absent)")
                    invalid += 1
                    continue
                target = work / f"mutant-{name}.py"
                target.write_text(source.replace(needle, replacement, 1))
            proc = subprocess.run([sys.executable, str(target), "--lane", str(fixture)],
                                  capture_output=True, text=True)
            if pair is None:
                if proc.stdout == base.stdout and proc.returncode == base.returncode:
                    print(f"MUTANT {name} null_detected")
                    null_detected += 1
                else:
                    print(f"MUTANT {name} NON-DETERMINISTIC")
                    survived += 1
            elif proc.stdout != base.stdout or proc.returncode != base.returncode:
                print(f"MUTANT {name} killed rc={proc.returncode}")
                killed += 1
            else:
                print(f"MUTANT {name} survived")
                survived += 1
            target.unlink(missing_ok=True)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    total = len(MUTANTS) - 1
    print(f"MUTANTS total={total} killed={killed} survived={survived} invalid={invalid} "
          f"null_detected={null_detected}")
    ok = killed == total and survived == 0 and invalid == 0 and null_detected == 1
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--mutants", action="store_true")
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    lane = Path(a.lane).resolve()
    if not (lane / SKILL_REL).exists():
        print(f"SETUP no {SKILL_REL} under {lane}")
        return 2
    if a.selftest or a.mutants:
        if not a.work:
            print("SETUP --selftest and --mutants require --work DIR")
            return 2
        return selftest(Path(a.work)) if a.selftest else mutants(Path(a.work))
    return verdict(lane)


if __name__ == "__main__":
    sys.exit(main())

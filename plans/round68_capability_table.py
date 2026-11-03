#!/usr/bin/env python3
"""Round 68, A3: the capability-table completeness gate.

Frozen predicate (plans/round-68-claims.md, Amendment A3):

  `python3 plans/round68_capability_table.py --lane .` exits 0 and prints
  `PREDICATE R68-A3 pass` with `MISMATCH n=0` iff every capability the lane's
  SCORECARD round sections (rounds 64-68) declare as entered carries exactly one
  row in the `## Capabilities` table, with the declaring round named in its
  first-working-round cell and a backticked evidence path that exists.

  Mismatch classes: T1 a declared capability has no row; T2 the row's
  first-working-round cell does not name the declaring round; T3 the row's
  evidence cell carries no backticked path, or the path does not exist;
  T4 the table carries a duplicate capability name.

`--selftest --work <dir>` proves each class can fail on its own fixture:
  s1 the pre-fix table (four capabilities absent) -> T1 x4
  s2 a table whose network-service row names round 99 -> T2
  s3 a table whose sqlite row evidence path is absent -> T3
  s4 a table with the network-service row duplicated -> T4
  s5 the compliant table -> pass

Exit 0 = pass; 1 = mismatches; 2 = could-not-evaluate.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

# Frozen before data: the capabilities the lane's round sections 64-68 declare
# as entered, with the round that first demonstrated each.
DECLARED = {
    "offline-network-service-grader-probe": "64",
    "offline-db-state-grader-probe": "65",
    "offline-torch-tensor-parallel-grader-probe": "66",
    "offline-torch-pipeline-parallel-grader-probe": "67",
}

BACKTICK_RE = re.compile(r"`([^`]+)`")
PATH_RE = re.compile(r"(?:plans|corpus)/[A-Za-z0-9_./-]+")


def table_rows(scorecard: str) -> list[list[str]]:
    lines = scorecard.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == "## Capabilities")
    except StopIteration:
        return []
    rows: list[list[str]] = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue
        if cells and cells[0].lower() == "capability":
            continue
        rows.append(cells)
    return rows


def check(scorecard: str, lane: Path) -> list[tuple[str, list[str]]]:
    """Return one (class, findings) pair per check; findings are row-level."""
    rows = table_rows(scorecard)
    names = [r[0] for r in rows if r]

    missing = [f"T1 {name}: no row" for name in DECLARED if name not in names]

    bad_round = []
    bad_evidence = []
    for name, rnd in DECLARED.items():
        hits = [r for r in rows if r and r[0] == name]
        if not hits:
            continue
        row = hits[0]
        first_round = row[3] if len(row) > 3 else ""
        if rnd not in first_round:
            bad_round.append(f"T2 {name}: want round {rnd}, got {first_round!r}")
        evidence = row[2] if len(row) > 2 else ""
        # A backticked evidence cell may carry a whole command; the path inside it
        # is the evidence pointer the frozen sentence names.
        paths = []
        for tok in BACKTICK_RE.findall(evidence):
            paths.extend(PATH_RE.findall(tok))
        if not paths:
            bad_evidence.append(f"T3 {name}: no backticked evidence path")
        else:
            absent = [p for p in paths if not (lane / p).exists()]
            if absent:
                bad_evidence.append(f"T3 {name}: absent evidence path {absent}")

    seen = set()
    dups = []
    for name in names:
        if name in seen:
            dups.append(f"T4 {name}: duplicate row")
        seen.add(name)
    return [("T1", missing), ("T2", bad_round), ("T3", bad_evidence), ("T4", dups)]


def compliant_table() -> str:
    lines = ["## Capabilities", "", "| Capability | What it can now do | Evidence pointer | First-working round |", "|---|---|---|---|"]
    for name, rnd in DECLARED.items():
        ev = {
            "offline-network-service-grader-probe": "`plans/round68_c1_pypi_finish.py`",
            "offline-db-state-grader-probe": "`plans/round65_c1_sqlite_probe.py`",
            "offline-torch-tensor-parallel-grader-probe": "`plans/round66_c1_tensor_probe.py`",
            "offline-torch-pipeline-parallel-grader-probe": "`plans/round67_c1_pipeline_probe.py`",
        }[name]
        lines.append(f"| {name} | fixture | {ev} | {rnd} |")
    lines.append("")
    return "\n".join(lines)


def selftest(lane: Path, work: Path) -> int:
    work.mkdir(parents=True, exist_ok=True)
    good = compliant_table()
    fixtures = [
        ("s5-compliant", good, 0),
        ("s1-pre-fix", good.replace(
            "| offline-network-service-grader-probe | fixture | `plans/round68_c1_pypi_finish.py` | 64 |\n"
            "| offline-db-state-grader-probe | fixture | `plans/round65_c1_sqlite_probe.py` | 65 |\n"
            "| offline-torch-tensor-parallel-grader-probe | fixture | `plans/round66_c1_tensor_probe.py` | 66 |\n"
            "| offline-torch-pipeline-parallel-grader-probe | fixture | `plans/round67_c1_pipeline_probe.py` | 67 |\n", ""), 4),
        ("s2-wrong-round", good.replace("| 64 |", "| 99 |"), 1),
        ("s3-absent-evidence", good.replace("`plans/round65_c1_sqlite_probe.py`", "`plans/absent_probe.py`"), 1),
        ("s4-duplicate", good + "| offline-network-service-grader-probe | fixture | `plans/round68_c1_pypi_finish.py` | 64 |\n", 1),
    ]
    refused = 0
    green_ok = 0
    for name, text, want in fixtures:
        path = work / f"{name}.md"
        path.write_text(text, encoding="utf-8")
        results = check(text, lane)
        findings = [item for _, items in results for item in items]
        got = len(findings)
        print(f"SELFTEST {name} want={want} got={got} findings={findings or 'none'}")
        if want and got == want:
            refused += 1
        if want == 0 and got == 0:
            green_ok += 1
    ok = refused == len(fixtures) - 1 and green_ok == 1
    print(f"SELFTEST n={len(fixtures)} red-refused={refused} green-ok={green_ok}")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Round 68, A3: capability-table completeness gate.")
    ap.add_argument("--lane", default=os.environ.get("UFO_LANE_ROOT", str(Path(__file__).resolve().parent.parent)))
    ap.add_argument("--scorecard", default=None)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--work", default=None)
    args = ap.parse_args(argv)
    lane = Path(args.lane).resolve()
    scorecard_path = Path(args.scorecard) if args.scorecard else lane / "SCORECARD.md"
    if args.selftest:
        work = Path(args.work) if args.work else Path(os.environ.get("TMPDIR", "/tmp")) / "r68-a3-selftest"
        try:
            return selftest(lane, work)
        except OSError as exc:
            print(f"SELFTEST could-not-evaluate {exc}")
            return 2
    try:
        scorecard = scorecard_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"SETUP could-not-evaluate {exc}")
        return 2
    results = check(scorecard, lane)
    mismatches = 0
    for code, findings in results:
        print(f"{code} {'ok' if not findings else 'mismatch'} n={len(findings)}")
        for item in findings:
            print(f"  {item}")
        mismatches += len(findings)
    print(f"MISMATCH n={mismatches}")
    print(f"PREDICATE R68-A3 {'pass' if mismatches == 0 else 'fail'}")
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

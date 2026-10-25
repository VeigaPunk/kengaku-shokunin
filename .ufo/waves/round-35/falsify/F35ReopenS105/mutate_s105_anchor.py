#!/usr/bin/env python3
"""F35ReopenS105 — mutation probe: does any instrument check the S105 anchor cell?

Read-only against the lane; writes only inside the fixture clone the caller names.
For each mutant of the S105 anchor cell we run BOTH instruments that claim to gate it:
  1. plans/round35_c1_verify.py   (the frozen C1 predicate: V2 rows, V3 located quotes)
  2. plans/sources_adopt.py --quote-file --artifact   (the lane's canonical anchor gate,
     whose `words()` is len(text.split()) — the same counter round30_defects.py uses)

A mutant that still passes BOTH instruments demonstrates the blind spot. A mutant that is
caught demonstrates the instrument's reach.

Usage:
  python3 mutate_s105_anchor.py --lane <fixture-lane> --fleet <fleet-root> --work <scratch>
"""
import argparse
import pathlib
import subprocess
import sys

ANCHOR = ('tests/test_outputs.py:42 "assert flag_idx < donor_idx < dhfr_idx < acceptor_idx '
          '< snap_idx, (" (9 words)')

MUTANTS = {
    "baseline": ANCHOR,
    "A_wrong_line_and_wrong_quote":
        'tests/test_outputs.py:71 "assert 15 <= gc <= 35, (" (7 words)',
    "B_right_quote_wrong_line":
        'tests/test_outputs.py:999 "assert flag_idx < donor_idx < dhfr_idx < acceptor_idx '
        '< snap_idx, (" (9 words)',
    "C_right_quote_right_line_wrong_count":
        'tests/test_outputs.py:42 "assert flag_idx < donor_idx < dhfr_idx < acceptor_idx '
        '< snap_idx, (" (99 words)',
}


def restore(lane, tip):
    subprocess.run(["git", "-C", str(lane), "checkout", "-q", tip, "--", "corpus/SOURCES.md"],
                   check=True)


def run_c1(lane, fleet):
    r = subprocess.run([sys.executable, "plans/round35_c1_verify.py", "--lane", str(lane),
                        "--fleet", str(fleet)], cwd=lane, capture_output=True, text=True)
    out = r.stdout.strip().splitlines()
    summary = next((l for l in out if l.startswith("checks=")), "checks=?")
    pred = next((l for l in out if l.startswith("PREDICATE")), "PREDICATE=?")
    return r.returncode, f"{summary} | {pred}"


def run_gate(lane, rows_file, artifact):
    r = subprocess.run([sys.executable, "plans/sources_adopt.py", "--quote-file", str(rows_file),
                        "--artifact", str(artifact)], cwd=lane, capture_output=True, text=True)
    line = next((l for l in r.stdout.splitlines() if l.strip().startswith("ok ")
                 or l.strip().startswith("no ")), r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "")
    return r.returncode, line.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--fleet", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--tip", default="dfee6fff631ebc5f623ba4506e5c7992a215401c")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    rows_file = work / "rows.txt"
    src = lane / "corpus/SOURCES.md"

    print(f"anchor cell under test:\n  {ANCHOR}\n")
    print(f"{'mutant':42s} {'C1 counter':38s} {'sources_adopt gate'}")
    print("-" * 120)
    for name, anchor in MUTANTS.items():
        restore(lane, a.tip)
        text = src.read_text()
        assert ANCHOR in text, "anchor cell not found in SOURCES.md"
        src.write_text(text.replace(ANCHOR, anchor))
        row = [l for l in src.read_text().splitlines() if l.startswith("| S105 ")][0]
        rows_file.write_text(row)
        rc1, c1 = run_c1(lane, a.fleet)
        rg, g = run_gate(lane, rows_file, "corpus/evidence/round35/tb2-eval/test_outputs.py")
        print(f"{name:42s} {c1:38s} rc={rg} {g}")
    restore(lane, a.tip)
    rc1, c1 = run_c1(lane, a.fleet)
    print(f"\nrestored baseline: {c1}")


if __name__ == "__main__":
    main()

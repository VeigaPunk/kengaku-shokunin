#!/usr/bin/env python3
"""Dangling evidence-pointer checker for a filed round report (round 87; mined mistake reference-drift).

A pointer is a backticked repo-relative path beginning with plans/, corpus/, scripts/, .ufo/ or considerthese/.
A pointer resolves when the path exists in the lane worktree, or when some ref of the lane contains it
(`git log --all -- <path>` non-empty). Paths with placeholders (`*`, `<`, `{`, `…`, `|`) are skipped.

Prints `DEFECT pointer <path> (report line <n>)` for each unresolved pointer, then
`POINTERS n=<n> missing=<n>`. Exit 0 when nothing is missing, 1 otherwise, 2 when the report is unreadable.

Red-before evidence (committed in .ufo/waves/round-87/L1/paths-red.txt): run on the round-86 report,
which cites `.ufo/waves/round-86/L1/outside-gates.txt` (exists in no ref) -> exit 1.

Usage: python3 plans/round87_report_paths.py --lane <repo> --report <report.md>
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

POINTER = re.compile(r"`((?:plans|corpus|scripts|\.ufo|considerthese)/[^`\s]+)`")
SKIP = ("*", "<", "{", "…", "|", "...")


def resolves(lane: Path, path: str) -> bool:
    if (lane / path).exists():
        return True
    proc = subprocess.run(["git", "-C", str(lane), "log", "--all", "--oneline", "--", path],
                          capture_output=True, text=True, timeout=120)
    return proc.returncode == 0 and bool(proc.stdout.strip())


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=".")
    parser.add_argument("--report", required=True)
    args = parser.parse_args(argv)
    lane = Path(args.lane).resolve()
    try:
        lines = Path(args.report).read_text(encoding="utf-8").splitlines()
    except OSError as error:
        print(f"DEFECT SETUP {error}")
        return 2
    total = 0
    missing = 0
    for number, line in enumerate(lines, start=1):
        for match in POINTER.finditer(line):
            path = match.group(1).split(":")[0].rstrip(".,;)")
            if any(token in path for token in SKIP):
                continue
            total += 1
            if not resolves(lane, path):
                missing += 1
                print(f"DEFECT pointer {path} (report line {number})")
    print(f"POINTERS n={total} missing={missing}")
    return 0 if missing == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

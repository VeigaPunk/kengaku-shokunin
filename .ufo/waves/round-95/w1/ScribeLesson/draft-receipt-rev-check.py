#!/usr/bin/env python3
"""DRAFT for the L1 — Q77's executable half.

A measurement receipt that stamps a revision must stamp one that resolves as a
commit in the lane it claims to measure. A receipt that stamps no revision is
reported as UNSTAMPED (informational: it asserts no revision, so it cannot
misattribute a measurement; it is simply not evidence about a revision).

usage: draft-receipt-rev-check.py --lane DIR --receipt FILE [--receipt FILE ...]
       draft-receipt-rev-check.py --lane DIR --scan DIR

exit 0 = every receipt offered as evidence names a lane revision (or names none)
exit 1 = at least one receipt names a revision that is not an object of the lane
exit 2 = setup (no such file, unreadable receipt, no receipt named)
"""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

# A receipt stamps its revision as "HEAD <40 hex>" (sometimes "REV <40 hex>").
STAMP = re.compile(r"\b(?:HEAD|REV|LANE_TIP)\s+([0-9a-f]{40})\b")


def lane_has(lane: pathlib.Path, rev: str) -> bool:
    p = subprocess.run(["git", "-C", str(lane), "cat-file", "-e", f"{rev}^{{commit}}"],
                       capture_output=True)
    return p.returncode == 0


def check(lane: pathlib.Path, path: pathlib.Path) -> str:
    """-> 'ok' | 'bad' | 'unstamped'"""
    text = path.read_text(encoding="utf-8", errors="replace")
    head = text.split("\n", 1)[0]
    revs = sorted(set(STAMP.findall(head)))
    if not revs:
        print(f"RECEIPT-REV {path} head=- verdict=UNSTAMPED")
        return "unstamped"
    ok = True
    for rev in revs:
        good = lane_has(lane, rev)
        ok = ok and good
        print(f"RECEIPT-REV {path} head={rev} verdict={'IN-LANE' if good else 'NOT-IN-LANE'}")
    return "ok" if ok else "bad"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--receipt", action="append", default=[])
    ap.add_argument("--scan")
    a = ap.parse_args(argv)
    lane = pathlib.Path(a.lane).resolve()
    paths = [pathlib.Path(p) for p in a.receipt]
    if a.scan:
        root = pathlib.Path(a.scan)
        paths += sorted(p for p in root.rglob("*")
                        if p.is_file() and p.suffix in (".txt", ".log"))
    if not paths:
        print("SETUP no receipts named")
        return 2
    tally = {"ok": 0, "bad": 0, "unstamped": 0}
    for p in paths:
        try:
            tally[check(lane, p)] += 1
        except OSError as e:
            print(f"RECEIPT-REV {p} verdict=UNREADABLE ({e})")
            tally["bad"] += 1
    print(f"RECEIPTS total={len(paths)} in-lane={tally['ok']} not-in-lane={tally['bad']} unstamped={tally['unstamped']}")
    if tally["bad"]:
        print("PREDICATE RECEIPT-REV fail")
        return 1
    print("PREDICATE RECEIPT-REV pass")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

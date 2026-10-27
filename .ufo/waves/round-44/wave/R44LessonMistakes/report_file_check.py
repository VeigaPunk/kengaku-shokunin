#!/usr/bin/env python3
"""Every dispatched seat leaves a report file (round-43 closure D3).

Read-only. Usage:
  python3 report_file_check.py --lane <lane> --reports .ufo/waves/round-43/build \
      --results .ufo/waves/round-43/build-results.json
  python3 report_file_check.py --lane <lane> --reports .ufo/waves/round-44/wave \
      --dispatch .ufo/waves/round-44/wave-dispatch.json
Prints `REPORTS seats=<n> files=<m> missing=<names>`; exit 1 when any is missing.
"""
import argparse, json, sys
from pathlib import Path

def names_from(results=None, dispatch=None):
    if results:
        d = json.loads(Path(results).read_text())
        return [r.get("name") or r.get("id") for r in d["results"]]
    d = json.loads(Path(dispatch).read_text())
    return [t["name"] for t in d["taskCall"]["tasks"]]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--reports", required=True)
    ap.add_argument("--results")
    ap.add_argument("--dispatch")
    a = ap.parse_args()
    lane = Path(a.lane).resolve()
    names = names_from(a.results, a.dispatch)
    reports = lane / a.reports
    present = {p.stem for p in reports.glob("*.md")}
    missing = [n for n in names if n not in present]
    print(f"REPORTS seats={len(names)} files={len([n for n in names if n in present])} "
          f"missing={len(missing)}{':' + ','.join(missing) if missing else ''}")
    return 1 if missing else 0

if __name__ == "__main__":
    sys.exit(main())

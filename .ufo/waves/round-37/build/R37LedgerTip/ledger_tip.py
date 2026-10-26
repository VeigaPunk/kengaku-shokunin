#!/usr/bin/env python3
"""Ledger-at-tip re-runner (round 37 wave 1, considerthese/2026-10-25.md proposal 2(a)).

Re-runs EVERY routed-defect row's check at the lane tip, on a clean shared clone of the lane,
using the two check bodies of record:
  corpus/defects.jsonl        -> plans/defect_ledger.py      CHECKS (r34_d1..r34_d5)
  corpus/defects-round35.jsonl -> plans/round36_c1_verify.py CHECKS (r35_d1..r35_d4)
No ledger row and no check body is edited here: the clone's tip bytes are imported as-is, so a
check that fails fails on the tip, not on a local rewrite.

Per row it prints
  <id> status=<open|closed> observed=<pass|fail> agree=<yes|NO> <check note> ledger=<file> kind=<pin|live>
  kind=live  the check exercises behaviour (runs the package gate, the battery, the line fixtures,
             a repo-state query with a zero-tolerance observation)
  kind=pin   the check only pins closure bytes (a manifest digest list, a committed path count, a
             correction/erratum line, a quote's presence in a frozen capture); a pin failing means
             the closure evidence moved, not that the defect class came back
and then the summary line
  rows=<n> closed=<n> observed_pass=<n> mismatches=<n>
mismatches counts every closed row whose check fails plus every open row whose check passes (stale
self-assessment), exactly as the two checkers of record define it.

Usage:
  python3 ledger_tip.py --source /path/to/lane --work /path/to/scratch
The clone is created at <work>/lane (must not exist), verified with rev-parse --show-toplevel, and
left in place for inspection; the caller removes the scratch tree.
  python3 ledger_tip.py --lane /path/to/clone            (control mode)
runs the same checks on an already prepared tree WITHOUT the clean-tree refusal, so a deliberately
broken clone can be used to show each check still bites. Control mode prints `dirty=<n>`.
"""
import argparse
import importlib.util
import json
import pathlib
import subprocess
import sys

LEDGERS = (
    ("corpus/defects.jsonl", "plans/defect_ledger.py"),
    ("corpus/defects-round35.jsonl", "plans/round36_c1_verify.py"),
)

# Closure-byte pins vs behaviour checks. Both kinds may be `closed` in the ledger; only a failing
# `live` row is a behavioural regression.
KIND = {
    "r34_d1": "live",   # git ls-files --others over the round-34 paths
    "r34_d2": "pin",    # committed path count under three fixed mirror roots
    "r34_d3": "pin",    # SHA256SUMS digest list of a frozen capture
    "r34_d4": "pin",    # the SCORECARD correction line still says what it said
    "r34_d5": "pin",    # frozen capture quote + erratum/mistake rows
    "r35_d1": "live",   # 14-fixture battery + genuine package re-run through the gate
    "r35_d2": "live",   # whole-lane untracked set + 6 directional line fixtures
    "r35_d3": "pin",    # committed nested-wave path count at the branch tip
    "r35_d4": "pin",    # toolathlon recount vs the round-36 erratum line
}


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def clone_lane(source, work):
    dest = work / "lane"
    if dest.exists():
        raise SystemExit(f"refuse to reuse {dest}; remove it first")
    subprocess.run(["git", "clone", "-q", "--shared", str(source), str(dest)], check=True)
    top = subprocess.run(["git", "-C", str(dest), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True).stdout.strip()
    if pathlib.Path(top).resolve() != dest.resolve():
        raise SystemExit(f"clone top {top} != {dest}")
    head = subprocess.run(["git", "-C", str(dest), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()
    dirty = subprocess.run(["git", "-C", str(dest), "status", "--porcelain"],
                           capture_output=True, text=True, check=True).stdout.strip()
    if dirty:
        raise SystemExit(f"clone is not clean:\n{dirty}")
    return dest, head


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", help="lane to clone (shared, read-only)")
    ap.add_argument("--work", help="scratch dir; clone goes to <work>/lane")
    ap.add_argument("--lane", help="control mode: run on this tree, no clean-tree refusal")
    ap.add_argument("--keep-notes", action="store_true", help="print the check note even on pass")
    a = ap.parse_args()
    if a.lane:
        lane = pathlib.Path(a.lane).resolve()
        head = subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
        dirty = len([x for x in subprocess.run(["git", "-C", str(lane), "status", "--porcelain"],
                                               capture_output=True, text=True, check=True
                                               ).stdout.splitlines() if x])
        print(f"TIP commit={head} control={lane} dirty={dirty}")
    else:
        if not (a.source and a.work):
            ap.error("either --lane, or both --source and --work")
        work = pathlib.Path(a.work).resolve()
        work.mkdir(parents=True, exist_ok=True)
        lane, head = clone_lane(pathlib.Path(a.source).resolve(), work)
        print(f"TIP commit={head} clone={lane}")

    modules = {rel: load_module(rel.replace("/", "_")[:-3], lane / rel) for _l, rel in LEDGERS}
    rows = closed = passed = mism = 0
    for ledger_rel, mod_rel in LEDGERS:
        mod = modules[mod_rel]
        ledger = [json.loads(l) for l in (lane / ledger_rel).read_text().splitlines() if l.strip()]
        lclosed = lpassed = lmism = 0
        for r in ledger:
            fn = mod.CHECKS.get(r.get("check"))
            if fn is None:
                ok, note = False, f"unknown check {r.get('check')!r}"
            else:
                try:
                    ok, note = fn(lane)
                except Exception as e:  # a crash is an observed failure, never a pass
                    ok, note = False, f"error {type(e).__name__}: {e}"
            st = r.get("status")
            is_closed = st == "closed"
            agree = (is_closed and ok) or (st == "open" and not ok)
            kind = KIND.get(r.get("check"), "unknown")
            rows += 1
            closed += is_closed
            passed += ok
            mism += not agree
            lclosed += is_closed
            lpassed += ok
            lmism += not agree
            tail = note if (a.keep_notes or not ok) else ""
            print(f"{r['id']} status={st} observed={'pass' if ok else 'fail'} "
                  f"agree={'yes' if agree else 'NO'} {tail}".rstrip()
                  + f" ledger={ledger_rel} kind={kind}")
        print(f"LEDGER {ledger_rel} rows={len(ledger)} closed={lclosed} "
              f"observed_pass={lpassed} mismatches={lmism}")
    print(f"rows={rows} closed={closed} observed_pass={passed} mismatches={mism}")
    return 0 if (rows and mism == 0) else 1


if __name__ == "__main__":
    sys.exit(main())

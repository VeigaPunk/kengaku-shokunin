#!/usr/bin/env python3
"""C2CritPredicate2 — D suite: the fixed laundering runs (B3/C2/C3 re-run with the
red-row list captured from the LANE ledger before the fixture is stubbed/greened)."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

sys.path.insert(0, "/fast/scratch/hyaku/kengaku-r53/C2CritPredicate2")
from harness import (SEAT, COUNTER, git, lane_tree, make_fixture, load_ledger, save_ledger,
                     stub_all, clone_source, run_counter, report, results)

OUT = SEAT / "out"
RED_ROWS = [n for n, e in load_ledger(SEAT / "lane").get("rows", {}).items()
            if e.get("state") == "red"]
print("red rows:", RED_ROWS)


def green_all(D):
    led = load_ledger(D)
    for n, e in led["rows"].items():
        e["exit"] = 0; e["state"] = "green"
        e.pop("evidence", None); e.pop("reason", None)
    save_ledger(D, led)


def uv_to_python(D):
    led = load_ledger(D)
    for n, e in led["rows"].items():
        a = e.get("argv") or []
        if a and a[0] == "uv":
            i = a.index("python3")
            e["argv"] = a[i:]
    save_ledger(D, led)


def fixture(label, mutate):
    def _mut(D):
        uv_to_python(D)
        green_all(D)
        if mutate:
            mutate(D)
    D = make_fixture(label, _mut, stub=True)
    S = clone_source(D, label)
    return D, S


def main():
    (OUT / "d.red-rows.txt").write_text("\n".join(RED_ROWS) + "\n")

    # ---- D1: all twelve red rows -> --help / kind=help (12 = 15.4% > the 10% cap) -----
    def d1(D):
        led = load_ledger(D)
        for n in RED_ROWS:
            e = led["rows"][n]
            e["argv"] = ["python3", e["argv"][1], "--help"]
            e["kind"] = "help"; e["exit"] = 0; e["state"] = "green"
            e.pop("evidence", None); e.pop("reason", None)
        save_ledger(D, led)
    D, S = fixture("d1-launder-all-twelve-via-help", d1)
    rc, out = run_counter(D, S, "d1-launder-all-twelve-via-help")
    report("D1-launder-all-twelve-red-rows-via---help", "help_limit", rc, out,
           notes="12 help-kind rows = 15.4% of 78 -> the 10% cap should trip")

    # ---- D2: 7 via --help (under the cap) + 5 via --selftest (selftest is UNCAPPED) ---
    def d2(D):
        led = load_ledger(D)
        for i, n in enumerate(RED_ROWS):
            e = led["rows"][n]
            if i < 7:
                e["argv"] = ["python3", e["argv"][1], "--help"]
                e["kind"] = "help"
            else:
                e["argv"] = ["python3", e["argv"][1], "--selftest"]
                e["kind"] = "selftest"
            e["exit"] = 0; e["state"] = "green"
            e.pop("evidence", None); e.pop("reason", None)
        save_ledger(D, led)
    D, S = fixture("d2-mixed-laundering", d2)
    rc, out = run_counter(D, S, "d2-mixed-laundering")
    report("D2-mixed-help-plus-selftest-laundering", "PREDICATE R53-C2 pass", rc, out,
           notes="all 12 red rows laundered; 7 help (under cap) + 5 selftest (uncapped)")

    # ---- D3: all twelve red rows -> --selftest / kind=selftest (selftest is UNCAPPED) --
    def d3(D):
        led = load_ledger(D)
        for n in RED_ROWS:
            e = led["rows"][n]
            e["argv"] = ["python3", e["argv"][1], "--selftest"]
            e["kind"] = "selftest"; e["exit"] = 0; e["state"] = "green"
            e.pop("evidence", None); e.pop("reason", None)
        save_ledger(D, led)
    D, S = fixture("d3-launder-all-twelve-via-selftest", d3)
    rc, out = run_counter(D, S, "d3-launder-all-twelve-via-selftest")
    report("D3-launder-all-twelve-red-rows-via---selftest", "PREDICATE R53-C2 pass", rc, out,
           notes="selftest kind has NO fraction cap; 12/78 = 15.4%")

    (OUT / "summary-d.json").write_text(json.dumps(results, indent=1))
    print("\n=== summary ===")
    for r in results:
        print(f"{r['verdict']:14s} {r['label']:56s} rc={r['rc']}  seen={r['seen']!r}")


if __name__ == "__main__":
    main()

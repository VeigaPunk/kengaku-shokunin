#!/usr/bin/env python3
"""C2CritPredicate2 — E suite: the REAL tree, doctored ledger.

No stubs.  The lane's committed tree at the tip is exported verbatim into a fixture repo;
ONLY plans/round53-tipstate.json is rewritten, so that every row the counter actually
observes as non-zero at the tip is re-declared green against an argv that prints usage and
exits 0.  If the counter prints PREDICATE R53-C2 pass on this tree, the ledger's declared
tip-state is forgeable with a single committed file.
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

sys.path.insert(0, "/fast/scratch/hyaku/kengaku-r53/C2CritPredicate2")
from harness import (SEAT, COUNTER, git, make_fixture, load_ledger, save_ledger,
                     clone_source, run_counter, report, results)

OUT = SEAT / "out"
LANE = SEAT / "lane"


def main():
    # 1. measure, on the real tree, what the counter actually observes
    D = make_fixture("e-real-tree", lambda D: None, stub=False)
    S = clone_source(D, "e-real-tree")
    rc, out = run_counter(D, S, "e0-real-tree-unmodified", jobs=4, timeout=900)
    report("E0-real-tree-unmodified-ledger", "PREDICATE R53-C2", rc, out,
           notes="the honest baseline on the real tree")

    # 2. which rows does the counter observe as non-zero on the real tree?
    red_observed = []
    for line in out.splitlines():
        if line.strip().startswith("MISMATCH "):
            red_observed.append(line.split()[1])
    (OUT / "e.mismatched-rows.txt").write_text("\n".join(red_observed) + "\n")
    print("observed non-zero rows:", red_observed)

    # 3. doctor the ledger: for each such row, re-declare it green against `--help`
    #    (every one of these scripts is argparse-based; `--help` exits 0).
    def doctor(D2):
        led = load_ledger(D2)
        for n in red_observed:
            e = led["rows"][n]
            argv = list(e.get("argv") or [])
            # keep the interpreter + script, replace every argument with --help
            script = next((a for a in argv if a.endswith(".py")), None)
            e["argv"] = ["python3", script, "--help"] if script else argv
            e["kind"] = "help"; e["exit"] = 0; e["state"] = "green"
            e.pop("evidence", None); e.pop("reason", None)
        save_ledger(D2, led)
    D2 = make_fixture("e-real-tree-doctored", doctor, stub=False)
    S2 = clone_source(D2, "e-real-tree-doctored")
    rc2, out2 = run_counter(D2, S2, "e1-real-tree-doctored-ledger", jobs=4, timeout=900)
    report("E1-real-tree-doctored-ledger", "PREDICATE R53-C2 pass", rc2, out2,
           notes="only plans/round53-tipstate.json changed; every row re-declared green")

    # 4. show that the doctored rows really fail on their DOCUMENTED commands
    doc = []
    skill = (D2 / "SKILL.md").read_text()
    for n in red_observed:
        e = load_ledger(D2)["rows"][n]
        doc.append(f"{n}: documented argv (from the committed ledger before doctoring) = "
                   f"{json.dumps(load_ledger(LANE)['rows'][n]['argv'])}")
    (OUT / "e.documented-argv-vs-doctored.txt").write_text("\n".join(doc) + "\n")

    (OUT / "summary-e.json").write_text(json.dumps(results, indent=1))
    print("\n=== summary ===")
    for r in results:
        print(f"{r['verdict']:14s} {r['label']:40s} rc={r['rc']}  seen={r['seen']!r}")


if __name__ == "__main__":
    main()

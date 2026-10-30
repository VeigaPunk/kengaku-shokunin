#!/usr/bin/env python3
"""C2CritPredicate2 — C suite: the strongest laundering variants.

B1/B2 showed that pointing a red row's argv at `--help` (kind=help) makes the counter
certify it green.  These attacks ask: can the same laundering be done WITHOUT the help
cap (i.e. using the `selftest` kind, which has no fraction cap), and can it be done for
ALL twelve red rows at once so the whole registry reads green?
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

sys.path.insert(0, "/fast/scratch/hyaku/kengaku-r53/C2CritPredicate2")
from harness import (SEAT, COUNTER, git, lane_tree, make_fixture, load_ledger, save_ledger,
                     stub_all, clone_source, run_counter, report, results)

OUT = SEAT / "out"


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


def real_script(D, rel):
    data = subprocess.run(["git", "-C", str(SEAT / "lane"), "show", f"HEAD:{rel}"],
                          capture_output=True, text=True)
    if data.returncode == 0:
        p = D / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(data.stdout)


def fixture(label, mutate, keep_real=()):
    def _mut(D):
        uv_to_python(D)
        green_all(D)
        for rel in keep_real:
            real_script(D, rel)
        if mutate:
            mutate(D)
    D = make_fixture(label, _mut, stub=True)
    S = clone_source(D, label)
    return D, S


def main():
    RED_ROWS = [n for n, e in load_ledger(SEAT / "lane").get("rows", {}).items()
                if e.get("state") == "red"]
    (OUT / "c.red-rows.txt").write_text("\n".join(RED_ROWS) + "\n")

    # ---- C1: launder a red row with kind=selftest (NO fraction cap on selftest) ---------
    # round51_surfaces.py --selftest exits 0; its documented entry command exits 1.
    def c1(D):
        led = load_ledger(D)
        e = led["rows"]["round51-surfaces"]
        e["argv"] = ["python3", "plans/round51_surfaces.py", "--selftest"]
        e["kind"] = "selftest"; e["exit"] = 0; e["state"] = "green"
        e.pop("evidence", None); e.pop("reason", None)
        save_ledger(D, led)
    D, S = fixture("c1-launder-via-selftest-kind", c1,
                   keep_real=("plans/round51_surfaces.py",))
    rc, out = run_counter(D, S, "c1-launder-via-selftest-kind")
    report("C1-launder-red-row-via-selftest-kind", "PREDICATE R53-C2 pass", rc, out,
           notes="selftest kind has NO fraction cap (only `help` does)")

    # ---- C2: launder ALL 12 red rows via --selftest, using a script whose --selftest exits 0
    # To make every red row's --selftest exit 0 we keep the real scripts but that is not
    # possible for scripts with no --selftest switch.  Instead: point EVERY red row at a
    # single always-green script *named in that row's own entry cell* is impossible
    # (entry_mismatch checks the path), so we substitute --help per row and check the cap.
    def c2(D):
        led = load_ledger(D)
        for n in RED_ROWS:
            e = led["rows"][n]
            e["argv"] = ["python3", e["argv"][1], "--help"]
            e["kind"] = "help"; e["exit"] = 0; e["state"] = "green"
            e.pop("evidence", None); e.pop("reason", None)
        save_ledger(D, led)
    D, S = fixture("c2-launder-all-twelve", c2)
    rc, out = run_counter(D, S, "c2-launder-all-twelve")
    report("C2-launder-all-twelve-red-rows", "help_limit", rc, out,
           notes="12 help rows = 15.4% > 10% cap -> must be caught")

    # ---- C3: mixed laundering -- 7 via --help (under the cap) and the rest via --selftest
    def c3(D):
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
    D, S = fixture("c3-mixed-laundering", c3)
    rc, out = run_counter(D, S, "c3-mixed-laundering")
    report("C3-mixed-help-and-selftest-laundering", "PREDICATE R53-C2 pass", rc, out,
           notes="7 help (under cap) + 5 selftest (uncapped) -> all 12 red rows laundered")

    # ---- C4: does the counter detect the laundered row at all when the ARGUMENTS change?
    #     Replace argv's --lane . with --manifest <a manifest that makes it pass>.
    #     round51_surfaces.py takes --manifest/--province; find a green invocation.
    probe = subprocess.run(["python3", "plans/round51_surfaces.py", "--lane", "."],
                           cwd=str(SEAT / "lane"), capture_output=True, text=True)
    (OUT / "c4.round51-surfaces-entry-exit.txt").write_text(f"exit={probe.returncode}\n" + probe.stdout[-1200:])

    (OUT / "summary-c.json").write_text(json.dumps(results, indent=1))
    print("\n=== summary ===")
    for r in results:
        print(f"{r['verdict']:14s} {r['label']:52s} rc={r['rc']}  seen={r['seen']!r}")


if __name__ == "__main__":
    main()

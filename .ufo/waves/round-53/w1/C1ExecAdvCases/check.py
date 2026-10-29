#!/usr/bin/env python3
"""Score a presence-only classifier against the adversarial case set.

usage: check.py CLASSIFIER.py [--cases cases.json] [--ambiguous ambiguous.json]
                              [--only SUBSTR] [-q]

CLASSIFIER.py must define classify_source(src) -> {test key: 'P1'|'P0'} (keys `name` or
`Class.name`). A case passes iff every expected key is present with the expected class
and no `must_not_include` key is returned. Keys returned but not expected are reported
(`extra`) and never fail a case: they are tests the author did not annotate.
Ambiguous cases (spec silent) are printed informationally with both readings; they never
affect the exit code. Exit 0 iff every case passes (and the classifier did not raise).
"""
import argparse
import importlib.util
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(path):
    spec = importlib.util.spec_from_file_location("classifier_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.classify_source


def clause(cid):
    return cid.split("-", 1)[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("classifier")
    ap.add_argument("--cases", default=str(HERE / "cases.json"))
    ap.add_argument("--ambiguous", default=str(HERE / "ambiguous.json"))
    ap.add_argument("--only", default="")
    ap.add_argument("-q", action="store_true", help="print only failures and totals")
    a = ap.parse_args()

    classify = load(a.classifier)
    cases = json.loads(Path(a.cases).read_text())
    cases = [c for c in cases if a.only in c["id"]]

    by_clause = defaultdict(lambda: [0, 0, 0, 0])  # cases, case_fail, tests, test_fail
    n_fail = n_tests = n_test_fail = 0
    for c in cases:
        cl = clause(c["id"])
        try:
            got = classify(c["source"])
            err = None
        except Exception as e:  # noqa: BLE001 - a crash is a failure, not a skip
            got, err = {}, f"{type(e).__name__}: {e}"
        bad = []
        if err:
            bad.append(f"RAISED {err}")
        for k, want in c["expected"].items():
            n_tests += 1
            by_clause[cl][2] += 1
            have = got.get(k)
            if have != want:
                n_test_fail += 1
                by_clause[cl][3] += 1
                bad.append(f"{k}: want {want} got {have}")
        for k in c.get("must_not_include", []):
            if k in got:
                bad.append(f"{k}: must not be reported (got {got[k]})")
        extra = sorted(set(got) - set(c["expected"]) - set(c.get("must_not_include", [])))
        by_clause[cl][0] += 1
        if bad:
            n_fail += 1
            by_clause[cl][1] += 1
            print(f"FAIL {c['id']}: " + "; ".join(bad))
        elif not a.q:
            print(f"pass {c['id']}")
        if extra and not a.q:
            print(f"     extra keys (unannotated): {extra}")

    print()
    for cl in sorted(by_clause):
        cs, cf, ts, tf = by_clause[cl]
        print(f"CLAUSE {cl:8s} cases={cs} case_fail={cf} tests={ts} test_fail={tf}")
    print(f"TOTAL cases={len(cases)} case_fail={n_fail} tests={n_tests} test_fail={n_test_fail}")

    amb_path = Path(a.ambiguous)
    if amb_path.exists() and not a.only:
        amb = json.loads(amb_path.read_text())
        print(f"\nAMBIGUOUS (informational, {len(amb)} cases): classifier output vs reading A / reading B")
        agree_a = agree_b = 0
        for c in amb:
            try:
                got = classify(c["source"])
            except Exception as e:  # noqa: BLE001
                print(f"  {c['id']}: RAISED {type(e).__name__}: {e}")
                continue
            ra = all(got.get(k) == v for k, v in c["reading_a"].items())
            rb = all(got.get(k) == v for k, v in c["reading_b"].items()) if c["reading_b"] else not got
            agree_a += ra
            agree_b += rb
            tag = "A" if ra and not rb else "B" if rb and not ra else "A=B" if ra and rb else "neither"
            if not a.q:
                print(f"  {c['id']}: got {got} -> follows {tag}")
        print(f"AMBIGUOUS follows_A={agree_a} follows_B={agree_b} of {len(amb)}")

    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()

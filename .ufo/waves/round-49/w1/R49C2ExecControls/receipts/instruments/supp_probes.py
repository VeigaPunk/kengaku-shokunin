#!/usr/bin/env python3
"""Supplementary discrimination probes for the wave-1 round-49 C2 counter candidate (scratch only).

Not a frozen control and not a scored run. Two questions the three frozen controls cannot answer:

  A/B  V7P satisfiability — round-48 routed defect 3 is "a frozen requirement-tag set with no violating
       case makes a counter leg unsatisfiable". V7P must DEFECT on the frozen tables and go ok on the
       same tables after a case/map amendment that adds a violating case for `both-print` and
       `toolchain` and repairs the two unparsable map rows. If B cannot be reached, V7P is
       unsatisfiable by construction and refuses the claim.
  C/D  V14 mechanics — the mutation leg must count a mutant caught only when it flips a substantive
       leg (V3/V4/V7/V7P/V9/V10/V12), and must report the floor honestly: a plan of no-op mutants
       must be unmet, not met.
"""
from __future__ import annotations

import json
import pathlib
import shutil
import sys
import tempfile

CAND = pathlib.Path(__file__).with_name("round49_c2_verify.py")
BASE = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("./lane-base")
WORK = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else pathlib.Path("./supp-work")


def load(path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("r49c2", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def copy_tree(src, dst):
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".git", "__pycache__"))
    return dst


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    c = load(CAND)
    m = c.load_r46(BASE)
    failures = []

    pkg, pins, src = c.load_pkg(BASE, m)
    ok, note = c.v7p(pkg, m)
    print(f"A v7p-frozen  {'ok' if ok else 'DEFECT'} {note}")
    if ok:
        failures.append("V7P passed the frozen tables (it must defect there)")

    amend = copy_tree(BASE, WORK / "tables-amended")
    dry = amend / "corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt"
    dry.write_text(dry.read_text()
                   + "CASE both-print-violator predicted=fail tests=F regrade=same violates=both-print "
                     "end=recipe -- supplementary: a state whose two runtimes print different values\n"
                   + "CASE toolchain-violator predicted=fail tests=F regrade=same violates=toolchain "
                     "end=recipe -- supplementary: a state that exercises both toolchains differently\n")
    receipt = amend / "corpus/evidence/round46/polyglot-c-py-probe.txt"
    receipt.write_text(receipt.read_text()
                       + "CASE both-print-violator predicted=fail observed=fail tests=F predicted_tests=F "
                         "match=yes regrade=same violates=both-print -- supplementary\n"
                       + "CASE toolchain-violator predicted=fail observed=fail tests=F predicted_tests=F "
                         "match=yes regrade=same violates=toolchain -- supplementary\n")
    entry = amend / "corpus/knowledge/tb2-polyglot-c-py-grader.md"
    body = entry.read_text()
    body = body.replace(
        "| instruction.md:7 | both-print | not exercised | no frozen case violates it |",
        "| `instruction.md:7` | `both-print` | enforced | `both-print-violator` |")
    body = body.replace(
        "| instruction.md:9 | toolchain | not exercised | no frozen case violates it |",
        "| `instruction.md:9` | `toolchain` | enforced | `toolchain-violator` |")
    entry.write_text(body)
    apkg, _p, _s = c.load_pkg(amend, m)
    ok, note = c.v7p(apkg, m)
    print(f"B v7p-amended {'ok' if ok else 'DEFECT'} {note}")
    if not ok:
        failures.append("V7P stayed unsatisfiable after a violating case and a repaired map")

    four = copy_tree(BASE, WORK / "mut-four")
    (four / "plans/mutants49").mkdir(parents=True, exist_ok=True)
    (four / "plans/mutants49/plan.json").write_text(json.dumps({"N": 4, "mutants": [
        {"id": "m-receipt-observed", "file": "corpus/evidence/round46/polyglot-c-py-probe.txt",
         "find": "CASE nop predicted=fail observed=fail", "replace": "CASE nop predicted=fail observed=pass"},
        {"id": "m-entry-case-row", "file": "corpus/knowledge/tb2-polyglot-c-py-grader.md",
         "find": "| `nop` | F | fail |", "replace": "| `nop` | P | pass |"},
        {"id": "m-noop-a", "file": "plans/filler46/entry.md", "find": "do-nothing", "replace": "do nothing"},
        {"id": "m-noop-b", "file": "plans/filler46/dry-cases.txt", "find": "do nothing end state 0",
         "replace": "do nothing end state zero"},
    ]}))
    fpkg, _p, _s = c.load_pkg(four, m)
    ok, note = c.v14(four, fpkg, WORK / "v14-four", m)
    print(f"C v14 2-flip+2-noop floor=2 {'ok' if ok else 'DEFECT'} {note}")
    if not ok:
        failures.append("V14 missed mutants that do flip substantive legs")

    none = copy_tree(BASE, WORK / "mut-noop")
    (none / "plans/mutants49").mkdir(parents=True, exist_ok=True)
    (none / "plans/mutants49/plan.json").write_text(json.dumps({"N": 2, "mutants": [
        {"id": "m-noop-a", "file": "plans/filler46/entry.md", "find": "do-nothing", "replace": "do nothing"},
        {"id": "m-noop-b", "file": "plans/filler46/dry-cases.txt", "find": "do nothing end state 0",
         "replace": "do nothing end state zero"},
    ]}))
    npkg, _p, _s = c.load_pkg(none, m)
    ok, note = c.v14(none, npkg, WORK / "v14-none", m)
    print(f"D v14 0-flip floor=1 {'ok' if ok else 'DEFECT'} {note}")
    if ok:
        failures.append("V14 reported met on a floor no no-op mutant can reach")
    print(f"SUPP {'ok' if not failures else 'FAIL'} failures={failures or 0}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())

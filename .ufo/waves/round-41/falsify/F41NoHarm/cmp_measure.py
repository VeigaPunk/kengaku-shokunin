#!/usr/bin/env python3
"""Normalise two round-41 measure.sh transcripts and diff them.

Normalisation removes only (a) the scratch root that measure.sh interpolates and
(b) the measured commit id, so any surviving difference is a verdict difference.
Usage: cmp_measure.py A.txt B.txt [--keep-tip]
"""
import difflib
import re
import sys

SCRATCH = re.compile(r"/fast/scratch/hyaku/kengaku-r41/(L1/measure|F41NoHarm/measure(?:-pinned)?)")
TIPS = re.compile(r"\b(74513c0625df7886357b866074104a0cf4bf9cc1|d7c77895752a2a5f317fa22f2362416ada50a04b|3d0058fbde484c9d6c23fd997d9ee09a0663bcdb)\b")
DURATION = re.compile(r"^elapsed=\d+s$|^master-run rc=\d+ elapsed=\d+s lines=\d+$|^pinned-run rc=\d+ elapsed=\d+s lines=\d+$")

VERDICT = re.compile(
    r"^(TIP |untracked_in_clone=|PINS |PINS-AFTER|FIXTURE |MUTANT |MUTANTS |MUTANTS-BY-TOOL|"
    r"BATTERY |ADVERTISED |PREDICATE |V[1-8] |    gate:|checks=|ORDER |ROUND-CLOSE |exit=|"
    r"tip |receipt |control receipt=|note compared=|receipts=|regrade |cases=|constraints_probe |"
    r"rows=|LEDGER |R3\d-D\d|REF AUDIT|GATE |registry_rows=|file\t|ok\t|\$ )"
)


def norm(path, keep_tip):
    out = []
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        line = SCRATCH.sub("<S>", line)
        if not keep_tip:
            line = TIPS.sub("<TIP>", line)
        if DURATION.search(line):
            continue
        out.append(line)
    return out


def main():
    a, b = sys.argv[1], sys.argv[2]
    keep_tip = "--keep-tip" in sys.argv
    na, nb = norm(a, keep_tip), norm(b, keep_tip)
    d = list(difflib.unified_diff(na, nb, a, b, lineterm="", n=1))
    va = [l for l in na if VERDICT.match(l)]
    vb = [l for l in nb if VERDICT.match(l)]
    print(f"lines A={len(na)} B={len(nb)} verdict_lines A={len(va)} B={len(vb)}")
    print(f"verdict_multiset_equal={sorted(va) == sorted(vb)}")
    if d:
        print(f"DIFF lines={len(d)}")
        print("\n".join(d))
    else:
        print("DIFF none")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Compare R41CritIndep's hand predictions with the frozen receipt's observed test letters.

  python3 compare.py <receipt> [<scratch-probe-output>]
Prints one line per case plus the agreement count. The second argument (optional) is the scratch
probe run's own output, used only for the three added cases.
"""
import re
import sys

sys.path.insert(0, "/fast/scratch/hyaku/kengaku-r41/R41CritIndep")
from predictions import CASE_ORDER, PRED  # noqa: E402


def letters(line):
    m = re.search(r"\btests=([SPCF]{3})\b", line)
    return m.group(1) if m else None


def main():
    observed = {}
    for line in open(sys.argv[1], encoding="utf-8"):
        if line.startswith("CASE "):
            cid = line.split()[1]
            observed[cid] = letters(line)
    ok = bad = 0
    extra_expected = {"dtend-tzid-only", "first-conflicting-decoy", "alice-wed-1000-shifted-1100"}
    for cid in CASE_ORDER:
        if cid in extra_expected:
            continue
        want = PRED[cid][0]
        got = observed.get(cid)
        same = got == want
        ok += same
        bad += not same
        print(f"CMP {cid} indep={want} receipt={got} {'agree' if same else 'DISAGREE'}")
    print(f"AGREE {ok}/25 disagree={bad} (receipt cases={len(observed)})")
    if len(sys.argv) > 2:
        seen = {}
        for line in open(sys.argv[2], encoding="utf-8"):
            if line.startswith("CASE "):
                seen[line.split()[1]] = letters(line)
        for cid in ("dtend-tzid-only", "first-conflicting-decoy", "alice-wed-1000-shifted-1100"):
            want, got = PRED[cid][0], seen.get(cid)
            print(f"EXTRA {cid} indep={want} observed={got} {'agree' if got == want else 'DISAGREE'}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

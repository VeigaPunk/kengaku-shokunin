#!/usr/bin/env python3
"""Record the /app/plaintexts.txt end state per case from the parity harness and diff it with
claims/c2-stage-check.txt (the probe's own staged sizes). Proves the state pytest graded is the state
the probe staged."""
from __future__ import annotations

import hashlib
import pathlib
import re
import shutil
import sys

sys.argv = [sys.argv[0]] + ["/fast/scratch/hyaku/kengaku-r44/R44PytestParity/w"]
import parity as P  # noqa: E402

STAGE = P.LANE / ".ufo/waves/round-44/claims/c2-stage-check.txt"


def staged():
    rows = {}
    for line in STAGE.read_text().splitlines():
        m = re.match(r"STAGECHECK (\S+) rc=(\d+) seed rc=(\d+) recipe rc=(\d+) plaintexts (\S+)", line)
        if m:
            tail = m.group(6) if m.lastindex >= 6 else m.group(5)
            rows[m.group(1)] = tail
    return rows


def main():
    rows = staged()
    root = P.WORK
    root.mkdir(parents=True, exist_ok=True)
    bad = 0
    for case in P.pr.CASES:
        work, rc, out = P.build(P.CAP, root, case)
        try:
            p = work / "app" / "plaintexts.txt"
            if p.exists():
                b = p.read_bytes()
                mine = f"bytes={len(b)}"
                digest = hashlib.sha256(b).hexdigest()
            else:
                mine, digest = "absent", "-"
            want = rows.get(case.cid)
            ok = want == mine
            bad += not ok
            print(f"STATE {case.cid} recipe_rc={rc} plaintexts={mine} sha256={digest}"
                  f" staged={want} same={'yes' if ok else 'NO'}")
        finally:
            shutil.rmtree(work, ignore_errors=True)
    print(f"state-parity cases={len(P.pr.CASES)} mismatched={bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

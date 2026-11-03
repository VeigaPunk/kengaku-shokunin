#!/usr/bin/env python3
"""Harness self-check stub -- NOT a strict-mode implementation.

The R67-C2 strict gate is built by another seat and does not exist yet, so it
was never run from this seat.  This stub exists only to exercise the control
flow of run_strict_fixtures.sh: expected.tsv parsing, exit-code comparison,
`CHECK defect` message gating, and the runner's own exit status.  It does not
implement any of the s1-s6 clauses and its runs are harness evidence only;
they MUST NOT be cited as evidence for R67-C2.

Modes (environment variable STUB_MODE):
  faithful  base.txt -> rc 0 with `CHECK ok`; every other fixture -> rc 1
            with a `CHECK defect:` line.  Matches expected.tsv, so the
            runner must exit 0.
  survivor  every fixture -> rc 0.  The gate never fires, so the runner must
            exit 1 (ten rows differ from expected_rc).
  crash     like faithful, but raises an uncaught exception on
            fixtures/m-s4-1.txt.  Python exits 1 with a traceback and no
            `CHECK defect` line, so the runner must fail exactly that row.
"""

import os
import pathlib
import sys


def main(argv):
    if len(argv) != 4 or argv[1] != "--check-receipt" or argv[3] != "--strict":
        print("stub usage: --check-receipt PATH --strict", file=sys.stderr)
        return 2
    mode = os.environ.get("STUB_MODE", "faithful")
    name = pathlib.Path(argv[2]).name

    if mode == "survivor":
        print("CHECK ok cases=5")
        print("PREDICATE R65-C1 pass")
        return 0
    if mode == "crash" and name == "m-s4-1.txt":
        raise RuntimeError("stub crash: uncaught exception must not read as a verdict")
    if name == "base.txt":
        print("CHECK ok cases=5")
        print("PREDICATE R65-C1 pass")
        return 0
    print("CHECK defect: (stub) %s" % name)
    print("PREDICATE R65-C1 fail")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

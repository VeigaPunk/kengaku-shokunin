#!/usr/bin/env python3
"""Dump full pytest output for two cases (one P, one F) as evidence of the parity harness."""
from __future__ import annotations

import pathlib
import sys

sys.argv = [sys.argv[0]] + ["/fast/scratch/hyaku/kengaku-r44/R44PytestParity/w"]
import parity as P  # noqa: E402  (import after argv is set so WORK resolves)

for cid in ("oracle-solve-sh", "hex-output"):
    case = next(c for c in P.pr.CASES if c.cid == cid)
    root = P.WORK
    root.mkdir(parents=True, exist_ok=True)
    work, rc, out = P.build(P.CAP, root, case)
    try:
        print(f"===== case {cid} recipe_rc={rc}")
        grc, gout = P.grade(P.CAP, work)
        print(f"----- pytest rc={grc}")
        print(gout)
    finally:
        import shutil
        shutil.rmtree(work, ignore_errors=True)

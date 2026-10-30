#!/usr/bin/env python3
"""C1MutClassifier: real-tree probe of the CONFIRM span (the counter's end_lineno use).

The counter's CONFIRM leg requires the confirmation's `quote` to be found inside the
test function's own line span:  span = src[lineno-1:end_lineno].  A quote taken from
the line *after* the test function ends is outside the span and must be rejected.

This probe builds, on a scratch copy of the lane, a confirmations.json whose quote is
taken from the line immediately AFTER each test's end_lineno, and runs the counter
twice: pristine and with the span widened by one line (end_lineno + 1).

If the widened counter accepts and the pristine rejects, the off-by-one is a live
weakening of the frozen CONFIRM leg.  The lane itself is never written.

usage: spanprobe.py
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE / "lane"
WORK = HERE / "spanprobe"
ENV = {**os.environ, "TMPDIR": str(WORK), "PYTHONDONTWRITEBYTECODE": "1"}


def run(cmd, cwd=None, timeout=1800):
    return subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True, timeout=timeout)


def norm(s):
    import re
    return re.sub(r"\s+", " ", s).strip()


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    conf = json.loads((LANE / "corpus/evidence/round53/confirmations.json").read_text())
    idx = {t["id"]: t for t in json.loads(
        (LANE / "corpus/evidence/round53/tests-index.json").read_text())["tests"]}
    graders = LANE / "corpus/evidence/round52/graders"

    # build the "quote from one line past the test's end" variant of every row
    forged = []
    n_moved = 0
    for r in conf:
        t = idx.get(r["test_id"])
        if not t:
            continue
        src = (graders / t["file"]).read_text(encoding="utf-8", errors="replace").splitlines()
        after = t["end_lineno"]            # 0-based index of the line after the test
        if after >= len(src):
            continue
        cand = src[after].strip()
        if len(norm(cand)) < 25:
            # pad to the quote length floor by taking a longer window
            cand = norm(" ".join(x.strip() for x in src[after:after + 2]))
        if len(norm(cand)) < 25:
            continue
        r2 = dict(r)
        r2["quote"] = cand
        forged.append(r2)
        n_moved += 1
    print(f"rows={len(conf)} quotes moved past the test span={n_moved}")
    if not forged:
        print("no row could be moved; nothing to probe")
        return 0

    # sanity: the forged quote must be OUTSIDE the pristine span and INSIDE the widened one
    t0 = idx[forged[0]["test_id"]]
    s0 = (graders / t0["file"]).read_text(encoding="utf-8", errors="replace").splitlines()
    sp_pristine = norm("\n".join(s0[t0["lineno"] - 1:t0["end_lineno"]]))
    sp_wide = norm("\n".join(s0[t0["lineno"] - 1:t0["end_lineno"] + 1]))
    q0 = norm(forged[0]["quote"])
    print(f"example {t0['id']}: quote in pristine span={q0 in sp_pristine} "
          f"in widened span={q0 in sp_wide}")

    results = {}
    for variant in ("pristine", "end_lineno-plus-1"):
        d = WORK / variant
        shutil.rmtree(d, ignore_errors=True)
        shutil.copytree(LANE, d, symlinks=True)
        (d / "corpus/evidence/round53/confirmations.json").write_text(json.dumps(forged, indent=1))
        if variant != "pristine":
            cp = d / "plans/round53_c1_triage.py"
            s = cp.read_text()
            old = 'span = norm("\\n".join(src[t["lineno"] - 1:t["end_lineno"]])) if t else ""'
            assert s.count(old) == 1
            cp.write_text(s.replace(old, old.replace('t["end_lineno"]]', 't["end_lineno"] + 1]')))
        # commit so the tree is clean (FREEZE requires a clean tree)
        run(["git", "-C", str(d), "-c", "user.name=c1mut", "-c", "user.email=c1mut@x",
             "commit", "-qam", "forged quotes (scratch probe)"])
        r = run([sys.executable, "plans/round53_c1_triage.py", "--lane", "."], cwd=d, timeout=1800)
        lines = [l for l in (r.stdout + r.stderr).splitlines()
                 if l.startswith(("CONFIRM", "REJECTED", "PREDICATE", "FREEZE", "ORACLE "))]
        print(f"\n--- {variant}: counter exit {r.returncode}")
        for l in lines[:14]:
            print("   ", l[:180])
        results[variant] = {"rc": r.returncode, "lines": lines}
    (HERE / "span-probe.json").write_text(json.dumps(
        {"forged_rows": len(forged), "example": t0["id"], "results": results}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

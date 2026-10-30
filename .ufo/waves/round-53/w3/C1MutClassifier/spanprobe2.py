#!/usr/bin/env python3
"""C1MutClassifier: does the CONFIRM leg's end_lineno off-by-one let a quote from a
DIFFERENT test's body pass?

The frozen leg-3 rule: a confirmation's `quote` must be found inside the test
function's own line span (src[lineno-1:end_lineno]).  Widening the span by one line
(src[lineno-1:end_lineno+1]) lets a quote from the next line -- which in a pytest
file is usually the *next* test's first line -- satisfy the rule.

This probe builds a real-tree confirmations.json whose quote is taken from the line
immediately AFTER the test's end_lineno (the next test's first line), and runs the
counter pristine vs with the span widened by one line.

The lane is never written; the probe runs on scratch copies.

usage: spanprobe2.py
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE / "lane"
WORK = HERE / "spanprobe2"
ENV = {**os.environ, "TMPDIR": str(WORK), "PYTHONDONTWRITEBYTECODE": "1"}


def run(cmd, cwd=None, timeout=1800):
    return subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True, timeout=timeout)


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    conf = json.loads((LANE / "corpus/evidence/round53/confirmations.json").read_text())
    idx = {t["id"]: t for t in json.loads(
        (LANE / "corpus/evidence/round53/tests-index.json").read_text())["tests"]}
    graders = LANE / "corpus/evidence/round52/graders"

    forged, details = [], []
    for r in conf:
        t = idx.get(r["test_id"])
        if not t:
            continue
        src = (graders / t["file"]).read_text(encoding="utf-8", errors="replace").splitlines()
        a = t["end_lineno"]                      # 0-based index of the line right after the test
        # the widened window is exactly one line: src[a]
        cand = norm(src[a]) if a < len(src) else ""
        if len(cand) < 20:
            details.append({"id": r["test_id"], "skipped": "next line shorter than 20 chars"})
            continue
        r2 = dict(r)
        r2["quote"] = cand
        forged.append(r2)
        details.append({"id": r["test_id"], "quote": cand[:120],
                        "in_pristine_span": norm(cand) in norm("\n".join(src[t["lineno"] - 1:t["end_lineno"]])),
                        "in_widened_span": norm(cand) in norm("\n".join(src[t["lineno"] - 1:t["end_lineno"] + 1]))})
    print(f"rows={len(conf)} forged with a next-line quote={len(forged)}")
    for d in details[:6]:
        print("  ", d)
    if not forged:
        print("nothing to probe")
        return 0

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
        run(["git", "-C", str(d), "-c", "user.name=c1mut", "-c", "user.email=c1mut@x",
             "commit", "-qam", "forged next-line quotes (scratch probe)"])
        r = run([sys.executable, "plans/round53_c1_triage.py", "--lane", "."], cwd=d, timeout=1800)
        lines = [l for l in (r.stdout + r.stderr).splitlines()
                 if l.startswith(("CONFIRM", "PREDICATE"))]
        rej = [l for l in (r.stdout + r.stderr).splitlines() if "REJECTED" in l]
        print(f"\n--- {variant}: counter exit {r.returncode}")
        for l in lines:
            print("   ", l[:200])
        for l in rej[:8]:
            print("    ", l.strip()[:180])
        results[variant] = {"rc": r.returncode, "lines": lines, "rejected": rej}
    (HERE / "span-probe2.json").write_text(json.dumps(
        {"forged": len(forged), "details": details, "results": results}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

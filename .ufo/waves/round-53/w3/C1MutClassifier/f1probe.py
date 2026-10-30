#!/usr/bin/env python3
"""C1MutClassifier: re-attack wave-1's finding F1 against the A1 counter.

Wave-1 seat C1MutCounter reported (F1): "a joint edit of the classifier and its
recorded digest in a later commit still passes FREEZE".  Amendment A1 changed the
FREEZE leg: the classifier and the freeze file must be added in ONE commit and never
touched by any later commit (git log -- path has exactly one entry each).

This probe re-measures F1 against the A1 counter on a scratch copy of the lane:
  F1a  edit the classifier AND the freeze file's classifier_sha256 in a later commit
  F1b  edit only the classifier in a later commit
  F1c  edit only the freeze file's classifier_sha256 in a later commit
and reports the FREEZE line and the exit code of each.

The lane is never written; every run is on a scratch copy.

usage: f1probe.py
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
WORK = HERE / "f1probe"
ENV = {**os.environ, "TMPDIR": str(WORK), "PYTHONDONTWRITEBYTECODE": "1"}
CLF = "plans/round53_c1_classify.py"
FZR = "plans/round53-c1-freeze.json"


def run(cmd, cwd=None, timeout=1800):
    return subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True, timeout=timeout)


def counter(d: Path):
    r = run([sys.executable, "plans/round53_c1_triage.py", "--lane", "."], cwd=d, timeout=1800)
    lines = [l for l in (r.stdout + r.stderr).splitlines()
             if l.startswith(("FREEZE", "ORACLE ", "PREDICATE"))]
    return {"rc": r.returncode, "lines": lines}


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    out = {}
    for variant in ("F1a-classifier-and-digest", "F1b-classifier-only", "F1c-digest-only"):
        d = WORK / variant
        shutil.rmtree(d, ignore_errors=True)
        shutil.copytree(LANE, d, symlinks=True)
        if variant != "F1c-digest-only":
            # use the M08 mutant (the one that changes the population: 10 ids move)
            shutil.copy(HERE / "mutants/M08-existq-B-to-K.py", d / CLF)
        if variant != "F1b-classifier-only":
            fz = json.loads((d / FZR).read_text())
            fz["classifier_sha256"] = hashlib.sha256((d / CLF).read_bytes()).hexdigest()
            (d / FZR).write_text(json.dumps(fz, indent=1))
        r = run(["git", "-C", str(d), "-c", "user.name=c1mut", "-c", "user.email=c1mut@x",
                 "commit", "-qam", f"variant {variant} (scratch probe)"])
        st = run(["git", "-C", str(d), "status", "--porcelain"])
        assert st.returncode == 0 and st.stdout.strip() == "", st.stdout
        lg = run(["git", "-C", str(d), "log", "--format=%H", "--", CLF])
        lg2 = run(["git", "-C", str(d), "log", "--format=%H", "--", FZR])
        res = counter(d)
        print(f"--- {variant}: counter exit {res['rc']}  "
              f"(commits touching classifier={len(lg.stdout.split())}, "
              f"freeze file={len(lg2.stdout.split())})")
        for l in res["lines"]:
            print("   ", l[:190])
        out[variant] = {"commit_rc": r.returncode, **res,
                        "commits_classifier": lg.stdout.split(),
                        "commits_freeze": lg2.stdout.split()}
    (HERE / "f1-probe.json").write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

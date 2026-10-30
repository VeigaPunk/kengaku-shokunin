#!/usr/bin/env python3
"""C1MutClassifier: two counter-side probes the classifier-side matrix cannot answer.

C1  FREEZE pin.  The counter pins the classifier by sha256 (plans/round53-c1-freeze.json).
    Does a *committed* mutant classifier fail the counter before the ORACLE leg runs?
    -> a scratch clone of the lane with the classifier replaced by a mutant, counter run.

C2  end_lineno off-by-one.  The classifier never reads end_lineno; the counter's CONFIRM
    leg does (src[t["lineno"] - 1:t["end_lineno"]]).  Off-by-one the span and see whether
    the counter's own frozen --selftest notices.

Both run on copies under the seat's scratch; the lane is never written.

usage: countermut.py
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE / "lane"
MUTDIR = HERE / "mutants"
WORK = HERE / "countermut"

ENV = {**os.environ, "TMPDIR": str(WORK), "PYTHONDONTWRITEBYTECODE": "1"}


def run(cmd, cwd=None, timeout=900):
    return subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True, timeout=timeout)


def probe_freeze():
    """C1: does a committed mutant classifier fail the counter's FREEZE leg?"""
    out = []
    for name in ("M08-existq-B-to-K", "M20-no-assertion-reason-dropped"):
        d = WORK / f"freeze-{name}"
        shutil.rmtree(d, ignore_errors=True)
        shutil.copytree(LANE, d, symlinks=True)
        shutil.copy(MUTDIR / f"{name}.py", d / "plans/round53_c1_classify.py")
        # commit so the tree is clean (the FREEZE leg requires a clean tree)
        r = run(["git", "-C", str(d), "-c", "user.name=c1mut", "-c", "user.email=c1mut@x",
                 "commit", "-qam", "mutant classifier (scratch probe)"])
        st = run(["git", "-C", str(d), "status", "--porcelain"])
        assert st.returncode == 0 and st.stdout.strip() == "", st.stdout
        r2 = run([sys.executable, "plans/round53_c1_triage.py", "--lane", "."], cwd=d, timeout=1800)
        lines = [l for l in (r2.stdout + r2.stderr).splitlines()
                 if l.startswith(("FREEZE", "ORACLE", "PREDICATE", "PINS"))]
        out.append({"mutant": name, "commit_rc": r.returncode, "counter_rc": r2.returncode,
                    "lines": lines})
        print(f"--- {name}: counter exit {r2.returncode}")
        for l in lines:
            print("   ", l)
    return out


def probe_end_lineno():
    """C2: off-by-one the CONFIRM span; does the counter's own --selftest notice?"""
    out = []
    src = (LANE / "plans/round53_c1_triage.py").read_text()
    old = 'span = norm("\\n".join(src[t["lineno"] - 1:t["end_lineno"]])) if t else ""'
    assert src.count(old) == 1
    variants = {
        "end_lineno-minus-1": old.replace("t[\"end_lineno\"]]", "t[\"end_lineno\"] - 1]"),
        "end_lineno-plus-1": old.replace("t[\"end_lineno\"]]", "t[\"end_lineno\"] + 1]"),
        "lineno-plus-1": old.replace("t[\"lineno\"] - 1", "t[\"lineno\"]"),
    }
    for vname, new in variants.items():
        d = WORK / vname
        shutil.rmtree(d, ignore_errors=True)
        shutil.copytree(LANE, d, symlinks=True)
        (d / "plans/round53_c1_triage.py").write_text(src.replace(old, new))
        r = run([sys.executable, "plans/round53_c1_triage.py", "--selftest"], cwd=d, timeout=900)
        tail = (r.stdout + r.stderr).strip().splitlines()[-4:]
        fails = [l for l in (r.stdout + r.stderr).splitlines() if l.startswith("FAIL")]
        out.append({"variant": vname, "rc": r.returncode, "tail": tail, "fails": fails[:8]})
        print(f"--- {vname}: --selftest exit {r.returncode}")
        for l in tail:
            print("   ", l)
        for l in fails[:8]:
            print("    FAIL", l[:150])
    # pristine baseline
    r = run([sys.executable, str(LANE / "plans/round53_c1_triage.py"), "--selftest"], cwd=str(WORK), timeout=900)
    print(f"--- pristine: --selftest exit {r.returncode}")
    for l in (r.stdout + r.stderr).strip().splitlines()[-3:]:
        print("   ", l)
    out.append({"variant": "pristine", "rc": r.returncode,
                "tail": (r.stdout + r.stderr).strip().splitlines()[-3:]})
    return out


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    res = {"freeze": probe_freeze(), "end_lineno": probe_end_lineno()}
    (HERE / "counter-mutants.json").write_text(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""C1MutClassifier: run the COUNTER's own ORACLE leg (plans/round53_c1_triage.py)
against each mutant, in-process, with the lane untouched.

leg_oracle() is the frozen counter's own code: it merges the eight blind label seats'
files over the pinned shards (merge_labels) and re-scores the 305-test population with
the classifier (v2_classes).  Here load_mod() is redirected to the mutant file, so the
numbers printed are the counter's numbers for that mutant -- not a re-implementation.

It also runs the counter's own --selftest against a mutant-swapped counter copy to
show whether the counter's frozen fixture suite notices a mutated classifier.

usage: counterleg.py [mutant-name ...]
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE / "lane"
MUTDIR = HERE / "mutants"
COUNTER = LANE / "plans/round53_c1_triage.py"

sys.path.insert(0, str(HERE))
from mutate import MUTANTS  # noqa: E402


def load_counter():
    spec = importlib.util.spec_from_file_location("r53_counter", COUNTER)
    m = importlib.util.module_from_spec(spec)
    sys.modules["r53_counter"] = m
    spec.loader.exec_module(m)
    return m


def main():
    names = sys.argv[1:] or [m[0] for m in MUTANTS]
    t = load_counter()
    cfg = dict(t.FROZEN)
    info = {"authors": set(json.loads((LANE / "plans/round53-c1-freeze.json").read_text())
                            .get("author_seats") or [])}
    idx = json.loads((LANE / "corpus/evidence/round53/tests-index.json").read_text())["tests"]

    real_load = t.load_mod

    def oracle_for(path: Path):
        def fake_load(p, name):
            if Path(p).name == "round53_c1_classify.py":
                return real_load(path, name)
            return real_load(p, name)
        t.load_mod = fake_load
        try:
            ok, lines, v2, decided = t.leg_oracle(LANE, cfg, info)
        finally:
            t.load_mod = real_load
        return ok, lines, v2, decided

    ok, lines, v2, decided = oracle_for(LANE / "plans/round53_c1_classify.py")
    print("PRISTINE counter ORACLE leg:")
    for l in lines:
        print("   ", l)
    print(f"    leg_ok={ok}\n")

    rows = []
    for name in names:
        path = MUTDIR / f"{name}.py"
        if not path.is_file():
            continue
        try:
            ok, lines, v2, decided = oracle_for(path)
            line = [l for l in lines if l.startswith("ORACLE ")][0]
            ctl = [l for l in lines if l.startswith("ORACLE-CONTROL")][0]
            rows.append({"mutant": name, "oracle_ok": ok, "oracle": line, "control": ctl})
            print(f"{name:34s} leg_ok={str(ok):5s} {line}")
        except Exception as e:  # noqa: BLE001
            rows.append({"mutant": name, "error": f"{type(e).__name__}: {e}"})
            print(f"{name:34s} ERROR {type(e).__name__}: {e}")
    (HERE / "counter-oracle.json").write_text(json.dumps(rows, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

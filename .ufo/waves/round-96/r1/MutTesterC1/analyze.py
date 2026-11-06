#!/usr/bin/env python3
"""Compare every (mutant, input) run against the pristine run on the same input.

Matrix: each mutant's planned inputs + I0-T (every mutant at T) + the two rebuilt P2 controls
(I1-P1b do-nothing, I2-forged-case). Kill criterion (seat spec): a mutant is killed if some input
makes its PREDICATE line or exit code differ from the pristine counter's on that input.
Full-stdout equality is recorded as a secondary observation (the TARGET line is not
predicate-bearing).
"""
import json
import pathlib
import re

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r96/MutTesterC1")
RUNS = S / "runs"
PLAN = json.loads((S / "plan.json").read_text())
CONTROLS = ["I0-T", "I1-P1b", "I2-forged-case"]


def parse(name: str) -> dict | None:
    p = RUNS / f"{name}.txt"
    if not p.exists():
        return None
    text = p.read_text()
    rc = None
    m = re.search(r"^# rc (-?\d+)$", text, re.M)
    if m:
        rc = int(m.group(1))
    pred = next((ln for ln in text.splitlines() if ln.startswith("PREDICATE ")), "")
    legs = next((ln for ln in text.splitlines() if ln.startswith("LEGS ")), "")
    tgt = next((ln for ln in text.splitlines() if ln.startswith("TARGET ")), "")
    defects = [ln for ln in text.splitlines() if ln.startswith("DEFECT ")]
    body = "\n".join(ln for ln in text.splitlines() if not ln.startswith("# "))
    return {"rc": rc, "pred": pred, "legs": legs, "tgt": tgt, "defects": defects, "body": body}


rows = []
for mut, inps in PLAN.items():
    if mut.startswith("_"):
        continue
    for inp in dict.fromkeys(list(inps) + CONTROLS):
        base = parse(f"M00-orig--{inp}")
        got = parse(f"{mut}--{inp}")
        if base is None or got is None:
            rows.append({"mutant": mut, "input": inp, "status": "MISSING"})
            continue
        killed = (base["rc"], base["pred"]) != (got["rc"], got["pred"])
        rows.append({
            "mutant": mut, "input": inp, "status": "killed" if killed else "survived",
            "base_rc": base["rc"], "mut_rc": got["rc"],
            "base_pred": base["pred"].replace("PREDICATE R96-C1 ", ""),
            "mut_pred": got["pred"].replace("PREDICATE R96-C1 ", ""),
            "base_legs": base["legs"].replace("LEGS ", ""),
            "mut_legs": got["legs"].replace("LEGS ", ""),
            "target_differs": base["tgt"] != got["tgt"],
            "stdout_differs": base["body"] != got["body"],
            "mut_defects": got["defects"],
        })

verdict = {}
for r in rows:
    m = r["mutant"]
    if m not in verdict or (verdict[m]["status"] != "killed" and r["status"] == "killed"):
        verdict[m] = r
for m in sorted(verdict):
    v = verdict[m]
    print(f"{m:32s} {v['status']:9s} via {v['input']:26s} base=rc{v.get('base_rc')}/{v.get('base_pred')} "
          f"mut=rc{v.get('mut_rc')}/{v.get('mut_pred')} tgt_diff={v.get('target_differs')} "
          f"stdout_diff={v.get('stdout_differs')}")
    if v["status"] == "killed":
        for d in v["mut_defects"][:2]:
            print(f"    mutant defect: {d}")
        print(f"    pristine legs: {v['base_legs']}")
        print(f"    mutant   legs: {v['mut_legs']}")

(S / "analysis.json").write_text(json.dumps(rows, indent=1))
killed = sum(1 for v in verdict.values() if v["status"] == "killed")
print(f"\nmutants={len(verdict)} killed={killed} survived={len(verdict) - killed}")
print("pairs=%d" % len(rows))

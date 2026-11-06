#!/usr/bin/env python3
"""Build leg-disabled copies of the R98-C2 counter (scratch only) and run the matrix."""
from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path("/fast/scratch/hyaku/kengaku-r98/MutC2")
CLONE = ROOT / "clone"
COUNTER = CLONE / "plans/round98_c2_nested_bind.py"
T = "8e37fc65d5649bb37166fdd6b1657445a8cb55b9"

LEGS = {
    "L1": "    k1 = sha(gate_base) == GATE_SHA and sha(blob(lane, rev, GATE)) == GATE_SHA\n",
    "L2": "    k2 = derived == POP and len(POP) > 0\n",
    "L3": "    k3 = not still\n",
    "L4": "    k4 = not unbound\n",
    "L5": "    k5 = not changed\n",
    "L6": "    k6 = not caps\n",
    "L7": "    k7 = not new_old\n",
}


def build_counters() -> dict[str, str]:
    src = COUNTER.read_text()
    out = {}
    for leg, anchor in LEGS.items():
        if src.count(anchor) != 1:
            raise SystemExit(f"{leg}: anchor count {src.count(anchor)}")
        patched = src.replace(anchor, anchor + f"    k{leg[1]} = True  # MUTANT {leg}: leg disabled\n")
        p = ROOT / "counter" / f"{leg}.py"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(patched)
        out[leg] = str(p)
    return out


def run(label: str, script: Path, rev: str) -> dict:
    work = ROOT / "w" / label
    receipt = ROOT / "receipts" / f"{label}.txt"
    cmd = [sys.executable, str(script), "--lane", ".", "--rev", rev, "--work", str(work)]
    p = subprocess.run(cmd, cwd=str(CLONE), capture_output=True, text=True, timeout=1800)
    receipt.write_text(p.stdout + p.stderr + f"rc={p.returncode}\n")
    return {"label": label, "script": str(script), "rev": rev, "rc": p.returncode,
            "receipt": str(receipt)}


def main() -> int:
    man = json.loads((ROOT / "mutants.json").read_text())
    by_id = {m["id"]: m["commit"] for m in man["mutants"]}
    counters = build_counters()
    base = str(COUNTER)
    jobs = []
    for mid in sorted(by_id):
        jobs.append((f"in-{mid}", Path(base), by_id[mid]))
    logic = {
        "L1": [("M13", by_id["M13"])],
        "L2": [("T", T), ("M17", by_id["M17"])],
        "L3": [("T", T), ("M17", by_id["M17"]), ("M19", by_id["M19"])],
        "L4": [("T", T), ("M11", by_id["M11"]), ("M12", by_id["M12"]), ("M16", by_id["M16"])],
        "L5": [("T", T), ("M08", by_id["M08"])],
        "L6": [("T", T), ("M09", by_id["M09"]), ("M10", by_id["M10"])],
        "L7": [("T", T), ("M14", by_id["M14"])],
    }
    for leg, targets in logic.items():
        for tname, rev in targets:
            jobs.append((f"logic-{leg}-{tname}", Path(counters[leg]), rev))
    results = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        futs = [pool.submit(run, *j) for j in jobs]
        for f in futs:
            results.append(f.result())
    (ROOT / "runs.json").write_text(json.dumps(results, indent=2) + "\n")
    for r in results:
        text = Path(r["receipt"]).read_text()
        pred = [ln for ln in text.splitlines() if ln.startswith("PREDICATE")]
        legs = [ln for ln in text.splitlines() if ln.startswith("LEGS")]
        print(f'{r["label"]:<18} rc={r["rc"]} {pred[0] if pred else "?"} | {legs[0] if legs else "?"}')
    return 0


if __name__ == "__main__":
    sys.exit(main())

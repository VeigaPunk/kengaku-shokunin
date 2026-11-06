#!/usr/bin/env python3
"""Summarize the R98-C2 mutation matrix from receipts."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path("/fast/scratch/hyaku/kengaku-r98/MutC2")
LEG = re.compile(r"K(\d)=(pass|fail)")


def parse(label: str) -> dict:
    text = (ROOT / "receipts" / f"{label}.txt").read_text()
    legs = {}
    for m in LEG.finditer(text):
        legs[f"K{m.group(1)}"] = m.group(2)
    pred = next((ln.split()[-1] for ln in text.splitlines() if ln.startswith("PREDICATE")), "?")
    target = next((ln for ln in text.splitlines() if ln.startswith("TARGET")), "")
    defects = [ln for ln in text.splitlines() if ln.startswith("DEFECT ")]
    rc = next((ln.split("=")[1] for ln in text.splitlines() if ln.startswith("rc=")), "?")
    return {"legs": legs, "fail": [k for k, v in legs.items() if v == "fail"],
            "predicate": pred, "target": target, "defects": defects, "rc": rc}


def main() -> int:
    runs = json.loads((ROOT / "runs.json").read_text())
    rows = []
    for r in runs:
        p = parse(r["label"])
        rows.append({"label": r["label"], "rev": r["rev"], **p})
    (ROOT / "summary.json").write_text(json.dumps(rows, indent=2) + "\n")
    for r in rows:
        print(f'{r["label"]:<18} {r["predicate"]:<5} rc={r["rc"]} fail={",".join(r["fail"]) or "-"}')
        for d in r["defects"]:
            print("      " + d)
        if r["label"].startswith("in-") and r["predicate"] == "pass":
            print("      TARGET " + r["target"].split("TARGET ", 1)[-1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

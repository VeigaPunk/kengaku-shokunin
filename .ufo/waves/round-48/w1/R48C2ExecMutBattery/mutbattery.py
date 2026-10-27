REV a543d92083557dd9b33ee674e9b99b03411f80af
--- mutbattery.py (scratch-only harness, sha256 aed528fca0b6f215169e71d1f607150e0ad3b284314280633080387eb0c006f1)
#!/usr/bin/env python3
"""R48C2ExecMutBattery — wave-1 mutation battery on the committed C2 package bytes.

Read-only against the lane; every mutation is applied to a scratch copy of the clone at the
stage-1 freeze (a543d920). The detector is the COMMITTED counter `plans/round46_c3_verify.py`
(the digest-pinned import base named by the frozen C2 contract) plus the committed package gate
`plans/pkg_gate.py` run WITHOUT `--rerun` (P10 = fresh probe re-run disabled), which is the
V8/Q40 pre-receipt mode. No probe case is executed: the only probe invocation is `--dry`
(counter leg V5).

Leg set: the counter's legs minus V2 (its gate call passes --rerun, i.e. a full probe run,
forbidden before the stage-2 commit by the frozen Q30 ordering) and minus V11 (executes the
captured grader in a sandbox; not a substantive leg and not needed by this battery).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys

COUNTER_REL = "plans/round46_c3_verify.py"
GATE_REL = "plans/pkg_gate.py"
SPEC_REL = "plans/pkg-spec-r46.json"
LEG_SET = ("V1", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V12", "V13")
EXCLUDED = ("V2", "V11")


def load_counter(lane: pathlib.Path):
    path = lane / COUNTER_REL
    spec = importlib.util.spec_from_file_location("r46_c3_%d" % abs(hash(str(path))), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def measure(lane: pathlib.Path, work: pathlib.Path) -> dict:
    """Run the committed counter's leg set and the P10-disabled package gate on `lane`."""
    work.mkdir(parents=True, exist_ok=True)
    out = {"lane": str(lane), "legs": [], "gate": [], "notes": []}
    mod = load_counter(lane)
    try:
        pkg = mod.real_pkg(lane)
    except Exception as e:  # unreadable package: every leg is a DEFECT, never a pass
        out["notes"].append("PACKAGE unreadable: %s: %s" % (type(e).__name__, e))
        for name in LEG_SET:
            out["legs"].append({"leg": name, "ok": False, "note": "package unreadable: %s" % e})
        pkg = None
    if pkg is not None:
        res = mod.run_legs(lane, pkg, work, LEG_SET)
        out["legs"] = [{"leg": n, "ok": bool(ok), "note": note} for n, ok, note in res]
    # the package gate with P10 disabled: no --rerun, so the fresh probe re-run never happens
    gate = subprocess.run([sys.executable, str(lane / GATE_REL), "package", "--root", str(lane),
                           "--spec", str(lane / SPEC_REL)], capture_output=True, text=True, timeout=1800)
    for line in gate.stdout.splitlines():
        if line.startswith("P") and " " in line:
            clause, rest = line.split(" ", 1)
            state = "DEFECT" if rest.startswith("DEFECT") else ("ok" if rest.startswith("ok") else "?")
            out["gate"].append({"clause": clause, "ok": state == "ok", "note": rest})
    out["gate_exit"] = gate.returncode
    out["gate_stderr"] = gate.stderr.strip()[:300]
    substantive = ("V3", "V4", "V7", "V9", "V10", "V12")
    out["substantive_legs"] = list(substantive)
    out["substantive_defects"] = sorted({l["leg"] for l in out["legs"]
                                         if l["leg"] in substantive and not l["ok"]})
    out["defective_legs"] = sorted({l["leg"] for l in out["legs"] if not l["ok"]})
    out["gate_defective_clauses"] = sorted({g["clause"] for g in out["gate"] if not g["ok"]})
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="R48C2 mutation battery driver")
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    res = measure(pathlib.Path(a.lane).resolve(), pathlib.Path(a.work).resolve())
    pathlib.Path(a.out).write_text(json.dumps(res, indent=1, sort_keys=True))
    print("legs=" + ",".join("%s:%s" % (l["leg"], "ok" if l["ok"] else "DEFECT") for l in res["legs"]))
    print("gate=" + ",".join("%s:%s" % (g["clause"], "ok" if g["ok"] else "DEFECT") for g in res["gate"]))
    print("gate_exit=%s" % res["gate_exit"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Live cross-check: run the REAL pinned grader (probe run_grader) on the 18 case
contents and compare its observed pass/fail + assertion to my independent checker.
Scratch-only; never imports anything from indep.py.
"""
import importlib.util
import pathlib
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
GRADER = LANE / "corpus/evidence/round35/tb2-eval/test_outputs.py"
PROBE = LANE / "plans/tb2_grader_probe.py"

spec = importlib.util.spec_from_file_location("tb2_probe", PROBE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

src = GRADER.read_text()
parts = probe.components(src)
cases = probe.build_cases(parts)

ref = []
for name, content, pred, req in cases:
    obs, msg = probe.run_grader(str(GRADER), content)
    ref.append((name, obs, msg))
    print(f"live case={name} observed={obs} assertion={msg!r}")

# ground truth from my checker file? No: recompute here? The receipt is the frozen
# ground truth; this live run just confirms the receipt is live-fresh.
print(f"live_cases={len(ref)}")

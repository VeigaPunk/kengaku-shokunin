#!/usr/bin/env python3
"""Map each battery fixture to the gate clauses it trips (scratch, wave 1). Imports the frozen C1
counter's own fixture builders so the mapping is measured on the battery, not reasoned about."""
import importlib.util
import pathlib
import shutil
import subprocess
import sys
import tempfile

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
GATE = LANE / ".ufo/waves/round-36/build/R36GateA/pkg_gate.py"
spec_path = LANE / "plans/round36_c1_verify.py"
spec = importlib.util.spec_from_file_location("c1", spec_path)
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)

S = c1.load_spec(LANE)
tmp = pathlib.Path(tempfile.mkdtemp(prefix="k36-map-"))
try:
    items = [(f"P{p}", d) for p, _l, _e, d in c1.build_package_fixtures(LANE, S, tmp)]
    items = [(pid, ["package", "--root", str(d), "--require-clean-tree"]) for pid, d in items]
    items += [(tid, argv) for tid, _l, _e, argv in c1.build_line_fixtures(LANE, S, tmp)]
    for fid, argv in items:
        r = subprocess.run([sys.executable, str(GATE), *argv, "--spec", str(LANE / c1.SPEC_REL)],
                           capture_output=True, text=True)
        fired = [l.split()[0] for l in r.stdout.splitlines() if "DEFECT" in l]
        print(f"{fid} rc={r.returncode} fires={fired or 'none'}")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

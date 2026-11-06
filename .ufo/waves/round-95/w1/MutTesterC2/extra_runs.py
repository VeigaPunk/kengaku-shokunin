#!/usr/bin/env python3
"""The two census-mutant runs at T that battery.py's build_jobs mis-addressed (it ran them at P1)."""
import subprocess
import sys
import time
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r95/MutTesterC2")
LANE = S / "lane"
T = "afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239"
REC = S / "receipts"
WORK = S / "work"
PY = sys.executable

JOBS = [
    ("XM1-designated-forced-T", MUT := S / "mut" / "XM1-designated-forced.py"),
    ("XM3-honest-dropped-T", S / "mut" / "XM3-honest-dropped.py"),
]

for jid, mut in JOBS:
    argv = [PY, "-I", "-B", str(mut), "--lane", str(LANE), "--rev", T, "--work", str(WORK / jid)]
    t0 = time.time()
    p = subprocess.run(argv, cwd=str(LANE), capture_output=True, text=True, timeout=3600)
    dt = time.time() - t0
    (REC / f"{jid}.out").write_text(p.stdout)
    (REC / f"{jid}.txt").write_text(
        f"# id {jid}\n# argv {argv}\n# cwd {LANE}\n{p.stdout}# stderr:\n{p.stderr}rc={p.returncode} seconds={dt:.1f}\n")
    print(f"DONE {jid} rc={p.returncode} {dt:.0f}s", flush=True)
print("extra T runs complete", flush=True)

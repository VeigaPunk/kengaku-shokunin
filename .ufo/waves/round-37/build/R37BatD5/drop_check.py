#!/usr/bin/env python3
"""Load-bearing check for the d5 battery module: drop one fixture at a time, confirm its mutant survives.

Usage: python3 drop_check.py <scratch>   (run from the lane root; reads the delivered module read-only)
Writes each variant module under <scratch>/drop-<fid>/d5.py and prints the counter's MUTANT line.
"""
import pathlib
import subprocess
import sys

S = pathlib.Path(sys.argv[1])
LANE = pathlib.Path.cwd()
MODULE = LANE / ".ufo/waves/round-37/build/R37BatD5/battery/d5.py"
PAIRS = [("d5-m48-file-unreadable", "M48"), ("d5-m49-two-lines", "M49"),
         ("d5-m50-label-altered", "M50"), ("d5-m51-require-missing", "M51"),
         ("d5-m52-forbid-present", "M52"), ("d5-m53-capture-missing", "M53"),
         ("d5-m55-quote-absent", "M55")]

text = MODULE.read_text()
print("sha256(module) =", __import__("hashlib").sha256(text.encode()).hexdigest())
print("dropped_fixture | mutant | counter result")
for fid, mid in PAIRS:
    lines = text.splitlines(keepends=True)
    kept = [l for l in lines if not l.strip().startswith('{"fid": "%s"' % fid)]
    assert len(kept) == len(lines) - 1, fid
    d = S / ("drop-" + fid)
    d.mkdir(parents=True, exist_ok=True)
    (d / "d5.py").write_text("".join(kept))
    r = subprocess.run([sys.executable, "plans/round37_c1_verify.py", "--lane", str(LANE),
                        "--battery-dir", str(d), "--only", mid, "--work", str(S)],
                       capture_output=True, text=True)
    mut = [l for l in r.stdout.splitlines() if l.startswith("MUTANT ")]
    bat = [l for l in r.stdout.splitlines() if l.startswith("BATTERY ")]
    print(f"{fid} | {mid} | {mut[-1] if mut else 'NO MUTANT LINE'}")
    print(f"   {bat[0] if bat else 'NO BATTERY LINE'}")

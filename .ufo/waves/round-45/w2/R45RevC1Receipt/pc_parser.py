#!/usr/bin/env python3
"""Positive/negative control for handcheck_c1.parse_log: can it actually see an outside open?

PC1: strace a python that opens a file under the scratch root OUTSIDE the fixture dir -> parse_log
must report >=1 successful outside open (the parser is not vacuous).
PC2: strace a python that opens a file INSIDE the fixture dir -> parse_log must report 0.
"""
import importlib.util
import pathlib
import subprocess
import sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r45/R45RevC1Receipt/pc")
sys.argv = ["pc_parser.py", str(S)]  # satisfy handcheck_c1's module-level ROOT
spec = importlib.util.spec_from_file_location(
    "hc", "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/w2/"
          "R45RevC1Receipt/handcheck_c1.py")
hc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hc)

d = S / "d"
out = S / "outside"
d.mkdir(parents=True, exist_ok=True)
out.mkdir(parents=True, exist_ok=True)
(out / "f.txt").write_bytes(b"x")
(d / "in.txt").write_bytes(b"y")


def trace(expr, tag):
    log = S / f"log_{tag}"
    cmd = ["/usr/bin/strace", "-f", "-qq", "-y", "-e", "trace=open,openat,openat2,creat",
           "-o", str(log), "/usr/bin/python3", "-c", expr]
    subprocess.run(cmd, cwd=str(d), capture_output=True)
    succ, failed = hc.parse_log(log, d, (S,))
    print(f"PC {tag}: succ_outside={len(succ)} failed_touch={len(failed)}")
    for l in succ[:3]:
        print("PC SUCC-LINE " + l)
    for l in failed[:3]:
        print("PC FAIL-LINE " + l)
    return len(succ), len(failed)


s1, f1 = trace(f"open({str(out / 'f.txt')!r},'rb')", "outside")
s2, f2 = trace(f"open({str(d / 'in.txt')!r},'rb')", "inside")
ok = s1 >= 1 and f1 == 0 and s2 == 0 and f2 == 0
print(f"PC RESULT {'PARSER-DETECTS' if ok else 'PARSER-BLIND'} outside=({s1},{f1}) inside=({s2},{f2})")
sys.exit(0 if ok else 1)

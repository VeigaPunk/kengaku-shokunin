#!/usr/bin/env python3
"""Generate the three probe-case gblock.txt files (valid-balanced, linker-g-only, linker-4aa)
from the lane's probe builder, exactly as the receipt's frozen cases were defined."""
import hashlib
import importlib.util
import pathlib
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
PROBE = LANE / "plans" / "tb2_grader_probe.py"
GRADER = LANE / "corpus" / "evidence" / "round35" / "tb2-eval" / "test_outputs.py"

spec = importlib.util.spec_from_file_location("tb2_probe", PROBE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

src = GRADER.read_text()
parts = probe.components(src)
cases = {c[0]: c for c in probe.build_cases(parts)}
want = ["valid-balanced", "linker-g-only", "linker-4aa"]
outdir = pathlib.Path(sys.argv[1])
for name in want:
    n, content, pred, req = cases[name]
    d = outdir / name
    d.mkdir(parents=True, exist_ok=True)
    p = d / "gblock.txt"
    p.write_bytes(content.encode())
    print(f"{name} pred={pred} nt={len(content.strip())} "
          f"sha256={hashlib.sha256(content.encode()).hexdigest()} req={req!r}")
print(f"grader_sha256={hashlib.sha256(src.encode()).hexdigest()}")

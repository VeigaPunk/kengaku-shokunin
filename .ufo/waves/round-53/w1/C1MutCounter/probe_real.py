#!/usr/bin/env python3
"""Real-tree probe: each CFG/constant mutant run on the clean probe clone; killed iff stdout or rc differs from pristine."""
import re, subprocess, sys, json, hashlib
from pathlib import Path
S = Path("/fast/scratch/hyaku/kengaku-r53/C1MutCounter")
PROBE = S / "probe"
TARGET = PROBE / "plans/round53_c1_triage.py"
PRISTINE = S / "pristine_triage.py"
src = (S / "mutate.py").read_text()
block = src[src.index("M = ["): src.index("\ndef run_selftest")]
ns = {}
exec(block, ns)
M = [m for m in ns["M"] if m[1] in ("CONST",) or m[0] in ("K11", "P01", "P08", "P11", "P12", "F04", "F02", "K05", "C07")]
def real(path):
    p = subprocess.run([sys.executable, "plans/round53_c1_triage.py", "--lane", "."], cwd=PROBE, capture_output=True, text=True, timeout=600)
    return p.returncode, p.stdout
base_rc, base_out = real(PRISTINE)
TARGET.write_bytes(PRISTINE.read_bytes())
base_rc, base_out = real(None)
print("REAL-BASE rc=%d" % base_rc); print(base_out)
rows = []
for mid, grp, ln, old, new, note in M:
    lines = PRISTINE.read_text().split("\n")
    assert lines[ln - 1].count(old) == 1, mid
    lines[ln - 1] = lines[ln - 1].replace(old, new)
    TARGET.write_text("\n".join(lines))
    try:
        rc, out = real(None)
    finally:
        TARGET.write_bytes(PRISTINE.read_bytes())
    diff = [l for l in out.split("\n") if l not in base_out.split("\n")]
    rows.append(dict(id=mid, rc=rc, visible=(rc != base_rc or out != base_out), changed_lines=diff[:3]))
    print(mid, "rc=%d" % rc, "visible=%s" % (rc != base_rc or out != base_out), diff[:2])
Path(S / "work/probe_real.json").write_text(json.dumps(dict(base_rc=base_rc, base_out=base_out, rows=rows), indent=1))
print("restored", hashlib.sha256(TARGET.read_bytes()).hexdigest() == hashlib.sha256(PRISTINE.read_bytes()).hexdigest())

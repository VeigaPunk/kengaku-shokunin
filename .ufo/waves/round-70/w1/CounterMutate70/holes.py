#!/usr/bin/env python3
"""Two edge probes on R70-C1 --check-receipt, both outside the six assigned
checks' happy path: (H1) the probe-blob `absent` escape, (H2) last-wins
duplicate VECTOR/CASE lines."""

import pathlib
import shutil
import subprocess
import sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r70/CounterMutate70")
L = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
PROBE_REL = "plans/round70_c1_nginx_probe.py"
GRADER_REL = ("corpus/evidence/round52/graders/nginx-request-logging/"
              "tests/test_outputs.py")
ZERO = "0" * 64

probe_bytes = (L / PROBE_REL).read_bytes()
good = (S / "receipts" / "baseline.txt").read_text()
print("== H1: probe-blob absent escape ==")
h1 = S / "hole" / "uncommitted"
if h1.exists():
    shutil.rmtree(h1)
(h1 / "plans").mkdir(parents=True)
(h1 / GRADER_REL).parent.mkdir(parents=True)
(h1 / GRADER_REL).write_bytes((L / GRADER_REL).read_bytes())
# an instrument edited after the run: one comment line appended
edited = probe_bytes + b"# post-run edit\n"
(h1 / PROBE_REL).write_bytes(edited)
import hashlib
edited_sha = hashlib.sha256(edited).hexdigest()
print("edited probe sha256", edited_sha, "(frozen lane blob has 9aef6d33...)")
rec = good.replace(good.splitlines()[0],
                   f"PROBE {PROBE_REL} sha256 {edited_sha}")
rec = "\n".join(ZERO if ln.startswith("PROBE_BLOB ") else ln
                for ln in rec.splitlines()) + "\n"
p = S / "receipts" / "h1-absent.txt"
p.write_text(rec, encoding="utf-8")
r = subprocess.run([sys.executable, str(h1 / PROBE_REL), "--check-receipt", str(p)],
                   capture_output=True, text=True)
print("rc=", r.returncode)
print(r.stdout, end="")
print("H1 rc=%d accepted=%s (edited instrument + forged PROBE_BLOB accepted)"
      % (r.returncode, r.returncode == 0))

print()
print("== H2: duplicate VECTOR line, last-wins ==")
bad_line = "VECTOR K1 FFFFFFFF expected FFFFFFFF agree=True\n"
h2 = good.replace("VECTOR K1 PPPPPPPP expected PPPPPPPP agree=True\n",
                  bad_line + "VECTOR K1 PPPPPPPP expected PPPPPPPP agree=True\n")
p2 = S / "receipts" / "h2-dup-vector.txt"
p2.write_text(h2, encoding="utf-8")
base = S / "lane-baseline"
r2 = subprocess.run([sys.executable, str(base / PROBE_REL), "--check-receipt", str(p2)],
                    capture_output=True, text=True)
print("rc=", r2.returncode)
print(r2.stdout, end="")
print("H2 rc=%d accepted=%s (contradictory K1 vector line present)"
      % (r2.returncode, r2.returncode == 0))

print()
print("== H3: duplicate CASE line, last-wins ==")
h3 = good.replace("CASE K1 case_sha256=", "CASE K1 case_sha256=" + ZERO + " x=0\nCASE K1 case_sha256=", 1)
p3 = S / "receipts" / "h3-dup-case.txt"
p3.write_text(h3, encoding="utf-8")
r3 = subprocess.run([sys.executable, str(base / PROBE_REL), "--check-receipt", str(p3)],
                    capture_output=True, text=True)
print("rc=", r3.returncode)
print(r3.stdout, end="")
print("H3 rc=%d accepted=%s" % (r3.returncode, r3.returncode == 0))

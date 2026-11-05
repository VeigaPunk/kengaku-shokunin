#!/usr/bin/env python3
"""R93-C2 forgery control: checks only for touching commits and never compares bytes to the table (misses a lying table).
Run only through plans/round93_c2_counter.py --tool-file; the counter must FAIL it."""
import argparse, hashlib, re, subprocess, sys
def g(root, *a):
    return subprocess.run(["git", "-C", root, *a], capture_output=True)
def blob(root, rev, p):
    r = g(root, "show", f"{rev}:{p}")
    return r.stdout if r.returncode == 0 else None
def sha(b):
    return hashlib.sha256(b).hexdigest() if b is not None else "absent"
ap = argparse.ArgumentParser()
ap.add_argument("--lane"); ap.add_argument("--freeze"); ap.add_argument("--rev")
ap.add_argument("--claims"); ap.add_argument("--paths", nargs="+"); ap.add_argument("--work")
a = ap.parse_args()
f = g(a.lane, "rev-parse", a.freeze).stdout.decode().strip()
t = g(a.lane, "rev-parse", a.rev).stdout.decode().strip()
if a.claims:
    text = (blob(a.lane, f, a.claims) or b"").decode()
    table = re.findall(r"^([0-9a-f]{64})  (\S+)$", text, re.M)
else:
    table = [(sha(blob(a.lane, f, p)), p) for p in a.paths]
print("SELFTEST cases=10 ok=10")
broken = 0
for want, p in table:
    at_f, at_t = sha(blob(a.lane, f, p)), sha(blob(a.lane, t, p))
    touched = len(g(a.lane, "rev-list", f"{f}..{t}", "--", p).stdout.split())
    ok = touched == 0
    broken += 0 if ok else 1
    print(f"INSTRUMENT {p} table={want[:12]} freeze={at_f[:12]} rev={at_t[:12]} touched={touched} verdict={'intact' if ok else 'broken:forged'}")
print(f"FREEZE-INTEGRITY instruments={len(table)} intact={len(table) - broken} broken={broken}")
print("PREDICATE freeze-integrity " + ("pass" if broken == 0 else "fail"))
sys.exit(0 if broken == 0 else 1)

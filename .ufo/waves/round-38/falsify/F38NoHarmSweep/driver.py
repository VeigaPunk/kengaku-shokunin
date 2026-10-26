#!/usr/bin/env python3
"""No-harm sweep driver: run a JSON job list in parallel inside one clone, one log per job.

Usage: driver.py <jobs.json> <clone_root> <receipt_dir> [parallel]
Each job: {"label": str, "cmd": [argv...], "work": optional scratch dir (created), "timeout": seconds}
Writes <receipt_dir>/<label>.log and <receipt_dir>/summary.tsv (label, rc, secs, last stdout/stderr line).
"""
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

jobs_path, clone, rdir = sys.argv[1], sys.argv[2], sys.argv[3]
par = int(sys.argv[4]) if len(sys.argv) > 4 else 6
jobs = json.load(open(jobs_path))
os.makedirs(rdir, exist_ok=True)


def run(job):
    label = job["label"]
    env = dict(os.environ)
    env["TMPDIR"] = job.get("tmpdir", os.environ.get("TMPDIR", "/tmp"))
    if job.get("work"):
        os.makedirs(job["work"], exist_ok=True)
    t0 = time.time()
    try:
        p = subprocess.run(job["cmd"], cwd=clone, env=env, capture_output=True, text=True,
                           timeout=job.get("timeout", 1800))
        out, rc = (p.stdout or "") + (p.stderr or ""), p.returncode
    except subprocess.TimeoutExpired as e:
        out = "TIMEOUT after %ss\n" % job.get("timeout", 1800) + str(e.stdout or "") + str(e.stderr or "")
        rc = 124
    secs = time.time() - t0
    with open(os.path.join(rdir, label + ".log"), "w") as f:
        f.write("$ " + " ".join(job["cmd"]) + "\n[cwd=%s]\n" % clone + out + "\nEXIT=%d SECS=%.2f\n" % (rc, secs))
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return (label, rc, secs, lines[-1] if lines else "")


with ThreadPoolExecutor(max_workers=par) as ex:
    rows = list(ex.map(run, jobs))
with open(os.path.join(rdir, "summary.tsv"), "w") as f:
    for label, rc, secs, last in rows:
        f.write("%s\t%d\t%.2f\t%s\n" % (label, rc, secs, last))
for label, rc, secs, last in rows:
    print("%-34s rc=%-3d %7.2fs  %s" % (label, rc, secs, last[:150]))

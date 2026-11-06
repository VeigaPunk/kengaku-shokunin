#!/usr/bin/env python3
"""Run the frozen R98-C1 counter once per mutant fixture (pristine baseline and
restored run included), 6 at a time.  Writes out/<name>.out and out/<name>.rc."""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path("/fast/scratch/hyaku/kengaku-r98/MutC1")
T = "8e37fc65d5649bb37166fdd6b1657445a8cb55b9"
PRistine = ROOT / "clone"
OUT = ROOT / "out"


def run_one(job):
    name, fixture, rev = job
    env = dict(os.environ)
    env["TMPDIR"] = str(ROOT / "tmp" / name)
    os.makedirs(env["TMPDIR"], exist_ok=True)
    out = OUT / f"{name}.out"
    with out.open("w") as fh:
        p = subprocess.run(
            [sys.executable, "plans/round98_c1_replay.py", "--lane", ".", "--rev", rev,
             "--work", str(ROOT / "w" / name), "--grader-venv", str(ROOT / "G")],
            cwd=fixture, env=env, stdout=fh, stderr=subprocess.STDOUT)
    (OUT / f"{name}.rc").write_text(str(p.returncode) + "\n")
    print(f"{name} rc={p.returncode}", flush=True)
    return name, p.returncode


def main(names):
    manifest = {m["name"]: m for m in json.loads((ROOT / "manifest.json").read_text())}
    jobs = []
    if "baseline" in names:
        jobs.append(("baseline", str(PRistine), T))
    if "restored" in names:
        jobs.append(("restored", str(ROOT / "mutants" / "r1_lanetip_nonancestor"), T))
    for n in names:
        if n in ("baseline", "restored"):
            continue
        m = manifest[n]
        jobs.append((n, m["fixture"], m["commit"]))
    OUT.mkdir(exist_ok=True)
    jobs = [j for j in jobs if not (OUT / f"{j[0]}.rc").exists()]
    print(f"{len(jobs)} jobs to run", flush=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        for name, rc in pool.map(run_one, jobs):
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

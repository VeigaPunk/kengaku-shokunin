#!/usr/bin/env python3
"""Run every mutant fixture through the proposal copy's --check-receipt --strict.

Records probe sha, fixture sha before/after, exit code, the first default-mode
finding, the first strict defect, the full stdout/stderr, and the gate's own
`CHECK strict probe sha256=` line. Never writes to the lane.
"""
import hashlib
import json
import os
import pathlib
import subprocess
import sys

PROBE = pathlib.Path(sys.argv[1]).resolve()
FIX = pathlib.Path(sys.argv[2]).resolve()
OUT = pathlib.Path(sys.argv[3]).resolve()
OUT.mkdir(parents=True, exist_ok=True)


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


env = dict(os.environ)
env["TMPDIR"] = str(OUT.parent)
env["PYTHONDONTWRITEBYTECODE"] = "1"
results = []
for fixture in sorted(FIX.glob("*.txt")):
    before = sha(fixture)
    proc = subprocess.run(
        [sys.executable, str(PROBE), "--check-receipt", str(fixture), "--strict"],
        capture_output=True, text=True, env=env, cwd=str(OUT.parent), timeout=120)
    after = sha(fixture)
    out = proc.stdout.splitlines()
    strict_sha = next((l.split("sha256=")[1].split()[0] for l in out
                       if l.startswith("CHECK strict probe sha256=")), "(none)")
    first_fail = next((l for l in out if l.startswith("CHECK fail ")), "(none)")
    first_defect = next((l for l in out if l.startswith("CHECK defect:")), "(none)")
    predicate = next((l for l in out if l.startswith("PREDICATE ")), "(none)")
    (OUT / (fixture.stem + ".txt")).write_text(
        "$ python3 %s --check-receipt %s --strict\n"
        "exit=%d\n--- stdout ---\n%s--- stderr ---\n%s"
        "probe_sha=%s fixture_sha_before=%s fixture_sha_after=%s\n"
        % (PROBE, fixture, proc.returncode, proc.stdout, proc.stderr,
           sha(PROBE), before, after))
    row = dict(fixture=fixture.name, exit=proc.returncode,
               strict_probe_sha=strict_sha, first_default_finding=first_fail,
               first_strict_defect=first_defect, predicate=predicate,
               sha_before=before, sha_after=after, unchanged=(before == after),
               defect_count=sum(1 for l in out if l.startswith("CHECK defect:")),
               fail_count=sum(1 for l in out if l.startswith("CHECK fail ")))
    results.append(row)
    print("%-46s exit=%d fails=%d defects=%d | %s | %s"
          % (fixture.stem, row["exit"], row["fail_count"], row["defect_count"],
             row["predicate"], row["first_strict_defect"]))

(OUT / "results.json").write_text(json.dumps(
    {"probe": str(PROBE), "probe_sha": sha(PROBE), "results": results}, indent=2) + "\n")
print("probe_sha %s" % sha(PROBE))

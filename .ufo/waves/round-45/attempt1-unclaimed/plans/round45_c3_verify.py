#!/usr/bin/env python3
"""Round-45 C3 counter (novelty): re-measures the 14-task F1 answer-leak census from pinned captures.

Frozen predicate: `python3 plans/round45_c3_verify.py --lane .` prints `checks=9 defects=0`, then
`PREDICATE C3 pass`, exit 0, on a clean clone of the landing tip.

The census is a new measurement construct: the grader's literal answer token, non-test literal channels, and
published artefact channels are enumerated per task and compared to an instrument-generated receipt. The 2026-10-26
round-44 labrat report established 14/14 answer leaks; this counter tests the frozen remeasurement, not the
historical claim. The prior-art receipt is pinned and required by V9.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import tempfile

SPEC = "plans/census-spec-r45.json"
SPEC_SHA256 = "FROZEN-FILL"
INSTRUMENT = "plans/f1_leak_census.py"
INSTRUMENT_SHA256 = "FROZEN-FILL"
RECEIPT = "corpus/evidence/round45/f1-leak-census.txt"
RECEIPT_SHA256 = "FROZEN-FILL"
PRIOR_ART = "corpus/evidence/round45/prior-art.txt"
PRIOR_ART_SHA256 = "FROZEN-FILL"
CAPTURES = {
    "corpus/evidence/round45/f1-census": "FROZEN-FILL",
    "corpus/evidence/round45/tb2-password-recovery": "FROZEN-FILL",
    "corpus/evidence/round44/tb2-feal-linear-cryptanalysis": "FROZEN-FILL",
}
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"


def sha256(p):
    try:
        return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
    except OSError:
        return None


def v1(lane):
    bad = []
    for rel, digest in CAPTURES.items():
        if sha256(lane / rel / "SHA256SUMS") != digest:
            bad.append(rel + "/SHA256SUMS")
    return not bad, f"capture_manifests={len(CAPTURES)} bad={bad or 0}"


def v2(lane):
    bad = [r for r, d in ((SPEC, SPEC_SHA256), (INSTRUMENT, INSTRUMENT_SHA256)) if sha256(lane / r) != d]
    return not bad, f"pins={2-len(bad)}/2 bad={bad or 0}"


def run_census(lane):
    r = subprocess.run([sys.executable, str(lane / INSTRUMENT), "--lane", str(lane)],
                       capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout


def v3(lane):
    rc, out = run_census(lane)
    good = rc == 0 and "spec_mismatches=0" in out
    return good, f"instrument_exit={rc} spec_mismatches={'0' if good else 'nonzero'}"


def v4(lane):
    if sha256(lane / RECEIPT) != RECEIPT_SHA256:
        return False, "receipt not at freeze digest"
    rc, out = run_census(lane)
    same = rc == 0 and out == (lane / RECEIPT).read_text()
    return same, f"rerun_exit={rc} byte_equal={same}"


def v5(lane):
    spec = json.loads((lane / SPEC).read_text())
    tasks = spec.get("tasks", {})
    if len(tasks) != 14:
        return False, f"task_count={len(tasks)} expected=14"
    missing = []
    for name, t in tasks.items():
        cap = lane / t["capture"]
        for n in t["decide_lines"]:
            if n < 1 or not (cap / t["grader"]).is_file() or n > len((cap / t["grader"]).read_text().splitlines()):
                missing.append(f"{name}:{n}")
        for rel in t["env_files"]:
            if not (cap / rel).is_file():
                missing.append(f"{name}:{rel}")
    return not missing, f"task_rows={len(tasks)} bad={missing or 0}"


def v6(lane):
    r = subprocess.run([CENSUS, "validate", "--file", str(lane / "corpus/SOURCES.md")],
                       capture_output=True, text=True, timeout=300)
    return r.returncode == 0, f"census_exit={r.returncode}"


def v7(lane):
    try:
        text = (lane / RECEIPT).read_text()
        entry = (lane / "corpus/knowledge/f1-answer-leak-census.md").read_text()
    except OSError:
        return False, "receipt or entry absent"
    want = [l.split()[1:] for l in text.splitlines() if l.startswith("TASK ")]
    got = [l.split("`", 2)[1] for l in entry.splitlines() if l.startswith("| `") and "TASK" not in l]
    all_named = all(name in entry for name, *_rest in want)
    summary = [l for l in text.splitlines() if l.startswith("census ")]
    ok = len(want) == 14 and all_named and len(summary) == 1
    return ok, f"tasks={len(want)} entry_names_all={all_named} summary={len(summary)}"


def v8(lane):
    spec = json.loads((lane / SPEC).read_text())
    receipt = (lane / RECEIPT).read_text()
    want = {"tasks": len(spec["tasks"])}
    m = re.search(r"^census tasks=(\d+) grader_literal=(\d+) nt_any=(\d+) derivable=(\d+) no_leak=(\d+) spec_mismatches=(\d+)$",
                  receipt, re.M)
    if not m:
        return False, "summary absent or malformed"
    counts = list(map(int, m.groups()))
    ok = counts[0] == want["tasks"] and counts[1] == 14 and counts[2] == 14 and counts[3] >= 5 and counts[4] == 0 and counts[5] == 0
    return ok, f"summary={counts}"


def v9(lane):
    p = lane / PRIOR_ART
    if sha256(p) != PRIOR_ART_SHA256:
        return False, "prior-art receipt not at freeze digest"
    text = p.read_text()
    ok = all(x in text for x in ("2026-10-26", "VERDICT:", "https://"))
    return ok, f"dated={('2026-10-26' in text)} verdict={'VERDICT:' in text} url={'https://' in text}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    if a.work:
        pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    checks = [v1, v2, v3, v4, v5, v6, v7, v8, v9]
    defects = 0
    for i, fn in enumerate(checks, 1):
        try:
            ok, note = fn(lane)
        except Exception as e:
            ok, note = False, f"error {type(e).__name__}: {e}"
        defects += not ok
        print(f"V{i} {'ok' if ok else 'DEFECT'} {note}")
    print(f"checks={len(checks)} defects={defects}")
    print(f"PREDICATE C3 {'pass' if defects == 0 else 'fail'}")
    return 0 if defects == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Record the same CLI detectors and mapping diagnostics for one byte state."""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument("--root", type=Path, required=True)
parser.add_argument("--receipts", type=Path, required=True)
parser.add_argument("--phase", choices=("pristine", "mutated", "restored"), required=True)
args = parser.parse_args()
script = args.root / "plans/config_projection.py"
receipt = args.receipts / args.phase
receipt.mkdir(parents=True, exist_ok=False)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def detector(mode):
    command = [sys.executable, "-B", str(script), mode, "--root", str(args.root)]
    started = time.monotonic()
    timed_out = False
    try:
        process = subprocess.run(command, capture_output=True, timeout=120)
        stdout, stderr, code = process.stdout, process.stderr, process.returncode
    except subprocess.TimeoutExpired as error:
        stdout, stderr, code = error.stdout or b"", error.stderr or b"", None
        timed_out = True
    stem = mode.removeprefix("--")
    (receipt / (stem + ".stdout")).write_bytes(stdout)
    (receipt / (stem + ".stderr")).write_bytes(stderr)
    return {"mode": mode, "command": command, "exit_code": code, "timed_out": timed_out,
            "elapsed_seconds": round(time.monotonic() - started, 6),
            "stdout_bytes": len(stdout), "stderr_bytes": len(stderr),
            "stdout_sha256": sha(stdout), "stderr_sha256": sha(stderr)}


with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    detectors = list(pool.map(detector, ("--selftest", "--summary", "--json")))

module = runpy.run_path(str(script), run_name="probe_inert_module")
fixture_path = args.root / "plans/fixtures/r29/hand/index-shuffled-ids.fixture.json"
fixture = json.loads(fixture_path.read_bytes())
hand_result, hand_findings = module["audit_text"](
    fixture["input_raw_text"],
    {fixture["profile_name"]: {"purpose": "hand", "values": fixture["profile_values"]}},
)
hand_tasks = hand_result["profiles"][fixture["profile_name"]]["tasks"]
actual_records = [{"task_id": task["task_id"], "output_ordinal": task["output_index"],
                   "output_filename": task["output_filename"], "projected_task": task["projected_task"]}
                  for task in hand_tasks]
hand_mismatches = []
for index, (expected, actual) in enumerate(zip(fixture["expected_records"], actual_records, strict=True)):
    for key in expected:
        if expected[key] != actual[key]:
            hand_mismatches.append({"fixture_path": "/expected_records/%d/%s" % (index, key),
                                    "actual_path": "/profiles/%s/tasks/%d/%s" % (fixture["profile_name"], index, "output_index" if key == "output_ordinal" else key),
                                    "expected": expected[key], "actual": actual[key]})
hand = {"fixture_sha256": sha(fixture_path.read_bytes()), "case_id": fixture["case_id"],
        "actual_records": actual_records, "mismatch_count": len(hand_mismatches),
        "mismatches": hand_mismatches, "findings": hand_findings,
        "index_mapping": hand_result["index_mapping"]}
(receipt / "hand-diagnostic.json").write_text(json.dumps(hand, indent=2) + "\n")

frozen = None
if next(record for record in detectors if record["mode"] == "--json")["exit_code"] == 0:
    frozen_result = json.loads((receipt / "json.stdout").read_bytes())
    raw = json.loads((args.root / module["RAW"]).read_bytes())
    frozen = {"raw_task_count": len(raw),
              "raw_index_task_id_mismatches": [{"index": index, "task_id": task["task_id"]}
                                                for index, task in enumerate(raw) if index != task["task_id"]],
              "population": frozen_result["population"], "findings": frozen_result["findings"],
              "index_mapping": frozen_result["index_mapping"], "profiles": {}}
    for profile, record in frozen_result["profiles"].items():
        mismatches = [{"path": "/profiles/%s/tasks/%d/output_filename" % (profile, index),
                       "expected": "config_files/%d.json" % index, "actual": task["output_filename"]}
                      for index, task in enumerate(record["tasks"])
                      if task["output_filename"] != "config_files/%d.json" % index]
        frozen["profiles"][profile] = {"task_count": len(record["tasks"]),
                                        "filename_mismatch_count": len(mismatches), "mismatches": mismatches}
    (receipt / "frozen-diagnostic.json").write_text(json.dumps(frozen, indent=2) + "\n")

result = {"phase": args.phase, "instrument_sha256": sha(script.read_bytes()), "detectors": detectors,
          "hand_mismatch_count": len(hand_mismatches), "hand_mismatches": hand_mismatches,
          "frozen_raw_task_count": None if frozen is None else frozen["raw_task_count"],
          "frozen_index_task_id_mismatch_count": None if frozen is None else len(frozen["raw_index_task_id_mismatches"]),
          "frozen_profiles": None if frozen is None else frozen["profiles"]}
(receipt / "detector-result.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
for mode in ("selftest", "summary"):
    stdout = (receipt / (mode + ".stdout")).read_text()
    stderr = (receipt / (mode + ".stderr")).read_text()
    print("%s %s stdout:" % (args.phase, mode))
    print(stdout if mode == "selftest" else "\n".join(line for line in stdout.splitlines() if line.startswith(("POPULATION ", "INDEX ", "TOTAL "))))
    if stderr:
        print("%s %s stderr:" % (args.phase, mode))
        print(stderr)

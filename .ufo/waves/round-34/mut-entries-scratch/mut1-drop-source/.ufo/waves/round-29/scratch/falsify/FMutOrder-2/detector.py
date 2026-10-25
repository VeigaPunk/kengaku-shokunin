#!/usr/bin/env python3
"""One bounded detector, reused unchanged for all three byte states."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time

sys.dont_write_bytecode = True
parser = argparse.ArgumentParser()
parser.add_argument("phase", choices=("pristine", "mutated", "restored"))
args = parser.parse_args()
root = Path("/tmp/KengakuR29-2.FMutOrder-2.WuoW6r")
lane = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
evidence = Path(__file__).resolve().parent
script = root / "plans/config_projection.py"
phase_dir = evidence / args.phase
phase_dir.mkdir(exist_ok=True)
tracked = (
    "plans/config_projection.py",
    "plans/fixtures/r29/manifest.json",
    "plans/fixtures/r29/generate_test_data.py",
    "plans/fixtures/r29/profiles.json",
    "plans/fixtures/r28/webarena/config_files/test.raw.json",
    "plans/fixtures/r29/hand/cascade-order.case.json",
    "plans/fixtures/r29/hand/url-only.fixture.json",
    "plans/fixtures/r29/hand/url-only.expected.json",
    "plans/fixtures/r29/hand/index-shuffled-ids.fixture.json",
)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

hashes = {scope: {p: digest(base / p) for p in tracked} for scope, base in (("copy", root), ("lane", lane))}

def run_mode(mode):
    command = [sys.executable, str(script), mode, "--root", str(root)]
    started = time.monotonic()
    try:
        result = subprocess.run(command, capture_output=True, timeout=60, check=False, cwd=root)
        record = {"argv": command, "exit_code": result.returncode, "timeout_seconds": 60}
        stdout, stderr = result.stdout, result.stderr
    except subprocess.TimeoutExpired as error:
        record = {"argv": command, "exit_code": None, "timeout_seconds": 60, "timed_out": True}
        stdout, stderr = error.stdout or b"", error.stderr or b""
    record["elapsed_seconds"] = round(time.monotonic() - started, 6)
    stem = mode.removeprefix("--")
    (phase_dir / (stem + ".stdout.txt")).write_bytes(stdout)
    (phase_dir / (stem + ".stderr.txt")).write_bytes(stderr)
    record["stdout_sha256"] = hashlib.sha256(stdout).hexdigest()
    record["stderr_sha256"] = hashlib.sha256(stderr).hexdigest()
    record["stdout_bytes"] = len(stdout)
    record["stderr_bytes"] = len(stderr)
    if mode == "--json" and record["exit_code"] == 0:
        parsed = json.loads(stdout)
        record["population"] = parsed["population"]
        record["findings"] = parsed["findings"]
        record["projected_text_sha256"] = {name: p["projected_text_sha256"] for name, p in parsed["profiles"].items()}
    return stem, record

with ThreadPoolExecutor(max_workers=3) as pool:
    results = dict(pool.map(run_mode, ("--selftest", "--summary", "--json")))

# Localize the exact hand assertion operands without changing or bypassing the CLI detector.
spec = importlib.util.spec_from_file_location("isolated_projection_probe", script)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
case = json.loads((root / "plans/fixtures/r29/hand/cascade-order.case.json").read_text())
text, steps = module.project(case["raw_serialized_text"], case["values"])
actual_hits = [step["applied_replacements"] for step in steps]
actual_order = [step["name"] for step in steps]
expected_text = case["expected_projected_text"]
expected_hits = case["expected_dynamic_replacement_hits_by_source_step"]
expected_order = case["source_order"]
mismatches = []
for field, expected, actual in (("projected_text", expected_text, text), ("dynamic_replacement_hits_by_source_step", expected_hits, actual_hits), ("replacement_step_names", expected_order, actual_order)):
    if actual != expected:
        mismatches.append({"location": "plans/config_projection.py:selftest:438/cascade-order.case.json:" + field, "expected": expected, "actual": actual})
expected_task, actual_task = json.loads(expected_text)[0], json.loads(text)[0]
if expected_task["start_url"] != actual_task["start_url"]:
    mismatches.append({"location": "hand_projection:/0/start_url", "expected": expected_task["start_url"], "actual": actual_task["start_url"]})
expected_remaining = case["expected_remaining_known_token_occurrences"]
actual_remaining = sum(text.count("__%s__" % name) for name in expected_order)
if expected_remaining != actual_remaining:
    mismatches.append({"location": "cascade-order.case.json:29:expected_remaining_known_token_occurrences", "expected": expected_remaining, "actual": actual_remaining})
summary = {
    "writer": "KengakuR29-2.FMutOrder-2",
    "phase": args.phase,
    "python_version": sys.version,
    "hashes": hashes,
    "detectors": results,
    "hand_probe": {"case_id": case["case_id"], "actual_text": text, "expected_text": expected_text, "actual_hits": actual_hits, "expected_hits": expected_hits, "actual_order": actual_order, "expected_order": expected_order, "actual_remaining_known_token_occurrences": actual_remaining, "expected_remaining_known_token_occurrences": expected_remaining, "mismatches": mismatches},
}
(phase_dir / "receipt.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
for mode in ("selftest", "summary"):
    print("=== %s stdout ===" % mode)
    print((phase_dir / (mode + ".stdout.txt")).read_text(), end="")
    print("=== %s stderr ===" % mode)
    print((phase_dir / (mode + ".stderr.txt")).read_text(), end="")

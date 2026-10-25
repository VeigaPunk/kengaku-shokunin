#!/usr/bin/env python3
"""Capture the identical bounded selftest and witness for one immutable script state."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE / "lane"
PRODUCTION = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
INPUTS = (
    "plans/benchmark_spec_audit.py",
    "plans/fixtures/r28/contract-expected.json",
    "plans/fixtures/r28/webarena/manifest.json",
    "plans/fixtures/r28/webarena/selected-task-ids.json",
    "plans/fixtures/r28/webarena/LICENSE",
    "plans/fixtures/r28/webarena/config_files/test.raw.json",
    "plans/fixtures/r28/webarena/evaluation_harness/evaluators.py",
    "plans/fixtures/r28/webarena/evaluation_harness/helper_functions.py",
)

def hashes(root):
    return {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in INPUTS}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

parser = argparse.ArgumentParser()
parser.add_argument("phase", choices=("pristine", "mutated", "restored"))
args = parser.parse_args()
output = HERE / args.phase
output.mkdir(exist_ok=False)
environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TMPDIR=str(HERE / "temp"))
commands = {
    "stock-selftest": [sys.executable, "-B", str(ROOT / "plans/benchmark_spec_audit.py"), "--root", str(ROOT), "--selftest"],
    "independent-witness": [sys.executable, "-B", str(HERE / "witness.py")],
}
record = {
    "phase": args.phase,
    "python": sys.version,
    "production_before": hashes(PRODUCTION),
    "scratch_before": hashes(ROOT),
    "backup_sha256": digest(HERE / "benchmark_spec_audit.pristine.py"),
    "detector_sha256": digest(Path(__file__).resolve()),
    "witness_sha256": digest(HERE / "witness.py"),
    "witness_spec_sha256": digest(HERE / "duplicate-witness.json"),
    "commands": {},
}

def run(item):
    name, command = item
    try:
        result = subprocess.run(command, cwd=HERE, env=environment, capture_output=True, text=True, timeout=30)
        captured = {"command": command, "exit": result.returncode, "stdout": result.stdout, "stderr": result.stderr, "timed_out": False}
    except subprocess.TimeoutExpired as error:
        captured = {"command": command, "exit": None, "stdout": str(error.stdout or ""), "stderr": str(error.stderr or ""), "timed_out": True}
    (output / (name + ".stdout")).write_text(captured["stdout"])
    (output / (name + ".stderr")).write_text(captured["stderr"])
    (output / (name + ".exit.txt")).write_text(str(captured["exit"]) + "\n")
    return name, captured

with ThreadPoolExecutor(max_workers=2) as executor:
    record["commands"] = dict(executor.map(run, commands.items()))
record["production_after"] = hashes(PRODUCTION)
record["scratch_after"] = hashes(ROOT)
record["production_unchanged_during_probe"] = record["production_before"] == record["production_after"]
record["scratch_unchanged_during_probe"] = record["scratch_before"] == record["scratch_after"]
record["detector_clean"] = all(result["exit"] == 0 for result in record["commands"].values())
(output / "capture.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
print(json.dumps(record, indent=2, sort_keys=True))
raise SystemExit(0 if record["detector_clean"] else 1)

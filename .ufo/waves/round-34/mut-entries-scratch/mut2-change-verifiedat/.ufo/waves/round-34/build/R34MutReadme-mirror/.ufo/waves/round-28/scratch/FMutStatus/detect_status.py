#!/usr/bin/env python3
"""One hand-expected CLI witness: queued+cited, with complete live used-by."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


root = Path(__file__).resolve().parent
contract = json.loads((root / "expected.json").read_text())
input_sha256 = {
    relative: hashlib.sha256((root / relative).read_bytes()).hexdigest()
    for relative in contract["input_sha256"]
}
command = [
    sys.executable, "-B", str(root / "plans/registry_check.py"),
    "--root", str(root), "--json",
]
record = {
    "command": command,
    "cwd": str(root),
    "python": sys.version,
    "script_sha256": hashlib.sha256((root / "plans/registry_check.py").read_bytes()).hexdigest(),
    "input_sha256": input_sha256,
    "expected_exit": contract["expected_exit"],
    "expected_result": contract["expected_result"],
}
if input_sha256 != contract["input_sha256"]:
    record.update(detector_exit=2, observation="inconclusive_fixture_drift")
else:
    try:
        probe = subprocess.run(
            command, cwd=root, capture_output=True, text=True, timeout=15,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        record.update(actual_exit=probe.returncode, stdout=probe.stdout, stderr=probe.stderr)
        actual = json.loads(probe.stdout)
        record["actual_result"] = actual
        if probe.returncode not in (0, 1):
            record.update(detector_exit=2, observation="inconclusive_cli_setup_exit")
        else:
            matches = (
                probe.returncode == contract["expected_exit"]
                and actual == contract["expected_result"]
                and not probe.stderr
            )
            record.update(
                detector_exit=0 if matches else 1,
                observation="expected_status_failure_observed" if matches else "expected_status_failure_mismatch",
            )
    except (OSError, subprocess.TimeoutExpired, ValueError) as error:
        record.update(detector_exit=2, observation="inconclusive_detector_error", error=repr(error))
print(json.dumps(record, indent=2, sort_keys=True))
raise SystemExit(record["detector_exit"])
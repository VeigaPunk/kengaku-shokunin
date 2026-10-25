#!/usr/bin/env python3
"""Exercise only the assigned lane-owned audit function on hand-authored data."""
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
specification = json.loads((HERE / "duplicate-witness.json").read_text())
script = HERE / "lane/plans/benchmark_spec_audit.py"
spec = importlib.util.spec_from_file_location("fmut_schema_audit", script)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
result = audit.audit_tasks(specification["tasks"], specification["expected_population"])
actual = {
    "findings": result["findings"],
    "duplicate_task_ids": result["duplicate_task_ids"],
    "missing_task_ids": result["missing_task_ids"],
    "unexpected_task_ids": result["unexpected_task_ids"],
    "task_count": result["metrics"]["task_count"],
    "distinct_task_ids": result["metrics"]["distinct_task_ids"],
}
expected = specification["expected"]
matched = actual == expected
print(json.dumps({"matched": matched, "expected": expected, "actual": actual}, indent=2, sort_keys=True))
raise SystemExit(0 if matched else 1)

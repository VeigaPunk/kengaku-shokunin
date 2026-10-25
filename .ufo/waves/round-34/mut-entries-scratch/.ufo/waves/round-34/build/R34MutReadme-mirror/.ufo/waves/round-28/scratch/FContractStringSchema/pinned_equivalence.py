#!/usr/bin/env python3
"""Does the pinned-population output distinguish production from each scratch mutant? (in-process, no upstream code)."""
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
HERE = Path(__file__).resolve().parent
tasks = json.loads((LANE / "plans/fixtures/r28/webarena/config_files/test.raw.json").read_text())


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(module):
    return json.dumps(module.audit_tasks(json.loads(json.dumps(tasks))), sort_keys=True, default=repr)


reference = digest(load(LANE / "plans/benchmark_spec_audit.py"))
ref = json.loads(reference)
print("production pinned: findings", len(ref["findings"]), "task_count", ref["metrics"]["task_count"], "string_operators", ref["metrics"]["string_operators"], "selected", ref["selected_task_ids"])
for path in sorted((HERE / "mut").glob("M*.py")):
    print(path.stem, "IDENTICAL_PINNED_OUTPUT" if digest(load(path)) == reference else "DIFFERS")

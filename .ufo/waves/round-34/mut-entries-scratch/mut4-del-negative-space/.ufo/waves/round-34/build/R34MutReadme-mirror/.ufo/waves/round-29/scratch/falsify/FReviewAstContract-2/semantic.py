#!/usr/bin/env python3
"""Demonstrate that ACCEPTED mutants are semantically different generators.

For each mutant accepted by source_contract(), actually RUN the mutant generator
in a /tmp sandbox with a stub browser_env.env_config (synthetic *.invalid values,
no host env, no network, no credentials) and compare the artifacts it writes with
the artifacts the instrument's projection implies.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

BASE = Path("/tmp/freview-astcontract")
GEN = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/generate_test_data.py")
RAW = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json")
spec = importlib.util.spec_from_file_location("cp", BASE / "config_projection.py")
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)
source = GEN.read_text()
raw_text = RAW.read_text()


def mutant(old, new):
    assert old in source
    return source.replace(old, new, 1)


MUTANTS = {
    "M01_filename_fstring_not_an_open": mutant(
        '        with open(f"config_files/{idx}.json", "w") as f:\n            json.dump(item, f, indent=2)',
        '        name = f"config_files/{idx}.json"\n        print(name)'),
    "M02_filename_single_shared_file": mutant(
        '        with open(f"config_files/{idx}.json", "w") as f:\n            json.dump(item, f, indent=2)',
        '        with open("config_files/all.json", "w") as f:\n            f.write(f"config_files/{idx}.json")'),
    "M03_raw_truncated_after_replaces": mutant(
        "    data = json.loads(raw)",
        "    raw = raw[:100]\n    data = json.loads(raw)"),
    "M05_raw_appended_after_replaces": mutant(
        "    data = json.loads(raw)",
        '    raw = raw + " "\n    data = json.loads(raw)'),
    "M07_data_filtered_before_enumerate": mutant(
        "    for idx, item in enumerate(data):",
        '    data = [d for d in data if d["task_id"] % 2 == 0]\n    for idx, item in enumerate(data):'),
    "M08_data_reversed_before_enumerate": mutant(
        "    for idx, item in enumerate(data):",
        "    data = list(reversed(data))\n    for idx, item in enumerate(data):"),
}

ENV_STUB = """GITLAB = "http://gitlab.invalid:1"
REDDIT = "http://reddit.invalid:2"
SHOPPING = "http://shopping.invalid:3"
SHOPPING_ADMIN = "http://shopping-admin.invalid:4"
WIKIPEDIA = "http://wikipedia.invalid:5"
MAP = "http://map.invalid:6"
"""

out = {}
for name, text in MUTANTS.items():
    try:
        cp.source_contract(text)
    except cp.Unevaluable as error:
        out[name] = {"accepted": False, "reason": error.finding}
        continue
    sand = BASE / "sandbox" / name
    if sand.exists():
        shutil.rmtree(sand)
    (sand / "browser_env").mkdir(parents=True)
    (sand / "config_files").mkdir(parents=True)
    (sand / "browser_env" / "__init__.py").write_text("")
    (sand / "browser_env" / "env_config.py").write_text(ENV_STUB)
    (sand / "config_files" / "test.raw.json").write_text(raw_text)
    (sand / "gen.py").write_text(text)
    proc = subprocess.run([sys.executable, "gen.py"], cwd=sand, capture_output=True, text=True, timeout=300)
    files = sorted(p.name for p in (sand / "config_files").iterdir())
    numeric = [f for f in files if f[:-5].isdigit()]
    entry = {}
    if numeric:
        first = json.loads((sand / "config_files" / numeric[0]).read_text())
        entry["file0_task_id"] = first.get("task_id")
        entry["file0_start_url"] = first.get("start_url")
    out[name] = {
        "accepted": True,
        "exit_code": proc.returncode,
        "stderr_tail": proc.stderr.strip().splitlines()[-1:] if proc.stderr else [],
        "config_files_written": len(files),
        "per_index_files": len(numeric),
        "file_names_sample": files[:4],
        "file0_task_id": entry.get("file0_task_id"),
    }
    print(name, json.dumps(out[name], sort_keys=True))

# instrument-side expectation for the same input, profile distinct_origins
profiles = json.loads((BASE.parent.parent / "kengaku-shokunin" / "plans" / "fixtures" / "r29" / "profiles.json").read_text()) \
    if False else json.loads(Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/profiles.json").read_text())
res, findings = cp.audit_text(raw_text, profiles, expected_population=812)
tasks = res["profiles"]["distinct_origins"]["tasks"]
expect = {
    "instrument_output_filename_task0": tasks[0]["output_filename"],
    "instrument_task0_task_id": tasks[0]["task_id"],
    "instrument_task0_start_url": tasks[0]["projected_task"].get("start_url"),
    "instrument_task_count": len(tasks),
    "instrument_claims": res["source_contract_placeholder"] if "source_contract_placeholder" in res else None,
}
print("INSTRUMENT", json.dumps(expect, sort_keys=True))
Path(BASE / "semantic-results.json").write_text(json.dumps({"mutants": out, "instrument": expect}, indent=2, sort_keys=True))

#!/usr/bin/env python3
"""Falsification probe for source_contract() AST extraction strictness.

Imports the COPY of the production instrument (read-only use) and feeds it
mutants of the pinned generator bytes. Reports which mutants are silently
ACCEPTED by source_contract() even though the generator semantics differ.
"""
import importlib.util
import json
import sys
from pathlib import Path

PROD = Path("/tmp/freview-astcontract/config_projection.py")
GEN = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/generate_test_data.py")

spec = importlib.util.spec_from_file_location("cp", PROD)
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)

source = GEN.read_text()


def mutant(name, old, new, count=1):
    assert old in source, name
    text = source.replace(old, new, count)
    assert text != source, name
    return name, text


MUTANTS = [
    mutant("M00_control_unmutated", "x = 1\n", "x = 1\n") if False else ("M00_control_unmutated", source),
    # --- filename template not bound to any open()/write() ---
    mutant("M01_filename_fstring_not_an_open",
            '        with open(f"config_files/{idx}.json", "w") as f:\n            json.dump(item, f, indent=2)',
            '        name = f"config_files/{idx}.json"\n        print(name)'),
    mutant("M02_filename_single_shared_file",
            '        with open(f"config_files/{idx}.json", "w") as f:\n            json.dump(item, f, indent=2)',
            '        with open("config_files/all.json", "w") as f:\n            f.write(f"config_files/{idx}.json")'),
    # --- unrecognized statements that mutate raw are silently ignored ---
    mutant("M03_raw_truncated_after_replaces",
            "    data = json.loads(raw)",
            "    raw = raw[:100]\n    data = json.loads(raw)"),
    mutant("M04_raw_upper_after_replaces",
            "    data = json.loads(raw)",
            "    raw = raw.upper()\n    data = json.loads(raw)"),
    mutant("M05_raw_appended_after_replaces",
            "    data = json.loads(raw)",
            "    raw = raw + \" \"\n    data = json.loads(raw)"),
    mutant("M06_raw_mutated_after_parse",
            "    for idx, item in enumerate(data):",
            "    raw = raw + \" \"\n    for idx, item in enumerate(data):"),
    # --- data mutated between json.loads and enumerate ---
    mutant("M07_data_filtered_before_enumerate",
            "    for idx, item in enumerate(data):",
            "    data = [d for d in data if d[\"task_id\"] % 2 == 0]\n    for idx, item in enumerate(data):"),
    mutant("M08_data_reversed_before_enumerate",
            "    for idx, item in enumerate(data):",
            "    data = list(reversed(data))\n    for idx, item in enumerate(data):"),
    # --- import surface ---
    mutant("M09_relative_star_import",
            "from browser_env.env_config import *",
            "from .browser_env.env_config import *"),
    mutant("M10_star_import_shadowed_by_module_binding",
            "from browser_env.env_config import *",
            "from browser_env.env_config import *\nGITLAB = \"http://shadowed.invalid\""),
    # --- parse / loop ordering ---
    mutant("M11_enumerate_before_json_loads",
            "    data = json.loads(raw)\n    for idx, item in enumerate(data):",
            "    for idx, item in enumerate(data):\n        pass\n    data = json.loads(raw)"),
    # --- input path not extracted ---
    mutant("M12_other_input_file",
            'with open("config_files/test.raw.json", "r") as f:',
            'with open("config_files/other.raw.json", "r") as f:'),
    # --- entry point not extracted ---
    mutant("M13_main_never_invoked",
            'if __name__ == "__main__":\n    main()',
            'if __name__ == "__main__":\n    pass'),
    # --- duplicate parse ---
    mutant("M14_second_json_loads",
            "    for idx, item in enumerate(data):",
            "    data = json.loads(raw)\n    for idx, item in enumerate(data):"),
]


def classify(text):
    try:
        contract = cp.source_contract(text)
    except cp.Unevaluable as error:
        return "REJECT", error.finding
    return "ACCEPT", contract


rows = []
for name, text in MUTANTS:
    status, detail = classify(text)
    row = {"mutant": name, "status": status}
    if status == "REJECT":
        row["reason"] = detail.get("id") + " / " + str(detail.get("detail"))
    else:
        row["contract"] = detail
    rows.append(row)
    print("%-45s %s %s" % (name, status, "" if status == "ACCEPT" else detail.get("detail")))

Path("/tmp/freview-astcontract/probe-results.json").write_text(json.dumps(rows, indent=2, sort_keys=True))
print()
print("ACCEPTED_MUTANTS", json.dumps([r["mutant"] for r in rows if r["status"] == "ACCEPT"]))

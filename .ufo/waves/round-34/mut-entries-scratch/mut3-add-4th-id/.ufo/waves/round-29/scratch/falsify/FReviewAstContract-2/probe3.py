#!/usr/bin/env python3
"""Final consolidated falsification battery for source_contract() AST strictness.

14 well-formed mutants of the pinned generator (semantics changed, shape preserved),
each classified by source_contract() and, when accepted, executed in a /tmp sandbox
with a synthetic stub browser_env.env_config to record the observable difference.
"""
import importlib.util
import json
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

LOOP = '    for idx, item in enumerate(data):\n        with open(f"config_files/{idx}.json", "w") as f:\n            json.dump(item, f, indent=2)\n'
PARSE = "    data = json.loads(raw)\n"
OPEN_RAW = 'with open("config_files/test.raw.json", "r") as f:'

def mut(old, new):
    assert old in source, old
    text = source.replace(old, new, 1)
    assert text != source
    return text

BODY = '        with open(f"config_files/{idx}.json", "w") as f:\n            json.dump(item, f, indent=2)\n'
MUTANTS = {
 "M01_filename_fstring_is_not_an_open": mut(BODY, '        name = f"config_files/{idx}.json"\n        print(name)\n'),
 "M02_filename_all_tasks_share_one_file": mut(BODY, '        with open("config_files/all.json", "w") as f:\n            f.write(f"config_files/{idx}.json")\n'),
 "M03_raw_truncated_before_parse": mut(PARSE, "    raw = raw[:100]\n" + PARSE),
 "M04_raw_uppercased_before_parse": mut(PARSE, "    raw = raw.upper()\n" + PARSE),
 "M05_raw_appended_before_parse": mut(PARSE, '    raw = raw + " "\n' + PARSE),
 "M06_raw_mutated_after_parse": mut(LOOP, '    raw = raw + " "\n' + LOOP),
 "M07_data_filtered_before_enumerate": mut(LOOP, '    data = [d for d in data if d["task_id"] % 2 == 0]\n' + LOOP),
 "M08_data_reversed_before_enumerate": mut(LOOP, "    data = list(reversed(data))\n" + LOOP),
 "M09_relative_star_import": mut("from browser_env.env_config import *", "from .browser_env.env_config import *"),
 "M10_star_import_shadowed_by_module_binding": mut("from browser_env.env_config import *", "from browser_env.env_config import *\nGITLAB = \"http://shadowed.invalid\""),
 "M11_enumerate_loop_before_json_loads": mut(PARSE + LOOP, LOOP + PARSE),
 "M12_other_input_file_read": mut(OPEN_RAW, 'with open("config_files/other.raw.json", "r") as f:'),
 "M13_main_never_invoked": mut('if __name__ == "__main__":\n    main()', 'if __name__ == "__main__":\n    pass'),
 "M14_data_reparsed_from_different_text": mut(PARSE, PARSE + "    data = json.loads(raw.upper())\n"),
}

ENV_STUB = ('GITLAB = "http://gitlab.invalid:1"\nREDDIT = "http://reddit.invalid:2"\nSHOPPING = "http://shopping.invalid:3"\n'
            'SHOPPING_ADMIN = "http://shopping-admin.invalid:4"\nWIKIPEDIA = "http://wikipedia.invalid:5"\nMAP = "http://map.invalid:6"\n')

def execute(name, text):
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
    numeric = sorted([f for f in files if f[:-5].isdigit()], key=lambda n: int(n[:-5]))
    rec = {"exit_code": proc.returncode, "config_files_entries": len(files),
           "per_index_files_written": len(numeric),
           "error_tail": proc.stderr.strip().splitlines()[-1] if proc.stderr else ""}
    if numeric:
        first = json.loads((sand / "config_files" / numeric[0]).read_text())
        rec["file0_task_id"] = first.get("task_id")
        rec["file0_start_url"] = first.get("start_url")
    shadow = sum((sand / "config_files" / f).read_text().count("shadowed.invalid") for f in files)
    rec["shadowed_value_occurrences_in_written_files"] = shadow
    return rec

rows = []
for name, text in [("M00_control_unmutated", source)] + sorted(MUTANTS.items()):
    reason = None
    try:
        contract = cp.source_contract(text)
        status = "ACCEPT"
    except cp.Unevaluable as error:
        contract, status, reason = None, "REJECT", error.finding.get("detail")
    row = {"mutant": name, "status": status}
    if status == "REJECT":
        row["reason"] = reason
    else:
        row["contract_reported"] = {k: contract[k] for k in ("parse_line", "enumerate_loop_line", "per_task_filename_template", "output_index", "env_config_star_import_line")}
        row["execution_witness"] = execute(name, text)
    rows.append(row)
    print("%-42s %-6s %s" % (name, status, json.dumps(row.get("execution_witness", row.get("reason")), sort_keys=True)))

accepted = [r["mutant"] for r in rows if r["status"] == "ACCEPT" and r["mutant"] != "M00_control_unmutated"]
print()
print("TOTAL_MUTANTS", len(MUTANTS), "ACCEPTED", len(accepted), "REJECTED", len(MUTANTS) - len(accepted))
Path(BASE / "final-battery.json").write_text(json.dumps(rows, indent=2, sort_keys=True))

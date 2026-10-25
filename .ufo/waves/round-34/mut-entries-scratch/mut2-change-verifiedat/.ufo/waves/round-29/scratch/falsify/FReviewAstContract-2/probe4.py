#!/usr/bin/env python3
"""Re-check at dbcecded: 14 well-formed semantics-changing mutants + semantically inert
variants against the repaired source_contract(). Usage: probe4.py <module.py>"""
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

BASE = Path("/tmp/freview-astcontract")
MODULE = Path(sys.argv[1] if len(sys.argv) > 1 else BASE / "config_projection_dbcecded.py")
GEN = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/generate_test_data.py")
RAW = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r28/webarena/config_files/test.raw.json")
spec = importlib.util.spec_from_file_location("cp", MODULE)
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)
source = GEN.read_text()
raw_text = RAW.read_text()

LOOP = '    for idx, item in enumerate(data):\n        with open(f"config_files/{idx}.json", "w") as f:\n            json.dump(item, f, indent=2)\n'
PARSE = "    data = json.loads(raw)\n"
BODY = '        with open(f"config_files/{idx}.json", "w") as f:\n            json.dump(item, f, indent=2)\n'
OPEN_RAW = 'with open("config_files/test.raw.json", "r") as f:'

def mut(old, new):
    assert old in source, old
    text = source.replace(old, new, 1)
    assert text != source
    return text

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
# semantically inert variants (behaviour-preserving) to characterise residual acceptance
INERT = {
 "S01_comment_added": mut("import json\n", "import json\n# harmless comment\n"),
 "S02_module_docstring_text_changed": source.replace('"""Replace the website placeholders with website domains from env_config',
                                                       '"""Replace the website placeholders with website domains from env_config (wording)'),
 "S03_blank_line_added": mut("import json\n", "import json\n\n"),
 "S04_local_variable_renamed": source.replace("        raw = f.read()", "        rawtext = f.read()"),
}

ENV_STUB = ('GITLAB = "http://gitlab.invalid:1"\nREDDIT = "http://reddit.invalid:2"\nSHOPPING = "http://shopping.invalid:3"\n'
            'SHOPPING_ADMIN = "http://shopping-admin.invalid:4"\nWIKIPEDIA = "http://wikipedia.invalid:5"\nMAP = "http://map.invalid:6"\n')

def execute(name, text):
    sand = BASE / "sandbox2" / name
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
    rec = {"exit_code": proc.returncode, "config_files_entries": len(files), "per_index_files_written": len(numeric),
           "error_tail": proc.stderr.strip().splitlines()[-1] if proc.stderr else ""}
    if numeric:
        first = json.loads((sand / "config_files" / numeric[0]).read_text())
        rec["file0_task_id"] = first.get("task_id")
    return rec

rows = []
for group, table in (("SEMANTICS_CHANGING", MUTANTS), ("SEMANTICALLY_INERT", INERT)):
    for name, text in [("M00_control_unmutated", source)] + sorted(table.items()) if group == "SEMANTICS_CHANGING" else sorted(table.items()):
        reason = None
        try:
            contract = cp.source_contract(text)
            status = "ACCEPT"
        except cp.Unevaluable as error:
            contract, status, reason = None, "REJECT", error.finding
        row = {"group": group, "mutant": name, "status": status}
        if status == "REJECT":
            row["finding"] = reason
        else:
            row["contract_claims"] = {k: contract[k] for k in ("parse_line", "enumerate_loop_line", "per_task_filename_template", "output_index", "env_config_star_import_line")}
            row["execution_witness"] = execute(name, text)
        rows.append(row)
        print("%-20s %-42s %-6s %s" % (group, name, status, "" if status == "ACCEPT" else json.dumps(reason, sort_keys=True)[:150]))

changing = [r for r in rows if r["group"] == "SEMANTICS_CHANGING" and r["mutant"] != "M00_control_unmutated"]
inert = [r for r in rows if r["group"] == "SEMANTICALLY_INERT"]
print()
print("SEMANTICS_CHANGING total=%d accepted=%d rejected=%d" % (len(changing), sum(r["status"] == "ACCEPT" for r in changing), sum(r["status"] == "REJECT" for r in changing)))
print("ACCEPTED_SEMANTICS_CHANGING", json.dumps([r["mutant"] for r in changing if r["status"] == "ACCEPT"]))
print("SEMANTICALLY_INERT total=%d accepted=%d rejected=%d" % (len(inert), sum(r["status"] == "ACCEPT" for r in inert), sum(r["status"] == "REJECT" for r in inert)))
print("ACCEPTED_INERT", json.dumps([r["mutant"] for r in inert if r["status"] == "ACCEPT"]))
print("CONTROL", json.dumps([r["status"] for r in rows if r["mutant"] == "M00_control_unmutated"]))
Path(BASE / ("recheck-" + MODULE.stem + ".json")).write_text(json.dumps(rows, indent=2, sort_keys=True))

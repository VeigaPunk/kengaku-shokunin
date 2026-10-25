#!/usr/bin/env python3
"""Write string/eval-type mutants of the audit into scratch, run each mutant's own selftest and the probe battery."""
import json
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
HERE = Path(__file__).resolve().parent
SOURCE = (LANE / "plans/benchmark_spec_audit.py").read_text()
MUTANTS = {
    "M01_drop_duplicate_eval_type": ('        if len(kinds) != len(set(kinds)):\n            fail("duplicate_eval_type")\n', ""),
    "M02_exact_any_type": ('(operator == "exact_match" and isinstance(value, str))', '(operator == "exact_match")'),
    "M03_must_any_elements": ('(operator == "must_include" and isinstance(value, list) and all(isinstance(v, str) for v in value))', '(operator == "must_include" and isinstance(value, list))'),
    "M04_fuzzy_any_elements": ('(value == "N/A" or isinstance(value, list) and all(isinstance(v, str) for v in value))', '(value == "N/A" or isinstance(value, list))'),
    "M05_accept_empty_refs": ("if not isinstance(refs, dict) or not refs:", "if not isinstance(refs, dict):"),
    "M06_coerce_none_refs": ('refs = evaluation.get("reference_answers", {})', 'refs = evaluation.get("reference_answers") or {}'),
    "M07_accept_empty_eval_types": ("kinds_ok = isinstance(kinds, list) and bool(kinds) and all", "kinds_ok = isinstance(kinds, list) and all"),
    "M08_note_presence_only": ('not isinstance(evaluation.get("string_note"), str)', '"string_note" not in evaluation'),
    "M09_drop_approach_order": ('records[-1]["reference_approach_order"] = list(refs) if isinstance(refs, dict) else None', 'records[-1]["reference_approach_order"] = None'),
    "M10_skip_unknown_when_string": ('            if kind not in TYPES:', '            if kind not in TYPES and "string_match" not in kinds:'),
    "M11_list_refs_accepted": ("if not isinstance(refs, dict) or not refs:\n                fail(\"reference_answers_invalid\")\n            else:\n                for operator, value in refs.items():",
                               "if not refs:\n                fail(\"reference_answers_invalid\")\n            elif isinstance(refs, dict):\n                for operator, value in refs.items():"),
}
results = {}
for name, (old, new) in MUTANTS.items():
    assert SOURCE.count(old) == 1, name
    path = HERE / "mut" / f"{name}.py"
    path.parent.mkdir(exist_ok=True)
    path.write_text(SOURCE.replace(old, new))
    env = {"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin"}
    selftest = subprocess.run([sys.executable, "-B", str(path), "--root", str(LANE), "--selftest"], capture_output=True, text=True, env=env)
    probe = subprocess.run([sys.executable, "-B", str(HERE / "probe.py"), str(path)], capture_output=True, text=True, env=env)
    cases = json.loads(probe.stdout)["cases"]
    record_delta = []
    if cases["N01_nonactive_none"]["record_reference_answers"] is not None:
        record_delta.append("N01_record_refs_not_None")
    if cases["A01_exact_ok"]["record_approach_order"] != ["exact_match"]:
        record_delta.append("A01_approach_order_lost")
    results[name] = {"selftest_exit": selftest.returncode, "selftest_tail": (selftest.stdout + selftest.stderr).strip().splitlines()[-1][:160],
                     "probe_mismatch": json.loads(probe.stdout)["mismatch"], "record_delta": record_delta}
print(json.dumps(results, indent=1))

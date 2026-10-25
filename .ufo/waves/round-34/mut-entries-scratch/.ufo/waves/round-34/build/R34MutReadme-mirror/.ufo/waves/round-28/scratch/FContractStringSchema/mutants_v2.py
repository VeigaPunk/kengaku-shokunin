#!/usr/bin/env python3
"""Re-anchored v1 mutants plus controls for the v2 repairs; each mutant's own selftest, probe_v2, pinned equivalence."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
HERE = Path(__file__).resolve().parent
SOURCE = (LANE / "plans/benchmark_spec_audit.py").read_text()
STRING_GUARD = 'if not isinstance(refs, dict):\n                fail("reference_answers_invalid")'
MUTANTS = {
    # v1 mutants, re-anchored where the v2 text moved.
    "M01_drop_duplicate_eval_type": ('        if len(kinds) != len(set(kinds)):\n            fail("duplicate_eval_type")\n', ""),
    "M02_exact_any_type": ('(operator == "exact_match" and isinstance(value, str))', '(operator == "exact_match")'),
    "M03_must_any_elements": ('(operator == "must_include" and isinstance(value, list) and all(isinstance(v, str) for v in value))', '(operator == "must_include" and isinstance(value, list))'),
    "M04_fuzzy_any_elements": ('(value == "N/A" or isinstance(value, list) and all(isinstance(v, str) for v in value))', '(value == "N/A" or isinstance(value, list))'),
    "M05r_reject_empty_refs": (STRING_GUARD, 'if not isinstance(refs, dict) or not refs:\n                fail("reference_answers_invalid")'),
    "M06_coerce_none_refs": ('refs = evaluation.get("reference_answers")\n', 'refs = evaluation.get("reference_answers") or {}\n'),
    "M07_accept_empty_eval_types": ("kinds_ok = isinstance(kinds, list) and bool(kinds) and all", "kinds_ok = isinstance(kinds, list) and all"),
    "M08_note_presence_only": ('not isinstance(evaluation.get("string_note"), str)', '"string_note" not in evaluation'),
    "M09_drop_approach_order": ('records[-1]["reference_approach_order"] = list(refs) if isinstance(refs, dict) else None', 'records[-1]["reference_approach_order"] = None'),
    "M10_skip_unknown_when_string": ('            if kind not in TYPES:', '            if kind not in TYPES and "string_match" not in kinds:'),
    "M11_list_refs_accepted": (STRING_GUARD + "\n            else:\n                for operator, value in refs.items():",
                               'if refs is None:\n                fail("reference_answers_invalid")\n            elif isinstance(refs, dict):\n                for operator, value in refs.items():'),
    # Controls for the v2 repairs named by KengakuR28.
    "R01_mask_again_on_invalid_types": ("kinds = [value for value in kinds if isinstance(value, str)] if isinstance(kinds, list) else []", "kinds = []"),
    "R02_unlabeled_invalid_bucket": ('counts["eval_type_sets"][",".join(sorted(kinds)) if kinds_ok else "<INVALID>"] += 1', 'counts["eval_type_sets"][",".join(sorted(kinds))] += 1'),
    "R03_unlabeled_invalid_order_bucket": ('counts["eval_type_orders"][",".join(kinds) if kinds_ok else "<INVALID>"] += 1', 'counts["eval_type_orders"][",".join(kinds)] += 1'),
    "R04_record_filtered_types": ('"eval_types": evaluation.get("eval_types"),', '"eval_types": kinds,'),
    "R05_invent_absent_refs": ('refs = evaluation.get("reference_answers")\n', 'refs = evaluation.get("reference_answers", {})\n'),
    "R06_presence_always_true": ('"reference_answers_present": "reference_answers" in evaluation,', '"reference_answers_present": True,'),
    "R07_strata_admit_invalid_types": ("if sites_ok and kinds_ok and type(tid) is int:", "if sites_ok and type(tid) is int:"),
    "R08_string_checks_only_when_types_valid": ('        if "string_match" in kinds:\n            if not isinstance(refs, dict):', '        if kinds_ok and "string_match" in kinds:\n            if not isinstance(refs, dict):'),
    "R09_duplicate_only_when_types_valid": ("        if len(kinds) != len(set(kinds)):", "        if kinds_ok and len(kinds) != len(set(kinds)):"),
}


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tasks_text = (LANE / "plans/fixtures/r28/webarena/config_files/test.raw.json").read_text()
def pinned(module):
    return json.dumps(module.audit_tasks(json.loads(tasks_text)), sort_keys=True, default=repr)


reference = pinned(load(LANE / "plans/benchmark_spec_audit.py"))
ref = json.loads(reference)
print("production pinned: findings", len(ref["findings"]), "string_operators", ref["metrics"]["string_operators"],
      "eval_type_sets", ref["metrics"]["eval_type_sets"], "selected", ref["selected_task_ids"],
      "refs_present_false", sum(1 for t in ref["tasks"] if not t["reference_answers_present"]),
      "nonactive_refs_none", sum(1 for t in ref["tasks"] if "string_match" not in t["eval_types"] and t["reference_answers"] is None))
env = {"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin"}
results = {}
for name, (old, new) in MUTANTS.items():
    assert SOURCE.count(old) == 1, (name, SOURCE.count(old))
    path = HERE / "mut_v2" / f"{name}.py"
    path.parent.mkdir(exist_ok=True)
    path.write_text(SOURCE.replace(old, new))
    selftest = subprocess.run([sys.executable, "-B", str(path), "--root", str(LANE), "--selftest"], capture_output=True, text=True, env=env)
    probe = subprocess.run([sys.executable, "-B", str(HERE / "probe_v2.py"), str(path)], capture_output=True, text=True, env=env)
    tail = (selftest.stdout + selftest.stderr).strip().splitlines()[-1]
    results[name] = {"selftest_exit": selftest.returncode, "selftest_tail": tail[:200], "probe_kills": json.loads(probe.stdout)["mismatch"],
                     "pinned_identical": pinned(load(path)) == reference}
    print(name, "selftest_exit", selftest.returncode, "| probe_v2 kills", results[name]["probe_kills"], "| pinned identical", results[name]["pinned_identical"], "|", tail[:110])
(HERE / "mutants_v2.json").write_text(json.dumps(results, indent=1))

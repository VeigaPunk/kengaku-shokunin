"""Scratch mutants of the audit: does stock --selftest kill them, and does a task-shape probe kill them?"""
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
HERE = Path(__file__).resolve().parent
source = (LANE / "plans/benchmark_spec_audit.py").read_text()
MUTANTS = {
    "M0_identity": ("def selftest(root):", "def selftest(root):"),
    "M1_bool_id_accepted": ("if type(tid) is not int:", "if not isinstance(tid, int):"),
    "M2_non_object_silent": ('            fail("task_not_object", type(task).__name__)\n', "            pass\n"),
    "M3_sites_unchecked": ('            fail("sites_invalid")\n', "            pass\n"),
    "M4_intent_unchecked": ('            fail("intent_invalid")\n', "            pass\n"),
    "M5_eval_object_unchecked": ('            fail("eval_not_object")\n', "            pass\n"),
    "M6_missing_flag_ok": ("if type(value) is not bool:", "if value is not None and type(value) is not bool:"),
    "M7_kinds_empty_ok": ("isinstance(kinds, list) and bool(kinds) and", "isinstance(kinds, list) and"),
    "M8_nonlist_shape_reverted": ('"metrics": {}, "selected_task_ids": [], "duplicate_task_ids": [], "missing_task_ids": [], "unexpected_task_ids": []}', '"metrics": {}}'),
    "M9_nonobject_record_dropped": ('            records.append({"task_id": None, "raw_task": task,', '            0 and records.append({"task_id": None, "raw_task": task,'),
    "M10_flag_bucket_conflated": ('str(value).lower() if type(value) is bool else "invalid:" + json.dumps(value, sort_keys=True)', "str(value).lower()"),
    "M11_nonobject_detail_dropped": ('fail("task_not_object", type(task).__name__)', 'fail("task_not_object")'),
}
pristine = json.loads((LANE / "plans/fixtures/r28/webarena/config_files/test.raw.json").read_text())
BASE = {"task_id": 0, "sites": ["s"], "intent": "q", "require_login": True, "require_reset": False,
        "eval": {"eval_types": ["string_match"], "reference_answers": {"exact_match": "a"}}}


def pinned_with(fn):
    tasks = json.loads(json.dumps(pristine))
    fn(tasks)
    return tasks


KILL_PROBES = {
    "M0_identity": ([BASE], 1),
    "M1_bool_id_accepted": (pinned_with(lambda t: t[1].__setitem__("task_id", True)), 812),
    "M2_non_object_silent": ([BASE, 7], 1),
    "M3_sites_unchecked": ([dict(BASE, sites=None)], 1),
    "M4_intent_unchecked": ([dict(BASE, intent=None)], 1),
    "M5_eval_object_unchecked": ([dict(BASE, eval=None)], 1),
    "M6_missing_flag_ok": ([{k: v for k, v in BASE.items() if k != "require_reset"}], 1),
    "M7_kinds_empty_ok": ([dict(BASE, eval={"eval_types": [], "reference_answers": None})], 1),
    "M8_nonlist_shape_reverted": ({}, 1),
    "M9_nonobject_record_dropped": ([7], 1),
    "M10_flag_bucket_conflated": ([dict(BASE, require_reset="false")], 1),
    "M11_nonobject_detail_dropped": ([7], 1),
}


def observe(module, tasks, size):
    try:
        r = module.audit_tasks(tasks, expected_population=size)
    except Exception as error:
        return "CRASH " + type(error).__name__
    return {"ids": sorted({f["id"] for f in r["findings"]}), "keys": sorted(r), "records": [t.get("raw_task") for t in r["tasks"]],
            "reset_flags": r["metrics"].get("reset_flags"), "details": [f.get("detail") for f in r["findings"] if f["id"] == "task_not_object"]}


sys.path.insert(0, str(LANE / "plans"))
import benchmark_spec_audit as production  # noqa: E402

mdir = HERE / "mutants"
mdir.mkdir(exist_ok=True)
for name, (old, new) in MUTANTS.items():
    assert source.count(old) == 1, name
    path = mdir / f"{name}.py"
    path.write_text(source.replace(old, new))
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    st = subprocess.run([sys.executable, "-B", str(path), "--root", str(LANE), "--selftest"], capture_output=True, text=True, env=env)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    tasks, size = KILL_PROBES[name]
    mutant_obs, production_obs = observe(module, tasks, size), observe(production, tasks, size)
    print(json.dumps({"mutant": name, "selftest_exit": st.returncode, "selftest_survived": st.returncode == 0,
                      "selftest_tail": (st.stdout + st.stderr).strip().splitlines()[-1][:60],
                      "probe_kills": mutant_obs != production_obs, "mutant_obs": mutant_obs if mutant_obs != production_obs else "same"}))

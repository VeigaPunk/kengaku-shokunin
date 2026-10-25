"""Hand-expected task-shape mutations against production audit_tasks; production bytes read-only."""
import copy
import json
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans")
from benchmark_spec_audit import audit_tasks  # noqa: E402

BASE = {"task_id": 0, "sites": ["shopping"], "intent": "answer question", "require_login": True, "require_reset": False,
        "eval": {"eval_types": ["string_match"], "reference_answers": {"exact_match": "a"}}}
ABSENT = object()


def mutate(path, value):
    task = copy.deepcopy(BASE)
    node = task
    for key in path[:-1]:
        node = node[key]
    if value is ABSENT:
        del node[path[-1]]
    else:
        node[path[-1]] = value
    return task


# (name, tasks, expected finding ids, expected record count)
CASES = [
    ("clean", [BASE], set(), 1),
    ("top_dict", {"0": BASE}, {"tasks_not_list"}, 0),
    ("top_null", None, {"tasks_not_list"}, 0),
    ("top_empty_list", [], {"missing_task_id", "population_size"}, 0),
    ("task_int", [5], {"task_not_object", "missing_task_id"}, 1),
    ("task_null", [None], {"task_not_object", "missing_task_id"}, 1),
    ("task_list", [[BASE]], {"task_not_object", "missing_task_id"}, 1),
    ("task_empty_obj", [{}], {"task_id_invalid", "sites_invalid", "intent_invalid", "flag_invalid", "eval_not_object", "eval_types_invalid", "missing_task_id"}, 1),
    ("id_true", [mutate(["task_id"], True)], {"task_id_invalid", "missing_task_id"}, 1),
    ("id_false", [mutate(["task_id"], False)], {"task_id_invalid", "missing_task_id"}, 1),
    ("id_str", [mutate(["task_id"], "0")], {"task_id_invalid", "missing_task_id"}, 1),
    ("id_float", [mutate(["task_id"], 0.0)], {"task_id_invalid", "missing_task_id"}, 1),
    ("id_null", [mutate(["task_id"], None)], {"task_id_invalid", "missing_task_id"}, 1),
    ("id_missing", [mutate(["task_id"], ABSENT)], {"task_id_invalid", "missing_task_id"}, 1),
    ("id_negative", [mutate(["task_id"], -1)], {"missing_task_id", "unexpected_task_id"}, 1),
    ("id_big", [mutate(["task_id"], 812)], {"missing_task_id", "unexpected_task_id"}, 1),
    ("sites_missing", [mutate(["sites"], ABSENT)], {"sites_invalid"}, 1),
    ("sites_null", [mutate(["sites"], None)], {"sites_invalid"}, 1),
    ("sites_empty", [mutate(["sites"], [])], {"sites_invalid"}, 1),
    ("sites_str", [mutate(["sites"], "shopping")], {"sites_invalid"}, 1),
    ("sites_blank_member", [mutate(["sites"], [""])], {"sites_invalid"}, 1),
    ("sites_bool_member", [mutate(["sites"], [True])], {"sites_invalid"}, 1),
    ("intent_missing", [mutate(["intent"], ABSENT)], {"intent_invalid"}, 1),
    ("intent_null", [mutate(["intent"], None)], {"intent_invalid"}, 1),
    ("intent_blank", [mutate(["intent"], "   ")], {"intent_invalid"}, 1),
    ("intent_int", [mutate(["intent"], 7)], {"intent_invalid"}, 1),
    ("intent_list", [mutate(["intent"], ["x"])], {"intent_invalid"}, 1),
    ("eval_missing", [mutate(["eval"], ABSENT)], {"eval_not_object", "eval_types_invalid"}, 1),
    ("eval_null", [mutate(["eval"], None)], {"eval_not_object", "eval_types_invalid"}, 1),
    ("eval_list", [mutate(["eval"], [])], {"eval_not_object", "eval_types_invalid"}, 1),
    ("kinds_missing", [mutate(["eval", "eval_types"], ABSENT)], {"eval_types_invalid"}, 1),
    ("kinds_null", [mutate(["eval", "eval_types"], None)], {"eval_types_invalid"}, 1),
    ("kinds_empty", [mutate(["eval", "eval_types"], [])], {"eval_types_invalid"}, 1),
    ("kinds_str", [mutate(["eval", "eval_types"], "string_match")], {"eval_types_invalid"}, 1),
    ("kinds_bool_member", [mutate(["eval", "eval_types"], [True])], {"eval_types_invalid"}, 1),
    ("kinds_dup", [mutate(["eval", "eval_types"], ["string_match", "string_match"])], {"duplicate_eval_type"}, 1),
    ("login_missing", [mutate(["require_login"], ABSENT)], {"flag_invalid"}, 1),
    ("login_null", [mutate(["require_login"], None)], {"flag_invalid"}, 1),
    ("login_str_true", [mutate(["require_login"], "true")], {"flag_invalid"}, 1),
    ("login_int_1", [mutate(["require_login"], 1)], {"flag_invalid"}, 1),
    ("reset_missing", [mutate(["require_reset"], ABSENT)], {"flag_invalid"}, 1),
    ("reset_int_0", [mutate(["require_reset"], 0)], {"flag_invalid"}, 1),
    ("reset_str_False", [mutate(["require_reset"], "False")], {"flag_invalid"}, 1),
]

rows = []
for name, tasks, expected, n_records in CASES:
    try:
        result = audit_tasks(tasks, expected_population=1)
    except Exception as error:  # a crash is itself the observation
        rows.append({"case": name, "crash": f"{type(error).__name__}: {error}"})
        continue
    actual = {f["id"] for f in result["findings"]}
    row = {"case": name, "ids_ok": actual == expected, "records_ok": len(result["tasks"]) == n_records,
           "keys": sorted(result), "login_flags": result["metrics"].get("login_flags"),
           "reset_flags": result["metrics"].get("reset_flags"), "eval_type_sets": result["metrics"].get("eval_type_sets"),
           "selected": result.get("selected_task_ids", "ABSENT_KEY"),
           "raw_retained": [r.get("raw_task") == t for r, t in zip(result["tasks"], tasks)] if isinstance(tasks, list) else None,
           "failed_detail": [f.get("detail") for f in result["findings"] if f["id"] in ("task_not_object", "flag_invalid")]}
    if actual != expected:
        row["actual"], row["expected"] = sorted(actual), sorted(expected)
    rows.append(row)

for row in rows:
    print(json.dumps(row, sort_keys=True))
print("crashes", sum("crash" in r for r in rows), "id_mismatch", sum(r.get("ids_ok") is False for r in rows),
      "record_mismatch", sum(r.get("records_ok") is False for r in rows), "cases", len(rows))

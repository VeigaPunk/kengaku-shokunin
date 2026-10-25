#!/usr/bin/env python3
"""Scope-aware (Amendment 2) re-probe: vacuity out of scope, `{}` native-compatible, raw fields not invented."""
import copy
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
PATH = sys.argv[1]
spec = importlib.util.spec_from_file_location("audit_under_test", PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

BASE = {"task_id": 0, "sites": ["site"], "intent": "answer question", "require_login": False, "require_reset": False,
        "eval": {"eval_types": ["string_match"], "reference_answers": {"exact_match": "answer"}, "string_note": ""}}


def task(**eval_overrides):
    t = copy.deepcopy(BASE)
    for key, value in eval_overrides.items():
        if value is ...:
            t["eval"].pop(key, None)
        else:
            t["eval"][key] = value
    return t


URL = dict(eval_types=["url_match"], reference_url="__SITE__/x")
# (name, task, expected findings, record expectations {field: value}, metric expectations {metric: value})
CASES = [
    ("A01_exact_ok", task(), [], {"reference_approach_order": ["exact_match"], "reference_answers_present": True}, {"string_operators": {"exact_match": 1}}),
    ("A02_exact_int", task(reference_answers={"exact_match": 5}), ["string_operator_invalid"], {}, {}),
    ("A03_exact_list", task(reference_answers={"exact_match": ["a"]}), ["string_operator_invalid"], {}, {}),
    ("A04_must_str", task(reference_answers={"must_include": "a"}), ["string_operator_invalid"], {}, {}),
    ("A05_must_mixed", task(reference_answers={"must_include": ["a", 3]}), ["string_operator_invalid"], {}, {}),
    ("A06_fuzzy_lower_na", task(reference_answers={"fuzzy_match": "n/a"}), ["string_operator_invalid"], {}, {}),
    ("A07_fuzzy_dict", task(reference_answers={"fuzzy_match": {"a": "b"}}), ["string_operator_invalid"], {}, {}),
    ("A08_na_no_note", task(reference_answers={"fuzzy_match": "N/A"}, string_note=...), ["string_note_invalid"], {}, {}),
    ("A09_na_none_note", task(reference_answers={"fuzzy_match": "N/A"}, string_note=None), ["string_note_invalid"], {}, {}),
    ("A10_na_note_ok", task(reference_answers={"fuzzy_match": "N/A"}, string_note="why"), [], {}, {}),
    ("A11_refs_none", task(reference_answers=None), ["reference_answers_invalid"], {"reference_answers": None, "reference_answers_present": True, "reference_approach_order": None}, {}),
    ("A12_refs_list", task(reference_answers=["a"]), ["reference_answers_invalid"], {"reference_answers": ["a"], "reference_approach_order": None}, {}),
    ("A13_refs_absent", task(reference_answers=...), ["reference_answers_invalid"], {"reference_answers": None, "reference_answers_present": False, "reference_approach_order": None}, {}),
    ("A14_refs_empty_dict_inscope_accepted", task(reference_answers={}), [], {"reference_answers": {}, "reference_answers_present": True, "reference_approach_order": []}, {}),
    ("A15_unknown_op_alone", task(reference_answers={"bogus": "x"}), ["string_operator_invalid"], {}, {"string_operators": {"bogus": 1}}),
    ("A16_unknown_op_mixed", task(reference_answers={"exact_match": "a", "bogus": "x"}), ["string_operator_invalid"], {"reference_approach_order": ["exact_match", "bogus"]}, {}),
    ("A17_fuzzy_mixed", task(reference_answers={"fuzzy_match": ["a", 3]}), ["string_operator_invalid"], {}, {}),
    ("A18_refs_scalar", task(reference_answers="answer"), ["reference_answers_invalid"], {"reference_answers": "answer"}, {}),
    # Out-of-scope vacuity: accepted by declared scope; observation only.
    ("V01_must_empty_list", task(reference_answers={"must_include": []}), [], {}, {}),
    ("V02_fuzzy_empty_list", task(reference_answers={"fuzzy_match": []}), [], {}, {}),
    ("V03_must_empty_string", task(reference_answers={"must_include": [""]}), [], {}, {}),
    ("V04_must_blank_string", task(reference_answers={"must_include": ["   "]}), [], {}, {}),
    ("V05_must_quote_pair", task(reference_answers={"must_include": ["\"\""]}), [], {}, {}),
    # Eval types.
    ("E01_duplicate", task(eval_types=["string_match", "string_match"]), ["duplicate_eval_type"], {"eval_types": ["string_match", "string_match"]}, {"eval_type_sets": {"string_match,string_match": 1}}),
    ("E02_unknown_plus_string", task(eval_types=["string_match", "bogus"]), ["unknown_eval_type"], {}, {}),
    ("E03_case_variant", task(eval_types=["String_Match"]), ["unknown_eval_type"], {}, {}),
    ("E04_eval_types_str", task(eval_types="string_match"), ["eval_types_invalid"], {"eval_types": "string_match"}, {"eval_type_sets": {"<INVALID>": 1}, "eval_type_orders": {"<INVALID>": 1}, "site_eval_strata": 0}),
    ("E05_eval_types_empty", task(eval_types=[]), ["eval_types_invalid"], {"eval_types": []}, {"eval_type_sets": {"<INVALID>": 1}, "site_eval_strata": 0}),
    ("E06_nonstr_member_unmasked", task(eval_types=["string_match", 5], reference_answers={"exact_match": 3}), ["eval_types_invalid", "string_operator_invalid"], {"eval_types": ["string_match", 5], "schema_status": "FAILED"}, {"eval_type_sets": {"<INVALID>": 1}, "site_eval_strata": 0, "selected_count": 0}),
    ("E07_eval_types_absent", task(eval_types=...), ["eval_types_invalid"], {"eval_types": None}, {"eval_type_sets": {"<INVALID>": 1}}),
    ("E08_unknown_only_malformed_refs", task(eval_types=["bogus"], reference_answers={"exact_match": 3}), ["unknown_eval_type"], {}, {}),
    ("E09_dup_and_unknown", task(eval_types=["bogus", "bogus"]), ["duplicate_eval_type", "unknown_eval_type"], {}, {}),
    ("E10_mixed_dup_nonstr", task(eval_types=["string_match", "string_match", None], reference_answers={"must_include": 3}), ["eval_types_invalid", "duplicate_eval_type", "string_operator_invalid"], {}, {"site_eval_strata": 0}),
    ("E11_mixed_unknown_nonstr", task(eval_types=[{"x": 1}, "bogus"]), ["eval_types_invalid", "unknown_eval_type"], {"eval_types": [{"x": 1}, "bogus"]}, {}),
    ("E12_mixed_nonstr_good_refs", task(eval_types=["string_match", 1.5]), ["eval_types_invalid"], {}, {"string_operators": {"exact_match": 1}}),
    ("E13_mixed_nonstr_absent_refs", task(eval_types=[True, "string_match"], reference_answers=...), ["eval_types_invalid", "reference_answers_invalid"], {"reference_answers_present": False}, {}),
    # Nonactive preservation.
    ("N01_nonactive_none", task(**URL, reference_answers=None), [], {"reference_answers": None, "reference_answers_present": True, "reference_approach_order": None}, {"string_operators": {}}),
    ("N02_nonactive_malformed", task(**URL, reference_answers={"exact_match": 3}), [], {"reference_answers": {"exact_match": 3}, "reference_approach_order": ["exact_match"]}, {"string_operators": {}}),
    ("N03_nonactive_absent", task(**URL, reference_answers=...), [], {"reference_answers": None, "reference_answers_present": False, "reference_approach_order": None}, {}),
    ("N04_na_combined_after_exact", task(reference_answers={"exact_match": "a", "fuzzy_match": "N/A"}, string_note="why"), [], {"reference_approach_order": ["exact_match", "fuzzy_match"]}, {}),
    ("N05_eval_not_object", dict(BASE, eval=None), ["eval_not_object", "eval_types_invalid"], {"reference_answers": None, "reference_answers_present": False, "eval_types": None}, {}),
]

out = {"path": PATH, "cases": {}}
mismatch = []
for name, t, expected, rec_exp, met_exp in CASES:
    r = module.audit_tasks([t], expected_population=1)
    actual = sorted({f["id"] for f in r["findings"]})
    record = r["tasks"][0]
    problems = []
    if set(actual) != set(expected):
        problems.append(f"findings {actual} != {sorted(expected)}")
    for key, value in rec_exp.items():
        if record.get(key, "<missing>") != value:
            problems.append(f"record.{key}={record.get(key, '<missing>')!r} != {value!r}")
    for key, value in met_exp.items():
        if r["metrics"].get(key) != value:
            problems.append(f"metrics.{key}={r['metrics'].get(key)!r} != {value!r}")
    if record.get("raw_task") != t:
        problems.append("raw_task not preserved")
    out["cases"][name] = {"actual": actual, "problems": problems}
    if problems:
        mismatch.append(name)
out["mismatch"] = mismatch
print(json.dumps(out, indent=1, sort_keys=True, default=repr))
print("CASES", len(CASES), "MISMATCH", len(mismatch), ",".join(mismatch), file=sys.stderr)

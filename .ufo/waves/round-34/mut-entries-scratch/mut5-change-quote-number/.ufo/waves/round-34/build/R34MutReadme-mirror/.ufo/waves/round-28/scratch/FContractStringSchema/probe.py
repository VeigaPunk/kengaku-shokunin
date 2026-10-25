#!/usr/bin/env python3
"""Hand-expected miniature string-schema probes against audit_tasks loaded from an explicit path.

Expected sets are derived by hand from the pinned scorer (evaluators.py:80-170, 355-374) plus the
audit's own declared rules; nothing upstream is imported or executed.
"""
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


def run(t):
    r = module.audit_tasks([t], expected_population=1)
    return r, sorted({f["id"] for f in r["findings"]})


# (name, task, hand-expected finding set, why)
CASES = [
    ("A01_exact_ok", task(), [], "scorer exact_match(ref: str)"),
    ("A02_exact_int", task(reference_answers={"exact_match": 5}), ["string_operator_invalid"], "beartype rejects int ref"),
    ("A03_exact_list", task(reference_answers={"exact_match": ["a"]}), ["string_operator_invalid"], "beartype rejects list ref"),
    ("A04_must_str", task(reference_answers={"must_include": "a"}), ["string_operator_invalid"], "assert isinstance(value, list) at :143"),
    ("A05_must_mixed", task(reference_answers={"must_include": ["a", 3]}), ["string_operator_invalid"], "beartype rejects int element"),
    ("A06_fuzzy_lower_na", task(reference_answers={"fuzzy_match": "n/a"}), ["string_operator_invalid"], "non-N/A str hits assert list at :165"),
    ("A07_fuzzy_dict", task(reference_answers={"fuzzy_match": {"a": "b"}}), ["string_operator_invalid"], "assert list"),
    ("A08_na_no_note", task(reference_answers={"fuzzy_match": "N/A"}, string_note=...), ["string_note_invalid"], "KeyError at :161 when score!=1"),
    ("A09_na_none_note", task(reference_answers={"fuzzy_match": "N/A"}, string_note=None), ["string_note_invalid"], "beartype ua_match(ref: str)"),
    ("A10_na_note_ok", task(reference_answers={"fuzzy_match": "N/A"}, string_note="unachievable"), [], "compatible"),
    ("A11_refs_none", task(reference_answers=None), ["reference_answers_invalid"], "None.items() AttributeError"),
    ("A12_refs_list", task(reference_answers=["a"]), ["reference_answers_invalid"], "list.items() AttributeError"),
    ("A13_refs_absent", task(reference_answers=...), ["reference_answers_invalid"], "KeyError at :137"),
    ("A14_refs_empty_dict", task(reference_answers={}), ["reference_answers_invalid"], "audit's own vacuity rule (scorer returns 1.0)"),
    ("A15_unknown_op_alone", task(reference_answers={"bogus": "x"}), ["string_operator_invalid"], "no case _: silent no-op, vacuous 1.0"),
    ("A17_fuzzy_mixed", task(reference_answers={"fuzzy_match": ["a", 3]}), ["string_operator_invalid"], "beartype fuzzy_match(ref: str)"),
    ("A16_unknown_op_mixed", task(reference_answers={"exact_match": "a", "bogus": "x"}), ["string_operator_invalid"], "silent no-op op"),
    # Vacuous-but-crash-free shapes: same scorer outcome (score stays 1.0 regardless of prediction) as A14/A15.
    ("V01_must_empty_list", task(reference_answers={"must_include": []}), ["VACUOUS"], "loop over [] -> 1.0, like A14"),
    ("V02_fuzzy_empty_list", task(reference_answers={"fuzzy_match": []}), ["VACUOUS"], "loop over [] -> 1.0, like A14"),
    ("V03_must_empty_string", task(reference_answers={"must_include": [""]}), ["VACUOUS"], "'' in pred always true"),
    ("V04_must_blank_string", task(reference_answers={"must_include": ["   "]}), ["VACUOUS"], "clean_answer strips ref to ''"),
    ("V05_must_quote_pair", task(reference_answers={"must_include": ["\"\""]}), ["VACUOUS"], "clean_answer strips quote pair to ''"),
    # Eval-type shapes.
    ("E01_duplicate", task(eval_types=["string_match", "string_match"]), ["duplicate_eval_type"], "two StringEvaluators, product"),
    ("E02_unknown_plus_string", task(eval_types=["string_match", "bogus"]), ["unknown_eval_type"], "router ValueError at :372"),
    ("E03_case_variant", task(eval_types=["String_Match"]), ["unknown_eval_type"], "match is exact"),
    ("E04_eval_types_str", task(eval_types="string_match"), ["eval_types_invalid"], "iterates chars -> ValueError"),
    ("E05_eval_types_empty", task(eval_types=[]), ["eval_types_invalid"], "audit rule; scorer returns empty comb 1.0"),
    ("E06_eval_types_nonstr_masks", task(eval_types=["string_match", 5], reference_answers={"exact_match": 3}), ["eval_types_invalid", "string_operator_invalid"], "both defects present in task"),
    ("E07_eval_types_absent", task(eval_types=...), ["eval_types_invalid"], "KeyError at :361"),
    ("E08_unknown_only_malformed_refs", task(eval_types=["bogus"], reference_answers={"exact_match": 3}), ["unknown_eval_type"], "string not active; refs unread"),
    ("E09_dup_and_unknown", task(eval_types=["bogus", "bogus"]), ["duplicate_eval_type", "unknown_eval_type"], "both"),
    # Nonactive preservation.
    ("N01_nonactive_none", task(eval_types=["url_match"], reference_url="__SITE__/x", reference_answers=None), [], "refs unread"),
    ("N02_nonactive_malformed", task(eval_types=["url_match"], reference_url="__SITE__/x", reference_answers={"exact_match": 3}), [], "refs unread"),
    ("N03_nonactive_absent", task(eval_types=["url_match"], reference_url="__SITE__/x", reference_answers=...), [], "refs unread"),
    ("N04_na_combined_after_exact", task(reference_answers={"exact_match": "a", "fuzzy_match": "N/A"}, string_note="why"), [], "crash-free; overwrite semantics are contract, not schema"),
]

out = {"path": PATH, "cases": {}}
mismatch = []
for name, t, expected, why in CASES:
    r, actual = run(t)
    record = r["tasks"][0] if r["tasks"] else {}
    row = {"expected": expected, "actual": actual, "why": why,
           "record_reference_answers": record.get("reference_answers", "<missing>"),
           "record_approach_order": record.get("reference_approach_order", "<missing>"),
           "record_eval_types": record.get("eval_types", "<missing>"),
           "schema_status": record.get("schema_status"),
           "eval_type_sets": r["metrics"].get("eval_type_sets"),
           "string_operators": r["metrics"].get("string_operators"),
           "strata": r["metrics"].get("site_eval_strata"), "selected": r["selected_task_ids"]}
    out["cases"][name] = row
    exp = set(expected) - {"VACUOUS"}
    if expected == ["VACUOUS"]:
        if actual:  # any finding at all is acceptable for vacuous shapes
            continue
        mismatch.append(name)
    elif set(actual) != exp:
        mismatch.append(name)
out["mismatch"] = mismatch
print(json.dumps(out, indent=1, sort_keys=True, default=repr))
print("MISMATCH", len(mismatch), ",".join(mismatch), file=sys.stderr)

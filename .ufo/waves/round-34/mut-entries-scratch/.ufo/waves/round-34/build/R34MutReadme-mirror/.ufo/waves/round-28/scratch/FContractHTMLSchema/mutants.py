"""Miniature HTML-schema mutants against production audit_tasks (read-only import, bytecode disabled).
Expected column is hand-derived from pinned evaluators.py HTMLContentEvaluator:244-333 and StringEvaluator:79-111."""
import copy
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("audit", sys.argv[1])
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

base = {"task_id": 0, "sites": ["site"], "intent": "i", "require_login": False, "require_reset": False,
        "eval": {"eval_types": ["program_html"], "program_html": [{"url": "last", "locator": "", "required_contents": {"must_include": ["x"]}}]}}


def run(name, mutate, upstream):
    t = copy.deepcopy(base)
    mutate(t)
    r = audit.audit_tasks([t], expected_population=1)
    ids = sorted({f["id"] for f in r["findings"]})
    m = r["metrics"]
    print(json.dumps({"case": name, "audit_findings": ids, "html_operators": m.get("html_operators"), "targets": m.get("program_html_targets"), "upstream_hand_derived": upstream}))


def tg(t):
    return t["eval"]["program_html"][0]


def setrc(v):
    return lambda t: tg(t).__setitem__("required_contents", v)


run("baseline", lambda t: None, "scores per selection")
run("both_ops_exact_wins", setrc({"exact_match": "a", "must_include": ["b"]}), "if/elif: exact_match only; must_include silently ignored")
run("both_ops_exact_invalid_include_valid", setrc({"exact_match": 5, "must_include": ["b"]}), "exact branch taken -> beartype violation on ref:int (crash)")
run("both_ops_exact_valid_include_invalid", setrc({"exact_match": "a", "must_include": 5}), "exact branch taken; invalid must_include never read (no crash)")
run("exact_list", setrc({"exact_match": ["a"]}), "beartype violation ref:list (crash)")
run("exact_none", setrc({"exact_match": None}), "beartype violation (crash)")
run("exact_blank", setrc({"exact_match": ""}), "passes iff cleaned selection empty")
run("include_string", setrc({"must_include": "abc"}), "assert isinstance list fails (crash)")
run("include_tuple_like_dict", setrc({"must_include": {"a": 1}}), "assert list fails (crash)")
run("include_int_item", setrc({"must_include": [1]}), "AttributeError int.split (crash)")
run("include_empty_list", setrc({"must_include": []}), "loop never runs -> target vacuously 1.0")
run("include_empty_string_item", setrc({"must_include": [""]}), "'' in pred -> vacuous 1.0")
run("include_blank_or_alternative", setrc({"must_include": ["x |OR| "]}), "split -> ['x',''] ; '' in pred -> vacuous 1.0")
run("include_whitespace_alternative", setrc({"must_include": ["x |OR|  "]}), "alt ' ' cleaned to '' -> vacuous 1.0")
run("fuzzy_only", setrc({"fuzzy_match": ["a"]}), "ValueError Unknown required_contents (crash)")
run("include_plus_fuzzy_extra", setrc({"must_include": ["a"], "fuzzy_match": ["b"]}), "must_include only; fuzzy silently ignored")
run("rc_empty_dict", setrc({}), "ValueError (crash)")
run("rc_list", setrc(["must_include"]), "'must_include' in list True -> list['must_include'] TypeError (crash)")
run("rc_missing", lambda t: tg(t).pop("required_contents"), "KeyError (crash)")
run("url_missing", lambda t: tg(t).pop("url"), "KeyError (crash)")
run("locator_missing", lambda t: tg(t).pop("locator"), "KeyError (crash)")
run("target_extra_key_typo", lambda t: tg(t).__setitem__("prep_action", ["x"]), "ignored silently")
run("program_html_missing", lambda t: t["eval"].pop("program_html"), "KeyError (crash)")
run("program_html_empty", lambda t: t["eval"].__setitem__("program_html", []), "loop never runs -> vacuous 1.0")
run("program_html_not_routed", lambda t: (t["eval"].__setitem__("eval_types", ["url_match"]), t["eval"].__setitem__("reference_url", "u")), "HTML evaluator not constructed; targets ignored")
run("program_html_dict", lambda t: t["eval"].__setitem__("program_html", {"url": "last"}), "iterates keys -> str['url'] TypeError (crash)")


def js(t, pa):
    tg(t)["locator"] = "document.title"
    tg(t)["prep_actions"] = pa


run("prep_js_list_str", lambda t: js(t, ["x()"]), "evaluated; exceptions swallowed")
run("prep_js_string", lambda t: js(t, "abc"), "iterates characters; exceptions swallowed; no crash")
run("prep_js_int", lambda t: js(t, 5), "TypeError iterating int inside try -> swallowed; no crash")
run("prep_js_list_int", lambda t: js(t, [5]), "f-string '() => 5' evaluates; no crash")
run("prep_js_empty_list", lambda t: js(t, []), "no-op")
run("prep_full_page_list", lambda t: tg(t).__setitem__("prep_actions", ["x()"]), "never executed (only JS-locator branch reads prep_actions)")
run("prep_helper_int", lambda t: (tg(t).__setitem__("locator", "func:f(__page__)"), tg(t).__setitem__("prep_actions", 5)), "never read; no crash")
run("prep_null_js", lambda t: js(t, None), "TypeError inside try swallowed; no crash")

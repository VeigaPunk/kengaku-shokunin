#!/usr/bin/env python3
"""Static inventory of original WebArena task specs, never a task-validity verdict."""
import argparse
import ast
import collections
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

FIXTURE = Path("plans/fixtures/r28/webarena")
MANIFEST_SHA256 = "c78b1478c5cb18dd7621723023e7ff15342401c72fc04a939a8d4d290323a6dd"
SELECTION_SHA256 = "5f7eea2e6868553dbda4d7a4be491b3cbaaeb532f1c44dfb9fb40006ff3ed17a"
TYPES = {"string_match", "url_match", "program_html"}
LIMITS = [
    "WebArena repository snapshot dce04686a56253aefba7b18a4fa0937cf1dc987b (2025-11-26), not its 2023-07-25 release or WebArena-Verified.",
    "Static schema and predicate inventory is not semantic task validity, actual task success or contamination evidence.",
    "No upstream code imports/execution, model calls, browser actions, benchmark site traffic or auth material opened.",
    "Selected16 are minimum IDs of first16 lexicographic site/evaluator strata, not a representative/random sample.",
    "Live DOM/API state, fixture resets, navigation and external LLM judge outcomes are unverified.",
]


def classify_locator(value):
    if not value.strip():
        return "full_page"
    if value.startswith("document.") or value.startswith("[...document."):
        return "javascript"
    if value.startswith("func:"):
        return "helper"
    return "unsupported"


def audit_tasks(tasks, expected_population=812):
    findings, records = [], []
    counts = {key: collections.Counter() for key in ("eval_type_sets", "eval_type_orders", "site_sets", "login_flags", "reset_flags", "string_operators", "url_rules", "html_operators", "locator_classes", "target_url_classes")}
    ids, strata = [], collections.defaultdict(list)
    target_count = 0
    if not isinstance(tasks, list):
        return {"findings": [{"id": "tasks_not_list"}], "tasks": [], "metrics": {}}
    for position, task in enumerate(tasks):
        local = []
        def fail(finding, detail=""):
            local.append({"id": finding, "task_position": position, "task_id": task.get("task_id") if isinstance(task, dict) else None, "detail": detail})
        if not isinstance(task, dict):
            fail("task_not_object")
            findings.extend(local)
            continue
        tid = task.get("task_id")
        if type(tid) is not int:
            fail("task_id_invalid")
        else:
            ids.append(tid)
        sites = task.get("sites")
        sites_ok = isinstance(sites, list) and bool(sites) and all(isinstance(x, str) and x for x in sites)
        if not sites_ok:
            fail("sites_invalid")
        if not isinstance(task.get("intent"), str) or not task.get("intent", "").strip():
            fail("intent_invalid")
        for flag, key in (("require_login", "login_flags"), ("require_reset", "reset_flags")):
            value = task.get(flag)
            if type(value) is not bool:
                fail("flag_invalid", flag)
            counts[key][str(value).lower()] += 1
        evaluation = task.get("eval")
        if not isinstance(evaluation, dict):
            fail("eval_not_object")
            evaluation = {}
        kinds = evaluation.get("eval_types")
        kinds_ok = isinstance(kinds, list) and bool(kinds) and all(isinstance(x, str) for x in kinds)
        if not kinds_ok:
            fail("eval_types_invalid")
            kinds = []
        if len(kinds) != len(set(kinds)):
            fail("duplicate_eval_type")
        for kind in kinds:
            if kind not in TYPES:
                fail("unknown_eval_type", kind)
        if sites_ok and kinds_ok and type(tid) is int:
            strata[(tuple(sorted(sites)), tuple(sorted(kinds)))].append(tid)
        counts["eval_type_sets"][",".join(sorted(kinds))] += 1
        counts["eval_type_orders"][",".join(kinds)] += 1
        if sites_ok:
            counts["site_sets"][",".join(sorted(sites))] += 1
        refs = evaluation.get("reference_answers", {})
        if "string_match" in kinds:
            if not isinstance(refs, dict) or not refs:
                fail("reference_answers_invalid")
            else:
                for operator, value in refs.items():
                    counts["string_operators"][operator] += 1
                    valid = (operator == "exact_match") or (operator == "must_include" and isinstance(value, list) and all(isinstance(v, str) for v in value)) or (operator == "fuzzy_match" and (value == "N/A" or isinstance(value, list) and all(isinstance(v, str) for v in value)))
                    if not valid:
                        fail("string_operator_invalid", operator)
                    if operator == "fuzzy_match" and value == "N/A" and not isinstance(evaluation.get("string_note"), str):
                        fail("string_note_invalid")
        if "url_match" in kinds:
            rule = evaluation.get("url_note", "GOLD in PRED")
            if not isinstance(evaluation.get("reference_url"), str) or not evaluation.get("reference_url"):
                fail("reference_url_invalid")
            elif any(not alternative for alternative in evaluation["reference_url"].split(" |OR| ")):
                fail("reference_url_empty_alternative")
            if rule != "GOLD in PRED":
                fail("url_rule_unsupported", str(rule))
            counts["url_rules"][str(rule)] += 1
        targets = evaluation.get("program_html", [])
        if "program_html" in kinds:
            if not isinstance(targets, list) or not targets:
                fail("program_html_invalid")
                targets = []
            target_count += len(targets)
            for index, target in enumerate(targets):
                if not isinstance(target, dict):
                    fail("target_not_object", str(index))
                    continue
                url, locator, required = target.get("url"), target.get("locator"), target.get("required_contents")
                if not isinstance(url, str) or not url:
                    fail("target_url_invalid", str(index))
                else:
                    counts["target_url_classes"]["last" if url == "last" else "helper" if url.startswith("func") else "navigation"] += 1
                    if url.startswith("func") and not url.startswith("func:"):
                        fail("target_url_func_malformed", str(index))
                if not isinstance(locator, str):
                    fail("locator_invalid", str(index))
                else:
                    category = classify_locator(locator)
                    counts["locator_classes"][category] += 1
                    if category == "unsupported":
                        fail("locator_unsupported", str(index))
                if not isinstance(required, dict):
                    fail("required_contents_invalid", str(index))
                    continue
                # The source uses if/elif: exact_match takes precedence if both occur.
                operator = "exact_match" if "exact_match" in required else "must_include" if "must_include" in required else None
                if operator is None:
                    fail("html_operator_unsupported", str(index))
                else:
                    counts["html_operators"][operator] += 1
                    value = required[operator]
                    if not (isinstance(value, str) if operator == "exact_match" else isinstance(value, list) and all(isinstance(v, str) for v in value)):
                        fail("html_operator_value_invalid", str(index))
                if "prep_actions" in target and not (isinstance(target["prep_actions"], list) and all(isinstance(v, str) for v in target["prep_actions"])):
                    fail("prep_actions_invalid", str(index))
        findings.extend(local)
        records.append({"task_id": tid, "raw_task": task, "sites": sites, "intent": task.get("intent"), "eval_types": kinds, "require_login": task.get("require_login"), "require_reset": task.get("require_reset"), "reference_answers": refs, "reference_url": evaluation.get("reference_url"), "url_note": evaluation.get("url_note", "GOLD in PRED"), "program_html": targets, "schema_status": "FAILED" if local else "SCHEMA_COMPATIBLE", "unchecked": ["intent completeness", "runtime state", "contamination", "model ability"]})
        records[-1]["reference_approach_order"] = list(refs) if isinstance(refs, dict) else None
    duplicate_ids = sorted(tid for tid, count in collections.Counter(ids).items() if count > 1)
    missing_ids = sorted(set(range(expected_population)) - set(ids))
    unexpected_ids = sorted(set(ids) - set(range(expected_population)))
    for key, values in (("duplicate_task_id", duplicate_ids), ("missing_task_id", missing_ids), ("unexpected_task_id", unexpected_ids)):
        if values:
            findings.append({"id": key, "task_ids": values})
    if len(tasks) != expected_population:
        findings.append({"id": "population_size", "actual": len(tasks), "expected": expected_population})
    selection = [min(values) for key, values in sorted(strata.items())][:16]
    metrics = {"task_count": len(tasks), "distinct_task_ids": len(set(ids)), "site_eval_strata": len(strata), "selected_count": len(selection), "program_html_targets": target_count, **{key: dict(sorted(counter.items())) for key, counter in counts.items()}}
    return {"metrics": metrics, "selected_task_ids": selection, "duplicate_task_ids": duplicate_ids, "missing_task_ids": missing_ids, "unexpected_task_ids": unexpected_ids, "findings": findings, "tasks": records}


def scorer_contract(source):
    """Static facts tied to pinned code, never a substitute for executing the scorer."""
    tree = ast.parse(source)
    router = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "evaluator_router")
    dispatch = {}
    for node in ast.walk(router):
        if isinstance(node, ast.Match):
            for case in node.cases:
                if isinstance(case.pattern, ast.MatchValue) and isinstance(case.pattern.value, ast.Constant):
                    constructors = [call.func.id for statement in case.body for call in ast.walk(statement) if isinstance(call, ast.Call) and isinstance(call.func, ast.Name)]
                    dispatch[case.pattern.value.value] = constructors
    comb = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "EvaluatorComb")
    product_lines = [node.lineno for node in ast.walk(comb) if isinstance(node, ast.AugAssign) and isinstance(node.op, ast.Mult) and isinstance(node.target, ast.Name) and node.target.id == "score"]
    override_lines = [node.lineno for node in ast.walk(tree) if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "score" for target in node.targets) and any(isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute) and call.func.attr == "ua_match" for call in ast.walk(node.value))]
    if dispatch != {"string_match": ["StringEvaluator"], "url_match": ["URLEvaluator"], "program_html": ["HTMLContentEvaluator"]} or not product_lines or not override_lines:
        raise ValueError("scorer_contract_unrecognized")
    return {"authority": "static source facts, no runtime evaluation", "dispatch": dispatch, "composition": {"operation": "ordered product; mutable page state means order matters", "source_lines": product_lines}, "na_fallback": {"operation": "assignment overwrites accumulated string-approach score", "source_lines": override_lines}, "failure_phases": {"unknown_eval_type": "router construction raises ValueError", "unknown_url_rule": "evaluator call raises ValueError", "unknown_html_operator_or_locator": "evaluator call raises ValueError", "javascript_locator_exception": "selected text becomes empty; not necessarily score zero", "dynamic_helper_or_navigation_error": "not absorbed by the JavaScript locator exception handler"}}


def read_snapshot(root):
    fixture = root / FIXTURE
    raw = (fixture / "manifest.json").read_bytes()
    if hashlib.sha256(raw).hexdigest() != MANIFEST_SHA256:
        return {"findings": [{"id": "manifest_tampered"}], "limitations": LIMITS}, 2
    manifest = json.loads(raw)
    for relative, expected in manifest["files"].items():
        actual = hashlib.sha256((fixture / relative).read_bytes()).hexdigest()
        if actual != expected["sha256"]:
            return {"findings": [{"id": "snapshot_tampered", "path": relative}], "limitations": LIMITS}, 2
    selected_bytes = (fixture / "selected-task-ids.json").read_bytes()
    if hashlib.sha256(selected_bytes).hexdigest() != SELECTION_SHA256:
        return {"findings": [{"id": "selection_tampered"}], "limitations": LIMITS}, 2
    result = audit_tasks(json.loads((fixture / "config_files/test.raw.json").read_text()))
    if result["selected_task_ids"] != json.loads(selected_bytes):
        result["findings"].append({"id": "selection_mismatch"})
    anchors = []
    for relative in ("evaluation_harness/evaluators.py", "evaluation_harness/helper_functions.py"):
        tree = ast.parse((fixture / relative).read_text())
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                anchors.append({"file": relative, "name": node.name, "line": node.lineno, "end_line": node.end_lineno})
    result.update(upstream_revision=manifest["upstream_revision"], source_sha256={name: value["sha256"] for name, value in manifest["files"].items()}, contract_anchors=anchors, limitations=LIMITS)
    result["scorer_contract"] = scorer_contract((fixture / "evaluation_harness/evaluators.py").read_text())
    return result, int(bool(result["findings"]))


def selftest(root):
    cases = []
    source = (root / FIXTURE / "evaluation_harness/evaluators.py").read_text()
    expected_contract = json.loads((root / "plans/fixtures/r28/contract-expected.json").read_text())
    contract = scorer_contract(source)
    assert contract["dispatch"] == expected_contract["dispatch"]
    assert contract["composition"]["source_lines"] == expected_contract["product_lines"]
    assert contract["na_fallback"]["source_lines"] == expected_contract["na_override_lines"]
    cases.append("hand_expected_scorer_contract")
    try:
        scorer_contract(source.replace("score *= cur_score", "score += cur_score"))
    except ValueError as error:
        assert str(error) == "scorer_contract_unrecognized"
        cases.append("scorer_product_mutation")
    else:
        raise AssertionError("scorer_product_mutation survived")
    miniature = [{"task_id": 0, "sites": ["site"], "intent": "answer question", "require_login": False, "require_reset": False, "eval": {"eval_types": ["string_match"], "reference_answers": {"exact_match": "answer"}}}]
    def probe(name, tasks, expected, size=1):
        result = audit_tasks(tasks, expected_population=size)
        actual = {f["id"] for f in result["findings"]}
        assert actual == set(expected), (name, actual, expected)
        cases.append(name)
        return result
    import copy
    good = probe("hand_exact", miniature, [])
    assert good["metrics"]["string_operators"] == {"exact_match": 1} and good["selected_task_ids"] == [0]
    changed = copy.deepcopy(miniature); changed[0]["eval"]["eval_types"] = ["unknown"]
    probe("unknown_evaluator", changed, ["unknown_eval_type"])
    changed = copy.deepcopy(miniature); changed[0]["eval"]["reference_answers"] = {"unknown": "answer"}
    probe("unknown_string_operator", changed, ["string_operator_invalid"])
    changed = copy.deepcopy(miniature); changed[0]["eval"]["reference_answers"] = {"fuzzy_match": "N/A"}
    probe("na_requires_reason", changed, ["string_note_invalid"])
    changed[0]["eval"]["string_note"] = "not achievable"
    probe("na_reason_present", changed, [])
    probe("duplicate_and_missing_ids", miniature * 2, ["duplicate_task_id", "missing_task_id"], 2)
    changed = copy.deepcopy(miniature); changed[0]["eval"] = {"eval_types": ["url_match"], "reference_url": "__SITE__/x"}
    probe("hand_url", changed, [])
    changed[0]["eval"]["url_note"] = "EXACT"
    probe("unknown_url_rule", changed, ["url_rule_unsupported"])
    changed[0]["eval"]["url_note"] = "GOLD in PRED"
    changed[0]["eval"]["reference_url"] = "__SITE__/x |OR| "
    probe("empty_url_alternative", changed, ["reference_url_empty_alternative"])
    changed[0]["eval"] = {"eval_types": ["program_html"], "program_html": [{"url": "last", "locator": "", "required_contents": {"must_include": ["x |OR| y"]}}]}
    result = probe("hand_html", changed, [])
    assert result["metrics"]["program_html_targets"] == 1 and result["metrics"]["locator_classes"] == {"full_page": 1}
    changed[0]["eval"]["program_html"][0]["locator"] = "document.title"
    probe("hand_javascript_locator", changed, [])
    changed[0]["eval"]["program_html"][0]["locator"] = "func:helper(__page__)"
    probe("hand_helper_locator", changed, [])
    changed[0]["eval"]["program_html"][0]["url"] = "func_without_colon"
    probe("malformed_helper_url", changed, ["target_url_func_malformed"])
    changed[0]["eval"]["program_html"][0]["url"] = "last"
    changed[0]["eval"]["program_html"][0]["locator"] = "not-a-supported-locator"
    probe("unknown_locator", changed, ["locator_unsupported"])
    changed[0]["eval"]["program_html"][0]["locator"] = None
    invalid = probe("invalid_locator_keeps_target_count", changed, ["locator_invalid"])
    assert invalid["metrics"]["program_html_targets"] == 1
    changed = copy.deepcopy(miniature); changed[0]["require_reset"] = "false"
    probe("typed_flag", changed, ["flag_invalid"])
    with tempfile.TemporaryDirectory(prefix="kengaku-r28-audit-") as temp:
        scratch = Path(temp)
        shutil.copytree(root / FIXTURE, scratch / FIXTURE)
        command = [sys.executable, str(Path(__file__).resolve()), "--root", str(scratch), "--json"]
        def cli(name, expected):
            output = subprocess.run(command, capture_output=True, text=True)
            assert output.returncode == 2 and json.loads(output.stdout)["findings"][0]["id"] == expected, (name, output.returncode, output.stdout, output.stderr)
            cases.append(name)
        target = scratch / FIXTURE / "config_files/test.raw.json"
        target.write_bytes(target.read_bytes() + b" ")
        cli("cli_snapshot_pin", "snapshot_tampered")
        target.unlink()
        cli("cli_missing_input", "input_missing")
        manifest = scratch / FIXTURE / "manifest.json"
        manifest.write_bytes(manifest.read_bytes() + b" ")
        cli("cli_manifest_pin", "manifest_tampered")
    print("SELFTEST clean cases=" + str(len(cases)) + " " + ",".join(cases))
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest(args.root)
    try:
        result, code = read_snapshot(args.root)
    except (OSError, ValueError, KeyError, TypeError, SyntaxError) as error:
        result, code = {"findings": [{"id": "input_missing" if isinstance(error, FileNotFoundError) else "input_invalid", "detail": str(error)}], "limitations": LIMITS}, 2
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for limit in LIMITS:
            print("LIMIT " + limit)
        for finding in result["findings"]:
            print("FINDING " + json.dumps(finding, sort_keys=True))
        metrics = result.get("metrics", {})
        for key in ("eval_type_sets", "site_sets", "string_operators", "html_operators", "locator_classes"):
            print(key.upper() + " " + json.dumps(metrics.get(key, {}), sort_keys=True))
        print("TOTAL " + " ".join(f"{key}={metrics.get(key, 'unavailable')}" for key in ("task_count", "distinct_task_ids", "site_eval_strata", "selected_count", "program_html_targets")) + f" findings={len(result['findings'])} exit={code}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())

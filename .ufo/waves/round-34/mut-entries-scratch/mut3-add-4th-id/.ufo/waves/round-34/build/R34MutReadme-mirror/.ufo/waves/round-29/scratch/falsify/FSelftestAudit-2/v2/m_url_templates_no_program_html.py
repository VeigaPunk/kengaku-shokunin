#!/usr/bin/env python3
"""Offline source-faithful projection of pinned WebArena generate_test_data.py.

Projects the pinned raw task file under three frozen synthetic `*.invalid` profiles by the pinned
generator's six ordered global serialized-text replacements, then parses the projected text and
maps enumerate output ordinals to task IDs. The generator is parsed as inert AST data and never
imported or executed; host environment values, auth state, benchmark sites and the network are
never read; no config_files/test.json or per-task file is ever written. Audit output is stdout only;
--selftest writes only inside a private directory under /tmp and runs its CLI child isolated (-I -S,
empty environment). Assertions are load-bearing: under python -O every mode exits 2.
"""
import argparse
import ast
import bisect
import collections
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

MANIFEST = "plans/fixtures/r29/manifest.json"
MANIFEST_SHA256 = "f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87"
GENERATOR = "plans/fixtures/r29/generate_test_data.py"
RAW = "plans/fixtures/r28/webarena/config_files/test.raw.json"
PROFILES = "plans/fixtures/r29/profiles.json"
HAND = "plans/fixtures/r29/hand"
# Seat-authored hand fixtures are authenticated before the selftest consumes them.
HAND_SHA256 = {
    "cascade-order.case.json": "4f957db3c3a8c19e951b6b225e9520cfc631fc09f864c9b4aad72464d9639fb3",
    "index-shuffled-ids.fixture.json": "938771045ddbe6bdf6323858bc2c3204e38d028f1086bf83758b79a255fc9254",
    "url-only.expected.json": "e68e7a0dd8719b85a8db143748989a36dbc955a23b67209b8d76add720f1f5e5",
    "url-only.fixture.json": "2c78b19909c0c9b4b601f500301d1036c7e00d31454594ec4435c7d28407055e",
}
ORDER = ("GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP")
POPULATION = 812
# Persisted stimulus classes, keyed by frozen profile name. They label the synthetic stimulus;
# no profile is a documented deployment baseline, and stimulus effects are never findings.
STIMULUS = {
    "distinct_origins": "origin-only synthetic values; not the README-documented SHOPPING_ADMIN '/admin' shape",
    "path_prefix": "synthetic '/prefix' path on all six values; changes URL path structure by design",
    "trailing_slash_sensitivity": "synthetic trailing '/' on all six values; a token followed by '/' becomes '//' by design",
}
# Category is strictly the JSON path, never the value shape or the `sites` metadata.
URL_FIELD_TEMPLATES = frozenset({"start_url", "eval.reference_url"})
MARKER_RE = re.compile(r"__[A-Za-z0-9]+(?:_[A-Za-z0-9]+)*__")
NUMBER_RE = re.compile(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][-+]?[0-9]+)?")
# Exact module statements of the pinned generator (docstring excluded), as ast.unparse renders them
# on Python 3.9+. Any semantically different generator, even one that keeps the six replace calls,
# is source_contract_unrecognized.
EXPECTED_STATEMENTS = [
    "import json",
    "from browser_env.env_config import *",
    "def main() -> None:\n    with open('config_files/test.raw.json', 'r') as f:\n        raw = f.read()\n"
    + "".join("    raw = raw.replace('__%s__', %s)\n" % (name, name) for name in ORDER)
    + "    with open('config_files/test.json', 'w') as f:\n        f.write(raw)\n    data = json.loads(raw)\n"
    "    for idx, item in enumerate(data):\n        with open(f'config_files/{idx}.json', 'w') as f:\n            json.dump(item, f, indent=2)",
    "if __name__ == '__main__':\n    main()",
]
# Built-in hand witnesses (raw text byte-equal to the adopted seat-authored fixtures; selftest checks).
INDEX_WITNESS_RAW = '[{"task_id":1,"intent":"ID 1 occurs first","start_url":"__GITLAB__/index-witness/first"},{"task_id":0,"intent":"ID 0 occurs second","start_url":"__REDDIT__/index-witness/second"}]'
ORDER_WITNESS_RAW = '[{"task_id":0,"start_url":"__GITLAB__/probe"}]\n'
ORDER_WITNESS_VALUES = {"MAP": "https://map.invalid/order", "WIKIPEDIA": "__MAP__", "SHOPPING_ADMIN": "__WIKIPEDIA__", "SHOPPING": "__SHOPPING_ADMIN__", "REDDIT": "__SHOPPING__", "GITLAB": "__REDDIT__"}
LIMITS = [
    "scope: offline projection of one pinned generator over one pinned raw task file; not an actual deployment config, env_config value or observed endpoint",
    "profiles: three frozen synthetic *.invalid sensitivity stimuli, not deployment recommendations; their per-profile effects are stimulus observations, never model or task errors",
    "units: 2436 = 812 tasks x 3 synthetic profiles of one input; not independent trials, samples or files written",
    "upstream also writes one whole test.json per profile run (813 file writes per run to the same 813 paths); only the 812 per-index task objects are counted as projections",
    "offsets are Unicode codepoint offsets in the ORIGINAL raw input text, never byte offsets or step-input offsets",
    "upstream text-mode I/O uses the locale encoding and universal newlines; the pinned raw file is ASCII without carriage returns, so that difference is inert here",
    "no runtime evaluator, browser, helper, judge, task-validity, model-performance or contamination claim; unread metadata such as sites is not a consumed predicate",
    "projected_task keeps source key order; would_be_file_sha256 = sha256 of json.dumps(task, indent=2), the bytes upstream json.dump writes; json_pointer is rooted at the parsed task array (/<output_index>/...)",
    "per-token task counts are not additive (a task may carry several tokens); a changed leaf's tokens are the six tokens literally present in its ORIGINAL text; category is by JSON path, so non_url_field leaves may hold URL-shaped strings",
    "frozen data cannot reveal replacement order (no profile value contains a token) or positional naming (index == task_id); the built-in order and index witnesses below show both",
]


class Unevaluable(Exception):
    def __init__(self, finding, **detail):
        super().__init__(finding)
        self.finding = {"id": finding, **detail}


def source_contract(source):
    """Extract the replacement contract from generator bytes as inert AST data."""
    try:
        tree = ast.parse(source)
    except SyntaxError as error:
        raise Unevaluable("source_contract_unrecognized", detail="syntax: " + str(error))
    star = [node.lineno for node in tree.body if isinstance(node, ast.ImportFrom) and node.module == "browser_env.env_config" and [a.name for a in node.names] == ["*"]]
    mains = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "main"]
    if not star or len(mains) != 1:
        raise Unevaluable("source_contract_unrecognized", detail="missing star import or unique main")
    steps, parse_line, loop = [], None, None
    for statement in mains[0].body:
        value = getattr(statement, "value", None)
        if isinstance(statement, ast.Assign) and isinstance(value, ast.Call) and isinstance(value.func, ast.Attribute) and value.func.attr == "replace":
            target, call = statement.targets, value
            if not (len(target) == 1 and isinstance(target[0], ast.Name) and target[0].id == "raw" and isinstance(call.func.value, ast.Name) and call.func.value.id == "raw"
                    and len(call.args) == 2 and not call.keywords and isinstance(call.args[0], ast.Constant) and isinstance(call.args[0].value, str) and isinstance(call.args[1], ast.Name)):
                raise Unevaluable("source_contract_unrecognized", detail="non-literal replace step", line=statement.lineno)
            if parse_line is not None:
                raise Unevaluable("source_contract_unrecognized", detail="replace after parse", line=statement.lineno)
            steps.append({"token": call.args[0].value, "name": call.args[1].id, "line": statement.lineno})
        elif isinstance(statement, ast.Assign) and ast.unparse(statement) == "data = json.loads(raw)":
            parse_line = statement.lineno
        elif isinstance(statement, ast.For) and ast.unparse(statement.target) == "(idx, item)" and ast.unparse(statement.iter) == "enumerate(data)":
            loop = statement
    if [(s["token"], s["name"]) for s in steps] != [("__%s__" % name, name) for name in ORDER]:
        raise Unevaluable("source_contract_unrecognized", detail="replacement tokens/order/names differ", observed=[(s["token"], s["name"]) for s in steps])
    filename = [ast.unparse(node) for node in ast.walk(loop) if isinstance(node, ast.JoinedStr)] if loop else []
    if parse_line is None or filename != ["f'config_files/{idx}.json'"]:
        raise Unevaluable("source_contract_unrecognized", detail="parse or enumerate-index output contract missing")
    statements = [node for node in tree.body if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str))]
    rendered = [ast.unparse(node).replace("for (idx, item) in", "for idx, item in") for node in statements]  # 3.9/3.10 parenthesize tuple targets
    if rendered != EXPECTED_STATEMENTS:
        index = next((i for i, (a, b) in enumerate(zip(rendered, EXPECTED_STATEMENTS)) if a != b), min(len(rendered), len(EXPECTED_STATEMENTS)))
        raise Unevaluable("source_contract_unrecognized", detail="module statements differ from the persisted exact generator contract", statement_index=index)
    return {"authority": "inert AST facts of pinned generator bytes; never imported or executed; exact statement match", "env_config_star_import_line": star[0],
            "replace_steps": steps, "parse_line": parse_line, "enumerate_loop_line": loop.lineno,
            "per_task_filename_template": "config_files/{idx}.json", "output_index": "enumerate position, not item task_id"}


def read_pinned(root):
    """Read every pinned input once and retain only authenticated bytes."""
    try:
        manifest_bytes = (root / MANIFEST).read_bytes()
    except OSError as error:
        raise Unevaluable("input_missing", path=MANIFEST, detail=type(error).__name__)
    if hashlib.sha256(manifest_bytes).hexdigest() != MANIFEST_SHA256:
        raise Unevaluable("manifest_tampered")
    manifest = json.loads(manifest_bytes)
    if sorted(manifest["files"]) != sorted([GENERATOR, RAW, PROFILES]) or tuple(manifest["replacement_order"]) != ORDER:
        raise Unevaluable("manifest_contract_mismatch")
    verified = {}
    for relative, pin in manifest["files"].items():
        try:
            data = (root / relative).read_bytes()
        except OSError as error:
            raise Unevaluable("input_missing", path=relative, detail=type(error).__name__)
        if hashlib.sha256(data).hexdigest() != pin["sha256"]:
            raise Unevaluable("snapshot_tampered", path=relative)
        verified[relative] = data
    return manifest, verified


def check_profiles(profiles):
    if not isinstance(profiles, dict):
        raise Unevaluable("profile_invalid_type", path="$")
    missing, extra = sorted(set(STIMULUS) - set(profiles)), sorted(set(profiles) - set(STIMULUS))
    if missing or extra:
        raise Unevaluable("profile_missing" if missing else "profile_unexpected", profiles=missing or extra)
    for name, profile in profiles.items():
        values = profile.get("values") if isinstance(profile, dict) else None
        if not isinstance(values, dict) or not isinstance(profile.get("purpose"), str):
            raise Unevaluable("profile_invalid_type", profile=name)
        check_values(values, name)


def check_values(values, name):
    for key in ORDER:
        if key not in values:
            raise Unevaluable("profile_missing_key", profile=name, key=key)
        if not isinstance(values[key], str):
            raise Unevaluable("profile_invalid_type", profile=name, key=key)
    if set(values) - set(ORDER):
        raise Unevaluable("profile_unexpected_key", profile=name, keys=sorted(set(values) - set(ORDER)))


def project(raw_text, values):
    """Exactly the generator's six ordered global str.replace calls on serialized text."""
    text, steps = raw_text, []
    for name in ORDER:
        token = "__%s__" % name
        steps.append({"name": name, "token": token, "applied_replacements": text.count(token)})
        text = text.replace(token, values[name])
    return text, steps


def string_spans(text):
    """Codepoint spans [start, end) of every JSON string literal with its path and key/value role."""
    spans, length = [], len(text)

    def skip(i):
        while i < length and text[i] in " \t\n\r":
            i += 1
        return i

    def value(i, path):
        i = skip(i)
        char = text[i]
        if char == '"':
            decoded, end = json.decoder.scanstring(text, i + 1)
            spans.append((i, end, path, "value", decoded))
            return end
        if char in "{[":
            close, index = ("}" if char == "{" else "]"), 0
            i = skip(i + 1)
            if text[i] == close:
                return i + 1
            while True:
                i = skip(i)
                if char == "{":
                    key, end = json.decoder.scanstring(text, i + 1)
                    spans.append((i, end, path, "key", key))
                    i = skip(end)
                    assert text[i] == ":"
                    i = value(i + 1, path + (key,))
                else:
                    i = value(i, path + (index,))
                    index += 1
                i = skip(i)
                if text[i] == ",":
                    i += 1
                    continue
                assert text[i] == close
                return i + 1
        for literal in ("true", "false", "null", "NaN", "Infinity", "-Infinity"):
            if text.startswith(literal, i):
                return i + len(literal)
        match = NUMBER_RE.match(text, i)
        assert match, i
        return match.end()

    end = skip(value(0, ()))
    assert end == length
    return spans


def pointer(path):
    return "".join("/" + str(part).replace("~", "~0").replace("/", "~1") for part in path)


def template(path):
    parts = []
    for part in path[1:]:
        if not isinstance(part, int):
            parts.append(part)
        elif parts:
            parts[-1] += "[]"
        else:
            parts.append("[]")
    return ".".join(parts)


def provenance(raw_text, spans):
    starts = [span[0] for span in spans]
    records = []
    for name in ORDER:
        token, at = "__%s__" % name, raw_text.find("__%s__" % name)
        while at != -1:
            index = bisect.bisect_right(starts, at) - 1
            span = spans[index] if index >= 0 and spans[index][0] < at and at + len(token) <= spans[index][1] else None
            path = span[2] + ((span[4],) if span and span[3] == "key" else ()) if span else None
            records.append({"token": token, "original_input_codepoint_offset": at, "string_role": span[3] if span else "outside_string",
                            "json_pointer": pointer(span[2]) if span else None, "task_index": path[0] if path else None,
                            "path_template": template(span[2]) if span else None})
            at = raw_text.find(token, at + len(token))
    return records


def diff(original, projected, path, changed, problems):
    if type(original) is not type(projected):
        problems.append(pointer(path))
    elif isinstance(original, dict):
        if list(original) != list(projected):
            problems.append(pointer(path))
        else:
            for key in original:
                diff(original[key], projected[key], path + (key,), changed, problems)
    elif isinstance(original, list):
        if len(original) != len(projected):
            problems.append(pointer(path))
        else:
            for index, item in enumerate(original):
                diff(item, projected[index], path + (index,), changed, problems)
    elif isinstance(original, str):
        if original != projected:
            changed.append((path, original, projected))
    elif original != projected:
        problems.append(pointer(path))


def string_values(node, keys=False):
    """Decoded string leaves in document order; object keys only when requested."""
    if isinstance(node, dict):
        for key, value in node.items():
            if keys:
                yield key
            yield from string_values(value, keys)
    elif isinstance(node, list):
        for value in node:
            yield from string_values(value, keys)
    elif isinstance(node, str):
        yield node


def audit_text(raw_text, profiles, expected_population=None):
    """Project one raw serialized text under every profile; return result and invariant findings."""
    findings = []
    original = json.loads(raw_text)
    spans = string_spans(raw_text)
    occurrences = provenance(raw_text, spans)
    tokens = ["__%s__" % name for name in ORDER]
    ids = [task.get("task_id") if isinstance(task, dict) else None for task in original] if isinstance(original, list) else []
    if not isinstance(original, list) or (expected_population is not None and (len(original) != expected_population or sorted(ids) != list(range(expected_population)))):
        findings.append({"id": "input_population_mismatch"})
    key_paths = collections.Counter((span[2], span[4]) for span in spans if span[3] == "key")
    duplicate_keys = sorted(pointer(path + (key,)) for (path, key), count in key_paths.items() if count > 1)
    if duplicate_keys:
        findings.append({"id": "duplicate_json_key", "pointers": duplicate_keys[:20], "count": len(duplicate_keys)})
    markers = collections.Counter(match.group() for match in MARKER_RE.finditer(raw_text) if match.group() not in tokens)
    population = {
        "input_task_count": len(original) if isinstance(original, list) else None, "distinct_task_ids": len(set(map(json.dumps, ids))),
        "original_occurrences_by_token": {token: raw_text.count(token) for token in tokens},
        "occurrence_roles": dict(collections.Counter(record["string_role"] for record in occurrences)),
        "tasks_with_token": {token: len({r["task_index"] for r in occurrences if r["token"] == token}) for token in tokens},
        "tasks_with_any_token": len({r["task_index"] for r in occurrences}),
        "other_double_underscore_markers": dict(sorted(markers.items())),
        "tokens_followed_by_slash": sum(raw_text.startswith("/", r["original_input_codepoint_offset"] + len(r["token"])) for r in occurrences),
        "duplicate_object_keys": len(duplicate_keys),
    }
    if population["occurrence_roles"].get("key") or population["occurrence_roles"].get("outside_string"):
        findings.append({"id": "token_outside_string_value", "roles": population["occurrence_roles"]})
    results, index_mismatches = {}, []
    if isinstance(original, list):
        index_mismatches = [{"output_index": i, "task_id": task_id} for i, task_id in enumerate(ids) if task_id != i]
    for name, profile in profiles.items():
        projected_text, steps = project(raw_text, profile["values"])
        record = {"purpose": profile["purpose"], "stimulus_class": STIMULUS.get(name), "values": profile["values"], "steps": steps,
                  "projected_text_sha256": hashlib.sha256(projected_text.encode("utf-8")).hexdigest(),
                  "remaining_known_tokens_text": {token: projected_text.count(token) for token in tokens}}
        try:
            projected = json.loads(projected_text)
        except ValueError as error:
            findings.append({"id": "projection_json_invalid", "profile": name, "detail": str(error)})
            record["parsed_task_count"] = None
            results[name] = record
            continue
        changed, problems = [], []
        diff(original, projected, (), changed, problems)
        if problems:
            findings.append({"id": "projection_structure_changed", "profile": name, "paths": problems[:20], "count": len(problems)})
        decoded = list(string_values(projected, keys=True))
        record["remaining_known_tokens_decoded"] = {token: sum(text.count(token) for text in decoded) for token in tokens}
        by_task, unexplained = collections.defaultdict(list), 0
        for path, before, after in changed:
            carried = [token for token in tokens if token in before]
            unexplained += not carried
            by_task[path[0]].append({"json_pointer": pointer(path), "path_template": template(path),
                                     "category": "url_field" if template(path) in URL_FIELD_TEMPLATES else "non_url_field",
                                     "tokens": carried, "original": before, "projected": after})
        carriers = sum(1 for text in string_values(original) if any(token in text for token in tokens))
        if unexplained:
            findings.append({"id": "leaf_change_unexplained", "profile": name, "count": unexplained})
        if not problems and carriers != len(changed):
            findings.append({"id": "token_leaf_unchanged", "profile": name, "token_leaves": carriers, "changed": len(changed)})
        leaves_flat = [leaf for items in by_task.values() for leaf in items]
        junctions = sum(1 for r in occurrences if raw_text.startswith("/", r["original_input_codepoint_offset"] + len(r["token"])) and profile["values"][r["token"][2:-2]].endswith("/"))
        record.update({
            "parsed_task_count": len(projected) if isinstance(projected, list) else None,
            "string_leaf_count": sum(1 for _ in string_values(projected)), "changed_leaf_count": len(changed), "changed_task_count": len(by_task),
            "changed_leaves_by_category": dict(sorted(collections.Counter(leaf["category"] for leaf in leaves_flat).items())),
            "changed_leaves_by_path_template": dict(sorted(collections.Counter(leaf["path_template"] for leaf in leaves_flat).items())),
            "changed_leaves_with_multiple_occurrences": sum(1 for path, before, _ in changed if sum(before.count(t) for t in tokens) > 1),
            "changed_leaves_by_token": {token: sum(1 for leaf in leaves_flat if token in leaf["tokens"]) for token in tokens},
            "changed_tasks_by_token": {token: len({task for task, items in by_task.items() if any(token in leaf["tokens"] for leaf in items)}) for token in tokens},
            "stimulus_observations": {"value_slash_then_raw_slash_junctions": junctions},
            "tasks": [{"output_index": i, "output_filename": "config_files/%d.json" % i,
                       "task_id": task.get("task_id") if isinstance(task, dict) else None,
                       "index_equals_task_id": isinstance(task, dict) and task.get("task_id") == i,
                       "would_be_file_sha256": hashlib.sha256(json.dumps(task, indent=2).encode("utf-8")).hexdigest(),
                       "projected_task": task, "changed_leaves": by_task.get(i, [])} for i, task in enumerate(projected)] if isinstance(projected, list) else [],
        })
        if any(record["remaining_known_tokens_text"].values()) or any(record["remaining_known_tokens_decoded"].values()):
            findings.append({"id": "known_token_remaining", "profile": name})
        if expected_population is not None and record["parsed_task_count"] != expected_population:
            findings.append({"id": "projection_population_changed", "profile": name})
        results[name] = record
    population["task_profile_projections"] = sum(len(r.get("tasks", [])) for r in results.values())
    population["profile_count"] = len(results)
    return {"population": population, "occurrence_provenance": occurrences, "profiles": results,
            "index_mapping": {"output_index_rule": "enumerate position", "unit": "input tasks (profile-invariant)",
                              "index_equals_task_id_count": len(ids) - len(index_mismatches), "index_task_id_mismatches": index_mismatches}}, findings


def witnesses():
    """Run the built-in hand witnesses through the same projection path; never pinned-data evidence."""
    index, _ = audit_text(INDEX_WITNESS_RAW, {"hand": {"purpose": "hand witness", "values": {n: "http://%s.invalid:1" % n.lower().replace("_", "-") for n in ORDER}}})
    order_text, order_steps = project(ORDER_WITNESS_RAW, ORDER_WITNESS_VALUES)
    mapping_order = ORDER_WITNESS_RAW
    for name in ORDER_WITNESS_VALUES:
        mapping_order = mapping_order.replace("__%s__" % name, ORDER_WITNESS_VALUES[name])
    return {"index": {"raw": INDEX_WITNESS_RAW, "records": [{"output_filename": t["output_filename"], "task_id": t["task_id"], "index_equals_task_id": t["index_equals_task_id"]} for t in index["profiles"]["hand"]["tasks"]]},
            "order": {"raw": ORDER_WITNESS_RAW, "values": ORDER_WITNESS_VALUES, "applied_replacements": [s["applied_replacements"] for s in order_steps],
                      "source_order_text": order_text, "mapping_order_text": mapping_order}}


def audit(root):
    manifest, verified = read_pinned(root)
    contract = source_contract(verified[GENERATOR])
    profiles = json.loads(verified[PROFILES])
    check_profiles(profiles)
    raw_text = verified[RAW].decode("utf-8")
    result, findings = audit_text(raw_text, profiles, expected_population=POPULATION)
    if result["population"]["task_profile_projections"] != POPULATION * len(STIMULUS):
        findings.append({"id": "projection_count_invalid"})
    result.update(inputs={path: pin["sha256"] for path, pin in manifest["files"].items()}, manifest_sha256=MANIFEST_SHA256,
                  upstream_revision=manifest["upstream_revision"], source_contract=contract,
                  raw_text_sha256=hashlib.sha256(verified[RAW]).hexdigest(), witnesses=witnesses(), findings=findings, limitations=LIMITS)
    return result, int(bool(findings))


def summary_lines(result, code):
    lines = ["LIMIT " + limit for limit in result.get("limitations", LIMITS)]
    lines += ["FINDING " + json.dumps(finding, sort_keys=True) for finding in result.get("findings", [])]
    population = result.get("population")
    if population:
        lines.append("POPULATION " + json.dumps({key: population[key] for key in ("input_task_count", "distinct_task_ids", "profile_count", "task_profile_projections", "tasks_with_any_token")}, sort_keys=True))
        lines.append("ORIGINAL_OCCURRENCES_BY_TOKEN " + json.dumps(population["original_occurrences_by_token"]))
        lines.append("TASKS_WITH_TOKEN_NOT_ADDITIVE " + json.dumps(population["tasks_with_token"]))
        lines.append("OCCURRENCE_ROLES " + json.dumps(population["occurrence_roles"], sort_keys=True))
        lines.append("OTHER_MARKERS_NOT_ENV_TOKENS " + json.dumps(population["other_double_underscore_markers"]))
        lines.append("INDEX " + json.dumps({"unit": "input tasks", "index_equals_task_id_count": result["index_mapping"]["index_equals_task_id_count"], "index_task_id_mismatches": len(result["index_mapping"]["index_task_id_mismatches"])}))
        lines.append("DUPLICATE_OBJECT_KEYS %d" % population["duplicate_object_keys"])
        if "witnesses" in result:
            lines.append("INDEX_WITNESS hand " + json.dumps(result["witnesses"]["index"]["records"]))
            order = result["witnesses"]["order"]
            lines.append("ORDER_WITNESS hand applied_replacements=%s source_order_text=%s mapping_order_text=%s" % (json.dumps(order["applied_replacements"]), json.dumps(order["source_order_text"]), json.dumps(order["mapping_order_text"])))
        for name, record in result["profiles"].items():
            lines.append("PROFILE %s purpose=%s" % (name, json.dumps(record["purpose"])))
            lines.append("PROFILE %s stimulus=%s" % (name, json.dumps(record["stimulus_class"])))
            lines.append("PROFILE %s applied_replacements=%s" % (name, json.dumps({s["name"]: s["applied_replacements"] for s in record["steps"]})))
            keys = ("parsed_task_count", "string_leaf_count", "changed_leaf_count", "changed_task_count", "changed_leaves_with_multiple_occurrences", "projected_text_sha256")
            lines.append("PROFILE %s %s" % (name, " ".join("%s=%s" % (key, record.get(key)) for key in keys)))
            for key in ("changed_leaves_by_category", "changed_leaves_by_path_template", "changed_leaves_by_token", "changed_tasks_by_token", "remaining_known_tokens_text", "remaining_known_tokens_decoded", "stimulus_observations"):
                lines.append("PROFILE %s %s=%s" % (name, key, json.dumps(record.get(key), sort_keys=key != "changed_leaves_by_token" and key != "changed_tasks_by_token")))
    lines.append("TOTAL findings=%d exit=%d" % (len(result.get("findings", [])), code))
    return lines


def selftest(root):
    cases = []
    values = {name: "http://%s.invalid:1" % name.lower().replace("_", "-") for name in ORDER}

    def run(raw, vals=values):
        return audit_text(raw, {"distinct_origins": {"purpose": "hand", "values": vals}})

    # Six tokens, one leaf each, plus a non-URL leaf: global replacement reaches intent too.
    raw = json.dumps([{"task_id": 0, "start_url": "__%s__/p" % name, "intent": "see __%s__" % name} for name in ORDER])
    result, findings = run(raw)
    record = result["profiles"]["distinct_origins"]
    assert not findings and [s["applied_replacements"] for s in record["steps"]] == [2] * 6
    assert record["changed_leaf_count"] == 12 and record["changed_leaves_by_category"] == {"non_url_field": 6, "url_field": 6}
    assert record["tasks"][5]["projected_task"]["intent"] == "see http://map.invalid:1"
    assert list(record["changed_leaves_by_token"].values()) == [2] * 6 and list(record["changed_tasks_by_token"].values()) == [1] * 6
    assert list(result["population"]["original_occurrences_by_token"].values()) == [2] * 6 and list(result["population"]["tasks_with_token"].values()) == [1] * 6
    cases.append("six_tokens_and_non_url_field")
    # Two occurrences in one leaf: occurrence, leaf and task units stay separate.
    result, _ = run('[{"task_id": 0, "start_url": "__GITLAB__/a |OR| __GITLAB__/b", "x": ["__REDDIT__"]}]')
    record = result["profiles"]["distinct_origins"]
    assert result["population"]["original_occurrences_by_token"]["__GITLAB__"] == 2 and record["changed_leaf_count"] == 2 and record["changed_task_count"] == 1
    assert record["changed_leaves_with_multiple_occurrences"] == 1 and record["tasks"][0]["changed_leaves"][1]["json_pointer"] == "/0/x/0"
    cases.append("units_not_pooled")
    # Codepoint, not byte, offsets in the original input frame, and key/value role.
    raw = '[{"intent": "\u00e9\u00e9 __MAP__", "__GITLAB__": 1}]'
    result, findings = run(raw)
    prov = {r["token"]: r for r in result["occurrence_provenance"]}
    assert prov["__MAP__"]["original_input_codepoint_offset"] == raw.index("__MAP__") == 16 and len(raw[:16].encode()) == 18
    assert prov["__GITLAB__"]["string_role"] == "key" and {f["id"] for f in findings} == {"token_outside_string_value", "projection_structure_changed"}
    cases.append("codepoint_offsets_and_key_token")
    # Escaped token spelling is not literal serialized text: raw projection leaves it, decoded census sees it.
    result, findings = run(json.dumps([{"intent": "\\u005f\\u005f%s__ and __%s__" % (name, name)} for name in ORDER]).replace("\\\\u005f", "\\u005f"))
    record = result["profiles"]["distinct_origins"]
    assert [s["applied_replacements"] for s in record["steps"]] == [1] * 6 and list(record["remaining_known_tokens_text"].values()) == [0] * 6
    assert list(record["remaining_known_tokens_decoded"].values()) == [1] * 6 and {f["id"] for f in findings} == {"known_token_remaining"}
    cases.append("escaped_token_not_replaced")
    # Quote or backslash values break JSON instead of being repaired; a JSON escape is decoded, not kept literal.
    for bad in ('http://x"y', "http://x\\y"):
        _, findings = run('[{"start_url": "__GITLAB__"}]', dict(values, GITLAB=bad))
        assert [f["id"] for f in findings] == ["projection_json_invalid"], (bad, findings)
    result, _ = run('[{"start_url": "__GITLAB__"}]', dict(values, GITLAB="a\\nb"))
    assert result["profiles"]["distinct_origins"]["tasks"][0]["projected_task"]["start_url"] == "a\nb"
    cases.append("quote_backslash_decode_failure_and_escape_semantics")
    # Missing or non-string map entries are could-not-evaluate findings.
    for name, vals, expected in (("missing", {k: v for k, v in values.items() if k != "MAP"}, "profile_missing_key"), ("nonstring", dict(values, MAP=7), "profile_invalid_type"), ("extra", dict(values, EXTRA="x"), "profile_unexpected_key")):
        try:
            check_values(vals, name)
        except Unevaluable as error:
            assert error.finding["id"] == expected
        else:
            raise AssertionError(name)
    cases.append("profile_map_errors")
    # Seat-authored hand fixtures (independent writers), authenticated, then consumed unchanged.
    assert {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted((root / HAND).iterdir())} == HAND_SHA256, "hand_fixture_tampered"
    cases.append("hand_fixtures_authenticated")
    order_case = json.loads((root / HAND / "cascade-order.case.json").read_text(encoding="utf-8"))
    text, steps = project(order_case["raw_serialized_text"], order_case["values"])
    assert text == order_case["expected_projected_text"] and [s["applied_replacements"] for s in steps] == order_case["expected_dynamic_replacement_hits_by_source_step"]
    wrong = order_case["raw_serialized_text"]
    for name in order_case["mapping_insertion_order"]:
        wrong = wrong.replace("__%s__" % name, order_case["values"][name])
    assert wrong == order_case["predicted_mapping_order_mutant_text"] != text
    assert order_case["raw_serialized_text"] == ORDER_WITNESS_RAW and order_case["values"] == ORDER_WITNESS_VALUES
    built_in = witnesses()
    assert built_in["order"]["source_order_text"] == text and built_in["order"]["mapping_order_text"] == wrong
    cases.append("hand_cascade_order_" + order_case["case_id"])
    url_case = json.loads((root / HAND / "url-only.fixture.json").read_text(encoding="utf-8"))
    url_expected = json.loads((root / HAND / "url-only.expected.json").read_text(encoding="utf-8"))
    result, findings = run(url_case["raw_text"], url_case["values"])
    record = result["profiles"]["distinct_origins"]
    assert [t["projected_task"] for t in record["tasks"]] == url_expected["projection"] and not findings
    assert sorted("$[%d]%s" % (int(l["json_pointer"].split("/")[1]), "".join("." + p for p in l["json_pointer"].split("/")[2:])) for t in record["tasks"] for l in t["changed_leaves"]) == url_expected["changed_string_leaf_paths"]
    assert {k: v for k, v in result["population"]["original_occurrences_by_token"].items()} == url_expected["raw_replacement_occurrences_by_token"]
    assert result["population"]["other_double_underscore_markers"] == {"__last_url__": 1, "__page__": 1}
    categories = {l["json_pointer"]: l["category"] for t in record["tasks"] for l in t["changed_leaves"]}
    assert categories == {"/0/start_url": "url_field", "/0/intent": "non_url_field", "/0/eval/reference_answer_raw_annotation": "non_url_field"}
    cases.append("hand_url_only_" + url_case["case_id"])
    index_case = json.loads((root / HAND / "index-shuffled-ids.fixture.json").read_text(encoding="utf-8"))
    assert index_case["input_raw_text"] == INDEX_WITNESS_RAW
    result, findings = run(index_case["input_raw_text"], index_case["profile_values"])
    tasks = result["profiles"]["distinct_origins"]["tasks"]
    assert [{"task_id": t["task_id"], "output_ordinal": t["output_index"], "output_filename": t["output_filename"], "projected_task": t["projected_task"]} for t in tasks] == index_case["expected_records"]
    assert [t["index_equals_task_id"] for t in tasks] == index_case["expected_index_equals_task_id"] and result["index_mapping"]["index_task_id_mismatches"] == [{"output_index": 0, "task_id": 1}, {"output_index": 1, "task_id": 0}]
    assert built_in["index"]["records"] == [{"output_filename": "config_files/0.json", "task_id": 1, "index_equals_task_id": False}, {"output_filename": "config_files/1.json", "task_id": 0, "index_equals_task_id": False}]
    cases.append("hand_index_" + index_case["case_id"])
    # Trailing-slash values are substituted verbatim: '//' junctions are never normalized or repaired.
    slash = dict(values, GITLAB="http://gitlab.invalid:1/")
    result, findings = run('[{"start_url": "__GITLAB__/a", "eval": {"program_html": [{"required_contents": {"must_include": ["__GITLAB__/b"]}}]}}]', slash)
    record = result["profiles"]["distinct_origins"]
    assert not findings and record["tasks"][0]["projected_task"]["start_url"] == "http://gitlab.invalid:1//a"
    assert record["stimulus_observations"] == {"value_slash_then_raw_slash_junctions": 2}
    assert [(l["path_template"], l["category"], l["projected"]) for l in record["tasks"][0]["changed_leaves"]] == [("start_url", "url_field", "http://gitlab.invalid:1//a"), ("eval.program_html[].required_contents.must_include[]", "non_url_field", "http://gitlab.invalid:1//b")]
    cases.append("verbatim_slash_and_path_category")
    # Duplicate keys diverge text and object views; list-shaped tasks still get templates; source key order is kept.
    _, findings = run('[{"a": "__GITLAB__", "a": "__REDDIT__"}]')
    assert "duplicate_json_key" in {f["id"] for f in findings}
    result, findings = run('[["__GITLAB__"], {"z": "__MAP__", "a": 1}]')
    assert not findings and result["profiles"]["distinct_origins"]["tasks"][0]["changed_leaves"][0]["path_template"] == "[]"
    assert list(result["profiles"]["distinct_origins"]["tasks"][1]["projected_task"]) == ["z", "a"]
    cases.append("duplicate_keys_list_tasks_key_order")
    # Source contract: order swap, literal RHS, extra step, filename, mutated data and dropped writes are unrecognized.
    source = (root / GENERATOR).read_text(encoding="utf-8")
    assert [s["name"] for s in source_contract(source)["replace_steps"]] == list(ORDER)
    for name, mutated in (("order_swap", source.replace('raw = raw.replace("__GITLAB__", GITLAB)\n    raw = raw.replace("__REDDIT__", REDDIT)', 'raw = raw.replace("__REDDIT__", REDDIT)\n    raw = raw.replace("__GITLAB__", GITLAB)')),
                          ("literal_rhs", source.replace('"__MAP__", MAP)', '"__MAP__", "x")')),
                          ("extra_step", source.replace("    data = json.loads(raw)", '    raw = raw.replace("__X__", X)\n    data = json.loads(raw)')),
                          ("id_filename", source.replace("{idx}.json", "{item['task_id']}.json")),
                          ("data_mutated", source.replace("    data = json.loads(raw)\n", "    data = json.loads(raw)\n    data = data[::2]\n")),
                          ("write_dropped", source.replace("            json.dump(item, f, indent=2)", "            pass")),
                          ("text_truncated", source.replace("    with open(\"config_files/test.json\"", "    raw = raw[:100]\n    with open(\"config_files/test.json\""))):
        assert mutated != source, name
        try:
            source_contract(mutated)
        except Unevaluable as error:
            assert error.finding["id"] == "source_contract_unrecognized"
            cases.append("source_" + name)
        else:
            raise AssertionError(name)
    # Exit mapping: findings exit 1, could-not-evaluate and unexpected errors exit 2.
    from unittest.mock import patch
    for raised, expected_code, expected_id in ((None, 1, "x"), (Unevaluable("snapshot_tampered"), 2, "snapshot_tampered"), (RuntimeError("boom"), 2, "internal_error")):
        def fake(_root, raised=raised):
            if raised:
                raise raised
            return {"findings": [{"id": "x"}], "limitations": LIMITS}, 1
        captured = []
        with patch(__name__ + ".audit", fake), patch("builtins.print", lambda text: captured.append(text)):
            assert main(["--json"]) == expected_code and json.loads(captured[0])["findings"][0]["id"] == expected_id
    cases.append("exit_mapping")
    with tempfile.TemporaryDirectory(prefix="kengaku-r29-projection-", dir="/tmp") as temp:
        scratch = Path(temp)
        for relative in (MANIFEST, GENERATOR, RAW, PROFILES):
            (scratch / relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / relative, scratch / relative)
        child = [sys.executable, "-I", "-S", str(Path(__file__).resolve())]
        command = child + ["--root", str(scratch), "--json"]
        optimized = subprocess.run([sys.executable, "-I", "-S", "-O"] + child[3:] + ["--root", str(scratch), "--summary"], capture_output=True, text=True, env={})
        assert optimized.returncode == 2 and "assertions_disabled" in optimized.stdout, optimized
        cases.append("cli_optimized_refused")

        def cli(name, expected, code=2):
            output = subprocess.run(command, capture_output=True, text=True, env={})
            assert output.returncode == code and json.loads(output.stdout)["findings"][0]["id"] == expected, (name, output.returncode, output.stdout[:300], output.stderr[-300:])
            cases.append(name)

        target = scratch / RAW
        target.write_bytes(target.read_bytes() + b" ")
        cli("cli_snapshot_tampered", "snapshot_tampered")
        target.unlink()
        cli("cli_input_missing", "input_missing")
        shutil.copyfile(root / RAW, target)
        manifest = scratch / MANIFEST
        # Coherent rebinding: change the input AND its manifest pin; the persisted manifest pin rejects it.
        target.write_bytes(target.read_bytes().replace(b'"task_id": 0,', b'"task_id": 0, "extra": "__MAP__",', 1))
        rebound = json.loads(manifest.read_bytes())
        rebound["files"][RAW]["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
        manifest.write_text(json.dumps(rebound, indent=2) + "\n", encoding="utf-8")
        cli("cli_coherent_rebinding", "manifest_tampered")
        shutil.copyfile(root / RAW, target)
        shutil.copyfile(root / MANIFEST, manifest)
        # Post-read replacement: only retained authenticated bytes may feed projection.
        from unittest.mock import patch
        original_read = Path.read_bytes
        for relative, replacement in ((RAW, b"[1,2,3]"), (GENERATOR, b"x = 1\n"), (PROFILES, b"{}")):
            victim, swapped = scratch / relative, []

            def replace_after_read(path, victim=victim, swapped=swapped, replacement=replacement):
                data = original_read(path)
                if path == victim and not swapped:
                    swapped.append(True)
                    path.write_bytes(replacement)
                return data
            with patch.object(Path, "read_bytes", replace_after_read):
                retained, code = audit(scratch)
            assert swapped and code == 0 and retained["population"]["task_profile_projections"] == 2436, relative
            shutil.copyfile(root / relative, victim)
            cases.append("post_read_replacement_" + Path(relative).name)
        manifest.write_bytes(manifest.read_bytes() + b" ")
        cli("cli_manifest_tampered", "manifest_tampered")
    print("SELFTEST clean cases=%d %s" % (len(cases), ",".join(cases)))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Offline source-faithful projection of pinned WebArena generate_test_data.py.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--summary", action="store_true", help="human-readable lines (the default)")
    mode.add_argument("--json", action="store_true")
    mode.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if not __debug__:
        result, code = {"findings": [{"id": "assertions_disabled", "detail": "python -O strips load-bearing checks"}], "limitations": LIMITS}, 2
    elif args.selftest:
        return selftest(args.root)
    else:
        try:
            result, code = audit(args.root)
        except Unevaluable as error:
            result, code = {"findings": [error.finding], "limitations": LIMITS}, 2
        except Exception as error:
            result, code = {"findings": [{"id": "internal_error", "detail": repr(error)}], "limitations": LIMITS}, 2
    if args.json:
        print(json.dumps(result, separators=(",", ":")))
    else:
        print("\n".join(summary_lines(result, code)))
    return code


if __name__ == "__main__":
    raise SystemExit(main())

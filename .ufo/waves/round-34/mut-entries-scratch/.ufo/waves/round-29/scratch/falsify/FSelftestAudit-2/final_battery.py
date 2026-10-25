#!/usr/bin/env python3
"""Final battery against the PINNED HEAD instrument (sha256 5673405e...), stored in lane scratch.
Every mutant is applied to a copy; the copy is run with --selftest --root <lane>.
Kill attribution = deepest traceback frame inside the mutant file -> source line -> selftest case."""
import subprocess, sys, re, os, shutil
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
HERE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FSelftestAudit-2")
SRC = HERE / "head/config_projection.py"
W = HERE / "final_mut"; shutil.rmtree(W, ignore_errors=True); W.mkdir(parents=True)

TXT = SRC.read_text()
src_lines = TXT.splitlines()
appends = [(i+1, l.strip()) for i, l in enumerate(src_lines) if "cases.append" in l]
def case_for(n):
    c = None
    for ln, t in appends:
        if ln <= n: c = (ln, t)
    return c

M = {
 # --- prereg line 73-77 required witnesses ---
 "A1_order_reversed": ('ORDER = ("GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP")',
   'ORDER = ("MAP", "WIKIPEDIA", "SHOPPING_ADMIN", "SHOPPING", "REDDIT", "GITLAB")'),
 "A2_wrong_order_mapping_insertion": ('''    text, steps = raw_text, []
    for name in ORDER:
        token = "__%s__" % name
        steps.append({"name": name, "token": token, "applied_replacements": text.count(token)})
        text = text.replace(token, values[name])
    return text, steps''', '''    text, steps = raw_text, []
    for name in values:
        token = "__%s__" % name
        steps.append({"name": name, "token": token, "applied_replacements": text.count(token)})
        text = text.replace(token, values[name])
    return text, steps'''),
 "A3_wrong_url_only_substitution": ('''    text, steps = raw_text, []
    for name in ORDER:
        token = "__%s__" % name
        steps.append({"name": name, "token": token, "applied_replacements": text.count(token)})
        text = text.replace(token, values[name])
    return text, steps''', '''    import json as _json
    _obj = _json.loads(raw_text)
    def _walk(node):
        if isinstance(node, dict):
            for _k, _v in list(node.items()):
                if _k in ("start_url", "reference_url", "url") and isinstance(_v, str):
                    for _n in ORDER:
                        _v = _v.replace("__%s__" % _n, values[_n])
                    node[_k] = _v
                elif isinstance(_v, (dict, list)):
                    _walk(_v)
        elif isinstance(node, list):
            for _i in node:
                _walk(_i)
    _walk(_obj)
    return _json.dumps(_obj), [{"name": n, "token": "__%s__" % n, "applied_replacements": 0} for n in ORDER]'''),
 "A4_index_by_task_id_filename": ('"output_index": i, "output_filename": "config_files/%d.json" % i,',
   '"output_index": i, "output_filename": "config_files/%d.json" % (task.get("task_id") if isinstance(task, dict) else i),'),
 "A5_manifest_sha_pin_removed": ('    if hashlib.sha256(manifest_bytes).hexdigest() != MANIFEST_SHA256:\n        raise Unevaluable("manifest_tampered")',
   '    if False:\n        raise Unevaluable("manifest_tampered")'),
 "A6_snapshot_pin_removed": ('        if hashlib.sha256(data).hexdigest() != pin["sha256"]:\n            raise Unevaluable("snapshot_tampered", path=relative)',
   '        if False:\n            raise Unevaluable("snapshot_tampered", path=relative)'),
 "A7_reread_raw_from_disk": ('    raw_text = verified[RAW].decode("utf-8")', '    raw_text = (root / RAW).read_bytes().decode("utf-8")'),
 "A8_reread_generator_from_disk": ('    contract = source_contract(verified[GENERATOR])', '    contract = source_contract((root / GENERATOR).read_bytes().decode("utf-8"))'),
 "A9_reread_profiles_from_disk": ('    profiles = json.loads(verified[PROFILES])', '    profiles = json.loads((root / PROFILES).read_bytes())'),
 "A10_provenance_byte_offset": ('"original_input_codepoint_offset": at,', '"original_input_codepoint_offset": len(raw_text[:at].encode()),'),
 "A11_escape_backslash_not_decoded": ('        decoded = list(string_values(projected, keys=True))',
   '        decoded = list(string_values(projected, keys=True))\n        decoded = [d for d in decoded if "\\\\n" not in d]'),
 # --- findings/gates ---
 "B1_drop_known_token_remaining": ('        if any(record["remaining_known_tokens_text"].values()) or any(record["remaining_known_tokens_decoded"].values()):\n            findings.append({"id": "known_token_remaining", "profile": name})',
   '        if False:\n            findings.append({"id": "known_token_remaining", "profile": name})'),
 "B2_drop_leaf_change_unexplained": ('        if unexplained or (not problems and carriers != len(changed)):', '        if False:'),
 "B3_drop_token_outside_string_value": ('        findings.append({"id": "token_outside_string_value", "roles": population["occurrence_roles"]})', '        pass'),
 "B4_drop_projection_structure_changed": ('            findings.append({"id": "projection_structure_changed", "profile": name, "paths": problems[:20], "count": len(problems)})', '            pass'),
 "B5_drop_projection_count_invalid": ('    if result["population"]["task_profile_projections"] != POPULATION * len(STIMULUS):\n        findings.append({"id": "projection_count_invalid"})', '    if False:\n        findings.append({"id": "projection_count_invalid"})'),
 "B6_drop_task_population_invalid": ('        findings.append({"id": "task_population_invalid"})', '        pass'),
 "B7_drop_profile_missing_extra": ('    if missing or extra:\n        raise Unevaluable("profile_missing" if missing else "profile_unexpected", profiles=missing or extra)', '    if False:\n        raise Unevaluable("profile_missing" if missing else "profile_unexpected", profiles=missing or extra)'),
 "B8_drop_manifest_contract_check": ('    if sorted(manifest["files"]) != sorted([GENERATOR, RAW, PROFILES]) or tuple(manifest["replacement_order"]) != ORDER:\n        raise Unevaluable("manifest_contract_mismatch")', '    if False:\n        raise Unevaluable("manifest_contract_mismatch")'),
 "B9_check_values_missing_key_off": ('    for key in ORDER:\n        if key not in values:\n            raise Unevaluable("profile_missing_key", profile=name, key=key)', '    for key in ORDER:\n        if False:\n            raise Unevaluable("profile_missing_key", profile=name, key=key)'),
 "B10_check_values_extra_key_off": ('    if set(values) - set(ORDER):\n        raise Unevaluable("profile_unexpected_key", profile=name, keys=sorted(set(values) - set(ORDER)))', '    if False:\n        raise Unevaluable("profile_unexpected_key", profile=name, keys=sorted(set(values) - set(ORDER)))'),
 "B11_profile_purpose_not_required": ('        if not isinstance(values, dict) or not isinstance(profile.get("purpose"), str):\n            raise Unevaluable("profile_invalid_type", profile=name)', '        if not isinstance(values, dict):\n            raise Unevaluable("profile_invalid_type", profile=name)'),
 "B12_audit_always_exit0": ('    return result, int(bool(findings))', '    return result, 0'),
 "B13_input_missing_renamed": ('            raise Unevaluable("input_missing", path=relative)', '            raise Unevaluable("snapshot_tampered", path=relative)'),
 "B14_drop_source_order_check": ('    if [(s["token"], s["name"]) for s in steps] != [("__%s__" % name, name) for name in ORDER]:', '    if False:'),
 "B15_drop_source_filename_check": ("    if parse_line is None or filename != [\"f'config_files/{idx}.json'\"]:\n        raise Unevaluable(\"source_contract_unrecognized\", detail=\"parse or enumerate-index output contract missing\")",
   '    if parse_line is None:\n        raise Unevaluable("source_contract_unrecognized", detail="parse or enumerate-index output contract missing")'),
 "B16_string_role_inverted": ('                spans.append((i, end, path, "key", key))', '                spans.append((i, end, path, "value", key))'),
 "B17_index_equals_always_true": ('"index_equals_task_id": isinstance(task, dict) and task.get("task_id") == i,', '"index_equals_task_id": True,'),
 "B18_multi_occurrence_zero": ('"changed_leaves_with_multiple_occurrences": sum(1 for path, before, _ in changed if sum(before.count(t) for t in tokens) > 1),', '"changed_leaves_with_multiple_occurrences": 0,'),
 "B19_other_markers_zero": ('"other_double_underscore_markers": dict(sorted(markers.items())),', '"other_double_underscore_markers": {},'),
 "B20_occurrence_roles_constant": ('"occurrence_roles": dict(collections.Counter(record["string_role"] for record in occurrences)),', '"occurrence_roles": {"value": len(occurrences)},'),
 "B21_changed_task_count_leaf_based": ('"changed_leaf_count": len(changed), "changed_task_count": len(by_task),', '"changed_leaf_count": len(changed), "changed_task_count": len(changed),'),
 "B22_url_templates_only_start_url": ('URL_FIELD_TEMPLATES = frozenset({"start_url", "eval.reference_url", "eval.program_html[].url"})', 'URL_FIELD_TEMPLATES = frozenset({"start_url"})'),
 "B23_url_templates_no_program_html": ('URL_FIELD_TEMPLATES = frozenset({"start_url", "eval.reference_url", "eval.program_html[].url"})', 'URL_FIELD_TEMPLATES = frozenset({"start_url", "eval.reference_url"})'),
 "B24_url_templates_include_intent": ('URL_FIELD_TEMPLATES = frozenset({"start_url", "eval.reference_url", "eval.program_html[].url"})', 'URL_FIELD_TEMPLATES = frozenset({"start_url", "eval.reference_url", "eval.program_html[].url", "intent"})'),
 "B25_drop_start_url_template": ('URL_FIELD_TEMPLATES = frozenset({"start_url", "eval.reference_url", "eval.program_html[].url"})', 'URL_FIELD_TEMPLATES = frozenset({"eval.reference_url", "eval.program_html[].url"})'),
 "B26_projected_text_sha_zero": ('"projected_text_sha256": hashlib.sha256(projected_text.encode("utf-8")).hexdigest(),', '"projected_text_sha256": "0" * 64,'),
 "B27_would_be_file_sha_zero": ('"would_be_file_sha256": hashlib.sha256(json.dumps(task, indent=2).encode("utf-8")).hexdigest(),', '"would_be_file_sha256": "0" * 64,'),
 "B28_stimulus_class_dropped": ('"stimulus_class": STIMULUS.get(name),', '"stimulus_class": None,'),
 "B29_upstream_revision_hardcoded": ('upstream_revision=manifest["upstream_revision"],', 'upstream_revision="deadbeef",'),
 "B30_changed_leaves_by_token_occurrence_based": ('"changed_leaves_by_token": {token: sum(1 for leaf in leaves_flat if token in leaf["tokens"]) for token in tokens},', '"changed_leaves_by_token": {token: sum(leaf["tokens"].count(token) for leaf in leaves_flat) for token in tokens},'),
 "B31_profile_count_zero": ('"profile_count": len(results),', '"profile_count": 0,'),
}

def run(p, extra=()):
    return subprocess.run([sys.executable, str(p), "--selftest", "--root", LANE] + list(extra),
                          capture_output=True, text=True, timeout=900)

rows = []
for name, (old, new) in sorted(M.items()):
    if old not in TXT:
        rows.append((name, "PATCH-FAILED", "-", "-", "")); print("%-38s PATCH-FAILED" % name); continue
    p = W / ("m_%s.py" % name)
    p.write_text(TXT.replace(old, new, 1))
    r = run(p)
    if r.returncode == 0:
        rows.append((name, "SURVIVED", "-", "-", "")); print("%-38s SURVIVED" % name); continue
    fr = re.findall(r'File "([^"]+)", line (\d+), in (\S+)', r.stderr)
    inst = [(f, int(l), fn) for f, l, fn in fr if f.endswith(p.name)]
    if not inst:
        rows.append((name, "KILLED", "-", "-", (r.stderr.strip().splitlines() or [""])[-1][:90]))
        print("%-38s KILLED (no instrument frame)" % name); continue
    f, ln, fn = inst[-1]; c = case_for(ln)
    cn = c[1] if c else "?"
    cn = cn.replace("cases.append(", "").rstrip(")")
    rows.append((name, "KILLED", "L%d" % ln, fn, cn))
    print("%-38s KILLED L%-4d %-12s -> %s" % (name, ln, fn, cn))

print()
print("SURVIVED:", [r[0] for r in rows if r[1] == "SURVIVED"])
print("PATCH-FAILED:", [r[0] for r in rows if r[1] == "PATCH-FAILED"])
import json
(HERE / "final_results.json").write_text(json.dumps(rows, indent=1))

#!/usr/bin/env python3
"""Battery 2: attack the prereg-required selftest witnesses (lines 73-77)."""
import shutil, subprocess, sys, os
from pathlib import Path

SRC = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py")
LANE_ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
WORK = Path("/tmp/r29-selftest-audit/mut2")
WORK.mkdir(parents=True, exist_ok=True)

M = {
 # post-read witness: does re-reading from disk get caught?
 "M13_reread_raw_from_disk": (
   '    raw_text = verified[RAW].decode("utf-8")',
   '    raw_text = (root / RAW).read_bytes().decode("utf-8")'),
 "M14_reread_generator_from_disk": (
   '    contract = source_contract(verified[GENERATOR])',
   '    contract = source_contract((root / GENERATOR).read_bytes().decode("utf-8"))'),
 "M15_reread_profiles_from_disk": (
   '    profiles = json.loads(verified[PROFILES])',
   '    profiles = json.loads((root / PROFILES).read_bytes())'),
 # true URL-only substitution mutant
 "M16_url_only_substitution": (
   '''        changed, problems = [], []
        diff(original, projected, (), changed, problems)''',
   '''        changed, problems = [], []
        _uonly = json.loads(json.dumps(original))
        def _ru(node):
            if isinstance(node, dict):
                for _k, _v in node.items():
                    if _k in ("start_url", "reference_url", "url"):
                        if isinstance(_v, str):
                            for _n in ORDER:
                                _v = _v.replace("__%s__" % _n, profile["values"][_n])
                            node[_k] = _v
                    else:
                        _ru(_v)
            elif isinstance(node, list):
                for _i in node:
                    _ru(_i)
        _ru(_uonly)
        diff(original, _uonly, (), changed, problems)'''),
 # exit code 1 never asserted
 "M17_audit_always_exit0": (
   '    return result, int(bool(findings))',
   '    return result, 0'),
 # projection_count_invalid finding dropped
 "M18_drop_projection_count_invalid": (
   '    if result["population"]["task_profile_projections"] != POPULATION * len(STIMULUS):\n        findings.append({"id": "projection_count_invalid"})',
   '    if False:\n        findings.append({"id": "projection_count_invalid"})'),
 # task_population_invalid dropped
 "M19_drop_task_population_invalid": (
   '        findings.append({"id": "task_population_invalid"})',
   '        pass'),
 # projection_structure_changed dropped
 "M20_drop_projection_structure_changed": (
   '            findings.append({"id": "projection_structure_changed", "profile": name, "paths": problems[:20], "count": len(problems)})',
   '            pass'),
 # token_outside_string_value dropped
 "M21_drop_token_outside_string_value": (
   '        findings.append({"id": "token_outside_string_value", "roles": population["occurrence_roles"]})',
   '        pass'),
 # input_missing path broken
 "M22_input_missing_renamed": (
   '            raise Unevaluable("input_missing", path=relative)',
   '            raise Unevaluable("snapshot_tampered", path=relative)'),
 # occurrence provenance: byte offset instead of codepoint for the key token
 "M23_provenance_offset_plus_one": (
   '"original_input_codepoint_offset": at,',
   '"original_input_codepoint_offset": at + 1,'),
 # string_spans key/value role inverted
 "M24_string_role_inverted": (
   '                spans.append((i, end, path, "key", key))',
   '                spans.append((i, end, path, "value", key))'),
 # escape semantics: keep literal backslash instead of JSON-decoded
 "M25_escape_semantics_literal": (
   '        changed, problems = [], []\n        diff(original, projected, (), changed, problems)',
   '        changed, problems = [], []\n        diff(original, projected, (), changed, problems)\n        if name == "distinct_origins":\n            pass'),
 # index_equals_task_id always true
 "M26_index_equals_always_true": (
   '"index_equals_task_id": isinstance(task, dict) and task.get("task_id") == i,',
   '"index_equals_task_id": True,'),
 # changed_leaves_with_multiple_occurrences always 0
 "M27_multi_occurrence_always_zero": (
   '"changed_leaves_with_multiple_occurrences": sum(1 for path, before, _ in changed if sum(before.count(t) for t in tokens) > 1),',
   '"changed_leaves_with_multiple_occurrences": 0,'),
}

def run(path):
    return subprocess.run([sys.executable, str(path), "--selftest", "--root", LANE_ROOT],
                          capture_output=True, text=True, timeout=600)

for name, (old, new) in M.items():
    text = SRC.read_text()
    if old not in text:
        print("%-42s PATCH-FAILED" % name); continue
    p = WORK / ("mut_%s.py" % name)
    p.write_text(text.replace(old, new, 1))
    r = run(p)
    st = "KILLED" if r.returncode != 0 else "SURVIVED"
    d = (r.stderr.strip().splitlines() or ["<none>"])[-1][:150]
    print("%-42s %-9s exit=%d  %s" % (name, st, r.returncode, d))

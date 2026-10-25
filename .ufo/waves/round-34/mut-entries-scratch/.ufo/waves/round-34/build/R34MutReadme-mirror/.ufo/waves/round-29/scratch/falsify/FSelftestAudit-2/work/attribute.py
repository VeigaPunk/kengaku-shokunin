#!/usr/bin/env python3
"""For each mutant, capture the traceback line number in config_projection.py that failed,
so each kill is attributed to a specific selftest assertion (and hence a named case)."""
import subprocess, sys, re, json
from pathlib import Path

SRC = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py")
LANE_ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
WORK = Path("/tmp/r29-selftest-audit/attrib"); WORK.mkdir(parents=True, exist_ok=True)

M = {
 "order_reversed": ('ORDER = ("GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP")',
   'ORDER = ("MAP", "WIKIPEDIA", "SHOPPING_ADMIN", "SHOPPING", "REDDIT", "GITLAB")'),
 "url_templates_only_start_url": ('URL_FIELD_TEMPLATES = frozenset({"start_url", "eval.reference_url", "eval.program_html[].url"})',
   'URL_FIELD_TEMPLATES = frozenset({"start_url"})'),
 "byte_offset_instead_codepoint": ('"original_input_codepoint_offset": at,',
   '"original_input_codepoint_offset": len(raw_text[:at].encode()),'),
 "drop_known_token_remaining": ('        if any(record["remaining_known_tokens_text"].values()) or any(record["remaining_known_tokens_decoded"].values()):\n            findings.append({"id": "known_token_remaining", "profile": name})',
   '        if False:\n            findings.append({"id": "known_token_remaining", "profile": name})'),
 "no_manifest_sha_pin": ('    if hashlib.sha256(manifest_bytes).hexdigest() != MANIFEST_SHA256:\n        raise Unevaluable("manifest_tampered")',
   '    if False:\n        raise Unevaluable("manifest_tampered")'),
 "drop_source_order_check": ('    if [(s["token"], s["name"]) for s in steps] != [("__%s__" % name, name) for name in ORDER]:',
   '    if False:'),
 "output_filename_task_id": ('"output_index": i, "output_filename": "config_files/%d.json" % i,',
   '"output_index": i, "output_filename": "config_files/%d.json" % (task.get("task_id") if isinstance(task, dict) else i),'),
 "reread_raw": ('    raw_text = verified[RAW].decode("utf-8")', '    raw_text = (root / RAW).read_bytes().decode("utf-8")'),
 "reread_generator": ('    contract = source_contract(verified[GENERATOR])', '    contract = source_contract((root / GENERATOR).read_bytes().decode("utf-8"))'),
 "reread_profiles": ('    profiles = json.loads(verified[PROFILES])', '    profiles = json.loads((root / PROFILES).read_bytes())'),
 "drop_structure_changed": ('            findings.append({"id": "projection_structure_changed", "profile": name, "paths": problems[:20], "count": len(problems)})',
   '            pass'),
 "drop_token_outside_string": ('        findings.append({"id": "token_outside_string_value", "roles": population["occurrence_roles"]})', '        pass'),
 "index_equals_always_true": ('"index_equals_task_id": isinstance(task, dict) and task.get("task_id") == i,', '"index_equals_task_id": True,'),
 "multi_occurrence_zero": ('"changed_leaves_with_multiple_occurrences": sum(1 for path, before, _ in changed if sum(before.count(t) for t in tokens) > 1),',
   '"changed_leaves_with_multiple_occurrences": 0,'),
 "other_markers_zero": ('"other_double_underscore_markers": dict(sorted(markers.items())),', '"other_double_underscore_markers": {},'),
 "occurrence_roles_always_value": ('"occurrence_roles": dict(collections.Counter(record["string_role"] for record in occurrences)),', '"occurrence_roles": {"value": len(occurrences)},'),
 "changed_task_count_leaf": ('"changed_leaf_count": len(changed), "changed_task_count": len(by_task),', '"changed_leaf_count": len(changed), "changed_task_count": len(changed),'),
 "drop_source_filename_check": ("    if parse_line is None or filename != [\"f'config_files/{idx}.json'\"]:\n        raise Unevaluable(\"source_contract_unrecognized\", detail=\"parse or enumerate-index output contract missing\")",
   '    if parse_line is None:\n        raise Unevaluable("source_contract_unrecognized", detail="parse or enumerate-index output contract missing")'),
 "check_values_extra_allowed": ('    if set(values) - set(ORDER):\n        raise Unevaluable("profile_unexpected_key", profile=name, keys=sorted(set(values) - set(ORDER)))',
   '    if False:\n        raise Unevaluable("profile_unexpected_key", profile=name, keys=sorted(set(values) - set(ORDER)))'),
 "input_missing_renamed": ('            raise Unevaluable("input_missing", path=relative)', '            raise Unevaluable("snapshot_tampered", path=relative)'),
 "provenance_offset_plus1": ('"original_input_codepoint_offset": at,', '"original_input_codepoint_offset": at + 1,'),
 "string_role_inverted": ('                spans.append((i, end, path, "key", key))', '                spans.append((i, end, path, "value", key))'),
}

# map assertion line -> case name (from reading the source)
CASES = {}
src_lines = SRC.read_text().splitlines()
# find cases.append lines and the nearest preceding cases.append gives the case of the assertions before it
appends = [(i+1, l) for i, l in enumerate(src_lines) if "cases.append" in l]

def case_for_line(n):
    best = None
    for ln, txt in appends:
        if ln <= n:
            best = (ln, txt.strip())
    return best

for name, (old, new) in M.items():
    t = SRC.read_text()
    if old not in t:
        print("%-34s PATCH-FAILED" % name); continue
    p = WORK / ("m_%s.py" % name)
    p.write_text(t.replace(old, new, 1))
    r = subprocess.run([sys.executable, str(p), "--selftest", "--root", LANE_ROOT], capture_output=True, text=True, timeout=600)
    if r.returncode == 0:
        print("%-34s SURVIVED" % name); continue
    m = re.search(r'File "([^"]+)", line (\d+), in (\S+)', r.stderr)
    if not m:
        print("%-34s KILLED (no tb) %s" % (name, r.stderr.strip().splitlines()[-1][:80])); continue
    f, ln = m.group(1), int(m.group(2))
    if f.endswith("m_%s.py" % name):
        c = case_for_line(ln)
        print("%-34s KILLED at %s:%d  fn=%s  -> %s" % (name, f.split('/')[-1], ln, m.group(3), c[1] if c else "?"))
    else:
        print("%-34s KILLED at %s:%d fn=%s" % (name, f, ln, m.group(3)))

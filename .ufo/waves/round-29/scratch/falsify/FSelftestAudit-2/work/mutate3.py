#!/usr/bin/env python3
"""Battery 3: probe which asserted-vs-unasserted behaviours the selftest actually pins."""
import subprocess, sys, os
from pathlib import Path

SRC = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py")
LANE_ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
WORK = Path("/tmp/r29-selftest-audit/mut3"); WORK.mkdir(parents=True, exist_ok=True)

M = {
 "M28_changed_leaves_by_token_occurrence_based": (
   '"changed_leaves_by_token": {token: sum(1 for leaf in leaves_flat if token in leaf["tokens"]) for token in tokens},',
   '"changed_leaves_by_token": {token: sum(1 for leaf in leaves_flat for _ in range(leaf["tokens"].count(token))) for token in tokens},'),
 "M29_changed_task_count_leaf_based": (
   '"changed_leaf_count": len(changed), "changed_task_count": len(by_task),',
   '"changed_leaf_count": len(changed), "changed_task_count": len(changed),'),
 "M30_occurrence_roles_always_value": (
   '"occurrence_roles": dict(collections.Counter(record["string_role"] for record in occurrences)),',
   '"occurrence_roles": {"value": len(occurrences)},'),
 "M31_manifest_contract_check_removed": (
   '    if sorted(manifest["files"]) != sorted([GENERATOR, RAW, PROFILES]) or tuple(manifest["replacement_order"]) != ORDER:\n        raise Unevaluable("manifest_contract_mismatch")',
   '    if False:\n        raise Unevaluable("manifest_contract_mismatch")'),
 "M32_projected_text_sha_wrong": (
   '"projected_text_sha256": hashlib.sha256(projected_text.encode("utf-8")).hexdigest(),',
   '"projected_text_sha256": "0" * 64,'),
 "M33_would_be_file_sha_wrong": (
   '"would_be_file_sha256": hashlib.sha256(json.dumps(task, indent=2).encode("utf-8")).hexdigest(),',
   '"would_be_file_sha256": "0" * 64,'),
 "M34_other_markers_census_zero": (
   '"other_double_underscore_markers": dict(sorted(markers.items())),',
   '"other_double_underscore_markers": {},'),
 "M35_profile_purpose_not_required": (
   '        if not isinstance(values, dict) or not isinstance(profile.get("purpose"), str):\n            raise Unevaluable("profile_invalid_type", profile=name)',
   '        if not isinstance(values, dict):\n            raise Unevaluable("profile_invalid_type", profile=name)'),
 "M36_check_values_extra_key_allowed": (
   '    if set(values) - set(ORDER):\n        raise Unevaluable("profile_unexpected_key", profile=name, keys=sorted(set(values) - set(ORDER)))',
   '    if False:\n        raise Unevaluable("profile_unexpected_key", profile=name, keys=sorted(set(values) - set(ORDER)))'),
 "M37_stimulus_class_dropped": (
   '"stimulus_class": STIMULUS.get(name),',
   '"stimulus_class": None,'),
 "M38_population_profile_count_wrong": (
   '"profile_count": len(results),',
   '"profile_count": 0,'),
 "M39_source_contract_filename_check_removed": (
   '    if parse_line is None or filename != ["f\'config_files/{idx}.json\'"]:\n        raise Unevaluable("source_contract_unrecognized", detail="parse or enumerate-index output contract missing")',
   '    if parse_line is None:\n        raise Unevaluable("source_contract_unrecognized", detail="parse or enumerate-index output contract missing")'),
 "M40_upstream_revision_hardcoded": (
   'result.update(inputs={path: pin["sha256"] for path, pin in manifest["files"].items()}, manifest_sha256=MANIFEST_SHA256,\n                  upstream_revision=manifest["upstream_revision"],',
   'result.update(inputs={path: pin["sha256"] for path, pin in manifest["files"].items()}, manifest_sha256=MANIFEST_SHA256,\n                  upstream_revision="deadbeef",'),
}

def run(p):
    return subprocess.run([sys.executable, str(p), "--selftest", "--root", LANE_ROOT],
                          capture_output=True, text=True, timeout=600)

for name, (old, new) in M.items():
    t = SRC.read_text()
    if old not in t:
        print("%-52s PATCH-FAILED" % name); continue
    p = WORK / ("mut_%s.py" % name)
    p.write_text(t.replace(old, new, 1))
    r = run(p)
    st = "KILLED" if r.returncode != 0 else "SURVIVED"
    d = (r.stderr.strip().splitlines() or ["<none>"])[-1][:120]
    print("%-52s %-9s exit=%d  %s" % (name, st, r.returncode, d))

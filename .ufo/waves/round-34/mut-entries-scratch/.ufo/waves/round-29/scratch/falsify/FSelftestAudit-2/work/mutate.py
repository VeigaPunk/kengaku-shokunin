#!/usr/bin/env python3
"""Mutation battery: apply a textual mutation to a copy of the instrument, run --selftest, record kill/survive."""
import shutil, subprocess, sys, os, hashlib
from pathlib import Path

SRC = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py")
LANE_ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
WORK = Path("/tmp/r29-selftest-audit/mut")
WORK.mkdir(parents=True, exist_ok=True)

MUTANTS = {
    # (name, old, new)
    "M01_url_templates_drop_eval_templates": (
        'URL_FIELD_TEMPLATES = frozenset({"start_url", "eval.reference_url", "eval.program_html[].url"})',
        'URL_FIELD_TEMPLATES = frozenset({"start_url"})'),
    "M02_url_templates_drop_program_html": (
        'URL_FIELD_TEMPLATES = frozenset({"start_url", "eval.reference_url", "eval.program_html[].url"})',
        'URL_FIELD_TEMPLATES = frozenset({"start_url", "eval.reference_url"})'),
    "M03_order_reversed": (
        'ORDER = ("GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP")',
        'ORDER = ("MAP", "WIKIPEDIA", "SHOPPING_ADMIN", "SHOPPING", "REDDIT", "GITLAB")'),
    "M04_provenance_byte_offset": (
        '"original_input_codepoint_offset": at,',
        '"original_input_codepoint_offset": len(raw_text[:at].encode()),'),
    "M05_drop_known_token_remaining_finding": (
        '        if any(record["remaining_known_tokens_text"].values()) or any(record["remaining_known_tokens_decoded"].values()):\n            findings.append({"id": "known_token_remaining", "profile": name})',
        '        if False:\n            findings.append({"id": "known_token_remaining", "profile": name})'),
    "M06_check_values_no_missing_key": (
        '    for key in ORDER:\n        if key not in values:\n            raise Unevaluable("profile_missing_key", profile=name, key=key)',
        '    for key in ORDER:\n        if False:\n            raise Unevaluable("profile_missing_key", profile=name, key=key)'),
    "M07_no_manifest_sha_pin": (
        '    if hashlib.sha256(manifest_bytes).hexdigest() != MANIFEST_SHA256:\n        raise Unevaluable("manifest_tampered")',
        '    if False:\n        raise Unevaluable("manifest_tampered")'),
    "M08_drop_profile_missing_finding": (
        '    if missing or extra:\n        raise Unevaluable("profile_missing" if missing else "profile_unexpected", profiles=missing or extra)',
        '    if False:\n        raise Unevaluable("profile_missing" if missing else "profile_unexpected", profiles=missing or extra)'),
    "M09_drop_source_contract_order_check": (
        '    if [(s["token"], s["name"]) for s in steps] != [("__%s__" % name, name) for name in ORDER]:',
        '    if False:'),
    "M10_output_filename_from_task_id": (
        '"output_index": i, "output_filename": "config_files/%d.json" % i,',
        '"output_index": i, "output_filename": "config_files/%d.json" % (task.get("task_id") if isinstance(task, dict) else i),'),
    "M11_escaped_token_text_census_decoded": (
        '"remaining_known_tokens_text": {token: projected_text.count(token) for token in tokens}',
        '"remaining_known_tokens_text": {token: 0 for token in tokens}'),
    "M12_drop_url_only_finding": (
        '        if unexplained or (not problems and carriers != len(changed)):',
        '        if False:'),
}

def run(path, extra_env=None):
    env = dict(os.environ)
    if extra_env:
        env.update(extra_env)
    p = subprocess.run([sys.executable, str(path), "--selftest", "--root", LANE_ROOT],
                       capture_output=True, text=True, env=env, timeout=600)
    return p

base = WORK / "base.py"
shutil.copyfile(SRC, base)
b = run(base)
print("BASELINE exit=%d" % b.returncode)
print("BASELINE stdout:", b.stdout.strip()[:200])
print("BASELINE stderr:", b.stderr.strip()[:400])
print("=" * 70)

results = []
for name, (old, new) in MUTANTS.items():
    text = SRC.read_text()
    if old not in text:
        results.append((name, "PATCH-FAILED", "old string not found"))
        print("%-45s PATCH-FAILED" % name)
        continue
    mutated = text.replace(old, new, 1)
    p = WORK / ("mut_%s.py" % name)
    p.write_text(mutated)
    r = run(p)
    status = "KILLED" if r.returncode != 0 else "SURVIVED"
    detail = (r.stderr.strip().splitlines() or ["<no stderr>"])[-1][:160]
    results.append((name, status, detail))
    print("%-45s %-9s exit=%d  %s" % (name, status, r.returncode, detail))
    # also run under -O to check assert-stripping behaviour
    rO = run(p, {"PYTHONOPTIMIZE": "1"})
    print("%-45s   under -O: exit=%d stdout=%s" % (name, rO.returncode, (rO.stdout.strip()[:40] or "<empty>")))
print("=" * 70)
for n, s, d in results:
    print("%-45s %s" % (n, s))

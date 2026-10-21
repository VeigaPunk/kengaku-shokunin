#!/usr/bin/env python3
"""Mutate-run-revert witness for plans/config_projection.py; every mutant runs on a /tmp copy.

Each mutant is one exact source replacement persisted below. A kill is a nonzero --selftest exit;
the frozen-data column records whether --summary alone would notice (findings or exit != control).
The lane is never written; output is one JSON receipt on stdout.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
TOOL = "plans/config_projection.py"
COPY = [TOOL, "plans/fixtures/r29/manifest.json", "plans/fixtures/r29/generate_test_data.py", "plans/fixtures/r29/profiles.json",
        "plans/fixtures/r28/webarena/config_files/test.raw.json", "plans/fixtures/r29/hand"]
MUTANTS = {
    "wrong_order_reversed": ('    for name in ORDER:\n        token = "__%s__" % name\n        steps.append', '    for name in reversed(ORDER):\n        token = "__%s__" % name\n        steps.append'),
    "url_only_substitution": ("        text = text.replace(token, values[name])\n    return text, steps",
                              "        text = re.sub(r'(\"(?:start_url|reference_url|url)\": \")' + re.escape(token), lambda m: m.group(1) + values[name], text)\n    return text, steps"),
    "index_by_task_id": ('"output_filename": "config_files/%d.json" % i,', '"output_filename": "config_files/%d.json" % task.get("task_id", i),'),
    "value_normalized_rstrip": ("text = text.replace(token, values[name])", 'text = text.replace(token, values[name].rstrip("/"))'),
    "category_by_value_shape": ('"category": "url_field" if template(path) in URL_FIELD_TEMPLATES else "non_url_field",', '"category": "url_field" if after.startswith(("http://", "https://")) else "non_url_field",'),
    "hash_then_reread": ("        verified[relative] = data", "        verified[relative] = (root / relative).read_bytes()"),
    "decoded_census_drops_wikipedia": ("for text in decoded) for token in tokens}", 'for text in decoded) for token in tokens if token != "__WIKIPEDIA__"}'),
    "runtime_marker_counted_as_token": ('"remaining_known_tokens_text": {token: projected_text.count(token) for token in tokens}}', '"remaining_known_tokens_text": {token: projected_text.count(token) for token in tokens + ["__last_url__"]}}'),
    "exact_contract_check_removed": ("    if rendered != EXPECTED_STATEMENTS:", "    if False:"),
    "unexpected_error_not_caught": ("        except Exception as error:", "        except (OSError, ValueError) as error:"),
}


def run(root, mode):
    output = subprocess.run([sys.executable, str(root / TOOL), "--root", str(root), mode], capture_output=True, text=True)
    return output.returncode, (output.stdout.strip().splitlines() or [""])[-1], (output.stderr.strip().splitlines() or [""])[-1][:200]


def main():
    source = (ROOT / TOOL).read_text(encoding="utf-8")
    receipt = {"tool_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(), "mutants": {}}
    with tempfile.TemporaryDirectory(prefix="kengaku-r29-witness-", dir="/tmp") as temp:
        scratch = Path(temp)
        for relative in COPY:
            target = scratch / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            (shutil.copytree if (ROOT / relative).is_dir() else shutil.copyfile)(ROOT / relative, target)
        receipt["control"] = {"selftest": run(scratch, "--selftest")[:2], "summary": run(scratch, "--summary")[:2]}
        for name, (old, new) in MUTANTS.items():
            assert source.count(old) == 1, name
            (scratch / TOOL).write_text(source.replace(old, new), encoding="utf-8")
            selftest, summary = run(scratch, "--selftest"), run(scratch, "--summary")
            receipt["mutants"][name] = {"old": old, "new": new, "selftest_exit": selftest[0], "selftest_last_stderr": selftest[2],
                                        "summary_exit": summary[0], "summary_total": summary[1], "killed": selftest[0] != 0,
                                        "frozen_summary_alone_detects": summary[1] != receipt["control"]["summary"][1]}
            (scratch / TOOL).write_text(source, encoding="utf-8")
        receipt["restored_sha256"] = hashlib.sha256((scratch / TOOL).read_bytes()).hexdigest()
    receipt["killed"] = sum(m["killed"] for m in receipt["mutants"].values())
    print(json.dumps(receipt, indent=1))
    return 0 if receipt["killed"] == len(MUTANTS) and receipt["control"]["selftest"][0] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

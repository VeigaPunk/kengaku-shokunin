#!/usr/bin/env python3
"""L1-authored alternate census; independent logic, NOT independent authorship.

The build oracle seat died before writing. This module never imports the audit.
Fresh falsify seats must independently replay the actual metrics.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    source = args.root / "plans/fixtures/r28/webarena/config_files/test.raw.json"
    raw = source.read_bytes()
    tasks = json.loads(raw)
    groups = defaultdict(list)
    for task in tasks:
        groups[(tuple(sorted(task["sites"])), tuple(sorted(task["eval"]["eval_types"])))].append(task["task_id"])
    selected = [min(values) for _, values in sorted(groups.items())][:16]
    histograms = {}
    histograms["eval_type_sets"] = Counter(",".join(sorted(task["eval"]["eval_types"])) for task in tasks)
    histograms["eval_type_orders"] = Counter(",".join(task["eval"]["eval_types"]) for task in tasks)
    histograms["site_sets"] = Counter(",".join(sorted(task["sites"])) for task in tasks)
    histograms["login_flags"] = Counter(str(task["require_login"]).lower() for task in tasks)
    histograms["reset_flags"] = Counter(str(task["require_reset"]).lower() for task in tasks)
    histograms["string_operators"] = Counter(operator for task in tasks if "string_match" in task["eval"]["eval_types"] for operator in task["eval"]["reference_answers"])
    histograms["url_rules"] = Counter(task["eval"].get("url_note", "GOLD in PRED") for task in tasks if "url_match" in task["eval"]["eval_types"])
    histograms["url_note_origin"] = Counter("explicit" if "url_note" in task["eval"] else "defaulted" for task in tasks if "url_match" in task["eval"]["eval_types"])
    targets = [target for task in tasks if "program_html" in task["eval"]["eval_types"] for target in task["eval"]["program_html"]]
    histograms["html_operators"] = Counter("exact_match" if "exact_match" in target["required_contents"] else "must_include" for target in targets)
    histograms["locator_classes"] = Counter("full_page" if not target["locator"].strip() else "javascript" if target["locator"].startswith(("document.", "[...document.")) else "helper" if target["locator"].startswith("func:") else "unsupported" for target in targets)
    histograms["target_url_classes"] = Counter("last" if target["url"] == "last" else "helper" if target["url"].startswith("func") else "navigation" for target in targets)
    metrics = {"task_count": len(tasks), "distinct_task_ids": len({task["task_id"] for task in tasks}), "site_eval_strata": len(groups), "selected_count": len(selected), "program_html_targets": len(targets), **histograms}
    print(json.dumps({"writer": "KengakuR28", "authority": "alternate implementation, not author-independent", "source_sha256": hashlib.sha256(raw).hexdigest(), "metrics": metrics, "selected_task_ids": selected}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

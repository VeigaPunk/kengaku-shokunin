#!/usr/bin/env python3
"""Read-only round28 counters. Revision label is caller-supplied, not inferred HEAD."""
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import re
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--revision", required=True, help="measured tree revision; caller must export or prove byte equality")
    args = parser.parse_args()
    root = args.root.resolve()
    output = {"measurement_root": str(root), "revision_label": args.revision, "revision_authority": "caller-supplied; see export/byte-equality receipt"}
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    def run(relative, *flags):
        code = root / relative
        if not code.is_file():
            return {"exit": None, "absent": True}
        result = subprocess.run([sys.executable, str(code), "--root", str(root), *flags], cwd=root, env=env, capture_output=True, text=True)
        try:
            parsed = json.loads(result.stdout)
        except ValueError:
            parsed = {"stdout": result.stdout, "stderr": result.stderr}
        return {"exit": result.returncode, "result": parsed}
    c1 = run("plans/benchmark_spec_audit.py", "--json")
    output["c1"] = {"exit": c1["exit"], "metrics": c1.get("result", {}).get("metrics"), "findings": c1.get("result", {}).get("findings"), "selected_task_ids": c1.get("result", {}).get("selected_task_ids")}
    c2 = run("plans/registry_check.py", "--json")
    output["c2"] = {"exit": c2["exit"], **{key: c2.get("result", {}).get(key) for key in ("source_rows_checked", "knowledge_files_expected", "reference_links", "mismatch_sources", "finding_count", "findings")}}
    state = run("plans/state_check.py", "--json")
    assertions = state.get("result", {}).get("assertions", [])
    p4 = [value for value in assertions if re.match(r"^P4(?:[a-e])?(?:\.|$)", value.get("id", ""))]
    output["historical_state"] = {"exit": state["exit"], "summary": state.get("result", {}).get("summary"), "total_json_records": len(assertions), "verdicts": dict(Counter(value["verdict"] for value in assertions)), "p4_ids": len(p4), "p4_verdicts": dict(Counter(value["verdict"] for value in p4))}
    source = root / "corpus/SOURCES.md"
    rows = [[cell.strip() for cell in line.split("|")[1:-1]] for line in source.read_text().splitlines() if re.match(r"^\|\s*S[0-9]{3,}\s*\|", line)]
    output["sources"] = {"rows": len(rows), "malformed": sum(len(row) != 11 for row in rows), "tiers": dict(Counter(row[3] for row in rows if len(row) == 11)), "statuses": dict(Counter(row[7] for row in rows if len(row) == 11))}
    actual = {"knowledge/" + path.name for path in (root / "corpus/knowledge").glob("*.md")}
    index = re.findall(r"^\|\s*`(knowledge/[^`|]+\.md)`\s*\|", (root / "corpus/README.md").read_text(), re.M)
    output["knowledge"] = {"files": len(actual), "index_rows": len(index), "unindexed": sorted(actual - set(index)), "dangling": sorted(set(index) - actual), "duplicate_rows": sorted(path for path, count in Counter(index).items() if count > 1)}
    print(json.dumps(output, indent=2, sort_keys=True))
    clean = c1["exit"] == 0 and c2["exit"] == 0 and state["exit"] == 0 and not output["sources"]["malformed"] and not any(output["knowledge"][key] for key in ("unindexed", "dangling", "duplicate_rows"))
    return 0 if clean else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Round28 author acceptance: baseline/only-delta/revert and preserved-state evidence.

Runs only lane-owned Python tools. Upstream benchmark files stay inert data.
All fixture writes use a temporary baseline export; no lane VCS mutation.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

BASE = "b9b24796277020d1b9b01923b45313d6a565e664"


ENTRY = "corpus/knowledge/webarena-task-spec-audit.md"
EXPECTED_ENTRY_SOURCES = {"S005", "S006", "S061", "S062", "S063", "S068", "S069"}


def entry_source_links(source_text, entry_text):
    """Separate admission fixture; not part of C2's frozen13-row measurement."""
    cited = set(re.findall(r"(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])", entry_text))
    rows = {}
    for line in source_text.splitlines():
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) == 11 and cells[0] in cited:
            rows[cells[0]] = cells
    findings = []
    for sid in sorted(cited):
        if sid not in rows:
            findings.append({"id": "admission_source_missing", "source": sid})
        elif rows[sid][7] != "mined":
            findings.append({"id": "admission_source_not_mined", "source": sid})
        elif ENTRY not in [path.strip() for path in rows[sid][10].split(",")]:
            findings.append({"id": "admission_used_by_missing", "source": sid})
    return {"sources": sorted(cited), "findings": findings, "exit": int(bool(findings))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    root, out = args.root.resolve(), args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    records = []
    def run(name, script, *flags, expected=0):
        command = [sys.executable, str(root / script), *map(str, flags)]
        result = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True)
        (out / (name + ".stdout")).write_text(result.stdout)
        (out / (name + ".stderr")).write_text(result.stderr)
        records.append({"name": name, "command": command, "exit": result.returncode, "expected_exit": expected})
        (out / "commands.json").write_text(json.dumps(records, indent=2) + "\n")
        assert result.returncode == expected, (name, result.returncode, result.stdout, result.stderr)
        return json.loads(result.stdout) if "--json" in flags or script.endswith("oracle.py") else result.stdout
    audit = "plans/benchmark_spec_audit.py"
    registry = "plans/registry_check.py"
    run("audit-selftest", audit, "--selftest")
    run("registry-selftest", registry, "--selftest")
    current_c1 = run("audit-current", audit, "--root", root, "--json")
    current_c2 = run("registry-current", registry, "--root", root, "--json")
    witness = run("audit-alternate", "plans/fixtures/r28/benchmark_oracle.py", "--root", root)
    assert current_c1["metrics"] == witness["metrics"]
    assert current_c1["selected_task_ids"] == witness["selected_task_ids"]
    witness_c2 = run("registry-alternate", "plans/fixtures/r28/registry_oracle.py", "--root", root)
    assert current_c2["reference_links"] == witness_c2["reference_links"]
    for item in current_c2["sources"]:
        other = witness_c2["sources"][item["source"]]
        assert all(item[key] == other[key] for key in ("status", "citing_files", "used_by", "missing_used_by"))
    # Freeze an export from the declared lane branch revision, never a guessed HEAD.
    git_env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    archive = subprocess.run(["git", "-C", str(root), "archive", BASE], env=git_env, capture_output=True, check=True).stdout
    with tempfile.TemporaryDirectory(prefix="kengaku-r28-baseline-") as temporary:
        base = Path(temporary)
        with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
            bundle.extractall(base, filter="data")
        population = Path("plans/fixtures/r28/registry/population.json")
        (base / population).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / population, base / population)
        before = run("registry-baseline-red", registry, "--root", base, "--json", expected=1)
        assert {finding["source"] for finding in before["findings"] if "source" in finding} == {"S038", "S050"}
        original = (base / "corpus/SOURCES.md").read_text()
        current_rows = {line.split("|")[1].strip(): line for line in (root / "corpus/SOURCES.md").read_text().splitlines() if line.startswith("| S")}
        base_rows = {line.split("|")[1].strip(): line for line in original.splitlines() if line.startswith("| S")}
        for sid in ("S038", "S050"):
            old = [cell.strip() for cell in base_rows[sid].split("|")[1:-1]]
            new = [cell.strip() for cell in current_rows[sid].split("|")[1:-1]]
            assert all(a == b for index, (a, b) in enumerate(zip(old, new)) if index not in (7, 9, 10)), sid
        after_s050 = original.replace(base_rows["S050"], current_rows["S050"])
        (base / "corpus/SOURCES.md").write_text(after_s050)
        red = run("registry-s050-only-red", registry, "--root", base, "--json", expected=1)
        assert {finding["source"] for finding in red["findings"] if "source" in finding} == {"S038"}
        after_both = after_s050.replace(base_rows["S038"], current_rows["S038"])
        (base / "corpus/SOURCES.md").write_text(after_both)
        green = run("registry-s038-only-delta-green", registry, "--root", base, "--json")
        assert green["finding_count"] == 0
        assert current_c2["reference_links"] == green["reference_links"]
        (out / "registry-only-delta.json").write_text(json.dumps({"base": BASE, "population_sha256": hashlib.sha256((root / population).read_bytes()).hexdigest(), "original_sources_sha256": hashlib.sha256(original.encode()).hexdigest(), "s050_only_sources_sha256": hashlib.sha256(after_s050.encode()).hexdigest(), "both_sources_sha256": hashlib.sha256(after_both.encode()).hexdigest(), "delta_from_red_to_green": {"source": "S038", "allowed_cells": ["status", "used-by"], "all_other_baseline_bytes_unchanged": True}, "before_mismatch_sources": before["mismatch_sources"], "after_s050_mismatch_sources": red["mismatch_sources"], "after_both_mismatch_sources": green["mismatch_sources"]}, indent=2) + "\n")
        # C2 with all C1 additions absent (no new rows, new entry, or benchmark files).
        assert len(green["sources"]) == 13
        projection = lambda result: [(item["source"], item["status"], item["citing_files"], item["missing_used_by"]) for item in result["sources"]]
        assert projection(green) == projection(current_c2)
        # C1 with C2 corrections absent: baseline knowledge and original registry.
        (base / "corpus/SOURCES.md").write_text(original)
        shutil.copytree(root / "plans/fixtures/r28/webarena", base / "plans/fixtures/r28/webarena")
        c1_without_c2 = run("audit-without-c2", audit, "--root", base, "--json")
        assert c1_without_c2["metrics"] == current_c1["metrics"]
        assert c1_without_c2["selected_task_ids"] == current_c1["selected_task_ids"]
    # Prospective C1 admission must not repeat the new-source used-by gap. The
    # deliberate red state removes only that canonical link; its repair adds it.
    draft = (root / ".ufo/waves/round-28/drafts/webarena-task-spec-audit.md").read_text()
    source_text = (root / "corpus/SOURCES.md").read_text()
    assert set(re.findall(r"(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])", draft)) == EXPECTED_ENTRY_SOURCES
    red_lines, green_lines = [], []
    for line in source_text.splitlines():
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) == 11 and cells[0] in EXPECTED_ENTRY_SOURCES:
            used = [path.strip() for path in cells[10].split(",") if path.strip() not in ("", "—", ENTRY)]
            cells[10] = ", ".join(used)
            red_lines.append("| " + " | ".join(cells) + " |")
            cells[10] = ", ".join(used + [ENTRY])
            green_lines.append("| " + " | ".join(cells) + " |")
        else:
            red_lines.append(line)
            green_lines.append(line)
    red_links = entry_source_links("\n".join(red_lines), draft)
    green_links = entry_source_links("\n".join(green_lines), draft)
    assert red_links["exit"] == 1 and {value["source"] for value in red_links["findings"]} == EXPECTED_ENTRY_SOURCES
    assert green_links["exit"] == 0
    actual_admission = (root / ENTRY).is_file()
    actual_links = entry_source_links(source_text, (root / ENTRY).read_text()) if actual_admission else None
    if actual_admission:
        assert actual_links["exit"] == 0
    (out / "admission-source-links.json").write_text(json.dumps({"red": red_links, "green": green_links, "actual_admission_present": actual_admission, "actual": actual_links, "not_counted_in_c2": True}, indent=2) + "\n")
    state = run("historical-state-current", "plans/state_check.py", "--root", root, "--json")
    previous = json.loads((root / "corpus/evidence/round27-calibration/state-final-json.json").read_text())
    def keyed(result):
        return {item["id"]: item["verdict"] for item in result["assertions"]}
    old_keys, new_keys = keyed(previous), keyed(state)
    assert all(new_keys.get(key) == verdict for key, verdict in old_keys.items()), "historical per-ID verdict changed"
    new_disclosures = {key: value for key, value in new_keys.items() if key not in old_keys}
    assert all(value == "OUT_OF_POPULATION" for value in new_disclosures.values()), "new checked population"
    assert {key: value for key, value in state["summary"].items() if key != "out_of_population"} == {key: value for key, value in previous["summary"].items() if key != "out_of_population"}
    assert state["summary"]["out_of_population"] == previous["summary"]["out_of_population"] + len(new_disclosures)
    protected = ["plans/state_check.py"]
    for relative in protected:
        old = subprocess.run(["git", "-C", str(root), "show", BASE + ":" + relative], env=git_env, capture_output=True, check=True).stdout
        assert old == (root / relative).read_bytes(), relative
    result = {"base_revision": BASE, "checks": len(records), "failed": 0, "c1_metrics_equal_alternate": True, "c2_projection_equal_alternate": True, "two_way_revert_counters_equal": True, "historical_existing_keyed_verdict_projection_unchanged": True, "new_out_of_population_disclosures": new_disclosures, "historical_summary": state["summary"], "instrument_sha256": {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in (audit, registry, "plans/state_check.py")}}
    (out / "acceptance.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

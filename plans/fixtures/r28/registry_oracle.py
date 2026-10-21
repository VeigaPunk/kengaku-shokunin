#!/usr/bin/env python3
"""L1 alternate derivation, not author-independent; does not import checker logic."""
import argparse
import json
from pathlib import Path
import re


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    pop = json.loads((args.root / "plans/fixtures/r28/registry/population.json").read_text())
    table = (args.root / "corpus/SOURCES.md").read_text().split("## Registry\n", 1)[1].split("\n## ", 1)[0]
    rows = {}
    duplicates = []
    for line in table.splitlines():
        cells = [value.strip() for value in line.split("|")]
        if len(cells) == 13 and re.fullmatch(r"S[0-9]{3,}", cells[1]):
            if cells[1] in rows:
                duplicates.append(cells[1])
            rows[cells[1]] = cells
    result = {}
    missing_files = []
    for sid in pop["source_ids"]:
        citing = []
        for name in pop["knowledge_paths"]:
            path = args.root / name
            if not path.is_file():
                missing_files.append(name)
                continue
            if sid in re.findall(pop["reference_pattern"], path.read_text()):
                citing.append(name)
        row = rows.get(sid)
        used = [] if not row or row[11] in ("", "—") else [value.strip().strip("`") for value in re.split(r"[,;]", row[11])]
        result[sid] = {"status": row[8] if row else None, "citing_files": sorted(citing), "used_by": sorted(used), "missing_used_by": sorted(set(citing) - set(used)), "status_mismatch": bool(citing) and (not row or row[8] != "mined")}
    mismatches = [sid for sid, value in result.items() if value["status_mismatch"] or value["missing_used_by"] or sid not in rows]
    print(json.dumps({"writer": "KengakuR28", "authority": "alternate logic, not author-independent", "source_rows_checked": len(result), "knowledge_files_expected": len(pop["knowledge_paths"]), "reference_links": sum(len(value["citing_files"]) for value in result.values()), "mismatch_sources": mismatches, "duplicate_ids": duplicates, "missing_files": sorted(set(missing_files)), "sources": result}, indent=2, sort_keys=True))
    return int(bool(mismatches or duplicates or missing_files))


if __name__ == "__main__":
    raise SystemExit(main())

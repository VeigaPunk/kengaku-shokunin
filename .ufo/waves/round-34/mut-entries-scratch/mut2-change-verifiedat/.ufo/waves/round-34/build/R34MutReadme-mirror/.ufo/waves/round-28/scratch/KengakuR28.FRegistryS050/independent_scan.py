#!/usr/bin/env python3
"""Independent re-derivation of registry_check semantics for S050 falsification.
Written from the frozen population contract; does NOT import plans/registry_check.py.
Read-only over production."""
import json, re, sys
from pathlib import Path

ROOT = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
POP = json.loads((ROOT / "plans/fixtures/r28/registry/population.json").read_text())
REF = re.compile(r"(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])")
SRC_ID = re.compile(r"S[0-9]{3,}\Z")
KINDS = {"spec", "docs", "paper", "code", "tool", "dataset", "talk", "book", "community", "own-work"}


def parse_registry(text):
    rows, findings, active, fenced = {}, [], False, False
    for number, line in enumerate(text.splitlines(), 1):
        if line.startswith("```") or line.startswith("~~~"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if line.startswith("## "):
            active = line.strip() == "## Registry"
        if not active or not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if not cells or not SRC_ID.fullmatch(cells[0]):
            continue
        if len(cells) != 11:
            findings.append({"id": "malformed_source_row", "source": cells[0], "line": number})
            continue
        if cells[0] in rows:
            findings.append({"id": "duplicate_source_id", "source": cells[0], "line": number})
            continue
        rows[cells[0]] = dict(zip(("id", "source", "kind", "tier", "scope", "anchor", "teaches", "status", "opened", "recheck", "used_by"), cells))
    return rows, findings


def check(root, population):
    rows, findings = parse_registry((root / "corpus/SOURCES.md").read_text())
    refs = {sid: set() for sid in population["source_ids"]}
    for relative in population["knowledge_paths"]:
        path = root / relative
        if not path.is_file():
            findings.append({"id": "knowledge_missing", "path": relative})
            continue
        for sid in set(REF.findall(path.read_text())) & refs.keys():
            refs[sid].add(relative)
    results = []
    for sid, citing in refs.items():
        row = rows.get(sid)
        if row is None:
            findings.append({"id": "source_missing", "source": sid})
            results.append({"source": sid, "status": None, "citing": sorted(citing), "used_by": [], "missing": sorted(citing)})
            continue
        used_by = [] if row["used_by"] in ("", "—") else [p.strip().strip("`") for p in re.split(r"[,;]", row["used_by"])]
        if row["status"] not in {"queued", "mined", "rejected"} or row["tier"] not in {"A", "B", "C"} or row["kind"] not in KINDS or (row["kind"] == "community" and row["tier"] == "A"):
            findings.append({"id": "invalid_source_enum", "source": sid})
        for relative in used_by:
            if not (root / relative).is_file():
                findings.append({"id": "used_by_missing", "source": sid, "path": relative})
        missing = sorted(citing - set(used_by))
        if citing and row["status"] != "mined":
            findings.append({"id": "cited_not_mined", "source": sid, "status": row["status"]})
        for relative in missing:
            findings.append({"id": "missing_used_by", "source": sid, "path": relative})
        results.append({"source": sid, "status": row["status"], "citing": sorted(citing), "used_by": sorted(used_by), "missing": missing})
    return {"source_rows_checked": len(refs), "knowledge_files_expected": len(population["knowledge_paths"]),
            "reference_links": sum(len(v) for v in refs.values()), "findings": findings, "sources": results}


if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT
    r = check(root, POP)
    print(json.dumps({k: r[k] for k in ("source_rows_checked", "knowledge_files_expected", "reference_links")}, indent=1))
    print("findings:", json.dumps(r["findings"]))
    for s in r["sources"]:
        if s["source"] in ("S038", "S050", "S058"):
            print(json.dumps(s, indent=1))

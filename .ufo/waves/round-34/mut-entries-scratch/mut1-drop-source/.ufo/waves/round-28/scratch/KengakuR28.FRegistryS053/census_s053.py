#!/usr/bin/env python3
"""Independent S053 census under frozen13/35 literal contract.

Reimplements the declared contract semantics (population.json reference_pattern,
11-column Registry table, standalone S-mention counting, used_by subset/liveness,
status-when-cited) from the frozen contract text. Imports no production module.
"""
import hashlib
import json
import re
from pathlib import Path, PurePosixPath

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
SCRATCH = LANE / ".ufo/waves/round-28/scratch/KengakuR28.FRegistryS053"
POP = LANE / "plans/fixtures/r28/registry/population.json"
POP_SHA = "1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014"
ROW_ID = "S053"
REF = re.compile(r"(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])")
SOURCE_ID = re.compile(r"S[0-9]{3,}\Z")
KINDS = {"spec", "docs", "paper", "code", "tool", "dataset", "talk", "book",
         "community", "own-work"}
STATUSES = {"queued", "mined", "rejected"}
TIERS = {"A", "B", "C"}
CELLS = ("id", "source", "kind", "tier", "scope", "anchor", "teaches", "status",
         "opened", "recheck", "used_by")


def safe_path(value):
    p = PurePosixPath(value)
    return bool(value) and not p.is_absolute() and ".." not in p.parts and "\\" not in value


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
        if not cells or not SOURCE_ID.fullmatch(cells[0]):
            continue
        sid = cells[0]
        if len(cells) != 11:
            findings.append({"id": "malformed_source_row", "source": sid, "line": number})
            continue
        if sid in rows:
            findings.append({"id": "duplicate_source_id", "source": sid, "line": number})
            continue
        rows[sid] = dict(zip(CELLS, cells))
    return rows, findings


def census(root, label):
    rows, pf = parse_registry((root / "corpus/SOURCES.md").read_text())
    refs = {sid: set() for sid in json.loads(POP.read_text())["source_ids"]}
    knowledge_hits = {}
    for rel in json.loads(POP.read_text())["knowledge_paths"]:
        p = root / rel
        if not p.is_file():
            pf.append({"id": "knowledge_missing", "path": rel})
            continue
        ids = set(REF.findall(p.read_text())) & refs.keys()
        knowledge_hits[rel] = sorted(ids)
        for sid in ids:
            refs[sid].add(rel)
    citing = refs[ROW_ID]
    out = {"label": label, "parse_findings": pf, "rows_parsed": len(rows),
           "population_rows": len(refs), "population_paths": len(json.loads(POP.read_text())["knowledge_paths"])}
    row = rows.get(ROW_ID)
    r = {"citing_files": sorted(citing), "citing_count": len(citing)}
    if row is None:
        r["row"] = None
        r["findings"] = [{"id": "source_missing", "source": ROW_ID}]
    else:
        r["row"] = row
        used_by = ([] if row["used_by"] in ("", "—")
                   else [x.strip().strip("`") for x in re.split(r"[,;]", row["used_by"])])
        findings = []
        if (row["status"] not in STATUSES or row["tier"] not in TIERS
                or row["kind"] not in KINDS
                or (row["kind"] == "community" and row["tier"] == "A")):
            findings.append({"id": "invalid_source_enum", "source": ROW_ID})
        for rel in used_by:
            if not safe_path(rel):
                findings.append({"id": "invalid_used_by", "source": ROW_ID, "path": rel})
            elif not (root / rel).is_file():
                findings.append({"id": "used_by_missing", "source": ROW_ID, "path": rel})
        missing = sorted(citing - set(used_by))
        if citing and row["status"] != "mined":
            findings.append({"id": "cited_not_mined", "source": ROW_ID, "status": row["status"]})
        for rel in missing:
            findings.append({"id": "missing_used_by", "source": ROW_ID, "path": rel})
        r["used_by_parsed"] = sorted(used_by)
        r["missing_used_by"] = missing
        r["findings"] = findings
    out[ROW_ID] = r
    out["mention_lines"] = {}
    for rel in sorted(citing):
        out["mention_lines"][rel] = [
            i + 1 for i, line in enumerate((root / rel).read_text().splitlines())
            if REF.search(line) and ROW_ID in REF.findall(line)
        ]
    out["co_mentions"] = {rel: knowledge_hits[rel] for rel in sorted(citing)}
    print(json.dumps(out, indent=1, ensure_ascii=False))


if hashlib.sha256(POP.read_bytes()).hexdigest() != POP_SHA:
    raise SystemExit("population.json pin mismatch — refusing derivation")
census(SCRATCH / "baseline", "baseline-b9b24796277020d1b9b01923b45313d6a565e664")
census(LANE, "current-final")

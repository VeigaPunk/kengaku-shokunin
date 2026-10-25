#!/usr/bin/env python3
"""Independent S038 falsification under the frozen13/35 literal contract.

Reimplements the contract rules from direct reading of plans/registry_check.py and
population.json. Imports no production module. Read-only over the lane; all
mutations happen inside scratch copies.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
REV = "b9b24796277020d1b9b01923b45313d6a565e664"
POP_REL = "plans/fixtures/r28/registry/population.json"
POP_SHA = "1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014"
REF = re.compile(r"(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])")
SID = re.compile(r"S[0-9]{3,}\Z")
KINDS = {"spec", "docs", "paper", "code", "tool", "dataset", "talk", "book", "community", "own-work"}
TARGET = "S038"
CELLS = ("id", "source", "kind", "tier", "scope", "anchor", "teaches", "status", "opened", "recheck", "used_by")


def git_blob(rev, rel):
    out = subprocess.run(["git", "--no-optional-locks", "show", f"{rev}:{rel}"],
                         cwd=ROOT, capture_output=True, check=True)
    return out.stdout


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
        if not cells or not SID.fullmatch(cells[0]):
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


def used_by_of(row):
    if row["used_by"] in ("", "—"):
        return []
    return [p.strip().strip("`") for p in re.split(r"[,;]", row["used_by"])]


def enum_ok(row):
    return (row["status"] in {"queued", "mined", "rejected"} and row["tier"] in {"A", "B", "C"}
            and row["kind"] in KINDS and not (row["kind"] == "community" and row["tier"] == "A"))


def derive(kg_text_fn, src_text):
    rows, row_findings = parse_registry(src_text)
    refs = {sid: set() for sid in POP["source_ids"]}
    target_mentions = []
    target_mention_total = 0
    for rel in POP["knowledge_paths"]:
        text = kg_text_fn(rel)
        hits = set(REF.findall(text)) & refs.keys()
        for sid in hits:
            refs[sid].add(rel)
        target_mention_total += len(re.findall(r"(?<![A-Za-z0-9_])S038(?![A-Za-z0-9_])", text))
        if TARGET in hits:
            for number, line in enumerate(text.splitlines(), 1):
                if re.search(r"(?<![A-Za-z0-9_])S038(?![A-Za-z0-9_])", line):
                    target_mentions.append({"path": rel, "line": number, "snippet": line.strip()[:120]})
    citing = sorted(refs[TARGET])
    row = rows.get(TARGET)
    rep = {
        "row_parse_findings": [f for f in row_findings if f.get("source") == TARGET],
        "citing_files": citing,
        "target_mention_lines": target_mentions,
        "target_mention_count": target_mention_total,
    }
    if row is None:
        rep.update({"present": False, "status": None, "used_by": [], "missing_used_by": citing,
                    "findings": [{"id": "source_missing", "source": TARGET}] + [{"id": "missing_used_by", "source": TARGET, "path": p} for p in citing]})
        return rep, refs, rows
    used_by = used_by_of(row)
    missing = sorted(set(citing) - set(used_by))
    findings = []
    if not enum_ok(row):
        findings.append({"id": "invalid_source_enum", "source": TARGET})
    for rel in used_by:
        if not safe_path(rel):
            findings.append({"id": "invalid_used_by", "source": TARGET, "path": rel})
        elif not kg_is_file(rel):
            findings.append({"id": "used_by_missing", "source": TARGET, "path": rel})
    if citing and row["status"] != "mined":
        findings.append({"id": "cited_not_mined", "source": TARGET, "status": row["status"]})
    for rel in missing:
        findings.append({"id": "missing_used_by", "source": TARGET, "path": rel})
    rep.update({"present": True, "row_cells": {k: row[k] for k in ("kind", "tier", "status", "used_by")},
                "used_by": used_by, "missing_used_by": missing,
                "enum_ok": enum_ok(row), "findings": findings})
    return rep, refs, rows


def kg_is_file(rel):
    return (ROOT / rel).is_file()


def load_pop():
    raw = (ROOT / POP_REL).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == POP_SHA, "population digest mismatch"
    return json.loads(raw)


POP = load_pop()
assert POP["base_revision"] == REV, "population base_revision mismatch"
assert len(POP["source_ids"]) == 13 and len(POP["knowledge_paths"]) == 35

cur_kg = lambda rel: (ROOT / rel).read_text()
cur_src = (ROOT / "corpus/SOURCES.md").read_text()
base_kg = lambda rel: git_blob(REV, rel).decode()
base_src = git_blob(REV, "corpus/SOURCES.md").decode()

after, refs_cur, rows_cur = derive(cur_kg, cur_src)
before, refs_base, rows_base = derive(base_kg, base_src)

# Per-cell S038 row diff, baseline -> current
cell_diff = {}
b, c = rows_base.get(TARGET), rows_cur.get(TARGET)
if b and c:
    cell_diff = {k: {"before": b[k], "after": c[k]} for k in CELLS if b[k] != c[k]}

# Does the baseline knowledge file already cite S038 (red provenance)?
base_attr = git_blob(REV, "corpus/knowledge/attribution-interval-calibration.md").decode()
base_attr_lines = [n for n, line in enumerate(base_attr.splitlines(), 1)
                   if re.search(r"(?<![A-Za-z0-9_])S038(?![A-Za-z0-9_])", line)]

totals = {
    "source_rows_checked": len(refs_cur),
    "knowledge_files_expected": len(POP["knowledge_paths"]),
    "reference_links_current": sum(len(v) for v in refs_cur.values()),
    "reference_links_baseline": sum(len(v) for v in refs_base.values()),
    "s038_citing_files": len(refs_cur[TARGET]),
    "s038_used_by_entries": len(after.get("used_by", [])),
}

digests = {
    "population_sha256": hashlib.sha256((ROOT / POP_REL).read_bytes()).hexdigest(),
    "current_SOURCES_sha256": hashlib.sha256((ROOT / "corpus/SOURCES.md").read_bytes()).hexdigest(),
    "baseline_SOURCES_sha256": hashlib.sha256(git_blob(REV, "corpus/SOURCES.md")).hexdigest(),
    "population_base_revision": POP["base_revision"],
}

out = {
    "expected_before": before,
    "current_after": after,
    "s038_row_cell_diff": cell_diff,
    "baseline_attribution_mentions_lines": base_attr_lines,
    "totals": totals,
    "digests": digests,
}
print(json.dumps(out, indent=2, ensure_ascii=False))

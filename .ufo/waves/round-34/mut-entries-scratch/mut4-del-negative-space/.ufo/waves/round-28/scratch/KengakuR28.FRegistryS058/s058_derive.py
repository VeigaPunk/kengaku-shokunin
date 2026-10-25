#!/usr/bin/env python3
"""Independent S058 falsification derivation. Own parser/regex only.

Reads frozen population + lane tree + baseline via read-only `git show`.
Imports no production oracle (registry_check.py / benchmark_spec_audit.py
are never imported). Writes nothing outside scratch.
"""
import json
import re
import subprocess
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
BASE = "b9b24796277020d1b9b01923b45313d6a565e664"
POP = json.loads((LANE / "plans/fixtures/r28/registry/population.json").read_text())
IDS, PATHS = POP["source_ids"], POP["knowledge_paths"]
REF = re.compile(r"(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])")
ROWID = re.compile(r"S[0-9]{3,}\Z")
KINDS = {"spec", "docs", "paper", "code", "tool", "dataset", "talk", "book", "community", "own-work"}


def gitshow(rel):
    r = subprocess.run(["git", "-C", str(LANE), "show", f"{BASE}:{rel}"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def parse_rows(text):
    """Own registry-table parser (11 cells, ## Registry section, fences skipped)."""
    rows, fenced, active = {}, False, False
    for n, line in enumerate(text.splitlines(), 1):
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
        if not cells or not ROWID.fullmatch(cells[0]):
            continue
        rows.setdefault(cells[0], {"malformed_line": n} if len(cells) != 11 else
                        dict(zip(("id", "source", "kind", "tier", "scope", "anchor",
                                  "teaches", "status", "opened", "recheck", "used_by"), cells)))
    return rows


def scan_mentions(text):
    """All standalone Sxxx matches with their line numbers and fence state."""
    out, fenced = [], False
    for n, line in enumerate(text.splitlines(), 1):
        if line.startswith("```") or line.startswith("~~~"):
            fenced = not fenced
            continue
        for m in REF.finditer(line):
            out.append({"line": n, "id": m.group(0), "in_fence": fenced})
    return out


def parse_used_by(cell):
    return [] if cell in ("", "—") else [p.strip().strip("`") for p in re.split(r"[,;]", cell)]


def row_report(sid, rows, counts, exist_root):
    row, citing = rows.get(sid), sorted(counts.get(sid, set()))
    if row is None or "malformed_line" in row:
        return {"row_present": False, "row": row, "citing_frozen": citing}
    used = parse_used_by(row["used_by"])
    findings = []
    if (row["status"] not in {"queued", "mined", "rejected"} or row["tier"] not in {"A", "B", "C"}
            or row["kind"] not in KINDS or (row["kind"] == "community" and row["tier"] == "A")):
        findings.append("invalid_source_enum")
    for p in used:
        bad = (not p) or p.startswith("/") or ".." in p.split("/") or "\\" in p
        if bad:
            findings.append(["invalid_used_by", p])
        elif not (exist_root / p).is_file():
            findings.append(["used_by_missing", p])
    missing = sorted(set(citing) - set(used))
    if citing and row["status"] != "mined":
        findings.append("cited_not_mined")
    findings.extend(["missing_used_by", p] for p in missing)
    return {"row_present": True, "status": row["status"], "tier": row["tier"], "kind": row["kind"],
            "opened": row["opened"], "recheck": row["recheck"], "used_by": sorted(used),
            "citing_frozen": citing, "missing_used_by": missing, "findings": findings}


cur_counts, base_counts, base_missing_files = {}, {}, []
for rel in PATHS:
    text = (LANE / rel).read_text()
    for sid in set(REF.findall(text)):
        cur_counts.setdefault(sid, set()).add(rel)
    btext = gitshow(rel)
    if btext is None:
        base_missing_files.append(rel)
        continue
    for sid in set(REF.findall(btext)):
        base_counts.setdefault(sid, set()).add(rel)

cur_rows = parse_rows((LANE / "corpus/SOURCES.md").read_text())
base_rows = parse_rows(gitshow("corpus/SOURCES.md"))

out = {
    "population_sha256_current_file": subprocess.run(
        ["sha256sum", str(LANE / "plans/fixtures/r28/registry/population.json")],
        capture_output=True, text=True).stdout.split()[0],
    "baseline_source_files_missing": base_missing_files,
    "S058_baseline": row_report("S058", base_rows, base_counts, LANE),
    "S058_current": row_report("S058", cur_rows, cur_counts, LANE),
    "reference_links_current_frozen13": sum(len(v) for k, v in cur_counts.items() if k in set(IDS)),
    "reference_links_baseline_frozen13": sum(len(v) for k, v in base_counts.items() if k in set(IDS)),
    "per_row_citing_current_all13": {sid: sorted(cur_counts.get(sid, set())) for sid in IDS},
    "per_row_citing_baseline_all13": {sid: sorted(base_counts.get(sid, set())) for sid in IDS},
}
b, c = base_rows.get("S058"), cur_rows.get("S058")
if b and c and "malformed_line" not in b and "malformed_line" not in c:
    out["S058_immutable_cell_delta"] = {k: [b[k], c[k]] for k in
                                        ("source", "kind", "tier", "scope", "anchor", "teaches") if b[k] != c[k]}
    out["S058_mutable_cell_delta"] = {k: [b[k], c[k]] for k in ("status", "opened", "recheck", "used_by") if b[k] != c[k]}
    out["S058_immutable_cells_identical"] = all(b[k] == c[k] for k in ("source", "kind", "tier", "scope", "anchor", "teaches"))

# mention-level detail for S058 in the only citing file (fence state matters to literal contract)
target = LANE / "corpus/knowledge/extraction-policy-comparison.md"
out["S058_mentions_current_extraction_policy"] = [m for m in scan_mentions(target.read_text()) if m["id"] == "S058"]
btarget = gitshow("corpus/knowledge/extraction-policy-comparison.md")
out["S058_mentions_baseline_extraction_policy"] = [m for m in scan_mentions(btarget) if m["id"] == "S058"] if btarget else None

# S058 row raw lines, baseline vs current
def raw_row(text, sid):
    fenced, active = False, False
    for n, line in enumerate(text.splitlines(), 1):
        if line.startswith("```") or line.startswith("~~~"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if line.startswith("## "):
            active = line.strip() == "## Registry"
        if active and line.lstrip().startswith("|") and line.split("|")[1].strip() == sid:
            return {"line": n, "text": line.rstrip("\n")}
    return None

out["S058_row_raw_baseline"] = raw_row(gitshow("corpus/SOURCES.md"), "S058")
out["S058_row_raw_current"] = raw_row((LANE / "corpus/SOURCES.md").read_text(), "S058")

dest = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-28/scratch/KengakuR28.FRegistryS058/derived-map.json")
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(out, indent=2, ensure_ascii=False))
print("derived map written; S058 baseline findings:", out["S058_baseline"]["findings"],
      "| current findings:", out["S058_current"]["findings"],
      "| ref_links cur/base:", out["reference_links_current_frozen13"], out["reference_links_baseline_frozen13"])

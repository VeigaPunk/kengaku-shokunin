#!/usr/bin/env python3
"""FRegistryS057 independent row map for S057 under the frozen13/35 literal contract.

Own stdlib parser derived from the written contract; imports nothing from plans/.
Reads production only; writes nothing.
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
BASE = ROOT / ".ufo/waves/round-28/scratch/FRegistryS057/baseline/corpus"
CURR = ROOT / "corpus"
POP = ROOT / "plans/fixtures/r28/registry/population.json"
PIN = "1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014"

REF = re.compile(r"(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])")
SID = re.compile(r"S[0-9]{3,}\Z")
COLS = ("id source kind tier scope anchor teaches status opened recheck used_by").split()

pop = json.loads(POP.read_text())
ids, paths = pop["source_ids"], pop["knowledge_paths"]


def parse_registry(text):
    rows, dups, malformed = {}, [], []
    active, fenced = False, False
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
        if not cells or not SID.fullmatch(cells[0]):
            continue
        if len(cells) != 11:
            malformed.append((cells[0], n))
            continue
        if cells[0] in rows:
            dups.append((cells[0], n))
            continue
        rows[cells[0]] = dict(zip(COLS, cells))
        rows[cells[0]]["_line"] = n
    return rows, dups, malformed


def used_by(cell):
    return [] if cell in ("", "—") else [p.strip().strip("`") for p in re.split(r"[,;]", cell)]


def scan_s057(know_root, rel):
    text = (know_root / rel).read_text()
    fenced = False
    lines, count = [], 0
    for n, line in enumerate(text.splitlines(), 1):
        if line.startswith("```") or line.startswith("~~~"):
            fenced = not fenced
        hits = [m for m in REF.findall(line) if m == "S057"]
        if hits:
            count += len(hits)
            lines.append({"line": n, "hits": len(hits), "in_fence": fenced, "text": line.strip()[:200]})
    return count, lines


def corpus_root(tag):
    """corpus/ dir per tag (SOURCES.md); knowledge joins need lane root = its parent."""
    return BASE if tag == "baseline" else CURR


def lane_root(tag):
    return BASE.parent if tag == "baseline" else ROOT


out = {"population_rows": len(ids), "population_paths": len(paths),
       "population_sha256": hashlib.sha256(POP.read_bytes()).hexdigest(),
       "population_sha_matches_pin": hashlib.sha256(POP.read_bytes()).hexdigest() == PIN}

for tag in ("baseline", "current"):
    root = corpus_root(tag)
    lane = lane_root(tag)
    rows, dups, malformed = parse_registry((root / "SOURCES.md").read_text())
    row = rows.get("S057")
    ub = used_by(row["used_by"]) if row else []
    citing, contexts = [], {}
    total_mentions = 0
    for rel in paths:
        count, lines = scan_s057(lane, rel)
        if count:
            citing.append(rel)
            contexts[rel] = {"mentions": count, "lines": lines}
            total_mentions += count
    out[tag] = {
        "sources_sha256": hashlib.sha256((root / "SOURCES.md").read_bytes()).hexdigest(),
        "s057_line": row["_line"],
        "s057_row": {k: v for k, v in row.items()},
        "duplicate_rows": dups,
        "malformed_rows": malformed,
        "registry_rows_total": len(rows),
        "used_by_parsed": ub,
        "used_by_files_exist": {p: (lane / p).is_file() for p in ub},
        "used_by_files_are_frozen_or_lesson": {p: (p in paths, p == "corpus/lessons/round-27.md") for p in ub},
        "citing_frozen_paths_S057": citing,
        "citing_subset_of_used_by": set(citing) <= set(ub),
        "mention_contexts": contexts,
        "total_S057_mentions_in_frozen35": total_mentions,
        "status": row["status"],
        "s057_in_frozen13": "S057" in ids,
    }

b, c = out["baseline"], out["current"]
out["row_cell_diff"] = {k: [b["s057_row"][k], c["s057_row"][k]]
                        for k in COLS if b["s057_row"][k] != c["s057_row"][k]}
out["citing_set_identical"] = b["citing_frozen_paths_S057"] == c["citing_frozen_paths_S057"]
print(json.dumps(out, indent=1, ensure_ascii=False))

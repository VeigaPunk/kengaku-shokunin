#!/usr/bin/env python3
"""Scratch acceptance experiment: rebuild the red->green path for S038 from baseline
bytes only, in scratch copies. No production mutation; no production import."""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
REV = "b9b24796277020d1b9b01923b45313d6a565e664"
CHECKER = ROOT / "plans/registry_check.py"
EXP = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-28/scratch/KengakuR28.FRegistryS038/exp")
POP_REL = "plans/fixtures/r28/registry/population.json"
TARGET_RE = r"(?<![A-Za-z0-9_])S038(?![A-Za-z0-9_])"

import re
SID = re.compile(r"S[0-9]{3,}\Z")


def git_blob(rel):
    return subprocess.run(["git", "--no-optional-locks", "show", f"{REV}:{rel}"],
                          cwd=ROOT, capture_output=True, check=True).stdout


def parse_lines(text):
    """Return {sid: (line_index, cells)} for Registry rows plus fence-aware scan."""
    rows, active, fenced = {}, False, False
    for i, line in enumerate(text.splitlines()):
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
        if cells and SID.fullmatch(cells[0]) and len(cells) == 11 and cells[0] not in rows:
            rows[cells[0]] = (i, cells)
    return rows


def rebuild_row(cells):
    return "| " + " | ".join(cells) + " |"


base_src = git_blob("corpus/SOURCES.md").decode()
base_rows = parse_lines(base_src)
cur_src = (ROOT / "corpus/SOURCES.md").read_text()
cur_rows = parse_lines(cur_src)

# S050 cell diff too (its repair is the co-required delta)
diffs = {}
for sid in ("S038", "S050"):
    b = dict(zip(CELL_KEYS := ("id", "source", "kind", "tier", "scope", "anchor", "teaches", "status", "opened", "recheck", "used_by"), base_rows[sid][1]))
    c = dict(zip(CELL_KEYS, cur_rows[sid][1]))
    diffs[sid] = {k: {"before": b[k], "after": c[k]} for k in CELL_KEYS if b[k] != c[k]}

S050_USED_BY_REPAIRED = "corpus/lessons/round-27.md, corpus/knowledge/extraction-policy-comparison.md"
S038_USED_BY = "corpus/knowledge/attribution-interval-calibration.md"


def with_cells(text, sid, **updates):
    idx, cells = parse_lines(text)[sid]
    new = cells.copy()
    keymap = {"status": 7, "used_by": 10}
    for k, v in updates.items():
        new[keymap[k]] = v
    lines = text.splitlines()
    lines[idx] = rebuild_row(new)
    return "\n".join(lines) + "\n"


variants = {
    "A_baseline": base_src,
    "B_s050_only": with_cells(base_src, "S050", used_by=S050_USED_BY_REPAIRED),
    "C_both": with_cells(with_cells(base_src, "S050", used_by=S050_USED_BY_REPAIRED), "S038", status="mined", used_by=S038_USED_BY),
    "D_s038_only": with_cells(base_src, "S038", status="mined", used_by=S038_USED_BY),
}

if EXP.exists():
    shutil.rmtree(EXP)
results = {}
for name, src in variants.items():
    root = EXP / name
    (root / "corpus/knowledge").mkdir(parents=True)
    (root / POP_REL).parent.mkdir(parents=True)
    shutil.copy(ROOT / POP_REL, root / POP_REL)
    (root / "corpus/SOURCES.md").write_text(src)
    for rel in json.loads((ROOT / POP_REL).read_text())["knowledge_paths"]:
        (root / rel).write_bytes(git_blob(rel))
    (root / "corpus/lessons").mkdir(parents=True, exist_ok=True)
    (root / "corpus/lessons/round-27.md").write_bytes(git_blob("corpus/lessons/round-27.md"))
    proc = subprocess.run([sys.executable, "-B", str(CHECKER), "--root", str(root), "--json"],
                          capture_output=True, text=True)
    payload = json.loads(proc.stdout)
    s038 = next(s for s in payload["sources"] if s["source"] == "S038")
    results[name] = {
        "exit": proc.returncode,
        "finding_count": payload["finding_count"],
        "findings": payload["findings"],
        "reference_links": payload["reference_links"],
        "s038": s038,
        "sources_sha256": hashlib.sha256(src.encode()).hexdigest(),
    }

# Fence-position of the two current mention lines
attr = (ROOT / "corpus/knowledge/attribution-interval-calibration.md").read_text()
fenced, fencepos = False, {}
for i, line in enumerate(attr.splitlines(), 1):
    if line.startswith("```") or line.startswith("~~~"):
        fenced = not fenced
    if re.search(TARGET_RE, line):
        fencepos[i] = "fenced" if fenced else "prose"

out = {"s038_s050_cell_diffs": diffs, "variants": results, "mention_fence_position": fencepos}
print(json.dumps(out, indent=2, ensure_ascii=False))

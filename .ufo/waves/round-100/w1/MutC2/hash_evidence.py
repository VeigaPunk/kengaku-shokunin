#!/usr/bin/env python3
"""Recompute the before/after sha256 of every tree mutant's touched files (no re-run needed)."""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, "/fast/scratch/hyaku/kengaku-r100/MutC2")
import driver  # noqa: E402

SRC = Path("/fast/scratch/hyaku/kengaku-r100/MutC2/base")
TMP = Path("/fast/scratch/hyaku/kengaku-r100/MutC2/hashwork")
SUBSET = ["corpus/SOURCES.md", "corpus/evidence", ".ufo/waves/round-100/L1/c2-live-refetch.txt",
          "plans/round-100-claims.md"]


def sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else "absent"


def build():
    if TMP.exists():
        shutil.rmtree(TMP)
    for rel in SUBSET:
        s, d = SRC / rel, TMP / rel
        d.parent.mkdir(parents=True, exist_ok=True)
        if s.is_dir():
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)


def files():
    for rel in SUBSET:
        s = SRC / rel
        if s.is_dir():
            for p in sorted(s.rglob("*")):
                if p.is_file():
                    yield str(p.relative_to(SRC))
        else:
            yield rel


out = {}
for mid, spec in sorted(driver.MUTANTS.items()):
    if "tree" not in spec or spec["tree"] in ("none", "no_claims"):
        continue
    build()
    driver.apply_tree(TMP, spec)
    before, after = {}, {}
    for rel in files():
        b, a = sha(SRC / rel), sha(TMP / rel)
        if a != b:
            before[rel], after[rel] = b, a
    out[mid] = dict(before=before, after=after)
    print(mid, json.dumps(out[mid]))

Path("/fast/scratch/hyaku/kengaku-r100/MutC2/results/tree_hashes.json").write_text(json.dumps(out, indent=1))

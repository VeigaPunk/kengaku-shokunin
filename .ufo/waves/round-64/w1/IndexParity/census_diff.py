#!/usr/bin/env python3
"""Differential of the round-13 coverage census's `lessons` category, base vs base+six-rows.

Uses the lane's own instrument functions (parse_index, category) so no second convention.
Read-only: the census writes nothing (it prints JSON to stdout).
"""
import importlib.util, json, pathlib, sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
spec = importlib.util.spec_from_file_location(
    "coverage_census", LANE / "corpus/evidence/round13-coverage/coverage_census.py")
census = importlib.util.module_from_spec(spec)
sys.modules["coverage_census"] = census
spec.loader.exec_module(census)

BASE = pathlib.Path("/fast/scratch/hyaku/kengaku-r64/IndexParity/diffroot/base/corpus/README.md")
PATCHED = pathlib.Path("/fast/scratch/hyaku/kengaku-r64/IndexParity/diffroot/patched/corpus/README.md")

lessons_dir = LANE / "corpus/lessons"
on_disk = sorted(p.name for p in lessons_dir.iterdir() if p.is_file())


def lessons_category(readme_text):
    rows = census.parse_index(readme_text)
    linked = rows["lessons"]
    discovered = {n for n in on_disk}
    found = set(linked)
    return {
        "files": len(discovered),
        "indexed": len(discovered & found),
        "unindexed": sorted(discovered - found),
        "dangling": sorted(found - discovered),
        "duplicate_rows": sorted({n for n in linked if linked.count(n) >= 2}),
    }


base = lessons_category(BASE.read_text(encoding="utf-8"))
patched = lessons_category(PATCHED.read_text(encoding="utf-8"))
print("BASE lessons category:")
print(json.dumps(base, indent=2, sort_keys=True))
print()
print("PATCHED lessons category:")
print(json.dumps(patched, indent=2, sort_keys=True))
print()
print(f"indexed: {base['indexed']} -> {patched['indexed']}")
print(f"unindexed count: {len(base['unindexed'])} -> {len(patched['unindexed'])}")
print(f"dangling: {base['dangling']} -> {patched['dangling']}")
print(f"duplicate_rows: {base['duplicate_rows']} -> {patched['duplicate_rows']}")

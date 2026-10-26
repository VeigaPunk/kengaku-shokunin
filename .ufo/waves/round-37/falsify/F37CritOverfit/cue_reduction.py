#!/usr/bin/env python3
"""How far can the overfit cue be coarsened before it stops reproducing the declared outputs?

Rebuilds the counter's 64 fixtures, reads the observed (exit, DEFECT set) per fixture from
overfit_table.json, and scores three progressively finer non-identity cues against the 16 output classes:

  E1  (flag set, set of working files that differ from the genuine package)
  E2  (flag set, set of differing file basenames)
  E3  E1 plus the byte size of the entry markdown
  E4  E3 plus the entry markdown's line count

An "ambiguous" cue value is one shared by fixtures with different declared outputs: a gate keyed on that
cue alone cannot match every declaration. The overfit_gate.py uses the finest cue available (exact content
identity) and matches.

Usage: python3 cue_reduction.py --lane CLONE --work SCRATCH/work4 --table SEATDIR/overfit_table.json
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import json
import pathlib
import shutil
import sys

SKIP = {".git", "__pycache__"}


def load(lane):
    spec = importlib.util.spec_from_file_location("k37", lane / "plans/round37_c1_verify.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def files(base):
    base = pathlib.Path(base)
    out = {}
    for p in sorted(base.rglob("*")):
        rel = p.relative_to(base).as_posix()
        if any(part in SKIP for part in pathlib.PurePosixPath(rel).parts):
            continue
        if p.is_file():
            out[rel] = (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_size,
                        p.read_text(errors="replace").count("\n"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--table", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    table = {r["fid"]: r for r in json.load(open(a.table))["fixtures"]}
    work.mkdir(parents=True, exist_ok=True)
    k37 = load(lane)
    r36 = k37.load_r36(lane)
    ctx = k37.Ctx(lane, r36)
    fixtures = k37.r36_fixtures(r36) + k37.battery37_fixtures(lane / k37.BATTERY_REL)
    recs = {}
    for i, fx in enumerate(fixtures):
        d = work / "fx" / f"f{i:03d}"
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
        argv = list(fx["build"](ctx, d))
        if "package" not in argv:
            continue
        recs[fx["fid"]] = (d, files(d), tuple(t for t in argv
                                              if t.startswith("--") and t not in
                                              ("--root", "--file", "--capture-dir", "--spec")))
    gen = recs["r36-P0"][1]

    def dset(fid):
        _, t, _ = recs[fid]
        return tuple(sorted((set(t) ^ set(gen)) | {k for k in set(t) & set(gen) if t[k][0] != gen[k][0]}))

    def entry(fid):
        return recs[fid][1].get("corpus/knowledge/tb2-protein-assembly-grader.md", (None, None, None))

    cues = {
        "E1 paths": lambda f: (recs[f][2], dset(f)),
        "E2 basenames": lambda f: (recs[f][2], tuple(sorted(p.rsplit("/", 1)[-1] for p in dset(f)))),
        "E3 E1+entry-size": lambda f: (recs[f][2], dset(f), entry(f)[1]),
        "E4 E3+entry-lines": lambda f: (recs[f][2], dset(f), entry(f)[1], entry(f)[2]),
    }
    fids = sorted(recs)
    for name, fn in cues.items():
        groups = collections.defaultdict(set)
        for f in fids:
            groups[fn(f)].add((table[f]["rc"], tuple(table[f]["defects"])))
        amb = [k for k, v in groups.items() if len(v) > 1]
        nfix = sum(1 for f in fids if len(groups[fn(f)]) > 1)
        print(f"{name}: cue_values={len(groups)} ambiguous_values={len(amb)} ambiguous_fixtures={nfix}")
        for k, v in [(k, groups[k]) for k in amb]:
            print(f"    {k!r} -> {sorted(v)}")
    print("entry-file collisions at equal (path, size, lines):")
    buckets = collections.defaultdict(list)
    for f in fids:
        e = entry(f)
        if dset(f) == ("corpus/knowledge/tb2-protein-assembly-grader.md",):
            buckets[(e[1], e[2])].append((f, table[f]["defects"]))
    for k, v in sorted(buckets.items(), key=lambda kv: str(kv[0])):
        if k[0] is None:
            continue
        if len({tuple(x[1]) for x in v}) > 1:
            print(f"    size={k[0]} lines={k[1]} -> {v}")


if __name__ == "__main__":
    sys.exit(main())

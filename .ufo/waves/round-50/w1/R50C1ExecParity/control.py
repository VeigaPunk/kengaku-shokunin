#!/usr/bin/env python3
"""Sensitivity control for the parity table: five honest classes the BASE fence refuses.

If the three fences and the harness can only ever print BREACH, the parity table is inert. This control
scores the five honest fixtures the round-50 claims name as the base fence's over-refusals
(`n17-replace-ref`, `n18-shallow-fetch`, `n20-linked-worktree`, `n21-separate-gitdir`,
`n22-alternates-in-d`) against the same three fences with the same harness. Expected: base BREACH on all
five (the measured control), repair ADMIT on all five (the claimed repair).

Usage: python3 control.py --lane DIR --fences DIR --work DIR
"""
from __future__ import annotations

import argparse
import importlib.util
import pathlib
import sys


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--fences", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    lane, fences, work = (pathlib.Path(a.lane).resolve(), pathlib.Path(a.fences).resolve(),
                          pathlib.Path(a.work).resolve())
    work.mkdir(parents=True, exist_ok=True)
    cnt = load(lane / "plans/round50_c1_verify.py", "k50_counter")
    hb = load(lane / "plans/honest50/build_honest_population.py", "k50_honest")
    k44 = load(lane / "plans/round44_c1_verify.py", "k50_k44")
    mods = [lane / "plans/honest50/modules/novel49/n17_replace_ref.py",
            lane / "plans/honest50/modules/novel49/n18_shallow_fetch.py",
            lane / "plans/honest50/modules/novel49/n20_linked_worktree.py",
            lane / "plans/honest50/modules/novel50/n21_separate_gitdir.py",
            lane / "plans/honest50/modules/novel50/n22_alternates_in_d.py"]
    harness = work / "harness.py"
    harness.write_text(cnt.HARNESS)
    rows = {}
    for name in ("base_fence.py", "r49_candidate.py", "repair_fence.py"):
        fpath = fences / name
        built, fails = cnt.build_all(hb, k44, [(m, m.stem) for m in mods], work / name.split("_")[0])
        for e in fails:
            print(f"BUILD-ERROR {name} {e}", flush=True)
        v = cnt.verdicts(fpath, built, harness, work / name.split("_")[0])
        vmap = dict(zip((x["dir"] for x in built), v))
        print(f"FENCE {name} sha256={cnt.sha256_file(fpath)} fixtures={len(built)}", flush=True)
        for x in built:
            hit = vmap[x["dir"]]
            rows.setdefault(x["fid"], {})[name] = (hit["v"], hit["why"])
    print("fid\tbase\tr49\trepair", flush=True)
    for fid in sorted(rows):
        cells = [rows[fid][k][0] for k in ("base_fence.py", "r49_candidate.py", "repair_fence.py")]
        print(f"{fid}\t" + "\t".join(cells), flush=True)
        for k in ("base_fence.py", "repair_fence.py"):
            print(f"  {k}: {rows[fid][k][0]} {rows[fid][k][1][:110]}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

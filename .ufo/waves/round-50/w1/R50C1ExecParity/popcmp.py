#!/usr/bin/env python3
"""Supplementary: the three fences over the frozen 126-fixture honest population.

The parity column "r49-candidate verdict" is only meaningful if that fence is distinguishable from the base
fence at all. This builds the frozen honest population once per fence and prints each fence's
admitted/refused/error rollup plus the base-vs-r49 and base-vs-repair verdict-vector differences.

Usage: python3 popcmp.py --lane DIR --fences DIR --work DIR
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import pathlib
import sys


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        while chunk := fh.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


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
    hb.ALLOW_NO_REPO = True
    k44 = load(lane / "plans/round44_c1_verify.py", "k50_k44")
    pop = lane / "plans/honest50/population.txt"
    print(f"POPULATION sha256={sha256_file(pop)} pin={cnt.POPULATION_SHA}", flush=True)
    rows = cnt.parse_population(pop)
    modules, seen = [], set()
    for r in rows:
        if r["module"] in seen:
            continue
        seen.add(r["module"])
        modules.append((lane / r["module"], r["module"].replace("/", "-")[:-3]))
    harness = work / "harness.py"
    harness.write_text(cnt.HARNESS)
    vec = {}
    for name in ("base_fence.py", "r49_candidate.py", "repair_fence.py"):
        fpath = fences / name
        built, fails = cnt.build_all(hb, k44, modules, work / name.split("_")[0])
        v = cnt.verdicts(fpath, built, harness, work / name.split("_")[0])
        vmap = dict(zip((x["dir"] for x in built), v))
        rec = {}
        for b in built:
            hit = vmap[b["dir"]]
            rec[b["fid"]] = (hit["v"], hit["why"])
        vec[name] = rec
        adm = sum(1 for k in rec if rec[k][0] == "ADMIT")
        ref = sum(1 for k in rec if rec[k][0] == "BREACH")
        err = sum(1 for k in rec if rec[k][0] == "ERROR")
        print(f"HONEST {name} sha256={sha256_file(fpath)} fixtures={len(built)} build_errors={len(fails)} "
              f"admitted={adm} refused={ref} error={err}", flush=True)
        by_fid = {r["fid"]: r["tree"] for r in rows}
        mis = [b["fid"] for b in built if b["fid"] not in by_fid
               or hb.tree_identity(b["dir"])[0] != by_fid[b["fid"]]]
        print(f"IDENTITY {name} mismatched={len(mis)} {mis[:6]}", flush=True)
    base = vec["base_fence.py"]
    for other in ("r49_candidate.py", "repair_fence.py"):
        changed = [(k, base[k][0], vec[other][k][0]) for k in base if base[k][0] != vec[other].get(k, ("?",))[0]]
        print(f"DIFF base->{other} changed={len(changed)}", flush=True)
        for k, x, y in sorted(changed):
            print(f"  {k}: {x} -> {y}   [{base[k][1][:80]}]", flush=True)
    print(f"DIFF r49->repair changed={sum(1 for k in base if vec['r49_candidate.py'][k][0] != vec['repair_fence.py'][k][0])}",
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

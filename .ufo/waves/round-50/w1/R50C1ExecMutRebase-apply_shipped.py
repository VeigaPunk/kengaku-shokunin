#!/usr/bin/env python3
"""Apply the SHIPPED battery (c1-mutants.json) to a fence and report per-row applies/caught.

Independent of the authoring tool: payloads come from the emitted JSON, application goes through the counter's
own apply_mutant, the predicate is the counter's (verdict-vector change over honest + refusals + sealed).
Usage: apply_shipped.py --lane CLONE --fence FENCE --battery JSON --work DIR
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--fence", required=True)
    ap.add_argument("--battery", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    fence_path = pathlib.Path(a.fence).resolve()
    work = pathlib.Path(tempfile.mkdtemp(prefix="k50-apply-", dir=a.work))
    spec = json.loads(pathlib.Path(a.battery).read_text())
    mutants = spec["mutants"]
    try:
        v = load(lane / "plans/round50_c1_verify.py", "v")
        hb = load(lane / "plans/honest50/build_honest_population.py", "hb")
        hb.ALLOW_NO_REPO = True
        k44 = load(lane / "plans/round44_c1_verify.py", "k44")
        rows = v.parse_population(lane / "plans/honest50/population.txt")
        mods, seen = [], set()
        for r in rows:
            if r["module"] in seen:
                continue
            seen.add(r["module"])
            mods.append((lane / r["module"], r["module"].replace("/", "-")[:-3]))
        honest, fails = v.build_all(hb, k44, mods, work / "honest")
        allfx = list(honest)
        for rel in ("plans/refusals46", "plans/sealed46", "plans/sealed50"):
            d = lane / rel
            if not d.is_dir():
                continue
            files = sorted(d.glob("*.py"))
            fx, _x = v.build_all(hb, k44, [(f, f"{rel.split('/')[-1]}-{f.stem}") for f in files],
                                 work / rel.replace("/", "-"))
            allfx += fx
        fence = load(fence_path, "fence_under_test")
        ref = v.verdicts(fence, allfx)
        refv = [(x["fid"], x["v"]) for x in ref]
        print(f"FENCE {fence_path} sha256={v.sha256_file(fence_path)}")
        print(f"BATTERY {a.battery} declared_candidate={spec['candidate_fence_sha256']} rows={len(mutants)}")
        print(f"FIXTURES honest={len(honest)} total={len(allfx)} build_errors={len(fails)}")
        caught = na = survived = 0
        for m in mutants:
            dest = work / "m" / f"{m['id']}.py"
            p, why = v.apply_mutant(fence_path, m["payload"], dest)
            if p is None:
                na += 1
                print(f"ROW {m['id']} NOT-APPLICABLE {why[:110]}")
                continue
            mod = load(p, "mut_" + m["id"].replace("-", "_"))
            mv = v.verdicts(mod, allfx)
            diffs = [(b["fid"], bq["v"], b["v"]) for bq, b in zip(ref, mv) if bq["v"] != b["v"]]
            if diffs:
                caught += 1
                print(f"ROW {m['id']} CAUGHT n={len(diffs)} first={diffs[0][0]} {diffs[0][1]}->{diffs[0][2]}")
            else:
                survived += 1
                print(f"ROW {m['id']} SURVIVED")
        print(f"SUMMARY rows={len(mutants)} caught={caught} survived={survived} not_applicable={na}")
        return 0 if caught >= 16 and survived == 0 and na == 0 else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

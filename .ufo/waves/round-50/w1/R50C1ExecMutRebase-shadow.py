#!/usr/bin/env python3
"""Per-row apply / verdict-change / reason-change table for a battery against one fence.

Verdict change is the counter's kill predicate; reason changes prove a mutation is *shadowed* (the leg is
reached but another leg still refuses) rather than unexercised.
Usage: shadow.py --lane CLONE --fence FENCE --battery JSON --work DIR
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
    work = pathlib.Path(tempfile.mkdtemp(prefix="k50-shadow-", dir=a.work))
    mutants = json.loads(pathlib.Path(a.battery).read_text())["mutants"]
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
        honest, _f = v.build_all(hb, k44, mods, work / "honest")
        allfx = list(honest)
        for rel in ("plans/refusals46", "plans/sealed46", "plans/sealed50"):
            d = lane / rel
            if not d.is_dir():
                continue
            files = sorted(d.glob("*.py"))
            fx, _x = v.build_all(hb, k44, [(f, f"{rel.split('/')[-1]}-{f.stem}") for f in files],
                                 work / rel.replace("/", "-"))
            allfx += fx
        ref = v.verdicts(load(fence_path, "ref"), allfx)
        print(f"FENCE {fence_path} sha256={v.sha256_file(fence_path)}")
        print("row\tapplies\tverdict_changes\treason_changes\texample_reason_after_mutation")
        for m in mutants:
            dest = work / "m" / f"{m['id']}.py"
            p, why = v.apply_mutant(fence_path, m["payload"], dest)
            if p is None:
                print(f"{m['id']}\tno\t0\t0\tpayload does not apply: {why[:80]}")
                continue
            mv = v.verdicts(load(p, "mt_" + m["id"].replace("-", "_")), allfx)
            vc = [1 for x, y in zip(ref, mv) if x["v"] != y["v"]]
            rc = [y["why"] for x, y in zip(ref, mv) if x["why"] != y["why"]]
            ex = (vc and "(verdict flip)") or (rc[0][:100] if rc else "-")
            print(f"{m['id']}\tyes\t{len(vc)}\t{len(rc)}\t{ex.replace(chr(9), ' ')}")
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

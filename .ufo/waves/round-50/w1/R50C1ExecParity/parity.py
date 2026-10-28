#!/usr/bin/env python3
"""R50C1ExecParity: before/after refusal parity across three fences.

For every fixture of plans/refusals46 (20 modules), plans/sealed46 (12 modules) and plans/sealed50 (the
assembled blind set), build the fixture ONCE PER FENCE ROUND with the counter's own builder contract and
score it with the counter's own out-of-process harness:

  base    plans/fixture_fence.py @ 71f5f5f (sha256 05d5fe03…)  == stage-1 freeze fence
  r49     .ufo/waves/round-49/w1/R49C1ExecFenceA/fence_a.py (sha256 b687b1d9…), the r49 candidate
  repair  plans/fixture_fence.py @ lane tip (the landed repair)

Usage: python3 parity.py --lane DIR --fences DIR --work DIR --out parity.tsv
"""
from __future__ import annotations

import argparse
import collections
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
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    lane, fences, work = (pathlib.Path(a.lane).resolve(), pathlib.Path(a.fences).resolve(),
                          pathlib.Path(a.work).resolve())
    work.mkdir(parents=True, exist_ok=True)

    cnt = load(lane / "plans/round50_c1_verify.py", "k50_counter")
    hb = load(lane / "plans/honest50/build_honest_population.py", "k50_honest")
    hb.ALLOW_NO_REPO = True                    # hostile legs include fixtures with no repo under d
    k44 = load(lane / "plans/round44_c1_verify.py", "k50_k44")

    fence_paths = collections.OrderedDict([
        ("base", fences / "base_fence.py"),
        ("r49", fences / "r49_candidate.py"),
        ("repair", fences / "repair_fence.py"),
    ])
    for f in fence_paths.values():
        print(f"FENCE {f.name} sha256={cnt.sha256_file(f)}", flush=True)

    sets = collections.OrderedDict()
    for rel in ("plans/refusals46", "plans/sealed46", "plans/sealed50"):
        d = lane / rel
        sets[rel.split("/")[-1]] = sorted(d.glob("*.py"))
    for k, v in sets.items():
        print(f"SET {k} modules={len(v)}", flush=True)

    # fixture build is fence-independent: build one independent population per scoring round so a fence
    # that mutates a fixture cannot poison a later round.
    rounds = {}
    harness = work / "harness.py"
    harness.write_text(cnt.HARNESS)
    for fname, fpath in fence_paths.items():
        built = {}
        failures = []
        for sname, files in sets.items():
            fx, fails = cnt.build_all(hb, k44, [(f, f"{sname}-{f.stem}") for f in files],
                                      work / fname / sname)
            built[sname] = fx
            failures += [f"{sname}/{e}" for e in fails]
            print(f"BUILD {fname} {sname} fixtures={len(fx)} build_errors={len(fails)}", flush=True)
        order = [x for s in sets for x in built[s]]
        v = cnt.verdicts(fpath, order, harness, work / fname)
        assert len(v) == len(order), (len(v), len(order))
        rounds[fname] = (built, dict(zip((x["dir"] for x in order), v)), failures)
        print(f"SCORE {fname} fixtures={len(v)}", flush=True)

    rows = []
    for sname, files in sets.items():
        for f in files:
            mod = str(f)
            per = {}
            for fname, (built, vmap, _fails) in rounds.items():
                for x in built[sname]:
                    if x["module"] != mod:
                        continue
                    hit = vmap.get(x["dir"])
                    per.setdefault(x["fid"], {})[fname] = hit["v"] if hit else "MISSING"
                    why = (hit["why"] if hit else "not built").replace(str(x["dir"]), "{D}")
                    why = why.replace(str(work.parent), "{W}")
                    per[x["fid"]].setdefault("why", {})[fname] = " ".join(why.split())[:140]
            for fid in sorted(per):
                cells = [per[fid].get(k, "MISSING") for k in fence_paths]
                changed = len(set(cells)) > 1
                whys = [per[fid]["why"].get(k, "") for k in fence_paths]
                rows.append("\t".join([sname, f.name, fid] + cells
                                       + ["CHANGED" if changed else "-"] + whys))

    hdr = "\t".join(["set", "module", "fid", "base", "r49", "repair", "changed",
                     "base_why", "r49_why", "repair_why"])
    pathlib.Path(a.out).write_text(hdr + "\n" + "\n".join(rows) + "\n")

    all_breach = all(r.split("\t")[3:6] == ["BREACH"] * 3 for r in rows)
    for sname in sets:
        sub = [r.split("\t") for r in rows if r.startswith(sname + "\t")]
        print(f"PARITY {sname} rows={len(sub)} base_breach={sum(1 for r in sub if r[3]=='BREACH')} "
              f"r49_breach={sum(1 for r in sub if r[4]=='BREACH')} "
              f"repair_breach={sum(1 for r in sub if r[5]=='BREACH')}", flush=True)
    non = [r for r in rows if r.split("\t")[3:6] != ["BREACH"] * 3]
    for r in non:
        print(f"NON-BREACH {r.split(chr(9))[0]} {r.split(chr(9))[2]} "
              f"base={r.split(chr(9))[3]} r49={r.split(chr(9))[4]} repair={r.split(chr(9))[5]}", flush=True)
    ch = [r for r in rows if "\tCHANGED\t" in r]
    print(f"CHANGED rows={len(ch)}", flush=True)
    for r in ch:
        p = r.split("\t")
        print(f"CHANGED {p[0]} {p[2]} base={p[3]} r49={p[4]} repair={p[5]}", flush=True)
    for fname, (_b, v, fails) in rounds.items():
        for e in fails:
            print(f"BUILD-ERROR {fname} {e}", flush=True)
    print(f"ALL-BREACH all_fences={all_breach} rows={len(rows)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

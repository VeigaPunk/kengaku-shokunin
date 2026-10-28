#!/usr/bin/env python3
"""Round-50 C1 counter: does the repaired fixture fence do what the lane says it does about HONEST fixtures?

Self-assessment under test (`SCORECARD.md`, capability `fenced-fixture-discovery`; `plans/fixture_fence.py`
docstring): "admit only a fixture whose git store, discovered repos and argv stay inside `d`". Round 48 measured
that the landed fence refuses ordinary `git init` states (`HONEST fixtures=120 admitted=112 refused=8`); round 49
extended the population to 124 and never scored a repair. This counter scores ONE question that the lane had no
instrument for before round 50: on a frozen population of honest repositories, does the fence admit every one,
while still refusing every frozen hostile module, under a mutant floor?

Frozen predicate (`plans/round-50-claims.md` §C1; the same sentence is the receipt label):
  C1 passes iff `python3 plans/round50_c1_verify.py --lane .` prints
    `POPULATION fixtures=126 pin=b5197f94… mismatched=0`,
    `HONEST fixtures=126 admitted=126 refused=0 error=0`,
    `REFUSALS total=20 clean=20 leaked=0`,
    `SEALED total=<S> clean=<S> leaked=0`,
    `MUTANTS total=23 caught>=12 floor=12 verdict=met`,
    `PREDICATE R50-C1 pass`, exit 0, on a clean clone of the landing tip.

Legs:
  POPULATION  `plans/honest50/population.txt` is the frozen population: 104 fixtures of the standing batteries
              (`plans/battery42|43|44`), the 9 r46 novel classes, the 7 r48 classes, the 4 r49 classes and the 2
              r50 classes (`plans/honest50/modules/novel50/n21,n22`). Each fixture is REBUILT here and its
              canonical identity must equal the pinned `tree_sha256`; a mismatch is `mismatched=` and fails.
  HONEST      every honest fixture must be ADMITTED (`breach() is None`). A refusal is over-refusal; an
              exception is `error=`, never an admission.
  REFUSALS    the 20 frozen hostile modules `plans/refusals46/` (each fixture must be REFUSED).
  SEALED      the 12 frozen modules `plans/sealed46/` plus any `plans/sealed50/` module authored blind against
              the repaired fence in wave 1 (each fixture must be REFUSED).
  MUTANTS     `plans/mutants50/c1-mutants.json`: each row's inline unified diff is applied to a copy of the
              fence under test; the mutant is CAUGHT iff the verdict vector over all three legs differs from the
              reference vector. A payload that does not apply, or leaves `breach` undefined, is `broken`, never
              caught.

Inherited from the round-46/49 counters: the fixture builder is the round-44 counter's `Ctx` (imported, not
copied) through `plans/honest50/build_honest_population.py`; fixture identity is the population builder's own
canonical digest. NOT measured here (named limits): outside-`d` reads made while deciding (the round-46 counter's
strace/B1-B6 legs, unchanged and not re-scored — the repaired fence starts no git child at all, and
`plans/round46_c1_verify.py` remains the standing instrument for that property); io_uring; host paths outside
the scratch root.

Receipt: the first line prints `REV <40-hex>` of the tree measured; a dirty tree prints `TREE dirty=<n>` and fails
the predicate in the default mode, because the predicate is bound to a clean clone.

Usage: python3 plans/round50_c1_verify.py --lane . [--work DIR] [--fence PATH] [--skip-mutants]
Exit: 0 predicate pass · 1 predicate fail · 2 setup error.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

HONEST_TOTAL = 126            # frozen literal; the counter cannot self-satisfy it from the file it reads
MUTANT_MIN = 12               # frozen floor: at least 12 rows, and at least 12 caught (Q38: directions witnessed)
REFUSALS_TOTAL = 20           # frozen: modules under plans/refusals46
SEALED46_TOTAL = 12           # frozen: modules under plans/sealed46
SEALED50_MIN = 6              # frozen: blind held-out modules authored in round 50 wave 1
POPULATION_SHA = "b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69"

FENCE_REL = "plans/fixture_fence.py"
POP_REL = "plans/honest50/population.txt"
BUILDER_REL = "plans/honest50/build_honest_population.py"
K44_REL = "plans/round44_c1_verify.py"
REFUSALS_REL = "plans/refusals46"
SEALED_RELS = ("plans/sealed46", "plans/sealed50")
MUTANTS_REL = "plans/mutants50/c1-mutants.json"


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        while chunk := fh.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def module_path(lane, module):
    """Population rows name the module by its lane-relative path (battery modules and honest50 modules alike)."""
    return lane / module


def parse_population(path):
    rows = []
    for line in path.read_text().splitlines():
        if not line.startswith("HONEST "):
            continue
        _tag, tree, population, module, fid, tool = line.split()
        rows.append({"tree": tree, "population": population, "module": module.split("#")[0],
                     "fid": fid, "tool": tool})
    return rows


def build_all(hb, k44, modules, work):
    """Build each module once into its own parent; return [{fid,tool,argv,dir,module}] and failures."""
    built, failures = [], []
    for i, (path, tag) in enumerate(modules):
        gen = work / f"m{i:03d}-{tag}"
        gen.mkdir(parents=True, exist_ok=True)
        try:
            for fid, tool, _expect, _defects, argv, d, _b in hb.build_once(k44, path, gen):
                built.append({"fid": fid, "tool": tool, "argv": argv, "dir": d, "module": str(path)})
        except Exception as e:                                          # a build failure is a receipt
            failures.append(f"{path.name}: {type(e).__name__}: {e}")
    return built, failures


def verdicts(fence_mod, fixtures):
    """One verdict per fixture: ADMIT / BREACH / ERROR (a raising fence is never an admission)."""
    out = []
    for f in fixtures:
        try:
            r = fence_mod.breach(f["dir"], f["argv"], f["tool"])
            out.append({"fid": f["fid"], "v": "BREACH" if r else "ADMIT", "why": str(r or "")[:200]})
        except Exception as e:
            out.append({"fid": f["fid"], "v": "ERROR", "why": f"{type(e).__name__}: {e}"})
    return out


def apply_mutant(fence_path, payload, dest):
    """Apply one inline unified diff to a copy of the fence; return (path, None) or (None, reason)."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(fence_path, dest)
    diff = dest.with_suffix(".patch")
    diff.write_text(payload if payload.endswith("\n") else payload + "\n")
    p = subprocess.run(["patch", "--batch", "--silent", "-p1", "-i", str(diff), str(dest)],
                       capture_output=True, text=True)
    if p.returncode != 0:
        return None, f"patch-rc={p.returncode} {p.stdout.strip()[-160:]}"
    try:
        load(dest, f"mutant_{dest.stem}")
    except Exception as e:
        return None, f"import: {type(e).__name__}: {e}"
    return dest, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", default=None)
    ap.add_argument("--fence", default=None, help="fence under test (default plans/fixture_fence.py)")
    ap.add_argument("--skip-mutants", action="store_true", help="testing only: omit the mutant leg")
    ap.add_argument("--allow-dirty", action="store_true", help="testing only: score a dirty tree")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    for rel in (FENCE_REL, POP_REL, BUILDER_REL, K44_REL):
        if not (lane / rel).is_file():
            print(f"SETUP missing {rel}", file=sys.stderr)
            return 2
    fence_path = pathlib.Path(a.fence).resolve() if a.fence else lane / FENCE_REL
    work = pathlib.Path(tempfile.mkdtemp(prefix="k50-c1-", dir=a.work))
    ok = True

    def say(line):
        print(line)

    try:
        rev = subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"], capture_output=True, text=True)
        rev = rev.stdout.strip() if rev.returncode == 0 else "unknown"
        dirty = subprocess.run(["git", "-C", str(lane), "status", "--porcelain"],
                               capture_output=True, text=True).stdout.strip().splitlines()
        say(f"REV {rev}")
        say(f"TREE dirty={len(dirty)}")
        if dirty and not a.allow_dirty:
            ok = False

        pop_path = lane / POP_REL
        pop_sha = sha256_file(pop_path)
        rows = parse_population(pop_path)
        say(f"FENCE {fence_path} sha256={sha256_file(fence_path)}")

        hb = load(lane / BUILDER_REL, "k50_honest")
        hb.ALLOW_NO_REPO = True          # hostile legs include fixtures with no repository under d (f6_above)
        k44 = load(lane / K44_REL, "k50_k44")
        modules = []
        seen = set()
        for r in rows:
            if r["module"] in seen:
                continue
            seen.add(r["module"])
            modules.append((module_path(lane, r["module"]), r["module"].replace("/", "-")[:-3]))
        honest, failures = build_all(hb, k44, modules, work / "honest")
        by_fid = {f["fid"]: f for f in honest}
        mismatched = [r["fid"] for r in rows
                      if r["fid"] not in by_fid or hb.tree_identity(by_fid[r["fid"]]["dir"])[0] != r["tree"]]
        say(f"POPULATION fixtures={len(rows)} pin={pop_sha} mismatched={len(mismatched)} build_errors={len(failures)}")
        if len(rows) != HONEST_TOTAL or pop_sha != POPULATION_SHA or mismatched or failures:
            ok = False
            for fid in mismatched[:8]:
                say(f"POPULATION-MISMATCH {fid}")
            for e in failures[:8]:
                say(f"BUILD-ERROR {e}")

        fence = load(fence_path, "k50_fence")
        honest_v = verdicts(fence, honest)
        refused = [x for x in honest_v if x["v"] != "ADMIT"]
        say(f"HONEST fixtures={len(honest_v)} admitted={len(honest_v) - len(refused)} "
            f"refused={sum(1 for x in refused if x['v'] == 'BREACH')} "
            f"error={sum(1 for x in refused if x['v'] == 'ERROR')}")
        if refused:
            ok = False
            for x in refused[:12]:
                say(f"HONEST-REFUSED {x['fid']} {x['why']}")

        hostile = []
        for rel in (REFUSALS_REL, *SEALED_RELS):
            d = lane / rel
            if not d.is_dir():
                continue
            hostile.append((rel, sorted(d.glob("*.py"))))
        hostile_built = []
        for rel, files in hostile:
            fixtures, fails = build_all(hb, k44, [(f, f"{rel.split('/')[-1]}-{f.stem}") for f in files],
                                        work / rel.replace("/", "-"))
            hostile_built.append((rel, files, fixtures, fails))

        def fids_of(f, fixtures):
            return {x["fid"] for x in fixtures if x["module"] == str(f)}

        def leg(rel, files, fixtures, fails):
            label = "REFUSALS" if rel == REFUSALS_REL else "SEALED"
            v = verdicts(fence, fixtures)
            leaked = [x for x in v if x["v"] == "ADMIT"]
            clean = sum(1 for f in files
                        if fids_of(f, fixtures)
                        and all(x["v"] == "BREACH" for x in v if x["fid"] in fids_of(f, fixtures)))
            say(f"{label} total={len(files)} clean={clean} leaked={len(leaked)} build_errors={len(fails)}")
            for e in fails[:8]:
                say(f"{label}-BUILD-ERROR {e}")
            if clean != len(files):
                for f in files:
                    miss = [x for x in v if x["fid"] in fids_of(f, fixtures) and x["v"] != "BREACH"]
                    for x in miss[:2]:
                        say(f"{label}-MISS {f.name} {x['fid']} {x['v']} {x['why']}")
            return clean, len(leaked), len(fails), v

        reference = list(honest_v)
        for rel, files, fixtures, fails in hostile_built:
            clean, leaked, nfail, v = leg(rel, files, fixtures, fails)
            reference += v
            if clean != len(files) or leaked or nfail:
                ok = False
        if (lane / REFUSALS_REL).is_dir():
            n = len(sorted((lane / REFUSALS_REL).glob("*.py")))
            if n != REFUSALS_TOTAL:
                say(f"REFUSALS-TOTAL {n} expected={REFUSALS_TOTAL}")
                ok = False
        if (lane / "plans/sealed50").is_dir():
            n = len(sorted((lane / "plans/sealed50").glob("*.py")))
            if n < SEALED50_MIN:
                say(f"SEALED50-TOTAL {n} expected_min={SEALED50_MIN}")
                ok = False

        if not a.skip_mutants:
            spec = json.loads((lane / MUTANTS_REL).read_text())
            mutants = spec["mutants"] if isinstance(spec, dict) else spec
            caught = broken = 0
            ref_vec = [(x["fid"], x["v"]) for x in reference]
            for m in mutants:
                dest = work / "mutants" / f"{m['id']}.py"
                path, why = apply_mutant(fence_path, m["payload"], dest)
                if path is None:
                    broken += 1
                    say(f"MUTANT broken {m['id']} {why}")
                    continue
                mod = load(path, f"k50_mut_{m['id'].replace('-', '_')}")
                mv = verdicts(mod, honest)
                for _rel, _files, fixtures, _fails in hostile_built:
                    mv += verdicts(mod, fixtures)
                if [(x["fid"], x["v"]) for x in mv] != ref_vec:
                    caught += 1
                else:
                    say(f"MUTANT survived {m['id']}")
            say(f"MUTANTS total={len(mutants)} caught={caught} broken={broken} floor={MUTANT_MIN} "
                f"verdict={'met' if caught >= MUTANT_MIN and len(mutants) >= MUTANT_MIN else 'unmet'}")
            if caught < MUTANT_MIN or len(mutants) < MUTANT_MIN:
                ok = False

        say(f"PREDICATE R50-C1 {'pass' if ok else 'fail'}")
        return 0 if ok else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

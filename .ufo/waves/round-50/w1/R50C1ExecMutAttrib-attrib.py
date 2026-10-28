#!/usr/bin/env python3
"""Kill attribution for the round-50 C1 mutant battery, witnessed on a chosen fixture-set ordering.

Reuses the frozen counter's own machinery (plans/round50_c1_verify.py imported as a module: parse_population,
build_all, verdicts, apply_mutant, module_path) so the verdicts are the counter's verdicts. The ONLY differences
from the counter's mutant leg are (a) the fixture list is iterated in a caller-chosen order, and (b) every
per-fixture verdict change is recorded instead of only a caught/not-caught bit.

Usage: attrib.py --lane LANE --fence FENCE --mutants JSON --work DIR --order pinned|reverse|shuffle:N --out JSON
"""
import argparse
import hashlib
import importlib.util
import json
import pathlib
import random
import sys

SEALED_RELS = ("plans/sealed46", "plans/sealed50")
REFUSALS_REL = "plans/refusals46"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ordered_rows(rows, order):
    rows = list(rows)
    if order == "pinned":
        return rows
    if order == "reverse":
        return rows[::-1]
    if order.startswith("shuffle:"):
        seed = int(order.split(":", 1)[1])
        random.Random(seed).shuffle(rows)
        return rows
    raise SystemExit(f"bad --order {order}")


def build(lane, work, order):
    cv = load(lane / "plans/round50_c1_verify.py", "k50_counter")
    rows = ordered_rows(cv.parse_population(lane / "plans/honest50/population.txt"), order)
    hb = load(lane / "plans/honest50/build_honest_population.py", "k50_honest")
    hb.ALLOW_NO_REPO = True                      # the counter's own setting for the hostile legs
    k44 = load(lane / "plans/round44_c1_verify.py", "k50_k44")

    modules, seen = [], set()
    for r in rows:                                # dedupe in the CHOSEN order
        if r["module"] in seen:
            continue
        seen.add(r["module"])
        modules.append((cv.module_path(lane, r["module"]), r["module"].replace("/", "-")[:-3]))
    honest, fail_h = cv.build_all(hb, k44, modules, work / "honest")

    hostile = []
    for rel in (REFUSALS_REL, *SEALED_RELS):
        d = lane / rel
        if not d.is_dir():
            continue
        files = sorted(d.glob("*.py"))
        fixtures, fails = cv.build_all(hb, k44, [(f, f"{rel.split('/')[-1]}-{f.stem}") for f in files],
                                       work / rel.replace("/", "-"))
        hostile.append({"rel": rel, "files": [f.name for f in files], "fixtures": fixtures, "fails": fails})
    return cv, rows, honest, fail_h, hostile


def sweep(cv, fence_mod, honest, hostile):
    """Verdict vector in the built order; one entry per fid."""
    v = cv.verdicts(fence_mod, honest)
    per_leg = []
    for h in hostile:
        leg = cv.verdicts(fence_mod, h["fixtures"])
        per_leg.append(leg)
        v += leg
    return v


def vec_digest(v):
    h = hashlib.sha256()
    for fid, val in sorted((x["fid"], x["v"]) for x in v):
        h.update(f"{fid}\t{val}\n".encode())
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--fence", required=True)
    ap.add_argument("--mutants", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--order", default="pinned")
    ap.add_argument("--out", required=True)
    ap.add_argument("--expect-fence-sha", default=None,
                    help="refuse to measure unless the fence has exactly this sha256 (moving-target guard)")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    fence_path = pathlib.Path(a.fence).resolve()
    work = pathlib.Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    cv0 = load(lane / "plans/round50_c1_verify.py", "k50_counter_sha")
    sha_before = cv0.sha256_file(fence_path)
    if a.expect_fence_sha and sha_before != a.expect_fence_sha:
        print(f"FENCE-UNEXPECTED {sha_before} expected={a.expect_fence_sha}", file=sys.stderr)
        return 3

    cv, rows, honest, fail_h, hostile = build(lane, work, a.order)
    fence = load(fence_path, "k50_fence_ref")
    ref = sweep(cv, fence, honest, hostile)
    ref_by_fid = {x["fid"]: x["v"] for x in ref}

    spec = json.loads(pathlib.Path(a.mutants).read_text())
    mutants = spec["mutants"] if isinstance(spec, dict) else spec
    sha_after = cv.sha256_file(fence_path)
    if sha_after != sha_before:
        print(f"FENCE-MOVED {sha_before} -> {sha_after}", file=sys.stderr)
        return 4
    report = {"order": a.order, "work": str(work), "fence_sha256": sha_before,
              "population_rows": len(rows), "honest_built": len(honest), "honest_build_failures": fail_h,
              "hostile": [{"rel": h["rel"], "files": len(h["files"]), "built": len(h["fixtures"]),
                           "fails": h["fails"]} for h in hostile],
              "ref_digest": vec_digest(ref), "ref_refused": [x["fid"] for x in ref if x["v"] != "ADMIT"],
              "fid_order": [x["fid"] for x in ref], "rows": []}
    for m in mutants:
        dest = work / "mutants" / f"{m['id']}.py"
        path, why = cv.apply_mutant(fence_path, m["payload"], dest)
        if path is None:
            report["rows"].append({"id": m["id"], "applies": False, "why": why, "changed": []})
            continue
        mod = load(path, f"k50_mut_{m['id'].replace('-', '_')}")
        got = sweep(cv, mod, honest, hostile)
        changed = [{"fid": x["fid"], "old": ref_by_fid.get(x["fid"]), "new": x["v"], "why_new": x["why"]}
                   for x in got if x["v"] != ref_by_fid.get(x["fid"])]
        report["rows"].append({"id": m["id"], "applies": True, "sha256": cv.sha256_file(path),
                               "changed": changed, "caught": bool(changed)})
    pathlib.Path(a.out).write_text(json.dumps(report, indent=1) + "\n")
    print(f"ORDER {a.order} work={work} ref_digest={report['ref_digest']} rows={len(report['rows'])} "
          f"applies={sum(1 for r in report['rows'] if r['applies'])} "
          f"caught={sum(1 for r in report['rows'] if r.get('caught'))}")


if __name__ == "__main__":
    sys.exit(main())

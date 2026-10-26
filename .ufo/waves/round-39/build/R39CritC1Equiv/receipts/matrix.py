#!/usr/bin/env python3
"""Pair matrix: reference gate vs each frozen M01..M07 copy over the frozen 86-fixture battery.

Usage: matrix.py LANE FIXTURES_JSON OUT_JSON
For every (mutant, fixture) in the mutant's clause family: run reference and mutant, record
(rc, DEFECT set, ok set) both sides, then classify every observable difference into the counter's
four declared directions using the counter's own exhibits() predicate, and count unclassified diffs.
"""
import importlib.util
import json
import pathlib
import sys
from concurrent.futures import ThreadPoolExecutor

LANE = pathlib.Path(sys.argv[1]).resolve()
FX = pathlib.Path(sys.argv[2]).resolve()
OUT = pathlib.Path(sys.argv[3]).resolve()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    c39 = load(LANE / "plans/round39_c1_verify.py", "c39")
    meta = json.loads(FX.read_text())
    spec_path = meta["spec_path"]
    fixtures = meta["fixtures"]
    gdir = OUT.parent / "gates"
    gdir.mkdir(parents=True, exist_ok=True)
    gate_src = (LANE / "plans/pkg_gate.py").read_text()
    ref_gate = gdir / "ref.py"
    ref_gate.write_text(gate_src)
    mutants = {}
    for mid, clause, direction, label, wit, old, new in c39.MUTANTS:
        assert gate_src.count(old) == 1, mid
        mg = gdir / f"{mid}.py"
        mg.write_text(gate_src.replace(old, new, 1))
        compile(mg.read_text(), str(mg), "exec")
        mutants[mid] = (clause, direction, label, wit, mg)

    jobs = [(mid, fx) for mid in mutants for fx in fixtures if c39.family_ok(mutants[mid][0], fx["argv"])]

    def run(job):
        mid, fx = job
        ref = c39.run_gate(ref_gate, spec_path, fx["argv"])
        mut = c39.run_gate(mutants[mid][4], spec_path, fx["argv"])
        return mid, fx["fid"], ref, mut

    res = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        for mid, fid, ref, mut in ex.map(run, jobs):
            res.setdefault(mid, []).append({"fid": fid, "ref": [ref[0], sorted(ref[1]), sorted(ref[2])],
                                            "mut": [mut[0], sorted(mut[1]), sorted(mut[2])]})
    fxmap = {f["fid"]: f for f in fixtures}
    report = {}
    for mid, (clause, direction, label, wit, _mg) in mutants.items():
        rows = sorted(res[mid], key=lambda r: r["fid"])
        flips, direction_hits, unclassified = [], {d: [] for d in c39.DIRECTIONS}, []
        for r in rows:
            fx = fxmap[r["fid"]]
            ref = (r["ref"][0], frozenset(r["ref"][1]), frozenset(r["ref"][2]))
            mut = (r["mut"][0], frozenset(r["mut"][1]), frozenset(r["mut"][2]))
            if ref == mut:
                continue
            hits = [d for d in c39.DIRECTIONS if c39.exhibits(clause, d, fx, ref, mut)]
            for d in hits:
                direction_hits[d].append(r["fid"])
            flips.append({"fid": r["fid"], "ref": r["ref"], "mut": r["mut"], "directions": hits})
            if not hits:
                unclassified.append(r["fid"])
        report[mid] = {"clause": clause, "direction": direction, "fixtures": len(rows),
                       "differences": len(flips), "direction_hits": {d: v for d, v in direction_hits.items() if v},
                       "declared_reachable_by": direction_hits[direction],
                       "unclassified": unclassified, "flips": flips}
        print(f"{mid} {clause} {direction} fixtures={len(rows)} differences={len(flips)} "
              f"declared_by={direction_hits[direction][:3]} other_dirs="
              f"{ {d: v[:3] for d, v in direction_hits.items() if d != direction and v} } "
              f"unclassified={unclassified[:3]}")
    OUT.write_text(json.dumps(report, indent=1))
    print("WROTE", OUT)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""F37XMutD4: four new (non-frozen) mutants of the gate's D4 clause, run against the full round-37
battery with the counter's own machinery (round37_c1_verify imported as a module).

Each mutant is an exact old -> new pair that occurs exactly once in the frozen gate
(sha256 ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41). Fixtures are built once
with counter.r36_fixtures + counter.battery37_fixtures, the reference gate is run on every fixture,
then each mutant gate is run on the same fixture argv; a mutant is killed when any fixture's
(returncode, DEFECT-clause set) differs from the reference. No lane file is touched: all work happens
in the caller's --work scratch dir.
"""
from __future__ import annotations

import argparse
import importlib.util
import pathlib
import py_compile
import shutil
import sys
import tempfile

D4_COUNT_OLD = 'if len(lines) != 1 or not lines[0].startswith(spec["d4"]["label"]):'

MUTANTS = [
    ("X1", "count off-by-one: a two-line file passes (len > 2 instead of len != 1)",
     D4_COUNT_OLD,
     'if len(lines) > 2 or not lines[0].startswith(spec["d4"]["label"]):'),
    ("X2", "branch reordered as a conjunction: the label check shadows the count check",
     D4_COUNT_OLD,
     'if not lines[0].startswith(spec["d4"]["label"]) and len(lines) != 1:'),
    ("X3", "last directional pattern unchecked (patterns[:-1])",
     'enumerate(spec["d4"]["patterns"], 1)',
     'enumerate(spec["d4"]["patterns"][:-1], 1)'),
    ("X4", "directional pattern regex loosened to case-insensitive",
     'if not re.search(pat, lines[0])]',
     'if not re.search(pat, lines[0], re.IGNORECASE)]'),
]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    c1 = load(lane / "plans/round37_c1_verify.py", "k37_c1_mod")
    gate_src = (lane / "plans/pkg_gate.py").read_text()
    gate_sha = c1.sha256(lane / "plans/pkg_gate.py")
    print(f"GATE plans/pkg_gate.py sha256={gate_sha} frozen={gate_sha == c1.GATE_SHA256}")
    if gate_sha != c1.GATE_SHA256:
        print("SETUP gate is not at the freeze digest", file=sys.stderr)
        return 2
    r36 = c1.load_r36(lane)
    ctx = c1.Ctx(lane, r36)
    fixtures = c1.r36_fixtures(r36) + c1.battery37_fixtures(lane / "plans/battery37")
    print(f"BATTERY fixtures={len(fixtures)}")

    root = pathlib.Path(tempfile.mkdtemp(prefix="d4mut-", dir=a.work))
    try:
        built = []
        for i, fx in enumerate(fixtures):
            d = root / "fx" / f"f{i:03d}"
            d.mkdir(parents=True)
            argv = list(fx["build"](ctx, d))
            if "--spec" in argv or not argv or argv[0] not in ("package", "d4-line", "d5-line"):
                print(f"SETUP fixture {fx['fid']} returned a forbidden argv", file=sys.stderr)
                return 2
            built.append((fx, d, argv))

        gdir = root / "gates"
        gdir.mkdir()
        ref_gate = gdir / "ref.py"
        ref_gate.write_text(gate_src)
        ref, wrong = [], 0
        for fx, d, argv in built:
            res = c1.run_gate(ref_gate, ctx.spec_path, argv)
            ref.append(res)
            want_rc = 0 if fx["expect"] == "accept" else 1
            declared = fx.get("defects")
            ok = res[0] == want_rc and (declared is None or res[1] == frozenset(declared))
            if fx["expect"] == "accept":
                ok = ok and not res[1]
            wrong += not ok
            if not ok:
                print(f"REFERENCE-WRONG {fx['fid']} rc={res[0]} defects={sorted(res[1])}")
        print(f"REFERENCE wrong={wrong}")

        # d4-specific isolation check: the note each d4 fixture provokes on the unmodified gate.
        for fx, d, argv in built:
            if fx["fid"].startswith("d4-"):
                out = c1.subprocess.run([sys.executable, str(ref_gate), *argv, "--spec", str(ctx.spec_path)],
                                        capture_output=True, text=True).stdout.strip().splitlines()
                print(f"D4FIXTURE {fx['fid']} note={' | '.join(out)}")

        killed = 0
        for mid, label, old, new in MUTANTS:
            if gate_src.count(old) != 1:
                print(f"MUTANT {mid} INVALID old occurs {gate_src.count(old)} times -- {label}")
                continue
            mg = gdir / f"{mid}.py"
            mg.write_text(gate_src.replace(old, new, 1))
            try:
                py_compile.compile(str(mg), doraise=True, cfile=str(gdir / f"{mid}.pyc"))
            except py_compile.PyCompileError as e:
                print(f"MUTANT {mid} INVALID compile -- {e}")
                continue
            by = None
            for j, (fx, d, argv) in enumerate(built):
                if c1.run_gate(mg, ctx.spec_path, argv) != ref[j]:
                    by = fx["fid"]
                    break
            if by:
                killed += 1
                print(f"MUTANT {mid} killed by={by} -- {label}")
            else:
                print(f"MUTANT {mid} SURVIVED -- {label}")
        print(f"EXTRA-MUTANTS total={len(MUTANTS)} killed={killed} survived={len(MUTANTS) - killed}")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""F37XMutD5 harness: extra (non-frozen) mutants of clause D5 of plans/pkg_gate.py, measured against
the full round-37 battery.

Reuses the frozen counter's machinery by importing plans/round37_c1_verify.py as a module:
load_r36, Ctx, r36_fixtures, battery37_fixtures, run_gate. Fixtures are built once, exactly as the
counter's main() builds them; then the reference gate and each extra mutant run over every fixture.

Observable result of one gate run = (exit code, set of clause ids printed DEFECT) -- run_gate's
return value, unchanged from the frozen counter -- so kill/survive here means the same thing it means
there. Each mutant is an exact `old -> new` replacement that must occur exactly once in the gate and
must compile, else it is reported INVALID (never counted killed or survived).

  --lane DIR   clean clone of the integration tip (default: this script's scratch clone)
  --work DIR   scratch parent for the built fixtures
  --gate PATH  gate to mutate (default: LANE/plans/pkg_gate.py)
  --notes      also print the reference gate's D5 note line for every d5-line fixture (isolation audit)
"""
import argparse
import importlib.util
import pathlib
import py_compile
import re
import subprocess
import sys
import tempfile
import shutil

GATE_REL = "plans/pkg_gate.py"

# (id, label, old, new) -- every pair must occur exactly once in the gate at the tip.
MUTANTS = [
    ("X1", "manifest row arity off by one (`>= 2` -> `> 2`): a genuine 2-field SHA256SUMS row stops pinning", 
     "any(len(parts) >= 2 and parts[0] == digest", "any(len(parts) > 2 and parts[0] == digest"),
    ("X2", "line-count threshold off by one (`!= 1` -> `> 2`): a two-line erratum still passes the label gate",
     'if len(lines) != 1 or not lines[0].startswith(d5["label"]):',
     'if len(lines) > 2 or not lines[0].startswith(d5["label"]):'),
    ("X3", "manifest pin applied to the first row only (`sums.splitlines()[:1]`)",
     "for parts in (row.split() for row in sums.splitlines()))",
     "for parts in (row.split() for row in sums.splitlines()[:1]))"),
    ("X4", "quote containment loosened to a 20-character prefix of the quote",
     'if re.sub(r"\\s+", "", d5["quote"]) not in flat:',
     'if re.sub(r"\\s+", "", d5["quote"])[:20] not in flat:'),
    ("S1", "branch reordered into an early return: an unpinned digest shadows the later quote check",
     '        if not pinned:\n            bad.append("capture digest is not the one in the manifest")',
     '        if not pinned:\n            return False, "capture digest is not the one in the manifest"'),
    ("S2", "capture tag-strip removed (normalisation dropped, quote check unchanged otherwise)",
     'flat = re.sub(r"\\s+", "", re.sub(r"<[^>]+>", "", read(capture) or ""))',
     'flat = re.sub(r"\\s+", "", read(capture) or "")'),
    ("S3", "capture whitespace removal dropped (tag-strip kept)",
     'flat = re.sub(r"\\s+", "", re.sub(r"<[^>]+>", "", read(capture) or ""))',
     'flat = re.sub(r"<[^>]+>", "", read(capture) or "")'),
]
COUNTED = ("X1", "X2", "X3", "X4")


def load_counter(lane):
    spec = importlib.util.spec_from_file_location("k37_counter", lane / "plans/round37_c1_verify.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_gate_full(gate, spec_path, argv):
    r = subprocess.run([sys.executable, str(gate), *argv, "--spec", str(spec_path)],
                       capture_output=True, text=True, timeout=900)
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--gate", default=None)
    ap.add_argument("--notes", action="store_true")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    gate_path = pathlib.Path(a.gate).resolve() if a.gate else lane / GATE_REL
    c = load_counter(lane)
    gate_src = gate_path.read_text()
    print(f"GATE {gate_path} sha256={c.sha256(gate_path)} frozen={c.sha256(gate_path) == c.GATE_SHA256}")
    r36 = c.load_r36(lane)
    ctx = c.Ctx(lane, r36)
    fixtures = c.r36_fixtures(r36) + c.battery37_fixtures(lane / c.BATTERY_REL)
    root = pathlib.Path(tempfile.mkdtemp(prefix="k37-d5mut-", dir=a.work))
    try:
        built = []
        ids = [f["fid"] for f in fixtures]
        assert len(set(ids)) == len(ids), "duplicate fixture id"
        for i, fx in enumerate(fixtures):
            d = root / "fx" / f"f{i:03d}"
            d.mkdir(parents=True)
            argv = list(fx["build"](ctx, d))
            assert argv and argv[0] in ("package", "d4-line", "d5-line") and "--spec" not in argv, fx["fid"]
            built.append((fx, d, argv))
        gdir = root / "gates"
        gdir.mkdir()
        ref_gate = gdir / "ref.py"
        ref_gate.write_text(gate_src)
        ref = [c.run_gate(ref_gate, ctx.spec_path, argv) for _fx, _d, argv in built]
        print(f"FIXTURES built={len(built)} reference_accepts="
              f"{[fx['fid'] for (fx, _d, _a), r in zip(built, ref) if r[0] == 0]}")
        def declared_ok(fx, r):
            want_rc = 0 if fx["expect"] == "accept" else 1
            if r[0] != want_rc:
                return False
            if fx.get("defects") is not None and r[1] != frozenset(fx["defects"]):
                return False
            return not (fx["expect"] == "accept" and r[1])

        wrong = sum(1 for (fx, _d, _a), r in zip(built, ref) if not declared_ok(fx, r))
        print(f"REFERENCE wrong={wrong} (fixtures whose observed result misses their declaration)")
        if a.notes:
            for (fx, _d, argv), r in zip(built, ref):
                if argv[0] != "d5-line":
                    continue
                out = run_gate_full(ref_gate, ctx.spec_path, argv).stdout.strip().splitlines()
                line = next((l for l in out if re.match(r"^D5 ", l)), "<no D5 line>")
                print(f"NOTE {fx['fid']} rc={r[0]} :: {line}")
        killed = survived = invalid = 0
        for mid, label, old, new in MUTANTS:
            if gate_src.count(old) != 1:
                invalid += 1
                print(f"EXTRA {mid} INVALID occurrences={gate_src.count(old)} -- {label}")
                continue
            mg = gdir / f"{mid}.py"
            mg.write_text(gate_src.replace(old, new, 1))
            try:
                py_compile.compile(str(mg), doraise=True, cfile=str(gdir / f"{mid}.pyc"))
            except py_compile.PyCompileError as e:
                invalid += 1
                print(f"EXTRA {mid} INVALID compile={e} -- {label}")
                continue
            diffs = [fx["fid"] for (fx, _d, argv), r in zip(built, ref)
                     if c.run_gate(mg, ctx.spec_path, argv) != r]
            if diffs:
                killed += 1
                print(f"EXTRA {mid} KILLED by={diffs[0]} differing={len(diffs)}/{len(built)} -- {label}")
                print(f"      all={','.join(diffs)}")
            else:
                survived += 1
                print(f"EXTRA {mid} SURVIVED differing=0/{len(built)} -- {label}")
        print(f"EXTRA total={len(MUTANTS)} counted={len(COUNTED)} killed={killed} survived={survived} invalid={invalid}")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

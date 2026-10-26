#!/usr/bin/env python3
"""R38BatD5 receipt driver: direct gate-vs-mutant evidence for D5 mutants N21 and N22.

Run with the lane clone as argv[1] and a scratch work dir as argv[2].  Prints, for every probe:

  * the reference gate's and the mutant gate's rc + clause lines on the seat fixture (the kill proof);
  * a manifest-shape matrix for N21 (the monotonicity table: mutant defect set is a superset);
  * the differing-fixture table for both mutants over the whole round-36 + battery37 + d5m battery.
"""
from __future__ import annotations

import importlib.util
import pathlib
import subprocess
import sys

LANE = pathlib.Path(sys.argv[1]).resolve()
WORK = pathlib.Path(sys.argv[2]).resolve()
SEAT = pathlib.Path(__file__).resolve().parent
BATTERY = SEAT / "battery"

if WORK.exists():
    import shutil as _wipe
    _wipe.rmtree(WORK)
WORK.mkdir(parents=True)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


r37 = load(LANE / "plans/round37_c1_verify.py", "kengaku_r37_c1")
r38 = load(LANE / "plans/round38_c1_verify.py", "kengaku_r38_c1")
r36 = r37.load_r36(LANE)
ctx = r37.Ctx(LANE, r36)
BDIR = pathlib.Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else BATTERY
if (BDIR / "d5m.py").is_file():
    d5m = load(BDIR / "d5m.py", "kengaku_b38_d5m")
else:
    import types
    d5m = types.SimpleNamespace(FIXTURES=[])

GATE_SRC = (LANE / "plans/pkg_gate.py").read_text()
MUT = {mid: (clause, old, new) for mid, clause, _dir, _label, old, new in r38.MUTANTS}


def gate_copy(tag, mid=None):
    p = WORK / f"gate-{tag}.py"
    src = GATE_SRC if mid is None else GATE_SRC.replace(*MUT[mid][1:], 1)
    p.write_text(src)
    return p


def run(gate, argv):
    full = [sys.executable, str(gate), *argv, "--spec", str(ctx.spec_path)]
    r = subprocess.run(full, capture_output=True, text=True, timeout=900)
    lines = [l for l in r.stdout.splitlines() if l[:1] in "PD" and (" ok " in l or " DEFECT " in l)]
    return r.returncode, lines, r.stdout, r.stderr


def verdict(tag, rc, lines):
    clause = [l.split()[0] for l in lines]
    return f"rc={rc} {','.join(clause) or 'silent'}"


def build_fx(fx, sub):
    d = WORK / sub
    if d.exists():
        import shutil
        shutil.rmtree(d)
    d.mkdir(parents=True)
    return d, list(fx["build"](ctx, d))


print("== seat fixtures: reference vs mutant (direct stdout) ==")
ref = gate_copy("ref")
gates = {"ref": ref, "N21": gate_copy("N21", "N21"), "N22": gate_copy("N22", "N22")}
for fx in d5m.FIXTURES:
    d, argv = build_fx(fx, "fx-" + fx["fid"])
    print(f"\n-- {fx['fid']} expect={fx['expect']} declared={fx['defects']} argv={argv[0]} {argv[1]}")
    for tag, g in gates.items():
        rc, lines, out, err = run(g, argv)
        print(f"   {tag:3s} {verdict(tag, rc, lines)}")
        for l in out.splitlines():
            print(f"        | {l}")
        if err.strip():
            print(f"        ! {err.strip()}")

print("\n== N21 manifest-shape matrix (same capture, same erratum line) ==")
capdir0, cap0 = d5m._captures(ctx, WORK / "mat-base")
digest = __import__("hashlib").sha256(cap0.read_bytes()).hexdigest()
name = cap0.name
shapes = [
    ("genuine-row-1", [(digest, name)]),
    ("decoy-1-genuine-2", [("0" * 64, "geniac-s105-reopen.html"), (digest, name)]),
    ("genuine-1-decoy-2", [(digest, name), ("0" * 64, "geniac-s105-reopen.html")]),
    ("blank-genuine-2", [("", ""), (digest, name)]),
    ("genuine-2-only-empty-line-1", [("", ""), (digest, name)]),
    ("decoy-only", [("0" * 64, "geniac-s105-reopen.html")]),
    ("empty-manifest", []),
    ("genuine-wrong-suffix", [(digest, "captures/nec-s091.html")]),
]
print(f"{'shape':30s} {'reference':16s} {'N21':16s} {'N22':16s} superset")
for tag, rows in shapes:
    d = WORK / ("mat-" + tag)
    if d.exists():
        import shutil
        shutil.rmtree(d)
    d.mkdir(parents=True)
    capdir = d / "captures"
    import shutil as _sh
    _sh.copytree(ctx.d5_capture_dir(), capdir)
    d5m._write_manifest(ctx, capdir, rows)
    argv = d5m._argv(ctx, d, capdir)
    res = {}
    for gtag, g in gates.items():
        rc, lines, _o, _e = run(g, argv)
        res[gtag] = (rc, {l.split()[0] for l in lines if " DEFECT " in l})
    sup = res["N21"][1] >= res["ref"][1]
    cells = {k: f"rc={v[0]} D={','.join(sorted(v[1])) or '-'}" for k, v in res.items()}
    print(f"{tag:30s} {cells['ref']:16s} {cells['N21']:16s} {cells['N22']:16s} superset={sup}")

print("\n== differing fixtures over the whole battery (round-36 + battery37 + d5m) ==")
fixtures = r37.r36_fixtures(r36) + r37.battery37_fixtures(LANE / r37.BATTERY_REL)
fixtures += [{**fx, "b38": True} for fx in d5m.FIXTURES]
base = WORK / "all"
if base.exists():
    import shutil
    shutil.rmtree(base)
base.mkdir(parents=True)
built = []
for i, fx in enumerate(fixtures):
    d = base / f"f{i:03d}"
    d.mkdir()
    built.append((fx, list(fx["build"](ctx, d))))
for mid in ("N21", "N22"):
    diff = []
    for fx, argv in built:
        if argv[0] != "d5-line":
            continue
        a = run(ref, argv)
        b = run(gates[mid], argv)
        if (a[0], a[1]) != (b[0], b[1]):
            diff.append((fx["fid"], verdict("r", a[0], a[1]), verdict("m", b[0], b[1])))
    print(f"{mid} differing={len(diff)}/{sum(1 for fx, a in built if a[0] == 'd5-line')} d5-line fixtures")
    for fid, ra, rb in diff:
        print(f"   {fid}: ref {ra} | mutant {rb}")

print("\n== counter predicate applied to the seat fixtures (both direction cells) ==")
for fx, argv in built:
    if not fx["fid"].startswith("d5m-"):
        continue
    a = run(ref, argv)
    for mid in ("N21", "N22"):
        b = run(gates[mid], argv)
        ra = (a[0], frozenset(l.split()[0] for l in a[1] if " DEFECT " in l), frozenset(l.split()[0] for l in a[1] if " ok " in l))
        rb = (b[0], frozenset(l.split()[0] for l in b[1] if " DEFECT " in l), frozenset(l.split()[0] for l in b[1] if " ok " in l))
        cells = {d: r38.attributed("D5", d, fx, argv, ra, rb) for d in ("silence", "mirror")}
        print(f"   {fx['fid']:24s} vs {mid}: silence={cells['silence']} mirror={cells['mirror']}")

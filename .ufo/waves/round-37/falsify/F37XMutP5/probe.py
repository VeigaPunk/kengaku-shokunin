#!/usr/bin/env python3
"""F37XMutP5 witness probes for the two survivors of harness.py.

A: X1 witness — the same mutation on a NON-first registry row (S107/instruction.md): reference rejects,
   X1 accepts, so X1 is a live P5 defect that the battery cannot see because both row fixtures pin
   `sorted(rows)[0]` (S105).
B: X4 witness — the p5-row-capture-unpinned fixture under the reference and under X4: same exit code and
   same clause set, different P5 reason => the survivor is an observable limit, not a no-op mutation.
C: supplementary (NOT one of the four): `sorted(capdir.iterdir())[:-1]` — the sweep skipping its last entry.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import pathlib
import py_compile
import subprocess
import sys
import tempfile

LANE = pathlib.Path(sys.argv[1]).resolve()
WORK = pathlib.Path(sys.argv[2]).resolve()
BDIR = pathlib.Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else None
GATE_REL = "plans/pkg_gate.py"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


c1 = load(LANE / "plans/round37_c1_verify.py", "kengaku_r37_c1")
gate_src = (LANE / GATE_REL).read_text()

MUT = {
    "X1": ('    for sid, row in p.spec["rows"].items():\n'
           '        name = row["capture"]\n'
           '        if name not in pinned:',
           '    for sid, row in list(p.spec["rows"].items())[:1]:\n'
           '        name = row["capture"]\n'
           '        if name not in pinned:'),
    "X4": ('        if name not in pinned:\n'
           '            bad.append(f"{sid}: capture {name} is not pinned in the manifest")\n'
           '        elif pinned[name] != row["sha256"]:\n'
           '            bad.append(f"{sid}: manifest digest differs from the spec pin")',
           '        if pinned.get(name) != row["sha256"]:\n'
           '            bad.append(f"{sid}: manifest digest differs from the spec pin")\n'
           '        elif name not in pinned:\n'
           '            bad.append(f"{sid}: capture {name} is not pinned in the manifest")'),
    "X3": ("    for f in sorted(capdir.iterdir()):",
           "    for f in sorted(capdir.iterdir())[:1]:"),
    "X3b": ("    for f in sorted(capdir.iterdir()):",
            "    for f in sorted(capdir.iterdir())[:-1]:"),
}


def p5_note(stdout):
    for line in stdout.splitlines():
        if line.startswith("P5 "):
            return line
    return None


def run(gate, spec_path, argv):
    r = subprocess.run([sys.executable, str(gate), *argv, "--spec", str(spec_path)],
                       capture_output=True, text=True, timeout=900)
    bad = sorted({l.split()[0] for l in r.stdout.splitlines()
                  if len(l.split()) > 1 and l.split()[0].startswith("P") and l.split()[1] == "DEFECT"})
    return {"rc": r.returncode, "defects": bad, "p5": p5_note(r.stdout)}


root = pathlib.Path(tempfile.mkdtemp(prefix="k37-mutp5-probe-", dir=WORK))
try:
    gdir = root / "gates"
    gdir.mkdir()
    ref = gdir / "ref.py"
    ref.write_text(gate_src)
    gates = {"ref": ref}
    for mid, (old, new) in MUT.items():
        assert gate_src.count(old) == 1, (mid, gate_src.count(old))
        g = gdir / f"{mid}.py"
        g.write_text(gate_src.replace(old, new, 1))
        py_compile.compile(str(g), doraise=True, cfile=str(gdir / f"{mid}.pyc"))
        gates[mid] = g

    r36 = c1.load_r36(LANE)
    ctx = c1.Ctx(LANE, r36)
    out = {}

    # A: off-pin digest on the LAST registry row (S107/instruction.md), bytes moved with the pin.
    sid = sorted(ctx.spec["rows"])[-1]
    cap = ctx.spec["rows"][sid]["capture"]
    d = root / "A"
    ctx.genuine_package(d)
    capdir = d / ctx.spec["capture_dir"]
    path = capdir / cap
    path.write_text(path.read_text() + "# line appended by the F37XMutP5 X1 witness\n")
    moved = hashlib.sha256(path.read_bytes()).hexdigest()
    mpath = capdir / "SHA256SUMS"
    lines = []
    for line in mpath.read_text().splitlines():
        if line.strip() and line.split()[-1] == cap:
            line = f"{moved}  {cap}"
        lines.append(line)
    mpath.write_text("\n".join(lines) + "\n")
    ctx.git_add(d)
    argv = ["package", "--root", str(d), "--require-clean-tree"]
    out["A_row_" + sid] = {k: run(v, ctx.spec_path, argv) for k, v in gates.items() if k in ("ref", "X1")}

    # B: the battery's own p5-row-capture-unpinned fixture under ref vs X4.
    fx = next(f for f in c1.battery37_fixtures(BDIR or (LANE / c1.BATTERY_REL)) if f["fid"] == "p5-row-capture-unpinned")
    d = root / "B"
    d.mkdir()
    argv = list(fx["build"](ctx, d))
    out["B_row_capture_unpinned"] = {k: run(v, ctx.spec_path, argv) for k, v in gates.items() if k in ("ref", "X4")}

    # C: supplementary sweep[:-1] over the two fixtures that probe coverage.
    names = [f["fid"] for f in c1.battery37_fixtures(BDIR or (LANE / c1.BATTERY_REL))]
    for fid in ("p5-extra-capture-file",):
        fx = next(f for f in c1.battery37_fixtures(BDIR or (LANE / c1.BATTERY_REL)) if f["fid"] == fid)
        d = root / ("C_" + fid)
        d.mkdir()
        argv = list(fx["build"](ctx, d))
        out["C_" + fid] = {k: run(v, ctx.spec_path, argv) for k, v in gates.items() if k in ("ref", "X3b", "X3")}

    print(json.dumps(out, indent=1))
finally:
    print("WORK " + str(root))

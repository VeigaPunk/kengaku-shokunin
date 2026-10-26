"""F38RevBatA evidence driver: rebuild each fixture dir exactly as round38_c1_verify.py does
(same r37.Ctx, same build()), then run the reference gate and the frozen mutant on the same
argv and print rc/stdout/stderr. Usage: driver.py LANE WORKDIR

Run against the F38RevBatA scratch clone at 8c7422d7a646515d80af44844e8ecc8a1fc1d30a after
restoring plans/battery38/{b1run,mainx}.py to their landed bytes (sha256 verified against the
fleet tree before the run). Kept as the receipt for ref-vs-mutant-evidence.txt.
"""
import importlib.util
import pathlib
import subprocess
import sys
import tempfile

LANE = pathlib.Path(sys.argv[1]).resolve()
WORK = pathlib.Path(sys.argv[2])


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


r37 = load(LANE / "plans/round37_c1_verify.py", "r37c")
r36 = r37.load_r36(LANE)
ctx = r37.Ctx(LANE, r36)
gate_src = (LANE / "plans/pkg_gate.py").read_text()

MUT = {
    "N01": ('return bool(pins) and not bad, f"pinned=', 'return not bad, f"pinned='),
    "N16": ('ok, note = False, f"clause error', 'ok, note = True, f"clause error'),
    "N17": ("            if not args.root.is_dir():", "            if False:"),
    "N18": ('        print(f"setup: {type(e).__name__}: {e}", file=sys.stderr)\n        return 2',
            '        print(f"setup: {type(e).__name__}: {e}", file=sys.stderr)\n        return 0'),
}

b1 = load(LANE / "plans/battery38/b1run.py", "b1")
mx = load(LANE / "plans/battery38/mainx.py", "mx")
cases = [
    ("N01", "b1run.FIXTURES[0]", b1.FIXTURES[0]),
    ("N16", "b1run.FIXTURES[1]", b1.FIXTURES[1]),
    ("N17", "mainx.FIXTURES[0]", mx.FIXTURES[0]),
    ("N18", "mainx.FIXTURES[1]", mx.FIXTURES[1]),
]

root = pathlib.Path(tempfile.mkdtemp(prefix="ev-", dir=WORK))
gdir = root / "gates"
gdir.mkdir()
for mid, tag, fx in cases:
    assert gate_src.count(MUT[mid][0]) == 1, (mid, "old not unique")
    d = root / fx["fid"]
    d.mkdir()
    argv = list(fx["build"](ctx, d))
    for label, src in (("REF", gate_src), (mid, gate_src.replace(MUT[mid][0], MUT[mid][1], 1))):
        g = gdir / f"{fx['fid']}.{label}.py"
        g.write_text(src)
        full = [sys.executable, str(g), *argv]
        if "--spec" not in argv:
            full += ["--spec", str(ctx.spec_path)]
        r = subprocess.run(full, capture_output=True, text=True, timeout=300)
        print(f"=== {fx['fid']} [{label}] rc={r.returncode}")
        for line in r.stdout.splitlines():
            print(f"  out| {line}")
        for line in r.stderr.splitlines():
            print(f"  err| {line}")
        if not r.stdout.strip() and not r.stderr.strip():
            print("  (no output)")

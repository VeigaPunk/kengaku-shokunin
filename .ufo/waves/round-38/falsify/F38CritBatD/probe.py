import importlib.util, pathlib, sys, tempfile, subprocess

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r38/F38CritBatD")
lane = S / "lane"


def load(p, n):
    sp = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


c = load(lane / "plans/round38_c1_verify.py", "c38")
r37 = load(lane / "plans/round37_c1_verify.py", "r37")
r36 = r37.load_r36(lane)
ctx = r37.Ctx(lane, r36)
fxs = [f for f in c.battery38_fixtures(lane / "plans/battery38")[0]
       if f["fid"].startswith(("p4a", "p4b"))]
root = pathlib.Path(tempfile.mkdtemp(prefix="probe-", dir=str(S)))
built = []
for i, fx in enumerate(fxs):
    d = root / "fx" / f"f{i}"
    d.mkdir(parents=True)
    built.append((fx, d, list(fx["build"](ctx, d))))
gdir = root / "gates"
gdir.mkdir()
gate_src = (lane / "plans/pkg_gate.py").read_text()


def run(gate, argv):
    full = [sys.executable, str(gate), *argv, "--spec", str(ctx.spec_path)]
    r = subprocess.run(full, capture_output=True, text=True, timeout=900)
    bad, ok = set(), set()
    for m in map(c.CLAUSE_LINE.match, r.stdout.splitlines()):
        if m:
            (bad if m.group(2) == "DEFECT" else ok).add(m.group(1))
    p4 = [l for l in r.stdout.splitlines() if l.startswith("P4 ")]
    crash = "Traceback" in r.stdout or "Traceback" in r.stderr
    return (r.returncode, frozenset(bad), frozenset(ok)), p4, crash


ref = gdir / "ref.py"
ref.write_text(gate_src)
refres = [run(ref, argv) for _fx, _d, argv in built]
for (fx, _d, _argv), (res, p4, crash) in zip(built, refres):
    print(f"REF   {fx['fid']:40s} rc={res[0]} rc_defects={sorted(res[1])} p4={p4} crash={crash}")
print()
for mid, clause, direction, label, old, new in c.MUTANTS:
    if mid not in ("N03", "N04", "N05", "N06"):
        continue
    mg = gdir / f"{mid}.py"
    mg.write_text(gate_src.replace(old, new, 1))
    for (fx, _d, argv), rref in zip(built, refres):
        mut, p4, crash = run(mg, argv)
        k = c.attributed(clause, direction, fx, argv, rref[0], mut)
        print(f"{mid}  {fx['fid']:40s} rc={mut[0]} rc_defects={sorted(mut[1])} p4={p4} crash={crash} attributed={k}")
    print()
print("ROOT", root)

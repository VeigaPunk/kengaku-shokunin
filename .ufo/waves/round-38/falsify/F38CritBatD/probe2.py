"""Breadth probe: do the four P4 fixtures cover the *whole* advertised sentence, or only the
mutant's exact boundary? Runs three sibling mutants against the full 86-fixture battery."""
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
fixtures, _side = c.battery38_fixtures(lane / "plans/battery38")
fixtures = r37.r36_fixtures(r36) + r37.battery37_fixtures(lane / r37.BATTERY_REL) + fixtures
root = pathlib.Path(tempfile.mkdtemp(prefix="probe2-", dir=str(S)))
built = []
for i, fx in enumerate(fixtures):
    d = root / "fx" / f"f{i:03d}"
    d.mkdir(parents=True)
    built.append((fx, d, list(fx["build"](ctx, d))))
gdir = root / "gates"
gdir.mkdir()
gsrc = (lane / "plans/pkg_gate.py").read_text()


def run(gate, argv):
    r = subprocess.run([sys.executable, str(gate), *argv, "--spec", str(ctx.spec_path)],
                       capture_output=True, text=True, timeout=900)
    bad, ok = set(), set()
    for m in map(c.CLAUSE_LINE.match, r.stdout.splitlines()):
        if m:
            (bad if m.group(2) == "DEFECT" else ok).add(m.group(1))
    return (r.returncode, frozenset(bad), frozenset(ok))


ref = gdir / "ref.py"
ref.write_text(gsrc)
refres = [run(ref, argv) for _fx, _d, argv in built]
print(f"FIXTURES built={len(built)}")
SIBLINGS = [
    ("X1-skip-last-quote", "for q in p.quotes[:-1]:\n        lines = p.capture(q.capture)"),
    ("X2-last-quote-only", "for q in p.quotes[-1:]:\n        lines = p.capture(q.capture)"),
    ("X3-skip-first-two", "for q in p.quotes[2:]:\n        lines = p.capture(q.capture)"),
    ("X4-first-two-only", "for q in p.quotes[:2]:\n        lines = p.capture(q.capture)"),
]
for name, new in SIBLINGS:
    old = "for q in p.quotes:\n        lines = p.capture(q.capture)"
    assert gsrc.count(old) == 1
    mg = gdir / f"{name}.py"
    mg.write_text(gsrc.replace(old, new, 1))
    hits = []
    for j, (fx, _d, argv) in enumerate(built):
        if argv[0] != "package":
            continue
        if c.attributed("P4", "silence", fx, argv, refres[j], run(mg, argv)):
            hits.append(fx["fid"])
    print(f"{name}: killed_by={hits or 'NONE'}")
print("ROOT", root)

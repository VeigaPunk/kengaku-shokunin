#!/usr/bin/env python3
"""For each frozen mutant, the clause line the reference and the mutant print on the attributed killer."""
import importlib.util, json, pathlib, subprocess, sys

S = pathlib.Path(sys.argv[1]).resolve()
LANE = S / "lane"
W = S / "attack" / "notes"
W.mkdir(parents=True, exist_ok=True)
d = json.loads((S / "attack" / "work" / "attrib.json").read_text())


def load(p, n):
    sp = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


c = load(LANE / "plans/round38_c1_verify.py", "k38")
r37 = load(LANE / c.R37_REL, "k37")
gate_src = (LANE / r37.GATE_REL).read_text()
r36 = r37.load_r36(LANE)
ctx = r37.Ctx(LANE, r36)
fx = r37.r36_fixtures(r36) + r37.battery37_fixtures(LANE / r37.BATTERY_REL)
fx += c.battery38_fixtures(LANE / c.BATTERY38_REL)[0]
byfid = {f["fid"]: f for f in fx}
gdir = W / "gates"
gdir.mkdir(exist_ok=True)
(gdir / "ref.py").write_text(gate_src)


def lines(gate, argv):
    full = [sys.executable, str(gate), *argv] + ([] if "--spec" in argv else ["--spec", str(ctx.spec_path)])
    r = subprocess.run(full, capture_output=True, text=True)
    keep = [l for l in r.stdout.splitlines() if not l.startswith("defects=")]
    return r.returncode, keep


for mid, rec in d["mutants"].items():
    k = rec["killers"][0]
    f = byfid[k["fid"]]
    dd = W / mid
    dd.mkdir(exist_ok=True)
    argv = list(f["build"](ctx, dd))
    m = [x for x in c.MUTANTS if x[0] == mid][0]
    mg = gdir / f"{mid}.py"
    mg.write_text(gate_src.replace(m[4], m[5], 1))
    rrc, rl = lines(gdir / "ref.py", argv)
    mrc, ml = lines(mg, argv)
    print(f"== {mid} {rec['clause']} {rec['declared']} killer={k['fid']} dir={k['dir']}")
    print(f"   ref   rc={rrc} | " + " | ".join(rl))
    print(f"   mut   rc={mrc} | " + " | ".join(ml))

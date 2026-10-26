#!/usr/bin/env python3
"""Independent attack on the frozen round-38 C1 kill table.

Re-uses only the lane's fixture builders and the lane's own gate copies; adds what the counter does not
record: for every mutant, EVERY fixture that attributes a kill (in both directions), the gate rc, and
whether the mutant run died with a Python traceback (a crash is not the advertised behaviour).
"""
import importlib.util, json, pathlib, py_compile, re, subprocess, sys

S = pathlib.Path(sys.argv[1]).resolve()          # scratch dir
LANE = S / "lane"
WORK = S / "attack" / "work"
WORK.mkdir(parents=True, exist_ok=True)


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
fixtures = r37.r36_fixtures(r36) + r37.battery37_fixtures(LANE / r37.BATTERY_REL)
fixtures += c.battery38_fixtures(LANE / c.BATTERY38_REL)[0]

CL = re.compile(r"^(P\d+|D4|D5) (ok|DEFECT) ")
GATES = WORK / "gates"
GATES.mkdir(exist_ok=True)


def run(gate, argv):
    full = [sys.executable, str(gate), *argv] + ([] if "--spec" in argv else ["--spec", str(ctx.spec_path)])
    r = subprocess.run(full, capture_output=True, text=True, timeout=900)
    bad, ok = set(), set()
    for m in map(CL.match, r.stdout.splitlines()):
        if m:
            (bad if m.group(2) == "DEFECT" else ok).add(m.group(1))
    return {"rc": r.returncode, "bad": frozenset(bad), "ok": frozenset(ok),
            "tb": "Traceback (most recent call last)" in r.stderr}


# build fixtures exactly as the counter does
built = []
for i, fx in enumerate(fixtures):
    d = WORK / "fx" / f"f{i:03d}"
    if not d.exists():
        d.mkdir(parents=True)
        argv = list(fx["build"](ctx, d))
    else:
        argv = list(fx["build"](ctx, d))
    built.append((fx, d, argv))

ref_gate = GATES / "ref.py"
ref_gate.write_text(gate_src)
ref = [run(ref_gate, argv) for _fx, _d, argv in built]

out = {"fixtures": len(built), "mutants": {}}
for mid, clause, direction, label, old, new in c.MUTANTS:
    assert gate_src.count(old) == 1, mid
    mg = GATES / f"{mid}.py"
    mg.write_text(gate_src.replace(old, new, 1))
    py_compile.compile(str(mg), doraise=True, cfile=str(GATES / f"{mid}.pyc"))
    fam = c.FAMILY.get(clause, "package")
    rec = {"clause": clause, "declared": direction, "killers": [], "dirs": {}, "tb": []}
    for j, (fx, d, argv) in enumerate(built):
        if clause != "MAIN" and argv[0] != fam:
            continue
        mut = c.run_gate(mg, ctx.spec_path, argv)
        dirs = []
        if clause == "MAIN":
            if c.attributed(clause, direction, fx, argv, (ref[j]["rc"], ref[j]["bad"], ref[j]["ok"]), mut):
                dirs.append("main")
        else:
            for dn in ("silence", "mirror"):
                if c.attributed(clause, dn, fx, argv, (ref[j]["rc"], ref[j]["bad"], ref[j]["ok"]), mut):
                    dirs.append(dn)
        if not dirs:
            continue
        raw = run(mg, argv)
        rec["killers"].append({"fid": fx["fid"], "dir": dirs, "ref_rc": ref[j]["rc"], "mut_rc": mut[0],
                               "ref_bad": sorted(ref[j]["bad"]), "mut_bad": sorted(mut[1]),
                               "mut_ok": sorted(mut[2]), "traceback": raw["tb"],
                               "b38": fx.get("b38", False)})
        rec["dirs"][fx["fid"]] = dirs
        if raw["tb"]:
            rec["tb"].append(fx["fid"])
    out["mutants"][mid] = rec
    print(f"{mid} {clause} {direction} killers={len(rec['killers'])} tb={rec['tb']} "
          f"{[k['fid'] for k in rec['killers']][:6]}", flush=True)

(WORK / "attrib.json").write_text(json.dumps(out, indent=1))
print("FIXTURES", len(built))

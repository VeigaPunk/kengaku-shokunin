"""Run the genuine gate over each p6 fixture and print every clause it marks DEFECT (R37BatP6 evidence)."""
import importlib.util, pathlib, shutil, subprocess, sys

S = pathlib.Path(sys.argv[1])
lane = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
mod_path = lane / ".ufo/waves/round-37/build/R37BatP6/battery/p6.py"
sp = importlib.util.spec_from_file_location("p6", mod_path)
mod = importlib.util.module_from_spec(sp); sp.loader.exec_module(mod)
spec = importlib.util.spec_from_file_location("r36", lane / "plans/round36_c1_verify.py")
r36 = importlib.util.module_from_spec(spec); spec.loader.exec_module(r36)
sys.path.insert(0, str(lane / "plans"))
import round37_c1_verify as c1
ctx = c1.Ctx(lane, r36)
for fx in mod.FIXTURES:
    d = S / "one" / fx["fid"]
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    argv = list(fx["build"](ctx, d))
    r = subprocess.run([sys.executable, "plans/pkg_gate.py", *argv, "--spec", "plans/pkg-spec-r35.json"],
                       cwd=lane, capture_output=True, text=True)
    lines = r.stdout.splitlines()
    print(f"{fx['fid']} rc={r.returncode} defects_declared={','.join(fx['defects'])}")
    for l in lines:
        if " DEFECT " in l:
            print("   " + l)
    print("   " + lines[-1])

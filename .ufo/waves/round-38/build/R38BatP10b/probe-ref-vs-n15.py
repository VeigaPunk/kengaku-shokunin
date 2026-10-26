import importlib.util, pathlib, subprocess, sys, hashlib, shutil
S = pathlib.Path("/fast/scratch/hyaku/kengaku-r38/R38BatP10b")
lane = S / "lane"
def load(p, n):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
r37 = load(lane / "plans/round37_c1_verify.py", "r37")
r36 = r37.load_r36(lane); ctx = r37.Ctx(lane, r36)
mod = load(pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-38/build/R38BatP10b/battery/p10b.py"), "p10b")
d = S / "manual" / "fx"; shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
argv = list(mod.FIXTURES[0]["build"](ctx, d))
print("ARGV", argv)
gsrc = (lane / "plans/pkg_gate.py").read_text()
old, new = 'return True, f"probe_rerun=byte-equal', 'return False, f"probe_rerun=byte-equal'
assert gsrc.count(old) == 1
mut = S / "manual" / "N15.py"; mut.write_text(gsrc.replace(old, new, 1))
for label, gate in (("REF", lane / "plans/pkg_gate.py"), ("REF2", lane / "plans/pkg_gate.py"), ("N15", mut)):
    r = subprocess.run([sys.executable, str(gate), *argv], capture_output=True, text=True)
    print(f"--- {label} rc={r.returncode}")
    for line in r.stdout.splitlines():
        if line.startswith("P10") or "DEFECT" in line or line.startswith("defects="):
            print("   ", line)
    if r.stderr.strip():
        print("    STDERR", r.stderr.strip()[:200])
print("RECEIPT", repr((d / "corpus/evidence/round35/tb2-grader-probe.txt").read_text()))
print("SPEC_SHA", hashlib.sha256((d / "p10b-spec.json").read_bytes()).hexdigest())

import importlib.util, pathlib, sys
S = pathlib.Path("/fast/scratch/hyaku/kengaku-r46/R46ExecC3Counter"); L = S / "lane"
spec = importlib.util.spec_from_file_location("c3", str(L / "plans/dev_pinned_c3_verify.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
work = S / "work-pos"; work.mkdir(parents=True, exist_ok=True)
pkg = m.real_pkg(L)
legs = ("V1", "V3", "V4", "V5", "V6", "V7", "V9", "V10", "V11", "V12", "V13")
res = m.run_legs(L, pkg, work, legs)
d = sum(1 for _n, ok, _x in res if not ok)
print(f"DEV POSITIVE checks={len(res)} defects={d}")
print("DEV POSITIVE", "all-ok" if d == 0 else "DEFECTS")
